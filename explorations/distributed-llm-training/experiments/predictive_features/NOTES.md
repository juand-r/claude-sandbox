# Analysis Notes — Predictive Features Experiment

## Run Summary

- 90 configs (3 LRs x 3 BSs x 10 seeds), all reached 7/7 milestones
- 630 total milestone records, 540 with time_to_next targets
- Runtime: 809s (~13.5 min) on 12 workers / 16 cores
- Full analysis output saved in `results/analysis_output.txt`

## Key Findings

### 1. wall_time dominates everything

The #1 predictor by far is `wall_time` (Spearman 0.91, RF importance 0.88). This is
a **confound**: runs that have already taken longer to reach milestone K tend to take
longer to reach K+1 as well. This is just saying "slow runs are slow" — it's not a
useful predictive feature, because you already know wall_time at selection time
(it's basically the same as greedy).

### 2. batch_size is highly predictive (and we know it at config time)

batch_size has Spearman 0.58 overall, and 0.94 at stage 0. Larger batch sizes =
slower per-step (more compute per step) = longer wall-clock time to next milestone.
This is also not interesting as a "discovered" feature — it's a hyperparameter we
already know.

### 3. Genuinely interesting features (after removing confounds)

Features that are NOT just config or accumulated time, ranked by Spearman:
- **grad_var** (-0.73): Higher gradient variance at a milestone → reaches next milestone *faster*.
  Could indicate the model is still in a high-learning-rate regime.
- **grad_layer_norm_std** (-0.74): Similar to grad_var. Non-uniform gradient distribution
  across layers predicts faster progress.
- **ppl_derivative** (0.71): Rate of PPL decrease. If PPL is still dropping fast when you
  hit a milestone, you reach the next one faster. Makes intuitive sense.
- **loss_slope** (0.70): Same signal as ppl_derivative.
- **grad_norm** (-0.70): Higher gradient norms → faster progress. The model is still
  making big updates.
- **adam_effective_step** (-0.68): Bigger effective Adam steps → faster. Same story.
- **grad_snr** (-0.46): Stage-dependent. Very strong at stage 0 (0.80) but weak later.
  Early gradient coherence matters for initial learning but not late convergence.

### 4. Stage-dependent effects (per-stage Spearman)

Some features change predictive power across stages:
- **grad_snr**: Strong early (0.80 at stage 0), weak late (0.15 at stage 4).
  Gradient coherence matters for initial learning but not fine-tuning.
- **hessian_trace**: Weak early (-0.05), strong late (0.72 at stage 5).
  Loss curvature becomes important in late training.
- **sharpness**: Same pattern as hessian_trace — late-stage signal (0.63 at stage 5).
- **weight_dist_from_init**: Increasingly negative later (-0.63 at stage 5).
  Models that have moved further from init by late training are slower to improve further.
- **lr**: More negative later (-0.60 at stage 5). Higher LR helps early but the
  effect becomes stronger as a predictor of slowness in late stages.

### 5. Model fit quality

- Linear regression R² = 0.96 — very high, but heavily driven by wall_time.
- Random forest R² = 0.996 (in-sample, likely overfit, but the feature importances
  are still informative for ranking).

### 6. Interpretation for distributed training

For a selection policy that goes beyond greedy:
- At early milestones: weight selection toward runs with high **grad_snr** and
  strong **ppl_derivative** (momentum).
- At late milestones: penalize runs with high **hessian_trace** or **sharpness**
  (stuck in sharp minima), and runs far from init (**weight_dist_from_init**).
- **grad_var** and **grad_norm** are useful throughout as indicators of "the model
  is still actively learning."

The null hypothesis (greedy is near-optimal) is **rejected**: features beyond
current PPL do predict future training speed, and the predictive features change
across training stages.
