# Plan: a small language model that also reports its own embedding coordinates

## Goal

Train one small transformer on two tasks at once:

1. Language modelling on TinyStories (next-token prediction).
2. Self-report: answer "what is coordinate i of the embedding vector of token
   t?" with a number.

Then test whether the self-report reads the current embedding (answers follow
a change of the embedding vector) and what self-report costs the language
model. Follows `../self-report-embeddings/` (same question, toy model, random
embeddings), where reading became near-exact once the model was trained on
thousands of distinct embedding vectors.

Decisions made with the user (2026-10-06): TinyStories; answers from a number
head; tied input and output embeddings.

## Setup

- Data: TinyStories (roneneldan/TinyStories on Hugging Face), training shard
  0 of 4 (529,930 stories) and the validation split (21,990 stories).
- Tokenizer: byte-level BPE with 4,096 tokens (including an end-of-story
  token), trained on the training shard.
- Model: GPT-style decoder, pre-LayerNorm, learned positional embeddings,
  width 128, 4 layers, 4 heads, feed-forward width 512 (GELU), context 128.
  Tied embeddings: the logits are the final internal state times E[text
  tokens]ᵀ.
- Extra symbols, appended to the embedding table but never predicted: QUERY
  and COORD_0 … COORD_127.
- Self-report question for (t, i): the sequence [QUERY, COORD_i, t]. The answer
  is a linear function of the internal state at the last position (t's
  position), taken before the final LayerNorm. Correct answer E[t, i], current
  value, no gradient through it.
- Design note (found while planning; corrected after the code review). The
  question puts t last. With pre-LayerNorm every block sees its input
  normalized; the unnormalized E[t] in the residual stream at t's position
  reaches the answer only through the fixed number-head readout w·x, the same
  for every coordinate, so picking out coordinate i must go through the blocks.
  Exact consequence: LayerNorm subtracts the mean, so a change of E[t] along the
  all-ones direction is invisible to the blocks and moves every answer by
  exactly Σw. Length is not strictly hidden: LayerNorm of x plus a large
  constant is nearly linear in x. So exact reading is not guaranteed;
  "direction tracked better than length" is a prediction to test. (I told the
  user earlier that reading before the final norm makes exact reading
  possible; that was too strong.)
- Tokens asked about: three quarters of the 4,096 text tokens (training
  tokens); the other quarter are held-out tokens, which appear in the language
  modelling data but are never asked about.
- Loss: cross-entropy (language modelling) + λ · (1 − R² of the self-report
  batch), λ = 1.
- Each step: one language-modelling batch (32 sequences × 128 tokens) and one
  self-report batch (256 questions). 15,000 steps (61M tokens), AdamW, learning
  rate 2e-3 with 200 warm-up steps and cosine decay to 2e-4.

## Runs

- Joint (λ = 1), seed 0.
- Language model only (λ = 0), seed 0: the baseline for what self-report costs.
- Joint (λ = 1), seed 1, if time allows.

## Measurements (at the end, `measure.py`)

1. Language modelling: validation loss (nats per token), compared with the
   baseline; a few generated stories.
2. Self-report R² on training tokens, held-out tokens, and random vectors drawn
   from a normal distribution matched per coordinate to the embedding table.
3. Follow and other movement (as in `../self-report-embeddings/`), from the
   Jacobian of the 128 answers about t with respect to E[t]; also follow for
   changes along E[t] (length) and across it (direction) separately.
4. Edit test: add a change to one embedding vector in the actual table, and
   measure both the change of the self-report and the change of the language
   model's next-token distributions after that token in validation text.
5. Measurement code checked on hand-made functions with known answers (tests).

## Steps

- [x] `prepare.py`: tokenizer and token files.
- [x] `lm.py`: model; `train.py`: joint training with logging and checkpoints.
- [x] `measure.py`: measurements 1-4.
- [x] Tests; independent code review by a separate Claude instance (NOTES.md).
- [x] Short trial run (canary), then the runs above; added a control run with the
      self-report's input detached (after the review of the report draft).
- [x] REPORT.md, PDF.

## Roadmap: the other options, for later

Each is a separate experiment, to be started only with the user's agreement.

1. Answers as text. The model writes the number as digit tokens (for example
   sign, two digits after the decimal point) instead of using a number head.
   Closer to how a language model would answer; harder to train and to score
   (scoring by parsing the digits; follow measured by finite changes, since the
   output is discrete).
2. Untied embeddings. Separate input and output tables; ask about the input
   table, the output table, or both. Asking about the output table is the first
   case where the weights asked about are not an input.
3. Synthetic language. A generated language with known structure (for example a
   small probabilistic grammar), so that we control what the embeddings must
   encode and can relate the self-report to that structure.
4. Weights that are not inputs. Ask about entries of a feed-forward matrix W₁;
   the model can only read them through their effect on its internal state.
   The hard and most interesting case.
5. A pretrained model. Fine-tune a small pretrained model (for example GPT-2
   small) to report its own embedding coordinates, then run the same follow and
   edit tests.
6. Length versus direction. If measurement 3 confirms that answers track the
   direction of E[t] better than its length, test architectures without the
   normalization that causes it.

## Stage 1 (asked for by the user, 2026-10-07): raise follow above 0.87

Follow of the control model is 0.871 / 0.868 (asked-about / never-asked tokens);
its accuracy was still rising when training stopped.

Phase 1 (`run_stage1.sh`, `finetune.py`, `quick_measure.py`): continue the
control model for 3,000 steps at constant learning rate 2·10⁻⁴, self-report
gradient stopped at the token embedding vectors, under four variants:
- [ ] more training only (λ = 1);
- [ ] self-report loss coefficient λ = 4;
- [ ] perturbed questions: x = E[t] + δ with |δ| = s·|E[t]|, s uniform in [0, 0.5],
      target x_i (λ = 1);
- [ ] λ = 4 and perturbed questions.
Measured: validation loss, centred R², follow, other movement, gain along E[t].

Phase 2: the best variant trained from scratch (seed 0, 15,000 steps), measured
with measure.py and compared with the control.

## Stage 2 (asked for by the user): answers written as text

After stage 1. The model writes the number as digit tokens; to be designed.
