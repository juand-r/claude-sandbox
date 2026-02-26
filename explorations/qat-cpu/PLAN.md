# QAT-CPU Build Plan

## Phase 1: Foundation [DONE]
- [x] Project directory and README
- [x] `qat_cpu.h` - all types, enums, structs, API declarations
- [x] `cpu_detect.c` - CPUID-based feature detection
- [x] `memory.c` - aligned alloc, tensor create/free, RNG

## Phase 2: GEMM Kernels [DONE]
- [x] `kernels_scalar.c` - scalar INT8 + FP32 GEMM (reference)
- [x] `kernels_avx2.c` - AVX2 INT8 GEMM (widened int32 multiply), AVX2 FP32 GEMM (vfmadd231ps)
- [x] `kernels_vnni.c` - AVX-512 VNNI INT8 GEMM (vpdpbusd), AVX-512 FP32 GEMM
- [x] `dispatch.c` - kernel dispatch (function pointer selection based on CPUID)
- [x] Tests: all SIMD outputs match scalar reference exactly (INT8) / within 1e-3 (FP32)
- Note: vpmaddubsw approach abandoned for AVX2 INT8 due to int16 saturation issues. Widened int32 approach used instead (still 3.5x faster than scalar).
- Note: VNNI kernel slower than AVX2 at 256x256 due to B-matrix packing overhead. Needs prepack optimization.

## Phase 3: Quantization [DONE]
- [x] `quantize.c` - per-channel symmetric (weights), per-token symmetric (activations)
- [x] INT32 -> FP32 dequantization with dual scales
- [x] Fake quantization
- [x] Tests: round-trip error 0.004 (within theoretical 0.008 bound)

## Phase 4: QAT Linear Layer [DONE]
- [x] `qat_linear.c` - forward (quantize -> INT8 GEMM -> dequant)
- [x] Backward with STE (FP32 GEMM, gradients bypass quantization)
- [x] Tests: gradient check 98% within 30% tolerance, QAT vs FP32 forward error <0.5%

## Phase 5: Transformer Components [DONE]
- [x] `layers.c` - RMSNorm, GeLU/SiLU, Softmax
- [x] Attention block (Q/K/V/O projections via QATLinear)
- [x] Full TransformerBlock with residuals

## Phase 6: Training Loop [DONE]
- [x] `optimizer.c` - Adam with FP32 master weights (AdamW)
- [x] `loss.c` - Cross-entropy loss
- [x] Training convergence verified: loss 2.20 -> 0.09 in 100 steps

## Phase 7: Scaling [DONE]
- [x] B-matrix prepack for VNNI kernel optimization
- [x] Multi-threaded GEMM (OpenMP)
- [x] OpenMP for quantization/dequantization
- [x] GEMM-based attention (replacing scalar triple loops)
- [x] AVX-512 vectorized quantization/dequantization
- [x] Pre-allocated weight transpose buffers
- [x] dim=512 training: QAT matches FP32 with 1.53x speedup
- [ ] NUMA-aware allocation
- [ ] Gradient accumulation

## Performance Optimization Log

### VNNI B-matrix prepack (commit TBD)
The original VNNI kernel repacked B-matrix data from row-major into VNNI-interleaved
format inside the innermost loop, once per row of A. For M=64, this meant 64x redundant
repacking. Fixed by hoisting the pack out of the i-loop:
- SIMD interleave (unpacklo/hi epi8/epi16) packs 16x4 bytes in ~5 instructions
- Column sums for unsigned correction precomputed once
- Result: QAT 22.5 -> 20.1 ms/step (11% improvement)

### OpenMP threading
Added `#pragma omp parallel for` to:
- INT8 GEMM (VNNI, AVX2) outer i-loop
- FP32 GEMM (AVX-512, AVX2) outer i-loop
- Quantization per-row loops
- Dequantization and bias-add loops
Threshold: `if(M >= 8)` to avoid thread overhead for tiny GEMMs.
Result: QAT 20.1 -> 14.6 ms/step, now matches FP32 (14.3 ms/step) = 0.98x

### Combined improvement (2000-step quick test)
- Before: FP32 14.9 ms/step, QAT 22.5 ms/step (0.67x)
- After:  FP32 14.3 ms/step, QAT 14.6 ms/step (0.98x)

### Full 30K training results (dim=128)
- FP32: ppl=6.32, 427.3 sec, 14.2 ms/step
- QAT:  ppl=6.59, 483.4 sec, 16.1 ms/step
- QAT speedup: 0.88x (was 0.67x before optimization)
- QAT perplexity ratio: 1.044 (matches FP32 quality, <5% increase)
- Generated text shows English words: "sword", "queen", "heaven", "soul", "grace"

### dim=512, 5K training results
After GEMM-based attention, AVX-512 quantize, pre-allocated buffers, and GEMM beta=0 NaN fix:
- FP32: ppl=8.65, 626.3 sec, 125.3 ms/step
- QAT:  ppl=8.75, 408.2 sec, 81.6 ms/step
- **QAT speedup: 1.53x**
- **QAT perplexity ratio: 1.011 (matches FP32 quality)**
- INT8 VNNI advantage finally dominates at this GEMM size (64x512x512)

## Benchmark Results (Xeon Platinum 8581C, 256x256 GEMM, 16 cores)

| Kernel       | INT8 GOPS (1T) | INT8 GOPS (16T) | FP32 GFLOPS (1T) | FP32 GFLOPS (16T) |
|--------------|----------------|-----------------|-------------------|--------------------|
| Scalar       | 4.3            | 5.0             | 4.6               | 4.6                |
| AVX2         | 14.4           | 146.0           | 26.4              | 180.5              |
| AVX-512/VNNI | 12.0           | 127.0           | 34.5              | 98.1               |

Note: FP32 AVX-512 is slower than AVX2 with 16 threads due to AVX-512 thermal
throttling (frequency downclocking when all cores run AVX-512 simultaneously).

## Notes
- Target: C11 with SIMD intrinsics + OpenMP
- No external dependencies for core pipeline
- Runtime dispatch via function pointers based on CPUID
- All matrices row-major, 64-byte aligned
- CPU: Intel Xeon Platinum 8581C (Emerald Rapids), 16 cores
- Full feature set: AVX2, AVX-512, VNNI, AMX (INT8 + BF16)
