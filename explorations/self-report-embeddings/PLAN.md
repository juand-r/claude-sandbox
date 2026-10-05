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
  blamed on the architecture (`canaries.perfect_reader`, 96 of the 128 MLP
  units, valid while every |x_j| < 15). Attention with zero queries averages the
  two positions; with index embeddings 10·e_i, position 1 holds
  x/2 + 15·e_i. The MLP cancels that and writes x_i/2 + 7.5 into coordinate 0
  (one ReLU per coordinate, active only for coordinate i); the readout undoes
  the scale and offset. (An earlier draft of this plan described a 2·d-unit
  version that did not account for the residual stream; it was wrong.)
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

Defined precisely in the docstring of `follow_test.py`. In short, for training
tokens and held-out tokens separately:

1. R² of the answers against the current embedding values (also a centred R²).
2. Local follow: J = ∂answers/∂E[t] from autograd; trace(J)/d (1 for a reader,
   0 for a memorizer) and the size of J's other part. Exact, no random changes.
3. Finite changes E[t] ← E[t] + δ at 1%, 10% and 100% of |E[t]|: follow ratio
   ⟨Δanswers, δ⟩/|δ|² (mean and median), other movement, R² of the change,
   fraction of jumps.
4. Brand-new embedding rows (never in E): R² of the answers.

Canaries: a hand-built perfect reader and a nearest-row memorizer, pushed through
the same code; `check_canaries` fails loudly if their known results are not
reproduced. Untrained models (same initialization) give a baseline.

Changes after the code review (2026-10-05, see NOTES.md): items 2, the median,
the jump fraction, the 1% size and R² of the change were added, because the mean
follow ratio is unreliable when answers jump, and "R² after change" (the earlier
item) hardly measured following at all.

## What would count as an answer

- Reads: follow ratio near 1, high R² on held-out and brand-new tokens.
- Memorized: high R² on training tokens only, follow ratio near 0.
- Something in between is possible and would be worth understanding.

## Steps

- [x] Virtualenv and requirements.txt.
- [x] `model.py`: the transformer and the data.
- [x] `train.py`: one run per (condition, seed); saves the model and a JSON log.
- [x] `follow_test.py`: measurements 1 to 4.
- [x] Tests (12) and canaries.
- [x] Independent code review by a subagent; findings addressed (NOTES.md).
- [ ] Run A and B, 3 seeds each (CPU, minutes each).
- [ ] Write up the results in plain language (REPORT.md).

## Later, only if the first version works and the user agrees

- Answers written as text tokens instead of a number.
- More content tokens than the model can memorize, and fewer: does the outcome
  depend on memorization capacity?
- Weights deeper in the model, read through their effect on known inputs.
- A pretrained model (e.g. GPT-2 small) fine-tuned to report its own embedding.
