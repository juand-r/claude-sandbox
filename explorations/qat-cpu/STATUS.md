# QAT-CPU Project Status

## What's Done

All 7 phases from PLAN.md are complete:

1. **Foundation** - memory, tensors, RNG, CPU detection
2. **GEMM Kernels** - scalar, AVX2, AVX-512 VNNI (INT8 + FP32)
3. **Quantization** - per-channel weight, per-token activation, AVX-512 vectorized
4. **QAT Linear** - INT8 forward + STE backward, pre-allocated buffers
5. **Transformer** - RMSNorm, GeLU, causal attention, residual blocks
6. **Training Loop** - Adam optimizer, cross-entropy loss, eval/generation
7. **Scaling** - GEMM-based attention, AVX-512 quantize, OpenMP, dim=512

## Key Results

### dim=128, 30K steps
- FP32: ppl=6.32, 14.2 ms/step
- QAT:  ppl=6.59, 16.1 ms/step (0.88x, QAT still slower due to small GEMM)
- Generated text: recognizable English words

### dim=512, 5K steps
- FP32: ppl=8.65, 125.3 ms/step
- QAT:  ppl=8.75, 81.6 ms/step (**1.53x speedup**)
- QAT perplexity ratio: 1.011 (matches FP32)
- Generated text: sub-word fragments (underfitted, only 5K steps)

The core thesis is proven: INT8 QAT via VNNI gives real speedups at sufficient
GEMM sizes while preserving training quality.

## What's Missing / Possible Next Steps

### Quality improvements (generation quality)
- **Longer training at dim=512**: 5K steps is not enough for a 6.5M param model.
  The dim=128 run at 30K steps produced English words at ppl=6.3. A 15-30K step
  run at dim=512 should produce much better text (and lower perplexity). This is
  the most obvious next step — but it takes ~30-60 min wall clock.

### Performance improvements
- **KV cache for generation** (opt #4 in notes): Currently generation recomputes
  the full sequence at each step. A KV cache would make generation O(seq*dim)
  instead of O(seq^2*dim). Doesn't affect training speed but matters if we care
  about generation throughput.
- **NUMA-aware allocation**: On multi-socket systems, memory placement matters.
  Not critical on our single-socket Xeon but would be needed for production.
- **Gradient accumulation**: Simulate larger batch sizes. Would improve training
  stability/quality but doesn't change the QAT vs FP32 comparison.
- **AMX kernels**: The Xeon 8581C has AMX-INT8 and AMX-BF16 (tile matrix
  multiply). AMX-INT8 does 16x16 INT8 GEMMs per instruction — potentially
  much faster than VNNI for large matrices. This would be a significant effort
  but the hardware is available.

### Architecture / code quality
- **Profiling**: We haven't done proper profiling to know the actual bottleneck
  breakdown (quantize vs GEMM vs attention vs optimizer). `perf` or VTune would
  tell us where the remaining time goes.
- **Memory pool**: Currently using posix_memalign per allocation. A pool allocator
  would reduce fragmentation and syscall overhead, especially in the attention
  forward/backward which mallocs ~7 temp buffers per call.
- **Batch dimension**: Currently batch=1 (one sequence per step). Batched training
  would improve GPU-style throughput but on CPU the benefit is less clear (we're
  already compute-bound at dim=512).

### What NOT to do (diminishing returns)
- Flash attention: at seq=64, the attention matrix is 16KB per head, fits in L1.
  No memory pressure to optimize.
- FP16/BF16 training: CPU doesn't benefit much from reduced precision in the
  backward pass (no native BF16 GEMM throughput advantage on this chip for
  training workloads).
