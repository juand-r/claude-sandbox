/*
 * quantize.c - Quantization/dequantization routines
 *
 * Per-channel symmetric for weights, per-token symmetric for activations.
 * INT32 -> FP32 dequantization with dual scales.
 * Fake quantization for training noise simulation.
 *
 * Hot-path functions have AVX-512 vectorized versions using GCC target
 * attributes (no need to compile the whole file with -mavx512f).
 */

#include "qat_cpu.h"
#include <immintrin.h>

/* ========================================================================
 * AVX-512 vectorized quantization of a single row.
 *
 * 1. absmax: _mm512_and_ps (clear sign bit) + _mm512_max_ps + horizontal reduce
 * 2. quantize: _mm512_mul_ps + _mm512_cvtps_epi32 (round) + _mm512_cvtsepi32_epi8 (saturate)
 *
 * _mm512_cvtsepi32_epi8 does signed saturation int32 -> int8, so no manual clamp needed.
 * _mm512_cvtps_epi32 rounds to nearest even (vs roundf's ties-away-from-zero),
 * but the difference only affects exact .5 values — negligible for quantization.
 * ======================================================================== */

__attribute__((target("avx512f,avx512bw")))
static void quantize_row_avx512(const float *src, int cols,
                                 int8_t *dst, float *scale_out) {
    const __m512i abs_mask_i = _mm512_set1_epi32(0x7FFFFFFF);
    __m512 vmax = _mm512_setzero_ps();

    /* Vectorized absmax (integer AND to clear sign bit — AVX-512F only) */
    int j = 0;
    for (; j + 16 <= cols; j += 16) {
        __m512 v = _mm512_loadu_ps(src + j);
        __m512 av = _mm512_castsi512_ps(
            _mm512_and_si512(_mm512_castps_si512(v), abs_mask_i));
        vmax = _mm512_max_ps(vmax, av);
    }
    float amax = _mm512_reduce_max_ps(vmax);
    for (; j < cols; j++) {
        float a = fabsf(src[j]);
        if (a > amax) amax = a;
    }

    float scale = (amax > 0.0f) ? (amax / 127.0f) : 1.0f;
    *scale_out = scale;

    /* Vectorized quantize: mul, round, saturate-pack to int8 */
    __m512 inv_scale_vec = _mm512_set1_ps(1.0f / scale);
    j = 0;
    for (; j + 16 <= cols; j += 16) {
        __m512 v = _mm512_loadu_ps(src + j);
        __m512 scaled = _mm512_mul_ps(v, inv_scale_vec);
        __m512i q32 = _mm512_cvtps_epi32(scaled);
        __m128i q8 = _mm512_cvtsepi32_epi8(q32);
        _mm_storeu_si128((__m128i *)(dst + j), q8);
    }
    /* Scalar tail */
    float inv_scale = 1.0f / scale;
    for (; j < cols; j++) {
        float val = src[j] * inv_scale;
        int32_t q = (int32_t)roundf(val);
        if (q > 127) q = 127;
        if (q < -128) q = -128;
        dst[j] = (int8_t)q;
    }
}

/* Scalar fallback for non-AVX-512 CPUs */
static void quantize_row_scalar(const float *src, int cols,
                                 int8_t *dst, float *scale_out) {
    float amax = 0.0f;
    for (int j = 0; j < cols; j++) {
        float a = fabsf(src[j]);
        if (a > amax) amax = a;
    }
    float scale = (amax > 0.0f) ? (amax / 127.0f) : 1.0f;
    *scale_out = scale;
    float inv_scale = 1.0f / scale;
    for (int j = 0; j < cols; j++) {
        float val = src[j] * inv_scale;
        int32_t q = (int32_t)roundf(val);
        if (q > 127) q = 127;
        if (q < -128) q = -128;
        dst[j] = (int8_t)q;
    }
}

/*
 * Per-channel symmetric quantization (for weights).
 * Each row is quantized independently:
 *   scale[i] = absmax(src[i, :]) / 127.0
 *   dst[i][j] = clamp(round(src[i][j] / scale[i]), -128, 127)
 *
 * If a row is all zeros, scale = 1.0 (avoid division by zero).
 * Dispatches to AVX-512 at runtime if available.
 */
void quantize_per_channel(const float *src, int rows, int cols,
                          int8_t *dst, float *scales) {
    int use_avx512 = __builtin_cpu_supports("avx512f");
    #pragma omp parallel for schedule(static) if(rows >= 8)
    for (int i = 0; i < rows; i++) {
        if (use_avx512) {
            quantize_row_avx512(src + i * cols, cols,
                                dst + i * cols, &scales[i]);
        } else {
            quantize_row_scalar(src + i * cols, cols,
                                dst + i * cols, &scales[i]);
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

__attribute__((target("avx512f,avx512bw")))
static void dequantize_row_avx512(const int32_t *acc, int cols,
                                   float sa, const float *scale_wt,
                                   float *out) {
    __m512 sa_vec = _mm512_set1_ps(sa);
    int j = 0;
    for (; j + 16 <= cols; j += 16) {
        __m512i a = _mm512_loadu_si512(acc + j);
        __m512 fa = _mm512_cvtepi32_ps(a);
        __m512 sw = _mm512_loadu_ps(scale_wt + j);
        __m512 result = _mm512_mul_ps(_mm512_mul_ps(fa, sa_vec), sw);
        _mm512_storeu_ps(out + j, result);
    }
    for (; j < cols; j++) {
        out[j] = (float)acc[j] * sa * scale_wt[j];
    }
}

void dequantize_int32(const int32_t *acc, int rows, int cols,
                      const float *scale_act, const float *scale_wt,
                      float *out) {
    int use_avx512 = __builtin_cpu_supports("avx512f");
    #pragma omp parallel for schedule(static) if(rows >= 8)
    for (int i = 0; i < rows; i++) {
        if (use_avx512) {
            dequantize_row_avx512(acc + i * cols, cols,
                                   scale_act[i], scale_wt,
                                   out + i * cols);
        } else {
            float sa = scale_act[i];
            for (int j = 0; j < cols; j++) {
                out[i * cols + j] = (float)acc[i * cols + j] * sa * scale_wt[j];
            }
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
 * Per-column symmetric quantization.
 * Each column is quantized independently:
 *   scale[j] = absmax(src[:, j]) / 127.0
 *   dst[i][j] = clamp(round(src[i][j] / scale[j]), -128, 127)
 *
 * Used in INT8 backward: the B matrix in C = A * B needs per-column scales
 * so that dequantize factors as out[i][j] = acc[i][j] * scaleA[i] * scaleB[j].
 */
void quantize_per_column(const float *src, int rows, int cols,
                          int8_t *dst, float *scales) {
    /* Find absmax per column */
    #pragma omp parallel for schedule(static) if(cols >= 8)
    for (int j = 0; j < cols; j++) {
        float amax = 0.0f;
        for (int i = 0; i < rows; i++) {
            float a = fabsf(src[i * cols + j]);
            if (a > amax) amax = a;
        }
        scales[j] = (amax > 0.0f) ? (amax / 127.0f) : 1.0f;
    }

    /* Quantize each element */
    #pragma omp parallel for schedule(static) if(rows >= 8)
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            float inv_scale = 1.0f / scales[j];
            float val = src[i * cols + j] * inv_scale;
            int32_t q = (int32_t)roundf(val);
            if (q > 127) q = 127;
            if (q < -128) q = -128;
            dst[i * cols + j] = (int8_t)q;
        }
    }
}

/*
 * Dequantize INT32 accumulator to FP32, accumulating into existing output.
 * out[i][j] += acc[i][j] * scale_act[i] * scale_wt[j]
 *
 * Same as dequantize_int32 but adds to out instead of overwriting.
 */
void dequantize_int32_acc(const int32_t *acc, int rows, int cols,
                           const float *scale_act, const float *scale_wt,
                           float *out) {
    #pragma omp parallel for schedule(static) if(rows >= 8)
    for (int i = 0; i < rows; i++) {
        float sa = scale_act[i];
        for (int j = 0; j < cols; j++) {
            out[i * cols + j] += (float)acc[i * cols + j] * sa * scale_wt[j];
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
