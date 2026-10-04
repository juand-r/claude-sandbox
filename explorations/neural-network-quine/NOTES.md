# Lab notes

## 2026-10-03/04: reading the paper

Source: arXiv:1803.05859v4 (8 pages, ALIFE 2018). Read text and all figures.

### Facts recovered from the paper's own numbers (verified by arithmetic)

1. "Average weight prediction margin" is described as the average absolute
   difference, but the reported values equal the RMS error sqrt(L_SR / N),
   N = 20,100, to every printed digit:
   90.16 → 0.0670 (paper 0.067), 32.10 → 0.0400 (0.040), 0.86 → 0.0065 (0.0065).
2. "Self-replicating quotient" equals ln(N / L_SR) exactly:
   ln(20100/32.10) = 6.440 (paper 6.44); ln(20100/0.86) = 10.059 (paper 10.06).
   The paper describes it as a log likelihood ratio against a random network
   with outputs uniform on [−0.5, 0.5] landing in the same ε-ball. Read as a
   genuine 20,100-dimensional ball of radius sqrt(L_SR), that probability is
   e^(−36,203) for L_SR = 32.10 (e^(−72,581) for 0.86), so quotients of
   36,203 and 72,581 nats, not 6.44 and 10.06.
   The paper's number behaves like a one-dimensional calculation. I do not know
   what calculation the authors did; I only know the formula their numbers obey.
3. Parameter counts 20,100 and 21,100 force: no biases; two learnable 100×100
   matrices plus a 100→1 output (plus 100→10 for the auxiliary quine).
   Fig. 7 shows the two square matrices ("l0", "l1"), consistent with this.

### E0: initialization (the paper's "He init" does not fit its numbers)

An untrained network's predictions are uncorrelated with its weights, so its
L_SR ≈ Σθ² + Σf². The paper's 90.16 therefore requires Σθ² < 90, i.e. weight
RMS < 0.067.

Initial L_SR, mean (sd) over 5 seeds, linear output:

| weight init | projection std 1.0 | projection std 0.1 |
|---|---|---|
| He normal, std sqrt(2/100) = 0.141 | 94,636 (14,475) | 7,873 (1,494) |
| He uniform | 97,725 (14,197) | 7,450 (1,365) |
| LeCun normal, std 0.1 | 17,410 (2,615) | 1,396 (269) |
| PyTorch nn.Linear default, U(±0.1), std 0.0577 | 1,310 (202) | 115.7 (11.4) |

Only the PyTorch default keeps Σθ² (≈ 67) below 90. With it, varying the
coordinate-projection std: 0.004 → 67.0, 0.03 → 72.1, 0.05 → 80.7,
0.07 → 92.7, 0.1 → 115.7.

Choice: weights U(±0.1); coordinate projection N(0, 0.0577²), the same std as
the weights. Initial L_SR over 20 seeds: 86.7 (sd 5.8). Paper: 90.16.
With SELU on the output: 106.5 (sd 11.0). I keep the linear output; the
data cannot separate the two, and a regression output through SELU is odd.

Inference (moderate confidence): the original code most likely used PyTorch
default initialization throughout, despite the text saying He init. Further
support: Fig. 4's SGD curve plateaus near 66, which is about Σθ² under this
init, i.e. the loss of a network that predicts zero everywhere.

### E0 for the auxiliary quine

Initial L_Aux, mean (sd) over 5 seeds (paper: 1072.05; Fig. 8 shows
λ·L_Task ≈ 990 and L_SR ≈ 80 at epoch 0):

| image input | L_SR | λ·L_Task | L_Aux |
|---|---|---|---|
| standardized pixels, projection N(0, 1/784) | 892 | 2777 | 3669 (366) |
| raw [0,1], projection std of nn.Linear(784,50) default | 153 | 968 | 1121 (102) |
| raw [0,1], projection std 0.0577 | 460 | 1938 | 2398 (238) |
| standardized, projection std of nn.Linear default | 466 | 2011 | 2477 (173) |

Choice: raw [0,1] pixels, projection std 1/sqrt(3·784), the std of a frozen
default nn.Linear(784, 50). It matches L_Aux and λ·L_Task; its L_SR is
higher than Fig. 8 suggests (153 vs ~80), with large seed variance.

λ·L_Task ≈ 990 on 10,000 test images means L_Task is summed over the test
set, about 9.9 nats per image at temperature 0.01. My implementation sums.

### First observations (smoke tests, seed 99)

- One Adamax epoch: L_SR 87 → 62.5, prediction RMS 0.03 → 0.0067,
  relative error L_SR/Σθ² = 1.007. The network learned to output ≈ 0.
- One regeneration (T=1): L_SR 0.74, but weight RMS 0.056 → 0.0059 and
  relative error 1.07. The loss fell because the weights shrank tenfold.

### Batch 1 (E1, E2, E5–E8, σ sweep): process notes

- Regeneration with T=0, seed 1, diverged: L_SR overflowed to inf, and the
  quotient's log(0) raised. Fixed: the run now logs a "diverged" row and
  stops when θ is non-finite. The crash itself was correct behaviour.
- xargs aborted the batch on that failure. `run_all.sh` now skips jobs whose
  log already ends in "wrote results" and no longer aborts on one failure.
- Mistakes of mine, to avoid repeating: (1) `pgrep -f experiments.py` inside a
  waiting shell loop matches the loop itself, so it never ends; wait on a
  log line instead. (2) A monitor grepping a log file that a later job will
  overwrite fires on the stale content; write each batch to a new file.

### Batch 1 first results (seed 0 and 1)

- E1 reproduces Fig. 4 qualitatively: Adagrad turns upward after epoch 4;
  RMSprop explodes from epoch 1; SGD plateaus near 65 (paper ~66);
  Adamax lowest (best 41.9 at epoch 24, seed 0; paper ~33 at epoch 30).
- In every run L_SR/Σθ² stays between 0.90 and 1.01. Adamax seed 0: L_SR
  tracks Σθ² at every epoch (epoch 24: 41.87 vs 42.43), prediction RMS stays
  ~0.006 while weight RMS is ~0.046. The loss falls because the weights
  shrink, while the network keeps predicting roughly zero.
- E5 (T=1, seed 0): L_SR after regeneration 0.88 at generation 1 (paper's
  best: 0.86), but weight RMS 0.0067 (initial 0.058) and L_SR/Σθ² = 0.999.
- E6 (T=0): seed 0 shrinks for two generations then explodes to NaN by
  generation 6; seed 1 explodes from generation 1. The paper reports collapse
  to the zero quine.

### E6 mechanism: pure regeneration has a threshold in weight scale

`diag_regen_scale.py` (output: results/diag_regen_scale.txt): pure regeneration
(T=0) from the default initial weights multiplied by α, 15 generations.

| seed | α=0.25 | 0.5 | 0.75 | 1.0 | 1.5 |
|---|---|---|---|---|---|
| 0 | zero | zero | zero | diverged | diverged |
| 1 | zero | zero | diverged | diverged | diverged |
| 2 | zero | zero | zero | diverged | diverged |

Below threshold the RMS falls faster than geometrically
(seed 0, α=0.25: 4.8e-4 → 7.2e-8 → 8.5e-18 → exactly 0). Interpretation:
with every weight scaled by ε, the output w_out·selu(W2·selu(W1·h0)) is
roughly cubic in ε (h0 does not scale), so θ = 0 is a superstable fixed point
of θ ↦ f_θ(C) with a finite basin; outside the basin the map diverges.
The paper's "rapidly converges to the zero quine" and my divergence are
consistent with opposite sides of one boundary; which side the default
initialization lands on depends on unstated details.

### Container restarts kill background runs (2026-10-04)

The container restarted at least twice while runs were in progress. Lost:
the two 10,000-epoch hill-climbing runs (logs stop at 00:48, epoch 2,400) and
the first three He-init 1,000-epoch runs (stop at 04:27, epoch ~200). I reported
the hill-climbing runs as "still running" from their last log line without
checking that the processes were alive. Lesson: check `ps`, not only logs.
Dead logs kept as `*.died-at-restart.log`. He runs relaunched 05:01.

### Background jobs killed by the tool's time limit (2026-10-04, ~06:00)

The 2 x 2 grid runner (xargs) was started as a background tool command with
the default 30-minute limit. At the limit the tool killed it and its children:
the four second-wave runs died at epoch ~240 (logs kept as
`*.killed-by-tool-timeout.log`). The queued one-layer launcher had the same
limit and was stopped before it could start anything.
Fix: long batches now run fully detached (`nohup setsid script &`), so no
tool limit applies; monitors only read logs.
Repeated mistake: a monitor's `pgrep -f "experiments.py optimizer"` matched the
monitor's own command line (same error as before). Use `pgrep -f "[e]xperiments.py"`.
Rule for myself: any background command longer than a few minutes gets
detached, and any pgrep inside a script uses the bracket pattern.

### Out-of-memory kill (2026-10-04)

Two damped Newton (Levenberg–Marquardt) runs at once (two-layer: ~6-10 GB peak
for the 20,100² Jacobian, AᵀA and its Cholesky factor; one-layer: ~3 GB) plus
Adamax jobs exceeded the 15 GB memory limit; the kernel killed both. Lost: 3
two-layer iterations and 1 iteration of the 1 − R² run (logs kept as
`*.oom-killed.log`). Rule: damped Newton runs strictly one at a time; check
memory before launching anything large next to them.

### Compact checkpoints

All trained networks are committed in `results/weights/` as θ + constructor
settings + SHA-256 of P (`quine.save_weights` / `quine.load_weights`;
`export_weights.py`). Settings were recovered by searching for the ones that
regenerate the stored P exactly; forward-pass flags (embedding/output SELU) come
from each run's JSON. 93 of 112 reproduce their logged final SSE after reload;
the stage copies reproduce their source runs; the rest are MNIST or diverged.
New runs write a compact copy automatically.

### Second out-of-memory kill (2026-10-04, ~19:40)

The two-layer damped Newton run on 1 − R² reached 13.2 GB and was killed after
one iteration (log: `logs/lmnorm_L2_seed0.oom-killed-2.log`). Cause: the
normalized residual's rank-one correction `A.sub_(torch.outer(r, d) / S)`
allocated two extra N × N temporaries (3.2 GB each for N = 20,100). Fixed with
the in-place `A.addr_(r, d, alpha=-1/S)`; tests pass. Relaunched.
Also: the container restarted at ~19:30, while nothing was running.

### Third out-of-memory kill (2026-10-04, ~20:00)

The relaunched two-layer 1 − R² damped Newton run died after one iteration at
12.3 GB. Two causes: (1) a second code problem: on a damping retry the previous
Cholesky factor stayed alive while the next was computed (three 3.2 GB matrices
at once); fixed by `del L` before retrying, so at most two N × N matrices are
live (~6.5 GB); (2) I ran the grounding diagnostic (its own Jacobian, ~1-2 GB)
at the same time. Rule: nothing else heavy while a two-layer damped Newton run
is active. Log kept as `logs/lmnorm_L2_seed0.oom-killed-3.log`. Relaunched.
