# INT8 Backward Pass Plan

## Motivation

With batch=8, QAT gives 0.98x speedup (no advantage) because the backward pass
is 100% FP32 in both modes and dominates step time. If we quantize the backward
GEMMs to INT8, we recover the VNNI advantage for ~70% of compute.

## Current Backward GEMM Inventory

### QAT Linear backward (qat_linear.c:195-241)

Two GEMMs per layer, called 11 times per step (4 blocks x {Wq,Wk,Wv,Wo} + 4 blocks x {ffn_up,ffn_down} ... wait, 4 layers x 6 = actually N_LAYERS=4, so 24 linear backward calls + 1 output head = 25).

Actually: N_LAYERS=4, each has 4 attention projections + 2 FFN = 6. Plus 1 output head.
Total: 4*6 + 1 = 25 qat_linear_backward calls per step.

**GEMM 1: grad_input** (line 206)
```
grad_input[batch x in_f] = grad_output[batch x out_f] * weight[out_f x in_f]
```
Dimensions:
- Attention projections: M=512, N=512, K=512
- FFN up backward:       M=512, N=512, K=2048
- FFN down backward:     M=512, N=2048, K=512
- Output head:           M=512, N=512, K=128 (vocab)

**GEMM 2: grad_weight** (line 221)
```
grad_weight[out_f x in_f] += grad_output^T[out_f x batch] * saved_input[batch x in_f]
```
Dimensions:
- Attention projections: M=512, N=512, K=512
- FFN up:                M=2048, N=512, K=512
- FFN down:              M=512, N=2048, K=512
- Output head:           M=128, N=512, K=512

### Attention per-head backward (layers.c:641-679)

4 GEMMs per head per batch item, all [64 x 64 x 64]. Total: 4 * 8 heads * 8 batch = 256 GEMMs.
These are small and already use OpenMP at the outer GEMM level. INT8 quantization
overhead would likely exceed savings for 64x64 matrices. **Skip these.**

## Plan: INT8 for QAT Linear Backward

### What to quantize

Only the two large GEMMs in `qat_linear_backward`:

1. **grad_input GEMM**: `grad_output * weight`
   - grad_output: FP32, changes every call -> quantize per-token (rows)
   - weight: FP32 master weights -> quantize per-channel (rows)
   - Already have weight quantized from forward pass! But it's transposed
     differently. Forward uses weight^T[in x out], backward uses weight[out x in].
     Actually the forward quantizes weight[out x in] then transposes. So we
     already have weight_q[out x in] and weight_scales[out] from the forward pass.
   - For this GEMM: A=grad_output[M x K], B=weight[K x N] where K=out_f, N=in_f
     But weight is stored as [out_f x in_f], so B = weight[out_f x in_f].
     The GEMM is C[M,N] = A[M,K] * B[K,N], so we need weight as [K x N] = [out_f x in_f].
     weight is already [out_f x in_f] row-major, so it's already in the right layout!
   - **Key insight**: We can reuse weight_q and weight_scales from the forward pass.
     No need to re-quantize. Just quantize grad_output per-token.

2. **grad_weight GEMM**: `grad_output^T * saved_input`
   - grad_output^T: need to transpose first, then quantize
   - saved_input: FP32 activations from forward pass -> quantize per-token
   - **Key insight**: We can quantize saved_input during the forward pass (when we
     already have it) and save the quantized version. This moves cost to forward.
     But forward already quantizes input for the INT8 GEMM... however that's the
     layer input, and saved_input is the same thing. So we already have input_q
     and input_scales from forward! Currently we free them. We should save them.

### Implementation Steps

1. **Extend QATLinear struct** to hold:
   - `saved_input_q` (TensorI8*) — quantized saved_input from forward
   - `saved_input_scales` (float*) — per-token scales
   - `use_int8_backward` flag

2. **Modify forward pass** (`qat_linear_forward`):
   - When use_int8_backward, save input_q and input_scales instead of freeing them
   - When !use_qat (FP32 forward), still quantize and save input for backward

3. **Modify backward pass** (`qat_linear_backward`):
   - GEMM 1 (grad_input): quantize grad_output per-token, use weight_q[out x in]
     as B matrix directly. INT8 GEMM -> dequantize with grad_output_scales * weight_scales.
   - GEMM 2 (grad_weight): transpose grad_output, quantize per-token.
     Use saved_input_q as B. INT8 GEMM -> dequantize.
   - grad_weight accumulation: need beta=1.0 semantics. INT8 GEMM gives fresh
     result, then we dequantize and add to existing grad_weight in FP32.

4. **Correctness test**: Run a few steps with INT8 backward, compare gradients
   to FP32 backward. Expect some quantization error. Measure max relative error
   per layer.

5. **Training test**: Run full training, compare convergence and final perplexity.

### Concerns

- **Gradient precision**: Weight gradients are small (often 1e-4 to 1e-6 range).
  Per-token INT8 quantization maps the range [-absmax, absmax] to [-127, 127].
  If gradients have high dynamic range across the K dimension, quantization
  error could be significant. This is the main risk.

- **grad_weight accumulation**: We accumulate grad_weight across the step (beta=1.0).
  With INT8, each call produces a fresh INT8 GEMM result that we dequantize and add.
  The accumulation itself stays FP32, which is fine.

- **Transpose overhead**: grad_output^T for GEMM 2 needs transposing before
  quantization. This is O(M*K) and is scalar. Could vectorize if needed.

### Expected Speedup

With batch=8 baseline (~184 ms/step FP32):
- Linear backward currently ~80+ ms (from the 650 vs 184 ms experiment,
  we know attention+linear backward is huge)
- If INT8 backward GEMMs are 1.5x faster (like forward), that's ~25-30% of
  backward time saved
- Rough estimate: 184 ms -> ~140-155 ms per step (15-25% improvement)
- QAT would finally be faster than FP32 with minibatching

### What NOT to do

- Don't INT8 the attention per-head backward GEMMs (64x64, too small)
- Don't quantize the gradient accumulation (keep FP32)
- Don't try to fuse quantize+GEMM (complexity not worth it)

## Results (1000 steps, batch=8, dim=512)

```
                          FP32        QAT     QAT+INT8bwd
ms/step:                 535.0      483.5        520.1
Val Perplexity:           7.73       7.68         7.76
Val BPB:                 2.951      2.941        2.957
Speedup vs FP32:            --      1.11x        1.03x
```

**Negative result.** INT8 backward is slower than QAT fwd-only (520 vs 484 ms/step).
Quality is fine (ppl 7.76 vs 7.73), but the quantization overhead defeats the purpose.

### Why it's slower

The per-column quantization needed for the B matrix in each backward GEMM is the
bottleneck. Unlike per-row quantization (which iterates contiguously in memory),
per-column quantization iterates column-major over row-major data -- cache-unfriendly
and not vectorized. Each backward call does:
1. quantize grad_output per-row (fast, contiguous)
2. INT8 GEMM 1 using per-column quantized weight (fast)
3. dequantize INT32 result (fast)
4. transpose grad_output (scalar, cache-unfriendly)
5. quantize transposed grad_output per-row (fast)
6. INT8 GEMM 2 using per-column quantized input (fast)
7. dequantize and accumulate (fast)

Steps 4 is overhead that doesn't exist in the FP32 path (FP32 GEMM handles
transpose via the alpha parameter). The per-column quantization in forward
(for both weight and saved_input) adds more overhead.

Net: the INT8 GEMM is faster, but we added ~5 extra memory-bound operations
per layer per step. At dim=512 with batch=8, the GEMMs aren't big enough for
the VNNI throughput advantage to overcome this overhead.

### Would it work at larger scale?

Possibly. The quantization overhead is O(M*K) while the GEMM is O(M*N*K).
As dimensions grow, the GEMM dominates more. At dim=2048 or dim=4096, the
ratio would shift in favor of INT8. But at our dim=512, the answer is no.
