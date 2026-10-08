"""Precompute every training run shown in the two neural-network decks and write them to build/data.json.

    .venv/bin/python experiments.py

The decks replay these runs; nothing is trained in the browser (except gradient descent on the 2D
cartoon surface, which is not a model). check_numbers.py re-derives the quoted numbers from this file
and checks the gradients by finite differences.

Runs (all deterministic: fixed starts and fixed random seeds)
  HOURS      last lecture's hours-of-study data (20 students, pass = 1 / fail = 0).
  gd_lr      class 1: full-batch gradient descent on logistic regression with the feature standardized,
             from (w, b) = (-1.5, 2), for three learning rates.
  opt        class 2: plain GD, momentum and Adam on the unstandardized feature (an elongated bowl).
  sgd        class 2: batch, mini-batch (5) and stochastic (1) gradient descent, standardized feature.
  xor        class 1 and 2: a 2-3-2 MLP (sigmoid hidden units, softmax output) trained on the XOR data of
             the SVM deck by full-batch gradient descent, from two seeds: one converges, one stalls.
  xor_lr     class 1: logistic regression on XOR (the best single line).
  overfit    class 2: a 2-40-2 MLP trained with Adam on 30 noisy two-moons points; training and
             validation loss per epoch, weights at the early-stopping epoch and at the end.
"""
import json
from pathlib import Path

import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression

OUT = Path(__file__).parent / "build" / "data.json"
sig = lambda z: 1 / (1 + np.exp(-z))
r4 = lambda a: np.round(np.asarray(a, float), 5).tolist()

# ---------------------------------------------------------------- logistic regression on HOURS
HX = np.array([0.6, 1.4, 2.2, 3.0, 3.6, 4.3, 4.9, 5.6, 6.3, 7.4, 3.3, 4.6, 5.3, 6.0, 6.8, 7.1, 7.7, 8.4, 9.0, 9.6])
HY = np.r_[np.zeros(10), np.ones(10)]
MU, SD = HX.mean(), HX.std()
XS = (HX - MU) / SD


def lr_loss(t, x, y):
    z = t[0] * x + t[1]
    return float(np.mean(np.logaddexp(0, z) - y * z))


def lr_grad(t, x, y):
    p = sig(t[0] * x + t[1])
    return np.array([np.mean((p - y) * x), np.mean(p - y)])


def run(update, t0, steps):
    t, path = np.array(t0, float), [list(t0)]
    state = {}
    for k in range(1, steps + 1):
        t = update(t, k, state)
        path.append(t.tolist())
    return path


def gd(x, y, eta):
    return lambda t, k, s: t - eta * lr_grad(t, x, y)


def momentum(x, y, eta, beta):
    def u(t, k, s):
        s["v"] = beta * s.get("v", np.zeros(2)) + lr_grad(t, x, y)
        return t - eta * s["v"]
    return u


def adam(x, y, eta, b1=0.9, b2=0.999, eps=1e-8):
    def u(t, k, s):
        g = lr_grad(t, x, y)
        s["m"] = b1 * s.get("m", np.zeros(2)) + (1 - b1) * g
        s["s"] = b2 * s.get("s", np.zeros(2)) + (1 - b2) * g * g
        return t - eta * (s["m"] / (1 - b1 ** k)) / (np.sqrt(s["s"] / (1 - b2 ** k)) + eps)
    return u


def grid(fn, wr, br, n=60):
    ws, bs = np.linspace(*wr, n + 1), np.linspace(*br, n + 1)
    return {"w": r4(ws), "b": r4(bs), "L": [[round(fn(np.array([w, b])), 5) for b in bs] for w in ws]}


opt_std = LogisticRegression(C=np.inf, tol=1e-12, max_iter=10000).fit(XS[:, None], HY)
T_STD = [float(opt_std.coef_[0][0]), float(opt_std.intercept_[0])]
opt_raw = LogisticRegression(C=np.inf, tol=1e-12, max_iter=10000).fit(HX[:, None], HY)
T_RAW = [float(opt_raw.coef_[0][0]), float(opt_raw.intercept_[0])]

START_STD = [-1.5, 2.0]
GD_LR = {}
for name, eta in [("small", 0.1), ("good", 1.0), ("large", 20.0)]:
    p = run(gd(XS, HY, eta), START_STD, 40)
    GD_LR[name] = {"eta": eta, "path": r4(p), "loss": [round(lr_loss(np.array(q), XS, HY), 5) for q in p]}

START_RAW = [-0.3, 2.0]
OPT = {}
for name, upd in [("gd", gd(HX, HY, 0.2)), ("momentum", momentum(HX, HY, 0.05, 0.9)), ("adam", adam(HX, HY, 0.15))]:
    p = run(upd, START_RAW, 150)
    OPT[name] = {"path": r4(p), "loss": [round(lr_loss(np.array(q), HX, HY), 5) for q in p]}
OPT_PARAMS = {"gd": {"eta": 0.2}, "momentum": {"eta": 0.05, "beta": 0.9}, "adam": {"eta": 0.15, "beta1": 0.9, "beta2": 0.999}}

# batch / mini-batch / stochastic on the standardized feature: 6 epochs each, one fixed shuffle per epoch
rng = np.random.default_rng(7)
ORDERS = [rng.permutation(20).tolist() for _ in range(6)]
SGD = {}
for name, bs, eta in [("batch", 20, 1.0), ("mini", 5, 1.0), ("sgd", 1, 0.5)]:
    t, path = np.array(START_STD, float), [START_STD]
    for order in ORDERS:
        for i in range(0, 20, bs):
            idx = order[i:i + bs]
            t = t - eta * lr_grad(t, XS[idx], HY[idx])
            path.append(t.tolist())
    SGD[name] = {"batch_size": bs, "eta": eta, "path": r4(path), "updates_per_epoch": 20 // bs,
                 "loss": [round(lr_loss(np.array(q), XS, HY), 5) for q in path]}

# ---------------------------------------------------------------- MLP: sigmoid hidden layer, softmax output


def xor_data():
    OFF = [[0, 0], [.9, .5], [-.7, .8], [.4, -.9], [-.8, -.4], [1.1, -.2]]   # as in the SVM deck
    X, y = [], []
    for cx, cy, lab in [[2.5, 2.5, 1], [7.5, 7.5, 1], [2.5, 7.5, -1], [7.5, 2.5, -1]]:
        for dx, dy in OFF:
            X.append([cx + dx, cy + dy]); y.append(lab)
    return np.array(X), np.array(y)


def mlp_forward(P, U):
    W1, b1, W2, b2 = P
    H = sig(U @ W1.T + b1)
    Z = H @ W2.T + b2
    Z = Z - Z.max(1, keepdims=True)
    E = np.exp(Z)
    return H, E / E.sum(1, keepdims=True)


def mlp_loss(P, U, Y):
    return float(-np.mean(np.log((mlp_forward(P, U)[1] * Y).sum(1) + 1e-300)))


def mlp_grad(P, U, Y):
    """Backpropagation for mean cross-entropy: delta2 = p - y, delta1 = (delta2 W2) * h (1 - h)."""
    W1, b1, W2, b2 = P
    n = len(U)
    H, Pr = mlp_forward(P, U)
    D2 = (Pr - Y) / n
    D1 = (D2 @ W2) * H * (1 - H)
    return [D1.T @ U, D1.sum(0), D2.T @ H, D2.sum(0)]


def init(H, seed, n_in=2, n_out=2):
    r = np.random.default_rng(seed)
    return [r.uniform(-1, 1, (H, n_in)), r.uniform(-1, 1, H), r.uniform(-1, 1, (n_out, H)), r.uniform(-1, 1, n_out)]


def acc(P, U, Y):
    return float(np.mean(mlp_forward(P, U)[1].argmax(1) == Y.argmax(1)))


pack = lambda P: [r4(p) for p in P]

XX, XYl = xor_data()
XU = (XX - 5) / 2.5                                   # inputs scaled to about [-1, 1]
XY = np.c_[XYl > 0, XYl < 0].astype(float)            # output 1 = green (+1), output 2 = purple
XOR_FRAMES = sorted(set([0] + [int(round(v)) for v in np.geomspace(1, 4000, 70)]))
XOR = {}
for name, seed in [("ok", 1), ("stuck", 0)]:
    P, frames = init(3, seed), []
    for it in range(4001):
        if it in XOR_FRAMES:
            frames.append({"it": it, "P": pack(P), "loss": round(mlp_loss(P, XU, XY), 5), "acc": acc(P, XU, XY)})
        G = mlp_grad(P, XU, XY)
        P = [p - 2.0 * g for p, g in zip(P, G)]
    XOR[name] = {"seed": seed, "eta": 2.0, "hidden": 3, "frames": frames}

xor_lr = LogisticRegression(C=np.inf, tol=1e-12, max_iter=10000).fit(XU, XYl)
XOR_LR = {"w": r4(xor_lr.coef_[0]), "b": float(xor_lr.intercept_[0]), "acc": float(xor_lr.score(XU, XYl)),
          "p_range": r4([xor_lr.predict_proba(XU)[:, 1].min(), xor_lr.predict_proba(XU)[:, 1].max()])}

# overfitting: 30 training points, 400 validation points, Adam on the full batch (1 update = 1 epoch)
Xa, ya = make_moons(430, noise=0.35, random_state=0)
Xt, yt, Xv, yv = Xa[:30], ya[:30], Xa[30:], ya[30:]
Yt, Yv = np.eye(2)[yt], np.eye(2)[yv]
P = init(40, 0)
m = [np.zeros_like(p) for p in P]; s = [np.zeros_like(p) for p in P]
ETA_OF, B1, B2, EPOCHS = 0.02, 0.9, 0.999, 3000
tr, va, snaps = [], [], {}
for t in range(1, EPOCHS + 1):
    G = mlp_grad(P, Xt, Yt)
    m = [B1 * a + (1 - B1) * g for a, g in zip(m, G)]
    s = [B2 * a + (1 - B2) * g * g for a, g in zip(s, G)]
    P = [p - ETA_OF * (a / (1 - B1 ** t)) / (np.sqrt(c / (1 - B2 ** t)) + 1e-8) for p, a, c in zip(P, m, s)]
    tr.append(mlp_loss(P, Xt, Yt)); va.append(mlp_loss(P, Xv, Yv))
    snaps[t] = pack(P)
best = int(np.argmin(va)) + 1
OVERFIT = {"train_X": r4(Xt), "train_y": yt.tolist(), "val_X": r4(Xv[:120]), "val_y": yv[:120].tolist(),
           "hidden": 40, "eta": ETA_OF, "epochs": EPOCHS, "train_loss": r4(tr), "val_loss": r4(va),
           "best_epoch": best, "P_best": snaps[best], "P_end": snaps[EPOCHS],
           "acc": {"train_best": acc(snaps_to := [np.array(a) for a in snaps[best]], Xt, Yt),
                   "val_best": acc(snaps_to, Xv, Yv),
                   "train_end": acc([np.array(a) for a in snaps[EPOCHS]], Xt, Yt),
                   "val_end": acc([np.array(a) for a in snaps[EPOCHS]], Xv, Yv)}}

DATA = {
    "HOURS": {"x": HX.tolist(), "y": HY.tolist(), "mean": MU, "sd": SD},
    "lr_std": {"opt": T_STD, "start": START_STD, "runs": GD_LR,
               "grid": grid(lambda t: lr_loss(t, XS, HY), (-2.5, 8.5), (-5.0, 4.5))},
    "lr_raw": {"opt": T_RAW, "start": START_RAW, "runs": OPT, "params": OPT_PARAMS,
               "grid": grid(lambda t: lr_loss(t, HX, HY), (-0.6, 1.4), (-6.5, 3.0))},
    "sgd": {"start": START_STD, "orders": ORDERS, "runs": SGD,
            "grid": grid(lambda t: lr_loss(t, XS, HY), (-2.0, 2.5), (-1.5, 2.6))},
    "xor": {"X": XX.tolist(), "y": XYl.tolist(), "runs": XOR, "lr": XOR_LR},
    "overfit": OVERFIT,
}
OUT.write_text(json.dumps(DATA, separators=(",", ":")))
print("wrote", OUT, f"{OUT.stat().st_size / 1e6:.2f} MB")
print("std opt", np.round(T_STD, 4), "raw opt", np.round(T_RAW, 4))
for k, v in GD_LR.items(): print(f"  gd eta={v['eta']}: loss after 40 = {v['loss'][-1]:.4f}, max loss on path {max(v['loss']):.3f}")
for k, v in OPT.items(): print(f"  {k}: loss after 150 = {v['loss'][-1]:.4f}, end {np.round(v['path'][-1], 3)}")
for k, v in SGD.items(): print(f"  {k}: {len(v['path']) - 1} updates, final loss {v['loss'][-1]:.4f}")
for k, v in XOR.items(): print(f"  xor {k}: final loss {v['frames'][-1]['loss']}, acc {v['frames'][-1]['acc']}, {len(v['frames'])} frames")
print("  xor logistic:", XOR_LR)
print("  overfit: best epoch", best, "val", round(va[best - 1], 3), "end val", round(va[-1], 3), OVERFIT["acc"])
