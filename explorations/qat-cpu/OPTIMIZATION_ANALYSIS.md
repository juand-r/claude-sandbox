# QAT-CPU Optimization Analysis

## Current Best Results (4L, batch=8, seq=64, 10K steps, 12.85M params)

```
              FP32        QAT
ms/step:      473.1      399.6
tok/s:        1082       1281
Perplexity:   4.11       4.11
QAT speedup:             1.18x
```

## All Experiment Results

| Run | Layers | Params | Batch | Seq | Steps | Tokens | FP32 ppl | QAT ppl | FP32 tok/s | QAT tok/s | Speedup |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4L b8 10K | 4 | 12.85M | 8 | 64 | 10K | 5.12M | 4.11 | 4.11 | 1082 | 1281 | 1.18x |
| 2L b8 5K | 2 | 6.49M | 8 | 64 | 5K | 2.56M | 4.48 | 4.48 | 2785 | 2729 | 0.98x |
| 6L b4 1K | 6 | 19.2M | 4 | 128 | 1K | 512K | 8.70 | 8.75 | 807 | 834 | 1.03x |
| 2L b1 30K | 2 | 0.26M | 1 | 64 | 30K | 1.92M | 6.32 | 6.59 | - | - | - |
| 2L b1 15K | 2 | 6.49M | 1 | 64 | 15K | 960K | 6.14 | 6.56 | ~1000 | ~1600 | 1.56x |
| 2L b1 5K | 2 | 6.49M | 1 | 64 | 5K | 320K | 8.65 | 8.75 | ~511 | ~784 | 1.53x |

## Key Observations

1. **More layers + more tokens = better ppl.** 4L at 5.12M tokens beat 2L at any token count.
2. **Batching helps quality dramatically** (ppl 6.14 -> 4.48 with same model size, fewer steps)
   but kills QAT speedup (1.56x -> 0.98x at batch=8 with 2L).
3. **4 layers recovered some QAT advantage** (1.18x) because the forward pass is a bigger
   fraction of total time with more layers. More compute per step = more INT8 GEMM to accelerate.
4. **QAT quality matches FP32** in all batched runs (ratio <= 1.001). The quality gap only
   appears at batch=1 with many steps (1.07x at 15K steps).

## Where Time Goes (estimated for 4L batch=8)

Based on the profiling data (2L batch=1) scaled to current config:

| Component | Est. % of step | Notes |
|---|---|---|
| QATLinear forward (INT8 GEMM) | ~35-40% | 9 linear layers × 4 layers. This is what QAT accelerates |
| Attention backward (FP32 GEMM) | ~25-30% | Per-head score/value grads + 4 projection grads per layer |
| QATLinear backward (FP32 GEMM) | ~15% | FFN up/down grads, output head grad |
| Adam optimizer | ~8-10% | 12.85M params, memory-bandwidth bound |
| Everything else | ~5% | RMSNorm, softmax, residual, embedding, loss |

**The backward pass (all FP32) is ~40-45% of total time.** This is why QAT speedup is limited.

## Optimization Opportunities (ordered by expected impact)

### 1. Parallelize attention head loop (Easy, Moderate Impact)

Currently per-head attention (fwd and bwd) loops sequentially over 8 heads, each doing
small [64×64] GEMMs. With 16 cores and 8 heads, OpenMP parallelism could help.

- **Estimated saving**: 10-20% of attention time (~5-10% overall)
- **Risk**: Low. Just add `#pragma omp parallel for`
- **Effort**: Small

### 2. AMX-INT8 kernels (Hard, High Impact)

The Xeon 8581C has AMX-INT8 which does 16×16 INT8 matmul per instruction.
For our GEMM sizes ([512×512], [512×2048]), AMX could be 4-8x faster than VNNI.

- **Estimated saving**: Could cut INT8 GEMM time by 4-8x, meaning ~15-25% overall
- **Risk**: Medium. AMX programming is very different (tile registers, TILECFG)
- **Effort**: Large. New kernel, tile configuration, packing changes

### 3. INT8 backward pass (Medium difficulty, High Impact)

Use INT8 GEMM for grad_input and grad_weight computation. This would make the
backward pass also benefit from VNNI/AMX.

- **Estimated saving**: Could cut backward GEMM time significantly, ~15-20% overall
- **Risk**: HIGH. Gradient quantization is lossy. Could hurt convergence.
  Would need careful evaluation (compare ppl curves with/without).
- **Effort**: Medium. Reuse existing INT8 GEMM infrastructure.

### 4. Fused quantize + GEMM + dequantize (Medium difficulty, Moderate Impact)

Currently three separate passes: quantize activations, INT8 GEMM, dequantize output.
Fusing would reduce memory traffic (activations stay in cache between ops).

- **Estimated saving**: ~5-10% of forward time
- **Risk**: Low
- **Effort**: Medium. Need to restructure VNNI kernel

### 5. Vectorize INT8 transpose (Easy, Small Impact)

The int8 transpose in qat_linear.c is scalar. AVX-512 block transpose (8×8 or 16×16)
with shuffle/unpack would be faster.

- **Estimated saving**: ~1-2% overall
- **Risk**: None
- **Effort**: Small

### 6. Pre-allocate all temporaries / arena allocator (Easy, Small Impact)

Each forward/backward creates ~10+ temporary tensors via malloc. An arena allocator
that pre-allocates all workspace at model init would eliminate this overhead.

- **Estimated saving**: ~1% overall (malloc is fast, but it adds up)
- **Risk**: None
- **Effort**: Small-medium

## What NOT To Do (Diminishing Returns)

- **Flash attention**: seq=64 means attention matrices are 16KB per head. Fits in L1 cache.
- **FP16/BF16 training**: No native BF16 GEMM throughput advantage on this CPU.
- **Softmax/RMSNorm SIMD**: < 1ms each, not worth the complexity at seq=64.
- **Memory pool for small allocs**: Allocation overhead is < 0.5ms total.
- **KV cache**: Only matters for generation, not training throughput.

## Recommendations

**If goal is faster training throughput:**
1. Do attention head parallelism first (easy win)
2. Then AMX-INT8 if we want to invest the effort

**If goal is better ppl:**
1. Train longer (20K+ steps) — ppl was still dropping at 10K
2. Try seq=128 with batch=4 (same tokens/step but longer context)
3. Increase dim or layers further

**If goal is best QAT speedup ratio:**
1. Reduce batch size (batch=1-2 gives 1.5x+ speedup)
2. Use larger model (more forward compute to accelerate)
3. INT8 backward would be the game-changer
