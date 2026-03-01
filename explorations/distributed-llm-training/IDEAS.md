# Training Ideas: Deep Dive

## Idea 1: Greedy Stepwise PPL Optimization

### The Proposal

Instead of one long training run, break it into stages:
1. Find best config (LR, batch size, seed, etc.) to reach PPL 15 fastest (wall clock)
2. Take that checkpoint
3. Find best config to go from PPL 15 → PPL 10 fastest
4. Repeat down to target PPL

### Is Greedy Suboptimal?

**Short answer: Yes, almost certainly, in theory. But possibly not by much in practice.**

Ways the greedy approach fails:

1. **Learning rate trap**: High LR reaches PPL 15 fast but lands in a region
   with sharp curvature. The optimizer state (Adam momentum, variance estimates)
   is adapted to this high-LR regime. Continuing from this checkpoint, even
   with a lower LR, may be worse than a config that reached PPL 15 more slowly
   but landed in a flatter region. This is the sharp-vs-flat minima problem
   (Keskar et al. 2017).

2. **Batch size interaction**: Small batch size gives faster initial progress
   (more parameter updates per second) but introduces more noise. This noise
   helps escape bad regions early (good for reaching PPL 15) but may prevent
   fine convergence later. Large batch is the opposite. The optimal batch size
   changes during training (Smith et al. 2018 "Don't Decay the Learning Rate,
   Increase the Batch Size").

3. **Optimizer state discontinuity**: When you checkpoint at PPL 15 and
   restart with new hyperparams, the optimizer's running statistics (Adam's m
   and v) were tuned for the old config. There's a transient period where the
   optimizer is confused. This "checkpoint warmup" cost might negate the time
   saved by greedy selection.

4. **Loss landscape path dependence**: Two configs at the same PPL are not at
   the same point in weight space. The "fastest to PPL 15" config may have
   taken the model to a region where further progress is harder, while a
   slower config placed it on a better trajectory.

### The Portfolio Optimization Analogy

This IS similar to portfolio optimization. Reframing:
- State = (model weights, optimizer state, current PPL)
- Action = choice of hyperparameter config
- Reward = -wall_clock_time to reach next PPL milestone
- We want to minimize total time to reach target PPL

The greedy approach optimizes each stage independently. The optimal approach
would solve the full sequential decision problem. This is literally an MDP.

### Mitigations (Making Greedy Work Better)

1. **Keep top-K, not top-1**: At each stage, keep the K best configs (by wall
   clock to milestone). This is basically Successive Halving / Hyperband
   (Jamieson & Talwalkar 2016, Li et al. 2017). Diversifies against the
   greedy trap.

2. **Include trajectory features in selection**: Don't just pick fastest to
   PPL 15. Also consider: gradient norm, loss curvature, effective LR. A
   config with lower gradient norm at PPL 15 (flatter region) may be better
   for the next stage even if it was slightly slower.

3. **Warm-restart the optimizer**: When switching configs, don't naively
   continue optimizer state. Reset or warm-start the optimizer for the new
   config. This reduces the state discontinuity problem.

4. **Overlap stages**: Don't hard-switch. Run the new config for a few steps
   alongside the old one and compare trajectories before committing.

### Verdict on Idea 1

The greedy approach is a reasonable starting point. Its main risk is myopia
around learning rate and optimizer state. The top-K mitigation (Hyperband-like)
largely addresses this. The portfolio optimization framing is correct and
suggests the problem could be formulated as a multi-stage stochastic
optimization, but the greedy+top-K heuristic is probably 90% as good with 10%
of the complexity.

**For the distributed setup**: This is a natural fit. Each session explores a
different config at each stage. Git coordinates the tournament (push
checkpoints + metrics, orchestrator picks winners). The parallelism directly
addresses the search cost.

---

## Idea 2: Speculative Layer Execution / Branch Point Prediction for Layers

### The Proposal

In a 12-layer model split across 2 workers (layers 1-6 and 7-12):
- Worker B (layers 7-12) is idle while Worker A (layers 1-6) computes
- What if Worker B predicts the layer-6 activations and starts computing
  speculatively?
- When real activations arrive, correct somehow

### Analysis

This is **speculative pipeline parallelism**, analogous to speculative
execution in CPUs (predict branch, execute speculatively, rollback if wrong).

**Existing literature** (from survey -- see REFERENCES.md for full list):

Weight prediction approaches (predict weights, not activations):
- **SpecTrain** (Chen et al. 2018): momentum-based weight prediction for
  pipelined model parallelism. Up to 8.91x speedup. Only works with SGDM.
- **PipeMare** (Yang et al. 2019/MLSys 2021): async pipeline with LR
  rescheduling and discrepancy correction. 2.7x less memory or 14.3x higher
  pipeline utilization.
- **PipeOptim** (Guan et al. 2023/TKDE 2025): optimizer-aware weight
  prediction (SGD, Adam, AdamW). Bubble-free 1F1B without accuracy loss.
- **Leap+Verify** (McEntire 2025): regime-adaptive speculative weight
  prediction K steps ahead. Detects training phases (chaotic/transition/stable).
- **Pipelined Backprop at Scale** (Kosson et al. 2020): linear weight
  prediction + spike compensation for batch-size-1 pipelining.

Decoupled / local learning approaches:
- **Synthetic Gradients** (Jaderberg et al. 2017): learned models predict error
  gradients from local activations only. Fully decoupled, async layer updates.
- **Decoupled Parallel Backprop** (Huo et al. 2018): delayed gradients to
  remove backward locking. Convergence proof for non-convex.
- **Features Replay** (Huo et al. 2018 NeurIPS): parallel-objective with
  features replay to avoid memory explosion of decoupled methods.
- **Belilovsky et al. 2019/2020/2021**: greedy layerwise learning that scales
  to ImageNet. 2021 paper specifically addresses distributed async setting
  with replay buffers and large communication delays.
- **Local Error Signals** (Nokland & Eidnes 2019): layer-wise training with
  local supervised signals, weights updated during forward pass.
- **Parallel Training with Local Updates** (Laskin et al. 2020): compares five
  variants of local parallelism, shows scaling beyond data-parallel regime.

Pipeline bubble reduction (non-speculative):
- **Zero Bubble PP** (Qi et al. 2024/ICLR): splits backward into input-grad
  and weight-grad for zero-bubble scheduling. 31% throughput improvement.
- **PipeFisher** (MLSys 2023): fills bubbles with K-FAC (second-order
  optimization). 50-75% training time reduction for BERT.

Staleness analysis:
- **PipeDream** (Harlap et al. 2019): weight stashing for consistent versions.
- **DSP** (Xu et al. 2020): formalized layer-wise staleness, convergence proof.
- **LayerPipe/LayerPipe2** (Unnikrishnan & Parhi 2021/2025): retiming theory
  for pipelined schedules, EMA weight prediction.

**Key finding: Nobody has done activation prediction specifically.** All
existing speculative methods predict *weights* (what the model parameters will
be at a future step) not *activations* (what intermediate layer outputs will
be for a given input). Activation prediction for pipeline bubble reduction
appears to be a novel or very niche direction.

**The prediction problem**:

How to predict layer-6 activations before layer 1-6 have run?

Options:
a) **Previous micro-batch's activations**: Simplest. Use layer-6 output from
   the previous input. Prediction error = how much activations change between
   consecutive inputs.

b) **Exponential moving average**: Track running statistics of layer-6
   activations, predict the mean. Only works if activation distribution is
   relatively stable.

c) **Small predictor network**: Train a tiny model (input → predicted layer-6
   activations). Adds complexity and its own training cost.

d) **Linear extrapolation**: Use the trend from the last few micro-batches.

**The correction problem**:

When real activations arrive and differ from predicted:

a) **Recompute**: Defeats the purpose. Only saves time if prediction is usually
   right.

b) **Accept the noise**: Treat prediction error as training noise. Early in
   training, gradients are already noisy, so this might work. Late in training,
   it could prevent convergence.

c) **Correction gradient**: Compute ∂L/∂(predicted_activation) and
   ∂(real - predicted), add a correction term. This is essentially a Taylor
   expansion correction.

d) **Just don't correct**: If using this for the forward pass only, the
   backward pass will use real activations (stored from the actual forward).
   The speculative forward was just to warm up Worker B's compute.

### Key Insight for Our Setup

In standard pipeline parallelism, the pipeline bubble is microseconds to
milliseconds. The prediction overhead may not be worth it.

**But in our setup, the "pipeline bubble" is minutes to hours** (waiting for
git push/pull between sessions). This completely changes the calculus.
Even a mediocre prediction that's 50% correlated with real activations could
be useful, because the alternative is doing nothing for that entire wait time.

This makes option (b) -- "accept the noise" -- much more attractive. If each
session is going to sit idle for 10 minutes waiting for activations from
another session, it's strictly better to train on predicted activations (even
noisy ones) than to do nothing.

### Rethinking for the Distributed Case

Actually, for our distributed setup, the cleanest version of this idea is:

**Decoupled local training with periodic synchronization.**

- Session A trains layers 1-6 with a local auxiliary loss (predict something
  useful from layer 6 output directly)
- Session B trains layers 7-12, taking inputs from Session A's last-known
  layer-6 activations (cached/pushed via git)
- Periodically, Session A pushes new activations, Session B pulls and adjusts
- End-to-end fine-tuning pass periodically to calibrate

This is closer to **local learning** (Belilovsky et al.) than speculative
execution, but it's the practical version of the idea for high-latency
communication.

### Verdict on Idea 2

Intellectually interesting. For standard pipeline parallelism (fast
interconnect), the gains are marginal because the bubble is small and
prediction overhead adds complexity. **For our high-latency setup, the idea
becomes much more compelling** because the bubble is so large that even noisy
speculative computation beats idle time.

**Novelty note**: The literature survey revealed that all existing speculative
pipeline methods predict *weights* (what model parameters will be at step t+k),
not *activations* (what layer outputs will be for a given input). Your idea of
predicting activations appears to be either novel or very niche. However,
the practical version for our setup is closer to **Belilovsky et al. 2021**
(decoupled greedy learning for async distributed), which directly addresses
asynchronous distributed training with large communication delays. Their
approach uses local auxiliary losses + replay buffers, which is essentially
what we'd end up implementing.

The cleanest implementation is decoupled local training (each layer group
trains with a local loss) with periodic synchronization.

---

## Idea 3 (Mine): Ensemble Distillation Instead of Weight Averaging

### The Problem with Weight Averaging

FedAvg and model souping average the weights of independently trained models.
This works well when models haven't diverged too much (same architecture, same
init, few local steps). But it breaks down when:
- Models train for many steps independently (our case -- high latency)
- Models end up in different basins of the loss landscape
- Weight permutation symmetry: two models may have learned the same function
  but with neurons in different order. Averaging their weights destroys both.

### The Proposal

Instead of averaging weights, use the N independently trained models as an
**ensemble teacher**:

1. Each session trains a model independently on its data shard
2. Push models to git
3. Orchestrator runs all N models on a shared dataset, collecting soft
   labels (probability distributions over vocabulary)
4. Train a fresh student model (or continue from a checkpoint) on the
   ensemble's soft labels (knowledge distillation, Hinton et al. 2015)
5. Push student model back, start next round

### Why This Is Better

- No weight permutation problem -- we're merging predictions, not weights
- Works even when models diverge significantly
- The ensemble is naturally better than any individual model (ensemble theory)
- The student model learns a compressed version of all N models' knowledge
- Well-understood theoretically (distillation, ensemble learning)

### Why This Is Worse

- Requires extra compute for the distillation step
- Need a shared unlabeled dataset for the teacher ensemble to label
- More complex orchestration (N forward passes + 1 training run per round)
- Slower per-round than simple averaging

### For Our Setup

This could work well if each session trains on different data. The ensemble
captures diverse knowledge. The distillation step could run on one session or
be distributed itself. The latency tolerance is high since we're doing
asynchronous rounds anyway.

---

## Idea 4 (Mine): Genetic / Evolutionary Strategy over Training Configs

### The Proposal

Treat each session as an individual in an evolutionary population:

1. Each session gets a "genome": (model architecture params, LR, batch size,
   optimizer settings, data ordering seed, etc.)
2. Each session trains for K steps, reports fitness (PPL, loss)
3. Orchestrator does selection + crossover + mutation:
   - Keep top configs
   - "Crossover": take model weights from parent A, hyperparams from parent B
   - "Mutation": perturb hyperparams randomly
4. Push new configs, repeat

This is basically **Population-Based Training** (PBT, Jaderberg et al. 2017)
but adapted for high-latency, asynchronous communication.

### Why It Fits Our Setup

- Naturally asynchronous -- sessions can finish at different times
- No weight merging needed -- just selection and copying
- Explores hyperparameter space efficiently
- Trivially parallelizable
- Each session is independent -- no inter-session communication during training
- Git is just used for the coordination/selection step

---

## ~~Idea 5 (Mine): Speculative Training with Rollback~~

**SKIP THIS -- On reflection, this is just Idea 4 (PBT) with a tree-structured
search instead of a flat population. The "speculative execution" framing doesn't
hold up: the "wait time" is ill-defined, and if your checkpoint isn't the winner,
all speculative work is wasted. The useful kernel (explore multiple branches from
each checkpoint) is already captured by Idea 4 with mutation.**

### The Proposal (combines Ideas 1 and 2)

Given high latency, each session "speculates" on multiple possible futures:

1. Session trains for K steps, reaching checkpoint C
2. Session then speculatively trains K more steps with 3 different configs:
   - Config A: continue current trajectory
   - Config B: reduce LR by half
   - Config C: increase batch size
3. Push all 4 checkpoints (C, C+A, C+B, C+C) and metrics
4. Orchestrator picks the best continuation
5. Other sessions pull and continue from the winning checkpoint

This is **speculative execution applied to hyperparameter search**, not layer
computation. It uses the idle time (waiting for coordination) productively by
exploring the decision tree.

### Why It's Interesting

- Turns the high-latency disadvantage into a feature -- the wait time is used
  for exploration
- Each round both trains AND searches
- Naturally handles the "greedy might be suboptimal" problem from Idea 1 by
  exploring multiple branches

---

## Summary: What's Worth Prototyping First?

| Idea | Complexity | Promise | Novelty | Fits Distributed Setup |
|------|-----------|---------|---------|----------------------|
| 1. Greedy PPL stages | Low | Medium | Low (Hyperband-like) | Yes (parallel search) |
| 2. Speculative activations | High | High (for high-latency) | **High** (unexplored) | Yes (high latency motivated) |
| 2b. Decoupled local training | Medium | High | Low (Belilovsky 2021) | Yes (directly applicable) |
| 3. Ensemble distillation | Medium | High | Low (well-studied) | Yes (no weight merge problems) |
| 4. Evolutionary/PBT | Low | High | Low (Jaderberg 2017) | Excellent (naturally async) |
| 5. Speculative training + rollback | Medium | High | Medium | Excellent (uses wait time) |

**My recommendation for first prototype**: Idea 4 (PBT/evolutionary). It's the
simplest to implement, naturally fits the async/high-latency constraints, and
gives us a working framework for running distributed experiments. Ideas 1 and 5
layer on top of it nicely.

Idea 2 (speculative layers) is the most novel but also the most complex. Worth
prototyping second, after we have the basic infrastructure.

Idea 3 (ensemble distillation) is the most theoretically grounded fallback if
weight merging doesn't work.
