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

Stage 1, phase 1 results (3,000 more steps from the control; follow on the same 128
asked-about / 128 never-asked tokens; start 0.870 / 0.854):
more training 0.893 / 0.878; λ = 4 0.896 / 0.880; perturbed questions 0.959 / 0.949;
both 0.968 / 0.959. Validation loss 2.295 to 2.307 in all four (start 2.307).
Interpretation: perturbed questions ask for correct answers near each embedding vector,
not only at it, which is the property follow measures; so the gain is from training for
the property directly. That is the intended property (answers computed from the current
value), but it should be stated plainly in the report.
Phase 2 started 05:55: control_jit_s0 (from scratch, perturbed questions, λ = 1) and the
stage-2 text run text_s0, in parallel.

Phase 2, first result: control_jit_s0 (from scratch, perturbed questions, λ = 1) has follow
0.886 / 0.880 (128 + 128 tokens), centred R² 0.970, validation loss 2.315; the original
control 0.870 / 0.854, 0.982, 2.307. Much less than the 3,000-step continuation with
perturbed questions (0.959 / 0.949). Not understood. Started 08:20: ft2_lam4_jit, 6,000
more steps from ft_lam4_jit (λ = 4, perturbed questions), to see whether follow keeps rising.

### 2026-10-07 ~08:55 UTC: ft2_lam4_jit finished
- 6,000 more steps from ft_lam4_jit (λ = 4, perturbed questions up to 50% of |E[t]|, lr 2e-4).
- Follow (asked/never, 128+128 tokens) by step: 0.968/0.959, 0.964/0.956, 0.952/0.945, 0.978/0.970,
  0.968/0.961, 0.990/0.984, 0.980/0.973. It moves by about ±0.02 between evaluations, so single
  evaluations are noisy; the trend over 6,000 steps is up by about 0.01 to 0.02.
- Other movement falls steadily: 0.271 -> 0.180. Centred R² rises: 0.979 -> 0.989. Validation loss 2.307 -> 2.290.
- Process mistake: the monitor for this run used `declare -A` and was apparently run by a shell
  without it; it delivered no events for 30 minutes. Rule: wrap monitor commands in `bash -c '...'`,
  and check that the first event arrives.
- Correction to the monitor note above: the real cause was `awk` (here mawk 1.3.4), which reads a
  pipe in large blocks, so `... | awk '!x[$0]++'` printed nothing until its buffer filled. Two later
  monitors failed the same way. Replaced by a small bash watcher that dedupes with a seen-file
  (scratchpad/watch.sh), tested by hand before arming.

### 2026-10-07 ~09:00 UTC: stage 2 (text answers), first full measurement of text_s0
Validation loss on measure.py's 100 × 32 windows (seed 4321), same windows for every run:

| run | answer | validation loss |
|---|---|---|
| lmonly_s0 | none | 2.146 |
| joint_detached_s0 (control) | number head | 2.290 |
| control_jit_s0 | number head, perturbed questions | 2.298 |
| text_s0 | text, 5 characters | 2.180 |

text_s0, over all asked-about / never-asked tokens (answer characters excluded):
- centred R² 0.951 / 0.948;
- valid-format rate without the character restriction: 1.0 / 1.0 (64 tokens × 128 coordinates each);
- finite-change follow at 30% of |E[t]| (256 tokens per set): mean 0.756 / 0.739, median 0.783 / 0.767.
  The number-head control on the same tokens and directions: mean 0.841 / 0.837, median 0.857 / 0.865.
- Observation: the text answers cost the language model much less than the number head
  (2.180 vs 2.290; LM-only 2.146). Not yet understood. Note the number-head control's
  centred R² is higher (0.982), so the comparison is not at equal accuracy.
- Next: continue text_s0 with perturbed questions (finetune_text.py, text_jit), as in stage 1.

### 2026-10-07 ~10:40 UTC: stage 1 result; stage 2 progress
- ft_slope (ft_lam4_jit + 3,000 steps with λ = 4, perturbed questions, slope loss weight 1):
  full measurement follow 0.994 / 0.992, other movement 0.139, centred R² 0.990 / 0.990,
  validation loss 2.289. Written up in REPORT.md section 10.
- Open: why perturbed questions help so much less from scratch (control_jit_s0: 0.885) than as a
  continuation (ft_jit: 0.959 on 128 + 128). Started control_slope_s0: the full recipe
  (λ = 4, perturbed questions 0.5, slope loss 1) from scratch, 15,000 steps, seed 0.
  The slope loss was moved from finetune.py into train.py for this (tests pass; 2-step smoke run ok).
- Text: text_jit_lam4 (text_s0 + 3,000 perturbed λ = 1 + 3,000 perturbed λ = 4), full measurement:
  centred R² 0.975 / 0.973, valid-format rate 1.0, follow at 30% 0.862 / 0.855 (number-head control,
  paired: 0.841 / 0.837), validation loss 2.180. Running: 6,000 more steps (text_jit_lam4_long).
- measure_text.py now takes several number-head references (to compare with ft_slope as well).
- analyze_review's random-vector centred R² (used in the report) and measure.py's r2_random
  (one mean over all answers, as in the training loss) are different measures; the report uses the former.
