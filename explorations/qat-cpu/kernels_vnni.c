/*
 * kernels_vnni.c - AVX-512 VNNI INT8 GEMM + AVX-512 FP32 GEMM
 *
 * INT8: Uses VPDPBUSD - 64 uint8*int8 MACs per instruction into 16 int32.
 *       B-matrix is prepacked into VNNI-friendly layout at GEMM start.
 * FP32: Uses VFMADD231PS (512-bit) - 16 FP32 FMAs per instruction.
 *
 * Compile with: -mavx512f -mavx512bw -mavx512vnni -mavx512vl
 *
 * VPDPBUSD semantics: for each of 16 int32 lanes:
 *   dst[i] += (u8[4i+0]*i8[4i+0] + u8[4i+1]*i8[4i+1] +
 *              u8[4i+2]*i8[4i+2] + u8[4i+3]*i8[4i+3])
 * So it does 4 uint8*int8 products per int32 lane, 16 lanes = 64 MACs.
 *
 * Unsigned trick: convert signed A -> unsigned by adding 128,
 * then correct with: C_true = C_computed - 128 * col_sums(B)
 */

#include "qat_cpu.h"
#include <immintrin.h>

/*
 * AVX-512 VNNI INT8 GEMM: C_i32[M,N] = A_i8[M,K] * B_i8[K,N]
 *
 * Optimization: B is prepacked into VNNI-interleaved format once at the
 * start, then reused for all M rows of A. This eliminates the O(M*N*K)
 * scattered loads that dominated the previous implementation.
 *
 * Strategy:
 *   1. Prepack B[K,N] into VNNI layout: for each 16-column strip and
 *      4-row strip, interleave 4 k-values into int32 lanes via SIMD shuffles.
 *   2. Precompute correction = 128 * col_sums(B) for unsigned trick.
 *   3. GEMM loop: sequential loads from prepacked B, one VPDPBUSD per chunk.
 */
void gemm_int8_vnni(int M, int N, int K,
                    const int8_t *A, int lda,
                    const int8_t *B, int ldb,
                    int32_t *C, int ldc) {
    int n_full = N / 16;        /* Number of full 16-wide strips */
    int n_tail = N % 16;
    int n_strips = n_full + (n_tail > 0 ? 1 : 0);
    int k_full = K / 4;         /* Number of full 4-wide k-strips */
    int k_tail = K % 4;
    int k_strips = k_full + (k_tail > 0 ? 1 : 0);

    /*
     * Step 1: Prepack B into VNNI format.
     *
     * For each 16-column strip js and 4-row strip ks, we produce a 64-byte
     * chunk where byte[dj*4+dk] = B[(ks*4+dk)*ldb + (js*16+dj)].
     *
     * For full strips (both j and k), we use SIMD interleave:
     *   Load 4 rows of 16 bytes -> unpacklo/hi -> interleave into VNNI layout.
     *
     * Layout: packed_b[(js * k_strips + ks) * 64 ... + 63]
     */
    size_t pack_bytes = (size_t)n_strips * k_strips * 64;
    int8_t *packed_b = (int8_t *)qat_alloc(pack_bytes);
    memset(packed_b, 0, pack_bytes);

    /* Pack full j-strips with SIMD interleave */
    for (int js = 0; js < n_full; js++) {
        int j = js * 16;

        /* Full k-strips: SIMD 4-row interleave */
        for (int ks = 0; ks < k_full; ks++) {
            int k = ks * 4;
            int8_t *dest = packed_b + (size_t)(js * k_strips + ks) * 64;

            /* Load 4 rows of 16 bytes each */
            __m128i r0 = _mm_loadu_si128((const __m128i *)&B[(k + 0) * ldb + j]);
            __m128i r1 = _mm_loadu_si128((const __m128i *)&B[(k + 1) * ldb + j]);
            __m128i r2 = _mm_loadu_si128((const __m128i *)&B[(k + 2) * ldb + j]);
            __m128i r3 = _mm_loadu_si128((const __m128i *)&B[(k + 3) * ldb + j]);

            /*
             * Interleave to produce VNNI layout:
             *   Lane L (int32): [B[k][j+L], B[k+1][j+L], B[k+2][j+L], B[k+3][j+L]]
             *
             * Step 1: Interleave bytes from row pairs
             *   lo01[i] = [r0[i], r1[i]] for i=0..7 (as 16-bit pairs)
             *   lo23[i] = [r2[i], r3[i]] for i=0..7
             * Step 2: Interleave 16-bit pairs into 32-bit lanes
             *   ll[i] = [r0[i], r1[i], r2[i], r3[i]] for i=0..3
             */
            __m128i lo01 = _mm_unpacklo_epi8(r0, r1);
            __m128i hi01 = _mm_unpackhi_epi8(r0, r1);
            __m128i lo23 = _mm_unpacklo_epi8(r2, r3);
            __m128i hi23 = _mm_unpackhi_epi8(r2, r3);

            __m128i ll = _mm_unpacklo_epi16(lo01, lo23);  /* dj 0..3 */
            __m128i lh = _mm_unpackhi_epi16(lo01, lo23);  /* dj 4..7 */
            __m128i hl = _mm_unpacklo_epi16(hi01, hi23);  /* dj 8..11 */
            __m128i hh = _mm_unpackhi_epi16(hi01, hi23);  /* dj 12..15 */

            /* Combine into 512-bit register and store */
            __m512i packed = _mm512_inserti32x4(
                _mm512_inserti32x4(
                    _mm512_inserti32x4(
                        _mm512_castsi128_si512(ll), lh, 1),
                    hl, 2),
                hh, 3);
            _mm512_store_si512((__m512i *)dest, packed);
        }

        /* K-tail: scalar packing for remaining k values */
        if (k_tail > 0) {
            int k = k_full * 4;
            int8_t *dest = packed_b + (size_t)(js * k_strips + k_full) * 64;
            for (int dj = 0; dj < 16; dj++) {
                for (int dk = 0; dk < k_tail; dk++) {
                    dest[dj * 4 + dk] = B[(k + dk) * ldb + j + dj];
                }
            }
        }
    }

    /* N-tail strip: scalar packing (< 16 columns remaining) */
    if (n_tail > 0) {
        int j = n_full * 16;
        for (int ks = 0; ks < k_strips; ks++) {
            int k = ks * 4;
            int k_count = (ks < k_full) ? 4 : k_tail;
            int8_t *dest = packed_b + (size_t)(n_full * k_strips + ks) * 64;
            for (int dj = 0; dj < n_tail; dj++) {
                for (int dk = 0; dk < k_count; dk++) {
                    dest[dj * 4 + dk] = B[(k + dk) * ldb + j + dj];
                }
            }
        }
    }

    /*
     * Step 2: Precompute correction for unsigned trick.
     * correction[j] = 128 * sum_k B[k][j]
     *
     * This is the same for all rows of A, so compute it once.
     */
    int32_t *correction = (int32_t *)qat_alloc((size_t)n_strips * 16 * sizeof(int32_t));
    memset(correction, 0, (size_t)n_strips * 16 * sizeof(int32_t));

    /* Full j-strips: vectorized column sum accumulation */
    for (int k = 0; k < K; k++) {
        for (int js = 0; js < n_full; js++) {
            int j = js * 16;
            __m128i b_bytes = _mm_loadu_si128((const __m128i *)&B[k * ldb + j]);
            __m512i b_ext = _mm512_cvtepi8_epi32(b_bytes);
            __m512i cur = _mm512_loadu_si512((const __m512i *)&correction[js * 16]);
            cur = _mm512_add_epi32(cur, b_ext);
            _mm512_storeu_si512((__m512i *)&correction[js * 16], cur);
        }
        /* N-tail: scalar column sum */
        if (n_tail > 0) {
            int j = n_full * 16;
            for (int dj = 0; dj < n_tail; dj++) {
                correction[n_full * 16 + dj] += (int32_t)B[k * ldb + j + dj];
            }
        }
    }

    /* Multiply column sums by 128 */
    for (int js = 0; js < n_strips; js++) {
        __m512i c = _mm512_loadu_si512((const __m512i *)&correction[js * 16]);
        c = _mm512_mullo_epi32(c, _mm512_set1_epi32(128));
        _mm512_storeu_si512((__m512i *)&correction[js * 16], c);
    }

    /*
     * Step 3: GEMM using prepacked B.
     *
     * For each row i of A, for each 16-column strip js:
     *   acc = sum over k-strips of VPDPBUSD(a_unsigned, packed_b[js][ks])
     *   result = acc - correction[js]
     *
     * OpenMP: each row of C is independent.
     */
    #pragma omp parallel for schedule(static) if(M >= 8)
    for (int i = 0; i < M; i++) {
        for (int js = 0; js < n_strips; js++) {
            __m512i acc = _mm512_setzero_si512();

            const int8_t *pb_base = packed_b + (size_t)js * k_strips * 64;

            for (int ks = 0; ks < k_strips; ks++) {
                int k = ks * 4;

                /* Pack A[i][k..k+3] as unsigned: add 128 to each byte */
                int k_count = (ks < k_full) ? 4 : k_tail;
                uint8_t ua[4] = {0, 0, 0, 0};
                for (int dk = 0; dk < k_count; dk++) {
                    ua[dk] = (uint8_t)((int16_t)A[i * lda + k + dk] + 128);
                }
                int32_t a_pat = (uint32_t)ua[0] | ((uint32_t)ua[1] << 8) |
                                ((uint32_t)ua[2] << 16) | ((uint32_t)ua[3] << 24);
                __m512i a_vec = _mm512_set1_epi32(a_pat);

                /* Load prepacked B chunk (64-byte aligned, sequential) */
                __m512i b_vec = _mm512_load_si512(
                    (const __m512i *)(pb_base + (size_t)ks * 64));

                /* VPDPBUSD: acc += dot4(a_unsigned, b_signed) per lane */
                acc = _mm512_dpbusd_epi32(acc, a_vec, b_vec);
            }

            /* Apply unsigned correction: subtract 128 * col_sums */
            __m512i corr = _mm512_load_si512(
                (const __m512i *)&correction[js * 16]);
            acc = _mm512_sub_epi32(acc, corr);

            /* Store result */
            int j = js * 16;
            if (js < n_full) {
                _mm512_storeu_si512((__m512i *)&C[i * ldc + j], acc);
            } else {
                /* Masked store for N-tail */
                __mmask16 mask = (__mmask16)((1u << n_tail) - 1);
                _mm512_mask_storeu_epi32(&C[i * ldc + j], mask, acc);
            }
        }
    }

    qat_free(packed_b);
    qat_free(correction);
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

    #pragma omp parallel for schedule(static) if(M >= 8)
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
