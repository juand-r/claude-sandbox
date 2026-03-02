# BF16 Backward GEMM Plan

## Motivation

QATLinear backward is 1573 ms (37.2% of step time) — all FP32 GEMMs.
AVX-512 BF16 (VDPBF16PS) is verified working on this CPU. This instruction
does 2 BF16 fused multiply-adds per FP32 lane (32 MACs/instruction vs 16
for VFMADD), and BF16 data is 2 bytes vs 4 — halving memory bandwidth
for the B matrix.

## Benchmark Results (prototype)

Tested a BF16 GEMM with B-prepacking against our current FP32 AVX-512 GEMM
at the actual backward pass sizes:

```
Size (MxNxK)       FP32 ms   BF16 ms   Speedup
512 x 1024 x 1024    5.84      2.93     1.99x
512 x 4096 x 1024   29.38     18.00     1.63x
1024 x 1024 x 512    4.28      2.27     1.88x
1024 x 512 x 4096   26.99     16.78     1.61x
64 x 128 x 64        0.02      0.03     0.69x  (SLOWER - don't use for attention)
```

BF16 is 1.6-2.0x faster for our backward GEMM sizes.
BF16 is SLOWER for attention head GEMMs (64x128x64) due to B-packing overhead.

Average relative error: 1.6-3.8%. This is fine for gradients — SGD noise
is much larger.

## Strategy

- Use BF16 GEMM **only** for QATLinear backward (large GEMMs)
- Keep FP32 GEMM for attention (small per-head GEMMs)
- BF16 GEMM has same function signature as FP32 GEMM (FP32 in/out, BF16 internal)

## VDPBF16PS Semantics

```c
__m512 _mm512_dpbf16_ps(__m512 src, __m512bh a, __m512bh b);
```

Each FP32 output lane i:
  dst[i] = src[i] + a_bf16[2i] * b_bf16[2i] + a_bf16[2i+1] * b_bf16[2i+1]

So each instruction does 16 FP32 outputs, each with 2 BF16 MACs = 32 MACs.
Compare: VFMADD does 16 FP32 MACs per instruction. VDPBF16PS is 2x.

BF16 format: top 16 bits of FP32 (1 sign + 8 exponent + 7 mantissa).
Convert FP32 -> BF16: just shift right 16 bits (truncation, not rounding).

## Implementation Plan

### Step 1: kernels_bf16.c — BF16 FP32 GEMM kernel

New file compiled with `-mavx512bf16 -mavx512f -mavx512bw`.

```c
void gemm_fp32_bf16(int M, int N, int K, float alpha,
                    const float *A, int lda,
                    const float *B, int ldb,
                    float beta, float *C, int ldc);
```

Algorithm:
1. **Pack B[K x N] into BF16 pairs**: for each k-pair (k, k+1), convert
   B[k][j] and B[k+1][j] to BF16, pack as [bf16_lo, bf16_hi] in one uint32.
   Layout: packed_b[k2 * N + j] = (bf16(B[2*k2+1][j]) << 16) | bf16(B[2*k2][j])

2. **GEMM loop** (OpenMP over M rows):
   - Apply beta to C row (zero if beta=0, scale if beta!=0)
   - For each k-pair:
     - Broadcast A[i][2*k2] and A[i][2*k2+1] as a BF16 pair
     - For each 16-wide N strip:
       - Load packed_b as __m512bh
       - c_v = _mm512_dpbf16_ps(c_v, a_bh, b_bh)
   - Handle K tail (odd K) with scalar FMA
   - Apply alpha if != 1.0

### Step 2: Makefile — add BF16 compilation

```makefile
CFLAGS_BF16 = $(CFLAGS_BASE) -mavx512f -mavx512bw -mavx512bf16
SRC_BF16 = kernels_bf16.c
OBJ_BF16 = $(SRC_BF16:.c=.o)
```

### Step 3: qat_cpu.h — add BF16 GEMM to dispatch

```c
typedef struct {
    gemm_int8_fn  int8_gemm;
    gemm_fp32_fn  fp32_gemm;
    gemm_fp32_fn  bf16_gemm;    /* NEW: BF16 GEMM for large matrices, NULL if unavailable */
    const char   *int8_name;
    const char   *fp32_name;
    const char   *bf16_name;    /* NEW */
} KernelDispatch;
```

### Step 4: dispatch.c — select BF16 GEMM when available

```c
if (cpu->has_avx512bf16) {
    kd->bf16_gemm = gemm_fp32_bf16;
    kd->bf16_name = "AVX-512 BF16";
} else {
    kd->bf16_gemm = kd->fp32_gemm;  /* fall back to FP32 */
    kd->bf16_name = "N/A (using FP32)";
}
```

### Step 5: qat_linear.c — use BF16 in backward

Replace `fp32_gemm` calls in `qat_linear_backward()` with `bf16_gemm`:

```c
/* GEMM 1: grad_input */
layer->kernels->bf16_gemm(batch, in_f, out_f, 1.0f,
                           grad_output->data, out_f,
                           layer->weight->data, in_f,
                           0.0f, grad_input->data, in_f);

/* GEMM 2: grad_weight (accumulate) */
layer->kernels->bf16_gemm(out_f, in_f, batch, 1.0f,
                           grad_output_t, batch,
                           layer->saved_input->data, in_f,
                           1.0f, layer->grad_weight->data, in_f);
```

Attention backward stays on `fp32_gemm` (small GEMMs, BF16 is slower).

### Step 6: Test correctness

- Existing test_qat GEMM tests with BF16 kernel
- New test: BF16 GEMM vs FP32 GEMM, verify max relative error < 5%
- Short training run: verify convergence not degraded

### Step 7: Profile

Run profile_qat and compare:
- QATLinear backward time (target: 1573 → ~900-1000 ms)
- Total step time (target: 4231 → ~3600-3800 ms)

## Backward Pass GEMM Details

Per layer backward (FP32 path, lines 320-341 of qat_linear.c):

```
GEMM 1: grad_input = grad_output * weight
  fp32_gemm(M=batch, N=in_f, K=out_f, alpha=1, ..., beta=0, ...)
  Sizes: [512 x in_f] = [512 x out_f] * [out_f x in_f]

GEMM 2: grad_weight += grad_output^T * saved_input
  fp32_gemm(M=out_f, N=in_f, K=batch, alpha=1, ..., beta=1, ...)
  Sizes: [out_f x in_f] = [out_f x 512] * [512 x in_f]
```

Layer types and GEMM sizes (per block, 6 blocks total):
| Layer    | out_f | in_f | GEMM 1 (MxNxK)     | GEMM 2 (MxNxK)     |
|----------|-------|------|---------------------|---------------------|
| q_proj   | 1024  | 1024 | 512 x 1024 x 1024  | 1024 x 1024 x 512  |
| k_proj   | 1024  | 1024 | 512 x 1024 x 1024  | 1024 x 1024 x 512  |
| v_proj   | 1024  | 1024 | 512 x 1024 x 1024  | 1024 x 1024 x 512  |
| o_proj   | 1024  | 1024 | 512 x 1024 x 1024  | 1024 x 1024 x 512  |
| up_proj  | 4096  | 1024 | 512 x 1024 x 4096  | 4096 x 1024 x 512  |
| gate_proj| 4096  | 1024 | 512 x 1024 x 4096  | 4096 x 1024 x 512  |
| down_proj| 1024  | 4096 | 512 x 4096 x 1024  | 1024 x 4096 x 512  |

Plus output head (1024 x vocab=128): too small, BF16 won't help much.

## Expected Savings

Using measured speedups per GEMM size:
- 512x1024x1024 at 1.99x: 24 calls × 6 blocks, dominant for q/k/v/o
- 512x4096x1024 at 1.63x: mixed up/gate/down
- 1024x1024x512 at 1.88x: weight grad for q/k/v/o
- 1024x512x4096 at 1.61x: weight grad for down

Weighted estimate: ~1.7x average across all backward GEMMs.
- QATLinear backward: 1573 → ~925 ms (save ~650 ms)
- Total step: 4231 → ~3580 ms (1.18x speedup)

## Risks

1. **Gradient precision**: BF16 mantissa is 7 bits vs FP32's 23 bits.
   Average relative error is 1.6-3.8%. This should be fine for gradients
   (SGD noise is much larger), but need to verify convergence.

2. **K-tail handling**: When K is odd, the last element can't pair up.
   Handle with a scalar FP32 FMA for the tail. All our K values are even
   (512, 1024, 4096) so this shouldn't matter in practice.

3. **B-packing overhead**: Currently done inside the GEMM call. For GEMM 1,
   B=weight is the same across all batch items — could pre-pack once per step.
   Optimization for later if needed.
