# Plan: reimplement "Neural Network Quine" (Chang & Lipson, 2018)

Paper: arXiv:1803.05859v4. A local copy is in `paper/quine.pdf`.

## What the paper does

A network takes a one-hot coordinate c (one per learnable weight) and outputs
a scalar, its guess of weight Θ_c. The self-replicating loss is
L_SR = Σ_c (f_Θ(c) − Θ_c)². The one-hot vector is mapped to the first layer
by a fixed random projection (it cannot be learnable: it would be larger than
the network it describes). Three training methods: gradient descent,
hill-climbing, and "regeneration" (replace Θ by f_Θ(C), alternating with
optimization). An "auxiliary quine" also classifies MNIST.

## Experiments to reproduce

| # | Experiment | Paper's result |
|---|---|---|
| E0 | Initial L_SR of vanilla quine | 90.16 |
| E1 | SGD, SGD+momentum, Adam, Adagrad, Adamax, RMSprop, 30 epochs (Fig. 4) | Adamax best (~33); Adagrad rises; RMSprop explodes |
| E2 | Adamax for 100 epochs | best test L_SR 32.10 |
| E3 | Hill-climbing, 10,000 epochs (Fig. 5) | 90 → ~64; ~5000 epochs to match SGD at 10 epochs |
| E4 | Hill-climbing started from SGD and from Adamax solutions | helps SGD, not Adamax |
| E5 | Regeneration, T=1 Adamax, G=10 (Fig. 6) | L_SR 0.86 |
| E6 | Regeneration with T=0 | collapses to the zero quine |
| E7 | Auxiliary quine, Adamax, 30 epochs (Fig. 8) | init L_Aux 1072.05; L_SR rises; test acc 90.41% |
| E8 | Same network, classification only | 96.33% |

## Unstated details and my resolutions

Each is a guess unless marked "forced". Logged with evidence in NOTES.md.

1. Biases: none. Forced by the parameter counts: 2·100·100 + 100 = 20,100
   and 20,100 + 100·10 = 21,100. Any biases would break both counts.
2. Layer structure: one-hot → fixed projection → 100 units → W1 (100×100)
   → W2 (100×100) → output. Forced by the count above and by Fig. 7, which
   shows two square weight matrices "l0" and "l1".
3. SELU placement: after the projection layer and after W1, W2. Whether the
   scalar weight output also passes through SELU is unclear ("every layer is
   followed by a SeLU"). Make it a flag; check both.
4. Projection distribution: not stated. Default N(0, 1) entries, so the
   first layer sees unit-variance input, the regime SELU is designed for.
5. Initialization: paper says He et al. (2015). But He-normal with fan_in=100
   gives E[Σw²] ≈ 402, and an untrained network's L_SR is roughly Σw² + Σf²,
   so ~400, not 90.16. Test several schemes and see which reproduces 90.16.
6. Minibatch loss: sum of squared errors over the 10 coordinates, as in Eq. 2.
   Targets Θ_t are a detached snapshot taken at the start of each epoch.
7. "Test loss": L_SR over all coordinates with the current weights as
   targets, computed at the end of each epoch.
8. Hill-climbing: per minibatch, perturb all parameters with N(0, σ²) noise;
   accept if the minibatch loss (snapshot targets) strictly decreases. σ is
   not given; pick by a short sweep and report the sweep.
9. Regeneration: the optimizer state is kept across generations (not stated).
10. Auxiliary quine pairing: each forward pass takes a coordinate and an
    image together. Training: each coordinate in the epoch's permutation is
    paired with a random training image. Test: fixed pairing, coordinate
    c with test image (c mod 10000), and test image i with coordinate i.
11. Auxiliary loss scaling: L_Aux = L_SR + λ·L_Task, λ = 0.01, L_Task the
    summed cross-entropy; softmax temperature 0.01 means softmax(z / 0.01).
12. MNIST input: standardize pixels (mean 0.1307, std 0.3081), then a fixed
    N(0, 1/784) projection to 50 units.
13. Classification-only baseline (E8): same architecture and epoch
    structure, loss λ·L_Task only.

## Derived metrics (from the paper's numbers, see NOTES.md)

- "Average weight prediction margin" = sqrt(L_SR / N) (RMS, not mean abs).
- "Self-replicating quotient" = ln(N / L_SR).
Report both, plus the relative error L_SR / Σ_c Θ_c², which the paper does
not report and which is the right check against the zero quine.

## Steps

- [x] quine.py: model, coordinate indexing, losses, training loops
- [x] tests (11, passing)
- [x] E0 initialization diagnostic → PyTorch-default init (NOTES.md)
- [x] E1, E2 (3 seeds)
- [x] E5, E6 (3 seeds) + diagnostics: diag_regen_scale.py, diag_regen_cycle.py
- [x] E3 σ sweep; [ ] E3 10,000 epochs (σ = 1e-5, 3e-5; running)
- [ ] E4 from SGD and Adamax solutions (σ = 3e-5 running; σ = 1e-5 queued)
- [x] E7, E8 (3 seeds)
- [x] sensitivity: literal He init, SELU output; [ ] literal He, Adamax 100 epochs (running)
- [x] REPORT.md draft; [ ] fill in E3, E4, literal-He 100 epochs

Changes of direction: item 5 (init) resolved against the paper's text, see NOTES.md E0.

## Focus (set by the user, 2026-10-05)

Work only on the two-layer network (the paper's architecture, N = 20,100).
No further one-layer runs unless the user asks.
