# Factored Embedding Dimension Analysis

## Architecture

The transformer body stays at `d_model` throughout. The projections are cheap linear layers.

## Input Side (d_in)

For `V=2`, `log2(V)=1`, and a 1-dim embedding is actually fine mathematically — it's just two points on a line, projected to `d_model`. The effective embedding matrix `V × d_model` is rank 1. That captures "these two tokens are different" in one direction.

But you might want `d_in=8` or so to give the projection more degrees of freedom — the model might benefit from encoding positional context (e.g., "this is bit 3 of a character") differently for 0 vs 1.

A heuristic like `d_in = max(8, 4 * ceil(log2(V)))` seems reasonable:

| Mode    | V     | d_in |
|---------|-------|------|
| Binary  | 2     | 8    |
| Base-4  | 4     | 8    |
| Nibble  | 16    | 16   |
| Char    | 128   | 28   |
| Bigram  | 16384 | 56   |

## Output Side (d_out)

This is the harder question. You're asking: what is the effective rank of the conditional next-token distribution matrix? There's no clean formula, but there are ways to find out:

1. **SVD of trained output weights:** Train with large `d_out`, then look at the singular value spectrum of the output weight matrix. Where it drops off tells you the effective rank.

2. **Sweep d_out and find the knee:** Run bigram with `d_out ∈ {16, 32, 64, 128, 256, 512}` and see where BPC stops improving. That's the empirical dimensionality.

3. **Heuristic:** Something like `d_out ~ sqrt(V)` might be in the right ballpark.
   - Bigram: `sqrt(16384) = 128`, which is what we already have.
   - Char: `sqrt(128) ≈ 11`, which feels too small.

Option 2 is the most honest and not hard to implement. A factorized embedding in `train_tok.c` with a `d_out` sweep for bigram would directly answer "how much rank does the output need?"
