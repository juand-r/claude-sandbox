/*
 * qat_cpu.h - QAT-CPU: Quantized LLM Training on CPU via SIMD Kernels
 *
 * Main header. All types, API declarations, inline helpers.
 * No external dependencies beyond libc and x86 intrinsics.
 */

#ifndef QAT_CPU_H
#define QAT_CPU_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <float.h>

/* ========================================================================
 * Constants
 * ======================================================================== */

#define QAT_ALIGN       64      /* AVX-512 cache line alignment */
#define QAT_INT8_MAX    127
#define QAT_INT8_MIN    (-128)
#define QAT_UINT8_OFFSET 128    /* For signed->unsigned conversion trick */

/* ========================================================================
 * CPU Feature Detection
 * ======================================================================== */

typedef struct {
    bool has_sse42;
    bool has_avx2;
    bool has_fma;
    bool has_avx512f;
    bool has_avx512bw;
    bool has_avx512vnni;
    bool has_avx512bf16;
    bool has_amx_tile;
    bool has_amx_int8;
    bool has_amx_bf16;
    char brand_string[64];
    int  num_cores;
} CpuFeatures;

/* Detect CPU features via CPUID. Call once at startup. */
void cpu_detect(CpuFeatures *features);

/* Print detected features to stdout. */
void cpu_features_print(const CpuFeatures *features);

/* ========================================================================
 * Memory Allocation
 * ======================================================================== */

/* Allocate 64-byte aligned memory. Returns NULL on failure. */
void *qat_alloc(size_t bytes);

/* Free aligned memory. */
void qat_free(void *ptr);

/* Allocate and zero-initialize. */
void *qat_calloc(size_t bytes);

/* ========================================================================
 * Tensor (simple 2D matrix)
 *
 * All tensors are row-major: data[row * cols + col]
 * Always 64-byte aligned.
 * ======================================================================== */

typedef struct {
    float *data;
    int    rows;
    int    cols;
    bool   owns_data;  /* If true, free data on tensor_free */
} Tensor;

/* Create a tensor (uninitialized data). */
Tensor *tensor_create(int rows, int cols);

/* Create a tensor initialized to zero. */
Tensor *tensor_zeros(int rows, int cols);

/* Create a tensor wrapping existing data (does not own). */
Tensor *tensor_wrap(float *data, int rows, int cols);

/* Free tensor. Frees data if owns_data is true. */
void tensor_free(Tensor *t);

/* Fill tensor with a constant value. */
void tensor_fill(Tensor *t, float val);

/* Fill tensor with random values in [lo, hi). */
void tensor_rand(Tensor *t, float lo, float hi, uint64_t *rng_state);

/* Print tensor to stdout (truncated for large tensors). */
void tensor_print(const Tensor *t, const char *name);

/* Copy tensor data: dst = src. Must have same shape. */
void tensor_copy(Tensor *dst, const Tensor *src);

/* Transpose FP32 matrix: dst[j*rows+i] = src[i*cols+j].
 * src: [rows x cols], dst: [cols x rows]. Must not alias. */
void transpose_fp32(const float *src, int rows, int cols, float *dst);

/* Number of elements. */
static inline int tensor_numel(const Tensor *t) {
    return t->rows * t->cols;
}

/* Size in bytes. */
static inline size_t tensor_bytes(const Tensor *t) {
    return (size_t)t->rows * t->cols * sizeof(float);
}

/* ========================================================================
 * INT8 Tensor (for quantized weights/activations)
 * ======================================================================== */

typedef struct {
    int8_t *data;
    int     rows;
    int     cols;
    bool    owns_data;
} TensorI8;

TensorI8 *tensor_i8_create(int rows, int cols);
void      tensor_i8_free(TensorI8 *t);

/* INT32 accumulator tensor (output of INT8 GEMM). */
typedef struct {
    int32_t *data;
    int      rows;
    int      cols;
    bool     owns_data;
} TensorI32;

TensorI32 *tensor_i32_create(int rows, int cols);
void       tensor_i32_free(TensorI32 *t);

/* ========================================================================
 * GEMM Kernel Function Pointer Types
 *
 * INT8 GEMM: C_int32[M,N] = A_int8[M,K] * B_int8[K,N]
 *   A is row-major [M x K], B is row-major [K x N]
 *   C is row-major [M x N], accumulated into int32
 *
 * FP32 GEMM: C[M,N] = A[M,K] * B[K,N]
 *   All row-major.
 *
 * For both: lda/ldb/ldc are leading dimensions (= number of columns).
 * ======================================================================== */

/* INT8 GEMM: C_i32[M,N] += A_i8[M,K] * B_i8[K,N] */
typedef void (*gemm_int8_fn)(
    int M, int N, int K,
    const int8_t *A, int lda,
    const int8_t *B, int ldb,
    int32_t *C, int ldc
);

/* FP32 GEMM: C[M,N] += alpha * A[M,K] * B[K,N] + beta * C[M,N] */
typedef void (*gemm_fp32_fn)(
    int M, int N, int K,
    float alpha,
    const float *A, int lda,
    const float *B, int ldb,
    float beta,
    float *C, int ldc
);

/* ========================================================================
 * Kernel Dispatch Table
 *
 * Populated at startup based on detected CPU features.
 * All code uses these function pointers for GEMM operations.
 * ======================================================================== */

typedef struct {
    gemm_int8_fn  int8_gemm;
    gemm_fp32_fn  fp32_gemm;
    const char   *int8_name;   /* e.g., "AVX-512 VNNI" */
    const char   *fp32_name;   /* e.g., "AVX-512" */
} KernelDispatch;

/* Initialize kernel dispatch based on CPU features. */
void kernel_dispatch_init(KernelDispatch *kd, const CpuFeatures *cpu);

/* Print which kernels were selected. */
void kernel_dispatch_print(const KernelDispatch *kd);

/* ========================================================================
 * GEMM Kernel Implementations
 * ======================================================================== */

/* --- Scalar reference (works everywhere) --- */
void gemm_int8_scalar(int M, int N, int K,
                      const int8_t *A, int lda,
                      const int8_t *B, int ldb,
                      int32_t *C, int ldc);

void gemm_fp32_scalar(int M, int N, int K,
                      float alpha,
                      const float *A, int lda,
                      const float *B, int ldb,
                      float beta,
                      float *C, int ldc);

/* --- AVX2 (Haswell+) --- */
void gemm_int8_avx2(int M, int N, int K,
                    const int8_t *A, int lda,
                    const int8_t *B, int ldb,
                    int32_t *C, int ldc);

void gemm_fp32_avx2(int M, int N, int K,
                    float alpha,
                    const float *A, int lda,
                    const float *B, int ldb,
                    float beta,
                    float *C, int ldc);

/* --- AVX-512 VNNI (Ice Lake+) --- */
void gemm_int8_vnni(int M, int N, int K,
                    const int8_t *A, int lda,
                    const int8_t *B, int ldb,
                    int32_t *C, int ldc);

void gemm_fp32_avx512(int M, int N, int K,
                      float alpha,
                      const float *A, int lda,
                      const float *B, int ldb,
                      float beta,
                      float *C, int ldc);

/* ========================================================================
 * Quantization
 * ======================================================================== */

/*
 * Per-channel symmetric quantization (for weights).
 * Quantizes each row independently:
 *   scale[i] = absmax(src[i,:]) / 127.0
 *   dst[i,j] = round(src[i,j] / scale[i])
 *
 * src: [rows x cols] FP32, dst: [rows x cols] INT8, scales: [rows]
 */
void quantize_per_channel(const float *src, int rows, int cols,
                          int8_t *dst, float *scales);

/*
 * Per-token symmetric quantization (for activations).
 * Same math as per-channel but over rows of activations.
 */
void quantize_per_token(const float *src, int rows, int cols,
                        int8_t *dst, float *scales);

/*
 * Dequantize INT32 accumulator to FP32.
 * out[i][j] = acc[i][j] * scale_act[i] * scale_wt[j]
 */
void dequantize_int32(const int32_t *acc, int rows, int cols,
                      const float *scale_act, const float *scale_wt,
                      float *out);

/*
 * Per-column symmetric quantization.
 * scale[j] = absmax(src[:, j]) / 127.0
 * dst[i][j] = clamp(round(src[i][j] / scale[j]), -128, 127)
 * scales: [cols]
 */
void quantize_per_column(const float *src, int rows, int cols,
                          int8_t *dst, float *scales);
/* Explicit scalar/AVX-512 variants for testing */
void quantize_per_column_scalar(const float *src, int rows, int cols,
                                 int8_t *dst, float *scales);
void quantize_per_column_avx512(const float *src, int rows, int cols,
                                  int8_t *dst, float *scales);

/*
 * Dequantize INT32 accumulator to FP32, accumulating (+=) into existing output.
 * out[i][j] += acc[i][j] * scale_act[i] * scale_wt[j]
 */
void dequantize_int32_acc(const int32_t *acc, int rows, int cols,
                           const float *scale_act, const float *scale_wt,
                           float *out);

/*
 * Add bias after dequantization: out[i][j] += bias[j]
 */
void add_bias(float *out, int rows, int cols, const float *bias);

/*
 * Fake quantization: quantize then immediately dequantize in FP32.
 * Used for layers that need to "see" quantization noise but stay in FP32.
 * out[i][j] = dequant(quant(src[i][j]))
 */
void fake_quantize_per_channel(const float *src, int rows, int cols,
                               float *out);

/* ========================================================================
 * QAT Linear Layer
 *
 * Forward: quantize weights+input -> INT8 GEMM -> dequantize -> add bias
 * Backward: FP32 GEMM with STE (uses FP32 master weights directly)
 *
 * Weight shape: [out_features x in_features] (row-major)
 * Input shape:  [batch x in_features]
 * Output shape: [batch x out_features]
 * ======================================================================== */

typedef struct {
    int in_features;
    int out_features;

    /* FP32 master weights and bias */
    Tensor *weight;          /* [out_features x in_features] */
    Tensor *bias;            /* [1 x out_features] or NULL */

    /* Gradients */
    Tensor *grad_weight;     /* [out_features x in_features] */
    Tensor *grad_bias;       /* [1 x out_features] or NULL */

    /* Quantized workspace (reused each forward pass) */
    TensorI8 *weight_q;     /* [out_features x in_features] INT8 */
    float    *weight_scales; /* [out_features] per-channel scales */

    /* Pre-allocated workspace to avoid per-call malloc/free */
    TensorI8  *weight_q_t;  /* [in_features x out_features] transposed INT8 */
    float     *weight_fp32_t; /* [in_features x out_features] transposed FP32 */

    /* Saved for backward pass */
    Tensor *saved_input;     /* [batch x in_features] from last forward */

    /* INT8 backward workspace.
     * GEMM 1 (grad_input): needs weight quantized per-column (per in_features).
     * GEMM 2 (grad_weight): needs saved_input quantized per-column (per in_features).
     */
    TensorI8 *weight_q_col;        /* [out_f x in_f] INT8, per-column quantized */
    float    *weight_col_scales;   /* [in_f] per-column scales */

    TensorI8 *saved_input_q;       /* [batch x in_f] INT8, per-column quantized */
    float    *saved_input_col_scales; /* [in_f] per-column scales */
    int       saved_input_batch;   /* batch size from last forward */

    /* Kernel dispatch (pointer to global dispatch table) */
    const KernelDispatch *kernels;

    /* If true, use INT8 quantized forward. If false, pure FP32 forward. */
    bool use_qat;

    /* If true, use INT8 GEMMs in backward pass too. */
    bool use_int8_backward;

    /* Weight cache: skip re-quantization when weights haven't changed.
     * Set to true by optimizer step, cleared after first quantize. */
    bool weights_dirty;
} QATLinear;

/* Create a QAT linear layer. Weights initialized with Kaiming uniform. */
QATLinear *qat_linear_create(int in_features, int out_features,
                             bool use_bias, const KernelDispatch *kd,
                             uint64_t *rng_state);

/* Free layer and all owned memory. */
void qat_linear_free(QATLinear *layer);

/*
 * Forward pass:
 *   1. Quantize weights to INT8 (per-channel)
 *   2. Quantize input to INT8 (per-token)
 *   3. INT8 GEMM -> INT32 accumulator
 *   4. Dequantize to FP32
 *   5. Add bias
 *   Returns output tensor [batch x out_features]. Caller must free.
 */
Tensor *qat_linear_forward(QATLinear *layer, const Tensor *input);

/*
 * Backward pass (STE):
 *   Given grad_output [batch x out_features]:
 *   1. grad_input  = grad_output * W_fp32^T    [batch x in_features]
 *   2. grad_weight = grad_output^T * saved_input [out_features x in_features]
 *   3. grad_bias   = sum(grad_output, dim=0)    [1 x out_features]
 *   Accumulates into layer->grad_weight, layer->grad_bias.
 *   Returns grad_input tensor. Caller must free.
 */
Tensor *qat_linear_backward(QATLinear *layer, const Tensor *grad_output);

/* Zero out accumulated gradients. */
void qat_linear_zero_grad(QATLinear *layer);

/* ========================================================================
 * RMSNorm Layer
 *
 * y = x * weight / rms(x)
 * rms(x) = sqrt(mean(x^2) + eps)
 * ======================================================================== */

typedef struct {
    int dim;
    Tensor *weight;          /* [1 x dim] */
    Tensor *grad_weight;     /* [1 x dim] */
    float eps;

    /* Saved for backward */
    Tensor *saved_input;
    float  *saved_rms;       /* [batch] */
} RMSNorm;

RMSNorm *rmsnorm_create(int dim, float eps);
void     rmsnorm_free(RMSNorm *layer);
Tensor  *rmsnorm_forward(RMSNorm *layer, const Tensor *input);
Tensor  *rmsnorm_backward(RMSNorm *layer, const Tensor *grad_output);
void     rmsnorm_zero_grad(RMSNorm *layer);

/* ========================================================================
 * Activation Functions (element-wise, FP32)
 * ======================================================================== */

/* GeLU forward: out = x * 0.5 * (1 + erf(x / sqrt(2)))
 * Uses tanh approximation for speed. */
void gelu_forward(const float *input, float *output, int n);
void gelu_backward(const float *input, const float *grad_output,
                   float *grad_input, int n);

/* SiLU forward: out = x * sigmoid(x) */
void silu_forward(const float *input, float *output, int n);
void silu_backward(const float *input, const float *grad_output,
                   float *grad_input, int n);

/* ========================================================================
 * Softmax (numerically stable)
 * ======================================================================== */

/* Softmax over last dimension.
 * input/output: [rows x cols], softmax applied per-row. */
void softmax_forward(const float *input, float *output, int rows, int cols);

/* Backward: given grad_output and forward output (softmax probs). */
void softmax_backward(const float *output, const float *grad_output,
                      float *grad_input, int rows, int cols);

/* ========================================================================
 * Attention Block
 *
 * Multi-head attention with QATLinear for Q/K/V/O projections.
 * Attention scores in FP32.
 * ======================================================================== */

typedef struct {
    int dim;
    int n_heads;
    int head_dim;

    QATLinear *wq;       /* [dim x dim] */
    QATLinear *wk;       /* [dim x dim] */
    QATLinear *wv;       /* [dim x dim] */
    QATLinear *wo;       /* [dim x dim] */

    /* Saved for backward */
    Tensor *saved_q;     /* [batch x dim] */
    Tensor *saved_k;     /* [batch x dim] */
    Tensor *saved_v;     /* [batch x dim] */
    Tensor *saved_attn;  /* [batch*n_heads x seq_len] attention weights */

    /* Kernel dispatch for GEMM calls in attention score/value computation */
    const KernelDispatch *kernels;

    bool causal;         /* If true, apply causal mask (lower-triangular) */
} Attention;

Attention *attention_create(int dim, int n_heads,
                            const KernelDispatch *kd, uint64_t *rng_state);
void       attention_free(Attention *attn);
Tensor    *attention_forward(Attention *attn, const Tensor *input,
                             int batch_size, int seq_len);
Tensor    *attention_backward(Attention *attn, const Tensor *grad_output,
                              int batch_size, int seq_len);
void       attention_zero_grad(Attention *attn);

/* ========================================================================
 * Transformer Block
 *
 * input -> RMSNorm -> Attention -> residual add
 *       -> RMSNorm -> FFN -> residual add
 *
 * FFN variants:
 *   GeLU:   up_proj -> GeLU -> down_proj
 *   SwiGLU: (SiLU(gate_proj) * up_proj) -> down_proj
 * ======================================================================== */

typedef struct {
    int dim;
    int hidden_dim;   /* FFN hidden dimension, typically 4*dim */
    int n_heads;
    bool use_swiglu;  /* If true, use SwiGLU FFN instead of GeLU */

    RMSNorm   *norm1;
    Attention *attn;
    RMSNorm   *norm2;
    QATLinear *ffn_up;     /* [dim -> hidden_dim] */
    QATLinear *ffn_gate;   /* [dim -> hidden_dim] (SwiGLU only, NULL otherwise) */
    QATLinear *ffn_down;   /* [hidden_dim -> dim] */

    /* Saved for backward */
    Tensor *saved_residual1;
    Tensor *saved_normed1;
    Tensor *saved_residual2;
    Tensor *saved_normed2;
    Tensor *saved_ffn_hidden;  /* Pre-activation (GeLU) or gate output (SwiGLU) */
    Tensor *saved_ffn_up;      /* SwiGLU only: up_proj output before gating */
} TransformerBlock;

TransformerBlock *transformer_block_create(int dim, int hidden_dim, int n_heads,
                                           bool use_swiglu,
                                           const KernelDispatch *kd,
                                           uint64_t *rng_state);
void              transformer_block_free(TransformerBlock *block);
Tensor           *transformer_block_forward(TransformerBlock *block,
                                            const Tensor *input,
                                            int batch_size, int seq_len);
Tensor           *transformer_block_backward(TransformerBlock *block,
                                             const Tensor *grad_output,
                                             int batch_size, int seq_len);
void              transformer_block_zero_grad(TransformerBlock *block);

/* ========================================================================
 * Adam Optimizer
 * ======================================================================== */

typedef struct {
    float lr;
    float beta1;
    float beta2;
    float eps;
    float weight_decay;
    int   step;         /* Current timestep (for bias correction) */
} AdamConfig;

/* A single parameter group tracked by Adam. */
typedef struct {
    float *param;       /* Pointer to parameter data */
    float *grad;        /* Pointer to gradient data */
    float *m;           /* First moment (allocated by optimizer) */
    float *v;           /* Second moment (allocated by optimizer) */
    int    numel;       /* Number of elements */
} AdamParam;

typedef struct {
    AdamConfig  config;
    AdamParam  *params;
    int         n_params;
    int         capacity;
} Adam;

Adam *adam_create(float lr, float beta1, float beta2, float eps,
                 float weight_decay);
void  adam_free(Adam *opt);

/* Register a parameter with the optimizer. */
void adam_add_param(Adam *opt, float *param, float *grad, int numel);

/* Perform one optimization step (updates all registered parameters). */
void adam_step(Adam *opt);

/* Zero all gradients for registered parameters. */
void adam_zero_grad(Adam *opt);

/* ========================================================================
 * Loss Functions
 * ======================================================================== */

/*
 * Cross-entropy loss.
 * logits: [batch x vocab_size] (raw, pre-softmax)
 * targets: [batch] (integer class labels)
 * Returns mean loss over batch.
 * grad_logits: [batch x vocab_size] output gradient (softmax(logits) - one_hot)
 */
float cross_entropy_loss(const float *logits, const int *targets,
                         int batch, int vocab_size,
                         float *grad_logits);

/* ========================================================================
 * RNG (xoshiro256** for fast, reproducible random numbers)
 * ======================================================================== */

/* Initialize RNG state from a seed. */
void rng_seed(uint64_t *state, uint64_t seed);

/* Generate a random uint64. */
uint64_t rng_next(uint64_t *state);

/* Generate a random float in [0, 1). */
float rng_uniform(uint64_t *state);

/* Generate a random float from standard normal (Box-Muller). */
float rng_normal(uint64_t *state);

/* ========================================================================
 * Utility / Debug
 * ======================================================================== */

/* Compute max absolute difference between two float arrays. */
float max_abs_diff(const float *a, const float *b, int n);

/* Compute relative error: max(|a-b|) / max(|a|, |b|, eps). */
float max_rel_error(const float *a, const float *b, int n);

/* Simple timer (returns wall-clock seconds). */
double timer_sec(void);

/* Compute GFLOPS given flop count and elapsed seconds. */
static inline double gflops(double flops, double seconds) {
    return flops / (seconds * 1e9);
}

#endif /* QAT_CPU_H */
