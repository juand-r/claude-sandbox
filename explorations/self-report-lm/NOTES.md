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

## 2026-10-06: review of the report draft (separate Claude instance)

All findings checked with `analyze_review.py` (results/review_checks_joint_s0.json) and fixed
in REPORT.md. The ones that changed conclusions:
- My section 6 explanation was wrong in its details. What block 0 cannot see is the
  centred vector E[t] + P[2] − mean (P[2] has length 1.36, so LayerNorm does not hide
  E[t]'s length as such). The trained model is nearly blind along it (response 0.005);
  the weak length response follows from E[t] overlapping that direction (cosine
  0.62-0.68).
- My per-frequency centred R² used set-wide means while the definition used the
  set's own; and the 97 rare held-out vectors are nearly identical (cosine 0.998).
  Replaced by follow per bin (0.34 / 0.79 / 0.83 on held-out tokens) and a rescaling
  test: rare held-out vectors rescaled to the frequent length are read well (score
  −1.34 → 0.96); frequent ones grown to the rare length are read badly (0.94 → −1.67).
- I had stated as fact that self-report pulls asked-about vectors into the reader's
  range. An optimizer explanation (Adam on rarely used rows) also fits. Control run
  started: self-report with its input detached (joint_detached_s0).
- Two validation sets were mixed (training log 20 × 32 windows, measurement 100 × 32);
  the cost is 0.102 on the measurement set, 0.107 on the log set.
- The edit test is a consistency check (both changes are guaranteed in kind), not
  evidence of a relation.
- Added: linear probe on the language-model-only model (held-out centred R² 0.834,
  not like for like); centred R² on random vectors (0.813); zero-count tokens (88
  training, 47 held-out).

## 2026-10-06: seed 1 and the control

Seed 1 reproduces every qualitative result of seed 0 with weaker numbers
(held-out centred R² 0.50 against 0.68; follow 0.67 against 0.75).

Control (self-report input detached, seed 0): held-out tokens read as well as
training tokens (centred R² 0.982 and 0.982; follow 0.87 and 0.87); rare
vectors stay long (about 4.1) in both sets and are read well; language-model
cost 0.144 against 0.102 for the joint run. So in the joint runs the
self-report reshaped the asked-about embedding vectors, and that shift is what
made the held-out tokens hard. Correction of mine: I wrote in the report that
this control would separate the two explanations for the shortening (pull into
the reader's range, or an Adam effect); it does not, since both act through
the self-report's gradient on the embedding table. Report revised (summary,
sections 5.2, 8, 10).

## 2026-10-06: terminology review of REPORT.md

The user could not follow my summary. A separate Claude instance reviewed the
report's terms; the main problems were: "self-report" never defined; "training
tokens", "reading", "frequent", "the hidden direction" each used for two things;
joint-run results presented as general before the control showed otherwise
("length alone decides" was wrong). Report rewritten with one vocabulary
(asked-about / never-asked tokens; joint / control / LM-only runs; follow, gain
along a direction, other movement, centred R², rescaling score), all four runs
defined in the setup, and the argument in order. A second cold read found
smaller problems (a wrong section reference, "weight" for the loss coefficient,
"good" with no measure behind it, the probe compared across seeds); fixed.
Added `norms_by_frequency.py` so the norm tables have a saved source.

## 2026-10-07: overnight work (stage 1: raise follow; stage 2: answers as text)

Stage 1, phase 1 started 04:50: four 3,000-step continuations of the control model
(finetune.py; quick_measure.py). Mistake: run_stage1.sh passes the step count where the
run name was meant (`$2` for `$1`) in the log path and the skip check, so both runs of a
pair log, interleaved, to logs/3000.log. The results files are named correctly (finetune.py
gets the right name) and hold each run's measurements. Not edited while running; fixed after.

Stage 2 code written (textanswer.py, train_text.py, measure_text.py). Design decisions
(mine; the user is asleep): five answer tokens (sign, digit, '.', digit, digit; resolution
0.01; clipped to ±9.99), all single-character tokens of the tokenizer; ordinary output layer;
control setting. Found while testing: with tied embeddings, the answer's cross-entropy
reaches every token's embedding vector through the output layer, so stopping the gradient
at the input is not enough for a control. Fixed: in the answer loss only the 13 answer
characters' rows of the output layer receive gradient; these 13 tokens are not asked about.
