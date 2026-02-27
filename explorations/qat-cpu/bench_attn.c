/*
 * bench_attn.c - A/B test for attention backward pass variants.
 *
 * Compares 4 configurations (2x2 factorial):
 *   A. Current interleaved layout (baseline)
 *   B. Head-first layout (no extract/scatter in inner loop)
 *   C. Interleaved + OpenMP on outer (b,h) loop
 *   D. Head-first + OpenMP on outer loop
 *
 * Each configuration is also run with OMP_NUM_THREADS=1 for a
 * single-threaded baseline.
 *
 * Verifies numerical equivalence between all variants.
 */

#include "qat_cpu.h"
#include <assert.h>
#include <omp.h>

/* Model dimensions matching train.c */
#define DIM         512
#define N_HEADS     8
#define HEAD_DIM    (DIM / N_HEADS)  /* 64 */
#define BATCH_SIZE  8
#define SEQ_LEN     64

#define N_WARMUP    5
#define N_ITERS     50

/* ======================================================================== */

/*
 * Fill tensor with deterministic pseudo-random values in [-0.1, 0.1].
 * Small range to keep softmax numerically reasonable.
 */
static void fill_random(float *data, int n, uint64_t *rng) {
    for (int i = 0; i < n; i++) {
        uint64_t r = rng_next(rng);
        data[i] = ((float)(r % 10000) / 10000.0f - 0.5f) * 0.2f;
    }
}

/* max_abs_diff is declared in qat_cpu.h and defined in memory.c */

/*
 * Run one backward variant n_iters times, return average time in ms.
 * Runs n_warmup iterations first (discarded).
 *
 * The backward pass modifies internal state (QATLinear grads), so we
 * re-run forward before each backward to restore saved activations.
 */
typedef Tensor *(*backward_fn)(Attention *, const Tensor *, int, int);

static double bench_backward(Attention *attn, const Tensor *input,
                              const Tensor *grad_output,
                              backward_fn bwd, int n_warmup, int n_iters) {
    int batch_size = BATCH_SIZE;
    int seq_len = SEQ_LEN;

    /* Warmup */
    for (int i = 0; i < n_warmup; i++) {
        Tensor *fwd = attention_forward(attn, input, batch_size, seq_len);
        Tensor *grad = bwd(attn, grad_output, batch_size, seq_len);
        tensor_free(fwd);
        tensor_free(grad);
    }

    /* Timed runs */
    double total_ms = 0.0;
    for (int i = 0; i < n_iters; i++) {
        /* Re-run forward to restore saved Q/K/V/attn */
        Tensor *fwd = attention_forward(attn, input, batch_size, seq_len);
        tensor_free(fwd);

        double t0 = timer_sec();
        Tensor *grad = bwd(attn, grad_output, batch_size, seq_len);
        double t1 = timer_sec();
        total_ms += (t1 - t0) * 1000.0;
        tensor_free(grad);
    }

    return total_ms / n_iters;
}

/*
 * Run backward once and return the grad_input tensor for comparison.
 */
static Tensor *run_once(Attention *attn, const Tensor *input,
                         const Tensor *grad_output, backward_fn bwd) {
    Tensor *fwd = attention_forward(attn, input, BATCH_SIZE, SEQ_LEN);
    tensor_free(fwd);
    return bwd(attn, grad_output, BATCH_SIZE, SEQ_LEN);
}

int main(void) {
    printf("=== Attention Backward A/B Test ===\n");
    printf("dim=%d, n_heads=%d, batch=%d, seq=%d\n",
           DIM, N_HEADS, BATCH_SIZE, SEQ_LEN);
    printf("Warmup=%d, Iterations=%d\n", N_WARMUP, N_ITERS);
    printf("OMP threads available: %d\n\n", omp_get_max_threads());

    /* Initialize — rng_next needs 4 uint64_t's (xoshiro256**) */
    uint64_t rng[4];
    rng_seed(rng, 42);
    CpuFeatures cpu;
    cpu_detect(&cpu);
    KernelDispatch kd_s;
    kernel_dispatch_init(&kd_s, &cpu);
    const KernelDispatch *kd = &kd_s;

    Attention *attn = attention_create(DIM, N_HEADS, kd, rng);
    attn->causal = true;

    /* Use FP32 forward — we only care about backward performance.
     * QAT mode uses INT8 GEMM for forward which may have alignment
     * requirements; FP32 mode is sufficient for populating saved state. */
    attn->wq->use_qat = false;
    attn->wk->use_qat = false;
    attn->wv->use_qat = false;
    attn->wo->use_qat = false;

    int total_tokens = BATCH_SIZE * SEQ_LEN;
    Tensor *input = tensor_create(total_tokens, DIM);
    Tensor *grad_output = tensor_create(total_tokens, DIM);
    fill_random(input->data, total_tokens * DIM, rng);
    fill_random(grad_output->data, total_tokens * DIM, rng);

    /* --- Phase 1: Verify numerical equivalence --- */
    printf("--- Numerical Equivalence Check ---\n");

    Tensor *ref = run_once(attn, input, grad_output, attention_backward);
    Tensor *hf  = run_once(attn, input, grad_output, attention_backward_headfirst);
    Tensor *omp_v = run_once(attn, input, grad_output, attention_backward_omp);
    Tensor *hf_omp = run_once(attn, input, grad_output, attention_backward_headfirst_omp);

    int n = total_tokens * DIM;
    float diff_hf     = max_abs_diff(ref->data, hf->data, n);
    float diff_omp    = max_abs_diff(ref->data, omp_v->data, n);
    float diff_hf_omp = max_abs_diff(ref->data, hf_omp->data, n);

    printf("  vs headfirst:        max|diff| = %.2e\n", diff_hf);
    printf("  vs omp:              max|diff| = %.2e\n", diff_omp);
    printf("  vs headfirst+omp:    max|diff| = %.2e\n", diff_hf_omp);

    /* Tolerance: FP32 GEMMs with 64-wide dot products, accumulated errors */
    float tol = 1e-3f;
    if (diff_hf > tol || diff_omp > tol || diff_hf_omp > tol) {
        printf("  WARNING: differences exceed tolerance %.1e!\n", tol);
    } else {
        printf("  All within tolerance %.1e -- OK\n", tol);
    }

    tensor_free(ref);
    tensor_free(hf);
    tensor_free(omp_v);
    tensor_free(hf_omp);

    /* --- Phase 2: Benchmark with full OMP threads --- */
    printf("\n--- Benchmark (OMP threads = %d) ---\n", omp_get_max_threads());

    double ms_baseline   = bench_backward(attn, input, grad_output,
                                           attention_backward, N_WARMUP, N_ITERS);
    double ms_headfirst  = bench_backward(attn, input, grad_output,
                                           attention_backward_headfirst, N_WARMUP, N_ITERS);
    double ms_omp        = bench_backward(attn, input, grad_output,
                                           attention_backward_omp, N_WARMUP, N_ITERS);
    double ms_hf_omp     = bench_backward(attn, input, grad_output,
                                           attention_backward_headfirst_omp, N_WARMUP, N_ITERS);

    printf("  %-30s %8.2f ms\n", "A. Interleaved (baseline):", ms_baseline);
    printf("  %-30s %8.2f ms  (%.2fx)\n", "B. Head-first:", ms_headfirst,
           ms_baseline / ms_headfirst);
    printf("  %-30s %8.2f ms  (%.2fx)\n", "C. Interleaved + outer OMP:", ms_omp,
           ms_baseline / ms_omp);
    printf("  %-30s %8.2f ms  (%.2fx)\n", "D. Head-first + outer OMP:", ms_hf_omp,
           ms_baseline / ms_hf_omp);

    /* --- Phase 3: Benchmark with OMP_NUM_THREADS=1 --- */
    printf("\n--- Benchmark (single-threaded, OMP_NUM_THREADS=1) ---\n");

    omp_set_num_threads(1);

    double ms1_baseline  = bench_backward(attn, input, grad_output,
                                           attention_backward, N_WARMUP, N_ITERS);
    double ms1_headfirst = bench_backward(attn, input, grad_output,
                                           attention_backward_headfirst, N_WARMUP, N_ITERS);
    double ms1_omp       = bench_backward(attn, input, grad_output,
                                           attention_backward_omp, N_WARMUP, N_ITERS);
    double ms1_hf_omp    = bench_backward(attn, input, grad_output,
                                           attention_backward_headfirst_omp, N_WARMUP, N_ITERS);

    printf("  %-30s %8.2f ms\n", "A. Interleaved (baseline):", ms1_baseline);
    printf("  %-30s %8.2f ms  (%.2fx)\n", "B. Head-first:", ms1_headfirst,
           ms1_baseline / ms1_headfirst);
    printf("  %-30s %8.2f ms  (%.2fx)\n", "C. Interleaved + outer OMP:", ms1_omp,
           ms1_baseline / ms1_omp);
    printf("  %-30s %8.2f ms  (%.2fx)\n", "D. Head-first + outer OMP:", ms1_hf_omp,
           ms1_baseline / ms1_hf_omp);

    /* --- Summary table --- */
    printf("\n--- Summary (ms per backward call) ---\n");
    printf("%-25s %10s %10s\n", "", "16 threads", "1 thread");
    printf("%-25s %10.2f %10.2f\n", "A. Interleaved", ms_baseline, ms1_baseline);
    printf("%-25s %10.2f %10.2f\n", "B. Head-first", ms_headfirst, ms1_headfirst);
    printf("%-25s %10.2f %10.2f\n", "C. Interleaved+outerOMP", ms_omp, ms1_omp);
    printf("%-25s %10.2f %10.2f\n", "D. Head-first+outerOMP", ms_hf_omp, ms1_hf_omp);

    /* Cleanup */
    tensor_free(input);
    tensor_free(grad_output);
    attention_free(attn);

    printf("\nDone.\n");
    return 0;
}
