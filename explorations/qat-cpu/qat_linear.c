/*
 * qat_linear.c - QAT Linear Layer
 *
 * Forward: quantize weights+input -> INT8 GEMM -> dequantize -> add bias
 * Backward: FP32 GEMM with STE (uses FP32 master weights directly)
 *
 * The STE is implicit: backward pass computes gradients using the FP32
 * master weights, not the quantized weights. This means d(quantize)/d(w) = 1.
 */

#include "qat_cpu.h"

QATLinear *qat_linear_create(int in_features, int out_features,
                             bool use_bias, const KernelDispatch *kd,
                             uint64_t *rng_state) {
    QATLinear *layer = (QATLinear *)calloc(1, sizeof(QATLinear));
    if (!layer) return NULL;

    layer->in_features = in_features;
    layer->out_features = out_features;
    layer->kernels = kd;

    /* FP32 master weights: [out_features x in_features] */
    layer->weight = tensor_create(out_features, in_features);

    /* Kaiming uniform initialization: U(-bound, bound) where bound = sqrt(1/in) */
    float bound = sqrtf(1.0f / (float)in_features);
    tensor_rand(layer->weight, -bound, bound, rng_state);

    /* Bias */
    if (use_bias) {
        layer->bias = tensor_zeros(1, out_features);
    }

    /* Gradient buffers */
    layer->grad_weight = tensor_zeros(out_features, in_features);
    if (use_bias) {
        layer->grad_bias = tensor_zeros(1, out_features);
    }

    /* Quantized workspace */
    layer->weight_q = tensor_i8_create(out_features, in_features);
    layer->weight_scales = (float *)qat_calloc(out_features * sizeof(float));

    /* Pre-allocate transposed weight buffers (batch-independent, reused every call) */
    layer->weight_q_t = tensor_i8_create(in_features, out_features);
    layer->weight_fp32_t = (float *)qat_alloc(
        (size_t)in_features * out_features * sizeof(float));

    /* saved_input is allocated during forward */
    layer->saved_input = NULL;

    /* Default: use INT8 quantized forward */
    layer->use_qat = true;
    layer->weights_dirty = true;  /* Need initial quantization */

    return layer;
}

void qat_linear_free(QATLinear *layer) {
    if (!layer) return;
    tensor_free(layer->weight);
    tensor_free(layer->bias);
    tensor_free(layer->grad_weight);
    tensor_free(layer->grad_bias);
    tensor_i8_free(layer->weight_q);
    qat_free(layer->weight_scales);
    tensor_i8_free(layer->weight_q_t);
    qat_free(layer->weight_fp32_t);
    tensor_free(layer->saved_input);
    free(layer);
}

/*
 * Forward pass:
 *   1. Quantize weights to INT8 (per-channel symmetric)
 *   2. Quantize input to INT8 (per-token symmetric)
 *   3. INT8 GEMM: output_i32 = input_i8 * weight_i8^T
 *      But weight is [out x in] and input is [batch x in].
 *      We need output[batch x out] = input[batch x in] * weight^T[in x out]
 *      So: A=input_i8 [batch x in], B=weight_i8^T [in x out], C=[batch x out]
 *      We'll just transpose weights into a temp buffer.
 *   4. Dequantize: out_fp32 = acc_i32 * scale_act * scale_wt
 *   5. Add bias
 *
 * Actually, let's think about this more carefully.
 *   output[i][j] = sum_k input[i][k] * weight[j][k]    (weight is [out x in])
 *                = sum_k input[i][k] * weight^T[k][j]
 *
 *   So it's: C[M x N] = A[M x K] * B_T[K x N]
 *   where M=batch, K=in, N=out, A=input, B=weight (and B_T is weight transposed)
 *
 *   Our GEMM does C = A * B where B is [K x N].
 *   So B = weight^T [in x out].
 *   We need to transpose weight [out x in] -> [in x out].
 */

/* Helper: transpose a matrix. */
static void transpose_i8(const int8_t *src, int rows, int cols, int8_t *dst) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            dst[j * rows + i] = src[i * cols + j];
        }
    }
}

static void transpose_fp32(const float *src, int rows, int cols, float *dst) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            dst[j * rows + i] = src[i * cols + j];
        }
    }
}

Tensor *qat_linear_forward(QATLinear *layer, const Tensor *input) {
    int batch = input->rows;
    int in_f = layer->in_features;
    int out_f = layer->out_features;

    /* Save input for backward pass */
    if (layer->saved_input) tensor_free(layer->saved_input);
    layer->saved_input = tensor_create(batch, in_f);
    tensor_copy(layer->saved_input, input);

    /* FP32-only forward path (no quantization) */
    if (!layer->use_qat) {
        /* Transpose weight (skip if cached from same step) */
        if (layer->weights_dirty) {
            transpose_fp32(layer->weight->data, out_f, in_f, layer->weight_fp32_t);
            layer->weights_dirty = false;
        }

        Tensor *output = tensor_zeros(batch, out_f);
        layer->kernels->fp32_gemm(batch, out_f, in_f,
                                   1.0f,
                                   input->data, in_f,
                                   layer->weight_fp32_t, out_f,
                                   0.0f,
                                   output->data, out_f);

        if (layer->bias) {
            add_bias(output->data, batch, out_f, layer->bias->data);
        }
        return output;
    }

    /* 1. Quantize weights (skip if cached from same step) */
    if (layer->weights_dirty) {
        quantize_per_channel(layer->weight->data, out_f, in_f,
                             layer->weight_q->data, layer->weight_scales);
        transpose_i8(layer->weight_q->data, out_f, in_f, layer->weight_q_t->data);
        layer->weights_dirty = false;
    }

    /* 2. Quantize input: [batch x in_f] -> INT8 with per-token scales */
    TensorI8 *input_q = tensor_i8_create(batch, in_f);
    float *input_scales = (float *)qat_alloc(batch * sizeof(float));
    quantize_per_token(input->data, batch, in_f, input_q->data, input_scales);

    /* 4. INT8 GEMM: C_i32[batch x out_f] = input_i8[batch x in_f] * weight_t_i8[in_f x out_f] */
    TensorI32 *acc = tensor_i32_create(batch, out_f);
    layer->kernels->int8_gemm(batch, out_f, in_f,
                               input_q->data, in_f,
                               layer->weight_q_t->data, out_f,
                               acc->data, out_f);

    /* 5. Dequantize: out[i][j] = acc[i][j] * scale_act[i] * scale_wt[j] */
    Tensor *output = tensor_create(batch, out_f);
    dequantize_int32(acc->data, batch, out_f,
                     input_scales, layer->weight_scales,
                     output->data);

    /* 6. Add bias */
    if (layer->bias) {
        add_bias(output->data, batch, out_f, layer->bias->data);
    }

    /* Cleanup temporaries (weight_q_t is pre-allocated, not freed here) */
    tensor_i8_free(input_q);
    tensor_i32_free(acc);
    qat_free(input_scales);

    return output;
}

/*
 * Backward pass (STE):
 *   grad_input  = grad_output * W_fp32         [batch x in_f] = [batch x out_f] * [out_f x in_f]
 *   grad_weight += grad_output^T * saved_input  [out_f x in_f] = [out_f x batch] * [batch x in_f]
 *   grad_bias   += sum(grad_output, dim=0)      [1 x out_f]
 *
 * Key STE property: we use W_fp32 (master weights) directly, not the quantized version.
 * This is the entire STE — gradients flow through as if quantization wasn't there.
 */
Tensor *qat_linear_backward(QATLinear *layer, const Tensor *grad_output) {
    int batch = grad_output->rows;
    int out_f = layer->out_features;
    int in_f = layer->in_features;

    /*
     * 1. grad_input = grad_output * weight
     *    [batch x in_f] = [batch x out_f] * [out_f x in_f]
     *    This is: C = A * B where A=[batch x out_f], B=weight[out_f x in_f]
     */
    Tensor *grad_input = tensor_zeros(batch, in_f);
    layer->kernels->fp32_gemm(batch, in_f, out_f,
                               1.0f,
                               grad_output->data, out_f,
                               layer->weight->data, in_f,
                               0.0f,
                               grad_input->data, in_f);

    /*
     * 2. grad_weight += grad_output^T * saved_input
     *    [out_f x in_f] = [out_f x batch] * [batch x in_f]
     *    This is: C = A^T * B. We'll transpose grad_output, then GEMM.
     */
    float *grad_output_t = (float *)qat_alloc(out_f * batch * sizeof(float));
    transpose_fp32(grad_output->data, batch, out_f, grad_output_t);

    layer->kernels->fp32_gemm(out_f, in_f, batch,
                               1.0f,
                               grad_output_t, batch,
                               layer->saved_input->data, in_f,
                               1.0f,  /* accumulate into existing grad_weight */
                               layer->grad_weight->data, in_f);
    qat_free(grad_output_t);

    /*
     * 3. grad_bias += sum(grad_output, dim=0)
     */
    if (layer->grad_bias) {
        for (int i = 0; i < batch; i++) {
            for (int j = 0; j < out_f; j++) {
                layer->grad_bias->data[j] += grad_output->data[i * out_f + j];
            }
        }
    }

    return grad_input;
}

void qat_linear_zero_grad(QATLinear *layer) {
    if (layer->grad_weight) {
        memset(layer->grad_weight->data, 0,
               tensor_bytes(layer->grad_weight));
    }
    if (layer->grad_bias) {
        memset(layer->grad_bias->data, 0,
               tensor_bytes(layer->grad_bias));
    }
}
