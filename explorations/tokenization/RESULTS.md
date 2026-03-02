# Tokenization Experiment Results

## Setup

- Model: DIM=128, N_LAYERS=4, N_HEADS=4, HIDDEN_DIM=512 (same body across all configs)
- Data: Shakespeare (~1.1M chars), 90/10 train/val split
- Training: 3000 steps, BATCH_SIZE=4, CHAR_CONTEXT=128 chars, FP32 only
- LR: 3e-4 with warmup(20)+cosine decay

## Results

| Mode    | Vocab  | Tok/Chr | SEQ_LEN | Params | BPC   | Loss (nats/tok) | PPL/tok | Time (s) |
|---------|--------|---------|---------|--------|-------|-----------------|---------|----------|
| Bigram  | 16384  | 0.5     | 64      | 5113K  | 2.771 | 3.841           | 46.57   | 477      |
| Char    | 128    | 1.0     | 128     | 951K   | 2.827 | 1.959           | 7.09    | 153      |
| Nibble  | 16     | 2.0     | 256     | 923K   | 3.040 | 1.054           | 2.87    | 238      |
| Base-4  | 4      | 4.0     | 512     | 920K   | 3.707 | 0.642           | 1.90    | 542      |
| Binary  | 2      | 7.0     | 896     | 919K   | 4.836 | 0.479           | 1.61    | 1177     |

Random baseline BPC: 7.0 for binary/char/bigram, 8.0 for base4/nibble (1 wasted bit).

## Analysis

### 1. Bigger tokens win on BPC

Clear monotonic trend: larger vocab (more info per token) → lower BPC.
Bigram (2.771) beats char (2.827) beats nibble (3.040) beats base4 (3.707) beats binary (4.836).

The ranking follows information density per token. With larger tokens, the model
processes more characters per attention position, enabling better long-range modeling
with the same O(n²) attention budget.

### 2. Binary is catastrophically bad

At BPC=4.836, binary is only 30% better than random (7.0). The generated text is
complete gibberish. The model must learn:
- Which 7-token groups form a character
- The bit patterns of common characters
- Character-level patterns (language model)
- All of this over 896-token sequences

With only 128 characters of actual context, spread over 896 positions, the attention
mechanism cannot effectively learn long-range character dependencies. Each attention
head processes 896×896 = 803K pairwise interactions, most of which are within-character
bit correlations rather than meaningful text patterns.

### 3. Bigram beats char despite softmax bottleneck

This is the most surprising result. The bigram model has:
- Severe softmax bottleneck: dim=128 but vocab=16384 (rank-128 logit matrix)
- 5.4x more parameters (5.1M vs 951K), mostly in embedding/output head
- Only 64 attention positions (vs 128 for char)

Yet it achieves better BPC. This suggests that:
- The shorter sequence (64 tokens) makes attention more effective per position
- Each token carrying 2 chars worth of information is very efficient
- The softmax bottleneck isn't as severe as feared at this training level
- The extra embedding parameters help compensate for the rank limitation

### 4. Per-token PPL is misleading across modes

Note the per-token PPL: binary=1.61, base4=1.90, nibble=2.87, char=7.09, bigram=46.57.
This makes binary look best and bigram worst! But per-token PPL is meaningless for
cross-mode comparison because the tokens carry different amounts of information.
BPC is the only fair metric.

### 5. Compute-quality tradeoff

| Mode    | BPC   | Time (s) | BPC × Time | Char/s |
|---------|-------|----------|------------|--------|
| Char    | 2.827 | 153      | 433        | ~10000 |
| Bigram  | 2.771 | 477      | 1321       | ~3200  |
| Nibble  | 3.040 | 238      | 723        | ~6400  |
| Base-4  | 3.707 | 542      | 2009       | ~3000  |
| Binary  | 4.836 | 1177     | 5694       | ~1300  |

Char is by far the best on compute-efficiency (BPC × Time product).
Bigram wins on raw BPC but is 3x slower (large output GEMM: 128→16384).

### 6. Memory/parameter analysis

The transformer body is identical across all configs (787K params).
The difference is entirely in embedding (vocab×dim) and output head (dim×vocab):

| Mode    | Body   | Embed  | Output | Total  | Embed+Output % |
|---------|--------|--------|--------|--------|----------------|
| Binary  | 787K   | 131K   | 0.3K   | 919K   | 14.3%          |
| Base-4  | 787K   | 132K   | 0.5K   | 920K   | 14.4%          |
| Nibble  | 787K   | 133K   | 2K     | 923K   | 14.7%          |
| Char    | 787K   | 147K   | 16K    | 951K   | 17.2%          |
| Bigram  | 787K   | 2228K  | 2097K  | 5113K  | 84.6%          |

Bigram's embedding+output head is 84.6% of total params. This is extreme.
If we could tie input/output embeddings, it would drop to ~2.2M/3.0M = 73%.

### 7. On the softmax bottleneck

For bigram: the logit matrix W_out ∈ R^{128×16384} has rank 128.
This means the model can only produce distributions that lie in a
128-dimensional subspace of the 16384-simplex. Despite this severe
limitation, bigram still achieves the best BPC.

Two possible explanations:
1. Natural language bigram distributions have low effective rank
   (most probability mass on a small number of likely bigrams)
2. At 3000 steps the model hasn't converged enough to hit the bottleneck

A follow-up experiment with larger dim (256+) would help distinguish these.

## Conclusions

1. **Token granularity matters enormously.** Going from char→binary (7x longer sequences)
   increases BPC by 71%. Going from char→bigram (2x shorter) improves BPC by 2%.

2. **Attention budget is key.** The fixed character context becomes a much longer token
   sequence for fine-grained tokenizations. Attention's O(n²) cost means the model
   wastes most of its capacity on within-character correlations rather than text patterns.

3. **Practical implication:** This supports the trend toward larger vocabularies (BPE, etc.)
   in modern LLMs. Packing more information per token is strictly better, up to the point
   where the softmax bottleneck or embedding overhead becomes prohibitive.

4. **For this model/data regime, character-level is the best efficiency tradeoff.**
   Bigram is slightly better on BPC but 3x more expensive and 5x more parameters.

## Follow-up Ideas

- [ ] Run bigram with larger dim (256, 512) to test softmax bottleneck limits
- [ ] Try BPE tokenization as a 6th config
- [ ] Test with more training steps (binary might eventually converge)
- [ ] Tie input/output embeddings for bigram (halve embedding params)
- [ ] Try intermediate token sizes: trigram, 4-gram
