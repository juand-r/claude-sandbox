# Neural Network Quine: a reimplementation

Paper: Oscar Chang and Hod Lipson, "Neural Network Quine", ALIFE 2018,
arXiv:1803.05859v4. Code, logs and raw results are in this directory; every
number below is printed by `summarize.py` from `results/*.json`, except where
a diagnostic script is named.

## Summary

I reimplemented the paper from its text. Several details are unstated, and
one stated detail (He initialization) is inconsistent with the paper's own
numbers. With an initialization chosen to match the paper's initial losses,
most of the paper's numbers reproduce:

- the initial loss of the untrained quine (86.7 ± 5.8 over 20 seeds; paper 90.16);
- the qualitative ranking of optimizers in its Fig. 4;
- the loss reached by regeneration (0.43 to 0.88 across three seeds; paper 0.86);
- the initial loss and final MNIST accuracy of the auxiliary quine
  (1064 and 89.7%; paper 1072 and 90.41%).

But the loss the paper reports, L_SR, can be lowered without any
self-replication: a network that outputs 0 for every coordinate scores
L_SR = Σθ², the sum of its squared weights, so shrinking the weights lowers
the loss. I therefore also tracked the ratio L_SR / Σθ². It is 1 for the
output-zero network and 0 for a perfect quine. At every solution the paper
reports, this ratio is between 0.94 and 1.02 in my runs. In this
reimplementation, none of the paper's methods produced a network that
predicts its own weights better than a network that outputs zero. The
reported drops in loss come from the weights getting smaller.

Two of the paper's claims did not reproduce at all:

- The cost of self-replication to classification accuracy. A network trained
  only to classify reached the same accuracy as the auxiliary quine (89.7%),
  not the paper's 96.33%.
- Regeneration without optimization collapsing to the all-zero network. With
  my initialization it diverges instead, for all three seeds. A scan over
  initial weight scale shows both outcomes exist, on either side of a threshold.

The paper reports no weight norms, so I cannot tell whether the authors'
networks were in the same regime as mine. Their regeneration result is
consistent with it: an RMS error of 0.0065 is what my runs produce when the
weights themselves have RMS 0.0046 to 0.0066.

## 1. The setup

A quine network takes a coordinate c, the index of one of its own weights,
and outputs a number f_θ(c), its estimate of the weight θ_c. Its loss is

    L_SR = Σ_c (f_θ(c) − θ_c)²,

summed over all N = 20,100 learnable weights. The coordinate enters as a
one-hot vector, mapped to the first layer by a fixed random projection (a
learnable projection would have more parameters than the network it is
supposed to describe). The network is a bias-free MLP with SELU activations:
projection to 100 units, then two learnable 100×100 matrices, then a 100→1
output. The auxiliary quine splits the first layer into 50 units for the
coordinate and 50 for a projected MNIST image, and adds a 100→10 classifier
head (N = 21,100).

Training methods, as in the paper:

- Gradient descent. Each epoch freezes a copy of the weights as targets, then
  visits every coordinate once in random minibatches of 10.
- Hill-climbing. For each minibatch, add Gaussian noise to every weight; keep
  the change if the minibatch loss against the frozen targets goes down.
- Regeneration. Alternate T epochs of Adamax with a step that overwrites
  every weight with the network's prediction of it.

## 2. Why L_SR alone is not enough

L_SR compares predictions with weights in absolute terms. A network that
predicts 0 everywhere has L_SR = Σθ², and so does a network whose
predictions are uncorrelated with its weights and very small. Any change that
shrinks the weights lowers L_SR, whether or not the network learns anything
about itself. The paper notices one form of this (the all-zero network has
L_SR = 0) but reports no quantity that separates shrinkage from prediction.

I report the relative error

    ρ = L_SR / Σθ².

ρ = 1 means the network is no better than predicting zero; ρ > 1 is worse;
ρ near 0 means the network reproduces its own weights. ρ is undefined for the
all-zero network, which is the trivial quine. A small L_SR with ρ ≈ 1 means
the weights are small and the network has not learned them.

## 3. Reproduction status

Mean (sd) over seeds 0 to 2 unless noted. "Paper" values are from its text or
read off its figures (marked ~).

| quantity | paper | this reimplementation | ρ in this reimplementation |
|---|---|---|---|
| initial L_SR, vanilla | 90.16 | 86.7 (5.8), 20 seeds | 1.25 (seed 0) |
| SGD, 30 epochs | plateau ~66 | 64.8 (0.1) | 0.98 |
| Adagrad | loss rises over time | best 64.2 at epoch 4, then rises to 74.9 | 0.99 at best |
| RMSprop | explodes | rises to 671 (165) | > 1 |
| Adamax, 30 epochs | ~33, best of the optimizers | best 41.8 (1.4), best of the optimizers | 0.985 |
| Adamax, 100 epochs | best 32.10 at the end | best still 41.8 at epoch ~25; rises to 58.8 by epoch 100 | 0.985 at best |
| hill-climbing, 10,000 epochs | 90 → ~64 | see section 6 | |
| hill-climbing from SGD solution | improves it significantly | see section 6 | |
| regeneration, T=1, G=10 | best 0.86 | best 0.88, 0.61, 0.43 (three seeds) | 0.999, 1.010, 1.000 |
| regeneration, T=0 | collapses to the zero quine | diverges, all three seeds | |
| auxiliary quine, initial L_Aux | 1072.05 | 1063.9 (53.0) | |
| auxiliary quine, L_SR over training | rises ~80 → ~260 | falls 138 → 63 | 1.02 at the end |
| auxiliary quine, test accuracy | 90.41% | 89.69% (0.81) | |
| classifier only, same network | 96.33% | 89.65% (0.71) | |

## 4. Gradient-based training (E1, E2)

Observation. The optimizers reproduce the shape of the paper's Fig. 4
(figure: `figures/e1_optimizers.png`). Every optimizer except RMSprop drops
from ~85 to between 62 and 67 in the first epoch. SGD then plateaus near 65, Adagrad turns
upward after epoch 4, RMSprop diverges, and Adamax goes lowest.

Observation. After the first epoch, ρ stays between 0.90 and 1.05 for every
optimizer except RMSprop (all epochs, all three seeds). The first-epoch drop is the network learning to
output almost nothing: for Adamax, seed 0, the prediction RMS falls from
0.030 to 0.0067 while the weight RMS stays at 0.056. By epoch 24
Adamax has lowered L_SR from 62 to 42, and Σθ² has fallen in step, from 62 to 42.

| Adamax, seed 0, epoch | 0 | 1 | 5 | 10 | 24 | 50 | 100 |
|---|---|---|---|---|---|---|---|
| L_SR | 83.8 | 62.5 | 55.0 | 48.4 | 41.9 | 42.8 | 53.7 |
| Σθ² | 66.8 | 62.1 | 55.2 | 48.7 | 42.4 | 43.2 | 54.8 |
| prediction RMS | 0.030 | 0.0067 | 0.0047 | 0.0053 | 0.0056 | 0.0064 | 0.0069 |

Interpretation. Within this reimplementation, gradient training of the
vanilla quine finds the output-zero solution within one epoch and then
lowers the loss by lowering the weight norm. I have not analysed why Adamax
shrinks the weights; the gradient of L_SR flows only through the predictions
(the targets are frozen within an epoch), so the shrinkage is an indirect
effect of the updates, not a direct pull toward zero.

One difference from the paper: my Adamax loss reaches its minimum around
epoch 25 and then rises (to 58.8 at epoch 100), whereas the paper's falls
to 32.10 at epoch 100. With SELU on the output layer (section 9) Adamax reaches
32.3 by epoch 30, again with ρ = 0.986.

## 5. Regeneration (E5, E6)

### 5.1 With optimization (T = 1)

Observation. After the first generation, L_SR measured after each
regeneration is 0.43 to 1.1 across three seeds, the paper's order of
magnitude (0.86). The weight RMS at that point is 0.0046 to 0.0074, about a
tenth of its initial value 0.058, and ρ is 0.998 to 1.013 (figure:
`figures/e5_regeneration.png`). Measured instead just after each Adamax
epoch, ρ is lower, 0.45 to 0.74.

The paper says of this solution: "the order of magnitude of the weights are in
line with what we would observe in a normal neural network". In my runs it is
not: the weights are an order of magnitude smaller than at initialization,
and about the size of the prediction error.

Mechanism test. `diag_regen_cycle.py` (output: `results/diag_regen_cycle.txt`)
follows one seed through four generations. Call the weights just after a
regeneration θ_R. During the next Adamax epoch:

- the network learns to output θ_R: relative error against θ_R falls to
  0.002 to 0.023;
- its own weights move to θ_R + Δ, with |Δ|² ≈ |θ_R|² (0.81 to 1.50 versus
  0.88 to 0.90);
- regeneration then writes θ_R back (relative change 0.002 to 0.023), and
  the network with weights θ_R predicts almost nothing (prediction RMS 7e-5).

Interpretation. Regeneration in this setting alternates between two
networks: one (θ_R + Δ) prints the other (θ_R), and the other prints
nothing. Neither prints itself. The ρ ≈ 0.5 seen after the Adamax epoch comes
from the θ_R part of θ_R + Δ, which the network reproduces; the Δ part it does
not. The loss the paper reports at the end of a generation (0.86 in the paper)
is the loss of the network that prints nothing, made small by its small weights.

### 5.2 Without optimization (T = 0)

Observation. Pure regeneration diverged for all three seeds: the weight RMS
falls for one or two generations, then grows without bound (seed 0: 0.030,
0.014, 0.065, 4.4, 4.9e4, 6.6e15) until the loss overflows.

Mechanism test. `diag_regen_scale.py` (output: `results/diag_regen_scale.txt`)
repeats pure regeneration with the initial weights multiplied by α:

| seed | α = 0.25 | 0.5 | 0.75 | 1.0 | 1.5 |
|---|---|---|---|---|---|
| 0 | zero | zero | zero | diverges | diverges |
| 1 | zero | zero | diverges | diverges | diverges |
| 2 | zero | zero | zero | diverges | diverges |

Below the threshold the weights collapse to exactly zero within four to six
generations, faster than geometric decay (seed 0, α = 0.25: RMS 4.8e-4,
7.2e-8, 8.5e-18, 0).

Interpretation. If every weight is scaled by ε, the output
w_out · selu(W2 · selu(W1 · h0)) scales roughly as ε³, because the first-layer
input h0 comes from the fixed projection and does not scale. So the all-zero
network is a strongly attracting fixed point of regeneration, but only within
a basin; outside it, the map diverges. The paper's observation (collapse to
zero) and mine (divergence) fit opposite sides of the same boundary. Which
side a run lands on depends on the initial weight scale, which the paper does
not pin down (section 9).

## 6. Hill-climbing (E3, E4)

Observation, noise sweep (50 epochs, figure: `figures/e3_hill_sweep.png`).
The acceptance rate is 49 to 52% for every noise level from σ = 1e-5 to 3e-3.
With σ ≥ 3e-4 the loss rises, and Σθ² rises with it (σ = 1e-3: Σθ² from 67 to
1043 in 50 epochs). The lowest loss after 50 epochs was at σ = 3e-5 (71.4).

Interpretation. Each step perturbs all 20,100 weights but checks only 10
predictions, against frozen targets. The check is close to a coin flip, so
the accepted steps are close to a random walk, and a random walk in weight
space inflates Σθ², which raises the next epoch's loss. Small σ limits the
damage. The paper does not state σ.

[E3 full-length runs and E4: to be filled in when the runs finish.]

## 7. The auxiliary quine (E7, E8)

Observation. The initial losses match the paper: L_Aux = 1063.9 (53.0) versus
1072.05, with λ·L_Task = 926 (30) versus ~990 in Fig. 8. After 30 Adamax
epochs the test accuracy is 89.69% (0.81), versus 90.41% in the paper
(figure: `figures/e7_auxiliary.png`).

Observation. Two results differ from the paper.

- L_SR falls, from 138 (24) to 63.0 (0.5), and ends at ρ = 1.02. In the
  paper it rises from ~80 to ~260 over 30 epochs.
- The same network trained on λ·L_Task alone, with the same epochs and the
  same image sampling, reaches 89.65% (0.71), the same as the quine. The
  paper reports 96.33% and reads the gap as self-replication taking up
  network capacity.

Interpretation. In this reimplementation the self-replication term does not
compete with classification, because it is satisfied by the output-zero
solution, which costs the classifier nothing. Without the L_SR term, L_SR
grows to 234 (65), i.e. the classifier-only network's weight output drifts;
with it, the output stays near zero. The accuracy curves of the two runs are
nearly identical epoch by epoch.

I cannot explain the 96.33% baseline. My baseline sees 21,100 training images
per epoch (one per coordinate), about 10.5 passes over MNIST in total, and its
input is a fixed random projection of 784 pixels to 50 numbers. The paper does
not say how its baseline was trained; it may have used full passes over the
data or a learnable input layer. This is a guess.

## 8. The paper's two derived metrics

Both formulas below are inferred from the paper's numbers, not stated in it.

The "average weight prediction margin" is described as the average absolute
difference between weights and predictions. The reported values equal the
RMS error sqrt(L_SR / N) to every printed digit: 90.16 → 0.0670 (paper 0.067),
32.10 → 0.0400 (0.040), 0.86 → 0.0065 (0.0065). The mean absolute error is
smaller; in my seed-0 initial network it is 0.0541 against an RMS error of 0.0646.

The "self-replicating quotient" is described as a log likelihood ratio: how
much more likely a perfect copy is under the network's noisy copying than by
chance, with chance modelled as outputs uniform on [−0.5, 0.5]. The reported
values equal ln(N / L_SR): ln(20100 / 32.10) = 6.440 (paper 6.44) and
ln(20100 / 0.86) = 10.059 (paper 10.06). Taken literally, the chance that a
uniform random point lands in the 20,100-dimensional ball of radius
sqrt(L_SR) around the weights is e^(−36,203) for L_SR = 32.10 and
e^(−72,581) for 0.86, which would give quotients of tens of thousands of
nats. I do not know what calculation the authors intended. Either way, both
metrics are functions of L_SR alone and so inherit its blindness to weight
shrinkage.

## 9. Unstated details, and how much they matter

PLAN.md lists every detail the paper leaves open and the choice made. Two
choices were not forced by the paper's numbers and could change the results.

Initialization. The paper says He et al. (2015). An untrained network's
predictions are unrelated to its weights, so its L_SR is about
Σθ² + Σ f². He-normal weights give Σθ² ≈ 402 on their own, so the paper's
initial 90.16 is out of reach; I measured 94,636 (14,475) with a unit-variance
projection and 7,873 (1,494) with a 0.1 projection. PyTorch's default
nn.Linear initialization, uniform on ±1/√100, gives Σθ² ≈ 67, and with the
coordinate projection at the same scale the initial L_SR is 86.7 (5.8) over
20 seeds. The same choice, together with a default nn.Linear(784, 50) on raw
[0, 1] pixels for the image projection, matches the auxiliary quine's initial
L_Aux and λ·L_Task. A further hint: the SGD plateau in the paper's Fig. 4
(~66) is close to Σθ² under this initialization, the loss of predicting
zero. My inference, with moderate confidence, is that the original code used
PyTorch's default initialization. NOTES.md has the full comparison.

SELU on the output. "Every layer is followed by a SeLU" can include the
scalar weight output. I left it linear. Both versions give initial losses
consistent with 90.16 (86.7 vs 106.5 mean over 20 seeds).

Sensitivity runs, seed 0:

| variant | Adamax, 30 epochs: best L_SR | ρ at best | regeneration (T=1) |
|---|---|---|---|
| defaults | 41.9 | 0.987 | best L_SR 0.881, weight RMS 0.0066, ρ 0.999 |
| SELU on the weight output | 32.3 | 0.986 | best L_SR 1.241, weight RMS 0.0079, ρ 0.999 |
| literal He init, N(0, 1) projection | 237 (from 97,831) | 0.771 | diverges (non-finite at generation 5) |

SELU on the output changes the numbers, not the conclusion. The literal He
initialization is a different regime: the loss starts three orders of
magnitude above the paper's, regeneration diverges, and it is the only
setting in which any method reached ρ clearly below 1.

[Literal-He Adamax at 100 epochs: to be filled in.]

## 10. Alternative explanations and remaining uncertainty

- My implementation could differ from the authors' in a way that matters.
  The forced details (no biases, layer sizes, minibatch of 10, frozen targets
  per epoch) and the matched initial losses limit the room for this, but do
  not remove it. The unforced choices are listed in PLAN.md.
- The authors' networks may have had larger weights than mine at the
  reported losses. The paper does not report weight norms, and Fig. 7 is
  log-normalized, which hides scale. Their regeneration figures (L_SR 0.86,
  RMS error 0.0065) are what my runs produce with weight RMS 0.005 to 0.007.
- Regeneration's outcome depends on initial scale (section 5.2), so another
  initialization could behave differently. Under the one other initialization
  I tried, the paper's literal He init, regeneration diverged.
- The tests (tests/test_quine.py) check the parameter layout, the forward
  pass against an explicit one-hot computation, the loss against a
  brute-force loop, simultaneous regeneration, hill-climbing acceptance, and
  frozen targets. They do not check the training dynamics against the paper,
  which is what this report is for.

## Reproduction

    ./run_all.sh                     # all runs, ~3 h on 4 CPU cores (hill-climbing dominates)
    .venv/bin/python summarize.py    # tables
    .venv/bin/python plots.py        # figures
    .venv/bin/python diag_regen_scale.py
    .venv/bin/python diag_regen_cycle.py

Seeds 0, 1 and 2; PyTorch 2.14.1 on CPU, one thread per run.
