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

### dim=512, 5K steps (before round 2 optimizations)
- FP32: ppl=8.65, 125.3 ms/step
- QAT:  ppl=8.75, 81.6 ms/step (**1.53x speedup**)
- QAT perplexity ratio: 1.011 (matches FP32)
- Generated text: sub-word fragments (underfitted, only 5K steps)

### After profiling + round 2 optimizations (profiler timings)
- FP32: 116.6 ms/step (-25.6%)
- QAT:  92.2 ms/step (-33.2%)
- Optimizations: AVX-512 Adam (-20.5 ms), AVX-512 GeLU with Padé tanh (-15.3 ms),
  weight quantization cache (-1.3 ms)

### dim=512, 15K steps (final run with all optimizations)
- FP32: ppl=6.14, 91.9 ms/step, 1378 sec (23 min)
- QAT:  ppl=6.56, 58.7 ms/step, 881 sec (15 min)
- **QAT speedup: 1.56x**
- **QAT perplexity ratio: 1.070** (7% quality gap)
- Generated text: word fragments and recognizable English words, not yet fluent

The core thesis is proven: INT8 QAT via VNNI gives real speedups at sufficient
GEMM sizes while preserving training quality.

### dim=512, batch=8, 5K steps (mini-batch implementation)
- FP32: ppl=4.48, BPB=2.163, 183.8 ms/step, 2785 tok/s, 0.1062 TFLOPS
- QAT:  ppl=4.48, BPB=2.164, 187.6 ms/step, 2729 tok/s, 0.1041 TFLOPS
- **QAT speedup: 0.98x** (no advantage — see below)
- **QAT perplexity ratio: 1.001** (essentially identical quality)
- Training time: FP32 919s, QAT 938s

**Key finding:** Mini-batching eliminated QAT's speed advantage. With batch=1,
the INT8 forward pass was a large fraction of total step time, so VNNI's 1.5x
speedup there translated to 1.56x overall. With batch=8, the FP32 backward pass
(identical in both modes) also benefits from larger GEMMs, and it dominates the
step time. The INT8 forward speedup is diluted.

**Upside:** Quality improved dramatically (ppl 6.14 -> 4.48 in fewer steps),
throughput tripled (~900 -> ~2700 tok/s), and MFU went from 1.5% to ~5%.

### dim=1024, batch=8, 300 steps (76M params, convergence run)
- FP32: ppl=12.52, BPB=3.647, 5552 ms/step, 184 tok/s, 1721 sec
- QAT:  ppl=12.39, BPB=3.631, 3761 ms/step, 272 tok/s, 1280 sec
- **QAT speedup: 1.36x**
- **QAT PPL ratio: 0.990** (QAT slightly better, within noise)

### dim=1024, batch=16, 300 steps (76M params, convergence run)
- FP32: ppl=12.13, BPB=3.601, 10932 ms/step, 187 tok/s, 3353 sec
- QAT:  ppl=12.16, BPB=3.604, 9289 ms/step, 220 tok/s, 3072 sec
- **QAT speedup: 1.08x**
- **QAT PPL ratio: 1.002** (essentially identical)

**Key finding:** At dim=1024 with 6 layers, QAT retains a meaningful speed
advantage even with batching (1.36x at BS=8, 1.08x at BS=16). This is better
than dim=512 (0.98x at BS=8), because the larger model has more forward-pass
compute to accelerate with INT8 VNNI. Quality is identical: convergence curves
track each other exactly at every checkpoint.

See CONVERGENCE_RUNS.md for detailed step-by-step comparisons.

## What's Missing / Possible Next Steps

### Quality improvements (generation quality)
- **Longer training at dim=512**: 5K steps is not enough for a 6.5M param model.
  The dim=128 run at 30K steps produced English words at ppl=6.3. A 15-30K step
  run at dim=512 should produce much better text (and lower perplexity). This is
  the most obvious next step — but it takes ~30-60 min wall clock.

### Performance improvements
- **KV cache for generation**: Currently generation recomputes the full sequence
  at each step. Doesn't affect training speed but matters for generation throughput.
- **AMX kernels**: The Xeon 8581C has AMX-INT8 and AMX-BF16 (tile matrix multiply).
  AMX-INT8 does 16x16 INT8 GEMMs per instruction — potentially much faster than
  VNNI for large matrices. Significant effort but hardware is available.
- **Parallelize attention head loop**: The per-head backward loop is sequential.
  With 8 heads and 16 cores, OpenMP could reduce the 22 ms attention backward.

### What's been done (profiling + optimization)
- **Profiling**: Done. See PROFILE_RESULTS.md for detailed breakdown.
- **AVX-512 Adam**: Done. -20.5 ms (-65%).
- **AVX-512 GeLU + fast Padé tanh**: Done. -15.3 ms (-98%).
- **Weight quantization cache**: Done. -1.3 ms (-3%).

### What NOT to do (diminishing returns)
- Flash attention: at seq=64, the attention matrix is 16KB per head, fits in L1.
- FP16/BF16 training: no native BF16 GEMM throughput advantage on this CPU.
- Softmax/RMSNorm vectorization: <1 ms each, not worth the complexity.
- Memory pool: allocation overhead is <0.5 ms total.
