/*
 * kernels_bf16.c - AVX-512 BF16 FP32 GEMM
 *
 * Uses VDPBF16PS: 2 BF16 fused multiply-adds per FP32 lane per instruction.
 * 32 BF16 MACs per instruction vs 16 FP32 MACs for VFMADD = 2x compute.
 * BF16 data is 2 bytes vs 4 = halved memory bandwidth for B matrix.
 *
 * B matrix is prepacked into BF16 pairs: for each pair of K rows (k, k+1),
 * two BF16 values are packed into one uint32 lane.
 *
 * Compile with: -mavx512f -mavx512bw -mavx512bf16
 *
 * VDPBF16PS semantics (per FP32 lane i):
 *   dst[i] = src[i] + a_bf16[2i]*b_bf16[2i] + a_bf16[2i+1]*b_bf16[2i+1]
 */

#include "qat_cpu.h"
#include <immintrin.h>

/*
 * AVX-512 BF16 FP32 GEMM: C[M,N] = alpha * A[M,K] * B[K,N] + beta * C[M,N]
 *
 * Takes FP32 inputs, converts to BF16 internally, outputs FP32.
 * B is prepacked into BF16 pairs for VDPBF16PS.
 *
 * Strategy:
 *   1. Prepack B into BF16 pair format: each uint32 holds two BF16 values
 *      from consecutive K rows for the same N column.
 *   2. GEMM loop: broadcast A pairs as BF16, dot-product with packed B.
 */
void gemm_fp32_bf16(int M, int N, int K,
                    float alpha,
                    const float *A, int lda,
                    const float *B, int ldb,
                    float beta,
                    float *C, int ldc) {
    int K2 = K / 2;         /* Number of k-pairs */
    int K_even = K2 * 2;
    int n16 = N - (N % 16); /* 16 FP32 output lanes per VDPBF16PS */

    /*
     * Step 1: Prepack B[K,N] into BF16 pairs.
     *
     * For each k-pair (2*k2, 2*k2+1) and column j:
     *   packed_b[k2 * N + j] = bf16(B[2*k2][j]) | (bf16(B[2*k2+1][j]) << 16)
     *
     * This puts two BF16 values into one uint32 slot, matching VDPBF16PS layout.
     */
    uint32_t *packed_b = (uint32_t *)qat_alloc((size_t)K2 * N * sizeof(uint32_t));

    for (int k2 = 0; k2 < K2; k2++) {
        int k = k2 * 2;
        int j;
        for (j = 0; j < n16; j += 16) {
            /* Load two rows of 16 FP32 values */
            __m512 b0 = _mm512_loadu_ps(&B[(k + 0) * ldb + j]);
            __m512 b1 = _mm512_loadu_ps(&B[(k + 1) * ldb + j]);

            /* Convert FP32 -> BF16 (truncate to top 16 bits) */
            __m256bh b0_bh = _mm512_cvtneps_pbh(b0);
            __m256bh b1_bh = _mm512_cvtneps_pbh(b1);

            /* Interleave into uint32 pairs: [bf16_lo, bf16_hi] per lane */
            __m512i b0_32 = _mm512_cvtepu16_epi32((__m256i)b0_bh);
            __m512i b1_32 = _mm512_cvtepu16_epi32((__m256i)b1_bh);
            __m512i packed = _mm512_or_si512(b0_32,
                                             _mm512_slli_epi32(b1_32, 16));
            _mm512_storeu_si512((__m512i *)&packed_b[k2 * N + j], packed);
        }
        /* Scalar tail for N % 16 */
        for (; j < N; j++) {
            uint32_t b0_bits, b1_bits;
            memcpy(&b0_bits, &B[(k + 0) * ldb + j], 4);
            memcpy(&b1_bits, &B[(k + 1) * ldb + j], 4);
            uint16_t b0_bf16 = (uint16_t)(b0_bits >> 16);
            uint16_t b1_bf16 = (uint16_t)(b1_bits >> 16);
            packed_b[k2 * N + j] = (uint32_t)b0_bf16 | ((uint32_t)b1_bf16 << 16);
        }
    }

    /*
     * Step 2: GEMM using VDPBF16PS.
     *
     * For each row i of A, for each k-pair:
     *   Broadcast [bf16(A[i][2k2]), bf16(A[i][2k2+1])] to all 16 lanes
     *   c[j] += a_bf16_lo * b_bf16_lo + a_bf16_hi * b_bf16_hi
     *
     * OpenMP: each row of C is independent.
     */
    #pragma omp parallel for schedule(static) if(M >= 8)
    for (int i = 0; i < M; i++) {
        /* Apply beta to C row */
        if (beta == 0.0f) {
            int j;
            for (j = 0; j < n16; j += 16)
                _mm512_storeu_ps(&C[i * ldc + j], _mm512_setzero_ps());
            for (; j < N; j++)
                C[i * ldc + j] = 0.0f;
        } else if (beta != 1.0f) {
            __m512 beta_v = _mm512_set1_ps(beta);
            int j;
            for (j = 0; j < n16; j += 16) {
                __m512 c_v = _mm512_loadu_ps(&C[i * ldc + j]);
                _mm512_storeu_ps(&C[i * ldc + j], _mm512_mul_ps(c_v, beta_v));
            }
            for (; j < N; j++)
                C[i * ldc + j] *= beta;
        }
        /* beta==1.0: leave C as-is (accumulate mode) */

        /* BF16 dot-product accumulation over k-pairs */
        for (int k2 = 0; k2 < K2; k2++) {
            int k = k2 * 2;

            /* Convert A[i][k] and A[i][k+1] to BF16, pack into uint32 */
            uint32_t a0_bits, a1_bits;
            memcpy(&a0_bits, &A[i * lda + k], 4);
            memcpy(&a1_bits, &A[i * lda + k + 1], 4);
            uint16_t a0_bf16 = (uint16_t)(a0_bits >> 16);
            uint16_t a1_bf16 = (uint16_t)(a1_bits >> 16);
            uint32_t a_pair = (uint32_t)a0_bf16 | ((uint32_t)a1_bf16 << 16);
            __m512bh a_bh = (__m512bh)_mm512_set1_epi32((int32_t)a_pair);

            int j;
            for (j = 0; j < n16; j += 16) {
                __m512 c_v = _mm512_loadu_ps(&C[i * ldc + j]);
                __m512bh b_bh = (__m512bh)_mm512_loadu_si512(
                    (const __m512i *)&packed_b[k2 * N + j]);
                c_v = _mm512_dpbf16_ps(c_v, a_bh, b_bh);
                _mm512_storeu_ps(&C[i * ldc + j], c_v);
            }
            /* Scalar tail for N % 16: use FP32 */
            float a0 = A[i * lda + k];
            float a1 = A[i * lda + k + 1];
            for (; j < N; j++) {
                C[i * ldc + j] += a0 * B[(k + 0) * ldb + j]
                                + a1 * B[(k + 1) * ldb + j];
            }
        }

        /* K tail: if K is odd, handle last element with scalar FP32 */
        if (K_even < K) {
            float a_val = A[i * lda + K_even];
            int j;
            for (j = 0; j < n16; j += 16) {
                __m512 a_v = _mm512_set1_ps(a_val);
                __m512 b_v = _mm512_loadu_ps(&B[K_even * ldb + j]);
                __m512 c_v = _mm512_loadu_ps(&C[i * ldc + j]);
                c_v = _mm512_fmadd_ps(a_v, b_v, c_v);
                _mm512_storeu_ps(&C[i * ldc + j], c_v);
            }
            for (; j < N; j++)
                C[i * ldc + j] += a_val * B[K_even * ldb + j];
        }

        /* Apply alpha if needed */
        if (alpha != 1.0f) {
            __m512 alpha_v = _mm512_set1_ps(alpha);
            int j;
            for (j = 0; j < n16; j += 16) {
                __m512 c_v = _mm512_loadu_ps(&C[i * ldc + j]);
                _mm512_storeu_ps(&C[i * ldc + j], _mm512_mul_ps(c_v, alpha_v));
            }
            for (; j < N; j++)
                C[i * ldc + j] *= alpha;
        }
    }

    qat_free(packed_b);
}
