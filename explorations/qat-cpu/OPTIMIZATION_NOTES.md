# QAT-CPU Performance Optimization Notes

## Current bottleneck analysis (dim=128, seq=64, 16 cores)

Per training step, the hot path is:
- 13 QATLinear forward (quantize + transpose + INT8 GEMM + dequantize)
- 13 QATLinear backward (2 FP32 GEMMs + transpose each)
- 2 attention forward: score computation + value multiply (scalar triple loops!)
- 2 attention backward: same scalar triple loops for gradients
- Softmax, RMSNorm, GeLU, optimizer

### Why QAT is still slower than FP32 at dim=128:
1. GEMM is too small (64x128x128 = 1M MACs). Overhead dominates.
2. Quantization/dequantization overhead: ~O(out*in + batch*in)
3. Attention score/value: scalar O(seq^2 * head_dim) loops, NOT using GEMM
4. Per-call malloc/free for temporaries

## Optimizations (ordered by impact)

### 1. Scale to dim=512
- GEMM goes from 64x128x128 to 64x512x512 (64x larger)
- INT8 VNNI advantage materializes: 64 MACs/VPDPBUSD vs 16 FMAs/VFMADD231PS
- Theoretical 4x INT8 throughput advantage becomes real at these sizes

### 2. GEMM-based attention scores/values [DONE]
Replaced scalar triple loops with:
- extract_head/scatter_head for contiguous per-head slices
- FP32 GEMM: scores_h = Q_h * K_h^T, out_h = attn_w * V_h
- Same approach for backward pass

### 3. Vectorize quantization with AVX-512 [DONE]
- absmax: integer AND to clear sign bit + _mm512_max_ps + horizontal reduce
- quantize: _mm512_mul_ps + _mm512_cvtps_epi32 + _mm512_cvtsepi32_epi8 (saturating pack)
- dequantize: _mm512_cvtepi32_ps + dual scale multiply
- Runtime dispatch via __builtin_cpu_supports("avx512f")
- Note: _mm512_and_ps requires AVX-512DQ; used _mm512_and_si512 with cast instead

### 4. KV cache for generation
Current: recomputes full sequence at each autoregressive step
Fix: cache K, V from previous tokens, only compute new Q
Reduces generation from O(n * seq^2 * dim) to O(n * seq * dim)
Training speed unaffected but generation samples become much faster.

### 5. Flash-attention insights
At seq=64, the attention matrix is 64x64x4 = 16KB per head — fits in L1 cache.
Flash attention's memory savings aren't needed at this scale.
However, the *fused kernel* idea applies: compute score + softmax + value multiply
in one pass, keeping data in L1. Worth considering for larger seq_len.

### 6. Reduce allocation overhead [DONE]
Pre-allocated weight transpose buffers (weight_q_t, weight_fp32_t) in QATLinear.
Reused across forward calls instead of malloc/free per call.

## Bug fix: GEMM beta=0 and NaN

All FP32 GEMM kernels (scalar, AVX2, AVX-512) had a subtle bug: when beta=0,
they computed `C[i][j] *= 0.0f` before accumulation. If C contained uninitialized
memory with NaN bit patterns, `0.0f * NaN = NaN` per IEEE 754. The fix: when
beta==0, zero C directly instead of multiplying. This caused QAT training at
dim=512 to produce NaN in attention scores and completely fail to converge.

## dim=512 results

After all optimizations:
- FP32: ppl=8.65, 626.3 sec, 125.3 ms/step
- QAT:  ppl=8.75, 408.2 sec, 81.6 ms/step
- **QAT speedup: 1.53x**
- **QAT perplexity ratio: 1.011** (matches FP32 quality)

## Profiling & Optimization Round 2

### Profiling (profile_qat.c)

Wrote a per-component timer-based profiler. Manually unrolls transformer_block
forward/backward and wraps each sub-operation with timer_sec() calls.
100 profiled steps + 5 warmup, dim=512.

Initial profile (before round 2 optimizations):
- QAT total: 138.1 ms/step
- Top bottlenecks: QATLinear fwd 31.5%, Adam 22.9%, Attn bwd 21.1%, GeLU 11.4%

Note: profiler overhead (~200 timer calls/step) inflates times vs the training
loop (which measured 81.6 ms/step). The relative breakdown is what matters.

### Optimization 7: AVX-512 Adam (optimizer.c)

Vectorized the AdamW inner loop with AVX-512 FMA intrinsics:
- Process 16 floats per iteration (was scalar)
- `_mm512_fmadd_ps` for `m = beta1*m + (1-beta1)*g` and `v = beta2*v + (1-beta2)*g^2`
- `_mm512_fnmadd_ps` for `param -= lr * update`
- Pre-compute `inv_bc1 = 1/(1-beta1^t)`, `inv_bc2 = 1/(1-beta2^t)` outside loop
  (avoids per-element division for bias correction)
- Scalar tail for remainder elements (n % 16)
- Runtime dispatch: `__builtin_cpu_supports("avx512f")`
- Uses `__attribute__((target("avx512f")))` so file compiles without -mavx512f

Result: Adam 31.6 ms -> 11.1 ms (**-65%**)

The optimizer is memory-bandwidth bound (4 arrays: param, grad, m, v = 104 MB
for 6.5M params). AVX-512 helps by reducing instruction count, allowing the
CPU to keep the memory pipeline fed. Further gains would need streaming stores
or non-temporal hints, but the arrays are reused soon so cache pollution isn't
the main issue.

### Optimization 8: AVX-512 GeLU with fast Padé tanh (layers.c)

Replaced scalar tanhf() with a fast rational polynomial approximation:
- Padé [7/7] approximant: tanh(x) ≈ x * P(x²) / Q(x²)
  - P(z) = 135135 + 17325z + 378z² + z³
  - Q(z) = 135135 + 62370z + 3150z² + 28z³
- Clamped to ±1 for |x| > 9 (where tanh saturates)
- AVX-512 version: `fast_tanh_avx512` evaluates both polynomials with FMA,
  single `_mm512_div_ps` for the ratio
- GeLU forward: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x³)))
- GeLU backward: derivative computed with same fast tanh
- Both forward and backward vectorized, with scalar fallback using fast_tanh

Result: GeLU 15.7 ms -> 0.38 ms (**-97.6%**)

The gain is from two effects:
1. fast_tanh is ~10x faster than libm tanhf (no function call overhead, no
   special-case handling for denormals/overflow)
2. AVX-512 processes 16 elements per iteration vs scalar 1

### Optimization 9: Weight quantization cache (qat_linear.c, qat_cpu.h, train.c)

Added `weights_dirty` flag to QATLinear:
- Set to `true` on creation and after each optimizer step
- Forward pass checks flag; skips quantize + transpose if weights unchanged
- In a training step, each of the 13 layers calls forward once, but weights
  only change once (after adam_step). So 12 of 13 quantizations were redundant
  within a step. With caching, each layer quantizes once on the first forward
  call after the optimizer step, then reuses until next step.
- `gpt_mark_weights_dirty()` in train.c sets flag on all 13 layers after adam_step

Result: QATLinear fwd 43.5 ms -> 42.2 ms (**-3%**)

Modest gain. At dim=512, per-layer quantize+transpose is ~0.1 ms, so saving
12 redundant calls saves ~1.2 ms. The GEMM itself (INT8 VNNI) dominates the
forward cost. The cache would matter more with larger weight matrices (e.g.
dim=2048 where quantization takes ~1.6 ms per layer).

### Combined results

```
                Before         After          Change
QAT total:      138.1 ms       92.2 ms        -33.2%
FP32 total:     156.7 ms      116.6 ms        -25.6%
```

Detailed comparison (QAT mode):
| Component       | Before   | After   | Savings              |
|-----------------|----------|---------|----------------------|
| Adam            | 31.6 ms  | 11.1 ms | -20.5 ms (-64.9%)    |
| GeLU            | 15.7 ms  | 0.38 ms | -15.3 ms (-97.6%)    |
| QATLinear fwd   | 43.5 ms  | 42.2 ms | -1.3 ms (-3.0%)      |

### Remaining bottleneck profile (QAT, 92.2 ms/step)

1. QATLinear forward: 42.2 ms (45.8%) — INT8 VNNI GEMM + quantize/dequant
2. Attention backward: 22.1 ms (24.0%) — FP32 GEMM (per-head score/value grads)
3. Adam optimizer: 11.1 ms (12.0%) — memory-bandwidth bound
4. QATLinear backward: 9.9 ms (10.7%) — FP32 GEMM (grad_input + grad_weight)
5. Everything else: <2 ms combined

## 15K Step Training Run (final)

Full end-to-end comparison with all optimizations applied:

```
                    FP32          QAT
Val perplexity:     6.14          6.56
ms/step:            91.9          58.7
Total time:         1378 sec      881 sec
Speedup:            --            1.56x
PPL ratio:          --            1.070
```

The QAT quality gap widened from 1.1% (at 5K steps) to 7% (at 15K steps).
This is expected: quantization noise accumulates more as the model trains
longer and the weight updates become smaller relative to quantization error.
7% perplexity increase is still acceptable for a 1.56x speedup.

Speed improved from 1.53x to 1.56x because the round 2 optimizations (Adam,
GeLU) saved more absolute time from the QAT path than the FP32 path. This is
because QAT's forward pass is faster (INT8 VNNI), so the fixed-cost operations
(Adam, GeLU, backward) were a larger fraction of QAT's total time.

## Metrics & Comparability

Added standard metrics to compare with the literature. Here's what we report
and how it's calculated:

### Quality metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| CE Loss (nats) | -mean(log(p(target))) | Raw cross-entropy, natural log |
| Perplexity | exp(CE_loss) | "Effective vocabulary size" per token |
| Bits per byte (BPB) | CE_loss / ln(2) | Tokenizer-agnostic; 1 token = 1 byte for us |

**BPB** is the key comparability metric. It's used by DeepSeek, Gemma, and
increasingly preferred over perplexity because it doesn't depend on tokenizer
choice. For character-level models like ours (1 token = 1 ASCII byte), BPB is
just the loss divided by ln(2) to convert nats to bits. For subword tokenizers:
BPB = total_CE_nats / (ln(2) * total_bytes_in_text).

Reference BPB values on Shakespeare-like text:
- Random (128 ASCII): 7.00 BPB
- Our FP32 at 15K (batch=1): ~2.63 BPB
- Our QAT at 15K (batch=1): ~2.72 BPB
- Our FP32 at 5K (batch=8): 2.163 BPB
- Our QAT at 5K (batch=8): 2.164 BPB
- Good char-level model (deep, 100K+ steps): ~1.2-1.5 BPB

### Speed metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| ms/step | wall_time / n_steps * 1000 | End-to-end step time |
| Tokens/sec | seq_len / (ms_per_step / 1000) | Training throughput |
| Effective TFLOPS | est_flops_per_step / step_time / 1e12 | Hardware utilization |

**Tokens/sec** is the most universal metric. nanoGPT, LLM.c, and most training
frameworks report this.

**Effective TFLOPS** shows how well we utilize the hardware. Our estimated FLOPs
per step (fwd+bwd) uses the standard approximation:
- Forward per token per layer: 2*dim*(4*dim + 2*hidden_dim)
- Output head: 2*dim*vocab_size
- Backward ≈ 2x forward, total ≈ 3x forward
- Per step = above * seq_len

For our model: ~2441M FLOPs/step → ~0.03-0.04 TFLOPS effective.
This is low because dim=512 GEMMs are too small to saturate the hardware.
A Xeon 8581C has ~2.4 TFLOPS peak FP32 (2.1 GHz * 16 cores * 2 FMA * 32 lanes),
so we're at ~1.5% MFU. Larger models would get much better utilization.

### How others compare

**GPTQ** (post-training quant): reports perplexity on WikiText2, PTB, C4. Not
directly comparable (PTQ vs QAT, subword vs char-level).

**BitNet b1.58** (1-bit QAT): reports perplexity and BPB, plus downstream task
accuracy (ARC, PIQA, WinoGrande, GSM8K). Training speed in tokens/sec and
energy per inference.

**nanoGPT/LLM.c**: reports val loss, tokens/sec, MFU. LLM.c targets ~50% MFU
on GPU; our CPU MFU is expectedly much lower.

**QLoRA**: reports chatbot benchmarks (Vicuna), human/GPT-4 eval, not raw ppl.

## Mini-batching (batch=8)

### Implementation
Added `BATCH_SIZE=8` constant. Linear layers (QATLinear, output head) process
`[batch*seq_len, dim]` matrices — they're already batch-agnostic. Attention
loops over batch items, computing per-sequence `[seq_len x seq_len]` attention.
See MINIBATCH_PLAN.md for detailed design.

### Results (dim=512, 5K steps)
```
                    FP32          QAT
Val perplexity:     4.48          4.48
Val BPB:            2.163         2.164
ms/step:            183.8         187.6
Tokens/sec:         2785          2729
Effective TFLOPS:   0.1062        0.1041
Speedup:            --            0.98x
```

### Analysis: Why QAT speedup disappeared

With batch=1 (M=64), the training step breakdown was roughly:
- INT8 forward: ~42 ms (QAT) vs ~65 ms (FP32) — VNNI wins big
- FP32 backward: ~22 ms (same for both)
- Other: ~11 ms (same for both)
- QAT total: 75 ms, FP32 total: 98 ms → 1.3x in forward, 1.56x overall

With batch=8 (M=512), all GEMMs scale up:
- INT8 forward: ~70 ms (QAT) vs ~90 ms (FP32) — VNNI still wins, but less dominant
- FP32 backward: ~80 ms (same for both) — now dominates both modes
- Other: ~35 ms (same for both)
- QAT total: 185 ms, FP32 total: 205 ms → ~1.1x theoretical, 0.98x measured

The backward pass (always FP32) benefits equally from larger M, so it takes a
bigger share of total time. The INT8 forward advantage gets diluted.

### Possible ways to recover QAT speedup
1. **Increase dim**: Larger weight matrices → bigger VNNI advantage in forward
2. **INT8 backward**: Use VNNI for gradient computation (sacrifices gradient precision)
3. **Gradient accumulation**: Multiple forward-only mini-batches, one backward.
   This would maximize the fraction of time spent in INT8 forward.
4. **Mixed precision backward (BF16)**: Not helpful on this CPU (no BF16 GEMM advantage)
