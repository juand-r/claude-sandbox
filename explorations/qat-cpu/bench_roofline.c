/*
 * bench_roofline.c - Memory bandwidth + GEMM throughput benchmark
 *
 * Measures:
 *   1. Peak memory bandwidth (STREAM triad: a = b + scalar * c)
 *   2. FP32 GEMM throughput at various sizes (matching our model's operations)
 *   3. INT8 GEMM throughput at same sizes
 *   4. Arithmetic intensity analysis for each GEMM size
 *
 * This tells us whether we're compute-bound or memory-bound at each size,
 * and where the crossover (roofline knee) is.
 */

#include "qat_cpu.h"
#include <assert.h>
#include <omp.h>

/* ========================================================================
 * Memory bandwidth benchmark (STREAM-style)
 * ======================================================================== */

/*
 * STREAM triad: a[i] = b[i] + scalar * c[i]
 * 3 memory accesses per element (2 reads + 1 write) = 12 bytes/element
 * 1 FMA per element = 2 FLOPs/element
 * Arithmetic intensity = 2 / 12 = 0.167 FLOPs/byte
 */
static double bench_bandwidth(int n_elements, int n_iters) {
    float *a = (float *)qat_alloc(n_elements * sizeof(float));
    float *b = (float *)qat_alloc(n_elements * sizeof(float));
    float *c = (float *)qat_alloc(n_elements * sizeof(float));
    float scalar = 3.14159f;

    /* Init */
    for (int i = 0; i < n_elements; i++) {
        a[i] = 0.0f;
        b[i] = 1.0f;
        c[i] = 2.0f;
    }

    /* Warmup */
    for (int i = 0; i < n_elements; i++)
        a[i] = b[i] + scalar * c[i];

    /* Timed */
    double t0 = timer_sec();
    for (int iter = 0; iter < n_iters; iter++) {
        #pragma omp parallel for
        for (int i = 0; i < n_elements; i++)
            a[i] = b[i] + scalar * c[i];
    }
    double elapsed = timer_sec() - t0;

    /* Prevent dead code elimination */
    volatile float sink = a[0];
    (void)sink;

    double bytes_total = (double)n_elements * 12.0 * n_iters; /* 2 reads + 1 write */
    double gb_per_sec = bytes_total / elapsed / 1e9;

    qat_free(a); qat_free(b); qat_free(c);
    return gb_per_sec;
}

/* ========================================================================
 * GEMM throughput benchmark
 * ======================================================================== */

typedef struct {
    int M, N, K;
    const char *label;
    double fp32_gflops;
    double int8_gflops;
    double arith_intensity; /* FLOPs/byte */
} GemmBench;

/*
 * Arithmetic intensity for GEMM C[MxN] = A[MxK] * B[KxN]:
 *   FLOPs = 2*M*N*K
 *   Memory = (M*K + K*N + M*N) * bytes_per_element
 *   AI = 2*M*N*K / ((M*K + K*N + M*N) * bpe)
 *
 * For FP32: bpe = 4
 * For INT8: bpe = 1 (inputs) but output is INT32 (4 bytes)
 *           Memory = M*K + K*N (INT8 reads) + M*N*4 (INT32 write)
 *
 * Note: this is "cold" AI. If matrices fit in cache, effective bandwidth
 * is much higher and the roofline shifts.
 */
static double gemm_arith_intensity_fp32(int M, int N, int K) {
    double flops = 2.0 * M * N * K;
    double bytes = ((double)M * K + (double)K * N + (double)M * N) * 4.0;
    return flops / bytes;
}

static double bench_fp32_gemm(gemm_fp32_fn gemm, int M, int N, int K, int n_iters) {
    float *A = (float *)qat_alloc(M * K * sizeof(float));
    float *B = (float *)qat_alloc(K * N * sizeof(float));
    float *C = (float *)qat_alloc(M * N * sizeof(float));

    /* Random init */
    for (int i = 0; i < M * K; i++) A[i] = (float)(i % 17) * 0.1f;
    for (int i = 0; i < K * N; i++) B[i] = (float)(i % 13) * 0.1f;
    memset(C, 0, M * N * sizeof(float));

    /* Warmup */
    gemm(M, N, K, 1.0f, A, K, B, N, 0.0f, C, N);

    /* Timed */
    double t0 = timer_sec();
    for (int i = 0; i < n_iters; i++) {
        gemm(M, N, K, 1.0f, A, K, B, N, 0.0f, C, N);
    }
    double elapsed = timer_sec() - t0;

    double flops_total = 2.0 * M * N * K * (double)n_iters;
    double gflops = flops_total / elapsed / 1e9;

    qat_free(A); qat_free(B); qat_free(C);
    return gflops;
}

static double bench_int8_gemm(gemm_int8_fn gemm, int M, int N, int K, int n_iters) {
    int8_t *A = (int8_t *)qat_alloc(M * K);
    int8_t *B = (int8_t *)qat_alloc(K * N);
    int32_t *C = (int32_t *)qat_alloc(M * N * sizeof(int32_t));

    for (int i = 0; i < M * K; i++) A[i] = (int8_t)((i % 17) - 8);
    for (int i = 0; i < K * N; i++) B[i] = (int8_t)((i % 13) - 6);
    memset(C, 0, M * N * sizeof(int32_t));

    /* Warmup */
    gemm(M, N, K, A, K, B, N, C, N);

    /* Timed */
    double t0 = timer_sec();
    for (int i = 0; i < n_iters; i++) {
        gemm(M, N, K, A, K, B, N, C, N);
    }
    double elapsed = timer_sec() - t0;

    double ops_total = 2.0 * M * N * K * (double)n_iters;
    double gops = ops_total / elapsed / 1e9;

    qat_free(A); qat_free(B); qat_free(C);
    return gops;
}

/* ========================================================================
 * Memory footprint analysis
 * ======================================================================== */

static void print_memory_analysis(int batch_size, int seq_len,
                                   int dim, int n_layers, int n_heads,
                                   int hidden_dim, int vocab_size) {
    int total_tokens = batch_size * seq_len;
    int head_dim = dim / n_heads;

    /* Model weights */
    long params = 0;
    /* Per layer: Wq, Wk, Wv, Wo = 4 * dim * dim, ffn_up = dim * hidden, ffn_down = hidden * dim */
    long per_layer = 4L * dim * dim + 2L * dim * hidden_dim;
    /* Plus RMSNorm weights: 2 * dim per layer */
    per_layer += 2L * dim;
    params += n_layers * per_layer;
    /* Embeddings */
    params += (long)vocab_size * dim + (long)seq_len * dim; /* actually max_seq_len, using seq_len */
    /* Output head */
    params += (long)dim * vocab_size;
    /* Final norm */
    params += dim;

    printf("\n=== Memory Footprint Analysis ===\n");
    printf("Config: batch=%d, seq=%d, dim=%d, layers=%d, heads=%d, hidden=%d\n",
           batch_size, seq_len, dim, n_layers, n_heads, hidden_dim);
    printf("\n--- Model Weights ---\n");
    printf("  Parameters:           %ld (%.1f MB FP32)\n", params, params * 4.0 / 1e6);
    printf("  Gradients:            %.1f MB\n", params * 4.0 / 1e6);
    printf("  Adam state (m+v):     %.1f MB\n", params * 8.0 / 1e6);
    printf("  Subtotal (static):    %.1f MB\n", params * 16.0 / 1e6);

    printf("\n--- Activations (per transformer block) ---\n");
    double mb = 1e6;
    double saved_res1 = total_tokens * dim * 4.0 / mb;
    double saved_norm1 = total_tokens * dim * 4.0 / mb;
    double saved_res2 = total_tokens * dim * 4.0 / mb;
    double saved_norm2 = total_tokens * dim * 4.0 / mb;
    double saved_ffn = total_tokens * hidden_dim * 4.0 / mb;
    double saved_qkv = 3.0 * total_tokens * dim * 4.0 / mb;
    double saved_attn = (double)batch_size * n_heads * seq_len * seq_len * 4.0 / mb;
    double saved_input = total_tokens * dim * 4.0 / mb;
    double per_block = saved_res1 + saved_norm1 + saved_res2 + saved_norm2 +
                       saved_ffn + saved_qkv + saved_attn + saved_input;

    printf("  saved_residual1:      %.1f MB  (%d x %d x 4B)\n", saved_res1, total_tokens, dim);
    printf("  saved_normed1:        %.1f MB  (%d x %d x 4B)\n", saved_norm1, total_tokens, dim);
    printf("  saved_residual2:      %.1f MB  (%d x %d x 4B)\n", saved_res2, total_tokens, dim);
    printf("  saved_normed2:        %.1f MB  (%d x %d x 4B)\n", saved_norm2, total_tokens, dim);
    printf("  saved_ffn_hidden:     %.1f MB  (%d x %d x 4B)\n", saved_ffn, total_tokens, hidden_dim);
    printf("  saved_q/k/v:          %.1f MB  (3 x %d x %d x 4B)\n", saved_qkv, total_tokens, dim);
    printf("  saved_attn_weights:   %.1f MB  (%d x %d x %d x %d x 4B)\n",
           saved_attn, batch_size, n_heads, seq_len, seq_len);
    printf("  saved_input (qatlin): %.1f MB  (%d x %d x 4B)\n", saved_input, total_tokens, dim);
    printf("  Per-block subtotal:   %.1f MB\n", per_block);
    printf("  All %d blocks:        %.1f MB\n", n_layers, n_layers * per_block);

    /* QATLinear saved_input per layer */
    /* 6 QATLinear per block, each saves [total_tokens, in_features] */
    double qatlin_saved = 0;
    /* Wq,Wk,Wv,Wo: in=dim, ffn_up: in=dim, ffn_down: in=hidden */
    for (int l = 0; l < n_layers; l++) {
        qatlin_saved += 4.0 * total_tokens * dim * 4.0 / mb;      /* Wq,Wk,Wv,Wo */
        qatlin_saved += total_tokens * dim * 4.0 / mb;             /* ffn_up */
        qatlin_saved += total_tokens * hidden_dim * 4.0 / mb;      /* ffn_down */
    }
    qatlin_saved += total_tokens * dim * 4.0 / mb;  /* output head */
    printf("\n--- QATLinear saved inputs ---\n");
    printf("  Total saved inputs:   %.1f MB\n", qatlin_saved);

    /* Intermediate tensors during forward/backward */
    double logits = total_tokens * (double)vocab_size * 4.0 / mb;
    double grad_logits = logits;
    printf("\n--- Intermediate tensors ---\n");
    printf("  Logits:               %.1f MB  (%d x %d x 4B)\n", logits, total_tokens, vocab_size);
    printf("  Grad logits:          %.1f MB\n", grad_logits);

    /* Attention per-head buffers (allocated each forward call) */
    double attn_bufs = 0;
    attn_bufs += 2.0 * seq_len * head_dim * 4.0 / mb;  /* q_h, k_h */
    attn_bufs += head_dim * seq_len * 4.0 / mb;          /* k_h_t */
    attn_bufs += seq_len * head_dim * 4.0 / mb;          /* v_h */
    attn_bufs += seq_len * seq_len * 4.0 / mb;            /* scores */
    attn_bufs += seq_len * seq_len * 4.0 / mb;            /* attn_w */
    attn_bufs += seq_len * head_dim * 4.0 / mb;          /* out_h */
    printf("  Attn per-head bufs:   %.1f MB (allocated/freed %d x %d times per step)\n",
           attn_bufs, batch_size, n_heads);

    double total_est = params * 16.0 / mb + n_layers * per_block +
                       qatlin_saved + logits + grad_logits;
    printf("\n--- Total estimated peak ---\n");
    printf("  Static (weights+opt): %.1f MB\n", params * 16.0 / mb);
    printf("  Activations:          %.1f MB\n", n_layers * per_block + qatlin_saved);
    printf("  Intermediates:        %.1f MB\n", logits + grad_logits);
    printf("  *** TOTAL:            %.1f MB ***\n", total_est);
    printf("  L3 cache:             260 MB\n");
    printf("  Ratio (total/L3):     %.1fx\n\n", total_est / 260.0);
}

/* ========================================================================
 * Main
 * ======================================================================== */

int main(void) {
    setvbuf(stdout, NULL, _IOLBF, 0);

    CpuFeatures cpu;
    cpu_detect(&cpu);
    KernelDispatch kd;
    kernel_dispatch_init(&kd, &cpu);

    printf("========================================\n");
    printf("Roofline Analysis Benchmark\n");
    printf("========================================\n");
    printf("CPU: %s\n", cpu.brand_string);
    printf("Cores: %d\n", cpu.num_cores);
    printf("Base clock: 2.1 GHz\n");
    /* Theoretical peaks for Xeon 8581C @ 2.1 GHz, 16 cores:
     * FP32: 16 FMA units * 2 (FMA) * 16 (AVX-512 width) * 2.1 GHz = 1075 GFLOPS
     *   Actually: per-core = 2 FMA ports * 16 floats * 2 (fma) * 2.1 GHz = 134.4 GFLOPS
     *   16 cores = 2150 GFLOPS  (but depends on turbo and FMA ports)
     * INT8 VNNI: 4x throughput multiplier on FP32
     */
    kernel_dispatch_print(&kd);

    /* === Memory Bandwidth === */
    printf("\n========================================\n");
    printf("1. Memory Bandwidth (STREAM Triad)\n");
    printf("========================================\n");
    printf("  a[i] = b[i] + scalar * c[i]\n");
    printf("  Arithmetic intensity: 0.167 FLOP/byte\n\n");

    /* Different array sizes to see cache effects */
    struct { int n; const char *label; } bw_sizes[] = {
        {     8192, "32 KB (fits L1)"},
        {   131072, "512 KB (fits L2)"},
        {  4194304, "16 MB (fits L3)"},
        { 67108864, "256 MB (~L3 size)"},
        {134217728, "512 MB (exceeds L3)"},
    };
    int n_bw = sizeof(bw_sizes) / sizeof(bw_sizes[0]);

    for (int i = 0; i < n_bw; i++) {
        int iters = (i < 3) ? 10000 : 100;
        double gb_s = bench_bandwidth(bw_sizes[i].n, iters);
        printf("  %-25s  %7.1f GB/s\n", bw_sizes[i].label, gb_s);
    }

    /* === Memory Footprint === */
    printf("\n========================================\n");
    printf("2. Memory Footprint Analysis\n");
    printf("========================================\n");

    printf("\n--- OLD config (batch=8, seq=64) ---");
    print_memory_analysis(8, 64, 512, 2, 8, 2048, 128);

    printf("\n--- NEW config (batch=32, seq=256) ---");
    print_memory_analysis(32, 256, 512, 2, 8, 2048, 128);

    /* === GEMM Benchmarks === */
    printf("\n========================================\n");
    printf("3. GEMM Throughput vs Size\n");
    printf("========================================\n\n");

    /* GEMM sizes that appear in our model:
     *
     * QATLinear (batched):
     *   Wq,Wk,Wv,Wo: [B*S, 512] x [512, 512]   (old: M=512, new: M=8192)
     *   ffn_up:       [B*S, 512] x [512, 2048]   (old: M=512, new: M=8192)
     *   ffn_down:     [B*S, 2048] x [2048, 512]  (old: M=512, new: M=8192)
     *   output_head:  [B*S, 512] x [512, 128]    (old: M=512, new: M=8192)
     *
     * Attention per-head (tiny GEMMs, per batch element per head):
     *   Scores:  [S, 64] x [64, S]   (M=S, N=S, K=64)
     *   Values:  [S, S]  x [S, 64]   (M=S, N=64, K=S)
     *
     * With old config: S=64,  B*S=512
     * With new config: S=256, B*S=8192
     */

    GemmBench benchmarks[] = {
        /* Linear layers - OLD config (M=B*S=512) */
        {512,  512,  512,  "Linear 512x512 (old B*S=512)",  0, 0, 0},
        {512,  2048, 512,  "FFN up 512->2048 (old B*S=512)", 0, 0, 0},
        {512,  512,  2048, "FFN dn 2048->512 (old B*S=512)", 0, 0, 0},

        /* Linear layers - NEW config (M=B*S=8192) */
        {8192, 512,  512,  "Linear 512x512 (new B*S=8192)", 0, 0, 0},
        {8192, 2048, 512,  "FFN up 512->2048 (new B*S=8192)", 0, 0, 0},
        {8192, 512,  2048, "FFN dn 2048->512 (new B*S=8192)", 0, 0, 0},
        {8192, 128,  512,  "Output 512->128 (new B*S=8192)", 0, 0, 0},

        /* Attention GEMMs - OLD config (seq=64) */
        {64,   64,   64,   "Attn scores (old S=64)",  0, 0, 0},
        {64,   64,   64,   "Attn values (old S=64)",  0, 0, 0},

        /* Attention GEMMs - NEW config (seq=256) */
        {256,  256,  64,   "Attn scores (new S=256)", 0, 0, 0},
        {256,  64,   256,  "Attn values (new S=256)", 0, 0, 0},

        /* For reference: square GEMMs at various sizes */
        {64,   64,   64,   "Square 64x64",   0, 0, 0},
        {128,  128,  128,  "Square 128x128", 0, 0, 0},
        {256,  256,  256,  "Square 256x256", 0, 0, 0},
        {512,  512,  512,  "Square 512x512", 0, 0, 0},
        {1024, 1024, 1024, "Square 1024x1024", 0, 0, 0},
        {2048, 2048, 2048, "Square 2048x2048", 0, 0, 0},
    };
    int n_bench = sizeof(benchmarks) / sizeof(benchmarks[0]);

    printf("  %-38s %6s %6s %6s  %8s %8s\n",
           "Operation", "M", "N", "K", "FP32 GF", "INT8 GOP");
    printf("  %-38s %6s %6s %6s  %8s %8s\n",
           "-------------------------------------", "------", "------", "------",
           "--------", "--------");

    for (int i = 0; i < n_bench; i++) {
        int M = benchmarks[i].M, N = benchmarks[i].N, K = benchmarks[i].K;
        /* Choose iterations to get ~1 second per benchmark */
        double flops_one = 2.0 * M * N * K;
        int iters = (int)(1e10 / flops_one);  /* target ~10 GFLOPS worth */
        if (iters < 10) iters = 10;
        if (iters > 100000) iters = 100000;

        benchmarks[i].fp32_gflops = bench_fp32_gemm(kd.fp32_gemm, M, N, K, iters);
        benchmarks[i].int8_gflops = bench_int8_gemm(kd.int8_gemm, M, N, K, iters);
        benchmarks[i].arith_intensity = gemm_arith_intensity_fp32(M, N, K);

        printf("  %-38s %6d %6d %6d  %7.1f  %7.1f\n",
               benchmarks[i].label, M, N, K,
               benchmarks[i].fp32_gflops, benchmarks[i].int8_gflops);
    }

    /* === Roofline Analysis === */
    printf("\n========================================\n");
    printf("4. Roofline Analysis\n");
    printf("========================================\n\n");

    /* Use the 256MB bandwidth as our "DRAM bandwidth" */
    /* Actually let's use multiple levels */
    printf("  %-38s  AI(F/B)  FP32 GF  INT8 GOP  Bound?\n", "Operation");
    printf("  %-38s  -------  -------  --------  ------\n",
           "-------------------------------------");

    for (int i = 0; i < n_bench; i++) {
        /* Simple heuristic: if throughput is < 50% of peak, likely memory-bound */
        double fp32_peak = benchmarks[n_bench-1].fp32_gflops; /* use largest GEMM as proxy */
        const char *bound = (benchmarks[i].fp32_gflops < 0.5 * fp32_peak) ? "MEM" : "COMPUTE";
        printf("  %-38s  %6.1f   %7.1f  %7.1f   %s\n",
               benchmarks[i].label, benchmarks[i].arith_intensity,
               benchmarks[i].fp32_gflops, benchmarks[i].int8_gflops, bound);
    }

    /* === Attention overhead analysis === */
    printf("\n========================================\n");
    printf("5. Attention Loop Overhead\n");
    printf("========================================\n\n");

    printf("  Per-head GEMM sizes with seq=%d:\n", 256);
    printf("    Scores: [256, 64] x [64, 256] = %d FLOPs\n", 2 * 256 * 256 * 64);
    printf("    Values: [256, 256] x [256, 64] = %d FLOPs\n", 2 * 256 * 64 * 256);
    printf("    Total per head: %d FLOPs\n", 2 * 2 * 256 * 256 * 64);
    printf("    Total per step: %d iterations x %d FLOPs = %.1f MFLOPs\n",
           32 * 8, 2 * 2 * 256 * 256 * 64,
           32.0 * 8 * 2 * 2 * 256 * 256 * 64 / 1e6);
    printf("\n");

    printf("  Overhead per iteration of attention inner loop:\n");
    printf("    - extract_head: 3 memcpy of %d x %d = %d bytes\n",
           256, 64, 3 * 256 * 64 * 4);
    printf("    - transpose K: %d x %d = %d bytes\n", 256, 64, 256 * 64 * 4);
    printf("    - causal mask: ~%d writes\n", 256 * 256 / 2);
    printf("    - softmax: %d rows of %d\n", 256, 256);
    printf("    - scatter_head: %d x %d = %d bytes\n", 256, 64, 256 * 64 * 4);
    printf("    - memcpy attn weights: %d bytes\n", 256 * 256 * 4);
    printf("    Total iterations: %d x %d = %d\n", 32, 8, 32 * 8);
    printf("    Estimated overhead: ~%.1f MB of data movement per step\n",
           32.0 * 8 * (3 * 256 * 64 * 4 + 256 * 64 * 4 + 256 * 256 * 4 + 256 * 64 * 4 + 256 * 256 * 4) / 1e6);

    /* === FLOPs accounting === */
    printf("\n========================================\n");
    printf("6. FLOPs Accounting (per step)\n");
    printf("========================================\n\n");

    int B = 32, S = 256;
    int total_tokens = B * S;
    double fwd_factor = 1.0, bwd_factor = 2.0; /* bwd ~= 2x fwd */

    /* Linear layer FLOPs */
    double lin_flops = 0;
    /* Per layer: 4 attn projections (dim->dim) + ffn_up (dim->hidden) + ffn_down (hidden->dim) */
    for (int l = 0; l < 2; l++) {
        lin_flops += 4.0 * 2.0 * total_tokens * 512 * 512;    /* Wq,Wk,Wv,Wo */
        lin_flops += 2.0 * total_tokens * 512 * 2048;           /* ffn_up */
        lin_flops += 2.0 * total_tokens * 2048 * 512;           /* ffn_down */
    }
    lin_flops += 2.0 * total_tokens * 512 * 128;                /* output head */
    double lin_flops_fwdbwd = lin_flops * (fwd_factor + bwd_factor);

    /* Attention GEMM FLOPs (per head, per batch element) */
    double attn_flops_per_head = 2.0 * S * S * 64 * 2;          /* scores + values */
    double attn_flops = attn_flops_per_head * B * 8 * 2;         /* n_heads * n_layers */
    double attn_flops_fwdbwd = attn_flops * (fwd_factor + bwd_factor);

    /* Old estimate (what estimate_flops_per_step computes) */
    double old_est_per_layer = 2.0 * 512 * (4.0 * 512 + 2.0 * 2048);
    double old_est_fwd_token = 2 * old_est_per_layer + 2.0 * 512 * 128;
    double old_est_total = 3.0 * old_est_fwd_token * total_tokens;

    printf("  Total tokens per step: %d x %d = %d\n", B, S, total_tokens);
    printf("\n  --- Linear layer FLOPs ---\n");
    printf("  Forward:              %.1f MFLOP\n", lin_flops / 1e6);
    printf("  Fwd+Bwd (3x):        %.1f MFLOP\n", lin_flops_fwdbwd / 1e6);

    printf("\n  --- Attention GEMM FLOPs ---\n");
    printf("  Per head (scores+val): %.0f FLOP\n", attn_flops_per_head);
    printf("  All heads/layers/batch: %.1f MFLOP\n", attn_flops / 1e6);
    printf("  Fwd+Bwd (3x):         %.1f MFLOP\n", attn_flops_fwdbwd / 1e6);

    printf("\n  --- Current estimate (linear only) ---\n");
    printf("  estimate_flops_per_step: %.1f MFLOP\n", old_est_total / 1e6);

    printf("\n  --- Corrected total ---\n");
    printf("  Linear + Attention:    %.1f MFLOP\n",
           (lin_flops_fwdbwd + attn_flops_fwdbwd) / 1e6);
    printf("  Attention fraction:    %.1f%%\n",
           attn_flops_fwdbwd / (lin_flops_fwdbwd + attn_flops_fwdbwd) * 100);
    printf("  Old estimate error:    %.1f%% (undercount)\n",
           (1.0 - old_est_total / (lin_flops_fwdbwd + attn_flops_fwdbwd)) * 100);

    /* Corrected MFU */
    printf("\n  --- Corrected MFU ---\n");
    double actual_ms_fp32 = 4561.3;  /* from training run */
    double actual_ms_qat  = 4758.0;
    double corrected_flops = lin_flops_fwdbwd + attn_flops_fwdbwd;
    printf("  FP32: %.4f TFLOPS (was %.4f with old estimate)\n",
           corrected_flops / actual_ms_fp32 / 1e9,
           old_est_total / actual_ms_fp32 / 1e9);
    printf("  QAT:  %.4f TFLOPS (was %.4f with old estimate)\n",
           corrected_flops / actual_ms_qat / 1e9,
           old_est_total / actual_ms_qat / 1e9);

    printf("\nDone.\n");
    return 0;
}
