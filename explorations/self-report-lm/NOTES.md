# Lab notes

## 2026-10-06: setup

Data: TinyStories from Hugging Face (roneneldan/TinyStories), downloaded with curl:
data/train-00000-of-00004-2d5a1467fff1081b.parquet (529,930 stories) and
data/validation-00000-of-00001-869c898b519ad725.parquet (21,990 stories),
saved as data/train0.parquet and data/valid.parquet (not committed; data/ is ignored).

Design note found while planning: with pre-LayerNorm the blocks see only
normalized inputs, so the question is laid out [QUERY, COORD_i, t] and the
answer is read at t's position (PLAN.md). Earlier I told the user that reading
before the final norm makes exact reading possible; that was too strong.

Timing: about 1.1 s per training step with 2 threads (measured while another
process was running), so two runs in parallel with 2 threads each.

Mistake: prepare.py first encoded all 530k stories in one batch; it reached 14
GB and was killed by the kernel (out of memory). Fixed by encoding in chunks of
10,000 stories; the tokenizer it had already saved is reused.

## 2026-10-06: code review (separate Claude instance) and fixes

No bug that would have invalidated the runs. Fixed before the main runs:
- Logged held-out R² used the 256 lowest held-out ids (mostly rare byte tokens);
  now a random subset.
- Checkpoints are written to a temporary file and renamed (a kill mid-write
  would have left a truncated checkpoint).
- edit_test held full log-prob tensors (about 7 GB); now batch by batch.
- The language-model-only baseline saw different text batches from step 2 on
  (one generator for text and questions); now two generators, so the two runs
  see the same text.
- Design note corrected (PLAN.md). Every LayerNorm subtracts the mean, so the
  blocks cannot see a change of E[t] along the all-ones direction: every answer
  then moves by exactly Σw (w: number-head weight). Now measured, and tested.
  Length is not strictly hidden either (LayerNorm of x plus a large constant is
  nearly linear in x), so "direction tracked better than length" is a
  prediction, not a consequence of the architecture.
- Tests were weak (five plausible bugs passed them); added tests that catch
  them: number head position and pre-final-norm reading, next-token targets,
  weight-decay groups, edit-test KL by hand, the all-ones direction. 12 pass.

Canary (300 steps, joint): 0.5 s per step with 2 threads; validation loss 4.52
(step 250) and 4.34 (step 300); self-report R² 0.34 (training tokens) and 0.41
(held-out, biased subset). Main runs set to 15,000 steps (61M tokens).

## 2026-10-06: main runs

joint_s0 and lmonly_s0 finished (15,000 steps each; validation loss 2.261 and
2.154). Seed-1 joint run started when the baseline finished.

Mistake: the Jacobian measurement used a generic autograd jacobian (128 backward
passes per token, about 69 s per token with the CPU shared). The first
measurement ran 44 minutes without finishing one model; I stopped it. Fixed:
each of the 128 question sequences gets its own copy of x, so one backward pass
gives all rows of J (1 s per token, identical result; tested).
