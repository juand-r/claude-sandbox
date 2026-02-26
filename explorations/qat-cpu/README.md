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
memory.c         - Aligned allocation, tensor ops
kernels_scalar.c - Scalar reference kernels
kernels_avx2.c   - AVX2 INT8/FP32 GEMM
kernels_vnni.c   - AVX-512 VNNI INT8 GEMM
kernels_fp32.c   - FP32 backward-pass GEMM (AVX2/AVX-512)
quantize.c       - Quantization/dequantization routines
qat_linear.c     - QAT linear layer (forward + backward + STE)
layers.c         - RMSNorm, GeLU, Softmax, Attention
optimizer.c      - Adam optimizer
train.c          - Training loop
test_main.c      - Test harness
bench_main.c     - Benchmarks
```
