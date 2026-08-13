/*
 * dispatch.c - Kernel dispatch based on CPU features
 *
 * Selects the best GEMM kernel for the detected CPU.
 */

#include "qat_cpu.h"

void kernel_dispatch_init(KernelDispatch *kd, const CpuFeatures *cpu) {
    /* INT8 GEMM: prefer VNNI > AVX2 > scalar */
    if (cpu->has_avx512vnni) {
        kd->int8_gemm = gemm_int8_vnni;
        kd->int8_name = "AVX-512 VNNI";
    } else if (cpu->has_avx2) {
        kd->int8_gemm = gemm_int8_avx2;
        kd->int8_name = "AVX2";
    } else {
        kd->int8_gemm = gemm_int8_scalar;
        kd->int8_name = "Scalar";
    }

    /* FP32 GEMM: prefer AVX-512 > AVX2 > scalar */
    if (cpu->has_avx512f) {
        kd->fp32_gemm = gemm_fp32_avx512;
        kd->fp32_name = "AVX-512";
    } else if (cpu->has_avx2 && cpu->has_fma) {
        kd->fp32_gemm = gemm_fp32_avx2;
        kd->fp32_name = "AVX2+FMA";
    } else {
        kd->fp32_gemm = gemm_fp32_scalar;
        kd->fp32_name = "Scalar";
    }
}

void kernel_dispatch_print(const KernelDispatch *kd) {
    printf("Kernel dispatch:\n");
    printf("  INT8 GEMM: %s\n", kd->int8_name);
    printf("  FP32 GEMM: %s\n", kd->fp32_name);
}
