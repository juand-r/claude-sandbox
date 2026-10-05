# Ideas and planned experiments

Further work beyond reproducing the paper. Goal: get the plain quine (no MNIST)
to genuinely reproduce its own weights, measured by R² (section 0). MNIST comes
only after that works.

Everything below marked "guess" or "hypothesis" is untested.

## 0. Conventions

- Model (embedding view): f_θ(c) = wᵀ σ(W₂ σ(W₁ p_c)), σ = selu, p_c = row c of
  the fixed random table P ∈ ℝ^(20,100 × 100). θ = (W₁, W₂, w), N = 20,100.
  The original implementation also applies σ to p_c (see idea 2).
- SSE = Σ_c (f_θ(c) − θ_c)² (the paper's L_SR).
- Success metric: R² = 1 − SSE / Σ_c (θ_c − mean θ)². R² = 1 is a perfect copy;
  R² = 0 is no better than guessing the mean weight. SSE alone rewards shrinking
  the weights and cannot tell copying from guessing zero.
- To do (approved for later): replace ρ = SSE / Σθ² with R² in REPORT.md.

## 1. Does the scale of P matter, separately from the weight scale?

Motivation. The two setups run so far change two things at once:

| setup | initial weight std | P scale s | result |
|---|---|---|---|
| default (matches paper's numbers) | 0.058 | 0.058 | R² ≈ 0 |
| He (matches paper's text) | 0.141 | 1 | R² ≈ 0.63 at epoch 100, ~0.75 at 200 |

So we cannot tell whether He works because of its larger weights, its larger P,
or both.

Hypothesis (reasoned, untested). Scale should matter more here than in an
ordinary network. In an ordinary network a fixed scale on p_c is absorbed by
W₁. Here W₁'s entries are also outputs the network must produce: a small P
forces a large W₁, which then has to be reproduced. The self-reference couples
the scale of P to what must be copied.

Test. Fill the 2 × 2 grid: default weights with s = 1, and He weights with
s = 0.058. Plain version, Adamax, 3 seeds each.

Prediction made before running (from activation sizes at initialization:
default setup h0..h2 RMS ~0.05-0.08, He setup ~1-1.6): the P scale matters more;
default weights + large P should work, He weights + small P should fail.

Result (two hidden layers, Adamax, 1,000 epochs, 3 seeds; `summarize.py`
table_grid; R² averaged over epochs 901-1000):

| | P scale 0.058 | P scale 1 |
|---|---|---|
| default weights | 0.39-0.43 | ≈ 0 (−0.03); weights collapse to RMS 0.02 |
| He weights | 0.55-0.57 | 0.84-0.86 |

The prediction was wrong. Default weights with large P is the one cell that
stays trapped at the guess-zero state. Small P does not prevent learning.

Second finding: the default/default cell, which is the setup that matches the
paper, does learn when trained long enough. It shrinks its weights until epoch
~50 (SSE minimum ~42, close to the paper's best of 32.10), then the weights grow
and R² rises steadily: 0.01 at epoch 100, 0.20 at 400, 0.44 at 1,000 (seed 0),
still rising. SSE rises at the same time (to ~1,290), because it grows with the
weights. So the paper stopped at 100 epochs, inside the shrink phase, and
selecting the lowest SSE picks the checkpoint just before learning starts.

Open: why does small-weight + large-P collapse? Not yet investigated.

### One hidden layer (N = 10,100): same grid

Requested by the user: f_θ(c) = wᵀ σ(W₁ σ(p_c)), θ = (W₁, w). Adamax, 1,000
epochs, 3 seeds per cell, R² averaged over epochs 901-1000:

| | P scale 0.058 | P scale 1 |
|---|---|---|
| default weights | 0.45-0.56 | ≈ 0 (−0.15); weights collapse to RMS 0.01 |
| He weights | 0.79-0.80 | 0.87-0.89 |

Same pattern as two layers, and the one-layer network copies itself as well
or better in every cell that learns. Mean R² at epochs 100 / 400 / 1,000:

| cell | two layers | one layer |
|---|---|---|
| default weights, P 0.058 | 0.01 / 0.23 / 0.43 | 0.09 / 0.39 / 0.50 |
| He weights, P 0.058 | 0.20 / 0.40 / 0.57 | 0.30 / 0.67 / 0.80 |
| He weights, P 1 | 0.61 / 0.81 / 0.85 | 0.60 / 0.81 / 0.88 |

Interpretation (tentative): the one-layer network has half as many weights to
reproduce with the same 100-unit width, so it has more capacity per weight it
must copy. Not tested beyond this grid.

## 2. SELU on the embedding lookup

Question raised: is P a layer (σ applied after it) or an embedding table (no
σ)? Both are the same matrix product on a one-hot input; the only difference is
whether σ is applied to p_c. The paper's "every layer is followed by a SeLU"
suggests σ; standard embedding practice suggests not.

Measured so far (seed 0 addresses): σ changes pairwise distances between
addresses by ~2% on average (correlation of distances before vs after: 0.94 at
s = 1, 0.97 at s = 0.058). At s = 1 the mean, length and angle statistics are
unchanged, because SELU is designed to keep mean 0 and variance 1 for standard
normal input; the shape of each entry's distribution changes (negatives squashed
toward −1.76). Training at epochs 20 and 30: no difference beyond seed spread.

Result (He init, Adamax, 1,000 epochs, 3 seeds each): no detectable difference.
Mean R² over seeds, averaged over the last 100 epochs: 0.850 with σ, 0.848
without. Seed-to-seed spread (0.80 to 0.87 at epoch 1,000) is larger than the
gap. Mean best R²: 0.869 with, 0.866 without. Tested only at P scale s = 1.

## 3. Does the distribution of P matter (Gaussian vs other)?

Guess: less than the scale. Random 100-dimensional vectors of the same scale
look alike geometrically: similar lengths, nearly perpendicular.

Test (if idea 1 shows P matters): compare Gaussian, uniform and ±1 entries at
the same scale.

## 4. Random addresses versus structured addresses

Motivation: how close to perpendicular are the addresses? Measured on the He P
(seed 0, 100,000 random pairs): cosine mean 0.000, sd 0.100 (= 1/√100, as
expected for random directions); the middle 90% of angles lie between 80.5°
and 99.5°. The closest of all 202 million pairs is at 57° (cosine 0.55).
At most 100 vectors can be exactly perpendicular in 100 dimensions; 20,100
random ones fit because each leans slightly toward every other.

Hypothesis (untested): near-perpendicularity helps in one way and may hurt in
another.

- Helps: telling coordinates apart. The network is a smooth function, so
  nearby addresses get nearby outputs (the paper's own argument for one-hot
  coordinates instead of feeding in c as a number). Random addresses are already
  far apart, so making them more perpendicular would add little.
- May hurt: no shared structure. A random address says nothing about which
  layer, row or column a weight belongs to. The network must then memorize
  20,100 unrelated numbers with 20,100 parameters, with no slack.

A quine chooses its own targets. It could make its weights easy to predict,
for example a smooth function of their addresses, but only if the addresses
carry structure. With random addresses there is nothing to be smooth in.

Guess: perpendicularity is not the bottleneck; lack of structure may be.

Test: random P versus a structured P whose address for weight (layer ℓ, row i,
column j) is built from a layer vector, a row vector and a column vector (e.g.
concatenated or summed). Plain version, He init. Related: the paper's own
future-work suggestion of low-rank weight matrices (Denil et al. 2013).

## 5. Optimize what we measure

The paper minimizes SSE, which rewards shrinking the weights. Train on the
relative error directly, SSE / Σθ² (or 1 − R²), so that shrinking does not help.
Proposed earlier; deferred by the user.

## 6. Full gradient instead of frozen targets

The paper freezes the targets θ̄ for each epoch, so the gradient flows only
through f_θ. The true gradient of SSE also has a term from the target,
−2 (f_θ(c) − θ_c) e_c. Try the full gradient. (My suggestion; not discussed yet.)

## 7. Push the He-init run further

Done (idea 2 runs). R² rises fast to ~0.81 by epoch 400, then slowly, to
~0.85 (mean over seeds) by epoch 1,000; best single epoch 0.85 to 0.88. The
weights keep growing throughout (RMS 0.14 at start, ~0.39 at epoch 1,000), so
SSE rises to 380 to 610 while R² improves.

## 8. Housekeeping

- Draw P from its own random generator, so P depends only on the seed. Today
  P shares a generator with the weight initialization, so the default and He
  setups get different draws of P, not just different scales. Changing this
  alters P for future runs. (Asked; not yet decided.)
- Long runs die when the container restarts (two did: the 10,000-epoch
  hill-climbing runs at epoch 2,400 and the first He 1,000-epoch runs at epoch
  ~200). Add periodic checkpoints so runs can resume, and check that processes
  are alive, not only that logs exist.
- Rerun the two 10,000-epoch hill-climbing runs (paper reproduction, E3).

## 9. Pushing R² toward 1 (current best: 0.87-0.89, one layer, He weights, P scale 1)

Goal set by the user: R² as close to 1 as possible, plain version only. The
collapse of small-weight + large-P is parked.

Diagnostic (`diag_gap.py`, seed 0 networks after 1,000 epochs). Is the
remaining error a failure to fit the frozen targets, or drift of the weights
during an epoch? One extra epoch from the saved network:

| network | R² now | lr 2e-3 (current) | lr 2e-4 | lr 2e-5 |
|---|---|---|---|---|
| one layer | 0.870 | 0.876 | 0.930 | 0.919 |
| two layers | 0.874 | 0.848 | 0.911 | 0.900 |

Drift is negligible (|Δθ|² < 0.1% of the weights' variance per epoch); R²
against the frozen copy equals R² against the current weights. The limit is
the learning rate: Adamax moves every weight by up to lr per step, so at the
paper's fixed 2e-3 the weights jitter around a better solution.

Plan, in order (each step decided by the previous result):

1. Learning-rate decay. Continue the six best networks at lr 2e-4 for 300
   epochs (running). Then try a schedule from scratch (e.g. cosine decay).
2. Loss that cannot be lowered by shrinking: train on SSE / Σ(θ − mean θ)²
   (= 1 − R²) instead of SSE (idea 5).
3. Full gradient through the target (idea 6), likely only safe together with 2,
   since pulling the weights toward the predictions also favours θ = 0.
4. Architecture: width of the hidden layer; structured addresses (idea 4).

### Section 9 results so far (one hidden layer unless stated; He weights, P scale 1)

R² per seed (0 / 1 / 2) after each stage, each stage continuing from the previous:

| stage | one layer | two layers |
|---|---|---|
| Adamax lr 2e-3, 1,000 epochs | 0.87 / 0.87 / 0.90 | 0.87 / 0.84 / 0.83 |
| + 300 epochs at lr 2e-4 | 0.947 / 0.959 / 0.966 | 0.945 / 0.933 / 0.947 |
| + 300 epochs at lr 2e-5 | 0.955 / 0.964 / 0.970 | 0.955 / 0.943 / 0.955 |
| + 300 epochs, full gradient, lr 2e-5 | 0.960 / 0.967 / 0.973 | 0.962 / 0.952 / 0.962 |
| (control: + 300 epochs, frozen targets) | 0.958 / 0.966 / 0.971 | 0.961 / 0.951 / 0.961 |
| + 20 iterations of damped Newton (Levenberg–Marquardt) on SSE | 0.983 / 0.985 / 0.987 | 0.971 (seed 0 only) |

Pure Newton fails: J − I has condition number ~5e6 and the linear model holds
only for steps ~1e-6 of the Newton step (`diag_newton.py`). Damped Newton works.

One layer, seed 0, 80 more damped Newton iterations from 0.9832:
on SSE 0.98515; on 1 − R² 0.98526. Both stall at the same value. (Correction,
later: not a local optimum. A fresh damped Newton start from the stalled network
reached 0.9884 in 10 iterations; the stall came from the damping μ ratcheting up
over a long run. A random 1% change plus repair reached 0.9901. See NOTES.md.)

Two layers, seed 0, damped Newton: 0.9545 → 0.9713 in 20 iterations (~2 min
each), still rising ~0.0008 per iteration at the end, damping falling.

Two layers, the recipe that now works best (seeds 0 / 1 / 2; REPORT.md sections
13 and 14):

| stage | R² |
|---|---|
| from random init: Adamax, full gradient, 1 − R² loss, lr 2e-3, 1,000 epochs | 0.940 / 0.942 / 0.939 |
| + 300 epochs at lr 2e-4 | 0.9926 / 0.9927 / 0.9926 |
| + 300 epochs at lr 2e-5 | 0.9941 / 0.9941 / 0.9945 |
| + damped Newton on 1 − R², old damping rule, 10 iterations, reset, 10 more | 0.99753 (seed 0 only) |
| (instead: Nielsen damping rule, 20 iterations) | 0.99659 (seed 0 only) |

Next candidates: the same damped Newton schedule on seeds 1 and 2; repeated
cycles of a 10% random change followed by repair (see section 10), against
plain restarts with the same number of iterations.

## 10. Reading off versus computing one's own state (introspection)

Motivation (discussion with the user). There are two ways a network can report
its own weights.

- Reading off. With one-hot addresses feeding straight into the weights, the
  report is a lookup: f(r, c) = e_rᵀ M e_c = M_rc. Every weight setting is then a
  perfect quine; nothing is learned. This is the neural analogue of a "cheating"
  program quine that prints its source by opening its own file. In linear form,
  with fixed addresses z_c stacked as Z, the quine condition is Zᵀθ = θ: quines
  are eigenvectors of Zᵀ with eigenvalue 1. One-hot addresses give Z = I, so every
  θ is a quine; shuffled one-hot addresses (a permutation) allow exactly the θ
  that are constant on each cycle; random addresses generically allow only θ = 0.
- Computing. With random addresses (the paper's fixed random table P), the
  network cannot look its weights up; it must compute outputs that happen to
  equal them. That is a learned self-model, not access.

Measurement (`diag_grounding.py`; output in
`results/diag_grounding_lm_L1_seed2.txt`). Causal test: if weight c is nudged,
does the report of weight c move with it? The self-sensitivity ∂f(c)/∂θ_c, the
diagonal of the Jacobian, is 1 for a reading-off network. For the best network
(one layer, seed 2, R² 0.987):

| block | weights | mean ∂f(c)/∂θ_c | median share of the report's sensitivity going to its own weight |
|---|---|---|---|
| W₁ (hidden layer) | 10,000 | 0.0001 | 0.0012 |
| w (output layer) | 100 | 0.95 | 0.044 |

Typical sensitivity of one report to all weights together, |J_c,:|: 38.

Observation. Hidden-layer weights are reported accurately but not causally: a
report does not depend on the weight it describes, only on the weights
collectively. Output weights are reported with self-sensitivity close to 1.

Interpretation, checked and rejected (2026-10-05). For an output weight w_j,
∂f/∂w_j equals h_j, the value of hidden unit j at w_j's own address. I guessed
that a mean of 0.95 meant a one-hot lookup channel (h_j ≈ 1, other units ≈ 0).
The check says no: h_j(c_j) has mean 0.95 but standard deviation 2.84, and the
other units are larger on average (mean |h_k(c_j)| 2.24). The mean of 0.95 is an
average of scattered values. Same for two layers (mean 4.07, sd 9.95; other
units 7.22).

Two layers (seed 0, R² 0.9941; `results/diag_grounding_L2_stage3fn_seed0.txt`):
mean ∂f(c)/∂θ_c is 0.0009 for W₁, 0.0008 for W₂, 4.07 for w; |J_c,:| median 121.

Connection to work on introspection in language models (from memory; check
before citing): Binder et al. (2024, "Looking Inward") test whether models
predict their own behaviour better than other models trained on that behaviour;
Lindsey (Anthropic, 2025) injects concepts into activations and separates
accuracy of a self-report from its grounding (causal dependence on the state it
describes) and internality (the dependence does not run through the model's own
outputs). The quine separates accuracy from grounding in a 10,000-weight system
where everything is measurable: R² 0.99, yet almost no per-weight grounding. An
accurate self-report alone is weak evidence of access to the state reported.

Questions and tests:

1. Verify the lookup channel for the output weights (above).
2. Does grounding of hidden-layer reports change with training, depth, or
   address structure (section 4)? Compute the table above for the other saved
   networks, including the paper-matching ones (R² ≈ 0) as a baseline.
3. Can grounding be trained? Add a term rewarding ∂f(c)/∂θ_c ≈ 1, and see what
   it costs in R².
4. Fragility. With every report depending strongly on all weights (|J_c,:| ≈
   38), small damage anywhere may corrupt many reports at once. Damage random
   weights and measure how many reports go wrong, and whether one regeneration
   step or a few optimization steps repair it (the paper's self-repair
   motivation).

### Section 10 result: change, then repair (`diag_absorb.py`, `results/diag_absorb.json`)

Start: one layer, seed 0, R² 0.9853 (`lmnorm_L1_seed0_cont80`). One random change
Δ of each size, then 10 iterations of damped Newton on 1 − R², compared with a
control run from the unchanged network. Singular values of J − I at the start:
3 below 0.001, 19 below 0.01, 178 below 0.1, 1,736 below 1 (of 10,100).

| run | R² after change | R² after 10 repair iterations | fraction of Δ kept | other movement / |Δ| |
|---|---|---|---|---|
| control | 0.9853 | 0.9884 | | |
| |Δ| = 1% of |θ| | 0.807 | 0.9904 | 0.09 | 3.4 |
| |Δ| = 10% of |θ| | −21.2 | 0.9899 | 0.14 | 1.4 |

Observation. Repair restores the network from heavy damage (R² −21 → 0.99 in 10
iterations), keeps only 9-14% of the change, and ends far from the control's end
point, at a slightly better R².

Interpretation (one network, one Δ per size). The near-quines form a broad region:
a change is neither absorbed nor undone; the network re-settles elsewhere in the
region. For pushing R² up, "change, then repair" beat plain continuation twice;
worth trying repeatedly (perturb-and-repair cycles), together with a damping
schedule that does not ratchet up. Saved networks: `results/weights/absorb_*.pt`.

Two layers (seed 0, from R² 0.9941; `results/diag_absorb_L2.json`; REPORT.md
section 16). Singular values of J − I: 4 below 0.001, 34 below 0.01, 336 below
0.1, 2,976 below 1 (of 20,100); largest 7,505.

| run | R² after change | R² after 10 repair iterations | fraction of Δ kept | other movement / |Δ| |
|---|---|---|---|---|
| control | 0.9941 | 0.9965 | | |
| |Δ| = 1% of |θ| | −0.26 | 0.9965 | 0.085 | 1.30 |
| |Δ| = 10% of |θ| | −152 | 0.9975 | 0.127 | 1.04 |

Same picture as one layer: the change is mostly not kept, the network re-settles
about one change-size from the control. Much more fragile (1% change → R² −0.26).
The 10% change again ended above the control (0.9975 vs 0.9965). Saved networks:
`results/weights/absorb_L2_*.pt`.
