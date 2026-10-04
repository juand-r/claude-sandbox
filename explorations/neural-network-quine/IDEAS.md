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

Open decision (asked, not yet answered): run these at 1,000 epochs after the
current He runs finish, or run 100 epochs now as a first look.

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
