# Attention Backward A/B Test Results

## Setup
- Model: dim=512, n_heads=8, head_dim=64
- Batch=8, seq_len=64 (64 total (b,h) iterations)
- CPU: Intel Xeon Platinum 8581C, 16 cores, AVX-512
- 5 warmup + 50 timed iterations

## 2x2 Factorial Results

### With 16 OMP threads (default)

| Config | Layout | OMP outer loop | Time (ms) | Speedup |
|--------|--------|---------------|-----------|---------|
| A | Interleaved (current) | No | 22.16 | 1.00x |
| B | Head-first | No | 25.98 | 0.85x |
| C | Interleaved | Yes | **16.96** | **1.31x** |
| D | Head-first | Yes | 22.29 | 0.99x |

### Single-threaded (OMP_NUM_THREADS=1)

| Config | Time (ms) | Speedup |
|--------|-----------|---------|
| A | 83.74 | 1.00x |
| B | 83.95 | 1.00x |
| C | 82.39 | 1.02x |
| D | 85.60 | 0.98x |

## Key Findings

1. **Head-first layout provides no benefit.** The layout conversion overhead
   (~4 ms for 7 passes over B*S*dim data) eliminates any gains from removing
   extract_head/scatter_head. The total data movement is the same in both
   layouts; the conversion just adds an extra full copy at the start and end.

2. **Outer-loop OpenMP is the clear winner (1.31x).** Distributing 64 (b,h)
   iterations across 16 cores gives a genuine speedup. Each thread runs serial
   GEMMs (nested OpenMP disabled by default), avoiding thread contention.

3. **Single-threaded: all variants equal.** Confirms the layout change has
   no effect on the actual per-head computation speed.

4. **Best combo is just C (interleaved + outer OMP).** Adding head-first
   layout to OMP (config D) just adds conversion overhead.

## Impact on Full Training Step

With attention backward at ~22 ms / ~24% of a ~92 ms step (QAT mode):
- Config C saves 5.2 ms → ~5.6% faster per step
- New step time: ~87 ms (estimated)

## Recommendation

Use `attention_backward_omp()` (Config C) as the default backward pass.
The head-first layout variants can be removed — they add complexity for no gain.
