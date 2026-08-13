# QAT-CPU: Quantized LLM Training on CPU via Hand-Tuned SIMD Kernels

First assembly-level, CPU-optimized quantization-aware training (QAT) pipeline for LLMs.
Exploits INT8 TOPS on Intel Xeons (AMX/VNNI) that sit idle during training.

## Architecture

- INT8 forward passes via VNNI/AMX GEMM kernels
- FP32/BF16 backward passes
- Straight-through estimator (STE) connecting them
- FP32 master weights updated by Adam

## How to Build

```bash
make            # build everything
make test       # run tests
make bench      # run benchmarks
make clean      # clean build artifacts
```

## Kernel Tiers (Runtime Dispatch)

1. **AMX INT8** (Sapphire Rapids+): TDPBSSD, ~245 INT8 TOPS
2. **AVX-512 VNNI** (Ice Lake+): VPDPBUSD, 64 MACs/instruction
3. **AVX2** (Haswell+): VPMADDUBSW + VPMADDWD, 32 MACs/iteration
4. **Scalar**: Reference implementation

## Project Structure

```
qat_cpu.h        - Main header (types, API, inline helpers)
cpu_detect.c     - CPU feature detection (CPUID)
memory.c         - Aligned allocation, tensor ops, RNG
kernels_scalar.c - Scalar reference INT8/FP32 GEMM
kernels_avx2.c   - AVX2 INT8/FP32 GEMM
kernels_vnni.c   - AVX-512 VNNI INT8 GEMM + AVX-512 FP32 GEMM
dispatch.c       - Runtime kernel dispatch via CPUID
quantize.c       - Quantization/dequantization (per-channel, per-token, per-column)
qat_linear.c     - QAT linear layer (INT8 forward, FP32 or INT8 backward, STE)
layers.c         - RMSNorm, GeLU, Softmax, Attention, TransformerBlock
optimizer.c      - Adam optimizer (AVX-512 vectorized)
loss.c           - Cross-entropy loss
train.c          - End-to-end training loop (FP32 vs QAT comparison)
profile_qat.c    - Per-component profiler (FP32 vs QAT vs QAT+INT8bwd)
test_main.c      - Test harness
bench_roofline.c - Roofline / GEMM throughput benchmark
bench_attn.c     - Attention backward A/B benchmark
```
