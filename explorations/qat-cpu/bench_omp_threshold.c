/*
 * bench_omp_threshold.c - Measure GEMM time with/without OpenMP at different sizes
 *
 * Tests whether OpenMP helps or hurts for small (attention-sized) vs
 * large (linear layer-sized) GEMMs.
 */

#include "qat_cpu.h"
#include <omp.h>

static void bench_gemm(const char *label, int M, int N, int K, int iters,
                       KernelDispatch *kd) {
    /* FP32 GEMM */
    float *A = (float *)qat_alloc(M * K * sizeof(float));
    float *B = (float *)qat_alloc(K * N * sizeof(float));
    float *C = (float *)qat_alloc(M * N * sizeof(float));
    for (int i = 0; i < M * K; i++) A[i] = 0.01f * (i % 97);
    for (int i = 0; i < K * N; i++) B[i] = 0.01f * (i % 89);

    gemm_fp32_fn gemm = kd->fp32_gemm;

    /* Warmup */
    for (int i = 0; i < 5; i++)
        gemm(M, N, K, 1.0f, A, K, B, N, 0.0f, C, N);

    double t0 = timer_sec();
    for (int i = 0; i < iters; i++)
        gemm(M, N, K, 1.0f, A, K, B, N, 0.0f, C, N);
    double elapsed = timer_sec() - t0;

    double us_per_call = (elapsed / iters) * 1e6;
    double gflops = (2.0 * M * N * K * iters) / elapsed / 1e9;
    printf("  %-40s [%4d x %4d x %4d]  %7.1f us/call  %6.2f GFLOP/s\n",
           label, M, N, K, us_per_call, gflops);

    qat_free(A);
    qat_free(B);
    qat_free(C);
}

static void bench_gemm_i8(const char *label, int M, int N, int K, int iters,
                          KernelDispatch *kd) {
    int8_t *A = (int8_t *)qat_alloc(M * K);
    int8_t *B = (int8_t *)qat_alloc(K * N);
    int32_t *C = (int32_t *)qat_alloc(M * N * sizeof(int32_t));
    for (int i = 0; i < M * K; i++) A[i] = (int8_t)(i % 127 - 63);
    for (int i = 0; i < K * N; i++) B[i] = (int8_t)(i % 127 - 63);

    gemm_int8_fn gemm = kd->int8_gemm;

    for (int i = 0; i < 5; i++)
        gemm(M, N, K, A, K, B, N, C, N);

    double t0 = timer_sec();
    for (int i = 0; i < iters; i++)
        gemm(M, N, K, A, K, B, N, C, N);
    double elapsed = timer_sec() - t0;

    double us_per_call = (elapsed / iters) * 1e6;
    double gops = (2.0 * M * N * K * iters) / elapsed / 1e9;
    printf("  %-40s [%4d x %4d x %4d]  %7.1f us/call  %6.2f GOP/s\n",
           label, M, N, K, us_per_call, gops);

    qat_free(A);
    qat_free(B);
    qat_free(C);
}

int main(void) {
    setvbuf(stdout, NULL, _IOLBF, 0);

    CpuFeatures cpu;
    cpu_detect(&cpu);
    KernelDispatch kd;
    kernel_dispatch_init(&kd, &cpu);

    int max_threads = omp_get_max_threads();

    printf("=== OpenMP Threshold Benchmark ===\n");
    printf("CPU cores: %d, OMP max threads: %d\n\n", cpu.num_cores, max_threads);

    /* Test sizes matching our model:
     * Attention per-head: M=64, K=64, N=64
     * Linear layer (batch=8): M=512, K=512, N=512  and  M=512, K=512, N=2048
     */

    printf("--- FP32 GEMM with OMP_NUM_THREADS=%d ---\n", max_threads);
    bench_gemm("Attn head (64x64x64)", 64, 64, 64, 2000, &kd);
    bench_gemm("Linear small (512x512x512)", 512, 512, 512, 200, &kd);
    bench_gemm("Linear large (512x2048x512)", 512, 2048, 512, 100, &kd);

    printf("\n--- INT8 GEMM with OMP_NUM_THREADS=%d ---\n", max_threads);
    bench_gemm_i8("Attn head (64x64x64)", 64, 64, 64, 2000, &kd);
    bench_gemm_i8("Linear small (512x512x512)", 512, 512, 512, 200, &kd);
    bench_gemm_i8("Linear large (512x2048x512)", 512, 2048, 512, 100, &kd);

    /* Now disable OpenMP and re-run */
    omp_set_num_threads(1);

    printf("\n--- FP32 GEMM with OMP_NUM_THREADS=1 ---\n");
    bench_gemm("Attn head (64x64x64)", 64, 64, 64, 2000, &kd);
    bench_gemm("Linear small (512x512x512)", 512, 512, 512, 200, &kd);
    bench_gemm("Linear large (512x2048x512)", 512, 2048, 512, 100, &kd);

    printf("\n--- INT8 GEMM with OMP_NUM_THREADS=1 ---\n");
    bench_gemm_i8("Attn head (64x64x64)", 64, 64, 64, 2000, &kd);
    bench_gemm_i8("Linear small (512x512x512)", 512, 512, 512, 200, &kd);
    bench_gemm_i8("Linear large (512x2048x512)", 512, 2048, 512, 100, &kd);

    printf("\nDone.\n");
    return 0;
}
