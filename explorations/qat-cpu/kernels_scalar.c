/*
 * kernels_scalar.c - Scalar reference GEMM implementations
 *
 * These are the reference implementations that work on any CPU.
 * All SIMD kernels are verified against these for correctness.
 */

#include "qat_cpu.h"

/*
 * Scalar INT8 GEMM: C_i32[M,N] += A_i8[M,K] * B_i8[K,N]
 *
 * Straightforward triple loop. No tricks needed for scalar.
 * A: [M x K] row-major, B: [K x N] row-major, C: [M x N] row-major.
 * C is zeroed then accumulated into.
 */
void gemm_int8_scalar(int M, int N, int K,
                      const int8_t *A, int lda,
                      const int8_t *B, int ldb,
                      int32_t *C, int ldc) {
    /* Zero output */
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            C[i * ldc + j] = 0;
        }
    }

    /* Accumulate: C[i][j] += A[i][k] * B[k][j] */
    for (int i = 0; i < M; i++) {
        for (int k = 0; k < K; k++) {
            int32_t a_val = (int32_t)A[i * lda + k];
            for (int j = 0; j < N; j++) {
                C[i * ldc + j] += a_val * (int32_t)B[k * ldb + j];
            }
        }
    }
}

/*
 * Scalar FP32 GEMM: C[M,N] = alpha * A[M,K] * B[K,N] + beta * C[M,N]
 *
 * Standard GEMM with alpha/beta scaling.
 * Loop order: i,k,j for better cache behavior on row-major matrices.
 */
void gemm_fp32_scalar(int M, int N, int K,
                      float alpha,
                      const float *A, int lda,
                      const float *B, int ldb,
                      float beta,
                      float *C, int ldc) {
    /* Scale C by beta (or zero if beta == 0) */
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            C[i * ldc + j] *= beta;
        }
    }

    /* Accumulate: C[i][j] += alpha * A[i][k] * B[k][j] */
    for (int i = 0; i < M; i++) {
        for (int k = 0; k < K; k++) {
            float a_scaled = alpha * A[i * lda + k];
            for (int j = 0; j < N; j++) {
                C[i * ldc + j] += a_scaled * B[k * ldb + j];
            }
        }
    }
}
