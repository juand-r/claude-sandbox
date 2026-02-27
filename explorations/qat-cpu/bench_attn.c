/*
 * bench_attn.c - Benchmark for attention backward pass.
 *
 * Times attention_backward() (which uses OpenMP on the outer (b,h) loop).
 * Tests with both full threads and single-threaded for comparison.
 */

#include "qat_cpu.h"
#include <omp.h>

/* Model dimensions matching train.c */
#define DIM         512
#define N_HEADS     8
#define BATCH_SIZE  8
#define SEQ_LEN     64

#define N_WARMUP    5
#define N_ITERS     50

static void fill_random(float *data, int n, uint64_t *rng) {
    for (int i = 0; i < n; i++) {
        uint64_t r = rng_next(rng);
        data[i] = ((float)(r % 10000) / 10000.0f - 0.5f) * 0.2f;
    }
}

static double bench_backward(Attention *attn, const Tensor *input,
                              const Tensor *grad_output,
                              int n_warmup, int n_iters) {
    /* Warmup */
    for (int i = 0; i < n_warmup; i++) {
        Tensor *fwd = attention_forward(attn, input, BATCH_SIZE, SEQ_LEN);
        Tensor *grad = attention_backward(attn, grad_output, BATCH_SIZE, SEQ_LEN);
        tensor_free(fwd);
        tensor_free(grad);
    }

    /* Timed runs */
    double total_ms = 0.0;
    for (int i = 0; i < n_iters; i++) {
        Tensor *fwd = attention_forward(attn, input, BATCH_SIZE, SEQ_LEN);
        tensor_free(fwd);

        double t0 = timer_sec();
        Tensor *grad = attention_backward(attn, grad_output, BATCH_SIZE, SEQ_LEN);
        double t1 = timer_sec();
        total_ms += (t1 - t0) * 1000.0;
        tensor_free(grad);
    }

    return total_ms / n_iters;
}

int main(void) {
    printf("=== Attention Backward Benchmark ===\n");
    printf("dim=%d, n_heads=%d, batch=%d, seq=%d\n",
           DIM, N_HEADS, BATCH_SIZE, SEQ_LEN);
    printf("Warmup=%d, Iterations=%d\n", N_WARMUP, N_ITERS);
    printf("OMP threads available: %d\n\n", omp_get_max_threads());

    uint64_t rng[4];
    rng_seed(rng, 42);
    CpuFeatures cpu;
    cpu_detect(&cpu);
    KernelDispatch kd_s;
    kernel_dispatch_init(&kd_s, &cpu);
    const KernelDispatch *kd = &kd_s;

    Attention *attn = attention_create(DIM, N_HEADS, kd, rng);
    attn->causal = true;
    attn->wq->use_qat = false;
    attn->wk->use_qat = false;
    attn->wv->use_qat = false;
    attn->wo->use_qat = false;

    int total_tokens = BATCH_SIZE * SEQ_LEN;
    Tensor *input = tensor_create(total_tokens, DIM);
    Tensor *grad_output = tensor_create(total_tokens, DIM);
    fill_random(input->data, total_tokens * DIM, rng);
    fill_random(grad_output->data, total_tokens * DIM, rng);

    /* Benchmark with full threads */
    int n_threads = omp_get_max_threads();
    double ms_full = bench_backward(attn, input, grad_output, N_WARMUP, N_ITERS);
    printf("  %d threads: %.2f ms/backward\n", n_threads, ms_full);

    /* Benchmark single-threaded */
    omp_set_num_threads(1);
    double ms_single = bench_backward(attn, input, grad_output, N_WARMUP, N_ITERS);
    printf("  1 thread:   %.2f ms/backward\n", ms_single);
    printf("  Speedup:    %.2fx\n", ms_single / ms_full);

    tensor_free(input);
    tensor_free(grad_output);
    attention_free(attn);

    printf("\nDone.\n");
    return 0;
}
