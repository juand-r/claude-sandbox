/*
 * memory.c - Aligned memory allocation, tensor operations, RNG, utilities
 *
 * All allocations are 64-byte aligned for AVX-512.
 */

#include "qat_cpu.h"
#include <time.h>
#include <sys/time.h>

/* ========================================================================
 * Aligned allocation
 * ======================================================================== */

void *qat_alloc(size_t bytes) {
    if (bytes == 0) bytes = QAT_ALIGN;
    void *ptr = NULL;
    int ret = posix_memalign(&ptr, QAT_ALIGN, bytes);
    if (ret != 0) {
        fprintf(stderr, "qat_alloc: posix_memalign failed for %zu bytes\n", bytes);
        return NULL;
    }
    return ptr;
}

void qat_free(void *ptr) {
    free(ptr);
}

void *qat_calloc(size_t bytes) {
    void *ptr = qat_alloc(bytes);
    if (ptr) memset(ptr, 0, bytes);
    return ptr;
}

/* ========================================================================
 * Tensor (FP32)
 * ======================================================================== */

Tensor *tensor_create(int rows, int cols) {
    Tensor *t = (Tensor *)malloc(sizeof(Tensor));
    if (!t) return NULL;
    t->rows = rows;
    t->cols = cols;
    t->owns_data = true;
    t->data = (float *)qat_alloc((size_t)rows * cols * sizeof(float));
    if (!t->data) {
        free(t);
        return NULL;
    }
    return t;
}

Tensor *tensor_zeros(int rows, int cols) {
    Tensor *t = tensor_create(rows, cols);
    if (t) memset(t->data, 0, (size_t)rows * cols * sizeof(float));
    return t;
}

Tensor *tensor_wrap(float *data, int rows, int cols) {
    Tensor *t = (Tensor *)malloc(sizeof(Tensor));
    if (!t) return NULL;
    t->data = data;
    t->rows = rows;
    t->cols = cols;
    t->owns_data = false;
    return t;
}

void tensor_free(Tensor *t) {
    if (!t) return;
    if (t->owns_data && t->data) qat_free(t->data);
    free(t);
}

void tensor_fill(Tensor *t, float val) {
    int n = t->rows * t->cols;
    for (int i = 0; i < n; i++) {
        t->data[i] = val;
    }
}

void tensor_rand(Tensor *t, float lo, float hi, uint64_t *rng_state) {
    int n = t->rows * t->cols;
    float range = hi - lo;
    for (int i = 0; i < n; i++) {
        t->data[i] = lo + range * rng_uniform(rng_state);
    }
}

void tensor_print(const Tensor *t, const char *name) {
    printf("%s [%d x %d]:\n", name, t->rows, t->cols);
    int max_rows = t->rows < 6 ? t->rows : 6;
    int max_cols = t->cols < 8 ? t->cols : 8;
    for (int i = 0; i < max_rows; i++) {
        printf("  [");
        for (int j = 0; j < max_cols; j++) {
            printf("%8.4f", t->data[i * t->cols + j]);
            if (j < max_cols - 1) printf(", ");
        }
        if (t->cols > max_cols) printf(", ...");
        printf("]\n");
    }
    if (t->rows > max_rows) printf("  ...\n");
}

void tensor_copy(Tensor *dst, const Tensor *src) {
    memcpy(dst->data, src->data, (size_t)src->rows * src->cols * sizeof(float));
}

/* ========================================================================
 * Transpose (row-major -> row-major)
 * dst[j * rows + i] = src[i * cols + j]
 * src: [rows x cols], dst: [cols x rows]
 * ======================================================================== */

void transpose_fp32(const float *src, int rows, int cols, float *dst) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            dst[j * rows + i] = src[i * cols + j];
        }
    }
}

/* ========================================================================
 * INT8 Tensor
 * ======================================================================== */

TensorI8 *tensor_i8_create(int rows, int cols) {
    TensorI8 *t = (TensorI8 *)malloc(sizeof(TensorI8));
    if (!t) return NULL;
    t->rows = rows;
    t->cols = cols;
    t->owns_data = true;
    t->data = (int8_t *)qat_alloc((size_t)rows * cols);
    if (!t->data) {
        free(t);
        return NULL;
    }
    return t;
}

void tensor_i8_free(TensorI8 *t) {
    if (!t) return;
    if (t->owns_data && t->data) qat_free(t->data);
    free(t);
}

/* ========================================================================
 * INT32 Tensor
 * ======================================================================== */

TensorI32 *tensor_i32_create(int rows, int cols) {
    TensorI32 *t = (TensorI32 *)malloc(sizeof(TensorI32));
    if (!t) return NULL;
    t->rows = rows;
    t->cols = cols;
    t->owns_data = true;
    t->data = (int32_t *)qat_alloc((size_t)rows * cols * sizeof(int32_t));
    if (!t->data) {
        free(t);
        return NULL;
    }
    return t;
}

void tensor_i32_free(TensorI32 *t) {
    if (!t) return;
    if (t->owns_data && t->data) qat_free(t->data);
    free(t);
}

/* ========================================================================
 * RNG: xoshiro256**
 * ======================================================================== */

static uint64_t splitmix64(uint64_t *state) {
    uint64_t z = (*state += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

void rng_seed(uint64_t *state, uint64_t seed) {
    /* state must be 4 uint64_t's (256 bits) */
    uint64_t sm = seed;
    state[0] = splitmix64(&sm);
    state[1] = splitmix64(&sm);
    state[2] = splitmix64(&sm);
    state[3] = splitmix64(&sm);
}

static inline uint64_t rotl(uint64_t x, int k) {
    return (x << k) | (x >> (64 - k));
}

uint64_t rng_next(uint64_t *s) {
    /* xoshiro256** */
    uint64_t result = rotl(s[1] * 5, 7) * 9;
    uint64_t t = s[1] << 17;
    s[2] ^= s[0];
    s[3] ^= s[1];
    s[1] ^= s[2];
    s[0] ^= s[3];
    s[2] ^= t;
    s[3] = rotl(s[3], 45);
    return result;
}

float rng_uniform(uint64_t *state) {
    /* Generate float in [0, 1) */
    uint64_t x = rng_next(state);
    return (float)(x >> 40) * 0x1.0p-24f;
}

float rng_normal(uint64_t *state) {
    /* Box-Muller transform */
    float u1 = rng_uniform(state);
    float u2 = rng_uniform(state);
    /* Avoid log(0) */
    if (u1 < 1e-10f) u1 = 1e-10f;
    return sqrtf(-2.0f * logf(u1)) * cosf(2.0f * (float)M_PI * u2);
}

/* ========================================================================
 * Utility / Debug
 * ======================================================================== */

float max_abs_diff(const float *a, const float *b, int n) {
    float max_d = 0.0f;
    for (int i = 0; i < n; i++) {
        float d = fabsf(a[i] - b[i]);
        if (d > max_d) max_d = d;
    }
    return max_d;
}

float max_rel_error(const float *a, const float *b, int n) {
    float max_e = 0.0f;
    for (int i = 0; i < n; i++) {
        float denom = fmaxf(fabsf(a[i]), fabsf(b[i]));
        denom = fmaxf(denom, 1e-8f);
        float e = fabsf(a[i] - b[i]) / denom;
        if (e > max_e) max_e = e;
    }
    return max_e;
}

double timer_sec(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec * 1e-6;
}
