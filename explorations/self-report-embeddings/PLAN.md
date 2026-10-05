# Plan: can a model report its own embedding weights, and do the reports follow changes?

## Question

Train a small transformer to answer "what is coordinate i of your embedding of
token t?". After training, change an embedding row. Does the answer change with
it (the model reads its weights), or does it stay the same (the model has
memorized the answers)?

Background (from the neural-network quine, `../neural-network-quine/`): the
quine matched its own weights with R² 0.9975, but changing a weight by 0.1 moved
its guess by about 0.001. Its answers were memorized, not read. The token
embedding is different: when the model reads token t, its internal state starts
as exactly the embedding row of t, which is made of weights. So a model can, in
principle, read those weights.

## Setup (first version)

- Tokens. V content tokens (the ones asked about) and d index tokens
  ("coordinate 0", ..., "coordinate d−1"). Start with V = 64, d = 32.
- Input. Two tokens: [t, i], content token t followed by index token i.
  No positional embeddings: the two token sets are disjoint, so the model can
  tell them apart without positions. Then the internal state at the first
  position is exactly the embedding row E[t].
- Model. A small transformer: width d = 32 (equal to the embedding size), 2
  layers, 4 attention heads, MLP width 128 with ReLU, causal attention. A linear
  output on the last position gives one number. No LayerNorm in the first
  version: LayerNorm divides the internal state by its size, so the answer could
  not follow a change in the size of E[t] exactly.
- An exact reader exists in this architecture, so failure to read cannot be
  blamed on the architecture. Construction: attention copies E[t] to the last
  position; the MLP then computes x_i exactly with two ReLU units per
  coordinate, x_i = relu(x_i + M·[index is i] − M) − relu(−x_i + M·[index is i] − M),
  valid when |x_i| < M. That needs 2d = 64 MLP units of the 128. (Check this
  with a hand-built model in the tests.)
- Target. E[t]_i, read from the model's current embedding table at each
  training step (so if the embeddings are trained, the targets move with them,
  as in the quine). No gradient flows through the target: the answer is pulled
  toward the weight, never the weight toward the answer. (The quine's "full
  gradient" did the opposite; that can be a later variant.)
- Loss. Mean squared error divided by the variance of the targets in the batch
  (= 1 − R² of the batch). Lesson from the quine: with plain squared error and
  trained embeddings, shrinking the embeddings lowers the loss without any
  reading.
- Data. Every pair (t, i) for the training tokens. 25% of the content tokens
  are held out: never asked about during training.

## The comparison

| condition | embedding rows of content tokens |
|---|---|
| A: fixed | random, never trained; the model can only learn to read or to memorize |
| B: trained | trained together with the rest of the model, targets moving with them |

Both conditions: 3 seeds. The index-token embeddings and all other weights are
trained in both.

## Measurements

All on the trained model, separately for training tokens and held-out tokens.

1. R²: answers against the current embedding values.
2. Follow test. Replace the embedding row of t by E[t] + δ, with δ random, at
   sizes 10% and 100% of |E[t]|. Then

   follow ratio = ⟨answers after − answers before, δ⟩ / |δ|²

   computed over the d coordinates of t. 1 means the answers moved exactly with
   the change; 0 means they ignored it.
3. Brand-new tokens. Give the model completely new random embedding rows (not
   from training) and measure R². A model that reads gets these right; a model
   that memorized cannot.

## What would count as an answer

- Reads: follow ratio near 1, high R² on held-out and brand-new tokens.
- Memorized: high R² on training tokens only, follow ratio near 0.
- Something in between is possible and would be worth understanding.

## Steps

- [ ] Virtualenv and requirements.txt.
- [ ] `model.py`: the transformer and the data.
- [ ] `train.py`: one run per (condition, seed); saves the model and a JSON log.
- [ ] `follow_test.py`: measurements 1 to 3.
- [ ] Tests: the internal state at position 1 equals E[t] exactly; a model
      whose output is the hand-built coordinate reader has follow ratio 1.
- [ ] Run A and B, 3 seeds each (CPU, minutes each).
- [ ] Write up the results in plain language (REPORT.md).

## Later, only if the first version works and the user agrees

- Answers written as text tokens instead of a number.
- More content tokens than the model can memorize, and fewer: does the outcome
  depend on memorization capacity?
- Weights deeper in the model, read through their effect on known inputs.
- A pretrained model (e.g. GPT-2 small) fine-tuned to report its own embedding.
