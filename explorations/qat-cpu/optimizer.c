/*
 * optimizer.c - Adam optimizer with FP32 master weights
 *
 * Standard AdamW: decoupled weight decay applied separately.
 * m = beta1*m + (1-beta1)*grad
 * v = beta2*v + (1-beta2)*grad^2
 * m_hat = m / (1 - beta1^step)
 * v_hat = v / (1 - beta2^step)
 * param -= lr * (m_hat / (sqrt(v_hat) + eps) + weight_decay * param)
 *
 * Hot loop vectorized with AVX-512 (runtime dispatch).
 */

#include "qat_cpu.h"
#include <immintrin.h>

Adam *adam_create(float lr, float beta1, float beta2, float eps,
                 float weight_decay) {
    Adam *opt = (Adam *)calloc(1, sizeof(Adam));
    if (!opt) return NULL;

    opt->config.lr = lr;
    opt->config.beta1 = beta1;
    opt->config.beta2 = beta2;
    opt->config.eps = eps;
    opt->config.weight_decay = weight_decay;
    opt->config.step = 0;

    opt->n_params = 0;
    opt->capacity = 16;
    opt->params = (AdamParam *)calloc(opt->capacity, sizeof(AdamParam));

    return opt;
}

void adam_free(Adam *opt) {
    if (!opt) return;
    for (int i = 0; i < opt->n_params; i++) {
        qat_free(opt->params[i].m);
        qat_free(opt->params[i].v);
    }
    free(opt->params);
    free(opt);
}

void adam_add_param(Adam *opt, float *param, float *grad, int numel) {
    if (opt->n_params >= opt->capacity) {
        opt->capacity *= 2;
        opt->params = (AdamParam *)realloc(opt->params,
                                            opt->capacity * sizeof(AdamParam));
    }

    AdamParam *p = &opt->params[opt->n_params];
    p->param = param;
    p->grad = grad;
    p->numel = numel;
    p->m = (float *)qat_calloc(numel * sizeof(float));
    p->v = (float *)qat_calloc(numel * sizeof(float));

    opt->n_params++;
}

/*
 * AVX-512 vectorized AdamW step for a single parameter group.
 *
 * Processes 16 floats per iteration. All 4 arrays (param, grad, m, v)
 * are read/written in one pass for cache efficiency.
 */
__attribute__((target("avx512f")))
static void adam_step_avx512(float *param, const float *grad, float *m, float *v,
                              int n, float beta1, float beta2,
                              float one_minus_b1, float one_minus_b2,
                              float lr, float eps, float wd,
                              float inv_bc1, float inv_bc2) {
    __m512 vb1   = _mm512_set1_ps(beta1);
    __m512 vb2   = _mm512_set1_ps(beta2);
    __m512 v1mb1 = _mm512_set1_ps(one_minus_b1);
    __m512 v1mb2 = _mm512_set1_ps(one_minus_b2);
    __m512 vlr   = _mm512_set1_ps(lr);
    __m512 veps  = _mm512_set1_ps(eps);
    __m512 vwd   = _mm512_set1_ps(wd);
    __m512 vibc1 = _mm512_set1_ps(inv_bc1);
    __m512 vibc2 = _mm512_set1_ps(inv_bc2);

    int i = 0;
    for (; i + 16 <= n; i += 16) {
        __m512 g = _mm512_loadu_ps(grad + i);
        __m512 mi = _mm512_loadu_ps(m + i);
        __m512 vi = _mm512_loadu_ps(v + i);
        __m512 pi = _mm512_loadu_ps(param + i);

        /* m = beta1*m + (1-beta1)*g */
        mi = _mm512_fmadd_ps(vb1, mi, _mm512_mul_ps(v1mb1, g));
        /* v = beta2*v + (1-beta2)*g*g */
        vi = _mm512_fmadd_ps(vb2, vi, _mm512_mul_ps(v1mb2, _mm512_mul_ps(g, g)));

        _mm512_storeu_ps(m + i, mi);
        _mm512_storeu_ps(v + i, vi);

        /* m_hat = m * inv_bc1,  v_hat = v * inv_bc2 */
        __m512 m_hat = _mm512_mul_ps(mi, vibc1);
        __m512 v_hat = _mm512_mul_ps(vi, vibc2);

        /* update = m_hat / (sqrt(v_hat) + eps) + wd * param */
        __m512 denom = _mm512_add_ps(_mm512_sqrt_ps(v_hat), veps);
        __m512 update = _mm512_add_ps(_mm512_div_ps(m_hat, denom),
                                       _mm512_mul_ps(vwd, pi));

        /* param -= lr * update */
        pi = _mm512_fnmadd_ps(vlr, update, pi);
        _mm512_storeu_ps(param + i, pi);
    }

    /* Scalar tail */
    for (; i < n; i++) {
        float g = grad[i];
        m[i] = beta1 * m[i] + one_minus_b1 * g;
        v[i] = beta2 * v[i] + one_minus_b2 * g * g;
        float m_hat = m[i] * inv_bc1;
        float v_hat = v[i] * inv_bc2;
        param[i] -= lr * (m_hat / (sqrtf(v_hat) + eps) + wd * param[i]);
    }
}

void adam_step(Adam *opt) {
    opt->config.step++;

    float beta1 = opt->config.beta1;
    float beta2 = opt->config.beta2;
    float lr = opt->config.lr;
    float eps = opt->config.eps;
    float wd = opt->config.weight_decay;
    int step = opt->config.step;

    float one_minus_b1 = 1.0f - beta1;
    float one_minus_b2 = 1.0f - beta2;

    /* Bias correction: multiply by 1/bc instead of dividing each element */
    float bc1 = 1.0f - powf(beta1, (float)step);
    float bc2 = 1.0f - powf(beta2, (float)step);
    float inv_bc1 = 1.0f / bc1;
    float inv_bc2 = 1.0f / bc2;

    int use_avx512 = __builtin_cpu_supports("avx512f");

    for (int p = 0; p < opt->n_params; p++) {
        AdamParam *param = &opt->params[p];

        if (use_avx512) {
            adam_step_avx512(param->param, param->grad, param->m, param->v,
                              param->numel, beta1, beta2,
                              one_minus_b1, one_minus_b2,
                              lr, eps, wd, inv_bc1, inv_bc2);
        } else {
            int n = param->numel;
            for (int i = 0; i < n; i++) {
                float g = param->grad[i];
                param->m[i] = beta1 * param->m[i] + one_minus_b1 * g;
                param->v[i] = beta2 * param->v[i] + one_minus_b2 * g * g;
                float m_hat = param->m[i] * inv_bc1;
                float v_hat = param->v[i] * inv_bc2;
                param->param[i] -= lr * (m_hat / (sqrtf(v_hat) + eps) +
                                         wd * param->param[i]);
            }
        }
    }
}

void adam_zero_grad(Adam *opt) {
    for (int p = 0; p < opt->n_params; p++) {
        memset(opt->params[p].grad, 0, opt->params[p].numel * sizeof(float));
    }
}
