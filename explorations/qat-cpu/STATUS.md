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

## Current Profile at dim=1024, batch=8 (QAT mode, 4231 ms/step)

```
QATLinear backward:  1573 ms  (37.2%)  -- FP32 GEMMs (grad_input + grad_weight)
QATLinear forward:    982 ms  (23.2%)  -- INT8 VNNI GEMMs + quantize/dequant
Attention backward:   826 ms  (19.5%)  -- small FP32 GEMMs (128x128 per head)
Attention forward:    471 ms  (11.1%)  -- small FP32 GEMMs (128x128 per head)
Optimizer (Adam):     112 ms   (2.6%)
RMSNorm:               72 ms   (1.7%)
GeLU:                   58 ms   (1.4%)
Residual + copies:      57 ms   (1.3%)
Everything else:        ~3 ms
```

QATLinear fwd+bwd = 60% of step time. Attention fwd+bwd = 31%. These are the
only targets worth attacking.

## What's Missing / Possible Next Steps

### Next performance targets (ranked by expected impact)

#### 1. ~~AMX-INT8 for QATLinear forward~~ BLOCKED
CPUID reports AMX-INT8/AMX-BF16/AMX-TILE and XCR0 has bits 17+18 set, but
AMX instructions cause SIGILL. arch_prctl(ARCH_REQ_XCOMP_PERM) returns EINVAL.
Container/VM does not expose AMX hardware. See AMX_PLAN.md for full research
(preserved for bare-metal access).

#### 1 (revised). ~~AVX-512 BF16 backward GEMMs~~ TESTED — NO BENEFIT
Implemented and tested (converge_bs8_bf16bwd.csv, 300 steps). Results:
- Speed: 4158 ms/step avg vs 3997 ms/step for FP32 backward — **4% slower**
- Quality: PPL 12.57 vs 12.39 (old QAT) — **0.18 ppl worse**
The on-the-fly FP32→BF16 conversion overhead negated the VDPBF16PS compute
advantage. The standalone GEMM benchmark showed 1.5-1.6x, but the conversion
cost adds up across 42 GEMM calls per step. Additionally, the 8-bit mantissa
introduced gradient noise similar to (but less than) INT8 backward.
**Verdict**: Revert to FP32 backward. BF16 backward is not viable without
pre-packed BF16 weight storage (which would add significant complexity).

#### 2. AVX-512 BF16 for attention GEMMs (826+471 = 1297 ms, 31%)
The attention forward/backward use FP32 GEMM. Same BF16 GEMM kernel can
serve these too — just call gemm_bf16 instead of gemm_fp32 for attention.
Since the attention GEMMs are 128x128 per head (small), the benefit comes
primarily from halved memory bandwidth.
- Estimated savings: 200-400 ms/step
- Effort: low (reuse BF16 GEMM from #1)
- Risk: low

#### 3. Cache-tiled GEMMs (applies to all GEMM paths)
Current GEMMs are naive row-parallel. At 1024x4096, the working set exceeds
L1/L2 cache. Tiling (e.g., 64x64 or 128x128 blocks) would improve cache reuse.
This helps all GEMM paths but is fiddly to implement correctly.
- Estimated savings: 10-20% across all GEMMs (~200-400 ms/step)
- Effort: high (micro-kernel design, tuning)
- Risk: low (pure optimization, no semantic change)

### Theoretical speed ceiling (with AVX-512 BF16, no AMX)

If BF16 gives ~1.5x on FP32 GEMMs (conservative, memory-bandwidth limited):
- QATLinear fwd: 982 ms (unchanged, already INT8)
- QATLinear bwd: 1573 → ~1050 ms
- Attn fwd: 471 → ~314 ms
- Attn bwd: 826 → ~550 ms
- Other: ~302 ms (unchanged)
- Total: ~3198 ms/step (1.32x over current)

If BF16 gives ~2x (optimistic, compute-limited regime):
- QATLinear bwd: 1573 → ~786 ms
- Attn fwd+bwd: 1297 → ~649 ms
- Total: ~2719 ms/step (1.56x over current)

Combined with cache tiling: plausible floor ~2400-2800 ms/step (1.5-1.8x).

### What's been done (profiling + optimization)
- **Profiling**: Done. See PROFILE_RESULTS.md for detailed breakdown.
- **AVX-512 Adam**: Done. -20.5 ms (-65%) at dim=512.
- **AVX-512 GeLU + fast Padé tanh**: Done. -15.3 ms (-98%) at dim=512.
- **Weight quantization cache**: Done. -1.3 ms (-3%) at dim=512.
- **OpenMP attention fwd+bwd**: Done. Parallelized head loops in attention.
- **INT8 backward exploration**: Tested, no quality benefit vs FP32 backward.
  See INT8_BACKWARD_PLAN.md.

### What NOT to do (diminishing returns at dim=1024)
- Flash attention: at seq=64, the attention matrix is 16KB per head, fits in L1.
- Softmax/RMSNorm vectorization: 72 ms combined (1.7%), not worth the complexity
  relative to the GEMM bottleneck.
- Memory pool: allocation overhead is negligible.
- INT8 backward: tested, doesn't help (see INT8_BACKWARD_PLAN.md).
