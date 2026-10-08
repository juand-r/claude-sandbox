"""Check every number quoted on the neural-network slides and in their speaker notes against an
independent recomputation (this file does not import experiments.py).

    .venv/bin/python check_numbers.py

Fails loudly (AssertionError) on the first mismatch.
"""
import json
from pathlib import Path

import numpy as np

D = json.loads((Path(__file__).parent / "build" / "data.json").read_text())
sig = lambda z: 1 / (1 + np.exp(-z))


def close(a, b, tol, what):
    assert abs(a - b) <= tol, f"{what}: {a} vs {b}"
    print(f"ok  {what}: {a:.6g}")


# ---------------------------------------------------------------- class 1, softmax example
z = np.array([2.0, 1.0, -1.0])
p = np.exp(z) / np.exp(z).sum()
for k, v in enumerate([0.71, 0.26, 0.04]):
    close(round(p[k], 2), v, 1e-9, f"softmax z=(2,1,-1), p{k + 1} (2 d.p.)")
close(round(-np.log(p[0]), 2), 0.35, 1e-9, "loss if class 1, -log 0.71")
close(round(-np.log(p[2]), 1), 3.3, 1e-9, "loss if class 3")
close(round(np.exp(z).sum(), 2), 10.48, 1e-9, "sum of exponentials")
close(round(-np.log(0.01), 1), 4.6, 1e-9, "-log 0.01")

# ---------------------------------------------------------------- one-hot: softmax of (f, 0) is the sigmoid
for f in [-3.0, -0.4, 0.0, 1.7]:
    close(np.exp(f) / (np.exp(f) + 1), sig(f), 1e-12, f"softmax (f, 0) = sigma(f), f={f}")

# ---------------------------------------------------------------- the cartoon surface (same formula as code_1.js)
M1, S1, A1, M2, S2, A2, C = np.array([1.2, .9]), 1.2, 1.0, np.array([-1.4, -1.1]), .8, .65, .04


def cart(t):
    return 1.6 - A1 * np.exp(-((t - M1) ** 2).sum() / S1) - A2 * np.exp(-((t - M2) ** 2).sum() / S2) + C * (t ** 2).sum()


def cart_grad(t):
    e1, e2 = A1 * np.exp(-((t - M1) ** 2).sum() / S1), A2 * np.exp(-((t - M2) ** 2).sum() / S2)
    return e1 * 2 * (t - M1) / S1 + e2 * 2 * (t - M2) / S2 + 2 * C * t


def fd(fn, t, h=1e-6):
    return np.array([(fn(t + h * e) - fn(t - h * e)) / (2 * h) for e in np.eye(len(t))])


for t in [np.array([.3, -.7]), np.array([1.9, -1.7]), np.array([-2.6, .6])]:
    close(np.abs(cart_grad(t) - fd(cart, t)).max(), 0, 1e-7, f"cartoon gradient vs finite differences at {t}")


def descend(t, eta=.25, steps=120):
    for _ in range(steps):
        t = t - eta * cart_grad(t)
    return t


A, B = descend(np.array([1.9, -1.7])), descend(np.array([-2.6, .6]))
print("    start A ends at", A.round(3), "loss", round(cart(A), 3), "; start B ends at", B.round(3), "loss", round(cart(B), 3))
assert np.linalg.norm(A - M1) < .2 and np.linalg.norm(B - M2) < .2, "the two starts must end in different valleys"
assert cart(B) > cart(A), "B's valley must be the shallower one (a local minimum)"
close(np.abs(cart_grad(A)).max(), 0, 1e-4, "start A reached a stationary point in 120 steps")
close(np.abs(cart_grad(B)).max(), 0, 1e-4, "start B reached a stationary point in 120 steps")

# ---------------------------------------------------------------- gradient descent on logistic regression (hours, standardized)
HX = np.array([0.6, 1.4, 2.2, 3.0, 3.6, 4.3, 4.9, 5.6, 6.3, 7.4, 3.3, 4.6, 5.3, 6.0, 6.8, 7.1, 7.7, 8.4, 9.0, 9.6])
HY = np.r_[np.zeros(10), np.ones(10)]
XS = (HX - HX.mean()) / HX.std()
close(XS.mean(), 0, 1e-12, "standardized hours: mean"); close(XS.std(), 1, 1e-12, "standardized hours: SD")
lr_loss = lambda t: np.mean(np.logaddexp(0, t[0] * XS + t[1]) - HY * (t[0] * XS + t[1]))   # average log loss
lr_grad = lambda t: np.array([np.mean((sig(t[0] * XS + t[1]) - HY) * XS), np.mean(sig(t[0] * XS + t[1]) - HY)])
t = np.array(D["lr_std"]["opt"])
close(np.abs(lr_grad(t)).max(), 0, 1e-6, "lr_std optimum has zero gradient")
close(round(lr_loss(t), 3), 0.495, 1e-9, "minimum average loss 0.495")
assert D["lr_std"]["start"] == [-1.5, 2.0]
for name, eta, quote in [("small", .1, None), ("good", 1., None), ("large", 20., None)]:
    t, L = np.array([-1.5, 2.0]), [lr_loss(np.array([-1.5, 2.0]))]
    for _ in range(40):
        t = t - eta * lr_grad(t); L.append(lr_loss(t))
    R = D["lr_std"]["runs"][name]
    assert R["eta"] == eta and len(R["loss"]) == 41
    close(np.abs(np.array(R["loss"]) - L).max(), 0, 1e-4, f"GD eta={eta}: replayed losses match a fresh run")
close(round(D["lr_std"]["runs"]["small"]["loss"][40], 2), 0.78, 1e-9, "eta=0.1, loss after 40 steps")
close(round(D["lr_std"]["runs"]["good"]["loss"][10], 2), 0.52, 1e-9, "eta=1, loss at step 10")
close(round(D["lr_std"]["runs"]["large"]["loss"][40], 2), 0.69, 1e-9, "eta=20, loss after 40 steps")
P1 = np.array(D["lr_std"]["runs"]["large"]["path"][1]); opt = np.array(D["lr_std"]["opt"])
assert np.sign(P1[0] - opt[0]) != np.sign(-1.5 - opt[0]), "eta=20: the first step jumps past the minimum in w"
Lg = D["lr_std"]["runs"]["large"]["loss"]
assert max(Lg[5:]) > min(Lg[:6]) + .3, "eta=20: the loss later goes back up"
print("ok  eta=20: first step jumps past the minimum; later the loss climbs")

# ---------------------------------------------------------------- the perceptron rule is SGD on max(0, -y f)
rng = np.random.default_rng(0)
for _ in range(5):
    w, b, x, y = rng.normal(size=3), rng.normal(), rng.normal(size=3), rng.choice([-1, 1])
    if y * (w @ x + b) >= 0:
        continue   # a correct point: zero loss, zero gradient
    gw = fd(lambda v: max(0, -y * (v @ x + b)), w)
    close(np.abs(-gw - y * x).max(), 0, 1e-6, "perceptron step = minus the gradient of max(0, -y f)")

# ---------------------------------------------------------------- XOR data and logistic regression's best line
X, y = np.array(D["xor"]["X"]), np.array(D["xor"]["y"])
assert len(X) == 24 and (y > 0).sum() == 12
for cx, cy in [(2.5, 2.5), (7.5, 7.5), (2.5, 7.5), (7.5, 2.5)]:
    assert (np.abs(X - [cx, cy]).max(1) < 1.5).sum() == 6, "six points per corner"
print("ok  XOR: 24 points, 6 per corner")
U = (X - 5) / 2.5
lr = D["xor"]["lr"]
assert lr["w"] == [0.0, 0.0] and abs(lr["b"]) < 1e-9 and lr["acc"] == 0.5
# w = 0, b = 0 is optimal: the gradient of the average log loss vanishes there
Y01 = (y > 0).astype(float)
g = np.r_[((0.5 - Y01)[:, None] * U).mean(0), (0.5 - Y01).mean()]
close(np.abs(g).max(), 0, 1e-12, "XOR: logistic regression gradient at w = 0, b = 0")

# ---------------------------------------------------------------- XOR by hand
for a, b_, want in [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]:
    h1, h2 = sig(20 * a + 20 * b_ - 10), sig(20 * a + 20 * b_ - 30)
    pr = sig(20 * h1 - 20 * h2 - 10)
    assert round(pr) == want and abs(pr - want) < 1e-3, (a, b_, pr)
print("ok  XOR by hand: OR, AND, OR-and-not-AND")
close(round(sig(-10), 5), 0.00005, 1e-12, "sigma(-10)"); close(round(sig(10), 5), 0.99995, 1e-12, "sigma(10)")
close(2 * 3 + 3 + 3 * 2 + 2, 17, 0, "parameters of a 2-3-2 network")

# ---------------------------------------------------------------- the XOR training run (2-3-2 MLP)


def forward(P, U):
    W1, b1, W2, b2 = [np.array(p) for p in P]
    H = sig(U @ W1.T + b1); Z = H @ W2.T + b2
    E = np.exp(Z - Z.max(1, keepdims=True))
    return H, E / E.sum(1, keepdims=True)


Y = np.c_[y > 0, y < 0].astype(float)
loss = lambda P: -np.mean(np.log((forward(P, U)[1] * Y).sum(1)))
flat = lambda P: np.concatenate([np.ravel(p) for p in P])
shapes = [(3, 2), (3,), (2, 3), (2,)]


def unflat(v):
    out, i = [], 0
    for s in shapes:
        n = int(np.prod(s)); out.append(v[i:i + n].reshape(s)); i += n
    return out


def backprop(P):
    W1, b1, W2, b2 = [np.array(p) for p in P]
    H, Pr = forward(P, U)
    D2 = (Pr - Y) / len(U); D1 = (D2 @ W2) * H * (1 - H)
    return [D1.T @ U, D1.sum(0), D2.T @ H, D2.sum(0)]


R = D["xor"]["runs"]["ok"]
F = R["frames"]
P0 = F[0]["P"]
assert all(np.abs(np.ravel(p)).max() <= 1 for p in P0), "starting weights between -1 and 1"
gfd = fd(lambda v: loss(unflat(v)), flat(P0))
close(np.abs(flat(backprop(P0)) - gfd).max(), 0, 1e-8, "backprop gradient vs finite differences (XOR start)")
P, its = [np.array(p) for p in P0], {f["it"]: f for f in F}
for it in range(4001):
    if it in its:
        assert abs(loss(P) - its[it]["loss"]) < 2e-4, (it, loss(P), its[it]["loss"])
    P = [p - 2.0 * g for p, g in zip(P, backprop(P))]
print(f"ok  XOR run: {len(F)} replay frames match a fresh 4,000-step run with eta = 2")
fl = lambda it: its[it]["loss"]
close(round(fl(0), 2), 0.72, 1e-9, "XOR loss at the start")
close(round(fl(29), 2), 0.66, 1e-9, "XOR loss after about 30 steps (step 29)")
first_all = min(f["it"] for f in F if f["acc"] == 1.0)
assert first_all <= 60 and all(f["acc"] == 1.0 for f in F if f["it"] >= 60)
print(f"ok  XOR: all 24 points correct from frame step {first_all} on (quoted: by step 60)")
close(round(F[-1]["loss"], 4), 0.0006, 1e-9, "XOR final loss")
