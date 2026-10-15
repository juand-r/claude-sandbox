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
close(round(-np.log(p[1]), 2), 1.35, 1e-9, "loss if class 2 (cross-entropy figure)")
close(round(-np.log(p[2]), 2), 3.35, 1e-9, "loss if class 3")
close(round(np.exp(z).sum(), 2), 10.48, 1e-9, "sum of exponentials")
for q, v in [(0.99, 0.01), (0.5, 0.69), (0.01, 4.61)]:
    close(round(-np.log(q), 2), v, 1e-9, f"-log {q} (the -log p(true class) slide)")
close(round(np.log(2), 2), 0.69, 1e-9, "log loss at y f(x) = 0")
for yf in [-2.5, -0.3, 0.0, 1.2, 4.0]:
    close(-np.log(sig(yf)), np.log1p(np.exp(-yf)), 1e-12, f"-log sigma(yf) = log(1 + e^-yf), yf={yf}")

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

# ---------------------------------------------------------------- bonus: softmax and cross-entropy fit together
zz = np.array([2.0, 1.0, -1.0]); lse = np.log(np.exp(zz).sum()); pp = np.exp(zz) / np.exp(zz).sum()
for c in range(3):
    close(-np.log(pp[c]), -zz[c] + lse, 1e-12, f"-log p_c = -z_c + logsumexp, c={c + 1}")
assert zz.max() <= lse <= zz.max() + np.log(3); print(f"ok  max z <= logsumexp = {lse:.4f} <= max z + log 3")
close(round(-zz[2] + lse, 2), 3.35, 1e-9, "loss with true class 3"); close(zz.max() - zz[2], 3.0, 0, "true score 3 behind the top")
close(round(np.log(3), 2), 1.10, 1e-9, "log 3")
yy = np.array([1.0, 0, 0]); gce = pp - yy
for k in range(3):
    ek = np.zeros(3); ek[k] = 1e-6
    fdk = ((-np.log(np.exp(zz + ek)[0] / np.exp(zz + ek).sum())) - (-np.log(np.exp(zz - ek)[0] / np.exp(zz - ek).sum()))) / 2e-6
    close(fdk, gce[k], 1e-8, f"dL/dz_{k + 1} = p_k - y_k (finite differences)")
for k, v in enumerate([-0.29, 0.26, 0.04]):
    close(round(gce[k], 2), v, 1e-9, f"p - y, entry {k + 1} (2 d.p.)")
close(gce.sum(), 0.0, 1e-12, "p - y adds to 0")
for sf in [-2.0, 0.3, 3.0]:
    close(-sf + np.log(np.exp(sf) + 1), np.log1p(np.exp(-sf)), 1e-12, f"scores (f, 0), class 1: log(1 + e^-f), f={sf}")
    close(-0 + np.log(np.exp(sf) + 1), np.log1p(np.exp(sf)), 1e-12, f"scores (f, 0), class 2: log(1 + e^f), f={sf}")
z1 = 2.0; close(round(-z1 + np.log(np.exp(z1) + np.e + np.exp(-1)), 2), 0.35, 1e-9, "plotted point z1 = 2, z2 = 1, z3 = -1")

# ---------------------------------------------------------------- bonus: softmax vs argmax, losses compared
def softmax_b(zv, beta=1.0):
    ev = np.exp(beta * np.asarray(zv, float)); return ev / ev.sum()
for k, v in enumerate([0.50, 0.33, 0.17]):
    close(round(np.array([3, 2, 1])[k] / 6, 2), v, 1e-9, f"(3,2,1) divided by the sum, entry {k + 1}")
for k, v in enumerate([0.67, 0.24, 0.09]):
    close(round(softmax_b([3, 2, 1])[k], 2), v, 1e-9, f"softmax (3,2,1), entry {k + 1}")
assert list(np.array([2, 1, -1]) / 2) == [1, 0.5, -0.5]; print("ok  (2,1,-1) divided by the sum: (1, 0.5, -0.5)")
close(np.abs(softmax_b([2, 1, -1], 0) - 1 / 3).max(), 0, 1e-12, "beta = 0: 1/3 each")
close(round(softmax_b([2, 1, -1], 5)[0], 2), 0.99, 1e-9, "beta = 5: p1")
close(softmax_b([2, 1, -1], 200)[0], 1.0, 1e-12, "beta = 200: argmax")
close(np.abs(softmax_b([2, 1, -1], 1) - softmax_b([12, 11, 9], 1)).max(), 0, 1e-12, "softmax ignores a shift of all scores")
for zq in [-2.0, -0.5, 0.5, 2.0]:
    close(max(0, 1 - zq), max(0, -(zq - 1)), 0, f"hinge(z) = perceptron loss(z - 1), z={zq}")

# ---------------------------------------------------------------- activation functions slide
aa = np.linspace(-6, 6, 12001)
close(np.abs(np.tanh(aa) - (2 * sig(2 * aa) - 1)).max(), 0.0, 1e-12, "tanh(a) = 2 sigma(2a) - 1")
ds = sig(aa) * (1 - sig(aa))
close(ds.max(), 0.25, 1e-12, "sigmoid slope at most 1/4"); close(aa[ds.argmax()], 0.0, 1e-9, "  ... reached at a = 0")
close((np.tanh(1e-6) - np.tanh(-1e-6)) / 2e-6, 1.0, 1e-9, "tanh slope at 0")

# ---------------------------------------------------------------- XOR by hand
for a, b_, want in [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]:
    h1, h2 = sig(20 * a + 20 * b_ - 10), sig(20 * a + 20 * b_ - 30)
    pr = sig(20 * h1 - 20 * h2 - 10)
    assert round(pr) == want and abs(pr - want) < 1e-3, (a, b_, pr)
print("ok  XOR by hand: OR, AND, OR-and-not-AND")
close(round(sig(-10), 5), 0.00005, 1e-12, "sigma(-10)"); close(round(sig(10), 5), 0.99995, 1e-12, "sigma(10)")
close(2 * 3 + 3 + 3 * 2 + 2, 17, 0, "parameters of a 2-3-2 network")
close(2 * 3 + 3 + 3 * 3 + 3, 21, 0, "parameters of the 2-3-3 network on the forward-propagation slide")

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

# ---------------------------------------------------------------- the decks' own constants agree with the ones checked here
import re
CODE1 = (Path(__file__).parent / "build" / "code_1.js").read_text()
CODE2 = (Path(__file__).parent / "build" / "code_2.js").read_text()
assert "const A=[1.9,-1.7],B=[-2.6,.6];" in CODE1, "class 1 landscape starts changed: update the checks above"
assert "const SCHED={epochs:100,step:30,tdecay:20};" in CODE2, "schedule constants changed: update the notes"
m = re.search(r"const LOCAL=\{start:(\[[^\]]*\]),eta:([\d.]+),beta:([\d.]+),\s*restarts:(\[.*?\]\])\}", CODE2, re.S)
LOCAL = {"start": json.loads(m.group(1)), "eta": float(m.group(2)), "beta": float(m.group(3)),
         "restarts": json.loads(re.sub(r"(?<![\d])\.(\d)", r"0.\1", m.group(4)))}
print("    class 2 local-minima constants:", LOCAL)

# ================================================================ class 2
# ---------------------------------------------------------------- backprop formulas on a 2-2-1 sigmoid network and a 2-2-2 softmax network
rng = np.random.default_rng(3)
x, W, b, v, c = rng.normal(size=2), rng.normal(size=(2, 2)), rng.normal(size=2), rng.normal(size=2), rng.normal()
for yy in [0.0, 1.0]:
    def L221(th):
        W_, b_, v_, c_ = th[:4].reshape(2, 2), th[4:6], th[6:8], th[8]
        pp = sig(v_ @ sig(W_ @ x + b_) + c_)
        return -yy * np.log(pp) - (1 - yy) * np.log(1 - pp)
    h = sig(W @ x + b); pp = sig(v @ h + c)
    zfd = (lambda e: (-yy * np.log(sig(v @ h + c + e)) - (1 - yy) * np.log(1 - sig(v @ h + c + e))))
    close((zfd(1e-6) - zfd(-1e-6)) / 2e-6, pp - yy, 1e-8, f"dL/dz = p - y (y={yy:.0f})")
    th = np.r_[W.ravel(), b, v, c]; g = fd(L221, th)
    close(np.abs(g[6:8] - (pp - yy) * h).max(), 0, 1e-8, "dL/dv_j = (p - y) h_j")
    close(np.abs(g[:4] - ((pp - yy) * v * h * (1 - h))[:, None].dot(x[None, :]).ravel()).max(), 0, 1e-8,
          "dL/dw_ji = (p - y) v_j h_j (1 - h_j) x_i")
V, cc, yv = rng.normal(size=(2, 2)), rng.normal(size=2), np.array([0.0, 1.0])
def L222(th):
    W_, b_, V_, c_ = th[:4].reshape(2, 2), th[4:6], th[6:10].reshape(2, 2), th[10:12]
    zz = V_ @ sig(W_ @ x + b_) + c_; pr = np.exp(zz - zz.max()); pr /= pr.sum()
    return -np.log(pr @ yv)
h = sig(W @ x + b); zz = V @ h + cc; pr = np.exp(zz - zz.max()); pr /= pr.sum()
d2 = pr - yv; d1 = (V.T @ d2) * h * (1 - h)
g = fd(L222, np.r_[W.ravel(), b, V.ravel(), cc])
close(np.abs(g - np.r_[np.outer(d1, x).ravel(), d1, np.outer(d2, h).ravel(), d2]).max(), 0, 1e-8,
      "matrix form: delta2 = p - y, delta1 = (W2^T delta2) h (1 - h); grads delta2 h^T, delta1 x^T")

# ---------------------------------------------------------------- the raw-hours valley: plain GD, momentum, Adam
lossr = lambda t: np.mean(np.logaddexp(0, t[0] * HX + t[1]) - HY * (t[0] * HX + t[1]))
gradr = lambda t: np.array([np.mean((sig(t[0] * HX + t[1]) - HY) * HX), np.mean(sig(t[0] * HX + t[1]) - HY)])
R = D["lr_raw"]; to = np.array(R["opt"]); pr_ = sig(to[0] * HX + to[1]); wq = pr_ * (1 - pr_)
ev = np.linalg.eigvalsh(np.array([[np.mean(wq * HX * HX), np.mean(wq * HX)], [np.mean(wq * HX), np.mean(wq)]]))
close(np.abs(gradr(to)).max(), 0, 1e-6, "raw optimum has zero gradient")
close(round(lossr(to), 3), 0.495, 1e-9, "raw minimum is the same 0.495")
close(round(ev[1] / ev[0], -1), 350, 1e-9, "curvature ratio across / along the valley, about 350")
close(round(2 / ev[1], 2), 0.36, 1e-9, "plain GD stable near the minimum for eta < 2 / lambda_max")
assert R["start"] == [-0.3, 2.0]
t, vv, mm, ss = {k: np.array([-0.3, 2.0]) for k in "gma"}, np.zeros(2), np.zeros(2), np.zeros(2)
Lr = {k: [lossr(t[k])] for k in "gma"}
for k in range(1, 151):
    t["g"] = t["g"] - 0.2 * gradr(t["g"])
    vv = 0.9 * vv + gradr(t["m"]); t["m"] = t["m"] - 0.05 * vv
    gg = gradr(t["a"]); mm = 0.9 * mm + 0.1 * gg; ss = 0.999 * ss + 0.001 * gg * gg
    t["a"] = t["a"] - 0.15 * (mm / (1 - 0.9 ** k)) / (np.sqrt(ss / (1 - 0.999 ** k)) + 1e-8)
    for q in "gma": Lr[q].append(lossr(t[q]))
for q, name in [("g", "gd"), ("m", "momentum"), ("a", "adam")]:
    close(np.abs(np.array(R["runs"][name]["loss"]) - Lr[q]).max(), 0, 1e-4, f"{name}: replayed losses match a fresh run")
assert R["params"] == {"gd": {"eta": 0.2}, "momentum": {"eta": 0.05, "beta": 0.9}, "adam": {"eta": 0.15, "beta1": 0.9, "beta2": 0.999}}
close(round(Lr["g"][150], 3), 0.555, 1e-9, "plain GD loss after 150 steps")
close(round(Lr["m"][150], 3), 0.500, 1e-9, "momentum loss after 150 steps")
close(round(Lr["a"][150], 3), 0.495, 1e-9, "Adam loss after 150 steps")
close(round(Lr["a"][80], 3), 0.495, 1e-9, "Adam at the minimum (3 d.p.) by step 80")
assert round(Lr["a"][60], 3) > 0.495

# ---------------------------------------------------------------- local minima on the cartoon
def path(t, eta, beta=0.0, steps=120):
    t, v_ = np.array(t, float), np.zeros(2)
    for _ in range(steps):
        v_ = beta * v_ + cart_grad(t); t = t - eta * v_
    return t
end = path(LOCAL["start"], LOCAL["eta"])
assert np.linalg.norm(end - M2) < .2, "plain GD from the corner ends in the shallow valley"
endm = path(LOCAL["start"], LOCAL["eta"], LOCAL["beta"], 400)
assert np.linalg.norm(endm - M1) < .2, "momentum from the same corner ends in the deep valley"
print("ok  cartoon: plain GD from", LOCAL["start"], "-> shallow valley; momentum -> deep valley")
ends = [path(s, LOCAL["eta"]) for s in LOCAL["restarts"]]
assert len(ends) == 8 and LOCAL["restarts"][0] == LOCAL["start"]
best = min(ends, key=cart)
assert np.linalg.norm(best - M1) < .2, "the best of the restarts is in the deep valley"
print(f"ok  restarts: {sum(np.linalg.norm(e - M1) < .2 for e in ends)} of 8 reach the deep valley; the best does")
St = D["xor"]["runs"]["stuck"]["frames"][-1]
assert St["it"] == 4000 and abs(St["acc"] * 24 - 14) < 1e-9
close(round(St["loss"], 2), 0.35, 1e-9, "stalled XOR run: loss after 4,000 steps (14 of 24 right)")

# ---------------------------------------------------------------- batch / mini-batch / stochastic
S = D["sgd"]
assert S["start"] == [-1.5, 2.0] and len(S["orders"]) == 6
for name, bs, eta, quote in [("batch", 20, 1.0, 0.59), ("mini", 5, 1.0, 0.50), ("sgd", 1, 0.5, 0.50)]:
    t, n = np.array([-1.5, 2.0]), 0
    for order in S["orders"]:
        assert sorted(order) == list(range(20))
        for i in range(0, 20, bs):
            idx = order[i:i + bs]; p_ = sig(t[0] * XS[idx] + t[1])
            t = t - eta * np.array([np.mean((p_ - HY[idx]) * XS[idx]), np.mean(p_ - HY[idx])]); n += 1
    r = S["runs"][name]
    assert r["batch_size"] == bs and r["eta"] == eta and r["updates_per_epoch"] == 20 // bs and n == 6 * (20 // bs)
    close(np.abs(np.array(r["path"][-1]) - t).max(), 0, 1e-4, f"{name}: replayed path ends where a fresh run ends")
    close(round(lr_loss(t), 2), quote, 1e-9, f"{name}: loss after 6 epochs ({n} steps)")

# ---------------------------------------------------------------- early stopping (validation loss recomputed on 400 fresh points)
from sklearn.datasets import make_moons
O = D["overfit"]
Xa, ya = make_moons(430, noise=0.35, random_state=0)
assert np.allclose(np.array(O["train_X"]), Xa[:30], atol=1e-5) and O["train_y"] == ya[:30].tolist()
Xv, Yv = Xa[30:], np.eye(2)[ya[30:]]
assert len(Xv) == 400 and O["hidden"] == 40 and O["eta"] == 0.02 and O["epochs"] == 3000
def mlp_loss_acc(P, Xq, Yq):
    W1, b1, W2, b2 = [np.array(p) for p in P]
    Z = sig(Xq @ W1.T + b1) @ W2.T + b2; E = np.exp(Z - Z.max(1, keepdims=True)); Pq = E / E.sum(1, keepdims=True)
    return -np.mean(np.log((Pq * Yq).sum(1))), np.mean(Pq.argmax(1) == Yq.argmax(1))
best = O["best_epoch"]
assert best == 443 and int(np.argmin(O["val_loss"])) + 1 == best
lv, av = mlp_loss_acc(O["P_best"], Xv, Yv); lt, at = mlp_loss_acc(O["P_best"], Xa[:30], np.eye(2)[ya[:30]])
close(lv, O["val_loss"][best - 1], 1e-4, "validation loss at epoch 443, recomputed on the 400 points")
close(round(lv, 2), 0.33, 1e-9, "lowest validation loss"); close(round(100 * at), 80, 0, "training accuracy at epoch 443 (%)")
close(round(100 * av), 89, 0, "validation accuracy at epoch 443 (%)")
lv, av = mlp_loss_acc(O["P_end"], Xv, Yv); lt, at = mlp_loss_acc(O["P_end"], Xa[:30], np.eye(2)[ya[:30]])
close(round(lv, 2), 1.37, 1e-9, "validation loss at the end"); close(round(lt, 2), 0.05, 1e-9, "training loss at the end")
close(round(100 * at), 93, 0, "training accuracy at the end (%)"); close(round(100 * av), 77, 0, "validation accuracy at the end (%)")
# ---------------------------------------------------------------- patience (class 2, "When to stop")
assert "const PATIENCE=400;" in CODE2, "the figure's patience changed: update the notes"
def patience_stop(P, v=O["val_loss"]):
    best, be = float("inf"), 0
    for e, x in enumerate(v, 1):
        if x < best: best, be = x, e
        if e - be >= P: return e, be
    return None, be
assert patience_stop(400) == (843, 443), patience_stop(400)
assert patience_stop(300) == (325, 25), patience_stop(300)
vl = O["val_loss"]
close(round(vl[24], 2), 0.35, 1e-9, "validation loss dips at epoch 25")
close(round(vl[442], 2), 0.33, 1e-9, "validation loss at epoch 443")
assert min(e for e in range(26, len(vl) + 1) if vl[e - 1] < vl[24]) == 327
print("ok  patience 400: stops at 843 with epoch 443; patience 300: stops at 325 with epoch 25; first beaten at 327")
close(2 * 2 + 2 + 2 + 1, 9, 0, "weights and biases of the 2-2-1 network")
# ---------------------------------------------------------------- class 2: the chain rule slides
# y = (3x + 1)^2 at x = 1; y = u1 u2 with u1 = x^2, u2 = 3x at x = 2
close(fd(lambda t: (3 * t[0] + 1) ** 2, np.array([1.0]))[0], 2 * 4 * 3, 1e-6, "chain rule: d/dx (3x + 1)^2 at x = 1 is 24")
close(fd(lambda t: (t[0] ** 2) * (3 * t[0]), np.array([2.0]))[0], 6 * 4 + 4 * 3, 1e-6, "branching chain rule: d/dx x^2 * 3x at x = 2 is 36")
close(9 * 2 ** 2, 36, 0, "check on the slide: 9x^2 at x = 2")
# ---------------------------------------------------------------- class 2: "Derivatives we will use"
zg = np.linspace(-5, 5, 41)
sg = 1 / (1 + np.exp(-zg))
dsg = (1 / (1 + np.exp(-(zg + 1e-6))) - 1 / (1 + np.exp(-(zg - 1e-6)))) / 2e-6
close(np.abs(dsg - sg * (1 - sg)).max(), 0, 1e-8, "sigmoid derivative is sigma(1 - sigma)")
close(sg[20] * (1 - sg[20]), 0.25, 1e-12, "sigmoid derivative at z = 0 is 1/4 (notes)")
close((np.log(2 + 1e-6) - np.log(2 - 1e-6)) / 2e-6, 0.5, 1e-8, "d/dp log p = 1/p at p = 2")

# ---------------------------------------------------------------- class 2: the worked backpropagation example (2-2-1, sigmoid units)
# Weights as on the slides; every quoted value is the exact value rounded to 3 decimals, and a student
# who rounds each intermediate value to 3 decimals gets the same answers.
EX = dict(x=np.array([2.0, 1.0]), y=1.0, W=np.array([[-0.5, 1.0], [0.5, -1.0]]), b=np.array([1.0, -0.5]),
          v=np.array([2.0, 0.5]), c=-1.0)
def ex_loss(th, kind):
    W_, b_, v_, c_ = th[:4].reshape(2, 2), th[4:6], th[6:8], th[8]
    zz_ = v_ @ sig(W_ @ EX["x"] + b_) + c_
    if kind == "reg":                      # regression: linear output, target 2
        return 0.5 * (zz_ - 2.0) ** 2
    pp = sig(zz_)                          # a class: sigmoid output, label 1
    return 0.5 * (pp - EX["y"]) ** 2 if kind == "mse" else -np.log(pp)
th0 = np.r_[EX["W"].ravel(), EX["b"], EX["v"], EX["c"]]
a = EX["W"] @ EX["x"] + EX["b"]; h = sig(a); z = EX["v"] @ h + EX["c"]; pp = sig(z)
r3 = lambda t: round(float(t), 3)
want = {"a1": 1.0, "a2": -0.5, "h1": 0.731, "h2": 0.378, "z": 0.651, "p": 0.657, "L_mse": 0.059, "L_ce": 0.420,
        "dLdp": -0.343, "dpdz": 0.225, "dz_mse": -0.077, "h1(1-h1)": 0.197, "dLdp_ce": -1.522}
got = {"a1": a[0], "a2": a[1], "h1": h[0], "h2": h[1], "z": z, "p": pp, "L_mse": 0.5 * (pp - 1) ** 2, "L_ce": -np.log(pp),
       "dLdp": pp - 1, "dpdz": pp * (1 - pp), "dz_mse": (pp - 1) * pp * (1 - pp), "h1(1-h1)": h[0] * (1 - h[0]), "dLdp_ce": -1 / pp}
for k in want:
    close(r3(got[k]), want[k], 1e-12, f"example: {k}")
# the hand computation, three decimals at each step
H1, H2 = 0.731, 0.378
close(r3(2 * H1 + 0.5 * H2 - 1), 0.651, 1e-12, "example by hand: z = 2(0.731) + 0.5(0.378) - 1")
close(r3(sig(0.651)), 0.657, 1e-12, "example by hand: p = sigma(0.651)")
close(r3(0.5 * 0.343 ** 2), 0.059, 1e-12, "example by hand: L = (0.343)^2 / 2")
close(r3(0.657 * 0.343), 0.225, 1e-12, "example by hand: p(1 - p)")
close(r3(-0.343 * 0.225), -0.077, 1e-12, "example by hand: dL/dz (squared error)")
close(r3(-0.077 * 0.731), -0.056, 1e-12, "example by hand: dL/dv1 (squared error)")
close(r3(-0.343 * 0.225 * 0.731), -0.056, 1e-12, "example by hand: dL/dv1, three factors at once")
close(round(0.731 * 0.269, 4), 0.1966, 1e-12, "example by hand: h1(1 - h1), 4 decimals")
close(round(float(h[0] * (1 - h[0])), 4), 0.1966, 1e-12, "example: h1(1 - h1), 4 decimals")
close(r3(-0.077 * 2 * 0.1966 * 2), -0.061, 1e-12, "example by hand: dL/dw11 (squared error)")
close(r3(-1 / 0.657), -1.522, 1e-12, "example by hand: dL/dp (cross-entropy)")
close(r3(-np.log(0.657)), 0.420, 1e-12, "example by hand: L (cross-entropy)")
close(r3(-0.343 * 0.731), -0.251, 1e-12, "example by hand: dL/dv1 (cross-entropy)")
close(r3(-0.343 * 2 * 0.1966 * 2), -0.270, 1e-12, "example by hand: dL/dw11 (cross-entropy)")
# the same gradients from numerical derivatives of the whole network
gm, gc = fd(lambda t: ex_loss(t, "mse"), th0), fd(lambda t: ex_loss(t, "ce"), th0)
close(r3(gm[6]), -0.056, 1e-12, "example: dL/dv1 (squared error), numerically")
close(r3(gm[0]), -0.061, 1e-12, "example: dL/dw11 (squared error), numerically")
close(r3(gc[6]), -0.251, 1e-12, "example: dL/dv1 (cross-entropy), numerically")
close(r3(gc[0]), -0.270, 1e-12, "example: dL/dw11 (cross-entropy), numerically")
close(r3(fd(lambda e: 0.5 * (sig(e[0]) - 1) ** 2, np.array([z]))[0]), -0.077, 1e-12, "example: dL/dz (squared error), numerically")
# regression: same network, linear output, target 2 (the first version on the slides)
close(r3(z), 0.651, 1e-12, "regression: y_hat = z")
close(r3(0.5 * (z - 2) ** 2), 0.910, 1e-12, "regression: L"); close(r3(0.5 * (0.651 - 2) ** 2), 0.910, 1e-12, "regression by hand: L")
close(r3(z - 2), -1.349, 1e-12, "regression: dL/dy_hat = dL/dz")
close(r3(-1.349 * 0.731), -0.986, 1e-12, "regression by hand: dL/dv1")
close(r3(-1.349 * 2 * 0.1966 * 2), -1.061, 1e-12, "regression by hand: dL/dw11 (slope to 4 decimals)")
close(r3(-1.349 * 2 * 0.197 * 2), -1.063, 1e-12, "regression by hand with the slope at 3 decimals (quoted in the notes)")
gr = fd(lambda t: ex_loss(t, "reg"), th0)
close(r3(gr[6]), -0.986, 1e-12, "regression: dL/dv1, numerically")
close(r3(gr[0]), -1.061, 1e-12, "regression: dL/dw11, numerically")
close(r3(2 - 0.1 * -0.986), 2.099, 1e-12, "regression: new v1 (eta = 0.1)"); close(r3(2 - 0.1 * gr[6]), 2.099, 1e-12, "regression: new v1, exact")
close(r3(-0.5 - 0.1 * -1.061), -0.394, 1e-12, "regression: new w11 (eta = 0.1)"); close(r3(-0.5 - 0.1 * gr[0]), -0.394, 1e-12, "regression: new w11, exact")
print(f"    regression: loss {ex_loss(th0, 'reg'):.4f} -> {ex_loss(th0 - 0.1 * gr, 'reg'):.4f} after one step (eta = 0.1) on all nine weights")
assert r3(ex_loss(th0 - 0.1 * gr, "reg")) == 0.489, ex_loss(th0 - 0.1 * gr, "reg")
# one step on all nine weights lowers the loss (quoted in the notes)
for kind, g in [("mse", gm), ("ce", gc)]:
    print(f"    example, {kind}: loss {ex_loss(th0, kind):.4f} -> {ex_loss(th0 - g, kind):.4f} after one step on all nine weights")
    assert ex_loss(th0 - g, kind) < ex_loss(th0, kind)
# the same example with two outputs (softmax, cross-entropy); output 1 keeps v11 = 2, v12 = 0.5, c1 = -1
V2, c2v, y2 = np.array([[2.0, 0.5], [1.0, 0.5]]), np.array([-1.0, -1.0]), np.array([1.0, 0.0])
def ex2_loss(th):
    W_, b_, V_, c_ = th[:4].reshape(2, 2), th[4:6], th[6:10].reshape(2, 2), th[10:12]
    zz = V_ @ sig(W_ @ EX["x"] + b_) + c_; pr = np.exp(zz - zz.max()); pr /= pr.sum()
    return -np.log(pr @ y2)
zz = V2 @ h + c2v; pr = np.exp(zz) / np.exp(zz).sum()
for k, w in [("z1", (zz[0], 0.651)), ("z2", (zz[1], -0.080)), ("e^z1", (np.exp(zz[0]), 1.917)), ("e^z2", (np.exp(zz[1]), 0.923)),
             ("p1", (pr[0], 0.675)), ("p2", (pr[1], 0.325)), ("L", (-np.log(pr[0]), 0.393))]:
    close(r3(w[0]), w[1], 1e-12, f"two outputs: {k}")
close(r3(1 * 0.731 + 0.5 * 0.378 - 1), -0.080, 1e-12, "two outputs by hand: z2")
close(r3(1.917 / (1.917 + 0.923)), 0.675, 1e-12, "two outputs by hand: p1 from the rounded exponentials")
close(r3(-np.log(0.675)), 0.393, 1e-12, "two outputs by hand: L")
close(r3(-0.325 * 2 * 0.1966 * 2), -0.256, 1e-12, "two outputs by hand: path through z1")
close(r3(0.325 * 1 * 0.1966 * 2), 0.128, 1e-12, "two outputs by hand: path through z2")
close(r3((-0.325 * 2 + 0.325 * 1) * 0.1966), -0.064, 1e-12, "two outputs by hand: dL/da1 (recipe notes)")
close(r3((pr[0] - 1) * 2 * h[0] * (1 - h[0]) * 2), -0.256, 1e-12, "two outputs: path through z1, exact")
close(r3(pr[1] * 1 * h[0] * (1 - h[0]) * 2), 0.128, 1e-12, "two outputs: path through z2, exact")
g2 = fd(ex2_loss, np.r_[EX["W"].ravel(), EX["b"], V2.ravel(), c2v])
close(r3(g2[0]), -0.128, 1e-12, "two outputs: dL/dw11, numerically")
close(r3(-0.256 + 0.128), -0.128, 1e-12, "two outputs: sum of the two rounded paths")
# squared error's extra factor p(1 - p): a confident wrong answer (p = 0.01, y = 1) gets a tiny gradient
close(r3((0.01 - 1) * 0.01 * 0.99), -0.010, 1e-12, "squared error at p = 0.01, y = 1: dL/dz")

# ---------------------------------------------------------------- class 2: the live network on the recap slide (biases 0)
assert "const START={W1:[[1.2,-.8],[-.6,1.5],[.9,.4]],W2:[[1.6,-1.1,.7],[-.9,1.3,-.5]],x:[1,.5]};" in CODE2, \
    "recap widget start values changed: update these checks and tests/recap2.js"
def recap_p(W1, W2, x):
    a = 1 / (1 + np.exp(-np.array(W1) @ np.array(x)))
    z = np.array(W2) @ a
    e = np.exp(z - z.max())
    return e / e.sum()
RW1, RW2 = [[1.2, -.8], [-.6, 1.5], [.9, .4]], [[1.6, -1.1, .7], [-.9, 1.3, -.5]]
close(round(recap_p(RW1, RW2, [1, .5])[0], 2), 0.79, 1e-12, "recap widget: p1 at the start")
RW1[0][0] = 3
close(round(recap_p(RW1, RW2, [1, .5])[0], 2), 0.87, 1e-12, "recap widget: p1 with w(x1->a1) = 3")
close(round(recap_p(RW1, RW2, [1, -.5])[0], 2), 0.94, 1e-12, "recap widget: p1 with w(x1->a1) = 3, x2 = -0.5")
close(round(recap_p(RW1, RW2, [1, 1])[0], 2), 0.82, 1e-12, "recap widget: p1 with w(x1->a1) = 3, x2 = 1")

print("all checks passed")
