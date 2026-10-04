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
