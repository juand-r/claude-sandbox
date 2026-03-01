/*
 * debug_qat.c - Diagnose QAT block 1 explosion
 * Manual step through block 1's forward to find where values explode.
 */

#include "qat_cpu.h"
#include <assert.h>

#define VOCAB_SIZE   128
#define DIM          512
#define N_LAYERS     2
#define N_HEADS      8
#define HIDDEN_DIM   2048
#define MAX_SEQ_LEN  128
#define SEQ_LEN      64

static void stats(const char *label, const float *data, int n) {
    float mn = data[0], mx = data[0], sum = 0, sum2 = 0;
    int n_nan = 0;
    for (int i = 0; i < n; i++) {
        float v = data[i];
        if (v != v) { n_nan++; continue; }
        if (v < mn) mn = v;
        if (v > mx) mx = v;
        sum += v;
        sum2 += v * v;
    }
    float mean = sum / n;
    float std = sqrtf(sum2 / n - mean * mean);
    printf("  %-35s min=%10.4f max=%10.4f std=%8.4f nan=%d\n",
           label, mn, mx, std, n_nan);
}

int main(void) {
    setvbuf(stdout, NULL, _IOLBF, 0);

    CpuFeatures cpu;
    cpu_detect(&cpu);
    KernelDispatch kd;
    kernel_dispatch_init(&kd, &cpu);

    uint64_t rng[4];
    rng_seed(rng, 42);

    Tensor *token_emb = tensor_create(VOCAB_SIZE, DIM);
    tensor_rand(token_emb, -0.02f, 0.02f, rng);
    Tensor *pos_emb = tensor_create(MAX_SEQ_LEN, DIM);
    tensor_rand(pos_emb, -0.02f, 0.02f, rng);

    TransformerBlock *block0 = transformer_block_create(DIM, HIDDEN_DIM, N_HEADS, &kd, rng);
    block0->attn->causal = true;
    TransformerBlock *block1 = transformer_block_create(DIM, HIDDEN_DIM, N_HEADS, &kd, rng);
    block1->attn->causal = true;

    int tokens[SEQ_LEN];
    for (int i = 0; i < SEQ_LEN; i++) {
        tokens[i] = (int)(rng_next(rng) % VOCAB_SIZE);
    }

    Tensor *x = tensor_create(SEQ_LEN, DIM);
    for (int s = 0; s < SEQ_LEN; s++) {
        for (int d = 0; d < DIM; d++) {
            x->data[s * DIM + d] =
                token_emb->data[tokens[s] * DIM + d] +
                pos_emb->data[s * DIM + d];
        }
    }
    stats("embedding:", x->data, SEQ_LEN * DIM);

    /* ---- QAT path ---- */
    printf("\n=== QAT PATH ===\n");
    Tensor *block0_out = transformer_block_forward(block0, x, SEQ_LEN);
    stats("block0 out:", block0_out->data, SEQ_LEN * DIM);

    printf("\n--- Block 1 step-through ---\n");
    Tensor *normed1 = rmsnorm_forward(block1->norm1, block0_out);
    stats("norm1:", normed1->data, SEQ_LEN * DIM);

    Tensor *q = qat_linear_forward(block1->attn->wq, normed1);
    stats("Q:", q->data, SEQ_LEN * DIM);
    Tensor *k = qat_linear_forward(block1->attn->wk, normed1);
    stats("K:", k->data, SEQ_LEN * DIM);
    Tensor *v = qat_linear_forward(block1->attn->wv, normed1);
    stats("V:", v->data, SEQ_LEN * DIM);
    tensor_free(q); tensor_free(k); tensor_free(v);

    Tensor *attn_out = attention_forward(block1->attn, normed1, SEQ_LEN);
    tensor_free(normed1);
    stats("attn out:", attn_out->data, SEQ_LEN * DIM);

    Tensor *after_attn = tensor_create(SEQ_LEN, DIM);
    for (int i = 0; i < SEQ_LEN * DIM; i++)
        after_attn->data[i] = block0_out->data[i] + attn_out->data[i];
    tensor_free(attn_out);
    stats("after_attn:", after_attn->data, SEQ_LEN * DIM);

    Tensor *normed2 = rmsnorm_forward(block1->norm2, after_attn);
    stats("norm2:", normed2->data, SEQ_LEN * DIM);

    Tensor *ffn_up_out = qat_linear_forward(block1->ffn_up, normed2);
    stats("ffn_up (pre-gelu):", ffn_up_out->data, SEQ_LEN * HIDDEN_DIM);
    tensor_free(normed2);

    gelu_forward(ffn_up_out->data, ffn_up_out->data, SEQ_LEN * HIDDEN_DIM);
    stats("ffn_up (post-gelu):", ffn_up_out->data, SEQ_LEN * HIDDEN_DIM);

    Tensor *ffn_out = qat_linear_forward(block1->ffn_down, ffn_up_out);
    tensor_free(ffn_up_out);
    stats("ffn_down:", ffn_out->data, SEQ_LEN * DIM);

    Tensor *block1_out = tensor_create(SEQ_LEN, DIM);
    for (int i = 0; i < SEQ_LEN * DIM; i++)
        block1_out->data[i] = after_attn->data[i] + ffn_out->data[i];
    tensor_free(after_attn); tensor_free(ffn_out);
    stats("block1 out:", block1_out->data, SEQ_LEN * DIM);

    /* ---- FP32 path with same weights ---- */
    printf("\n=== FP32 PATH (same weights, rewind rng) ===\n");

    /* Recreate with same rng state */
    uint64_t rng2[4];
    rng_seed(rng2, 42);
    Tensor *te2 = tensor_create(VOCAB_SIZE, DIM);
    tensor_rand(te2, -0.02f, 0.02f, rng2);
    Tensor *pe2 = tensor_create(MAX_SEQ_LEN, DIM);
    tensor_rand(pe2, -0.02f, 0.02f, rng2);

    TransformerBlock *b0f = transformer_block_create(DIM, HIDDEN_DIM, N_HEADS, &kd, rng2);
    b0f->attn->causal = true;
    TransformerBlock *b1f = transformer_block_create(DIM, HIDDEN_DIM, N_HEADS, &kd, rng2);
    b1f->attn->causal = true;

    /* Disable QAT */
    b0f->attn->wq->use_qat = false; b0f->attn->wk->use_qat = false;
    b0f->attn->wv->use_qat = false; b0f->attn->wo->use_qat = false;
    b0f->ffn_up->use_qat = false; b0f->ffn_down->use_qat = false;
    b1f->attn->wq->use_qat = false; b1f->attn->wk->use_qat = false;
    b1f->attn->wv->use_qat = false; b1f->attn->wo->use_qat = false;
    b1f->ffn_up->use_qat = false; b1f->ffn_down->use_qat = false;

    Tensor *b0f_out = transformer_block_forward(b0f, x, SEQ_LEN);
    stats("block0 fp32:", b0f_out->data, SEQ_LEN * DIM);

    Tensor *n1f = rmsnorm_forward(b1f->norm1, b0f_out);
    stats("norm1 fp32:", n1f->data, SEQ_LEN * DIM);

    Tensor *qf = qat_linear_forward(b1f->attn->wq, n1f);
    stats("Q fp32:", qf->data, SEQ_LEN * DIM);
    Tensor *kf = qat_linear_forward(b1f->attn->wk, n1f);
    stats("K fp32:", kf->data, SEQ_LEN * DIM);
    Tensor *vf = qat_linear_forward(b1f->attn->wv, n1f);
    stats("V fp32:", vf->data, SEQ_LEN * DIM);
    tensor_free(qf); tensor_free(kf); tensor_free(vf);

    Tensor *attn_f = attention_forward(b1f->attn, n1f, SEQ_LEN);
    tensor_free(n1f);
    stats("attn fp32:", attn_f->data, SEQ_LEN * DIM);

    Tensor *aa_f = tensor_create(SEQ_LEN, DIM);
    for (int i = 0; i < SEQ_LEN * DIM; i++)
        aa_f->data[i] = b0f_out->data[i] + attn_f->data[i];
    tensor_free(attn_f);
    stats("after_attn fp32:", aa_f->data, SEQ_LEN * DIM);

    Tensor *n2f = rmsnorm_forward(b1f->norm2, aa_f);
    stats("norm2 fp32:", n2f->data, SEQ_LEN * DIM);
    Tensor *up_f = qat_linear_forward(b1f->ffn_up, n2f);
    stats("ffn_up fp32 (pre-gelu):", up_f->data, SEQ_LEN * HIDDEN_DIM);
    tensor_free(n2f);
    gelu_forward(up_f->data, up_f->data, SEQ_LEN * HIDDEN_DIM);
    stats("ffn_up fp32 (post-gelu):", up_f->data, SEQ_LEN * HIDDEN_DIM);
    Tensor *down_f = qat_linear_forward(b1f->ffn_down, up_f);
    tensor_free(up_f);
    stats("ffn_down fp32:", down_f->data, SEQ_LEN * DIM);

    Tensor *b1f_out = tensor_create(SEQ_LEN, DIM);
    for (int i = 0; i < SEQ_LEN * DIM; i++)
        b1f_out->data[i] = aa_f->data[i] + down_f->data[i];
    tensor_free(aa_f); tensor_free(down_f);
    stats("block1 fp32:", b1f_out->data, SEQ_LEN * DIM);

    printf("\nDone.\n");
    return 0;
}
