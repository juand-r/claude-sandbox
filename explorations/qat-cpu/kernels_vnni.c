/*
 * kernels_vnni.c - AVX-512 VNNI INT8 GEMM + AVX-512 FP32 GEMM
 *
 * INT8: Uses VPDPBUSD - 64 uint8*int8 MACs per instruction into 16 int32.
 * FP32: Uses VFMADD231PS (512-bit) - 16 FP32 FMAs per instruction.
 *
 * Compile with: -mavx512f -mavx512bw -mavx512vnni
 *
 * VPDPBUSD semantics: for each of 16 int32 lanes:
 *   dst[i] += (u8[4i+0]*i8[4i+0] + u8[4i+1]*i8[4i+1] +
 *              u8[4i+2]*i8[4i+2] + u8[4i+3]*i8[4i+3])
 * So it does 4 uint8*int8 products per int32 lane, 16 lanes = 64 MACs.
 *
 * Same unsigned trick as AVX2: convert signed A -> unsigned by adding 128,
 * then correct with: C_true = C_computed - 128 * col_sums(B)
 */

#include "qat_cpu.h"
#include <immintrin.h>

/*
 * AVX-512 VNNI INT8 GEMM: C_i32[M,N] += A_i8[M,K] * B_i8[K,N]
 *
 * Process 16 output columns at a time (one zmm register of int32).
 * For the reduction dimension k, process 4 at a time (matches VPDPBUSD).
 *
 * Data layout for VPDPBUSD with row-major B:
 *   For output cols j..j+15, we need B[k..k+3][j..j+15].
 *   We interleave 4 rows of B into the format VPDPBUSD expects:
 *   For each of 16 output cols, pack 4 consecutive k values together.
 *
 *   A is broadcast: same 4 A values for all 16 output cols.
 */
void gemm_int8_vnni(int M, int N, int K,
                    const int8_t *A, int lda,
                    const int8_t *B, int ldb,
                    int32_t *C, int ldc) {
    int j_end_16 = N - (N % 16);
    int k_end_4 = K - (K % 4);

    for (int i = 0; i < M; i++) {
        /* Process 16 output columns at a time */
        for (int j = 0; j < j_end_16; j += 16) {
            __m512i acc = _mm512_setzero_si512();

            /* Process k in groups of 4 (VPDPBUSD does 4 u8*i8 per lane) */
            for (int k = 0; k < k_end_4; k += 4) {
                /*
                 * A values: A[i][k+0..3], broadcast to all lanes.
                 * Convert to unsigned: ua = a + 128.
                 *
                 * For VPDPBUSD, first operand (src1) is uint8, second (src2) is int8.
                 * Each int32 lane uses 4 consecutive bytes from each operand:
                 *   lane[L] += src1[4L+0]*src2[4L+0] + src1[4L+1]*src2[4L+1] +
                 *              src1[4L+2]*src2[4L+2] + src1[4L+3]*src2[4L+3]
                 *
                 * We want each lane L (corresponding to output col j+L) to compute:
                 *   sum_{dk=0}^{3} A[i][k+dk] * B[k+dk][j+L]
                 *
                 * So in src1 (uint8, A): repeat [ua0, ua1, ua2, ua3] for each lane
                 * In src2 (int8, B): for lane L, put [B[k][j+L], B[k+1][j+L],
                 *                                      B[k+2][j+L], B[k+3][j+L]]
                 */
                int8_t a0 = A[i * lda + k + 0];
                int8_t a1 = A[i * lda + k + 1];
                int8_t a2 = A[i * lda + k + 2];
                int8_t a3 = A[i * lda + k + 3];

                uint8_t ua0 = (uint8_t)((int16_t)a0 + 128);
                uint8_t ua1 = (uint8_t)((int16_t)a1 + 128);
                uint8_t ua2 = (uint8_t)((int16_t)a2 + 128);
                uint8_t ua3 = (uint8_t)((int16_t)a3 + 128);

                /* Broadcast A pattern to all 16 lanes */
                int32_t a_pattern = (uint32_t)ua0 | ((uint32_t)ua1 << 8) |
                                    ((uint32_t)ua2 << 16) | ((uint32_t)ua3 << 24);
                __m512i a_vec = _mm512_set1_epi32(a_pattern);

                /*
                 * Build B vector: for each of 16 lanes, pack 4 B values.
                 * b_vec lane L bytes = [B[k][j+L], B[k+1][j+L], B[k+2][j+L], B[k+3][j+L]]
                 */
                int32_t b_packed[16];
                for (int dj = 0; dj < 16; dj++) {
                    uint8_t b0 = (uint8_t)B[(k + 0) * ldb + j + dj];
                    uint8_t b1 = (uint8_t)B[(k + 1) * ldb + j + dj];
                    uint8_t b2 = (uint8_t)B[(k + 2) * ldb + j + dj];
                    uint8_t b3 = (uint8_t)B[(k + 3) * ldb + j + dj];
                    b_packed[dj] = (int32_t)((uint32_t)b0 | ((uint32_t)b1 << 8) |
                                             ((uint32_t)b2 << 16) | ((uint32_t)b3 << 24));
                }
                __m512i b_vec = _mm512_loadu_si512((const __m512i *)b_packed);

                /* VPDPBUSD: acc += dot4(a_vec, b_vec) per lane */
                acc = _mm512_dpbusd_epi32(acc, a_vec, b_vec);
            }

            /*
             * Correction for unsigned trick:
             * We computed (a+128)*b instead of a*b for k values processed by VNNI.
             * Need to subtract 128 * sum_k B[k][j'] for each output col j'.
             */
            __m512i correction = _mm512_setzero_si512();
            for (int k = 0; k < k_end_4; k++) {
                /* Sign-extend B[k][j..j+15] to int32 and accumulate */
                __m128i b_bytes = _mm_loadu_si128((const __m128i *)&B[k * ldb + j]);
                __m512i b_ext = _mm512_cvtepi8_epi32(b_bytes);
                correction = _mm512_add_epi32(correction, b_ext);
            }
            correction = _mm512_mullo_epi32(correction, _mm512_set1_epi32(128));
            acc = _mm512_sub_epi32(acc, correction);

            /* Handle remaining k values (not multiple of 4) with scalar */
            for (int k = k_end_4; k < K; k++) {
                int32_t a_val = (int32_t)A[i * lda + k];
                __m128i b_bytes = _mm_loadu_si128((const __m128i *)&B[k * ldb + j]);
                __m512i b_ext = _mm512_cvtepi8_epi32(b_bytes);
                __m512i a_broad = _mm512_set1_epi32(a_val);
                acc = _mm512_add_epi32(acc, _mm512_mullo_epi32(a_broad, b_ext));
            }

            /* Store 16 int32 results */
            _mm512_storeu_si512((__m512i *)&C[i * ldc + j], acc);
        }

        /* Handle remaining columns (< 16) with scalar */
        for (int j = j_end_16; j < N; j++) {
            int32_t sum = 0;
            for (int k = 0; k < K; k++) {
                sum += (int32_t)A[i * lda + k] * (int32_t)B[k * ldb + j];
            }
            C[i * ldc + j] = sum;
        }
    }
}

/*
 * AVX-512 FP32 GEMM: C[M,N] = alpha * A[M,K] * B[K,N] + beta * C[M,N]
 *
 * Uses 512-bit VFMADD231PS: 16 FP32 FMAs per instruction.
 * Loop order: i, k, j for cache-friendly access on row-major B.
 */
void gemm_fp32_avx512(int M, int N, int K,
                      float alpha,
                      const float *A, int lda,
                      const float *B, int ldb,
                      float beta,
                      float *C, int ldc) {
    __m512 beta_v = _mm512_set1_ps(beta);
    __m512 alpha_v = _mm512_set1_ps(alpha);

    int j_end_16 = N - (N % 16);

    for (int i = 0; i < M; i++) {
        /* Scale C row by beta */
        for (int j = 0; j < j_end_16; j += 16) {
            __m512 c_v = _mm512_loadu_ps(&C[i * ldc + j]);
            c_v = _mm512_mul_ps(c_v, beta_v);
            _mm512_storeu_ps(&C[i * ldc + j], c_v);
        }
        for (int j = j_end_16; j < N; j++) {
            C[i * ldc + j] *= beta;
        }

        /* Accumulate */
        for (int k = 0; k < K; k++) {
            __m512 a_v = _mm512_mul_ps(_mm512_set1_ps(A[i * lda + k]), alpha_v);

            for (int j = 0; j < j_end_16; j += 16) {
                __m512 b_v = _mm512_loadu_ps(&B[k * ldb + j]);
                __m512 c_v = _mm512_loadu_ps(&C[i * ldc + j]);
                c_v = _mm512_fmadd_ps(a_v, b_v, c_v);
                _mm512_storeu_ps(&C[i * ldc + j], c_v);
            }

            /* Scalar tail */
            float a_scaled = alpha * A[i * lda + k];
            for (int j = j_end_16; j < N; j++) {
                C[i * ldc + j] += a_scaled * B[k * ldb + j];
            }
        }
    }
}
