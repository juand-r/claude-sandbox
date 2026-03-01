/*
 * profile_qat.c - Per-component timing of FP32 vs QAT vs QAT+INT8bwd
 *
 * Manually unrolls transformer_block_forward/backward so we can time
 * each component (QATLinear fwd/bwd, attention, RMSNorm, GeLU, etc.).
 *
 * Uses the built-in attention_forward/backward (with OMP outer loop)
 * rather than re-implementing per-head loops.
 *
 * Three modes compared:
 *   1. FP32: pure FP32 forward + backward
 *   2. QAT:  INT8 forward, FP32 backward (STE)
 *   3. QAT+INT8bwd: INT8 forward + INT8 backward
 *
 * Config: 4 layers, batch=8, seq=64, dim=1024, 16 heads, hidden=4096.
 * Runs N_WARMUP warmup + N_PROFILE profiled steps, reports ms/step for each.
 */

#include "qat_cpu.h"
#include <assert.h>

#define VOCAB_SIZE   128
#define DIM          1024
#define N_LAYERS     4
#define N_HEADS      16
#define HIDDEN_DIM   4096
#define MAX_SEQ_LEN  256
#define SEQ_LEN      64
#define BATCH_SIZE   8
#define LR           3e-4f
#define WEIGHT_DECAY 0.01f

#define N_WARMUP     3
#define N_PROFILE    20

/* Timing accumulators (seconds) */
static double t_qatlin_fwd;      /* QATLinear forward (quantize + INT8 GEMM + dequant) */
static double t_qatlin_bwd;      /* QATLinear backward (FP32 GEMM + transpose) */
static double t_attn_fwd;        /* Attention forward (scores + softmax + values) */
static double t_attn_bwd;        /* Attention backward (OMP outer loop) */
static double t_rmsnorm;         /* RMSNorm forward + backward */
static double t_gelu;            /* GeLU forward + backward */
static double t_residual;        /* Residual adds + tensor copies */
static double t_optimizer;       /* Adam step */
static double t_loss;            /* Cross-entropy loss */
static double t_embedding;       /* Embedding lookup + grad scatter */

static void reset_timers(void) {
    t_qatlin_fwd = t_qatlin_bwd = 0;
    t_attn_fwd = t_attn_bwd = 0;
    t_rmsnorm = t_gelu = t_residual = 0;
    t_optimizer = t_loss = t_embedding = 0;
}

/* Timed wrappers for leaf operations */
static Tensor *timed_qatlin_fwd(QATLinear *l, const Tensor *in) {
    double t0 = timer_sec();
    Tensor *out = qat_linear_forward(l, in);
    t_qatlin_fwd += timer_sec() - t0;
    return out;
}

static Tensor *timed_qatlin_bwd(QATLinear *l, const Tensor *g) {
    double t0 = timer_sec();
    Tensor *out = qat_linear_backward(l, g);
    t_qatlin_bwd += timer_sec() - t0;
    return out;
}

static Tensor *timed_rmsnorm_fwd(RMSNorm *l, const Tensor *in) {
    double t0 = timer_sec();
    Tensor *out = rmsnorm_forward(l, in);
    t_rmsnorm += timer_sec() - t0;
    return out;
}

static Tensor *timed_rmsnorm_bwd(RMSNorm *l, const Tensor *g) {
    double t0 = timer_sec();
    Tensor *out = rmsnorm_backward(l, g);
    t_rmsnorm += timer_sec() - t0;
    return out;
}

/*
 * Timed transformer block forward.
 *
 * Manually unrolls the block to time each component, but uses the
 * built-in attention_forward for the attention sub-block (so the OMP
 * outer loop is exercised exactly as in training).
 */
static Tensor *timed_block_forward(TransformerBlock *block, const Tensor *input,
                                    int batch_size, int seq_len) {
    double t0;
    int dim = block->dim;
    int hidden_dim = block->hidden_dim;
    int total_tokens = batch_size * seq_len;

    /* Save residual 1 */
    t0 = timer_sec();
    if (block->saved_residual1) tensor_free(block->saved_residual1);
    block->saved_residual1 = tensor_create(total_tokens, dim);
    tensor_copy(block->saved_residual1, input);
    t_residual += timer_sec() - t0;

    /* RMSNorm 1 */
    Tensor *normed1 = timed_rmsnorm_fwd(block->norm1, input);

    /* Save normed1 */
    t0 = timer_sec();
    if (block->saved_normed1) tensor_free(block->saved_normed1);
    block->saved_normed1 = tensor_create(total_tokens, dim);
    tensor_copy(block->saved_normed1, normed1);
    t_residual += timer_sec() - t0;

    /* Attention forward (uses built-in with OMP) */
    t0 = timer_sec();
    Tensor *attn_out = attention_forward(block->attn, normed1, batch_size, seq_len);
    t_attn_fwd += timer_sec() - t0;
    tensor_free(normed1);

    /* Residual add + save residual 2 */
    t0 = timer_sec();
    Tensor *after_attn = tensor_create(total_tokens, dim);
    for (int i = 0; i < total_tokens * dim; i++)
        after_attn->data[i] = input->data[i] + attn_out->data[i];
    tensor_free(attn_out);
    if (block->saved_residual2) tensor_free(block->saved_residual2);
    block->saved_residual2 = tensor_create(total_tokens, dim);
    tensor_copy(block->saved_residual2, after_attn);
    t_residual += timer_sec() - t0;

    /* RMSNorm 2 */
    Tensor *normed2 = timed_rmsnorm_fwd(block->norm2, after_attn);

    /* Save normed2 */
    t0 = timer_sec();
    if (block->saved_normed2) tensor_free(block->saved_normed2);
    block->saved_normed2 = tensor_create(total_tokens, dim);
    tensor_copy(block->saved_normed2, normed2);
    t_residual += timer_sec() - t0;

    /* FFN up */
    Tensor *ffn_up = timed_qatlin_fwd(block->ffn_up, normed2);
    tensor_free(normed2);

    /* Save FFN hidden */
    t0 = timer_sec();
    if (block->saved_ffn_hidden) tensor_free(block->saved_ffn_hidden);
    block->saved_ffn_hidden = tensor_create(total_tokens, hidden_dim);
    tensor_copy(block->saved_ffn_hidden, ffn_up);
    t_residual += timer_sec() - t0;

    /* GeLU */
    t0 = timer_sec();
    gelu_forward(ffn_up->data, ffn_up->data, total_tokens * hidden_dim);
    t_gelu += timer_sec() - t0;

    /* FFN down */
    Tensor *ffn_out = timed_qatlin_fwd(block->ffn_down, ffn_up);
    tensor_free(ffn_up);

    /* Residual add 2 */
    t0 = timer_sec();
    Tensor *output = tensor_create(total_tokens, dim);
    for (int i = 0; i < total_tokens * dim; i++)
        output->data[i] = after_attn->data[i] + ffn_out->data[i];
    tensor_free(after_attn); tensor_free(ffn_out);
    t_residual += timer_sec() - t0;

    return output;
}

/*
 * Timed transformer block backward.
 *
 * Uses the built-in attention_backward (with OMP outer loop).
 * QATLinear backward calls are timed separately.
 */
static Tensor *timed_block_backward(TransformerBlock *block, const Tensor *grad_output,
                                     int batch_size, int seq_len) {
    double t0;
    int dim = block->dim;
    int hidden_dim = block->hidden_dim;
    int total_tokens = batch_size * seq_len;

    /* FFN down backward */
    Tensor *grad_ffn_act = timed_qatlin_bwd(block->ffn_down, grad_output);

    /* GeLU backward */
    t0 = timer_sec();
    Tensor *grad_ffn_up = tensor_create(total_tokens, hidden_dim);
    gelu_backward(block->saved_ffn_hidden->data, grad_ffn_act->data,
                  grad_ffn_up->data, total_tokens * hidden_dim);
    t_gelu += timer_sec() - t0;
    tensor_free(grad_ffn_act);

    /* FFN up backward */
    Tensor *grad_normed2 = timed_qatlin_bwd(block->ffn_up, grad_ffn_up);
    tensor_free(grad_ffn_up);

    /* RMSNorm 2 backward */
    Tensor *grad_after_attn = timed_rmsnorm_bwd(block->norm2, grad_normed2);
    tensor_free(grad_normed2);

    /* Residual connection */
    t0 = timer_sec();
    for (int i = 0; i < total_tokens * dim; i++)
        grad_after_attn->data[i] += grad_output->data[i];
    t_residual += timer_sec() - t0;

    /* Attention backward (built-in with OMP outer loop) */
    t0 = timer_sec();
    Tensor *grad_normed1 = attention_backward(block->attn, grad_after_attn,
                                               batch_size, seq_len);
    t_attn_bwd += timer_sec() - t0;

    /* RMSNorm 1 backward */
    Tensor *grad_input = timed_rmsnorm_bwd(block->norm1, grad_normed1);
    tensor_free(grad_normed1);

    /* Residual connection */
    t0 = timer_sec();
    for (int i = 0; i < total_tokens * dim; i++)
        grad_input->data[i] += grad_after_attn->data[i];
    tensor_free(grad_after_attn);
    t_residual += timer_sec() - t0;

    return grad_input;
}

/* ---- Minimal GPT model (mirrors train.c) ---- */

typedef struct {
    int vocab_size, dim, n_layers, n_heads, hidden_dim, max_seq_len;
    Tensor *token_emb, *pos_emb, *grad_token_emb, *grad_pos_emb;
    TransformerBlock **blocks;
    RMSNorm *final_norm;
    QATLinear *output_head;
    const KernelDispatch *kernels;
    int *saved_tokens;
    int saved_batch_size;
    int saved_seq_len;
    Tensor *saved_embed;
} ProfileGPT;

static ProfileGPT *pgpt_create(const KernelDispatch *kd, uint64_t *rng) {
    ProfileGPT *m = (ProfileGPT *)calloc(1, sizeof(ProfileGPT));
    m->vocab_size = VOCAB_SIZE; m->dim = DIM; m->n_layers = N_LAYERS;
    m->n_heads = N_HEADS; m->hidden_dim = HIDDEN_DIM;
    m->max_seq_len = MAX_SEQ_LEN; m->kernels = kd;
    m->token_emb = tensor_create(VOCAB_SIZE, DIM);
    tensor_rand(m->token_emb, -0.02f, 0.02f, rng);
    m->pos_emb = tensor_create(MAX_SEQ_LEN, DIM);
    tensor_rand(m->pos_emb, -0.02f, 0.02f, rng);
    m->grad_token_emb = tensor_zeros(VOCAB_SIZE, DIM);
    m->grad_pos_emb = tensor_zeros(MAX_SEQ_LEN, DIM);
    m->blocks = (TransformerBlock **)calloc(N_LAYERS, sizeof(TransformerBlock *));
    for (int i = 0; i < N_LAYERS; i++) {
        m->blocks[i] = transformer_block_create(DIM, HIDDEN_DIM, N_HEADS, false, kd, rng);
        m->blocks[i]->attn->causal = true;
    }
    m->final_norm = rmsnorm_create(DIM, 1e-5f);
    m->output_head = qat_linear_create(DIM, VOCAB_SIZE, false, kd, rng);
    return m;
}

static void pgpt_free(ProfileGPT *m) {
    if (!m) return;
    tensor_free(m->token_emb); tensor_free(m->pos_emb);
    tensor_free(m->grad_token_emb); tensor_free(m->grad_pos_emb);
    for (int i = 0; i < m->n_layers; i++) transformer_block_free(m->blocks[i]);
    free(m->blocks);
    rmsnorm_free(m->final_norm); qat_linear_free(m->output_head);
    free(m->saved_tokens); tensor_free(m->saved_embed); free(m);
}

static void pgpt_mark_weights_dirty(ProfileGPT *m) {
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        b->attn->wq->weights_dirty = true; b->attn->wk->weights_dirty = true;
        b->attn->wv->weights_dirty = true; b->attn->wo->weights_dirty = true;
        b->ffn_up->weights_dirty = true; b->ffn_down->weights_dirty = true;
    }
    m->output_head->weights_dirty = true;
}

static void pgpt_set_qat(ProfileGPT *m, bool use_qat) {
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        b->attn->wq->use_qat = use_qat; b->attn->wk->use_qat = use_qat;
        b->attn->wv->use_qat = use_qat; b->attn->wo->use_qat = use_qat;
        b->ffn_up->use_qat = use_qat; b->ffn_down->use_qat = use_qat;
    }
    m->output_head->use_qat = use_qat;
}

static void pgpt_set_int8_backward(ProfileGPT *m, bool use_int8_bwd) {
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        b->attn->wq->use_int8_backward = use_int8_bwd;
        b->attn->wk->use_int8_backward = use_int8_bwd;
        b->attn->wv->use_int8_backward = use_int8_bwd;
        b->attn->wo->use_int8_backward = use_int8_bwd;
        b->ffn_up->use_int8_backward = use_int8_bwd;
        b->ffn_down->use_int8_backward = use_int8_bwd;
    }
    m->output_head->use_int8_backward = use_int8_bwd;
}

static void pgpt_zero_grad(ProfileGPT *m) {
    memset(m->grad_token_emb->data, 0, tensor_bytes(m->grad_token_emb));
    memset(m->grad_pos_emb->data, 0, tensor_bytes(m->grad_pos_emb));
    for (int i = 0; i < m->n_layers; i++) transformer_block_zero_grad(m->blocks[i]);
    rmsnorm_zero_grad(m->final_norm);
    qat_linear_zero_grad(m->output_head);
}

static void pgpt_register_params(ProfileGPT *m, Adam *opt) {
    adam_add_param(opt, m->token_emb->data, m->grad_token_emb->data, tensor_numel(m->token_emb));
    adam_add_param(opt, m->pos_emb->data, m->grad_pos_emb->data, tensor_numel(m->pos_emb));
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        QATLinear *ls[] = {b->attn->wq, b->attn->wk, b->attn->wv,
                           b->attn->wo, b->ffn_up, b->ffn_down};
        for (int j = 0; j < 6; j++)
            adam_add_param(opt, ls[j]->weight->data, ls[j]->grad_weight->data, tensor_numel(ls[j]->weight));
        adam_add_param(opt, b->norm1->weight->data, b->norm1->grad_weight->data, tensor_numel(b->norm1->weight));
        adam_add_param(opt, b->norm2->weight->data, b->norm2->grad_weight->data, tensor_numel(b->norm2->weight));
    }
    adam_add_param(opt, m->final_norm->weight->data, m->final_norm->grad_weight->data, tensor_numel(m->final_norm->weight));
    adam_add_param(opt, m->output_head->weight->data, m->output_head->grad_weight->data, tensor_numel(m->output_head->weight));
}

/* ---- Main ---- */

int main(void) {
    setvbuf(stdout, NULL, _IOLBF, 0);

    CpuFeatures cpu;
    cpu_detect(&cpu);
    KernelDispatch kd;
    kernel_dispatch_init(&kd, &cpu);
    kernel_dispatch_print(&kd);

    printf("Profile config: %d layers, dim=%d, heads=%d, hidden=%d\n",
           N_LAYERS, DIM, N_HEADS, HIDDEN_DIM);
    printf("Batch: %d x %d = %d tokens/step\n", BATCH_SIZE, SEQ_LEN, BATCH_SIZE * SEQ_LEN);
    printf("Warmup: %d, Profiled: %d steps\n\n", N_WARMUP, N_PROFILE);

    int text_len;
    FILE *f = fopen("shakespeare.txt", "r");
    if (!f) { fprintf(stderr, "Failed to open shakespeare.txt\n"); return 1; }
    fseek(f, 0, SEEK_END); text_len = (int)ftell(f); fseek(f, 0, SEEK_SET);
    char *text = (char *)malloc(text_len + 1);
    text_len = (int)fread(text, 1, text_len, f); text[text_len] = '\0'; fclose(f);
    int *tokens = (int *)malloc(text_len * sizeof(int));
    for (int i = 0; i < text_len; i++) {
        int c = (unsigned char)text[i];
        tokens[i] = (c < VOCAB_SIZE) ? c : 0;
    }
    free(text);
    int train_len = text_len * 9 / 10;

    const char *modes[] = {"FP32", "QAT", "QAT+INT8bwd"};
    bool mode_qat[]     = {false, true, true};
    bool mode_int8bwd[] = {false, false, true};
    int total_tokens = BATCH_SIZE * SEQ_LEN;

    for (int mode = 0; mode < 3; mode++) {
        reset_timers();

        uint64_t rng[4]; rng_seed(rng, 42);
        ProfileGPT *model = pgpt_create(&kd, rng);
        pgpt_set_qat(model, mode_qat[mode]);
        pgpt_set_int8_backward(model, mode_int8bwd[mode]);
        Adam *opt = adam_create(LR, 0.9f, 0.999f, 1e-8f, WEIGHT_DECAY);
        pgpt_register_params(model, opt);

        uint64_t train_rng[4]; rng_seed(train_rng, 123);

        /* Run warmup + profiled steps */
        int total_steps = N_WARMUP + N_PROFILE;
        double total_wall = 0;

        for (int step = 0; step < total_steps; step++) {
            bool profiling = (step >= N_WARMUP);
            if (profiling && step == N_WARMUP)
                reset_timers();

            double step_start = profiling ? timer_sec() : 0;
            double t0;

            /* Sample batch */
            int *input_tokens = (int *)malloc(total_tokens * sizeof(int));
            int *target_tokens = (int *)malloc(total_tokens * sizeof(int));
            for (int b = 0; b < BATCH_SIZE; b++) {
                int start = (int)(rng_next(train_rng) % (train_len - SEQ_LEN - 1));
                memcpy(&input_tokens[b * SEQ_LEN], &tokens[start], SEQ_LEN * sizeof(int));
                memcpy(&target_tokens[b * SEQ_LEN], &tokens[start + 1], SEQ_LEN * sizeof(int));
            }

            pgpt_zero_grad(model);
            adam_zero_grad(opt);

            /* === FORWARD === */

            /* Embedding */
            if (profiling) t0 = timer_sec();
            Tensor *x = tensor_create(total_tokens, DIM);
            for (int b = 0; b < BATCH_SIZE; b++) {
                for (int s = 0; s < SEQ_LEN; s++) {
                    int idx = b * SEQ_LEN + s;
                    int tok = input_tokens[idx];
                    if (tok < 0 || tok >= VOCAB_SIZE) tok = 0;
                    for (int d = 0; d < DIM; d++)
                        x->data[idx * DIM + d] = model->token_emb->data[tok * DIM + d]
                                                + model->pos_emb->data[s * DIM + d];
                }
            }
            if (model->saved_embed) tensor_free(model->saved_embed);
            model->saved_embed = tensor_create(total_tokens, DIM);
            tensor_copy(model->saved_embed, x);
            if (model->saved_tokens) free(model->saved_tokens);
            model->saved_tokens = (int *)malloc(total_tokens * sizeof(int));
            memcpy(model->saved_tokens, input_tokens, total_tokens * sizeof(int));
            model->saved_batch_size = BATCH_SIZE;
            model->saved_seq_len = SEQ_LEN;
            if (profiling) t_embedding += timer_sec() - t0;

            /* Transformer blocks forward */
            for (int i = 0; i < N_LAYERS; i++) {
                Tensor *next = timed_block_forward(model->blocks[i], x,
                                                    BATCH_SIZE, SEQ_LEN);
                tensor_free(x); x = next;
            }

            /* Final norm */
            Tensor *normed = timed_rmsnorm_fwd(model->final_norm, x);
            tensor_free(x);

            /* Output head */
            Tensor *logits = timed_qatlin_fwd(model->output_head, normed);
            tensor_free(normed);

            /* Loss */
            if (profiling) t0 = timer_sec();
            float *gl = (float *)qat_calloc(total_tokens * VOCAB_SIZE * sizeof(float));
            float loss = cross_entropy_loss(logits->data, target_tokens,
                                             total_tokens, VOCAB_SIZE, gl);
            (void)loss;
            if (profiling) t_loss += timer_sec() - t0;

            /* === BACKWARD === */

            Tensor *gt = tensor_wrap(gl, total_tokens, VOCAB_SIZE);

            /* Output head backward */
            Tensor *grad = timed_qatlin_bwd(model->output_head, gt);
            free(gt);

            /* Final norm backward */
            Tensor *grad2 = timed_rmsnorm_bwd(model->final_norm, grad);
            tensor_free(grad);

            /* Transformer blocks backward */
            for (int i = N_LAYERS - 1; i >= 0; i--) {
                Tensor *prev = timed_block_backward(model->blocks[i], grad2,
                                                     BATCH_SIZE, SEQ_LEN);
                tensor_free(grad2); grad2 = prev;
            }

            /* Embedding gradient scatter */
            if (profiling) t0 = timer_sec();
            for (int b = 0; b < BATCH_SIZE; b++) {
                for (int s = 0; s < SEQ_LEN; s++) {
                    int idx = b * SEQ_LEN + s;
                    int tok = model->saved_tokens[idx];
                    if (tok < 0 || tok >= VOCAB_SIZE) tok = 0;
                    for (int d = 0; d < DIM; d++) {
                        model->grad_token_emb->data[tok * DIM + d] += grad2->data[idx * DIM + d];
                        model->grad_pos_emb->data[s * DIM + d] += grad2->data[idx * DIM + d];
                    }
                }
            }
            if (profiling) t_embedding += timer_sec() - t0;
            tensor_free(grad2);

            /* Optimizer */
            if (profiling) t0 = timer_sec();
            adam_step(opt);
            pgpt_mark_weights_dirty(model);
            if (profiling) t_optimizer += timer_sec() - t0;

            tensor_free(logits);
            qat_free(gl);
            free(input_tokens);
            free(target_tokens);

            if (profiling)
                total_wall += timer_sec() - step_start;
        }

        /* Report */
        double N = (double)N_PROFILE;
        double total_accounted = t_qatlin_fwd + t_qatlin_bwd + t_attn_fwd +
            t_attn_bwd + t_rmsnorm + t_gelu +
            t_residual + t_optimizer + t_loss + t_embedding;

        printf("\n========================================\n");
        printf("PROFILE: %s  (%d steps, %.1f ms/step)\n", modes[mode], N_PROFILE, total_wall / N * 1000.0);
        printf("========================================\n\n");

        /* Compute percentages relative to wall time */
        #define PLINE(label, val) \
            printf("  %-35s %7.2f ms  %5.1f%%\n", label, (val) / N * 1000.0, (val) / total_wall * 100.0)

        PLINE("QATLinear forward",  t_qatlin_fwd);
        PLINE("QATLinear backward", t_qatlin_bwd);
        PLINE("Attention forward",  t_attn_fwd);
        PLINE("Attention backward", t_attn_bwd);
        PLINE("RMSNorm (fwd+bwd)", t_rmsnorm);
        PLINE("GeLU (fwd+bwd)",    t_gelu);
        PLINE("Residual + copies", t_residual);
        PLINE("Optimizer (Adam)",  t_optimizer);
        PLINE("Loss (cross-entropy)", t_loss);
        PLINE("Embedding (lookup+grad)", t_embedding);
        printf("  %-35s %7s\n", "---", "---");
        printf("  %-35s %7.2f ms  (accounted: %.1f%%)\n", "TOTAL", total_wall / N * 1000.0,
               total_accounted / total_wall * 100.0);

        #undef PLINE

        /* Also show forward vs backward split */
        double fwd_total = t_qatlin_fwd + t_attn_fwd + t_rmsnorm * 0.5 + t_gelu * 0.5 + t_residual * 0.5;
        double bwd_total = t_qatlin_bwd + t_attn_bwd + t_rmsnorm * 0.5 + t_gelu * 0.5 + t_residual * 0.5;
        printf("\n  Forward:  ~%.1f ms (%.0f%%)\n", fwd_total / N * 1000.0, fwd_total / total_wall * 100.0);
        printf("  Backward: ~%.1f ms (%.0f%%)\n", bwd_total / N * 1000.0, bwd_total / total_wall * 100.0);
        printf("  Other:    ~%.1f ms (%.0f%%)\n",
               (t_optimizer + t_loss + t_embedding) / N * 1000.0,
               (t_optimizer + t_loss + t_embedding) / total_wall * 100.0);

        adam_free(opt);
        pgpt_free(model);
    }

    free(tokens);
    return 0;
}
