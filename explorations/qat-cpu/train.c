/*
 * train.c - End-to-end GPT training with QAT vs FP32 comparison
 *
 * Trains a small character-level GPT on Shakespeare.
 * Compares:
 *   1. FP32 baseline (pure floating-point forward + backward)
 *   2. QAT (INT8 forward via VNNI, FP32 backward via STE)
 *
 * Metrics: perplexity, generated text samples, wall-clock time.
 */

#include "qat_cpu.h"
#include <assert.h>

/* ========================================================================
 * Configuration (overridable via -D flags at compile time)
 * ======================================================================== */

#ifndef VOCAB_SIZE
#define VOCAB_SIZE   128   /* ASCII */
#endif
#ifndef DIM
#define DIM          512
#endif
#ifndef N_LAYERS
#define N_LAYERS     4
#endif
#ifndef N_HEADS
#define N_HEADS      8
#endif
#ifndef HIDDEN_DIM
#define HIDDEN_DIM   2048
#endif
#ifndef MAX_SEQ_LEN
#define MAX_SEQ_LEN  256
#endif
#ifndef SEQ_LEN
#define SEQ_LEN      64    /* Training sequence length */
#endif
#ifndef BATCH_SIZE
#define BATCH_SIZE   8     /* Mini-batch size (sequences per step) */
#endif
#ifndef N_STEPS
#define N_STEPS      10000
#endif
#ifndef EVAL_EVERY
#define EVAL_EVERY   1000
#endif
#ifndef GEN_EVERY
#define GEN_EVERY    2500
#endif
#define GEN_LEN      200
#define LR           3e-4f
#define WEIGHT_DECAY 0.01f
#define GEN_TEMP     0.8f

/* ========================================================================
 * GPT Model
 * ======================================================================== */

typedef struct {
    int vocab_size;
    int dim;
    int n_layers;
    int n_heads;
    int hidden_dim;
    int max_seq_len;

    /* Embeddings */
    Tensor *token_emb;          /* [vocab_size x dim] */
    Tensor *pos_emb;            /* [max_seq_len x dim] */
    Tensor *grad_token_emb;
    Tensor *grad_pos_emb;

    /* Transformer blocks */
    TransformerBlock **blocks;

    /* Output head */
    RMSNorm   *final_norm;
    QATLinear *output_head;     /* [dim x vocab_size] */

    const KernelDispatch *kernels;

    /* Saved for backward */
    int   *saved_tokens;        /* [batch_size * seq_len] */
    int    saved_batch_size;
    int    saved_seq_len;
    Tensor *saved_embed;        /* [batch_size * seq_len x dim] */
} GPTModel;

/* Forward declarations */
static void gpt_set_qat(GPTModel *model, bool use_qat);
static void gpt_set_int8_backward(GPTModel *model, bool use_int8_bwd);

static GPTModel *gpt_create(const KernelDispatch *kd, uint64_t *rng) {
    GPTModel *m = (GPTModel *)calloc(1, sizeof(GPTModel));

    m->vocab_size   = VOCAB_SIZE;
    m->dim          = DIM;
    m->n_layers     = N_LAYERS;
    m->n_heads      = N_HEADS;
    m->hidden_dim   = HIDDEN_DIM;
    m->max_seq_len  = MAX_SEQ_LEN;
    m->kernels      = kd;

    /* Embeddings: small random init */
    m->token_emb = tensor_create(VOCAB_SIZE, DIM);
    tensor_rand(m->token_emb, -0.02f, 0.02f, rng);
    m->pos_emb = tensor_create(MAX_SEQ_LEN, DIM);
    tensor_rand(m->pos_emb, -0.02f, 0.02f, rng);
    m->grad_token_emb = tensor_zeros(VOCAB_SIZE, DIM);
    m->grad_pos_emb = tensor_zeros(MAX_SEQ_LEN, DIM);

    /* Transformer blocks */
    m->blocks = (TransformerBlock **)calloc(N_LAYERS, sizeof(TransformerBlock *));
    for (int i = 0; i < N_LAYERS; i++) {
        m->blocks[i] = transformer_block_create(DIM, HIDDEN_DIM, N_HEADS, kd, rng);
        /* Enable causal masking */
        m->blocks[i]->attn->causal = true;
    }

    /* Output */
    m->final_norm = rmsnorm_create(DIM, 1e-5f);
    m->output_head = qat_linear_create(DIM, VOCAB_SIZE, false, kd, rng);

    m->saved_tokens = NULL;

    return m;
}

static void gpt_free(GPTModel *m) {
    if (!m) return;
    tensor_free(m->token_emb);
    tensor_free(m->pos_emb);
    tensor_free(m->grad_token_emb);
    tensor_free(m->grad_pos_emb);
    for (int i = 0; i < m->n_layers; i++) {
        transformer_block_free(m->blocks[i]);
    }
    free(m->blocks);
    rmsnorm_free(m->final_norm);
    qat_linear_free(m->output_head);
    free(m->saved_tokens);
    tensor_free(m->saved_embed);
    free(m);
}

static void gpt_set_qat(GPTModel *model, bool use_qat) {
    for (int i = 0; i < model->n_layers; i++) {
        TransformerBlock *b = model->blocks[i];
        b->attn->wq->use_qat = use_qat;
        b->attn->wk->use_qat = use_qat;
        b->attn->wv->use_qat = use_qat;
        b->attn->wo->use_qat = use_qat;
        b->ffn_up->use_qat = use_qat;
        b->ffn_down->use_qat = use_qat;
    }
    model->output_head->use_qat = use_qat;
}

static void gpt_set_int8_backward(GPTModel *model, bool use_int8_bwd) {
    for (int i = 0; i < model->n_layers; i++) {
        TransformerBlock *b = model->blocks[i];
        b->attn->wq->use_int8_backward = use_int8_bwd;
        b->attn->wk->use_int8_backward = use_int8_bwd;
        b->attn->wv->use_int8_backward = use_int8_bwd;
        b->attn->wo->use_int8_backward = use_int8_bwd;
        b->ffn_up->use_int8_backward = use_int8_bwd;
        b->ffn_down->use_int8_backward = use_int8_bwd;
    }
    model->output_head->use_int8_backward = use_int8_bwd;
}

/*
 * Forward pass with mini-batch support.
 *
 * tokens: [batch_size * seq_len] flattened token array.
 *   Sequences are contiguous: tokens[b*seq_len .. (b+1)*seq_len-1] is sequence b.
 * Returns logits: [batch_size * seq_len, vocab_size]
 */
static Tensor *gpt_forward(GPTModel *m, const int *tokens,
                            int batch_size, int seq_len) {
    assert(seq_len <= m->max_seq_len);
    int total_tokens = batch_size * seq_len;

    /* Save tokens for backward */
    if (m->saved_tokens) free(m->saved_tokens);
    m->saved_tokens = (int *)malloc(total_tokens * sizeof(int));
    memcpy(m->saved_tokens, tokens, total_tokens * sizeof(int));
    m->saved_batch_size = batch_size;
    m->saved_seq_len = seq_len;

    /*
     * 1. Embedding: x[b*S+s] = token_emb[tokens[b*S+s]] + pos_emb[s]
     *    Position embedding uses RELATIVE position s within each sequence.
     */
    Tensor *x = tensor_create(total_tokens, m->dim);
    for (int b = 0; b < batch_size; b++) {
        for (int s = 0; s < seq_len; s++) {
            int idx = b * seq_len + s;
            int tok = tokens[idx];
            if (tok < 0 || tok >= m->vocab_size) tok = 0;
            for (int d = 0; d < m->dim; d++) {
                x->data[idx * m->dim + d] =
                    m->token_emb->data[tok * m->dim + d] +
                    m->pos_emb->data[s * m->dim + d];  /* s, not idx */
            }
        }
    }

    /* Save embedding output for backward */
    if (m->saved_embed) tensor_free(m->saved_embed);
    m->saved_embed = tensor_create(total_tokens, m->dim);
    tensor_copy(m->saved_embed, x);

    /* 2. Transformer blocks — pass batch_size so attention is per-sequence */
    for (int i = 0; i < m->n_layers; i++) {
        Tensor *next = transformer_block_forward(m->blocks[i], x,
                                                  batch_size, seq_len);
        tensor_free(x);
        x = next;
    }

    /* 3. Final norm — batch-agnostic */
    Tensor *normed = rmsnorm_forward(m->final_norm, x);
    tensor_free(x);

    /* 4. Output head: [B*S x dim] -> [B*S x vocab_size] */
    Tensor *logits = qat_linear_forward(m->output_head, normed);
    tensor_free(normed);

    return logits;
}

/*
 * Backward pass with mini-batch support.
 * grad_logits: [batch_size * seq_len, vocab_size]
 */
static void gpt_backward(GPTModel *m, const Tensor *grad_logits) {
    int batch_size = m->saved_batch_size;
    int seq_len = m->saved_seq_len;

    /* Output head backward — batch-agnostic */
    Tensor *grad = qat_linear_backward(m->output_head, grad_logits);

    /* Final norm backward — batch-agnostic */
    Tensor *grad2 = rmsnorm_backward(m->final_norm, grad);
    tensor_free(grad);

    /* Transformer blocks backward (reverse order) */
    for (int i = m->n_layers - 1; i >= 0; i--) {
        Tensor *prev = transformer_block_backward(m->blocks[i], grad2,
                                                   batch_size, seq_len);
        tensor_free(grad2);
        grad2 = prev;
    }

    /*
     * Scatter gradients to embeddings.
     * Position embedding uses relative position s within each sequence.
     */
    for (int b = 0; b < batch_size; b++) {
        for (int s = 0; s < seq_len; s++) {
            int idx = b * seq_len + s;
            int tok = m->saved_tokens[idx];
            if (tok < 0 || tok >= m->vocab_size) tok = 0;
            for (int d = 0; d < m->dim; d++) {
                m->grad_token_emb->data[tok * m->dim + d] +=
                    grad2->data[idx * m->dim + d];
                m->grad_pos_emb->data[s * m->dim + d] +=  /* s, not idx */
                    grad2->data[idx * m->dim + d];
            }
        }
    }

    tensor_free(grad2);
}

/* Mark all QATLinear weight caches as stale (call after optimizer step) */
static void gpt_mark_weights_dirty(GPTModel *m) {
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        b->attn->wq->weights_dirty = true;
        b->attn->wk->weights_dirty = true;
        b->attn->wv->weights_dirty = true;
        b->attn->wo->weights_dirty = true;
        b->ffn_up->weights_dirty = true;
        b->ffn_down->weights_dirty = true;
    }
    m->output_head->weights_dirty = true;
}

static void gpt_zero_grad(GPTModel *m) {
    memset(m->grad_token_emb->data, 0, tensor_bytes(m->grad_token_emb));
    memset(m->grad_pos_emb->data, 0, tensor_bytes(m->grad_pos_emb));
    for (int i = 0; i < m->n_layers; i++) {
        transformer_block_zero_grad(m->blocks[i]);
    }
    rmsnorm_zero_grad(m->final_norm);
    qat_linear_zero_grad(m->output_head);
}

static void gpt_register_params(GPTModel *m, Adam *opt) {
    /* Embeddings */
    adam_add_param(opt, m->token_emb->data, m->grad_token_emb->data,
                   tensor_numel(m->token_emb));
    adam_add_param(opt, m->pos_emb->data, m->grad_pos_emb->data,
                   tensor_numel(m->pos_emb));

    /* Transformer blocks */
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        /* Attention projections */
        QATLinear *linears[] = {b->attn->wq, b->attn->wk, b->attn->wv,
                                b->attn->wo, b->ffn_up, b->ffn_down};
        for (int j = 0; j < 6; j++) {
            adam_add_param(opt, linears[j]->weight->data,
                           linears[j]->grad_weight->data,
                           tensor_numel(linears[j]->weight));
        }
        /* Norms */
        adam_add_param(opt, b->norm1->weight->data, b->norm1->grad_weight->data,
                       tensor_numel(b->norm1->weight));
        adam_add_param(opt, b->norm2->weight->data, b->norm2->grad_weight->data,
                       tensor_numel(b->norm2->weight));
    }

    /* Final norm */
    adam_add_param(opt, m->final_norm->weight->data,
                   m->final_norm->grad_weight->data,
                   tensor_numel(m->final_norm->weight));

    /* Output head */
    adam_add_param(opt, m->output_head->weight->data,
                   m->output_head->grad_weight->data,
                   tensor_numel(m->output_head->weight));
}

/* Count total parameters */
static int gpt_count_params(GPTModel *m) {
    int total = 0;
    total += tensor_numel(m->token_emb);
    total += tensor_numel(m->pos_emb);
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        QATLinear *linears[] = {b->attn->wq, b->attn->wk, b->attn->wv,
                                b->attn->wo, b->ffn_up, b->ffn_down};
        for (int j = 0; j < 6; j++) {
            total += tensor_numel(linears[j]->weight);
        }
        total += tensor_numel(b->norm1->weight);
        total += tensor_numel(b->norm2->weight);
    }
    total += tensor_numel(m->final_norm->weight);
    total += tensor_numel(m->output_head->weight);
    return total;
}

/* ========================================================================
 * Data Loading
 * ======================================================================== */

static char *load_text_file(const char *path, int *len) {
    FILE *f = fopen(path, "r");
    if (!f) {
        fprintf(stderr, "Cannot open %s\n", path);
        return NULL;
    }
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *buf = (char *)malloc(size + 1);
    *len = (int)fread(buf, 1, size, f);
    buf[*len] = '\0';
    fclose(f);
    return buf;
}

/* Convert text to token IDs (ASCII values, clamped to [0, VOCAB_SIZE-1]) */
static void text_to_tokens(const char *text, int len, int *tokens) {
    for (int i = 0; i < len; i++) {
        int c = (unsigned char)text[i];
        tokens[i] = (c < VOCAB_SIZE) ? c : 0;
    }
}

/* ========================================================================
 * Training
 * ======================================================================== */

/*
 * One training step with mini-batching:
 *   1. Sample BATCH_SIZE random sequences from data
 *   2. Forward: logits = model(input_tokens)  [B*S, vocab]
 *   3. Loss: cross-entropy against next-token targets
 *   4. Backward
 *   5. Optimizer step
 *   Returns mean loss across all tokens in the batch.
 */
static float train_step(GPTModel *model, Adam *opt,
                        const int *data, int data_len,
                        uint64_t *rng) {
    int seq_len = SEQ_LEN;
    int batch_size = BATCH_SIZE;
    int total_tokens = batch_size * seq_len;

    /* Build batched input and target arrays */
    int *input_tokens = (int *)malloc(total_tokens * sizeof(int));
    int *target_tokens = (int *)malloc(total_tokens * sizeof(int));

    for (int b = 0; b < batch_size; b++) {
        int start = (int)(rng_next(rng) % (data_len - seq_len - 1));
        memcpy(&input_tokens[b * seq_len], &data[start],
               seq_len * sizeof(int));
        memcpy(&target_tokens[b * seq_len], &data[start + 1],
               seq_len * sizeof(int));
    }

    /* Zero gradients */
    gpt_zero_grad(model);
    adam_zero_grad(opt);

    /* Forward — [B*S, vocab] */
    Tensor *logits = gpt_forward(model, input_tokens, batch_size, seq_len);

    /* Cross-entropy loss: treats all B*S tokens as independent samples */
    float *grad_logits = (float *)qat_calloc(total_tokens * VOCAB_SIZE * sizeof(float));
    float loss = cross_entropy_loss(logits->data, target_tokens,
                                     total_tokens, VOCAB_SIZE, grad_logits);

    /* Backward */
    Tensor *grad_tensor = tensor_wrap(grad_logits, total_tokens, VOCAB_SIZE);
    gpt_backward(model, grad_tensor);
    free(grad_tensor);

    /* Optimizer step */
    adam_step(opt);
    gpt_mark_weights_dirty(model);

    tensor_free(logits);
    qat_free(grad_logits);
    free(input_tokens);
    free(target_tokens);

    return loss;
}

/* ========================================================================
 * Evaluation
 * ======================================================================== */

/*
 * Bits per byte (BPB): tokenizer-agnostic quality metric.
 *
 * BPB = CE_loss_nats / ln(2)
 *
 * This works directly because we use character-level tokens (1 token = 1 byte).
 * For subword tokenizers you'd compute:
 *   BPB = total_CE_nats / (ln(2) * total_bytes)
 *
 * Reference values (character-level on Shakespeare-like text):
 *   Random baseline (128 ASCII): log(128)/ln(2) = 7.0 BPB
 *   Good char-level model: ~1.2-1.5 BPB
 */
static float loss_to_bpb(float ce_loss_nats) {
    return ce_loss_nats / logf(2.0f);
}

typedef struct {
    float loss;   /* average CE loss in nats */
    float ppl;    /* perplexity = exp(loss) */
    float bpb;    /* bits per byte = loss / ln(2) */
} EvalResult;

/*
 * Evaluate model on a data slice.
 * Returns loss (nats), perplexity, and bits-per-byte.
 * Evaluates on non-overlapping sequences.
 */
static EvalResult evaluate(GPTModel *model, const int *data, int data_len) {
    EvalResult r = {0};
    int seq_len = SEQ_LEN;
    int n_seqs = data_len / (seq_len + 1);
    if (n_seqs > 50) n_seqs = 50;  /* Cap to keep eval fast */
    if (n_seqs == 0) { r.ppl = 999.0f; r.bpb = 99.0f; return r; }

    float total_loss = 0.0f;
    float *grad_dummy = (float *)qat_calloc(seq_len * VOCAB_SIZE * sizeof(float));

    for (int s = 0; s < n_seqs; s++) {
        int start = s * (seq_len + 1);
        const int *input_tokens = &data[start];
        const int *target_tokens = &data[start + 1];

        Tensor *logits = gpt_forward(model, input_tokens, 1, seq_len);
        float loss = cross_entropy_loss(logits->data, target_tokens,
                                         seq_len, VOCAB_SIZE, grad_dummy);
        total_loss += loss;
        tensor_free(logits);
    }

    qat_free(grad_dummy);
    r.loss = total_loss / (float)n_seqs;
    r.ppl = expf(r.loss);
    r.bpb = loss_to_bpb(r.loss);
    return r;
}

/* ========================================================================
 * Text Generation
 * ======================================================================== */

/*
 * Sample a token from logits with temperature scaling.
 * temperature=0 -> argmax (greedy)
 * temperature=1 -> standard sampling
 * temperature>1 -> more random
 */
static int sample_token(const float *logits, int vocab_size,
                        float temperature, uint64_t *rng) {
    if (temperature < 1e-6f) {
        /* Greedy: argmax */
        int best = 0;
        float best_val = logits[0];
        for (int i = 1; i < vocab_size; i++) {
            if (logits[i] > best_val) {
                best_val = logits[i];
                best = i;
            }
        }
        return best;
    }

    /* Temperature-scaled softmax sampling */
    float max_val = logits[0];
    for (int i = 1; i < vocab_size; i++) {
        if (logits[i] > max_val) max_val = logits[i];
    }

    float sum = 0.0f;
    float *probs = (float *)qat_alloc(vocab_size * sizeof(float));
    for (int i = 0; i < vocab_size; i++) {
        probs[i] = expf((logits[i] - max_val) / temperature);
        sum += probs[i];
    }

    /* Normalize and sample */
    float r = rng_uniform(rng) * sum;
    float cumsum = 0.0f;
    int token = vocab_size - 1;
    for (int i = 0; i < vocab_size; i++) {
        cumsum += probs[i];
        if (cumsum >= r) {
            token = i;
            break;
        }
    }

    qat_free(probs);
    return token;
}

/*
 * Generate text autoregressively.
 * prompt: initial text (as C string)
 * max_tokens: number of tokens to generate
 * Returns newly allocated string. Caller must free.
 */
static char *generate_text(GPTModel *model, const char *prompt,
                           int max_tokens, float temperature, uint64_t *rng) {
    int prompt_len = (int)strlen(prompt);
    int total_len = prompt_len + max_tokens;
    if (total_len > MAX_SEQ_LEN) total_len = MAX_SEQ_LEN;
    max_tokens = total_len - prompt_len;

    int *tokens = (int *)malloc(total_len * sizeof(int));
    text_to_tokens(prompt, prompt_len, tokens);

    int cur_len = prompt_len;

    for (int i = 0; i < max_tokens; i++) {
        /* Forward through current sequence */
        Tensor *logits = gpt_forward(model, tokens, 1, cur_len);

        /* Sample from last position */
        int next = sample_token(&logits->data[(cur_len - 1) * VOCAB_SIZE],
                                VOCAB_SIZE, temperature, rng);
        tensor_free(logits);

        tokens[cur_len] = next;
        cur_len++;
    }

    /* Convert back to string */
    char *result = (char *)malloc(cur_len + 1);
    for (int i = 0; i < cur_len; i++) {
        int t = tokens[i];
        result[i] = (t >= 32 && t < 127) ? (char)t : '?';
    }
    result[cur_len] = '\0';

    free(tokens);
    return result;
}

/* ========================================================================
 * Full Training Run
 *
 * Returns: final validation perplexity, total wall-clock time
 * ======================================================================== */

typedef struct {
    float final_val_ppl;
    float final_val_bpb;     /* bits per byte */
    float final_val_loss;    /* raw CE loss (nats) */
    double total_time_sec;
    double ms_per_step;
    double tokens_per_sec;   /* training throughput */
    double tflops;           /* effective TFLOPS */
} TrainResult;

/*
 * Estimate FLOPs per training step (forward + backward).
 *
 * For a transformer with:
 *   - Attention: Q,K,V projections + output = 4 * 2 * dim^2 per layer
 *   - FFN: 2 * 2 * dim * hidden_dim per layer
 *   - Output head: 2 * dim * vocab_size
 *
 * Forward FLOPs per token:
 *   per_layer = 2*dim*(4*dim + 2*hidden_dim)
 *   total = n_layers * per_layer + 2*dim*vocab_size
 *
 * Backward ≈ 2x forward, so total ≈ 3x forward.
 * We count per step = seq_len tokens.
 */
static double estimate_flops_per_step(void) {
    double per_layer = 2.0 * DIM * (4.0 * DIM + 2.0 * HIDDEN_DIM);
    double fwd_per_token = N_LAYERS * per_layer + 2.0 * DIM * VOCAB_SIZE;
    double fwd_bwd_per_token = 3.0 * fwd_per_token;
    return fwd_bwd_per_token * SEQ_LEN * BATCH_SIZE;
}

static TrainResult train_model(const char *name, GPTModel *model,
                               const int *train_data, int train_len,
                               const int *val_data, int val_len,
                               uint64_t *rng, FILE *csv) {
    TrainResult result = {0};

    Adam *opt = adam_create(LR, 0.9f, 0.999f, 1e-8f, WEIGHT_DECAY);
    gpt_register_params(model, opt);

    printf("\n--- Training: %s ---\n", name);
    printf("Steps: %d, seq_len: %d, lr: %.4f\n", N_STEPS, SEQ_LEN, LR);

    double t_start = timer_sec();
    float smooth_loss = 0.0f;

    for (int step = 0; step < N_STEPS; step++) {
        double step_t0 = timer_sec();
        float loss = train_step(model, opt, train_data, train_len, rng);
        double step_time = timer_sec() - step_t0;

        /* Exponential moving average of loss */
        if (step == 0) smooth_loss = loss;
        else smooth_loss = 0.95f * smooth_loss + 0.05f * loss;

        if (step % EVAL_EVERY == 0 || step == N_STEPS - 1) {
            EvalResult eval = evaluate(model, val_data, val_len);
            double tok_per_sec = (double)(SEQ_LEN * BATCH_SIZE) / step_time;
            printf("  Step %4d/%d: loss=%.4f (smooth=%.4f), "
                   "val_ppl=%.2f, bpb=%.3f, "
                   "%.1f ms/step, %.0f tok/s\n",
                   step, N_STEPS, loss, smooth_loss,
                   eval.ppl, eval.bpb,
                   step_time * 1000.0, tok_per_sec);

            /* Log to CSV */
            if (csv) {
                double elapsed = timer_sec() - t_start;
                long tokens_seen = (long)(step + 1) * SEQ_LEN * BATCH_SIZE;
                fprintf(csv, "%s,%d,%ld,%.4f,%.4f,%.4f,%.3f,%.1f,%.0f,%.1f\n",
                        name, step, tokens_seen,
                        loss, smooth_loss,
                        eval.ppl, eval.bpb,
                        step_time * 1000.0, tok_per_sec, elapsed);
                fflush(csv);
            }
        }

        if (step > 0 && step % GEN_EVERY == 0) {
            uint64_t gen_rng[4];
            rng_seed(gen_rng, 12345);
            char *sample = generate_text(model, "The ", GEN_LEN, GEN_TEMP, gen_rng);
            printf("  [Sample] %s\n", sample);
            free(sample);
        }
    }

    double total_time = timer_sec() - t_start;
    result.total_time_sec = total_time;
    result.ms_per_step = (total_time / N_STEPS) * 1000.0;
    result.tokens_per_sec = (double)(SEQ_LEN * BATCH_SIZE) / (result.ms_per_step / 1000.0);
    result.tflops = estimate_flops_per_step() / (result.ms_per_step / 1000.0) / 1e12;

    EvalResult final_eval = evaluate(model, val_data, val_len);
    result.final_val_ppl = final_eval.ppl;
    result.final_val_bpb = final_eval.bpb;
    result.final_val_loss = final_eval.loss;

    printf("\n  Training complete: %.1f sec (%.1f ms/step)\n",
           total_time, result.ms_per_step);
    printf("  Final val loss: %.4f nats\n", result.final_val_loss);
    printf("  Final val perplexity: %.2f\n", result.final_val_ppl);
    printf("  Final val BPB: %.3f\n", result.final_val_bpb);
    printf("  Throughput: %.0f tok/s\n", result.tokens_per_sec);
    printf("  Effective TFLOPS: %.4f\n", result.tflops);

    /* Generate final samples */
    const char *prompts[] = {"The ", "KING:\n", "To be or not"};
    int n_prompts = 3;
    printf("\n  --- Generated Samples (%s) ---\n", name);
    for (int p = 0; p < n_prompts; p++) {
        uint64_t gen_rng[4];
        rng_seed(gen_rng, 42 + p);
        char *sample = generate_text(model, prompts[p], GEN_LEN, GEN_TEMP, gen_rng);
        printf("  [Prompt: \"%s\"]\n  %s\n\n", prompts[p], sample);
        free(sample);
    }

    adam_free(opt);
    return result;
}

/* ========================================================================
 * Main
 * ======================================================================== */

int main(int argc, char **argv) {
    (void)argc; (void)argv;

    /* Line-buffer stdout so progress prints appear when piped */
    setvbuf(stdout, NULL, _IOLBF, 0);

    printf("========================================\n");
    printf("QAT-CPU End-to-End Training\n");
    printf("========================================\n");

    /* CPU detection */
    CpuFeatures cpu;
    cpu_detect(&cpu);
    cpu_features_print(&cpu);

    KernelDispatch kd;
    kernel_dispatch_init(&kd, &cpu);
    kernel_dispatch_print(&kd);

    /* Load data */
    int text_len;
    char *text = load_text_file("shakespeare.txt", &text_len);
    if (!text) {
        fprintf(stderr, "Failed to load shakespeare.txt\n");
        return 1;
    }
    printf("\nData: %d chars loaded\n", text_len);

    /* Convert to tokens */
    int *tokens = (int *)malloc(text_len * sizeof(int));
    text_to_tokens(text, text_len, tokens);
    free(text);

    /* Train/val split: 90/10 */
    int train_len = text_len * 9 / 10;
    int val_len = text_len - train_len;
    int *train_data = tokens;
    int *val_data = tokens + train_len;
    printf("Train: %d tokens, Val: %d tokens\n", train_len, val_len);

    /* ---- Model info ---- */
    uint64_t rng_tmp[4];
    rng_seed(rng_tmp, 42);
    GPTModel *tmp = gpt_create(&kd, rng_tmp);
    int n_params = gpt_count_params(tmp);
    double flops_per_step = estimate_flops_per_step();
    printf("\nModel: %d layers, dim=%d, heads=%d, hidden=%d\n",
           N_LAYERS, DIM, N_HEADS, HIDDEN_DIM);
    printf("Batch: %d seqs x %d tokens = %d tokens/step\n",
           BATCH_SIZE, SEQ_LEN, BATCH_SIZE * SEQ_LEN);
    printf("Parameters: %d (%.1fK, %.2fM)\n",
           n_params, n_params / 1e3, n_params / 1e6);
    printf("Est. FLOPs/step: %.2fM (fwd+bwd, %d tokens)\n",
           flops_per_step / 1e6, BATCH_SIZE * SEQ_LEN);
    printf("Random baseline: ppl=%.0f, bpb=%.2f\n",
           (float)VOCAB_SIZE, logf((float)VOCAB_SIZE) / logf(2.0f));
    gpt_free(tmp);

    /* ---- Open CSV log ---- */
    FILE *csv = fopen("eval_log.csv", "w");
    if (csv) {
        fprintf(csv, "mode,step,tokens_seen,loss,smooth_loss,val_ppl,bpb,ms_per_step,tok_per_sec,elapsed_sec\n");
        fflush(csv);
    }

    /* ---- Train FP32 baseline ---- */
    uint64_t rng_fp32[4];
    rng_seed(rng_fp32, 42);
    GPTModel *model_fp32 = gpt_create(&kd, rng_fp32);
    gpt_set_qat(model_fp32, false);

    uint64_t train_rng_fp32[4];
    rng_seed(train_rng_fp32, 123);
    TrainResult res_fp32 = train_model("FP32", model_fp32,
                                        train_data, train_len,
                                        val_data, val_len,
                                        train_rng_fp32, csv);

    /* ---- Train QAT (INT8 forward, FP32 backward) ---- */
    uint64_t rng_qat[4];
    rng_seed(rng_qat, 42);  /* Same seed for same init */
    GPTModel *model_qat = gpt_create(&kd, rng_qat);
    gpt_set_qat(model_qat, true);

    uint64_t train_rng_qat[4];
    rng_seed(train_rng_qat, 123);  /* Same data order */
    TrainResult res_qat = train_model("QAT (INT8 fwd, FP32 bwd)", model_qat,
                                       train_data, train_len,
                                       val_data, val_len,
                                       train_rng_qat, csv);

    /* ---- Train QAT with INT8 backward ---- */
    uint64_t rng_qat2[4];
    rng_seed(rng_qat2, 42);
    GPTModel *model_qat2 = gpt_create(&kd, rng_qat2);
    gpt_set_qat(model_qat2, true);
    gpt_set_int8_backward(model_qat2, true);

    uint64_t train_rng_qat2[4];
    rng_seed(train_rng_qat2, 123);
    TrainResult res_qat2 = train_model("QAT (INT8 fwd+bwd)", model_qat2,
                                        train_data, train_len,
                                        val_data, val_len,
                                        train_rng_qat2, csv);

    if (csv) fclose(csv);

    /* ---- Comparison ---- */
    printf("\n========================================\n");
    printf("COMPARISON\n");
    printf("========================================\n");
    printf("%-25s %10s %10s %12s\n", "", "FP32", "QAT", "QAT+INT8bwd");
    printf("--- Quality ---\n");
    printf("%-25s %10.4f %10.4f %12.4f\n", "Val Loss (nats):",
           res_fp32.final_val_loss, res_qat.final_val_loss, res_qat2.final_val_loss);
    printf("%-25s %10.2f %10.2f %12.2f\n", "Val Perplexity:",
           res_fp32.final_val_ppl, res_qat.final_val_ppl, res_qat2.final_val_ppl);
    printf("%-25s %10.3f %10.3f %12.3f\n", "Val BPB:",
           res_fp32.final_val_bpb, res_qat.final_val_bpb, res_qat2.final_val_bpb);
    printf("--- Speed ---\n");
    printf("%-25s %10.1f %10.1f %12.1f\n", "Total Time (sec):",
           res_fp32.total_time_sec, res_qat.total_time_sec, res_qat2.total_time_sec);
    printf("%-25s %10.1f %10.1f %12.1f\n", "ms/step:",
           res_fp32.ms_per_step, res_qat.ms_per_step, res_qat2.ms_per_step);
    printf("%-25s %10.0f %10.0f %12.0f\n", "Tokens/sec:",
           res_fp32.tokens_per_sec, res_qat.tokens_per_sec, res_qat2.tokens_per_sec);
    printf("%-25s %10.4f %10.4f %12.4f\n", "Effective TFLOPS:",
           res_fp32.tflops, res_qat.tflops, res_qat2.tflops);

    float ppl_ratio = res_qat.final_val_ppl / res_fp32.final_val_ppl;
    float bpb_delta = res_qat.final_val_bpb - res_fp32.final_val_bpb;
    float speedup = res_fp32.total_time_sec / res_qat.total_time_sec;

    float ppl_ratio2 = res_qat2.final_val_ppl / res_fp32.final_val_ppl;
    float bpb_delta2 = res_qat2.final_val_bpb - res_fp32.final_val_bpb;
    float speedup2 = res_fp32.total_time_sec / res_qat2.total_time_sec;

    printf("\n--- Summary ---\n");
    printf("QAT (fwd only):\n");
    printf("  Perplexity ratio:  %.3f\n", ppl_ratio);
    printf("  BPB delta:         %+.3f bits/byte\n", bpb_delta);
    printf("  Speedup:           %.2fx\n", speedup);
    printf("QAT (fwd+bwd INT8):\n");
    printf("  Perplexity ratio:  %.3f\n", ppl_ratio2);
    printf("  BPB delta:         %+.3f bits/byte\n", bpb_delta2);
    printf("  Speedup:           %.2fx\n", speedup2);

    /* Cleanup */
    gpt_free(model_fp32);
    gpt_free(model_qat);
    gpt_free(model_qat2);
    free(tokens);

    return 0;
}
