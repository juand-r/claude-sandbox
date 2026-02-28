# Plan: Vectorize quantize_per_column with AVX-512

## Problem

`quantize_per_column` is the bottleneck preventing INT8 backward from being
faster than FP32 backward. At dim=1024, it adds +101 ms overhead per step
while INT8 GEMM only saves 5 ms.

The current implementation has two cache-unfriendly passes:
1. **absmax per column**: iterates column-by-column with stride=`cols` (cache miss every access)
2. **quantize per element**: row-major but recomputes `1.0/scales[j]` each row

## Approach: Row-Major Tiled AVX-512

Key insight: per-column statistics can be computed row-major by maintaining
a running max per column across rows. No transpose needed.

### Pass 1: Row-major absmax

Instead of iterating down each column (stride = cols*4 bytes, cache-hostile):
```c
// OLD: column-major iteration, 1 float per cache line used
for (int j = 0; j < cols; j++)
    for (int i = 0; i < rows; i++)
        amax[j] = max(amax[j], |src[i*cols + j]|);  // stride=cols
```

Iterate row-major and update 16 column-maxima simultaneously:
```c
// NEW: row-major, 16 columns per vector, full cache line utilization
float col_max[cols] = {0};  // fits in L1 for cols <= 4096 (16KB)
for (int i = 0; i < rows; i++) {
    for (int j = 0; j + 16 <= cols; j += 16) {
        __m512 v = _mm512_loadu_ps(src + i*cols + j);
        __m512 av = abs512(v);
        __m512 cur = _mm512_loadu_ps(col_max + j);
        _mm512_storeu_ps(col_max + j, _mm512_max_ps(cur, av));
    }
}
for (int j = 0; j < cols; j++)
    scales[j] = col_max[j] > 0 ? col_max[j] / 127.0f : 1.0f;
```

Why this is fast:
- Sequential memory access (row-major)
- Each `_mm512_loadu_ps` loads a full 64-byte cache line (16 floats)
- `col_max` array is only 4KB for dim=1024, fits in L1 cache
- Single pass over data

### Pass 2: Row-major vectorized quantize

```c
// Precompute inv_scales once (cols floats = 4KB for dim=1024)
float inv_scales[cols];
for (int j = 0; j < cols; j++)
    inv_scales[j] = 1.0f / scales[j];

#pragma omp parallel for schedule(static) if(rows >= 8)
for (int i = 0; i < rows; i++) {
    for (int j = 0; j + 16 <= cols; j += 16) {
        __m512 v = _mm512_loadu_ps(src + i*cols + j);
        __m512 is = _mm512_loadu_ps(inv_scales + j);
        __m512 scaled = _mm512_mul_ps(v, is);
        __m512i q32 = _mm512_cvtps_epi32(scaled);
        __m128i q8 = _mm512_cvtsepi32_epi8(q32);
        _mm_storeu_si128((__m128i *)(dst + i*cols + j), q8);
    }
    // scalar tail for cols not divisible by 16
}
```

## Call sites and matrix sizes (dim=1024)

1. **saved_input** (forward, every call when use_int8_backward):
   - [512 x 1024] for attn projections and output head (batch=512, in_f=1024)
   - [512 x 4096] for ffn_down (batch=512, in_f=4096)
   - Called 25 times per step

2. **weight** (forward, once per step via weights_dirty guard):
   - [1024 x 1024] for attn projections (out_f=1024, in_f=1024)
   - [4096 x 1024] for ffn_up (out_f=4096, in_f=1024)
   - [1024 x 4096] for ffn_down (out_f=1024, in_f=4096)
   - [128 x 1024] for output head
   - Called 7 times per step (4 attn + 2 FFN + 1 head), but guarded by weights_dirty

## OpenMP strategy

- **Pass 1 (absmax)**: Single-threaded. The entire matrix is ~2MB (512*1024*4),
  one sequential pass at ~30 GB/s takes < 0.1 ms. OMP overhead would exceed
  the computation. Could add per-thread accumulators + reduction later if needed.

- **Pass 2 (quantize)**: OMP parallel for on rows, same as current.

## Implementation steps

1. Add `quantize_per_column_avx512` to `quantize.c` with the row-major approach
2. Keep the scalar version as fallback
3. Add runtime dispatch in `quantize_per_column` (same pattern as existing code)
4. Add a test in `test_main.c`: compare AVX-512 vs scalar quantize_per_column output

## Correctness testing

- Generate random matrix [512 x 1024]
- Run both scalar and AVX-512 `quantize_per_column`
- Verify scales match exactly (float equality, since the max operation is deterministic)
- Verify quantized values match exactly (same rounding)
- Edge cases: zero columns, single-element rows, cols not divisible by 16

## Expected performance

Current per-column quantize overhead at dim=1024: ~101 ms/step across all calls.

Estimated after vectorization:
- Pass 1 (absmax): ~0.1 ms per call (was probably ~1-2 ms, mostly cache misses)
- Pass 2 (quantize): ~0.1 ms per call (was probably ~1-2 ms, partially cache-friendly)
- Total per call: ~0.2 ms (vs current ~3-4 ms)
- Total per step: ~5-8 ms (vs current ~101 ms)
- Net savings: ~93-96 ms

If this works, INT8 backward should be faster than FP32 backward by ~90 ms,
flipping the QAT+INT8bwd result from 1942 ms to ~1845 ms (vs QAT 1822 ms).
That would make it roughly break-even or slightly faster.

## Why not transpose?

Initially considered: transpose FP32 matrix → quantize per-row → transpose INT8 back.
Rejected because:
1. Requires 3 passes (transpose + quantize + transpose) vs 2 passes (absmax + quantize)
2. Two of the three passes involve scalar transposes (cache-unfriendly writes)
3. Needs temporary buffers for transposed FP32 and INT8 data
4. The row-major tiled approach is simpler, faster, and needs no extra buffers

## Risks

- The absmax pass is single-threaded. For very large matrices (dim=4096+), this
  might become a bottleneck. Can add OMP reduction if needed.
- The estimate assumes cache misses are the dominant cost. If the current code
  is actually compute-bound (unlikely at dim=1024), savings will be smaller.
- If INT8 backward still isn't faster after this, the remaining overhead is in
  the transpose+quantize of grad_output in the backward pass itself, which
  uses the same pattern and would benefit from the same optimization.
