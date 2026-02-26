/*
 * test_main.c - Test harness for QAT-CPU
 *
 * Verifies:
 * 1. SIMD GEMM kernels match scalar reference
 * 2. Quantization round-trip error
 * 3. QAT linear forward/backward correctness
 * 4. Gradient checking via finite differences
 * 5. Training convergence (loss decreases)
 */

#include "qat_cpu.h"
#include <assert.h>

/* Test infrastructure */
static int tests_run = 0;
static int tests_passed = 0;

#define TEST_START(name) do { \
    printf("\n--- TEST: %s ---\n", name); \
    tests_run++; \
} while(0)

#define TEST_PASS(name) do { \
    printf("PASS: %s\n", name); \
    tests_passed++; \
} while(0)

#define TEST_FAIL(name, ...) do { \
    printf("FAIL: %s - ", name); \
    printf(__VA_ARGS__); \
    printf("\n"); \
} while(0)

#define CHECK(cond, name, ...) do { \
    if (!(cond)) { TEST_FAIL(name, __VA_ARGS__); return; } \
} while(0)

/* ========================================================================
 * Test: INT8 GEMM scalar correctness
 * ======================================================================== */
static void test_gemm_int8_scalar(void) {
    TEST_START("INT8 GEMM scalar");

    int M = 4, N = 6, K = 8;
    int8_t *A = (int8_t *)qat_alloc(M * K);
    int8_t *B = (int8_t *)qat_alloc(K * N);
    int32_t *C = (int32_t *)qat_alloc(M * N * sizeof(int32_t));
    int32_t *C_ref = (int32_t *)qat_alloc(M * N * sizeof(int32_t));

    uint64_t rng[4];
    rng_seed(rng, 42);

    /* Fill with random INT8 values */
    for (int i = 0; i < M * K; i++) A[i] = (int8_t)(rng_next(rng) % 256 - 128);
    for (int i = 0; i < K * N; i++) B[i] = (int8_t)(rng_next(rng) % 256 - 128);

    /* Compute reference manually */
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            int32_t sum = 0;
            for (int k = 0; k < K; k++) {
                sum += (int32_t)A[i * K + k] * (int32_t)B[k * N + j];
            }
            C_ref[i * N + j] = sum;
        }
    }

    gemm_int8_scalar(M, N, K, A, K, B, N, C, N);

    /* Verify exact match */
    for (int i = 0; i < M * N; i++) {
        CHECK(C[i] == C_ref[i], "INT8 GEMM scalar",
              "mismatch at [%d]: got %d, expected %d", i, C[i], C_ref[i]);
    }

    qat_free(A); qat_free(B); qat_free(C); qat_free(C_ref);
    TEST_PASS("INT8 GEMM scalar");
}

/* ========================================================================
 * Test: INT8 GEMM SIMD vs scalar
 * ======================================================================== */
static void test_gemm_int8_simd(const char *name, gemm_int8_fn kernel) {
    TEST_START(name);

    /* Test several sizes including non-multiples of vector width */
    int sizes[][3] = {
        {1, 1, 1}, {4, 4, 4}, {7, 5, 3}, {16, 16, 16},
        {32, 32, 32}, {33, 17, 25}, {64, 64, 64}, {128, 64, 96}
    };
    int n_sizes = sizeof(sizes) / sizeof(sizes[0]);

    uint64_t rng[4];
    rng_seed(rng, 123);

    for (int s = 0; s < n_sizes; s++) {
        int M = sizes[s][0], N = sizes[s][1], K = sizes[s][2];

        int8_t *A = (int8_t *)qat_alloc(M * K);
        int8_t *B = (int8_t *)qat_alloc(K * N);
        int32_t *C_simd = (int32_t *)qat_calloc(M * N * sizeof(int32_t));
        int32_t *C_ref = (int32_t *)qat_calloc(M * N * sizeof(int32_t));

        for (int i = 0; i < M * K; i++) A[i] = (int8_t)(rng_next(rng) % 256 - 128);
        for (int i = 0; i < K * N; i++) B[i] = (int8_t)(rng_next(rng) % 256 - 128);

        gemm_int8_scalar(M, N, K, A, K, B, N, C_ref, N);
        kernel(M, N, K, A, K, B, N, C_simd, N);

        int mismatch = 0;
        for (int i = 0; i < M * N; i++) {
            if (C_simd[i] != C_ref[i]) {
                if (mismatch == 0) {
                    printf("  Size [%d x %d x %d]: first mismatch at [%d]: "
                           "SIMD=%d, scalar=%d\n", M, N, K, i, C_simd[i], C_ref[i]);
                }
                mismatch++;
            }
        }
        if (mismatch > 0) {
            printf("  Size [%d x %d x %d]: %d mismatches out of %d\n",
                   M, N, K, mismatch, M * N);
        }

        CHECK(mismatch == 0, name,
              "size [%d x %d x %d]: %d mismatches", M, N, K, mismatch);

        qat_free(A); qat_free(B); qat_free(C_simd); qat_free(C_ref);
    }

    TEST_PASS(name);
}

/* ========================================================================
 * Test: FP32 GEMM SIMD vs scalar
 * ======================================================================== */
static void test_gemm_fp32_simd(const char *name, gemm_fp32_fn kernel) {
    TEST_START(name);

    int sizes[][3] = {
        {1, 1, 1}, {4, 4, 4}, {7, 5, 3}, {16, 16, 16},
        {32, 32, 32}, {33, 17, 25}, {64, 64, 64}
    };
    int n_sizes = sizeof(sizes) / sizeof(sizes[0]);

    uint64_t rng[4];
    rng_seed(rng, 456);

    for (int s = 0; s < n_sizes; s++) {
        int M = sizes[s][0], N = sizes[s][1], K = sizes[s][2];

        float *A = (float *)qat_alloc(M * K * sizeof(float));
        float *B = (float *)qat_alloc(K * N * sizeof(float));
        float *C_simd = (float *)qat_calloc(M * N * sizeof(float));
        float *C_ref = (float *)qat_calloc(M * N * sizeof(float));

        for (int i = 0; i < M * K; i++) A[i] = rng_uniform(rng) * 2.0f - 1.0f;
        for (int i = 0; i < K * N; i++) B[i] = rng_uniform(rng) * 2.0f - 1.0f;

        float alpha = 1.0f, beta = 0.0f;
        gemm_fp32_scalar(M, N, K, alpha, A, K, B, N, beta, C_ref, N);
        kernel(M, N, K, alpha, A, K, B, N, beta, C_simd, N);

        float max_err = max_rel_error(C_ref, C_simd, M * N);
        /* Different summation order causes FP32 rounding differences.
         * 1e-3 is a reasonable tolerance for GEMM of this size. */
        CHECK(max_err < 1e-3f, name,
              "size [%d x %d x %d]: max relative error = %e", M, N, K, max_err);

        qat_free(A); qat_free(B); qat_free(C_simd); qat_free(C_ref);
    }

    TEST_PASS(name);
}

/* ========================================================================
 * Test: Quantization round-trip error
 * ======================================================================== */
static void test_quantization(void) {
    TEST_START("Quantization round-trip");

    int rows = 16, cols = 64;
    uint64_t rng[4];
    rng_seed(rng, 789);

    float *src = (float *)qat_alloc(rows * cols * sizeof(float));
    float *recovered = (float *)qat_alloc(rows * cols * sizeof(float));
    int8_t *quantized = (int8_t *)qat_alloc(rows * cols);
    float *scales = (float *)qat_alloc(rows * sizeof(float));

    /* Fill with random values in [-1, 1] */
    for (int i = 0; i < rows * cols; i++) {
        src[i] = rng_uniform(rng) * 2.0f - 1.0f;
    }

    /* Quantize and dequantize */
    quantize_per_channel(src, rows, cols, quantized, scales);

    /* Manual dequant: recovered[i][j] = quantized[i][j] * scales[i] */
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            recovered[i * cols + j] = (float)quantized[i * cols + j] * scales[i];
        }
    }

    /*
     * Check error using max absolute error relative to the row's absmax.
     * INT8 quantization error per element is at most scale/2 = absmax/(2*127).
     * For values near zero, relative error can be 100%, which is expected
     * and correct — the absolute error is still tiny.
     */
    float max_abs_err = max_abs_diff(src, recovered, rows * cols);
    /* Find max absmax across all rows to bound the expected error */
    float global_amax = 0.0f;
    for (int i = 0; i < rows * cols; i++) {
        float a = fabsf(src[i]);
        if (a > global_amax) global_amax = a;
    }
    float expected_max_err = global_amax / 127.0f;  /* Worst case per-element */
    printf("  Quantization round-trip max abs error: %e (expected bound: %e)\n",
           max_abs_err, expected_max_err);
    CHECK(max_abs_err <= expected_max_err + 1e-6f, "Quantization round-trip",
          "max abs error %e exceeds bound %e", max_abs_err, expected_max_err);

    /* Test fake quantization matches */
    float *fake_out = (float *)qat_alloc(rows * cols * sizeof(float));
    fake_quantize_per_channel(src, rows, cols, fake_out);

    float fake_err = max_abs_diff(recovered, fake_out, rows * cols);
    CHECK(fake_err < 1e-6f, "Fake quantization",
          "fake quant doesn't match manual round-trip: %e", fake_err);

    qat_free(src); qat_free(recovered); qat_free(quantized);
    qat_free(scales); qat_free(fake_out);
    TEST_PASS("Quantization round-trip");
}

/* ========================================================================
 * Test: QAT linear forward (compare INT8 path to FP32 reference)
 * ======================================================================== */
static void test_qat_linear_forward(const KernelDispatch *kd) {
    TEST_START("QAT linear forward");

    int batch = 8, in_f = 32, out_f = 16;
    uint64_t rng[4];
    rng_seed(rng, 1234);

    QATLinear *layer = qat_linear_create(in_f, out_f, true, kd, rng);

    /* Create input */
    Tensor *input = tensor_create(batch, in_f);
    tensor_rand(input, -1.0f, 1.0f, rng);

    /* QAT forward */
    Tensor *output = qat_linear_forward(layer, input);

    /* FP32 reference: output = input * weight^T + bias */
    Tensor *ref = tensor_zeros(batch, out_f);
    /* C[batch, out_f] = input[batch, in_f] * weight^T[in_f, out_f] */
    /* weight is [out_f x in_f], so weight^T is [in_f x out_f] */
    for (int i = 0; i < batch; i++) {
        for (int j = 0; j < out_f; j++) {
            float sum = 0.0f;
            for (int k = 0; k < in_f; k++) {
                sum += input->data[i * in_f + k] * layer->weight->data[j * in_f + k];
            }
            ref->data[i * out_f + j] = sum + layer->bias->data[j];
        }
    }

    /*
     * The QAT output should be close to FP32 reference.
     * Use mean absolute error normalized by mean absolute output,
     * since max_rel_error blows up on near-zero elements.
     */
    float sum_abs_err = 0.0f, sum_abs_ref = 0.0f;
    float max_abs = max_abs_diff(ref->data, output->data, batch * out_f);
    for (int idx = 0; idx < batch * out_f; idx++) {
        sum_abs_err += fabsf(ref->data[idx] - output->data[idx]);
        sum_abs_ref += fabsf(ref->data[idx]);
    }
    float mean_rel = sum_abs_err / fmaxf(sum_abs_ref, 1e-8f);
    printf("  QAT vs FP32: mean normalized error=%.4f, max abs err=%.4f\n",
           mean_rel, max_abs);

    /* INT8 quantization typically gives <5% mean error */
    CHECK(mean_rel < 0.10f, "QAT linear forward",
          "QAT mean normalized error too high: %e", mean_rel);

    tensor_free(input);
    tensor_free(output);
    tensor_free(ref);
    qat_linear_free(layer);
    TEST_PASS("QAT linear forward");
}

/* ========================================================================
 * Test: Gradient checking via finite differences
 *
 * Verify backward pass gradients match numerical gradient:
 *   d_numerical = (f(x+eps) - f(x-eps)) / (2*eps)
 * ======================================================================== */
static void test_gradient_check(const KernelDispatch *kd) {
    TEST_START("Gradient check (QAT linear)");

    /*
     * Larger dims = more quantization levels = smoother gradient landscape.
     * With in_f=64, each row has 64 values covering [-0.5, 0.5], giving
     * ~64 distinct quantization bins. This makes finite differences
     * agree better with STE.
     */
    int batch = 2, in_f = 64, out_f = 16;
    float eps = 5e-3f;  /* Larger eps to step across quantization bins */

    uint64_t rng[4];
    rng_seed(rng, 5678);

    QATLinear *layer = qat_linear_create(in_f, out_f, true, kd, rng);

    Tensor *input = tensor_create(batch, in_f);
    tensor_rand(input, -0.5f, 0.5f, rng);

    /* Forward pass to establish computational graph */
    Tensor *output = qat_linear_forward(layer, input);

    /* Create a simple loss: sum of all outputs (so grad_output = 1) */
    Tensor *grad_output = tensor_create(batch, out_f);
    tensor_fill(grad_output, 1.0f);

    /* Backward pass */
    qat_linear_zero_grad(layer);
    Tensor *grad_input = qat_linear_backward(layer, grad_output);

    /*
     * Check grad_input via finite differences.
     * For each input element, perturb +eps and -eps, compute forward,
     * sum outputs, compute numerical gradient.
     *
     * NOTE: Because the forward pass involves quantization (which is
     * a step function), the finite difference gradient won't match
     * the STE gradient for inputs near quantization boundaries.
     * The STE approximation assumes d(quant)/dx = 1, which is
     * only approximately true. We use a relaxed tolerance.
     */
    int n_checked = 0;
    int n_close = 0;
    float sum_abs_err = 0.0f, sum_abs_grad = 0.0f;

    for (int i = 0; i < batch; i++) {
        for (int j = 0; j < in_f; j++) {
            float orig = input->data[i * in_f + j];

            /* f(x + eps) */
            input->data[i * in_f + j] = orig + eps;
            Tensor *out_plus = qat_linear_forward(layer, input);
            float sum_plus = 0.0f;
            for (int k = 0; k < batch * out_f; k++) sum_plus += out_plus->data[k];

            /* f(x - eps) */
            input->data[i * in_f + j] = orig - eps;
            Tensor *out_minus = qat_linear_forward(layer, input);
            float sum_minus = 0.0f;
            for (int k = 0; k < batch * out_f; k++) sum_minus += out_minus->data[k];

            /* Restore */
            input->data[i * in_f + j] = orig;

            /* Numerical gradient */
            float num_grad = (sum_plus - sum_minus) / (2.0f * eps);
            float ana_grad = grad_input->data[i * in_f + j];

            float abs_err = fabsf(num_grad - ana_grad);
            float denom = fmaxf(fabsf(num_grad), fabsf(ana_grad));
            denom = fmaxf(denom, 1e-6f);
            float rel_err = abs_err / denom;

            sum_abs_err += abs_err;
            sum_abs_grad += fabsf(ana_grad);
            if (rel_err < 0.3f) n_close++;
            n_checked++;

            tensor_free(out_plus);
            tensor_free(out_minus);
        }
    }

    float mean_norm_err = sum_abs_err / fmaxf(sum_abs_grad, 1e-8f);
    float pct_close = 100.0f * (float)n_close / (float)n_checked;
    printf("  Gradient check: %d elements, %.0f%% within 30%% tolerance, "
           "mean normalized error: %.4f\n", n_checked, pct_close, mean_norm_err);

    /*
     * Due to quantization + STE, individual elements near quantization
     * boundaries can have large errors. What matters:
     * 1. Most elements agree (>50% within 30% tolerance)
     * 2. Mean error is reasonable (<50%)
     * 3. Training actually converges (tested separately)
     */
    CHECK(pct_close > 50.0f, "Gradient check",
          "too few gradients match: %.0f%%", pct_close);
    CHECK(mean_norm_err < 0.5f, "Gradient check",
          "mean normalized error too high: %e", mean_norm_err);

    tensor_free(input);
    tensor_free(output);
    tensor_free(grad_output);
    tensor_free(grad_input);
    qat_linear_free(layer);
    TEST_PASS("Gradient check (QAT linear)");
}

/* ========================================================================
 * Test: Training convergence
 * Verify loss decreases over training steps on a small model.
 * ======================================================================== */
static void test_training_convergence(const KernelDispatch *kd) {
    TEST_START("Training convergence");

    /* Tiny model: single QAT linear layer, learn to map random input to targets */
    int batch = 16, in_f = 32, n_classes = 8;
    int n_steps = 100;

    uint64_t rng[4];
    rng_seed(rng, 9999);

    QATLinear *layer = qat_linear_create(in_f, n_classes, true, kd, rng);
    Adam *opt = adam_create(0.01f, 0.9f, 0.999f, 1e-8f, 0.0f);

    adam_add_param(opt, layer->weight->data, layer->grad_weight->data,
                   tensor_numel(layer->weight));
    adam_add_param(opt, layer->bias->data, layer->grad_bias->data,
                   tensor_numel(layer->bias));

    /* Fixed input and targets */
    Tensor *input = tensor_create(batch, in_f);
    tensor_rand(input, -1.0f, 1.0f, rng);
    int *targets = (int *)qat_alloc(batch * sizeof(int));
    for (int i = 0; i < batch; i++) {
        targets[i] = (int)(rng_next(rng) % n_classes);
    }

    float *grad_logits = (float *)qat_alloc(batch * n_classes * sizeof(float));

    float first_loss = 0.0f, last_loss = 0.0f;

    for (int step = 0; step < n_steps; step++) {
        /* Zero gradients */
        adam_zero_grad(opt);

        /* Forward */
        Tensor *logits = qat_linear_forward(layer, input);

        /* Loss */
        float loss = cross_entropy_loss(logits->data, targets,
                                         batch, n_classes, grad_logits);

        if (step == 0) first_loss = loss;
        if (step == n_steps - 1) last_loss = loss;

        if (step % 20 == 0 || step == n_steps - 1) {
            printf("  Step %3d: loss = %.4f\n", step, loss);
        }

        /* Backward */
        Tensor *grad_out = tensor_wrap(grad_logits, batch, n_classes);
        Tensor *grad_in = qat_linear_backward(layer, grad_out);
        tensor_free(grad_in);
        /* Don't free grad_out since it wraps external data */
        free(grad_out);  /* Only free the struct, not the data */

        /* Optimizer step */
        adam_step(opt);

        tensor_free(logits);
    }

    printf("  First loss: %.4f, Last loss: %.4f\n", first_loss, last_loss);

    CHECK(last_loss < first_loss, "Training convergence",
          "loss did not decrease: first=%.4f, last=%.4f", first_loss, last_loss);
    CHECK(last_loss < first_loss * 0.5f, "Training convergence",
          "loss did not decrease enough: %.4f -> %.4f", first_loss, last_loss);

    qat_free(grad_logits);
    qat_free(targets);
    tensor_free(input);
    qat_linear_free(layer);
    adam_free(opt);
    TEST_PASS("Training convergence");
}

/* ========================================================================
 * Test: GEMM benchmark
 * ======================================================================== */
static void bench_gemm(const char *name, gemm_int8_fn kernel, int M, int N, int K) {
    printf("\n--- BENCH: %s [%d x %d x %d] ---\n", name, M, N, K);

    int8_t *A = (int8_t *)qat_alloc(M * K);
    int8_t *B = (int8_t *)qat_alloc(K * N);
    int32_t *C = (int32_t *)qat_calloc(M * N * sizeof(int32_t));

    uint64_t rng[4];
    rng_seed(rng, 42);
    for (int i = 0; i < M * K; i++) A[i] = (int8_t)(rng_next(rng) % 256 - 128);
    for (int i = 0; i < K * N; i++) B[i] = (int8_t)(rng_next(rng) % 256 - 128);

    /* Warmup */
    kernel(M, N, K, A, K, B, N, C, N);

    int n_iters = 10;
    double t0 = timer_sec();
    for (int i = 0; i < n_iters; i++) {
        kernel(M, N, K, A, K, B, N, C, N);
    }
    double elapsed = timer_sec() - t0;

    double flops_per = 2.0 * M * N * K;  /* 2 ops per MAC: multiply + add */
    double total_flops = flops_per * n_iters;
    printf("  Time: %.3f ms/iter, %.2f GOPS\n",
           (elapsed / n_iters) * 1000.0,
           gflops(total_flops, elapsed));

    qat_free(A); qat_free(B); qat_free(C);
}

static void bench_gemm_fp32(const char *name, gemm_fp32_fn kernel,
                             int M, int N, int K) {
    printf("\n--- BENCH: %s [%d x %d x %d] ---\n", name, M, N, K);

    float *A = (float *)qat_alloc(M * K * sizeof(float));
    float *B = (float *)qat_alloc(K * N * sizeof(float));
    float *C = (float *)qat_calloc(M * N * sizeof(float));

    uint64_t rng[4];
    rng_seed(rng, 42);
    for (int i = 0; i < M * K; i++) A[i] = rng_uniform(rng) * 2.0f - 1.0f;
    for (int i = 0; i < K * N; i++) B[i] = rng_uniform(rng) * 2.0f - 1.0f;

    /* Warmup */
    kernel(M, N, K, 1.0f, A, K, B, N, 0.0f, C, N);

    int n_iters = 10;
    double t0 = timer_sec();
    for (int i = 0; i < n_iters; i++) {
        kernel(M, N, K, 1.0f, A, K, B, N, 0.0f, C, N);
    }
    double elapsed = timer_sec() - t0;

    double flops_per = 2.0 * M * N * K;
    double total_flops = flops_per * n_iters;
    printf("  Time: %.3f ms/iter, %.2f GFLOPS\n",
           (elapsed / n_iters) * 1000.0,
           gflops(total_flops, elapsed));

    qat_free(A); qat_free(B); qat_free(C);
}

/* ========================================================================
 * Main
 * ======================================================================== */
int main(void) {
    printf("========================================\n");
    printf("QAT-CPU Test Suite\n");
    printf("========================================\n");

    /* Detect CPU */
    CpuFeatures cpu;
    cpu_detect(&cpu);
    cpu_features_print(&cpu);

    /* Set up kernel dispatch */
    KernelDispatch kd;
    kernel_dispatch_init(&kd, &cpu);
    kernel_dispatch_print(&kd);

    /* ---- Correctness tests ---- */
    printf("\n======== CORRECTNESS TESTS ========\n");

    test_gemm_int8_scalar();

    if (cpu.has_avx2) {
        test_gemm_int8_simd("INT8 GEMM AVX2 vs scalar", gemm_int8_avx2);
        test_gemm_fp32_simd("FP32 GEMM AVX2 vs scalar", gemm_fp32_avx2);
    }

    if (cpu.has_avx512vnni) {
        test_gemm_int8_simd("INT8 GEMM VNNI vs scalar", gemm_int8_vnni);
        test_gemm_fp32_simd("FP32 GEMM AVX-512 vs scalar", gemm_fp32_avx512);
    }

    test_quantization();
    test_qat_linear_forward(&kd);
    test_gradient_check(&kd);
    test_training_convergence(&kd);

    /* ---- Benchmarks ---- */
    printf("\n======== BENCHMARKS ========\n");

    int bM = 256, bN = 256, bK = 256;

    bench_gemm("INT8 scalar", gemm_int8_scalar, bM, bN, bK);
    if (cpu.has_avx2) {
        bench_gemm("INT8 AVX2", gemm_int8_avx2, bM, bN, bK);
    }
    if (cpu.has_avx512vnni) {
        bench_gemm("INT8 VNNI", gemm_int8_vnni, bM, bN, bK);
    }

    bench_gemm_fp32("FP32 scalar", gemm_fp32_scalar, bM, bN, bK);
    if (cpu.has_avx2) {
        bench_gemm_fp32("FP32 AVX2", gemm_fp32_avx2, bM, bN, bK);
    }
    if (cpu.has_avx512f) {
        bench_gemm_fp32("FP32 AVX-512", gemm_fp32_avx512, bM, bN, bK);
    }

    /* ---- Summary ---- */
    printf("\n========================================\n");
    printf("Results: %d/%d tests passed\n", tests_passed, tests_run);
    printf("========================================\n");

    return (tests_passed == tests_run) ? 0 : 1;
}
