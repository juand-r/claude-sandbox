/*
 * optimizer.c - Adam optimizer with FP32 master weights
 *
 * Standard AdamW: decoupled weight decay applied separately.
 * m = beta1*m + (1-beta1)*grad
 * v = beta2*v + (1-beta2)*grad^2
 * m_hat = m / (1 - beta1^step)
 * v_hat = v / (1 - beta2^step)
 * param -= lr * (m_hat / (sqrt(v_hat) + eps) + weight_decay * param)
 */

#include "qat_cpu.h"

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

void adam_step(Adam *opt) {
    opt->config.step++;

    float beta1 = opt->config.beta1;
    float beta2 = opt->config.beta2;
    float lr = opt->config.lr;
    float eps = opt->config.eps;
    float wd = opt->config.weight_decay;
    int step = opt->config.step;

    /* Bias correction factors */
    float bc1 = 1.0f - powf(beta1, (float)step);
    float bc2 = 1.0f - powf(beta2, (float)step);

    for (int p = 0; p < opt->n_params; p++) {
        AdamParam *param = &opt->params[p];
        int n = param->numel;

        for (int i = 0; i < n; i++) {
            float g = param->grad[i];

            /* Update moments */
            param->m[i] = beta1 * param->m[i] + (1.0f - beta1) * g;
            param->v[i] = beta2 * param->v[i] + (1.0f - beta2) * g * g;

            /* Bias-corrected moments */
            float m_hat = param->m[i] / bc1;
            float v_hat = param->v[i] / bc2;

            /* AdamW update: weight decay applied to param directly */
            param->param[i] -= lr * (m_hat / (sqrtf(v_hat) + eps) +
                                     wd * param->param[i]);
        }
    }
}

void adam_zero_grad(Adam *opt) {
    for (int p = 0; p < opt->n_params; p++) {
        memset(opt->params[p].grad, 0, opt->params[p].numel * sizeof(float));
    }
}
