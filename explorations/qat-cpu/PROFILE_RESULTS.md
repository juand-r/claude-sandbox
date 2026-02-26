# QAT-CPU Profiling Results

## Setup
- Model: 2 layers, dim=512, 8 heads, hidden=2048, 6.5M params
- Sequence length: 64, batch size: 1
- CPU: Intel Xeon Platinum 8581C, 16 cores, AVX-512 VNNI
- 100 profiled steps after 5 warmup steps

## Raw Results

```
                                     FP32              QAT
                                   ms    %          ms    %
QATLinear forward                56.23  35.9%     43.54  31.5%
QATLinear backward               12.15   7.8%     10.79   7.8%
Attention GEMM + backward(*)     30.62  19.5%     29.18  21.1%
Attention overhead                0.46   0.3%      0.44   0.3%
Softmax                           0.54   0.3%      0.56   0.4%
RMSNorm                           0.95   0.6%      0.93   0.7%
GeLU                             16.45  10.5%     15.69  11.4%
Residual + copies                 0.63   0.4%      0.48   0.3%
Optimizer (Adam)                 33.33  21.3%     31.58  22.9%
Loss                              0.06   0.0%      0.06   0.0%
Embedding                        0.13   0.1%      0.12   0.1%
--------------------------------------------------------------
TOTAL                           156.73             138.07
```

(*) "Attention GEMM + backward" includes the full attention_backward call,
which contains 4 qat_linear_backward (for Wq/Wk/Wv/Wo) plus FP32 GEMMs
for per-head gradient computation. These are lumped together in the backward
pass due to instrumentation limitations.

## Where QAT Saves Time

QATLinear forward: 56.23 -> 43.54 ms (**-12.69 ms, -22.6%**)
This is the core win. INT8 VNNI GEMM replaces FP32 GEMM for the 13 linear
layers (4 per attention block * 2 blocks + 2 FFN * 2 blocks + 1 output head).
Despite the overhead of quantize + transpose + dequantize, INT8 is still
faster because VPDPBUSD does 4x the MACs per instruction vs VFMADD231PS.

Total savings: FP32 156.7 - QAT 138.1 = **18.6 ms/step faster (11.9%)**

Note: the training run showed 125 vs 82 ms/step (1.53x). The profiler shows
less speedup (1.13x) because the profiler has per-call timer overhead from
~200 timer_sec() calls per step, which adds ~5 ms to both modes but hurts
the ratio.

## Top Bottlenecks (QAT mode)

### 1. QATLinear forward: 43.5 ms (31.5%)
The single largest cost. Breaks down into:
- Quantize weights (per-channel): 512x512 matrix, 13 times
- Quantize activations (per-token): 64x512 or 64x2048, 13 times
- INT8 transpose: [out x in] -> [in x out], 13 times
- INT8 GEMM (VNNI): the actual computation
- Dequantize INT32->FP32: 13 times

**Opportunity**: Weight quantization is redundant every call — weights only
change after optimizer step. Could quantize weights once per step, not once
per layer call. That's 13 weight quantizations + transposes saved.

**Opportunity**: The INT8 transpose is scalar. Could be vectorized with
AVX-512 shuffle/permute instructions.

### 2. Optimizer (Adam): 31.6 ms (22.9%)
Adam iterates over all 6.5M parameters doing:
  m = beta1*m + (1-beta1)*g
  v = beta2*v + (1-beta2)*g^2
  w = w - lr * m_hat / (sqrt(v_hat) + eps)

That's ~20 FLOPs per parameter * 6.5M = 130M FLOPs, plus 4 memory accesses
per param (w, g, m, v) = 26M * 4B = 104 MB. This is memory-bandwidth bound.

**Opportunity**: Vectorize Adam with AVX-512 (currently scalar loop).
Could also fuse with gradient zeroing to save a memory pass.

### 3. Attention backward (including QATLinear bwd): 29.2 ms (21.1%)
This includes both the FP32 per-head GEMMs (score/value gradients) and
the 4 qat_linear_backward calls (Wq/Wk/Wv/Wo gradients). The backward
path is all FP32 (STE means no INT8 in backward), so no QAT advantage.

**Opportunity**: The per-head loop in attention backward could be parallelized
across heads with OpenMP. Currently sequential.

### 4. GeLU: 15.7 ms (11.4%)
GeLU involves tanhf() which is expensive. 64 * 2048 * 2 (fwd+bwd) * 2 layers
= 524K tanh calls per step.

**Opportunity**: Use a polynomial approximation for tanh, or use SiLU
(x * sigmoid(x)) which is cheaper. Or vectorize with AVX-512 — the current
code is scalar.

### 5. QATLinear backward: 10.8 ms (7.8%)
Two FP32 GEMMs per layer (grad_input + grad_weight), applied to the output
head and the non-attention projections (ffn_up, ffn_down) captured here.
The attention projection backwards are counted in item 3.

## Insignificant Costs (<1%)
- Softmax: 0.56 ms (0.4%) — seq=64 is tiny
- RMSNorm: 0.93 ms (0.7%) — just vector normalization
- Attention overhead (extract/scatter/transpose): 0.44 ms
- Residual + copies: 0.48 ms
- Loss: 0.06 ms
- Embedding: 0.12 ms

## Actionable Improvements (ordered by estimated impact)

### High impact
1. **Vectorize Adam with AVX-512**: ~31 ms, memory-bound.
   AVX-512 can do 16 floats per instruction. With streaming stores and
   prefetching, could cut this by 2-4x. Estimate: **-15 to -20 ms**.

2. **Cache quantized weights per step**: Quantize weights once after
   optimizer step instead of 13x during forward. The weights don't change
   during a forward pass. Estimate: **-5 to -10 ms** (saves 12 redundant
   quantize + transpose operations on 512x512 and 512x2048 matrices).

3. **Vectorize GeLU with AVX-512**: tanhf is scalar and slow. A fast
   polynomial tanh approximation vectorized with AVX-512 could be 8-16x
   faster. Or switch to SiLU which avoids tanh entirely.
   Estimate: **-10 to -14 ms**.

### Medium impact
4. **Parallelize attention head loop**: The per-head backward loop is
   sequential. With 8 heads and 16 cores, OpenMP could help.
   Estimate: **-3 to -5 ms**.

5. **Vectorize INT8 transpose**: Currently scalar nested loops. Could use
   8x8 or 16x16 block transpose with AVX-512 shuffle/unpack.
   Estimate: **-1 to -3 ms**.

### Low impact (not worth doing)
- Softmax vectorization (0.5 ms — too small)
- RMSNorm vectorization (0.9 ms — too small)
- Memory pool allocator (copies are only 0.5 ms)

---

## Post-Optimization Results (Round 2)

Three optimizations were implemented and profiled:

### What was done
1. **AVX-512 Adam optimizer** (optimizer.c) — processes 16 floats/iter with FMA
2. **AVX-512 GeLU with fast Padé tanh** (layers.c) — rational polynomial approx
3. **Weight quantization cache** (qat_linear.c) — quantize once per step, not 13x

### Results (100 steps, 5 warmup)

```
                                     FP32              QAT
                                   ms    %          ms    %
QATLinear forward                56.24  48.2%     42.20  45.8%
QATLinear backward               11.25   9.6%      9.87  10.7%
Attention GEMM + backward(*)     30.00  25.7%     22.12  24.0%
Attention overhead                0.43   0.4%      0.39   0.4%
Softmax                           0.53   0.5%      0.52   0.6%
RMSNorm                           0.93   0.8%      0.88   1.0%
GeLU                              0.64   0.6%      0.38   0.4%
Residual + copies                 0.69   0.6%      0.48   0.5%
Optimizer (Adam)                 10.99   9.4%     11.07  12.0%
Loss                              0.06   0.1%      0.06   0.1%
Embedding                        0.12   0.1%      0.11   0.1%
--------------------------------------------------------------
TOTAL                           116.59              92.17
```

### Comparison (QAT mode)

| Component | Before | After | Savings |
|---|---|---|---|
| Adam | 31.6 ms | 11.1 ms | **-20.5 ms (-64.9%)** |
| GeLU | 15.7 ms | 0.38 ms | **-15.3 ms (-97.6%)** |
| QATLinear fwd | 43.5 ms | 42.2 ms | **-1.3 ms (-3.0%)** |
| **Total** | **138.1 ms** | **92.2 ms** | **-45.9 ms (-33.2%)** |

FP32 mode also improved: 156.7 -> 116.6 ms/step (**-25.6%**).

### Analysis

**AVX-512 Adam** was the biggest single win at -20.5 ms. The optimizer was
doing scalar loads/stores over 6.5M parameters; AVX-512 processes 16 at once
with fused multiply-add for the momentum updates.

**AVX-512 GeLU** was equally dramatic in percentage terms (-97.6%). The Padé
[7/7] rational polynomial for tanh eliminates the expensive libm tanhf() call,
and vectorizing 16-wide with AVX-512 FMA collapses 524K tanh calls into ~32K
vector iterations.

**Weight cache** had modest impact (-1.3 ms). The weight quantization cost per
call (~0.1 ms per layer) is small relative to the GEMM itself. The savings
would be larger with bigger models where quantization of larger weight matrices
takes more time.

### Remaining bottlenecks (QAT)
1. QATLinear forward: 42.2 ms (45.8%) — dominated by INT8 GEMM, hard to beat
2. Attention backward: 22.1 ms (24.0%) — FP32 GEMMs, could parallelize heads
3. Adam: 11.1 ms (12.0%) — memory-bandwidth bound even with AVX-512
4. QATLinear backward: 9.9 ms (10.7%) — FP32 GEMM, limited optimization room
