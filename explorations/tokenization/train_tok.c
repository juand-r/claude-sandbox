/*
 * train_tok.c - Tokenization strategy comparison experiment
 *
 * Compares 5 tokenization strategies for character-level LLM training:
 *   0: Binary  (vocab=2,     7 tokens/char)
 *   1: Base-4  (vocab=4,     4 tokens/char)
 *   2: Nibble  (vocab=16,    2 tokens/char)
 *   3: Char    (vocab=128,   1 token/char)  [baseline]
 *   4: Bigram  (vocab=16384, 0.5 tokens/char)
 *
 * Key constraint: character context is fixed across all configs.
 * Token sequence length varies: SEQ_LEN = CHAR_CONTEXT * tokens_per_char.
 *
 * Primary metric: BPC (bits per character).
 *   BPC = mean_CE_per_token * tokens_per_char / ln(2)
 *
 * Compile with -DTOKENIZE_MODE=N to select mode (default: 3=char).
 */

#include "qat_cpu.h"
#include <assert.h>

/* ========================================================================
 * Tokenization Configuration
 * ======================================================================== */

#ifndef TOKENIZE_MODE
#define TOKENIZE_MODE 3
#endif

#if TOKENIZE_MODE == 0
  #define VOCAB_SIZE 2
  #define TOKENS_PER_CHAR_INT 7
  #define TOKENS_PER_CHAR_F 7.0f
  #define MODE_NAME "binary"
#elif TOKENIZE_MODE == 1
  #define VOCAB_SIZE 4
  #define TOKENS_PER_CHAR_INT 4
  #define TOKENS_PER_CHAR_F 4.0f
  #define MODE_NAME "base4"
#elif TOKENIZE_MODE == 2
  #define VOCAB_SIZE 16
  #define TOKENS_PER_CHAR_INT 2
  #define TOKENS_PER_CHAR_F 2.0f
  #define MODE_NAME "nibble"
#elif TOKENIZE_MODE == 3
  #define VOCAB_SIZE 128
  #define TOKENS_PER_CHAR_INT 1
  #define TOKENS_PER_CHAR_F 1.0f
  #define MODE_NAME "char"
#elif TOKENIZE_MODE == 4
  #define VOCAB_SIZE 16384
  #define TOKENS_PER_CHAR_F 0.5f
  #define MODE_NAME "bigram"
#else
  #error "TOKENIZE_MODE must be 0-4"
#endif

/* ========================================================================
 * Model Configuration
 * ======================================================================== */

#ifndef CHAR_CONTEXT
#define CHAR_CONTEXT  128       /* Characters of context (fixed across configs) */
#endif

/* Token sequence length (derived from char context) */
#if TOKENIZE_MODE == 4
  #define SEQ_LEN     (CHAR_CONTEXT / 2)
#else
  #define SEQ_LEN     (CHAR_CONTEXT * TOKENS_PER_CHAR_INT)
#endif

#ifndef DIM
#define DIM           128
#endif
#ifndef N_LAYERS
#define N_LAYERS      4
#endif
#ifndef N_HEADS
#define N_HEADS       4
#endif
#ifndef HIDDEN_DIM
#define HIDDEN_DIM    512
#endif
#define MAX_SEQ_LEN   1024      /* Must be >= max SEQ_LEN (binary: 896) */
#ifndef BATCH_SIZE
#define BATCH_SIZE    4
#endif
#ifndef N_STEPS
#define N_STEPS       3000
#endif
#ifndef EVAL_EVERY
#define EVAL_EVERY    500
#endif
#define GEN_EVERY     1500
#define GEN_CHARS     100       /* Characters to generate */
#ifndef LR
#define LR            3e-4f
#endif
#define WEIGHT_DECAY  0.01f
#ifndef LR_WARMUP
#define LR_WARMUP     20
#endif
#define LR_MIN        (LR * 0.1f)
#define GEN_TEMP      0.8f

/* GEN_LEN in tokens */
#if TOKENIZE_MODE == 4
  #define GEN_LEN_TOKENS (GEN_CHARS / 2)
#else
  #define GEN_LEN_TOKENS (GEN_CHARS * TOKENS_PER_CHAR_INT)
#endif

#define STR_HELPER(x) #x
#define STR(x) STR_HELPER(x)

/* ========================================================================
 * Tokenization Functions
 * ======================================================================== */

/*
 * Encode text into tokens. Returns number of tokens written.
 * Caller must ensure tokens[] has enough space (text_len * 7 worst case).
 */
static int encode_text(const char *text, int text_len, int *tokens) {
#if TOKENIZE_MODE == 0  /* Binary: 7 bits MSB-first per char */
    for (int i = 0; i < text_len; i++) {
        int c = (unsigned char)text[i] & 0x7F;
        for (int b = 0; b < 7; b++) {
            tokens[i * 7 + b] = (c >> (6 - b)) & 1;
        }
    }
    return text_len * 7;

#elif TOKENIZE_MODE == 1  /* Base-4: 4 digits of 2 bits each */
    for (int i = 0; i < text_len; i++) {
        int c = (unsigned char)text[i] & 0x7F;
        tokens[i*4 + 0] = (c >> 6) & 3;
        tokens[i*4 + 1] = (c >> 4) & 3;
        tokens[i*4 + 2] = (c >> 2) & 3;
        tokens[i*4 + 3] = c & 3;
    }
    return text_len * 4;

#elif TOKENIZE_MODE == 2  /* Nibble: high nibble, low nibble */
    for (int i = 0; i < text_len; i++) {
        int c = (unsigned char)text[i] & 0x7F;
        tokens[i*2 + 0] = (c >> 4) & 0xF;
        tokens[i*2 + 1] = c & 0xF;
    }
    return text_len * 2;

#elif TOKENIZE_MODE == 3  /* Character: direct ASCII */
    for (int i = 0; i < text_len; i++) {
        tokens[i] = (unsigned char)text[i] & 0x7F;
    }
    return text_len;

#elif TOKENIZE_MODE == 4  /* Bigram: pair of chars -> c1*128 + c2 */
    int n = text_len / 2;
    for (int i = 0; i < n; i++) {
        int c1 = (unsigned char)text[2*i] & 0x7F;
        int c2 = (unsigned char)text[2*i + 1] & 0x7F;
        tokens[i] = c1 * 128 + c2;
    }
    return n;
#endif
}

/*
 * Decode tokens back to text. Returns number of chars written (excl NUL).
 * Non-printable chars become '?'.
 */
static int decode_tokens(const int *tokens, int n_tokens, char *text, int max_len) {
    int pos = 0;

#if TOKENIZE_MODE == 0  /* Binary */
    int n_chars = n_tokens / 7;
    for (int i = 0; i < n_chars && pos < max_len - 1; i++) {
        int c = 0;
        for (int b = 0; b < 7; b++)
            c = (c << 1) | (tokens[i*7 + b] & 1);
        text[pos++] = (c >= 32 && c < 127) ? (char)c : '?';
    }

#elif TOKENIZE_MODE == 1  /* Base-4 */
    int n_chars = n_tokens / 4;
    for (int i = 0; i < n_chars && pos < max_len - 1; i++) {
        int c = ((tokens[i*4+0] & 3) << 6) | ((tokens[i*4+1] & 3) << 4) |
                ((tokens[i*4+2] & 3) << 2) | (tokens[i*4+3] & 3);
        text[pos++] = (c >= 32 && c < 127) ? (char)c : '?';
    }

#elif TOKENIZE_MODE == 2  /* Nibble */
    int n_chars = n_tokens / 2;
    for (int i = 0; i < n_chars && pos < max_len - 1; i++) {
        int c = ((tokens[i*2] & 0xF) << 4) | (tokens[i*2+1] & 0xF);
        text[pos++] = (c >= 32 && c < 127) ? (char)c : '?';
    }

#elif TOKENIZE_MODE == 3  /* Character */
    for (int i = 0; i < n_tokens && pos < max_len - 1; i++) {
        int c = tokens[i];
        text[pos++] = (c >= 32 && c < 127) ? (char)c : '?';
    }

#elif TOKENIZE_MODE == 4  /* Bigram */
    for (int i = 0; i < n_tokens && pos + 1 < max_len - 1; i++) {
        int t = tokens[i];
        int c1 = t / 128;
        int c2 = t % 128;
        text[pos++] = (c1 >= 32 && c1 < 127) ? (char)c1 : '?';
        text[pos++] = (c2 >= 32 && c2 < 127) ? (char)c2 : '?';
    }
#endif

    text[pos] = '\0';
    return pos;
}

/* BPC from mean CE loss per token (nats) */
static float loss_to_bpc(float mean_ce_nats) {
    return mean_ce_nats * TOKENS_PER_CHAR_F / logf(2.0f);
}

/* Random baseline BPC (uniform over vocab at each position) */
static float random_baseline_bpc(void) {
    return logf((float)VOCAB_SIZE) * TOKENS_PER_CHAR_F / logf(2.0f);
}

/* ========================================================================
 * GPT Model (same architecture as qat-cpu/train.c, FP32 only)
 * ======================================================================== */

typedef struct {
    int vocab_size;
    int dim;
    int n_layers;
    int n_heads;
    int hidden_dim;
    int max_seq_len;

    Tensor *token_emb;          /* [vocab_size x dim] */
    Tensor *pos_emb;            /* [max_seq_len x dim] */
    Tensor *grad_token_emb;
    Tensor *grad_pos_emb;

    TransformerBlock **blocks;

    RMSNorm   *final_norm;
    QATLinear *output_head;     /* [dim x vocab_size] */

    const KernelDispatch *kernels;

    int   *saved_tokens;
    int    saved_batch_size;
    int    saved_seq_len;
    Tensor *saved_embed;
} GPTModel;

static GPTModel *gpt_create(const KernelDispatch *kd, uint64_t *rng) {
    GPTModel *m = (GPTModel *)calloc(1, sizeof(GPTModel));

    m->vocab_size   = VOCAB_SIZE;
    m->dim          = DIM;
    m->n_layers     = N_LAYERS;
    m->n_heads      = N_HEADS;
    m->hidden_dim   = HIDDEN_DIM;
    m->max_seq_len  = MAX_SEQ_LEN;
    m->kernels      = kd;

    m->token_emb = tensor_create(VOCAB_SIZE, DIM);
    tensor_rand(m->token_emb, -0.02f, 0.02f, rng);
    m->pos_emb = tensor_create(MAX_SEQ_LEN, DIM);
    tensor_rand(m->pos_emb, -0.02f, 0.02f, rng);
    m->grad_token_emb = tensor_zeros(VOCAB_SIZE, DIM);
    m->grad_pos_emb = tensor_zeros(MAX_SEQ_LEN, DIM);

    m->blocks = (TransformerBlock **)calloc(N_LAYERS, sizeof(TransformerBlock *));
    for (int i = 0; i < N_LAYERS; i++) {
        m->blocks[i] = transformer_block_create(DIM, HIDDEN_DIM, N_HEADS,
                                                 false, kd, rng);
        m->blocks[i]->attn->causal = true;
    }

    m->final_norm = rmsnorm_create(DIM, 1e-5f);
    m->output_head = qat_linear_create(DIM, VOCAB_SIZE, false, kd, rng);

    /* Ensure FP32 mode (no QAT) */
    for (int i = 0; i < N_LAYERS; i++) {
        TransformerBlock *b = m->blocks[i];
        b->attn->wq->use_qat = false;
        b->attn->wk->use_qat = false;
        b->attn->wv->use_qat = false;
        b->attn->wo->use_qat = false;
        b->ffn_up->use_qat = false;
        b->ffn_down->use_qat = false;
    }
    m->output_head->use_qat = false;

    m->saved_tokens = NULL;
    return m;
}

static void gpt_free(GPTModel *m) {
    if (!m) return;
    tensor_free(m->token_emb);
    tensor_free(m->pos_emb);
    tensor_free(m->grad_token_emb);
    tensor_free(m->grad_pos_emb);
    for (int i = 0; i < m->n_layers; i++)
        transformer_block_free(m->blocks[i]);
    free(m->blocks);
    rmsnorm_free(m->final_norm);
    qat_linear_free(m->output_head);
    free(m->saved_tokens);
    tensor_free(m->saved_embed);
    free(m);
}

static Tensor *gpt_forward(GPTModel *m, const int *tokens,
                            int batch_size, int seq_len) {
    assert(seq_len <= m->max_seq_len);
    int total_tokens = batch_size * seq_len;

    if (m->saved_tokens) free(m->saved_tokens);
    m->saved_tokens = (int *)malloc(total_tokens * sizeof(int));
    memcpy(m->saved_tokens, tokens, total_tokens * sizeof(int));
    m->saved_batch_size = batch_size;
    m->saved_seq_len = seq_len;

    Tensor *x = tensor_create(total_tokens, m->dim);
    for (int b = 0; b < batch_size; b++) {
        for (int s = 0; s < seq_len; s++) {
            int idx = b * seq_len + s;
            int tok = tokens[idx];
            if (tok < 0 || tok >= m->vocab_size) tok = 0;
            for (int d = 0; d < m->dim; d++) {
                x->data[idx * m->dim + d] =
                    m->token_emb->data[tok * m->dim + d] +
                    m->pos_emb->data[s * m->dim + d];
            }
        }
    }

    if (m->saved_embed) tensor_free(m->saved_embed);
    m->saved_embed = tensor_create(total_tokens, m->dim);
    tensor_copy(m->saved_embed, x);

    for (int i = 0; i < m->n_layers; i++) {
        Tensor *next = transformer_block_forward(m->blocks[i], x,
                                                  batch_size, seq_len);
        tensor_free(x);
        x = next;
    }

    Tensor *normed = rmsnorm_forward(m->final_norm, x);
    tensor_free(x);

    Tensor *logits = qat_linear_forward(m->output_head, normed);
    tensor_free(normed);

    return logits;
}

static void gpt_backward(GPTModel *m, const Tensor *grad_logits) {
    int batch_size = m->saved_batch_size;
    int seq_len = m->saved_seq_len;

    Tensor *grad = qat_linear_backward(m->output_head, grad_logits);
    Tensor *grad2 = rmsnorm_backward(m->final_norm, grad);
    tensor_free(grad);

    for (int i = m->n_layers - 1; i >= 0; i--) {
        Tensor *prev = transformer_block_backward(m->blocks[i], grad2,
                                                   batch_size, seq_len);
        tensor_free(grad2);
        grad2 = prev;
    }

    for (int b = 0; b < batch_size; b++) {
        for (int s = 0; s < seq_len; s++) {
            int idx = b * seq_len + s;
            int tok = m->saved_tokens[idx];
            if (tok < 0 || tok >= m->vocab_size) tok = 0;
            for (int d = 0; d < m->dim; d++) {
                m->grad_token_emb->data[tok * m->dim + d] +=
                    grad2->data[idx * m->dim + d];
                m->grad_pos_emb->data[s * m->dim + d] +=
                    grad2->data[idx * m->dim + d];
            }
        }
    }

    tensor_free(grad2);
}

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
    for (int i = 0; i < m->n_layers; i++)
        transformer_block_zero_grad(m->blocks[i]);
    rmsnorm_zero_grad(m->final_norm);
    qat_linear_zero_grad(m->output_head);
}

static void gpt_register_params(GPTModel *m, Adam *opt) {
    adam_add_param(opt, m->token_emb->data, m->grad_token_emb->data,
                   tensor_numel(m->token_emb));
    adam_add_param(opt, m->pos_emb->data, m->grad_pos_emb->data,
                   tensor_numel(m->pos_emb));

    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        QATLinear *linears[] = {b->attn->wq, b->attn->wk, b->attn->wv,
                                b->attn->wo, b->ffn_up, b->ffn_down};
        for (int j = 0; j < 6; j++) {
            adam_add_param(opt, linears[j]->weight->data,
                           linears[j]->grad_weight->data,
                           tensor_numel(linears[j]->weight));
        }
        adam_add_param(opt, b->norm1->weight->data, b->norm1->grad_weight->data,
                       tensor_numel(b->norm1->weight));
        adam_add_param(opt, b->norm2->weight->data, b->norm2->grad_weight->data,
                       tensor_numel(b->norm2->weight));
    }

    adam_add_param(opt, m->final_norm->weight->data,
                   m->final_norm->grad_weight->data,
                   tensor_numel(m->final_norm->weight));
    adam_add_param(opt, m->output_head->weight->data,
                   m->output_head->grad_weight->data,
                   tensor_numel(m->output_head->weight));
}

static int gpt_count_params(GPTModel *m) {
    int total = 0;
    total += tensor_numel(m->token_emb);
    total += tensor_numel(m->pos_emb);
    for (int i = 0; i < m->n_layers; i++) {
        TransformerBlock *b = m->blocks[i];
        QATLinear *linears[] = {b->attn->wq, b->attn->wk, b->attn->wv,
                                b->attn->wo, b->ffn_up, b->ffn_down};
        for (int j = 0; j < 6; j++)
            total += tensor_numel(linears[j]->weight);
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

/* ========================================================================
 * Training Step
 * ======================================================================== */

static float train_step(GPTModel *model, Adam *opt,
                        const int *data, int data_len,
                        uint64_t *rng) {
    int seq_len = SEQ_LEN;
    int batch_size = BATCH_SIZE;
    int total_tokens = batch_size * seq_len;

    int *input_tokens = (int *)malloc(total_tokens * sizeof(int));
    int *target_tokens = (int *)malloc(total_tokens * sizeof(int));

    for (int b = 0; b < batch_size; b++) {
        int start = (int)(rng_next(rng) % (data_len - seq_len - 1));
        memcpy(&input_tokens[b * seq_len], &data[start],
               seq_len * sizeof(int));
        memcpy(&target_tokens[b * seq_len], &data[start + 1],
               seq_len * sizeof(int));
    }

    gpt_zero_grad(model);
    adam_zero_grad(opt);

    Tensor *logits = gpt_forward(model, input_tokens, batch_size, seq_len);

    float *grad_logits = (float *)qat_calloc(total_tokens * VOCAB_SIZE * sizeof(float));
    float loss = cross_entropy_loss(logits->data, target_tokens,
                                     total_tokens, VOCAB_SIZE, grad_logits);

    Tensor *grad_tensor = tensor_wrap(grad_logits, total_tokens, VOCAB_SIZE);
    gpt_backward(model, grad_tensor);
    free(grad_tensor);

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

typedef struct {
    float loss;   /* mean CE per token (nats) */
    float bpc;    /* bits per character */
    float ppl;    /* perplexity per token */
} EvalResult;

static EvalResult evaluate(GPTModel *model, const int *data, int data_len) {
    EvalResult r = {0};
    int seq_len = SEQ_LEN;
    int n_seqs = data_len / (seq_len + 1);
    if (n_seqs > 50) n_seqs = 50;
    if (n_seqs == 0) { r.bpc = 99.0f; r.ppl = 999.0f; return r; }

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
    r.bpc = loss_to_bpc(r.loss);
    r.ppl = expf(r.loss);
    return r;
}

/* ========================================================================
 * Text Generation
 * ======================================================================== */

static int sample_token(const float *logits, int vocab_size,
                        float temperature, uint64_t *rng) {
    if (temperature < 1e-6f) {
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

    float max_val = logits[0];
    for (int i = 1; i < vocab_size; i++)
        if (logits[i] > max_val) max_val = logits[i];

    float sum = 0.0f;
    float *probs = (float *)qat_alloc(vocab_size * sizeof(float));
    for (int i = 0; i < vocab_size; i++) {
        probs[i] = expf((logits[i] - max_val) / temperature);
        sum += probs[i];
    }

    float r = rng_uniform(rng) * sum;
    float cumsum = 0.0f;
    int token = vocab_size - 1;
    for (int i = 0; i < vocab_size; i++) {
        cumsum += probs[i];
        if (cumsum >= r) { token = i; break; }
    }

    qat_free(probs);
    return token;
}

/*
 * Generate text. Prompt given as a string.
 * Returns newly allocated string. Caller must free.
 */
static char *generate_text(GPTModel *model, const char *prompt,
                           int gen_chars, float temperature, uint64_t *rng) {
    int prompt_len = (int)strlen(prompt);

    /* Encode prompt to tokens */
    int *prompt_tokens = (int *)malloc(prompt_len * 8 * sizeof(int));
    int prompt_tok_len = encode_text(prompt, prompt_len, prompt_tokens);

    /* Compute how many tokens to generate */
#if TOKENIZE_MODE == 4
    int gen_tokens = gen_chars / 2;
#else
    int gen_tokens = gen_chars * TOKENS_PER_CHAR_INT;
#endif

    int total_tok_len = prompt_tok_len + gen_tokens;
    if (total_tok_len > MAX_SEQ_LEN)
        total_tok_len = MAX_SEQ_LEN;
    gen_tokens = total_tok_len - prompt_tok_len;
    if (gen_tokens <= 0) {
        free(prompt_tokens);
        char *r = (char *)malloc(1);
        r[0] = '\0';
        return r;
    }

    int *tokens = (int *)malloc(total_tok_len * sizeof(int));
    memcpy(tokens, prompt_tokens, prompt_tok_len * sizeof(int));
    free(prompt_tokens);

    int cur_len = prompt_tok_len;

    for (int i = 0; i < gen_tokens; i++) {
        Tensor *logits = gpt_forward(model, tokens, 1, cur_len);
        int next = sample_token(&logits->data[(cur_len - 1) * VOCAB_SIZE],
                                VOCAB_SIZE, temperature, rng);
        tensor_free(logits);
        tokens[cur_len] = next;
        cur_len++;
    }

    /* Decode to text */
    char *result = (char *)malloc(cur_len * 2 + 1);  /* worst case: bigram 2x */
    decode_tokens(tokens, cur_len, result, cur_len * 2 + 1);
    free(tokens);

    return result;
}

/* ========================================================================
 * LR Schedule
 * ======================================================================== */

static float get_lr(int step, int total_steps) {
    if (LR_WARMUP > 0 && step < LR_WARMUP)
        return LR * ((float)(step + 1) / (float)LR_WARMUP);
    if (total_steps <= LR_WARMUP) return LR;
    float progress = (float)(step - LR_WARMUP) / (float)(total_steps - LR_WARMUP);
    if (progress > 1.0f) progress = 1.0f;
    return LR_MIN + 0.5f * (LR - LR_MIN) * (1.0f + cosf(3.14159265f * progress));
}

/* ========================================================================
 * Full Training Run
 * ======================================================================== */

typedef struct {
    float final_bpc;
    float final_loss;
    float final_ppl;
    double total_time_sec;
    double ms_per_step;
} TrainResult;

static TrainResult train_run(GPTModel *model,
                             const int *train_data, int train_len,
                             const int *val_data, int val_len,
                             uint64_t *rng, FILE *csv) {
    TrainResult result = {0};

    Adam *opt = adam_create(LR, 0.9f, 0.999f, 1e-8f, WEIGHT_DECAY);
    gpt_register_params(model, opt);

    printf("Steps: %d, seq_len: %d tokens (%d chars), batch: %d, lr: %.6f\n",
           N_STEPS, SEQ_LEN, CHAR_CONTEXT, BATCH_SIZE, LR);

    double t_start = timer_sec();
    float smooth_loss = 0.0f;

    for (int step = 0; step < N_STEPS; step++) {
        opt->config.lr = get_lr(step, N_STEPS);

        double step_t0 = timer_sec();
        float loss = train_step(model, opt, train_data, train_len, rng);
        double step_time = timer_sec() - step_t0;

        if (step == 0) smooth_loss = loss;
        else smooth_loss = 0.95f * smooth_loss + 0.05f * loss;

        if (step % EVAL_EVERY == 0 || step == N_STEPS - 1) {
            EvalResult eval = evaluate(model, val_data, val_len);
            int chars_per_step = BATCH_SIZE * CHAR_CONTEXT;
            double chars_per_sec = (double)chars_per_step / step_time;

            printf("  Step %4d/%d: loss=%.4f smooth=%.4f | "
                   "val_bpc=%.3f val_loss=%.4f val_ppl=%.2f | "
                   "lr=%.6f %.1fms/step %.0f char/s\n",
                   step, N_STEPS, loss, smooth_loss,
                   eval.bpc, eval.loss, eval.ppl,
                   opt->config.lr,
                   step_time * 1000.0, chars_per_sec);

            if (csv) {
                double elapsed = timer_sec() - t_start;
                long chars_seen = (long)(step + 1) * BATCH_SIZE * CHAR_CONTEXT;
                fprintf(csv, "%s,%d,%ld,%.4f,%.4f,%.3f,%.4f,%.2f,%.1f,%.0f,%.1f,%.6f\n",
                        MODE_NAME, step, chars_seen,
                        loss, smooth_loss,
                        eval.bpc, eval.loss, eval.ppl,
                        step_time * 1000.0, chars_per_sec, elapsed,
                        opt->config.lr);
                fflush(csv);
            }
        }

        if (step > 0 && step % GEN_EVERY == 0) {
            uint64_t gen_rng[4];
            rng_seed(gen_rng, 12345);
            char *sample = generate_text(model, "The ", GEN_CHARS, GEN_TEMP, gen_rng);
            printf("  [Sample] %s\n", sample);
            free(sample);
        }
    }

    double total_time = timer_sec() - t_start;
    result.total_time_sec = total_time;
    result.ms_per_step = (total_time / N_STEPS) * 1000.0;

    EvalResult final_eval = evaluate(model, val_data, val_len);
    result.final_bpc = final_eval.bpc;
    result.final_loss = final_eval.loss;
    result.final_ppl = final_eval.ppl;

    printf("\nTraining complete: %.1f sec (%.1f ms/step)\n",
           total_time, result.ms_per_step);
    printf("Final val BPC:  %.3f\n", result.final_bpc);
    printf("Final val loss: %.4f nats/token\n", result.final_loss);
    printf("Final val PPL:  %.2f (per-token)\n", result.final_ppl);

    /* Generate final samples */
    const char *prompts[] = {"The ", "KING:\n", "To be"};
    printf("\n--- Generated Samples ---\n");
    for (int p = 0; p < 3; p++) {
        uint64_t gen_rng[4];
        rng_seed(gen_rng, 42 + p);
        char *sample = generate_text(model, prompts[p], GEN_CHARS, GEN_TEMP, gen_rng);
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

    setvbuf(stdout, NULL, _IOLBF, 0);

    printf("========================================\n");
    printf("Tokenization Experiment: %s\n", MODE_NAME);
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

    /* Split at character level: 90/10 */
    int train_char_len = text_len * 9 / 10;
#if TOKENIZE_MODE == 4
    /* Align to even for bigram */
    train_char_len &= ~1;
#endif
    int val_char_len = text_len - train_char_len;
#if TOKENIZE_MODE == 4
    val_char_len &= ~1;
#endif

    /* Encode each split */
    int *train_tokens = (int *)malloc(train_char_len * 8 * sizeof(int));
    int train_tok_len = encode_text(text, train_char_len, train_tokens);

    int *val_tokens = (int *)malloc(val_char_len * 8 * sizeof(int));
    int val_tok_len = encode_text(text + train_char_len, val_char_len, val_tokens);

    free(text);

    printf("Train: %d chars -> %d tokens (%.1f tok/char)\n",
           train_char_len, train_tok_len, (float)train_tok_len / train_char_len);
    printf("Val:   %d chars -> %d tokens\n", val_char_len, val_tok_len);

    /* Model info */
    uint64_t rng_tmp[4];
    rng_seed(rng_tmp, 42);
    GPTModel *model = gpt_create(&kd, rng_tmp);
    int n_params = gpt_count_params(model);
    gpt_free(model);

    int emb_params = VOCAB_SIZE * DIM + MAX_SEQ_LEN * DIM;
    int head_params = DIM * VOCAB_SIZE;

    printf("\nMode: %s (vocab=%d, seq_len=%d tokens, %d chars context)\n",
           MODE_NAME, VOCAB_SIZE, SEQ_LEN, CHAR_CONTEXT);
    printf("Model: %d layers, dim=%d, heads=%d, hidden=%d\n",
           N_LAYERS, DIM, N_HEADS, HIDDEN_DIM);
    printf("Parameters: %d (%.1fK)\n", n_params, n_params / 1e3);
    printf("  Embedding: %d (%.1fK) = %.1f%% of total\n",
           emb_params, emb_params / 1e3, 100.0 * emb_params / n_params);
    printf("  Output head: %d (%.1fK) = %.1f%% of total\n",
           head_params, head_params / 1e3, 100.0 * head_params / n_params);
    printf("  Transformer body: %d (%.1fK) = %.1f%% of total\n",
           n_params - emb_params - head_params,
           (n_params - emb_params - head_params) / 1e3,
           100.0 * (n_params - emb_params - head_params) / n_params);
    printf("Random baseline BPC: %.2f\n", random_baseline_bpc());
#if TOKENIZE_MODE == 4
    printf("NOTE: softmax bottleneck -- vocab=%d > dim=%d (rank limited)\n",
           VOCAB_SIZE, DIM);
#endif

    /* Open CSV log */
    char csv_filename[256];
    snprintf(csv_filename, sizeof(csv_filename), "%s.csv", MODE_NAME);
    FILE *csv = fopen(csv_filename, "w");
    if (csv) {
        fprintf(csv, "mode,step,chars_seen,loss,smooth_loss,"
                     "bpc,val_loss,val_ppl,"
                     "ms_per_step,chars_per_sec,elapsed_sec,lr\n");
        fflush(csv);
    }
    printf("CSV log: %s\n", csv_filename);

    /* Create model and train */
    uint64_t rng_model[4], rng_train[4];
    rng_seed(rng_model, 42);
    rng_seed(rng_train, 123);
    model = gpt_create(&kd, rng_model);

    printf("\n--- Training ---\n");
    TrainResult res = train_run(model, train_tokens, train_tok_len,
                                val_tokens, val_tok_len,
                                rng_train, csv);

    if (csv) fclose(csv);

    /* Print machine-readable summary line (for run_all.sh to collect) */
    printf("\nSUMMARY:%s,%d,%.1f,%d,%d,%.3f,%.4f,%.2f,%.1f,%.2f\n",
           MODE_NAME, VOCAB_SIZE, TOKENS_PER_CHAR_F, SEQ_LEN,
           n_params, res.final_bpc, res.final_loss, res.final_ppl,
           res.total_time_sec, random_baseline_bpc());

    gpt_free(model);
    free(train_tokens);
    free(val_tokens);

    return 0;
}
