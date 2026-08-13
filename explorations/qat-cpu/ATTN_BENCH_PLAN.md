# Attention Backward A/B Test Plan

## Goal

Measure the impact of two independent optimizations on attention backward:
1. **Head-first layout**: Store Q/K/V in [n_heads, B, S, head_dim] instead of [B*S, dim]
   - Eliminates extract_head/scatter_head from inner loop (4+3 = 7 calls per iteration)
   - Direct pointer access — GEMM reads/writes contiguous head data
2. **OpenMP outer-loop**: Parallelize the (b,h) loop with `#pragma omp parallel for`
   - 64 iterations (batch=8, heads=8) across 16 cores
   - Inner GEMMs run serial (nested OMP disabled by default)

## 2x2 Factorial Design

| Config | Layout | OMP outer loop | OMP in GEMM | How to run |
|--------|--------|---------------|-------------|------------|
| A | Interleaved (current) | No | Yes (default) | `attention_backward()` |
| B | Head-first | No | Yes (default) | `attention_backward_headfirst()` |
| C | Interleaved (current) | Yes | No (nested) | `attention_backward_omp()` |
| D | Head-first | Yes | No (nested) | `attention_backward_headfirst_omp()` |

Also run each with OMP_NUM_THREADS=1 as a single-threaded baseline.

## Implementation

### 1. Layout conversion helpers (in layers.c)

```c
// [B*S, dim] → [n_heads, B*S, head_dim]
static void interleaved_to_headfirst(...)

// [n_heads, B*S, head_dim] → [B*S, dim]
static void headfirst_to_interleaved(...)
```

### 2. attention_backward_headfirst() (in layers.c)

Same algorithm as attention_backward(), but:
- Convert saved_q/k/v, grad_attn_out to head-first at the start
- Inner loop: use direct pointers (no extract_head/scatter_head)
- Write grad_q/k/v directly in head-first format
- Convert grad_q/k/v back to interleaved at the end
- Workspace per iteration: v_h_t, grad_attn_w, grad_scores, grad_scores_t (4 buffers)

### 3. OMP variants

Add `#pragma omp parallel for` versions of both backward functions.
Collapse the two loops (b, h) into a single parallel loop.
Each thread needs private workspace buffers.

### 4. bench_attn.c

- Initialize Attention, run forward to populate saved state
- Time each backward variant, many iterations
- Verify numerical equivalence (max abs diff)
- Print results table

### 5. What to measure

- Wall time per backward call (averaged over 100+ iterations)
- Breakdown: time in conversion, time in loop
- Numerical correctness: max |diff| between variants

## Expected Results

- Head-first should save the extract/scatter overhead (~0.4ms at batch=1, ~3ms at batch=8)
- Outer-loop OMP with 16 cores on 64 iterations should give ~4-8x speedup on the loop
  (less than 16x due to memory bandwidth sharing)
- Combined (D) should give the best result
- The conversion overhead (7 passes over B*S*dim data) may offset some gains
