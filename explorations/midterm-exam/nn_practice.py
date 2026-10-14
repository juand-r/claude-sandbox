"""Numbers for practice question 4 (neural networks), computed from the weights.

Usage: .venv/bin/python nn_practice.py
Weights are written W[l][j][i]: layer l, from node i of the previous layer to node j (as in lecture,
w_ji connects input i to unit j). The bias of unit j is b[l][j]. Values given to students are rounded
to 2 decimals, and the backprop solution uses those rounded values, as a student would.
"""
import numpy as np

sig = lambda z: 1 / (1 + np.exp(-z))
r2 = lambda v: np.round(v, 2)

# ---------------------------------------------------------------- 4.1 forward propagation, sign units
W1 = np.array([[0.5, -0.3], [-0.4, 0.6]]); b1 = np.array([0.2, -0.5])
W2 = np.array([[0.7, 0.4], [-0.6, 0.3]]); b2 = np.array([0.2, 0.1])
x = np.array([6, 4])
zB = W1 @ x + b1; B = np.sign(zB); zC = W2 @ B + b2; C = np.sign(zC)
print("4.1  zB =", zB, " B =", B, " zC =", zC, " C =", C)
assert np.all(np.abs(np.r_[zB, zC]) >= 0.3), "no pre-activation near 0 (sign(0) is ambiguous)"
assert C[0] != C[1], "exactly one output is +1"

# ---------------------------------------------------------------- 4.2 backpropagation, sigmoid -> ReLU -> linear
A = np.array([2.0, 1.0]); Y = 4.0; eta = 1.0
V1 = np.array([[0.5, -1.0], [1.0, 0.5], [-0.5, 1.5]]); c1 = np.array([0.5, -1.0, 0.0])      # A -> B (sigmoid)
V2 = np.array([[-1.0, 0.5, -1.0], [2.0, 1.0, -0.5], [0.5, 1.5, 1.0]]); c2 = np.array([0.5, -0.5, -1.0])  # B -> C (ReLU)
V3 = np.array([[1.5, -0.4, 2.0]]); c3 = np.array([0.5])                                   # C -> D (linear)
zB = V1 @ A + c1; Bv = r2(sig(zB))
zC = V2 @ Bv + c2; Cv = r2(np.maximum(zC, 0))
D = r2(V3 @ Cv + c3)[0]
print("4.2  zB =", r2(zB), " B =", Bv, " zC =", r2(zC), " C =", Cv, " D =", D, " Y =", Y)
assert (zC <= 0).sum() == 1, "exactly one ReLU unit is off"
assert np.all(np.abs(zC) > 0.1)
# gradient of E = 1/2 (D - Y)^2 with respect to W1_21 (from A1 to B2)
dD = D - Y
dC = dD * V3[0] * (zC > 0)                 # through the ReLU: slope 1 if on, 0 if off
dB2 = (dC * V2[:, 1]).sum()                # B2 feeds every C unit
dz_B2 = dB2 * Bv[1] * (1 - Bv[1])          # sigmoid slope
grad = dz_B2 * A[0]
print(f"     dE/dD = {dD:.4f}; dE/dC = {dC}; dE/dB2 = {dB2:.4f}; dE/dz_B2 = {dz_B2:.4f}; dE/dW1_21 = {grad:.4f}")
print(f"     W1_21: {V1[1,0]} -> {V1[1,0] - eta * grad:.4f}  (eta = {eta})")
# the unrounded D must not sit on a rounding boundary
assert abs((V3 @ Cv + c3)[0] - D) < 1e-9, "D is exact at 2 decimals"
