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

## Phase 7: Scaling (stretch)
- [ ] Multi-threaded GEMM (OpenMP)
- [ ] NUMA-aware allocation
- [ ] Gradient accumulation
- [ ] Larger model tests
- [ ] B-matrix prepack for VNNI kernel optimization

## Benchmark Results (Xeon Platinum 8581C, 256x256 GEMM)

| Kernel      | INT8 GOPS | FP32 GFLOPS |
|-------------|-----------|-------------|
| Scalar      | 3.4       | 2.8         |
| AVX2        | 12.1      | 24.4        |
| AVX-512/VNNI| 6.2       | 22.9        |

## Notes
- Target: C11 with SIMD intrinsics
- No external dependencies for core pipeline
- Runtime dispatch via function pointers based on CPUID
- All matrices row-major, 64-byte aligned
- CPU: Intel Xeon Platinum 8581C (Emerald Rapids), 16 cores
- Full feature set: AVX2, AVX-512, VNNI, AMX (INT8 + BF16)
