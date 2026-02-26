/*
 * kernels_avx2.c - AVX2 GEMM implementations
 *
 * INT8 GEMM: Widen to int32, SIMD on output columns. Avoids vpmaddubsw
 *            saturation issues. The VNNI kernel is the real workhorse.
 * FP32 GEMM: Uses VFMADD231PS (256-bit, 8 FP32 FMAs per instruction).
 *
 * Compile with: -mavx2 -mfma
 */

#include "qat_cpu.h"
#include <immintrin.h>

/*
 * AVX2 INT8 GEMM: C_i32[M,N] += A_i8[M,K] * B_i8[K,N]
 *
 * Strategy: for each (i, k), broadcast A[i][k] to 8 int32 lanes,
 * load 8 B[k][j:j+8] values sign-extended to int32, multiply and accumulate.
 * This avoids vpmaddubsw's int16 saturation issue entirely.
 *
 * Loop order: i, j_block, k (accumulate in registers).
 */
void gemm_int8_avx2(int M, int N, int K,
                    const int8_t *A, int lda,
                    const int8_t *B, int ldb,
                    int32_t *C, int ldc) {
    int j_end_8 = N - (N % 8);

    #pragma omp parallel for schedule(static) if(M >= 8)
    for (int i = 0; i < M; i++) {
        /* Process 8 output columns at a time */
        for (int j = 0; j < j_end_8; j += 8) {
            __m256i acc = _mm256_setzero_si256();

            for (int k = 0; k < K; k++) {
                /* Broadcast A[i][k] as int32 */
                __m256i a_v = _mm256_set1_epi32((int32_t)A[i * lda + k]);

                /* Load 8 bytes from B[k][j:j+8], sign-extend to int32 */
                __m128i b_bytes = _mm_loadl_epi64(
                    (const __m128i *)&B[k * ldb + j]);
                __m256i b_v = _mm256_cvtepi8_epi32(b_bytes);

                /* Multiply and accumulate */
                acc = _mm256_add_epi32(acc, _mm256_mullo_epi32(a_v, b_v));
            }

            _mm256_storeu_si256((__m256i *)&C[i * ldc + j], acc);
        }

        /* Scalar tail for remaining columns */
        for (int j = j_end_8; j < N; j++) {
            int32_t sum = 0;
            for (int k = 0; k < K; k++) {
                sum += (int32_t)A[i * lda + k] * (int32_t)B[k * ldb + j];
            }
            C[i * ldc + j] = sum;
        }
    }
}

/*
 * AVX2 FP32 GEMM: C[M,N] = alpha * A[M,K] * B[K,N] + beta * C[M,N]
 *
 * Uses 256-bit VFMADD231PS: 8 FP32 FMAs per instruction.
 * Loop order: i, k, j for cache-friendly access on row-major B.
 */
void gemm_fp32_avx2(int M, int N, int K,
                    float alpha,
                    const float *A, int lda,
                    const float *B, int ldb,
                    float beta,
                    float *C, int ldc) {
    __m256 beta_v = _mm256_set1_ps(beta);
    __m256 alpha_v = _mm256_set1_ps(alpha);

    int j_end_8 = N - (N % 8);

    #pragma omp parallel for schedule(static) if(M >= 8)
    for (int i = 0; i < M; i++) {
        /* Scale C row by beta */
        for (int j = 0; j < j_end_8; j += 8) {
            __m256 c_v = _mm256_loadu_ps(&C[i * ldc + j]);
            c_v = _mm256_mul_ps(c_v, beta_v);
            _mm256_storeu_ps(&C[i * ldc + j], c_v);
        }
        for (int j = j_end_8; j < N; j++) {
            C[i * ldc + j] *= beta;
        }

        /* Accumulate: C[i][j] += alpha * A[i][k] * B[k][j] */
        for (int k = 0; k < K; k++) {
            __m256 a_v = _mm256_mul_ps(_mm256_set1_ps(A[i * lda + k]), alpha_v);

            for (int j = 0; j < j_end_8; j += 8) {
                __m256 b_v = _mm256_loadu_ps(&B[k * ldb + j]);
                __m256 c_v = _mm256_loadu_ps(&C[i * ldc + j]);
                c_v = _mm256_fmadd_ps(a_v, b_v, c_v);
                _mm256_storeu_ps(&C[i * ldc + j], c_v);
            }

            /* Scalar tail */
            float a_scaled = alpha * A[i * lda + k];
            for (int j = j_end_8; j < N; j++) {
                C[i * ldc + j] += a_scaled * B[k * ldb + j];
            }
        }
    }
}
