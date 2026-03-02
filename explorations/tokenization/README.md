# Tokenization Strategy Comparison

Comparing 5 tokenization strategies for character-level LLM training on Shakespeare.
The key variable is how text characters are decomposed into model tokens.

## Configs

| Mode | Vocab | Tokens/Char | Token SEQ_LEN | Notes |
|------|-------|-------------|---------------|-------|
| Binary | 2 | 7 | 896 | Each char = 7 bits |
| Base-4 | 4 | 4 | 512 | Each char = 4 quaternary digits |
| Nibble | 16 | 2 | 256 | Each char = 2 hex digits |
| Char | 128 | 1 | 128 | Baseline (standard ASCII) |
| Bigram | 16384 | 0.5 | 64 | Each token = 2 chars |

All configs see 128 characters of context. The model architecture is identical
except for the embedding/output head dimensions (which scale with vocab size).

## How to run

```bash
# Build and run all 5 configs
bash run_all.sh

# Or build and run individually
make train_tok_char
./train_tok_char

# Override hyperparams
make train_tok_char TRAIN_CFLAGS="-DDIM=256 -DN_STEPS=5000"
```

## Metrics

- **BPC** (bits per character): primary comparison metric, normalizes across tokenizations
- **Loss**: cross-entropy in nats per token (NOT comparable across configs)
- **PPL**: exp(loss), per-token perplexity (NOT comparable across configs)

See PLAN.md for more details on experimental design.
