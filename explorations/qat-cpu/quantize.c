/*
 * quantize.c - Quantization/dequantization routines
 *
 * Per-channel symmetric for weights, per-token symmetric for activations.
 * INT32 -> FP32 dequantization with dual scales.
 * Fake quantization for training noise simulation.
 */

#include "qat_cpu.h"

/*
 * Per-channel symmetric quantization (for weights).
 * Each row is quantized independently:
 *   scale[i] = absmax(src[i, :]) / 127.0
 *   dst[i][j] = clamp(round(src[i][j] / scale[i]), -128, 127)
 *
 * If a row is all zeros, scale = 1.0 (avoid division by zero).
 */
void quantize_per_channel(const float *src, int rows, int cols,
                          int8_t *dst, float *scales) {
    #pragma omp parallel for schedule(static) if(rows >= 8)
    for (int i = 0; i < rows; i++) {
        /* Find absmax of this row */
        float amax = 0.0f;
        for (int j = 0; j < cols; j++) {
            float a = fabsf(src[i * cols + j]);
            if (a > amax) amax = a;
        }

        /* Compute scale */
        float scale = (amax > 0.0f) ? (amax / 127.0f) : 1.0f;
        scales[i] = scale;

        /* Quantize */
        float inv_scale = 1.0f / scale;
        for (int j = 0; j < cols; j++) {
            float val = src[i * cols + j] * inv_scale;
            int32_t q = (int32_t)roundf(val);
            if (q > 127) q = 127;
            if (q < -128) q = -128;
            dst[i * cols + j] = (int8_t)q;
        }
    }
}

/*
 * Per-token symmetric quantization (for activations).
 * Identical math to per-channel, applied to activation rows.
 */
void quantize_per_token(const float *src, int rows, int cols,
                        int8_t *dst, float *scales) {
    /* Same implementation as per-channel */
    quantize_per_channel(src, rows, cols, dst, scales);
}

/*
 * Dequantize INT32 accumulator to FP32.
 * out[i][j] = acc[i][j] * scale_act[i] * scale_wt[j]
 *
 * scale_act: [rows] - per-token scales from activation quantization
 * scale_wt:  [cols] - per-channel scales from weight quantization
 */
void dequantize_int32(const int32_t *acc, int rows, int cols,
                      const float *scale_act, const float *scale_wt,
                      float *out) {
    #pragma omp parallel for schedule(static) if(rows >= 8)
    for (int i = 0; i < rows; i++) {
        float sa = scale_act[i];
        for (int j = 0; j < cols; j++) {
            out[i * cols + j] = (float)acc[i * cols + j] * sa * scale_wt[j];
        }
    }
}

/*
 * Add bias: out[i][j] += bias[j]
 */
void add_bias(float *out, int rows, int cols, const float *bias) {
    #pragma omp parallel for schedule(static) if(rows >= 8)
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            out[i * cols + j] += bias[j];
        }
    }
}

/*
 * Fake quantization: quantize then immediately dequantize.
 * Simulates quantization noise in FP32 domain.
 *
 * For each row:
 *   scale = absmax(row) / 127.0
 *   out[i][j] = round(src[i][j] / scale) * scale
 */
void fake_quantize_per_channel(const float *src, int rows, int cols,
                               float *out) {
    for (int i = 0; i < rows; i++) {
        /* Find absmax */
        float amax = 0.0f;
        for (int j = 0; j < cols; j++) {
            float a = fabsf(src[i * cols + j]);
            if (a > amax) amax = a;
        }

        float scale = (amax > 0.0f) ? (amax / 127.0f) : 1.0f;
        float inv_scale = 1.0f / scale;

        for (int j = 0; j < cols; j++) {
            float q = roundf(src[i * cols + j] * inv_scale);
            if (q > 127.0f) q = 127.0f;
            if (q < -128.0f) q = -128.0f;
            out[i * cols + j] = q * scale;
        }
    }
}
