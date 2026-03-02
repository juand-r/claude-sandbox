# Tokenization Strategy Comparison Experiment

## Goal

Compare 5 tokenization strategies for character-level LLM training, measuring
BPC (bits per character) as the primary metric. All configs see the same
number of **characters** of context; the token sequence length varies.

## Configurations

| # | Mode    | Vocab  | Tok/Char | SEQ_LEN (tokens) | Random BPC (naive) |
|---|---------|--------|----------|-------------------|--------------------|
| 0 | Binary  | 2      | 7        | 896               | 7.0                |
| 1 | Base-4  | 4      | 4        | 512               | 8.0*               |
| 2 | Nibble  | 16     | 2        | 256               | 8.0*               |
| 3 | Char    | 128    | 1        | 128               | 7.0                |
| 4 | Bigram  | 16384  | 0.5      | 64                | 7.0                |

*Base-4 and nibble use 8 bits (4×2, 2×4) to encode 7-bit ASCII, wasting 1 bit.
The model must learn that certain digit positions have restricted range.

## Encoding Details

- **Binary**: 7 bits MSB-first per character. Token ∈ {0,1}.
- **Base-4**: 4 digits of 2 bits each from the byte. Token ∈ {0,1,2,3}.
- **Nibble**: High nibble, low nibble. Token ∈ {0..15}.
- **Character**: Direct ASCII value. Token ∈ {0..127}. (Baseline.)
- **Bigram**: Pair of consecutive chars → c1*128 + c2. Token ∈ {0..16383}.

## BPC Calculation

BPC = mean_CE_per_token (nats) × tokens_per_char / ln(2)

Since 1 ASCII char = 1 byte, BPC = BPB for all configs.

## Model Architecture (constant across configs)

- DIM=128, N_LAYERS=4, N_HEADS=4, HIDDEN_DIM=512
- BATCH_SIZE=4, CHAR_CONTEXT=128 chars
- FP32 only (no QAT) to isolate the tokenization variable
- Adam optimizer, LR=3e-4 with warmup+cosine decay
- N_STEPS=3000, EVAL_EVERY=500

## Softmax Bottleneck Concern

When vocab_size > dim, the output logit matrix has rank ≤ dim, limiting
the model's ability to represent arbitrary distributions over the vocabulary.

- Binary (V=2, D=128): no bottleneck
- Char (V=128, D=128): borderline (rank 128 in 128-dim space)
- Bigram (V=16384, D=128): **severe bottleneck** (rank 128 in 16384-dim space)

This means bigram results are likely worse than their theoretical potential.
To fully remove the bottleneck, we'd need dim ≥ 16384, which is impractical.

## Should dim scale with vocab?

From information theory: representing V distinct tokens needs log2(V) dimensions.
But in practice, the transformer body (attention, FFN) is the bulk of the model.
Scaling dim with vocab would conflate two variables (tokenization vs capacity).

**Decision**: keep dim constant. Note the bottleneck as a known limitation.

## Expected Outcomes

- Character (baseline) should perform well — it's the natural granularity.
- Binary/base-4 have very long sequences → harder for attention (O(n²)),
  but each token carries less info → maybe easier per-token prediction.
- Bigram has short sequences → fast attention, but huge vocab → softmax bottleneck.
- The overhead of wasted bits in base-4/nibble (8 bits for 7) should be learned quickly.

## Compute Budget

Rough per-step time estimates at DIM=128, BATCH_SIZE=4:
- Binary (SEQ=896): ~0.5-1s/step → ~25-50 min total
- Base-4 (SEQ=512): ~0.2-0.5s → ~10-25 min
- Nibble (SEQ=256): ~0.05-0.1s → ~3-5 min
- Char (SEQ=128): ~0.02-0.05s → ~1-2 min
- Bigram (SEQ=64): ~0.1-0.3s (large output head) → ~5-15 min

Total: ~45-100 minutes for all 5 configs.

## Status

- [x] Implement train_tok.c
- [x] Build all 5 configs
- [x] Run experiments
- [x] Analyze results (see RESULTS.md)

## Actual Timings (measured)

- Binary (SEQ=896): 393ms/step, 1177s total
- Base-4 (SEQ=512): 181ms/step, 542s total
- Nibble (SEQ=256): 79ms/step, 238s total
- Char (SEQ=128): 51ms/step, 153s total
- Bigram (SEQ=64): 159ms/step, 477s total (large output GEMM dominates)

Total: ~2587s = ~43 minutes
