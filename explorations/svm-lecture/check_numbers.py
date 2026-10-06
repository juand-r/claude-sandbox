"""Check the SVM deck: its solver against scikit-learn, and every number quoted on the slides.

Run (from this folder):
    .venv/bin/python -m pip install -r requirements.txt     # once
    (cd tests && NODE_PATH=$(npm root -g) node export.js)   # writes tests/solver_outputs.json
    .venv/bin/python check_numbers.py

Every check raises AssertionError on failure; the script prints what it verified.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from sklearn.svm import SVC

HERE = Path(__file__).parent
OUT = json.loads((HERE / "tests" / "solver_outputs.json").read_text())
DATA = {k: (np.array(v["X"], float), np.array(v["y"], float)) for k, v in OUT["data"].items()}
lift = lambda X: np.c_[X, (X[:, 0] - 5) ** 2 + (X[:, 1] - 5) ** 2]
DATA["RINGS_LIFTED"] = (lift(DATA["RINGS"][0]), DATA["RINGS"][1])


def sk_model(case):
    X, y = DATA[case["data"]]
    if case["kernel"] == "linear":
        return SVC(kernel="linear", C=case["C"], tol=1e-10).fit(X, y)
    return SVC(kernel="rbf", gamma=case["gamma"], C=case["C"], tol=1e-10).fit(X, y)


def separable(X, y):
    """Is there (w, b) with y_i (w.x_i + b) >= 1 for all i?  (a linear feasibility problem)"""
    A = -y[:, None] * np.c_[X, np.ones(len(X))]
    r = linprog(np.zeros(X.shape[1] + 1), A_ub=A, b_ub=-np.ones(len(X)), bounds=[(None, None)] * (X.shape[1] + 1))
    return r.status == 0


def gram(case, X):
    if case["kernel"] == "linear":
        return X @ X.T
    d2 = ((X[:, None, :] - X[None, :, :]) ** 2).sum(-1)
    return np.exp(-case["gamma"] * d2)


def dual_objective(alpha, y, K):
    """sum(alpha) - 1/2 alpha^T Q alpha with Q_ij = y_i y_j K_ij; its optimum is unique."""
    v = alpha * y
    return alpha.sum() - 0.5 * v @ K @ v


def primal_objective(w, b, X, y, C):
    return 0.5 * w @ w + C * np.maximum(0, 1 - y * (X @ w + b)).sum()


print("1. deck solver vs scikit-learn")
for c in OUT["cases"]:
    m = sk_model(c)
    X, y = DATA[c["data"]]
    K = gram(c, X)
    a_deck = np.array(c["alpha"])
    a_sk = np.zeros(len(X)); a_sk[m.support_] = np.abs(m.dual_coef_[0])
    D_deck, D_sk = dual_objective(a_deck, y, K), dual_objective(a_sk, y, K)
    assert abs(D_deck - D_sk) <= 1e-5 * max(1, abs(D_sk)), (c["name"], D_deck, D_sk)
    notes = []
    if c["kernel"] == "linear":
        w_sk, b_sk = m.coef_[0], m.intercept_[0]
        assert np.allclose(c["w"], w_sk, atol=2e-3), (c["name"], c["w"], w_sk)   # w is always unique
        if abs(c["b"] - b_sk) > 5e-3:
            # b is not unique in degenerate problems; then both values give the same primal objective
            P1, P2 = primal_objective(np.array(c["w"]), c["b"], X, y, c["C"]), primal_objective(np.array(c["w"]), b_sk, X, y, c["C"])
            assert abs(P1 - P2) <= 1e-5 * max(1, P1), (c["name"], c["b"], b_sk, P1, P2)
            notes.append(f"b not unique: deck {c['b']:.3f}, sklearn {b_sk:.3f}, same objective")
    else:
        d = np.abs(np.array(c["fgrid"]) - m.decision_function(np.array(c["grid"], float))).max()
        assert d < 5e-3, (c["name"], d)
    if set(c["sv"]) != set(m.support_.tolist()):
        # alpha need not be unique when extra points lie exactly on the margin; every support
        # vector either solver chose must then have y f(x) <= 1
        yf = y * m.decision_function(X)
        on_or_inside = set(np.where(yf <= 1 + 1e-3)[0].tolist())
        assert set(c["sv"]) <= on_or_inside and set(m.support_.tolist()) <= on_or_inside, (c["name"], c["sv"], m.support_)
        notes.append(f"support sets differ ({len(c['sv'])} vs {len(m.support_)}), all on or inside the margin")
    print(f"   ok  {c['name']:<20} dual objective {D_deck:9.4f}  support vectors {len(c['sv']):>2}" + ("  [" + "; ".join(notes) + "]" if notes else ""))

print("2. numbers on the slides")
case = lambda name: next(c for c in OUT["cases"] if c["name"] == name)
hard = case("SEP hard")
assert np.allclose(hard["w"], [0.5, 0.5], atol=1e-4) and abs(hard["b"] + 5) < 1e-3
a = {i: hard["alpha"][i] for i in hard["sv"]}
X, y = DATA["SEP"]
want = {(5.5, 6.5): 1 / 12, (7, 5): 1 / 6, (4.5, 3.5): 1 / 4}
for i, v in a.items():
    assert abs(v - want[tuple(X[i])]) < 1e-4, (X[i], v)
print("   ok  hard margin: w = (0.5, 0.5), b = -5, alpha = 1/12, 1/6, 1/4, width 2/||w|| =", round(2 / math.hypot(.5, .5), 2))

for C, width, nsv in [(0.01, 7.94, 14), (1, 3.18, 6), (100, 2.73, 5)]:
    c = case(f"SOFT C={C}")
    w = np.array(c["w"])
    assert abs(2 / np.linalg.norm(w) - width) < 0.01 and len(c["sv"]) == nsv, (C, 2 / np.linalg.norm(w), len(c["sv"]))
Xs, ys = DATA["SOFT"]
c1 = case("SOFT C=1")
yf = ys * (Xs @ np.array(c1["w"]) + c1["b"])
assert (yf < 0).sum() == 2, (yf < 0).sum()
print("   ok  soft margin: widths 7.94 / 3.18 / 2.73 and 14 / 6 / 5 support vectors at C = 0.01 / 1 / 100; 2 mistakes at C = 1")

assert separable(*DATA["SEP"]) and not separable(*DATA["SOFT"])
assert not separable(*DATA["RINGS"]) and separable(*DATA["RINGS_LIFTED"])
assert not separable(*DATA["XOR"])
print("   ok  separable: SEP yes, SOFT no, RINGS no, RINGS lifted to 3D yes, XOR no")

# slide 2: lines A, B, C separate the data and have narrower streets than the SVM
for k, deg, frac in [("A", 15, .5), ("B", 72, .5), ("C", 45, .82)]:
    u = np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])
    pr = X @ u
    lo, hi = pr[y < 0].max(), pr[y > 0].min()
    assert lo < hi, k
    cc = lo + frac * (hi - lo)
    width = 2 * (y * (pr - cc)).min()
    assert 0 < width < 2 / math.hypot(.5, .5) - 0.1, (k, width)
    print(f"   ok  line {k} separates, street width {width:.2f} < 2.83")

# slide 13: exercise
w, b = np.array([3., 4.]), -10.
P = {"A": ((3, 1), 1), "B": ((1, 1), -1), "C": ((2.4, .8), 1), "D": ((2, 1), -1), "E": ((3, .6), -1)}
f = {k: w @ np.array(p) + b for k, (p, _) in P.items()}
xi = {k: max(0., 1 - lab * f[k]) for k, (_, lab) in P.items()}
assert np.allclose([f[k] for k in "ABCDE"], [3, -3, .4, 0, 1.4]) and np.allclose([xi[k] for k in "ABCDE"], [0, 0, .6, 1, 2.4])
assert abs(2 / np.linalg.norm(w) - .4) < 1e-12
print("   ok  exercise: f = 3, -3, 0.4, 0, 1.4; xi = 0, 0, 0.6, 1, 2.4; width 0.4")

# slide 4: distance example (w = (0.3, 0.4), b = -3.5, x = (8, 7))
assert abs(math.hypot(.3, .4) - .5) < 1e-12 and abs((.3 * 8 + .4 * 7 - 3.5) / .5 - 3.4) < 1e-12
print("   ok  distance slide: ||w|| = 0.5, f(8, 7) = 1.7, d = |f|/||w|| = 3.4")
print("all checks passed")
