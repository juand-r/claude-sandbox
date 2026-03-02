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

#### 1. AMX-INT8 for QATLinear forward (982 ms, 23%)
The Xeon 8581C has AMX-INT8 tile registers. AMX does 16x64 * 64x16 INT8 matrix
multiplies per TDPBSSD instruction — works on 1K-element tiles vs VNNI's 64-byte
vectors. At dim=1024, the GEMMs are 1024x1024 and 1024x4096, large enough for
AMX to shine. Expected 2-4x over VNNI on the GEMM portion.
- Estimated savings: 300-500 ms/step
- Effort: moderate (new tile-based GEMM kernel, tilecfg setup)
- Risk: low (hardware confirmed available, well-documented ISA)

#### 2. BF16 backward GEMMs (1573 ms, 37%) — biggest single target
The backward pass is pure FP32. Two options:
- **AVX-512 BF16**: VDPBF16PS does 2 BF16 fused multiply-adds per cycle vs 1
  for FP32 VFMADD, and uses half the memory bandwidth (2 bytes vs 4 per element).
  Expected ~2x speedup on backward GEMMs.
- **AMX-BF16**: Tile-based BF16 GEMM, same architecture as AMX-INT8. Even faster
  than AVX-512 BF16 for large matrices.
- BF16 has same exponent range as FP32, just 8-bit mantissa vs 24-bit. For
  gradient computation this is fine — most frameworks use BF16 for gradients.
- Estimated savings: 500-800 ms/step (nearly halving the backward)
- Effort: moderate-high (BF16 conversion + GEMM kernel)
- Risk: low-medium (need to verify convergence is unaffected)

#### 3. AMX-BF16 for attention GEMMs (826+471 = 1297 ms, 31%)
The attention forward/backward use FP32 GEMM on 128x128 per-head matrices.
These are small for AMX (AMX tiles are 16x16), but there are 8 heads x 8 batch
items = 64 independent GEMMs per call. Could tile them or use BF16 to cut time.
- Estimated savings: 200-400 ms/step
- Effort: moderate
- Risk: low

#### 4. Cache-tiled GEMMs (applies to all GEMM paths)
Current GEMMs are naive row-parallel. At 1024x4096, the working set exceeds
L1/L2 cache. Tiling (e.g., 64x64 or 128x128 blocks) would improve cache reuse.
This helps all GEMM paths but is fiddly to implement correctly.
- Estimated savings: 10-20% across all GEMMs (~200-400 ms/step)
- Effort: high (micro-kernel design, tuning)
- Risk: low (pure optimization, no semantic change)

### Theoretical speed ceiling

If we got 2x on all GEMMs (AMX + BF16):
- QATLinear fwd: 982 → ~490 ms
- QATLinear bwd: 1573 → ~786 ms
- Attn fwd: 471 → ~235 ms
- Attn bwd: 826 → ~413 ms
- Other: ~302 ms (unchanged)
- Total: ~2226 ms/step (1.9x over current)

Combined with cache tiling (another 10-20%), plausible floor is ~1800-2000 ms/step
(2.1-2.4x over current 4231 ms/step).

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
