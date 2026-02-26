/*
 * profile_qat.c - Per-component timing of QAT vs FP32 training
 *
 * Manually unrolls transformer_block_forward/backward so we can time
 * each component (QATLinear fwd/bwd, attention, RMSNorm, GeLU, etc.).
 *
 * Runs 100 training steps after 5 warmup steps, reports ms/step for each.
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
#define LR           3e-4f
#define WEIGHT_DECAY 0.01f

/* Timing accumulators (seconds) */
static double t_qatlin_fwd;      /* QATLinear forward (quantize + INT8 GEMM + dequant) */
static double t_qatlin_bwd;      /* QATLinear backward (FP32 GEMM + transpose) */
static double t_attn_gemm;       /* Attention FP32 GEMMs (scores + values, fwd+bwd) */
static double t_attn_overhead;   /* Attention extract/scatter/transpose/mask */
static double t_softmax;         /* Softmax forward + backward */
static double t_rmsnorm;         /* RMSNorm forward + backward */
static double t_gelu;            /* GeLU forward + backward */
static double t_residual;        /* Residual adds + tensor copies */
static double t_optimizer;       /* Adam step */
static double t_loss;            /* Cross-entropy loss */
static double t_embedding;       /* Embedding lookup + grad scatter */

static void reset_timers(void) {
    t_qatlin_fwd = t_qatlin_bwd = 0;
    t_attn_gemm = t_attn_overhead = t_softmax = 0;
    t_rmsnorm = t_gelu = t_residual = 0;
    t_optimizer = t_loss = t_embedding = 0;
}

/* Timed wrappers */
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

/* Timed attention forward - instruments the internal components */
static Tensor *timed_attention_forward(Attention *attn, const Tensor *input, int seq_len) {
    double t0;
    int dim = attn->dim;
    int n_heads = attn->n_heads;
    int head_dim = attn->head_dim;
    float scale = 1.0f / sqrtf((float)head_dim);
    gemm_fp32_fn gemm = attn->kernels->fp32_gemm;

    /* Q, K, V projections */
    Tensor *q = timed_qatlin_fwd(attn->wq, input);
    Tensor *k = timed_qatlin_fwd(attn->wk, input);
    Tensor *v = timed_qatlin_fwd(attn->wv, input);

    /* Save for backward (timed as overhead) */
    t0 = timer_sec();
    if (attn->saved_q) tensor_free(attn->saved_q);
    if (attn->saved_k) tensor_free(attn->saved_k);
    if (attn->saved_v) tensor_free(attn->saved_v);
    attn->saved_q = tensor_create(seq_len, dim);
    attn->saved_k = tensor_create(seq_len, dim);
    attn->saved_v = tensor_create(seq_len, dim);
    tensor_copy(attn->saved_q, q);
    tensor_copy(attn->saved_k, k);
    tensor_copy(attn->saved_v, v);
    if (attn->saved_attn) tensor_free(attn->saved_attn);
    attn->saved_attn = tensor_create(n_heads * seq_len, seq_len);
    Tensor *attn_out = tensor_zeros(seq_len, dim);

    float *q_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
    float *k_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
    float *k_h_t = (float *)qat_alloc(head_dim * seq_len * sizeof(float));
    float *v_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
    float *scores = (float *)qat_alloc(seq_len * seq_len * sizeof(float));
    float *attn_w = (float *)qat_alloc(seq_len * seq_len * sizeof(float));
    float *out_h = (float *)qat_alloc(seq_len * head_dim * sizeof(float));
    t_attn_overhead += timer_sec() - t0;

    for (int h = 0; h < n_heads; h++) {
        /* Extract + transpose (overhead) */
        t0 = timer_sec();
        for (int s = 0; s < seq_len; s++) {
            memcpy(&q_h[s * head_dim], &q->data[s * dim + h * head_dim], head_dim * sizeof(float));
            memcpy(&k_h[s * head_dim], &k->data[s * dim + h * head_dim], head_dim * sizeof(float));
            memcpy(&v_h[s * head_dim], &v->data[s * dim + h * head_dim], head_dim * sizeof(float));
        }
        for (int i = 0; i < seq_len; i++)
            for (int j = 0; j < head_dim; j++)
                k_h_t[j * seq_len + i] = k_h[i * head_dim + j];
        t_attn_overhead += timer_sec() - t0;

        /* Score GEMM */
        t0 = timer_sec();
        gemm(seq_len, seq_len, head_dim, scale, q_h, head_dim, k_h_t, seq_len, 0.0f, scores, seq_len);
        t_attn_gemm += timer_sec() - t0;

        /* Causal mask (overhead) */
        t0 = timer_sec();
        if (attn->causal)
            for (int s1 = 0; s1 < seq_len; s1++)
                for (int s2 = s1 + 1; s2 < seq_len; s2++)
                    scores[s1 * seq_len + s2] = -1e9f;
        t_attn_overhead += timer_sec() - t0;

        /* Softmax */
        t0 = timer_sec();
        softmax_forward(scores, attn_w, seq_len, seq_len);
        t_softmax += timer_sec() - t0;

        /* Save attn weights (overhead) */
        t0 = timer_sec();
        memcpy(&attn->saved_attn->data[h * seq_len * seq_len], attn_w, seq_len * seq_len * sizeof(float));
        t_attn_overhead += timer_sec() - t0;

        /* Value GEMM */
        t0 = timer_sec();
        gemm(seq_len, head_dim, seq_len, 1.0f, attn_w, seq_len, v_h, head_dim, 0.0f, out_h, head_dim);
        t_attn_gemm += timer_sec() - t0;

        /* Scatter (overhead) */
        t0 = timer_sec();
        for (int s = 0; s < seq_len; s++)
            memcpy(&attn_out->data[s * dim + h * head_dim], &out_h[s * head_dim], head_dim * sizeof(float));
        t_attn_overhead += timer_sec() - t0;
    }

    t0 = timer_sec();
    qat_free(q_h); qat_free(k_h); qat_free(k_h_t);
    qat_free(v_h); qat_free(scores); qat_free(attn_w); qat_free(out_h);
    tensor_free(q); tensor_free(k); tensor_free(v);
    t_attn_overhead += timer_sec() - t0;

    /* Wo projection */
    Tensor *output = timed_qatlin_fwd(attn->wo, attn_out);
    tensor_free(attn_out);
    return output;
}

/* Timed transformer block forward */
static Tensor *timed_block_forward(TransformerBlock *block, const Tensor *input, int seq_len) {
    double t0;
    int dim = block->dim;
    int hidden_dim = block->hidden_dim;

    t0 = timer_sec();
    if (block->saved_residual1) tensor_free(block->saved_residual1);
    block->saved_residual1 = tensor_create(seq_len, dim);
    tensor_copy(block->saved_residual1, input);
    t_residual += timer_sec() - t0;

    Tensor *normed1 = timed_rmsnorm_fwd(block->norm1, input);

    t0 = timer_sec();
    if (block->saved_normed1) tensor_free(block->saved_normed1);
    block->saved_normed1 = tensor_create(seq_len, dim);
    tensor_copy(block->saved_normed1, normed1);
    t_residual += timer_sec() - t0;

    Tensor *attn_out = timed_attention_forward(block->attn, normed1, seq_len);
    tensor_free(normed1);

    t0 = timer_sec();
    Tensor *after_attn = tensor_create(seq_len, dim);
    for (int i = 0; i < seq_len * dim; i++)
        after_attn->data[i] = input->data[i] + attn_out->data[i];
    tensor_free(attn_out);
    if (block->saved_residual2) tensor_free(block->saved_residual2);
    block->saved_residual2 = tensor_create(seq_len, dim);
    tensor_copy(block->saved_residual2, after_attn);
    t_residual += timer_sec() - t0;

    Tensor *normed2 = timed_rmsnorm_fwd(block->norm2, after_attn);

    t0 = timer_sec();
    if (block->saved_normed2) tensor_free(block->saved_normed2);
    block->saved_normed2 = tensor_create(seq_len, dim);
    tensor_copy(block->saved_normed2, normed2);
    t_residual += timer_sec() - t0;

    Tensor *ffn_up = timed_qatlin_fwd(block->ffn_up, normed2);
    tensor_free(normed2);

    t0 = timer_sec();
    if (block->saved_ffn_hidden) tensor_free(block->saved_ffn_hidden);
    block->saved_ffn_hidden = tensor_create(seq_len, hidden_dim);
    tensor_copy(block->saved_ffn_hidden, ffn_up);
    t_residual += timer_sec() - t0;

    t0 = timer_sec();
    gelu_forward(ffn_up->data, ffn_up->data, seq_len * hidden_dim);
    t_gelu += timer_sec() - t0;

    Tensor *ffn_out = timed_qatlin_fwd(block->ffn_down, ffn_up);
    tensor_free(ffn_up);

    t0 = timer_sec();
    Tensor *output = tensor_create(seq_len, dim);
    for (int i = 0; i < seq_len * dim; i++)
        output->data[i] = after_attn->data[i] + ffn_out->data[i];
    tensor_free(after_attn); tensor_free(ffn_out);
    t_residual += timer_sec() - t0;

    return output;
}

/* Timed transformer block backward (uses the built-in backward since
 * it's already complex — but we time the sub-calls) */
static Tensor *timed_block_backward(TransformerBlock *block, const Tensor *grad_output, int seq_len) {
    double t0;
    int dim = block->dim;
    int hidden_dim = block->hidden_dim;

    /* FFN backward */
    Tensor *grad_ffn_act = timed_qatlin_bwd(block->ffn_down, grad_output);

    t0 = timer_sec();
    Tensor *grad_ffn_up = tensor_create(seq_len, hidden_dim);
    gelu_backward(block->saved_ffn_hidden->data, grad_ffn_act->data,
                  grad_ffn_up->data, seq_len * hidden_dim);
    t_gelu += timer_sec() - t0;
    tensor_free(grad_ffn_act);

    Tensor *grad_normed2 = timed_qatlin_bwd(block->ffn_up, grad_ffn_up);
    tensor_free(grad_ffn_up);

    Tensor *grad_after_attn = timed_rmsnorm_bwd(block->norm2, grad_normed2);
    tensor_free(grad_normed2);

    t0 = timer_sec();
    for (int i = 0; i < seq_len * dim; i++)
        grad_after_attn->data[i] += grad_output->data[i];
    t_residual += timer_sec() - t0;

    /* Attention backward (use the built-in, time the whole thing
     * minus the QATLinear calls which we time separately) */
    double t_before_attn_bwd = timer_sec();
    Tensor *grad_normed1 = attention_backward(block->attn, grad_after_attn, seq_len);
    double attn_bwd_total = timer_sec() - t_before_attn_bwd;
    /* Attention backward contains 4 qat_linear_backward calls internally.
     * We can't easily separate them without re-implementing attention_backward.
     * So we'll attribute the whole thing to attn_gemm + qatlin_bwd estimate. */
    t_attn_gemm += attn_bwd_total;  /* Approximate: mostly FP32 GEMMs */

    Tensor *grad_input = timed_rmsnorm_bwd(block->norm1, grad_normed1);
    tensor_free(grad_normed1);

    t0 = timer_sec();
    for (int i = 0; i < seq_len * dim; i++)
        grad_input->data[i] += grad_after_attn->data[i];
    tensor_free(grad_after_attn);
    t_residual += timer_sec() - t0;

    return grad_input;
}

/* ---- Minimal GPT model ---- */

typedef struct {
    int vocab_size, dim, n_layers, n_heads, hidden_dim, max_seq_len;
    Tensor *token_emb, *pos_emb, *grad_token_emb, *grad_pos_emb;
    TransformerBlock **blocks;
    RMSNorm *final_norm;
    QATLinear *output_head;
    const KernelDispatch *kernels;
    int *saved_tokens;
    int saved_seq_len;
    Tensor *saved_embed;
} GPTModel;

static GPTModel *gpt_create(const KernelDispatch *kd, uint64_t *rng) {
    GPTModel *m = (GPTModel *)calloc(1, sizeof(GPTModel));
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
        m->blocks[i] = transformer_block_create(DIM, HIDDEN_DIM, N_HEADS, kd, rng);
        m->blocks[i]->attn->causal = true;
    }
    m->final_norm = rmsnorm_create(DIM, 1e-5f);
    m->output_head = qat_linear_create(DIM, VOCAB_SIZE, false, kd, rng);
    return m;
}

static void gpt_free(GPTModel *m) {
    if (!m) return;
    tensor_free(m->token_emb); tensor_free(m->pos_emb);
    tensor_free(m->grad_token_emb); tensor_free(m->grad_pos_emb);
    for (int i = 0; i < m->n_layers; i++) transformer_block_free(m->blocks[i]);
    free(m->blocks);
    rmsnorm_free(m->final_norm); qat_linear_free(m->output_head);
    free(m->saved_tokens); tensor_free(m->saved_embed); free(m);
}

static void gpt_set_qat(GPTModel *m, bool use_qat) {
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        b->attn->wq->use_qat = use_qat; b->attn->wk->use_qat = use_qat;
        b->attn->wv->use_qat = use_qat; b->attn->wo->use_qat = use_qat;
        b->ffn_up->use_qat = use_qat; b->ffn_down->use_qat = use_qat;
    }
    m->output_head->use_qat = use_qat;
}

static void gpt_zero_grad(GPTModel *m) {
    memset(m->grad_token_emb->data, 0, tensor_bytes(m->grad_token_emb));
    memset(m->grad_pos_emb->data, 0, tensor_bytes(m->grad_pos_emb));
    for (int i = 0; i < m->n_layers; i++) transformer_block_zero_grad(m->blocks[i]);
    rmsnorm_zero_grad(m->final_norm);
    qat_linear_zero_grad(m->output_head);
}

static void gpt_register_params(GPTModel *m, Adam *opt) {
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

    const char *modes[] = {"FP32", "QAT"};
    bool use_qat[] = {false, true};

    for (int mode = 0; mode < 2; mode++) {
        reset_timers();

        uint64_t rng[4]; rng_seed(rng, 42);
        GPTModel *model = gpt_create(&kd, rng);
        gpt_set_qat(model, use_qat[mode]);
        Adam *opt = adam_create(LR, 0.9f, 0.999f, 1e-8f, WEIGHT_DECAY);
        gpt_register_params(model, opt);

        uint64_t train_rng[4]; rng_seed(train_rng, 123);
        int n_warmup = 5, n_profile = 100;

        /* Warmup (use built-in forward/backward, don't time) */
        for (int step = 0; step < n_warmup; step++) {
            int start = (int)(rng_next(train_rng) % (train_len - SEQ_LEN - 1));
            gpt_zero_grad(model); adam_zero_grad(opt);
            /* Use timed versions even during warmup (just to exercise same path) */
            /* ... actually just use the normal path */
            Tensor *x = tensor_create(SEQ_LEN, model->dim);
            for (int s = 0; s < SEQ_LEN; s++) {
                int tok = tokens[start + s]; if (tok < 0 || tok >= VOCAB_SIZE) tok = 0;
                for (int d = 0; d < DIM; d++)
                    x->data[s * DIM + d] = model->token_emb->data[tok * DIM + d] + model->pos_emb->data[s * DIM + d];
            }
            if (model->saved_embed) tensor_free(model->saved_embed);
            model->saved_embed = tensor_create(SEQ_LEN, DIM);
            tensor_copy(model->saved_embed, x);
            if (model->saved_tokens) free(model->saved_tokens);
            model->saved_tokens = (int *)malloc(SEQ_LEN * sizeof(int));
            memcpy(model->saved_tokens, &tokens[start], SEQ_LEN * sizeof(int));
            model->saved_seq_len = SEQ_LEN;
            for (int i = 0; i < N_LAYERS; i++) {
                Tensor *next = transformer_block_forward(model->blocks[i], x, SEQ_LEN);
                tensor_free(x); x = next;
            }
            Tensor *normed = rmsnorm_forward(model->final_norm, x); tensor_free(x);
            Tensor *logits = qat_linear_forward(model->output_head, normed); tensor_free(normed);
            float *gl = (float *)qat_calloc(SEQ_LEN * VOCAB_SIZE * sizeof(float));
            cross_entropy_loss(logits->data, &tokens[start + 1], SEQ_LEN, VOCAB_SIZE, gl);
            Tensor *gt = tensor_wrap(gl, SEQ_LEN, VOCAB_SIZE);
            /* Backward */
            Tensor *grad = qat_linear_backward(model->output_head, gt);
            Tensor *grad2 = rmsnorm_backward(model->final_norm, grad); tensor_free(grad);
            for (int i = N_LAYERS - 1; i >= 0; i--) {
                Tensor *prev = transformer_block_backward(model->blocks[i], grad2, SEQ_LEN);
                tensor_free(grad2); grad2 = prev;
            }
            tensor_free(grad2); free(gt);
            adam_step(opt);
            tensor_free(logits); qat_free(gl);
        }

        reset_timers();

        /* Profiled training loop */
        double total_wall = 0;
        for (int step = 0; step < n_profile; step++) {
            double t0, step_start = timer_sec();
            int start = (int)(rng_next(train_rng) % (train_len - SEQ_LEN - 1));
            gpt_zero_grad(model); adam_zero_grad(opt);

            /* === FORWARD === */

            /* Embedding */
            t0 = timer_sec();
            Tensor *x = tensor_create(SEQ_LEN, model->dim);
            for (int s = 0; s < SEQ_LEN; s++) {
                int tok = tokens[start + s]; if (tok < 0 || tok >= VOCAB_SIZE) tok = 0;
                for (int d = 0; d < DIM; d++)
                    x->data[s * DIM + d] = model->token_emb->data[tok * DIM + d] + model->pos_emb->data[s * DIM + d];
            }
            if (model->saved_embed) tensor_free(model->saved_embed);
            model->saved_embed = tensor_create(SEQ_LEN, DIM);
            tensor_copy(model->saved_embed, x);
            if (model->saved_tokens) free(model->saved_tokens);
            model->saved_tokens = (int *)malloc(SEQ_LEN * sizeof(int));
            memcpy(model->saved_tokens, &tokens[start], SEQ_LEN * sizeof(int));
            model->saved_seq_len = SEQ_LEN;
            t_embedding += timer_sec() - t0;

            /* Transformer blocks forward */
            for (int i = 0; i < N_LAYERS; i++) {
                Tensor *next = timed_block_forward(model->blocks[i], x, SEQ_LEN);
                tensor_free(x); x = next;
            }

            /* Final norm */
            Tensor *normed = timed_rmsnorm_fwd(model->final_norm, x);
            tensor_free(x);

            /* Output head */
            Tensor *logits = timed_qatlin_fwd(model->output_head, normed);
            tensor_free(normed);

            /* Loss */
            t0 = timer_sec();
            float *gl = (float *)qat_calloc(SEQ_LEN * VOCAB_SIZE * sizeof(float));
            float loss = cross_entropy_loss(logits->data, &tokens[start + 1], SEQ_LEN, VOCAB_SIZE, gl);
            (void)loss;
            t_loss += timer_sec() - t0;

            /* === BACKWARD === */

            Tensor *gt = tensor_wrap(gl, SEQ_LEN, VOCAB_SIZE);

            /* Output head backward */
            Tensor *grad = timed_qatlin_bwd(model->output_head, gt);
            free(gt);

            /* Final norm backward */
            Tensor *grad2 = timed_rmsnorm_bwd(model->final_norm, grad);
            tensor_free(grad);

            /* Transformer blocks backward */
            for (int i = N_LAYERS - 1; i >= 0; i--) {
                Tensor *prev = timed_block_backward(model->blocks[i], grad2, SEQ_LEN);
                tensor_free(grad2); grad2 = prev;
            }

            /* Embedding gradient scatter */
            t0 = timer_sec();
            for (int s = 0; s < SEQ_LEN; s++) {
                int tok = model->saved_tokens[s]; if (tok < 0 || tok >= VOCAB_SIZE) tok = 0;
                for (int d = 0; d < DIM; d++) {
                    model->grad_token_emb->data[tok * DIM + d] += grad2->data[s * DIM + d];
                    model->grad_pos_emb->data[s * DIM + d] += grad2->data[s * DIM + d];
                }
            }
            t_embedding += timer_sec() - t0;
            tensor_free(grad2);

            /* Optimizer */
            t0 = timer_sec();
            adam_step(opt);
            t_optimizer += timer_sec() - t0;

            tensor_free(logits);
            qat_free(gl);
            total_wall += timer_sec() - step_start;
        }

        /* Report */
        double N = (double)n_profile;
        double total_accounted = t_qatlin_fwd + t_qatlin_bwd + t_attn_gemm +
            t_attn_overhead + t_softmax + t_rmsnorm + t_gelu +
            t_residual + t_optimizer + t_loss + t_embedding;

        printf("\n========================================\n");
        printf("PROFILE: %s  (%d steps, %.1f ms/step)\n", modes[mode], n_profile, total_wall / N * 1000.0);
        printf("========================================\n\n");
        printf("  %-35s %7.2f ms  %5.1f%%\n", "QATLinear forward",  t_qatlin_fwd / N * 1000, t_qatlin_fwd / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "QATLinear backward", t_qatlin_bwd / N * 1000, t_qatlin_bwd / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "Attention FP32 GEMM (fwd+bwd)",  t_attn_gemm / N * 1000, t_attn_gemm / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "Attention overhead (copy/xpose)", t_attn_overhead / N * 1000, t_attn_overhead / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "Softmax (fwd+bwd)",              t_softmax / N * 1000, t_softmax / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "RMSNorm (fwd+bwd)",              t_rmsnorm / N * 1000, t_rmsnorm / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "GeLU (fwd+bwd)",                 t_gelu / N * 1000, t_gelu / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "Residual + tensor copies",       t_residual / N * 1000, t_residual / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "Optimizer (Adam)",               t_optimizer / N * 1000, t_optimizer / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "Loss (cross-entropy)",           t_loss / N * 1000, t_loss / total_wall * 100);
        printf("  %-35s %7.2f ms  %5.1f%%\n", "Embedding (lookup+grad)",        t_embedding / N * 1000, t_embedding / total_wall * 100);
        printf("  %-35s %7.2f ms\n", "---", 0.0);
        printf("  %-35s %7.2f ms  (accounted: %.1f%%)\n", "TOTAL", total_wall / N * 1000,
               total_accounted / total_wall * 100);

        adam_free(opt);
        gpt_free(model);
    }

    free(tokens);
    return 0;
}
