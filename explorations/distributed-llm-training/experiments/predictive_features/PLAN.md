# Experiment: Predictive Features at PPL Milestones

## Question

At PPL milestone K, which cheaply-computable features predict how fast a training
run will reach milestone K+1? If such features exist, greedy selection (pick the
fastest run) can be improved by weighting selection on these features. If no
features predict, either (a) greedy is near-optimal, or (b) the relevant state is
locked in the high-dimensional weights and we can't extract it cheaply.

## Setup

- **Model**: Small GPT-2-style transformer (~2M params), character-level
  - 4 layers, 128 hidden dim, 4 heads
  - Sequence length 64
- **Dataset**: Tiny Shakespeare (character-level, ~1MB)
- **Config grid** (varied across runs):
  - Learning rate: [3e-4, 1e-3, 3e-3]
  - Batch size: [16, 32, 64]
  - Seeds: [42, 123, 271, 314, 512, 619, 777, 888, 1024, 1337]
  - = 90 runs total (10 independent seeds per (lr, bs) cell)
- **Parallelism**: `multiprocessing.Pool` with 1 PyTorch thread per worker.
  Use `--workers N` to run N configs in parallel (default: sequential).
- **PPL milestones**: [50, 30, 20, 15, 12, 10, 8] (character-level PPL)
  - Initial PPL ≈ 65 (= vocab size for uniform predictions)

## Features (22 total)

### Cheap (no extra compute):
1. **grad_norm**: Global gradient L2 norm
2. **grad_var**: Variance of gradient norms across parameters
3. **grad_layer_norms**: Per-layer gradient L2 norms (vector)
4. **adam_m_mean**: Mean magnitude of Adam first moment
5. **adam_v_mean**: Mean magnitude of Adam second moment
6. **adam_effective_step**: Mean of |m|/sqrt(v+eps) — actual update scale
7. **adam_v_max**: Max second moment (detects exploded variance)
8. **loss_variance**: Variance of loss over last N mini-batches
9. **loss_slope**: Linear fit slope of loss over last N steps
10. **steps**: Steps taken to reach this milestone
11. **wall_time**: Wall-clock time to reach this milestone (seconds)
12. **weight_norm**: L2 norm of all weights
13. **weight_dist_from_init**: L2 distance from initial weights
14. **weight_layer_norms**: Per-layer weight L2 norms (vector)
15. **lr**: Current learning rate
16. **batch_size**: Current batch size
17. **stage**: Stage number (which milestone)
18. **ppl**: Current perplexity
19. **ppl_derivative**: Smoothed rate of PPL change over last N steps

### Medium cost (a few extra forward passes):
20. **grad_snr**: Gradient signal-to-noise ratio (mean²/var across 5 mini-batches)

### Expensive (extra backward passes, optional):
21. **sharpness**: SAM-style loss sharpness (perturb weights, measure loss change)
22. **hessian_trace**: Hutchinson stochastic trace estimate of Hessian

## Output

For each (config, milestone) pair, we log:
- All 22 features
- `time_to_next`: wall-clock seconds to reach next milestone (the target variable)
- `steps_to_next`: training steps to reach next milestone

Saved as JSON-lines in `results/`.

## Analysis

1. Pearson/Spearman correlation of each feature with time_to_next
2. Linear regression (features → time_to_next)
3. Random forest feature importance (captures non-linear relationships)
4. Check if predictive features change across stages (early vs late training)

## Null result interpretation

If no features predict time_to_next:
- Run a separate test: do multiple configs from the SAME PPL milestone diverge
  in time-to-next? If yes, state matters but our features don't capture it.
  If no, greedy is near-optimal.
