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
