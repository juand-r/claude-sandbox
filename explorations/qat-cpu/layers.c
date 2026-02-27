/*
 * layers.c - Transformer components
 *
 * RMSNorm, GeLU, SiLU, Softmax, Attention, TransformerBlock.
 * All FP32 (except projections which go through QATLinear).
 */

#include "qat_cpu.h"
#include <immintrin.h>
#include <omp.h>

/* ========================================================================
 * RMSNorm: y = x * weight / rms(x), rms(x) = sqrt(mean(x^2) + eps)
 * ======================================================================== */

RMSNorm *rmsnorm_create(int dim, float eps) {
    RMSNorm *layer = (RMSNorm *)calloc(1, sizeof(RMSNorm));
    if (!layer) return NULL;

    layer->dim = dim;
    layer->eps = eps;

    /* Initialize weight to ones */
    layer->weight = tensor_create(1, dim);
    tensor_fill(layer->weight, 1.0f);

    layer->grad_weight = tensor_zeros(1, dim);
    layer->saved_input = NULL;
    layer->saved_rms = NULL;

    return layer;
}

void rmsnorm_free(RMSNorm *layer) {
    if (!layer) return;
    tensor_free(layer->weight);
    tensor_free(layer->grad_weight);
    tensor_free(layer->saved_input);
    qat_free(layer->saved_rms);
    free(layer);
}

Tensor *rmsnorm_forward(RMSNorm *layer, const Tensor *input) {
    int batch = input->rows;
    int dim = layer->dim;

    /* Save input for backward */
    if (layer->saved_input) tensor_free(layer->saved_input);
    layer->saved_input = tensor_create(batch, dim);
    tensor_copy(layer->saved_input, input);

    /* Save RMS values */
    if (layer->saved_rms) qat_free(layer->saved_rms);
    layer->saved_rms = (float *)qat_alloc(batch * sizeof(float));

    Tensor *output = tensor_create(batch, dim);

    for (int i = 0; i < batch; i++) {
        /* Compute mean(x^2) */
        float sum_sq = 0.0f;
        for (int j = 0; j < dim; j++) {
            float x = input->data[i * dim + j];
            sum_sq += x * x;
        }
        float rms = sqrtf(sum_sq / (float)dim + layer->eps);
        layer->saved_rms[i] = rms;

        /* Normalize and scale */
        float inv_rms = 1.0f / rms;
        for (int j = 0; j < dim; j++) {
            output->data[i * dim + j] =
                input->data[i * dim + j] * inv_rms * layer->weight->data[j];
        }
    }

    return output;
}

Tensor *rmsnorm_backward(RMSNorm *layer, const Tensor *grad_output) {
    int batch = grad_output->rows;
    int dim = layer->dim;
    const float *x = layer->saved_input->data;
    const float *w = layer->weight->data;

    Tensor *grad_input = tensor_create(batch, dim);

    for (int i = 0; i < batch; i++) {
        float rms = layer->saved_rms[i];
        float inv_rms = 1.0f / rms;
        /*
         * y_j = x_j * w_j / rms
         * dy/dx_j = w_j / rms - x_j * w * x * (1/dim) / rms^3
         *
         * More precisely:
         *   d(rms)/d(x_j) = x_j / (dim * rms)
         *   dy_k/dx_j = delta(k,j) * w_k / rms - y_k * x_j / (dim * rms^2)
         *
         * grad_input[j] = sum_k grad_output[k] * dy_k/dx_j
         *               = grad_output[j] * w[j] / rms
         *                 - (x[j] / (dim * rms^2)) * sum_k (grad_output[k] * y_k)
         *
         * where y_k = x[k] * w[k] / rms
         */

        /* Compute sum_k (grad_output[k] * x[k] * w[k] / rms) */
        float dot = 0.0f;
        for (int j = 0; j < dim; j++) {
            float y_j = x[i * dim + j] * w[j] * inv_rms;
            dot += grad_output->data[i * dim + j] * y_j;
        }

        for (int j = 0; j < dim; j++) {
            float go = grad_output->data[i * dim + j];
            float xj = x[i * dim + j];
            grad_input->data[i * dim + j] =
                go * w[j] * inv_rms -
                xj * dot * inv_rms * inv_rms / (float)dim;
        }

        /* Accumulate grad_weight */
        for (int j = 0; j < dim; j++) {
            float go = grad_output->data[i * dim + j];
            float xj = x[i * dim + j];
            layer->grad_weight->data[j] += go * xj * inv_rms;
        }
    }

    return grad_input;
}

void rmsnorm_zero_grad(RMSNorm *layer) {
    if (layer->grad_weight) {
        memset(layer->grad_weight->data, 0, tensor_bytes(layer->grad_weight));
    }
}

/* ========================================================================
 * GeLU: x * 0.5 * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
 *
 * AVX-512 vectorized with fast polynomial tanh approximation.
 * tanh(x) ≈ x * (c0 + c2*x^2 + c4*x^4) / (c0 + d2*x^2 + d4*x^4)
 * Accurate to ~5e-5 in [-4.5, 4.5], clamped to ±1 outside.
 * (Padé [4/4] approximant fitted to tanh.)
 * ======================================================================== */

static const float GELU_SQRT_2_PI = 0.7978845608028654f;  /* sqrt(2/pi) */
static const float GELU_COEFF = 0.044715f;

/*
 * Fast tanh approximation using rational polynomial.
 * tanh(x) = x * P(x^2) / Q(x^2) where:
 *   P(z) = 135135 + 17325*z + 378*z^2 + z^3
 *   Q(z) = 135135 + 62370*z + 3150*z^2 + 28*z^3
 * (Padé [7/7] coefficients for tanh, reduced to [6/6] in x.)
 * Clamp input to [-9, 9] where tanh is ±1 to within float precision.
 */
static inline float fast_tanh(float x) {
    if (x > 9.0f) return 1.0f;
    if (x < -9.0f) return -1.0f;
    float x2 = x * x;
    float p = 135135.0f + x2 * (17325.0f + x2 * (378.0f + x2));
    float q = 135135.0f + x2 * (62370.0f + x2 * (3150.0f + x2 * 28.0f));
    return x * p / q;
}

/*
 * AVX-512 vectorized fast_tanh for 16 floats at once.
 * Same rational polynomial, clamped to [-1, 1].
 */
__attribute__((target("avx512f")))
static inline __m512 fast_tanh_avx512(__m512 x) {
    __m512 x2 = _mm512_mul_ps(x, x);

    /* P(x^2) = 135135 + x^2*(17325 + x^2*(378 + x^2)) */
    __m512 p = _mm512_fmadd_ps(x2, _mm512_set1_ps(1.0f),
               _mm512_set1_ps(378.0f));
    p = _mm512_fmadd_ps(x2, p, _mm512_set1_ps(17325.0f));
    p = _mm512_fmadd_ps(x2, p, _mm512_set1_ps(135135.0f));

    /* Q(x^2) = 135135 + x^2*(62370 + x^2*(3150 + x^2*28)) */
    __m512 q = _mm512_fmadd_ps(x2, _mm512_set1_ps(28.0f),
               _mm512_set1_ps(3150.0f));
    q = _mm512_fmadd_ps(x2, q, _mm512_set1_ps(62370.0f));
    q = _mm512_fmadd_ps(x2, q, _mm512_set1_ps(135135.0f));

    /* tanh = x * P / Q, clamped to [-1, 1] */
    __m512 result = _mm512_mul_ps(x, _mm512_div_ps(p, q));
    result = _mm512_min_ps(result, _mm512_set1_ps(1.0f));
    result = _mm512_max_ps(result, _mm512_set1_ps(-1.0f));
    return result;
}

__attribute__((target("avx512f")))
static void gelu_forward_avx512(const float *input, float *output, int n) {
    __m512 vc = _mm512_set1_ps(GELU_SQRT_2_PI);
    __m512 va = _mm512_set1_ps(GELU_COEFF);
    __m512 vhalf = _mm512_set1_ps(0.5f);
    __m512 vone = _mm512_set1_ps(1.0f);

    int i = 0;
    for (; i + 16 <= n; i += 16) {
        __m512 x = _mm512_loadu_ps(input + i);
        /* inner = sqrt(2/pi) * (x + 0.044715 * x^3) */
        __m512 x3 = _mm512_mul_ps(x, _mm512_mul_ps(x, x));
        __m512 inner = _mm512_mul_ps(vc, _mm512_fmadd_ps(va, x3, x));
        __m512 t = fast_tanh_avx512(inner);
        /* output = 0.5 * x * (1 + tanh) */
        __m512 out = _mm512_mul_ps(vhalf, _mm512_mul_ps(x, _mm512_add_ps(vone, t)));
        _mm512_storeu_ps(output + i, out);
    }
    /* Scalar tail */
    for (; i < n; i++) {
        float x = input[i];
        float inner = GELU_SQRT_2_PI * (x + GELU_COEFF * x * x * x);
        float t = fast_tanh(inner);
        output[i] = 0.5f * x * (1.0f + t);
    }
}

void gelu_forward(const float *input, float *output, int n) {
    if (__builtin_cpu_supports("avx512f")) {
        gelu_forward_avx512(input, output, n);
        return;
    }
    for (int i = 0; i < n; i++) {
        float x = input[i];
        float inner = GELU_SQRT_2_PI * (x + GELU_COEFF * x * x * x);
        float t = fast_tanh(inner);
        output[i] = 0.5f * x * (1.0f + t);
    }
}

/*
 * GeLU backward:
 *   d/dx [0.5 * x * (1 + tanh(c*(x + a*x^3)))]
 *   = 0.5 * (1 + tanh(inner)) + 0.5 * x * sech^2(inner) * c * (1 + 3*a*x^2)
 *   where c = sqrt(2/pi), a = 0.044715, inner = c*(x + a*x^3)
 */
__attribute__((target("avx512f")))
static void gelu_backward_avx512(const float *input, const float *grad_output,
                                  float *grad_input, int n) {
    __m512 vc = _mm512_set1_ps(GELU_SQRT_2_PI);
    __m512 va = _mm512_set1_ps(GELU_COEFF);
    __m512 v3a = _mm512_set1_ps(3.0f * GELU_COEFF);
    __m512 vhalf = _mm512_set1_ps(0.5f);
    __m512 vone = _mm512_set1_ps(1.0f);

    int i = 0;
    for (; i + 16 <= n; i += 16) {
        __m512 x = _mm512_loadu_ps(input + i);
        __m512 go = _mm512_loadu_ps(grad_output + i);
        __m512 x2 = _mm512_mul_ps(x, x);
        __m512 x3 = _mm512_mul_ps(x2, x);

        /* inner = c * (x + a*x^3) */
        __m512 inner = _mm512_mul_ps(vc, _mm512_fmadd_ps(va, x3, x));
        __m512 t = fast_tanh_avx512(inner);
        __m512 sech2 = _mm512_fnmadd_ps(t, t, vone);  /* 1 - t*t */

        /* d_inner = c * (1 + 3*a*x^2) */
        __m512 d_inner = _mm512_mul_ps(vc, _mm512_fmadd_ps(v3a, x2, vone));

        /* grad = 0.5*(1+t) + 0.5*x*sech2*d_inner */
        __m512 term1 = _mm512_mul_ps(vhalf, _mm512_add_ps(vone, t));
        __m512 term2 = _mm512_mul_ps(vhalf, _mm512_mul_ps(x, _mm512_mul_ps(sech2, d_inner)));
        __m512 grad = _mm512_add_ps(term1, term2);

        _mm512_storeu_ps(grad_input + i, _mm512_mul_ps(go, grad));
    }
    for (; i < n; i++) {
        float x = input[i];
        float inner = GELU_SQRT_2_PI * (x + GELU_COEFF * x * x * x);
        float t = fast_tanh(inner);
        float sech2 = 1.0f - t * t;
        float d_inner = GELU_SQRT_2_PI * (1.0f + 3.0f * GELU_COEFF * x * x);
        float grad = 0.5f * (1.0f + t) + 0.5f * x * sech2 * d_inner;
        grad_input[i] = grad_output[i] * grad;
    }
}

void gelu_backward(const float *input, const float *grad_output,
                   float *grad_input, int n) {
    if (__builtin_cpu_supports("avx512f")) {
        gelu_backward_avx512(input, grad_output, grad_input, n);
        return;
    }
    for (int i = 0; i < n; i++) {
        float x = input[i];
        float inner = GELU_SQRT_2_PI * (x + GELU_COEFF * x * x * x);
        float t = fast_tanh(inner);
        float sech2 = 1.0f - t * t;
        float d_inner = GELU_SQRT_2_PI * (1.0f + 3.0f * GELU_COEFF * x * x);
        float grad = 0.5f * (1.0f + t) + 0.5f * x * sech2 * d_inner;
        grad_input[i] = grad_output[i] * grad;
    }
}

/* ========================================================================
 * SiLU: x * sigmoid(x)
 * ======================================================================== */

void silu_forward(const float *input, float *output, int n) {
    for (int i = 0; i < n; i++) {
        float x = input[i];
        float sig = 1.0f / (1.0f + expf(-x));
        output[i] = x * sig;
    }
}

/*
 * SiLU backward: d/dx [x * sigmoid(x)] = sigmoid(x) + x * sigmoid(x) * (1 - sigmoid(x))
 *              = sigmoid(x) * (1 + x * (1 - sigmoid(x)))
 */
void silu_backward(const float *input, const float *grad_output,
                   float *grad_input, int n) {
    for (int i = 0; i < n; i++) {
        float x = input[i];
        float sig = 1.0f / (1.0f + expf(-x));
        float grad = sig * (1.0f + x * (1.0f - sig));
        grad_input[i] = grad_output[i] * grad;
    }
}

/* ========================================================================
 * Softmax (numerically stable, per-row)
 * ======================================================================== */

void softmax_forward(const float *input, float *output, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        /* Find max for numerical stability */
        float max_val = input[i * cols];
        for (int j = 1; j < cols; j++) {
            float v = input[i * cols + j];
            if (v > max_val) max_val = v;
        }

        /* Compute exp and sum */
        float sum_exp = 0.0f;
        for (int j = 0; j < cols; j++) {
            float e = expf(input[i * cols + j] - max_val);
            output[i * cols + j] = e;
            sum_exp += e;
        }

        /* Normalize */
        float inv_sum = 1.0f / sum_exp;
        for (int j = 0; j < cols; j++) {
            output[i * cols + j] *= inv_sum;
        }
    }
}

/*
 * Softmax backward:
 *   d(softmax_i)/d(logit_j) = softmax_i * (delta_ij - softmax_j)
 *   grad_input[j] = sum_i (grad_output[i] * softmax[i] * (delta_ij - softmax[j]))
 *                 = softmax[j] * (grad_output[j] - sum_i(grad_output[i] * softmax[i]))
 */
void softmax_backward(const float *output, const float *grad_output,
                      float *grad_input, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        /* Compute dot product: sum(grad_output * softmax) */
        float dot = 0.0f;
        for (int j = 0; j < cols; j++) {
            dot += grad_output[i * cols + j] * output[i * cols + j];
        }

        /* grad_input = softmax * (grad_output - dot) */
        for (int j = 0; j < cols; j++) {
            grad_input[i * cols + j] =
                output[i * cols + j] * (grad_output[i * cols + j] - dot);
        }
    }
}

/* ========================================================================
 * Attention
 *
 * Multi-head attention with QATLinear for Q/K/V/O projections.
 * For simplicity, this implements single-sequence attention (no KV cache).
 *
 * input: [seq_len x dim]
 * Q = input * Wq: [seq_len x dim]
 * K = input * Wk: [seq_len x dim]
 * V = input * Wv: [seq_len x dim]
 * attn = softmax(Q * K^T / sqrt(head_dim)): [n_heads x seq_len x seq_len]
 * out = attn * V: [seq_len x dim]
 * output = out * Wo: [seq_len x dim]
 * ======================================================================== */

Attention *attention_create(int dim, int n_heads,
                            const KernelDispatch *kd, uint64_t *rng_state) {
    Attention *attn = (Attention *)calloc(1, sizeof(Attention));
    if (!attn) return NULL;

    attn->dim = dim;
    attn->n_heads = n_heads;
    attn->head_dim = dim / n_heads;

    attn->causal = false;  /* Default: full attention (no mask) */
    attn->kernels = kd;

    attn->wq = qat_linear_create(dim, dim, false, kd, rng_state);
    attn->wk = qat_linear_create(dim, dim, false, kd, rng_state);
    attn->wv = qat_linear_create(dim, dim, false, kd, rng_state);
    attn->wo = qat_linear_create(dim, dim, false, kd, rng_state);

    return attn;
}

void attention_free(Attention *attn) {
    if (!attn) return;
    qat_linear_free(attn->wq);
    qat_linear_free(attn->wk);
    qat_linear_free(attn->wv);
    qat_linear_free(attn->wo);
    tensor_free(attn->saved_q);
    tensor_free(attn->saved_k);
    tensor_free(attn->saved_v);
    tensor_free(attn->saved_attn);
    free(attn);
}

/*
 * Helper: extract head slice from interleaved [seq x dim] to contiguous [seq x head_dim].
 * src[s][h*head_dim + d] -> dst[s * head_dim + d]
 */
static void extract_head(const float *src, int seq_len, int dim,
                          int head_dim, int h, float *dst) {
    for (int s = 0; s < seq_len; s++) {
        memcpy(&dst[s * head_dim],
               &src[s * dim + h * head_dim],
               head_dim * sizeof(float));
    }
}

/*
 * Helper: scatter head slice from contiguous [seq x head_dim] back to interleaved [seq x dim].
 * src[s * head_dim + d] -> dst[s][h*head_dim + d]
 */
static void scatter_head(const float *src, int seq_len, int dim,
                          int head_dim, int h, float *dst) {
    for (int s = 0; s < seq_len; s++) {
        memcpy(&dst[s * dim + h * head_dim],
               &src[s * head_dim],
               head_dim * sizeof(float));
    }
}

/*
 * Helper: transpose [rows x cols] -> [cols x rows].
 */
static void transpose_fp32(const float *src, int rows, int cols, float *dst) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            dst[j * rows + i] = src[i * cols + j];
        }
    }
}

/*
 * Attention forward with mini-batch support.
 *
 * input: [batch_size * seq_len, dim]
 * Q/K/V projections operate on the full flattened tensor (batch-agnostic).
 * Attention scores are computed per-sequence to avoid cross-sequence attention.
 * Output: [batch_size * seq_len, dim]
 */
Tensor *attention_forward(Attention *attn, const Tensor *input,
                          int batch_size, int seq_len) {
    int dim = attn->dim;
    int n_heads = attn->n_heads;
    int head_dim = attn->head_dim;
    int total_tokens = batch_size * seq_len;
    float scale = 1.0f / sqrtf((float)head_dim);
    gemm_fp32_fn gemm = attn->kernels->fp32_gemm;

    /* Q, K, V projections via QATLinear — operates on [B*S, dim] */
    Tensor *q = qat_linear_forward(attn->wq, input);
    Tensor *k = qat_linear_forward(attn->wk, input);
    Tensor *v = qat_linear_forward(attn->wv, input);

    /* Save for backward */
    if (attn->saved_q) tensor_free(attn->saved_q);
    if (attn->saved_k) tensor_free(attn->saved_k);
    if (attn->saved_v) tensor_free(attn->saved_v);
    attn->saved_q = tensor_create(total_tokens, dim);
    attn->saved_k = tensor_create(total_tokens, dim);
    attn->saved_v = tensor_create(total_tokens, dim);
    tensor_copy(attn->saved_q, q);
    tensor_copy(attn->saved_k, k);
    tensor_copy(attn->saved_v, v);

    /* Saved attention weights: [batch * n_heads * seq_len, seq_len] */
    if (attn->saved_attn) tensor_free(attn->saved_attn);
    attn->saved_attn = tensor_create(batch_size * n_heads * seq_len, seq_len);

    Tensor *attn_out = tensor_zeros(total_tokens, dim);

    /* Per-head, per-sequence buffers */
    float *q_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
    float *k_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
    float *k_h_t = (float *)qat_alloc(head_dim * seq_len * sizeof(float));
    float *v_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
    float *scores = (float *)qat_alloc(seq_len * seq_len * sizeof(float));
    float *attn_w = (float *)qat_alloc(seq_len * seq_len * sizeof(float));
    float *out_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));

    for (int b = 0; b < batch_size; b++) {
        /* Pointer to this sequence's Q/K/V data: [seq_len, dim] slice */
        float *q_b = &q->data[b * seq_len * dim];
        float *k_b = &k->data[b * seq_len * dim];
        float *v_b = &v->data[b * seq_len * dim];
        float *out_b = &attn_out->data[b * seq_len * dim];

        for (int h = 0; h < n_heads; h++) {
            /* Extract contiguous per-head slices from this sequence */
            extract_head(q_b, seq_len, dim, head_dim, h, q_h);
            extract_head(k_b, seq_len, dim, head_dim, h, k_h);
            extract_head(v_b, seq_len, dim, head_dim, h, v_h);

            /* K_h^T: [seq x hd] -> [hd x seq] */
            transpose_fp32(k_h, seq_len, head_dim, k_h_t);

            /* scores[seq x seq] = Q_h * K_h^T * scale */
            gemm(seq_len, seq_len, head_dim,
                 scale,
                 q_h, head_dim,
                 k_h_t, seq_len,
                 0.0f,
                 scores, seq_len);

            /* Causal mask (within this sequence only) */
            if (attn->causal) {
                for (int s1 = 0; s1 < seq_len; s1++) {
                    for (int s2 = s1 + 1; s2 < seq_len; s2++) {
                        scores[s1 * seq_len + s2] = -1e9f;
                    }
                }
            }

            /* Softmax */
            softmax_forward(scores, attn_w, seq_len, seq_len);

            /* Save attention weights: index by (b * n_heads + h) */
            int attn_idx = (b * n_heads + h) * seq_len * seq_len;
            memcpy(&attn->saved_attn->data[attn_idx],
                   attn_w, seq_len * seq_len * sizeof(float));

            /* out_h[seq x hd] = attn_w[seq x seq] * V_h[seq x hd] */
            gemm(seq_len, head_dim, seq_len,
                 1.0f,
                 attn_w, seq_len,
                 v_h, head_dim,
                 0.0f,
                 out_h, head_dim);

            /* Scatter back to interleaved output for this sequence */
            scatter_head(out_h, seq_len, dim, head_dim, h, out_b);
        }
    }

    qat_free(q_h);
    qat_free(k_h);
    qat_free(k_h_t);
    qat_free(v_h);
    qat_free(scores);
    qat_free(attn_w);
    qat_free(out_h);
    tensor_free(q);
    tensor_free(k);
    tensor_free(v);

    /* Output projection — operates on [B*S, dim] */
    Tensor *output = qat_linear_forward(attn->wo, attn_out);

    tensor_free(attn_out);

    return output;
}

/*
 * Attention backward pass.
 * Reverse the forward operations, using GEMM for per-head computations.
 *
 * Forward was:
 *   scores_h = Q_h * K_h^T * scale    [seq x seq]
 *   attn_w   = softmax(scores_h)      [seq x seq]
 *   out_h    = attn_w * V_h           [seq x hd]
 *
 * Backward:
 *   grad_attn_w = grad_out_h * V_h^T          [seq x seq] = [seq x hd] * [hd x seq]
 *   grad_V_h    = attn_w^T * grad_out_h       [seq x hd]  = [seq x seq] * [seq x hd]
 *   grad_scores = softmax_backward(attn_w, grad_attn_w)
 *   grad_Q_h    = grad_scores * K_h * scale   [seq x hd]  = [seq x seq] * [seq x hd]
 *   grad_K_h    = grad_scores^T * Q_h * scale [seq x hd]  = [seq x seq] * [seq x hd]
 */
/*
 * Attention backward with mini-batch support.
 * Mirrors the forward: Q/K/V backward on full [B*S, dim], attention per-sequence.
 *
 * The (b,h) loop is parallelized with OpenMP — each thread gets private workspace.
 * Inner GEMMs run single-threaded (nested parallelism disabled by default).
 */
Tensor *attention_backward(Attention *attn, const Tensor *grad_output,
                           int batch_size, int seq_len) {
    int dim = attn->dim;
    int n_heads = attn->n_heads;
    int head_dim = attn->head_dim;
    int total_tokens = batch_size * seq_len;
    float scale = 1.0f / sqrtf((float)head_dim);
    gemm_fp32_fn gemm = attn->kernels->fp32_gemm;

    /* Backward through output projection — [B*S, dim] */
    Tensor *grad_attn_out = qat_linear_backward(attn->wo, grad_output);

    /* Allocate gradient tensors for Q, K, V — full [B*S, dim] */
    Tensor *grad_q = tensor_zeros(total_tokens, dim);
    Tensor *grad_k = tensor_zeros(total_tokens, dim);
    Tensor *grad_v = tensor_zeros(total_tokens, dim);

    int total_iters = batch_size * n_heads;

    #pragma omp parallel
    {
        /* Per-thread workspace */
        float *go_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
        float *v_h  = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
        float *v_h_t = (float *)qat_alloc(head_dim * seq_len * sizeof(float));
        float *q_h  = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
        float *k_h  = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
        float *grad_attn_w  = (float *)qat_alloc(seq_len * seq_len * sizeof(float));
        float *grad_scores  = (float *)qat_alloc(seq_len * seq_len * sizeof(float));
        float *grad_scores_t = (float *)qat_alloc(seq_len * seq_len * sizeof(float));
        float *gq_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
        float *gk_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
        float *gv_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));

        #pragma omp for schedule(static)
        for (int bh = 0; bh < total_iters; bh++) {
            int b = bh / n_heads;
            int h = bh % n_heads;
            int off = b * seq_len * dim;
            int attn_idx = (b * n_heads + h) * seq_len * seq_len;
            const float *attn_w = &attn->saved_attn->data[attn_idx];

            /* Extract contiguous per-head slices for this sequence */
            extract_head(&grad_attn_out->data[off], seq_len, dim, head_dim, h, go_h);
            extract_head(&attn->saved_v->data[off], seq_len, dim, head_dim, h, v_h);
            extract_head(&attn->saved_q->data[off], seq_len, dim, head_dim, h, q_h);
            extract_head(&attn->saved_k->data[off], seq_len, dim, head_dim, h, k_h);

            /* grad_attn_w = grad_out_h * V_h^T */
            transpose_fp32(v_h, seq_len, head_dim, v_h_t);
            gemm(seq_len, seq_len, head_dim,
                 1.0f, go_h, head_dim, v_h_t, seq_len,
                 0.0f, grad_attn_w, seq_len);

            /* grad_V_h = attn_w^T * grad_out_h */
            float *attn_w_t = grad_scores_t;  /* reuse buffer */
            transpose_fp32(attn_w, seq_len, seq_len, attn_w_t);
            gemm(seq_len, head_dim, seq_len,
                 1.0f, attn_w_t, seq_len, go_h, head_dim,
                 0.0f, gv_h, head_dim);
            scatter_head(gv_h, seq_len, dim, head_dim, h, &grad_v->data[off]);

            /* Backward through softmax */
            softmax_backward(attn_w, grad_attn_w, grad_scores, seq_len, seq_len);

            /* grad_Q_h = grad_scores * K_h * scale */
            gemm(seq_len, head_dim, seq_len,
                 scale, grad_scores, seq_len, k_h, head_dim,
                 0.0f, gq_h, head_dim);
            scatter_head(gq_h, seq_len, dim, head_dim, h, &grad_q->data[off]);

            /* grad_K_h = grad_scores^T * Q_h * scale */
            transpose_fp32(grad_scores, seq_len, seq_len, grad_scores_t);
            gemm(seq_len, head_dim, seq_len,
                 scale, grad_scores_t, seq_len, q_h, head_dim,
                 0.0f, gk_h, head_dim);
            scatter_head(gk_h, seq_len, dim, head_dim, h, &grad_k->data[off]);
        }

        qat_free(go_h);
        qat_free(v_h);
        qat_free(v_h_t);
        qat_free(q_h);
        qat_free(k_h);
        qat_free(grad_attn_w);
        qat_free(grad_scores);
        qat_free(grad_scores_t);
        qat_free(gq_h);
        qat_free(gk_h);
        qat_free(gv_h);
    }

    /* Backward through Q, K, V projections — [B*S, dim] */
    Tensor *grad_from_q = qat_linear_backward(attn->wq, grad_q);
    Tensor *grad_from_k = qat_linear_backward(attn->wk, grad_k);
    Tensor *grad_from_v = qat_linear_backward(attn->wv, grad_v);

    /* Sum gradients from Q, K, V */
    Tensor *grad_input = tensor_create(total_tokens, dim);
    for (int i = 0; i < total_tokens * dim; i++) {
        grad_input->data[i] = grad_from_q->data[i] +
                               grad_from_k->data[i] +
                               grad_from_v->data[i];
    }

    tensor_free(grad_q);
    tensor_free(grad_k);
    tensor_free(grad_v);
    tensor_free(grad_from_q);
    tensor_free(grad_from_k);
    tensor_free(grad_from_v);
    tensor_free(grad_attn_out);

    return grad_input;
}

void attention_zero_grad(Attention *attn) {
    qat_linear_zero_grad(attn->wq);
    qat_linear_zero_grad(attn->wk);
    qat_linear_zero_grad(attn->wv);
    qat_linear_zero_grad(attn->wo);
}

/* ========================================================================
 * Transformer Block
 *
 * x -> norm1 -> attn -> + residual -> norm2 -> FFN -> + residual
 * FFN: up_proj -> GeLU -> down_proj
 * ======================================================================== */

TransformerBlock *transformer_block_create(int dim, int hidden_dim, int n_heads,
                                           const KernelDispatch *kd,
                                           uint64_t *rng_state) {
    TransformerBlock *block = (TransformerBlock *)calloc(1, sizeof(TransformerBlock));
    if (!block) return NULL;

    block->dim = dim;
    block->hidden_dim = hidden_dim;
    block->n_heads = n_heads;

    block->norm1 = rmsnorm_create(dim, 1e-5f);
    block->attn = attention_create(dim, n_heads, kd, rng_state);
    block->norm2 = rmsnorm_create(dim, 1e-5f);
    block->ffn_up = qat_linear_create(dim, hidden_dim, false, kd, rng_state);
    block->ffn_down = qat_linear_create(hidden_dim, dim, false, kd, rng_state);

    return block;
}

void transformer_block_free(TransformerBlock *block) {
    if (!block) return;
    rmsnorm_free(block->norm1);
    attention_free(block->attn);
    rmsnorm_free(block->norm2);
    qat_linear_free(block->ffn_up);
    qat_linear_free(block->ffn_down);
    tensor_free(block->saved_residual1);
    tensor_free(block->saved_residual2);
    tensor_free(block->saved_normed1);
    tensor_free(block->saved_normed2);
    tensor_free(block->saved_ffn_hidden);
    free(block);
}

/*
 * Transformer block forward with mini-batch support.
 * input: [batch_size * seq_len, dim]
 * All components except attention are batch-agnostic (just see N rows).
 * Attention needs batch_size to process sequences independently.
 */
Tensor *transformer_block_forward(TransformerBlock *block,
                                  const Tensor *input,
                                  int batch_size, int seq_len) {
    int dim = block->dim;
    int hidden_dim = block->hidden_dim;
    int total_tokens = batch_size * seq_len;

    /* Save residual 1 */
    if (block->saved_residual1) tensor_free(block->saved_residual1);
    block->saved_residual1 = tensor_create(total_tokens, dim);
    tensor_copy(block->saved_residual1, input);

    /* Norm -> Attention */
    Tensor *normed1 = rmsnorm_forward(block->norm1, input);
    if (block->saved_normed1) tensor_free(block->saved_normed1);
    block->saved_normed1 = tensor_create(total_tokens, dim);
    tensor_copy(block->saved_normed1, normed1);

    Tensor *attn_out = attention_forward(block->attn, normed1,
                                         batch_size, seq_len);
    tensor_free(normed1);

    /* Residual add */
    Tensor *after_attn = tensor_create(total_tokens, dim);
    for (int i = 0; i < total_tokens * dim; i++) {
        after_attn->data[i] = input->data[i] + attn_out->data[i];
    }
    tensor_free(attn_out);

    /* Save residual 2 */
    if (block->saved_residual2) tensor_free(block->saved_residual2);
    block->saved_residual2 = tensor_create(total_tokens, dim);
    tensor_copy(block->saved_residual2, after_attn);

    /* Norm -> FFN */
    Tensor *normed2 = rmsnorm_forward(block->norm2, after_attn);
    if (block->saved_normed2) tensor_free(block->saved_normed2);
    block->saved_normed2 = tensor_create(total_tokens, dim);
    tensor_copy(block->saved_normed2, normed2);

    /* FFN up: [B*S x dim] -> [B*S x hidden] */
    Tensor *ffn_up = qat_linear_forward(block->ffn_up, normed2);
    tensor_free(normed2);

    /* GeLU activation */
    if (block->saved_ffn_hidden) tensor_free(block->saved_ffn_hidden);
    block->saved_ffn_hidden = tensor_create(total_tokens, hidden_dim);
    tensor_copy(block->saved_ffn_hidden, ffn_up);

    gelu_forward(ffn_up->data, ffn_up->data, total_tokens * hidden_dim);

    /* FFN down: [B*S x hidden] -> [B*S x dim] */
    Tensor *ffn_out = qat_linear_forward(block->ffn_down, ffn_up);
    tensor_free(ffn_up);

    /* Residual add */
    Tensor *output = tensor_create(total_tokens, dim);
    for (int i = 0; i < total_tokens * dim; i++) {
        output->data[i] = after_attn->data[i] + ffn_out->data[i];
    }
    tensor_free(after_attn);
    tensor_free(ffn_out);

    return output;
}

Tensor *transformer_block_backward(TransformerBlock *block,
                                   const Tensor *grad_output,
                                   int batch_size, int seq_len) {
    int dim = block->dim;
    int hidden_dim = block->hidden_dim;
    int total_tokens = batch_size * seq_len;

    /* ---- FFN backward ---- */
    Tensor *grad_ffn_act = qat_linear_backward(block->ffn_down, grad_output);

    Tensor *grad_ffn_up = tensor_create(total_tokens, hidden_dim);
    gelu_backward(block->saved_ffn_hidden->data, grad_ffn_act->data,
                  grad_ffn_up->data, total_tokens * hidden_dim);
    tensor_free(grad_ffn_act);

    Tensor *grad_normed2 = qat_linear_backward(block->ffn_up, grad_ffn_up);
    tensor_free(grad_ffn_up);

    Tensor *grad_after_attn = rmsnorm_backward(block->norm2, grad_normed2);
    tensor_free(grad_normed2);

    /* Add residual gradient */
    for (int i = 0; i < total_tokens * dim; i++) {
        grad_after_attn->data[i] += grad_output->data[i];
    }

    /* ---- Attention backward ---- */
    Tensor *grad_normed1 = attention_backward(block->attn, grad_after_attn,
                                               batch_size, seq_len);

    Tensor *grad_input = rmsnorm_backward(block->norm1, grad_normed1);
    tensor_free(grad_normed1);

    /* Add residual gradient */
    for (int i = 0; i < total_tokens * dim; i++) {
        grad_input->data[i] += grad_after_attn->data[i];
    }
    tensor_free(grad_after_attn);

    return grad_input;
}

void transformer_block_zero_grad(TransformerBlock *block) {
    rmsnorm_zero_grad(block->norm1);
    attention_zero_grad(block->attn);
    rmsnorm_zero_grad(block->norm2);
    qat_linear_zero_grad(block->ffn_up);
    qat_linear_zero_grad(block->ffn_down);
}
