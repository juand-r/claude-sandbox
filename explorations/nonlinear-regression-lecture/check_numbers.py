"""Check the nonlinear regression deck: its tree, kNN and SVR code against scikit-learn, and the
numbers quoted on the slides and in the speaker notes.

Run (from this folder):
    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # once
    (cd tests && NODE_PATH=$(npm root -g) node export.js)                # writes tests/deck_outputs.json
    .venv/bin/python check_numbers.py

Every check raises AssertionError on failure; the script prints what it verified.
"""
import json
from pathlib import Path

import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).parent
OUT = json.loads((HERE / "tests" / "deck_outputs.json").read_text())
D = OUT["data"]
DOSE_X, DOSE_Y = np.array(D["DOSE"]["x"], float), np.array(D["DOSE"]["y"], float)
LIN_X, LIN_Y = np.array(D["LIN"]["x"], float), np.array(D["LIN"]["y"], float)
BMD_X, BMD_Y = np.array(D["BMD"]["x"], float), np.array(D["BMD"]["y"], float)
TWO_X, TWO_Y = np.array(D["TWO"]["X"], float), np.array(D["TWO"]["y"], float)
GX = np.array(OUT["gx"])

print("1. regression trees vs scikit-learn")
for t in OUT["trees"]:
    m = DecisionTreeRegressor(min_samples_split=t["minSplit"]).fit(DOSE_X[:, None], DOSE_Y)
    assert np.allclose(t["pred"], m.predict(GX[:, None]), atol=1e-9), t["minSplit"]
    assert len(t["leaves"]) == m.get_n_leaves(), (t["minSplit"], len(t["leaves"]), m.get_n_leaves())
print(f"   ok  predictions and leaf counts agree for min points to split = 2 … 19")
leaves = {t["minSplit"]: t["leaves"] for t in OUT["trees"]}
print("   leaves:", {k: len(v) for k, v in leaves.items()})

print("2. numbers on the tree slides")
L7 = leaves[7]
assert [(s["lo"], s["hi"]) for s in L7] == [(0, 14.5), (14.5, 23.5), (23.5, 29), (29, 40)], L7
vals = [s["value"] for s in L7]
assert np.allclose(vals, [25 / 6, 100, 221 / 4, 12 / 4]), vals
assert np.isclose(221 / 4, (66 + 60 + 50 + 45) / 4)
print(f"   ok  min split 7: thresholds 14.5, 23.5, 29; leaf values {[round(v, 2) for v in vals]}; "
      f"leaf sizes {[s['n'] for s in L7]}")
# order of the splits as the notes tell it: root 14.5, then 29 on the right, then 23.5
m7 = DecisionTreeRegressor(min_samples_split=7).fit(DOSE_X[:, None], DOSE_Y).tree_
assert m7.threshold[0] == 14.5 and m7.threshold[m7.children_right[0]] == 29.0
assert m7.threshold[m7.children_left[m7.children_right[0]]] == 23.5
print("   ok  split order: 14.5 (root), then 29, then 23.5; node sizes",
      [int(m7.n_node_samples[i]) for i in range(m7.node_count)])
sp = OUT["splits"]
own = []
for k in range(1, len(DOSE_X)):
    l, r = DOSE_Y[:k], DOSE_Y[k:]
    own.append(((DOSE_X[k - 1] + DOSE_X[k]) / 2, ((l - l.mean()) ** 2).sum() + ((r - r.mean()) ** 2).sum()))
assert np.allclose([(s["t"], s["sse"]) for s in sp], own)
first, best = sp[0], min(sp, key=lambda s: s["sse"])
assert first["t"] == 3 and first["mL"] == 0 and np.isclose(first["mR"], DOSE_Y[1:].mean())
assert best["t"] == 14.5
sse = np.array([s["sse"] for s in sp])
dips = [sp[i]["t"] for i in range(1, len(sp) - 1) if sse[i] < sse[i - 1] and sse[i] < sse[i + 1]]
assert len(dips) >= 2, dips
print(f"   ok  first threshold 3: means {first['mL']:.1f} / {first['mR']:.2f}, SSE {first['sse']:.0f}; "
      f"best 14.5: means {best['mL']:.2f} / {best['mR']:.2f}, SSE {best['sse']:.1f}; local minima at {dips}")
assert leaves[19] == [{"lo": 0, "hi": 40, "value": DOSE_Y.mean(), "n": 18}]
sse_tr = lambda t: ((DOSE_Y - np.array([next(s["value"] for s in leaves[t] if s["lo"] <= v < s["hi"]) for v in DOSE_X])) ** 2).sum()
assert sse_tr(2) < 1e-9
print(f"   ok  min split 2: training SSE 0 with {len(leaves[2])} leaves (runs of equal y share a leaf); "
      f"min split 7: SSE {sse_tr(7):.1f}; min split 19: one leaf, mean {DOSE_Y.mean():.2f}, SSE {sse_tr(19):.1f}")
ols = OUT["ols"]
b1, b0 = np.polyfit(DOSE_X, DOSE_Y, 1)
assert np.isclose(ols["b1"], b1) and np.isclose(ols["b0"], b0)
print(f"   ok  least-squares line: {b0:.2f} + {b1:.3f} x")

print("3. kNN regression vs scikit-learn")
G = np.array(OUT["knnGrid"])
for c in OUT["knn"]:
    k = c["k"]
    m = KNeighborsRegressor(n_neighbors=k, algorithm="brute").fit(BMD_X[:, None], BMD_Y)
    # compare only where the k-th and (k+1)-th nearest distances differ (no tie at the boundary)
    dist = np.abs(G[:, None] - BMD_X[None, :])
    ds = np.sort(dist, axis=1)
    ok = ds[:, k - 1] < ds[:, k] - 1e-9 if k < len(BMD_X) else np.ones(len(G), bool)
    assert np.allclose(np.array(c["pred"])[ok], m.predict(G[ok, None]), atol=1e-12), k
    print(f"   ok  k = {k:>2}: {ok.sum()} of {len(G)} grid ages agree (the rest have a tie for the k-th neighbour)")
k9 = next(c for c in OUT["knn"] if c["k"] == 9)
d40 = np.sort(np.abs(BMD_X - 40))
assert d40[8] < d40[9]
assert np.isclose(k9["at40"], KNeighborsRegressor(9).fit(BMD_X[:, None], BMD_Y).predict([[40]])[0])
print(f"   ok  prediction at age 40 with k = 9: {k9['at40']:.3f} (no tie: 9th distance {d40[8]}, 10th {d40[9]})")
for c in OUT["knn"]:
    print(f"       k = {c['k']:>2}: at 40 → {c['at40']:.3f}, training SSE {((BMD_Y - np.array(c['train'])) ** 2).sum():.3f}")
G2 = np.array(OUT["g2"])
for c in OUT["knn2"]:
    k = c["k"]
    dist = np.sqrt(((G2[:, None, :] - TWO_X[None, :, :]) ** 2).sum(-1))
    ds = np.sort(dist, axis=1)
    ok = ds[:, k - 1] < ds[:, k] - 1e-9
    m = KNeighborsRegressor(n_neighbors=k, algorithm="brute").fit(TWO_X, TWO_Y)
    assert np.allclose(np.array(c["pred"])[ok], m.predict(G2[ok]), atol=1e-12), k
    print(f"   ok  2D, k = {k}: {ok.sum()} of {len(G2)} grid points agree")

print("4. SVR vs scikit-learn")


def dual_objective(beta, X, y, eps, K):
    """½ cᵀKc + ε Σ(α + α*) − yᵀc with c = α − α*; the optimum value is unique."""
    n = len(y); a, s = beta[:n], beta[n:]
    c = a - s
    return 0.5 * c @ K @ c + eps * (a + s).sum() - y @ c


for c in OUT["svr"]:
    X, y = {"LIN": (LIN_X, LIN_Y), "DOSE": (DOSE_X, DOSE_Y)}[c["data"]]
    if c["kernel"] == "linear":
        m = SVR(kernel="linear", C=c["C"], epsilon=c["eps"], tol=1e-10).fit(X[:, None], y)
        K = np.outer(X, X)
    else:
        m = SVR(kernel="rbf", gamma=c["gamma"], C=c["C"], epsilon=c["eps"], tol=1e-10).fit(X[:, None], y)
        K = np.exp(-c["gamma"] * (X[:, None] - X[None, :]) ** 2)
    coef_sk = np.zeros(len(y)); coef_sk[m.support_] = m.dual_coef_[0]
    coef = np.array(c["coef"])
    # α and α* are never both positive at the optimum, so β = (max(c, 0), max(−c, 0))
    beta = lambda cf: np.r_[np.maximum(cf, 0), np.maximum(-cf, 0)]
    Dd, Ds = dual_objective(beta(coef), X, y, c["eps"], K), dual_objective(beta(coef_sk), X, y, c["eps"], K)
    assert abs(Dd - Ds) <= 1e-5 * max(1, abs(Ds)), (c["name"], Dd, Ds)
    pd, ps = np.array(c["pred"]), m.predict(np.array(c["grid"])[:, None])
    scale = max(1, np.abs(y).max())
    assert np.abs(pd - ps).max() <= 2e-3 * scale, (c["name"], np.abs(pd - ps).max())
    r = np.abs(y - m.predict(X[:, None]))
    EDGE = 1e-3   # as in the deck: within EDGE of the tube edge counts as on it
    out_sk, slack_sk = int((r > c["eps"] + EDGE).sum()), np.maximum(0, r - c["eps"]).sum()
    assert out_sk == c["out"] and abs(slack_sk - c["slack"]) < 1e-2 * max(1, slack_sk), (c["name"], out_sk, c["out"], slack_sk, c["slack"])
    extra = f"  w = {c['w'][0]:.3f} (sklearn {m.coef_[0][0]:.3f})" if c["w"] else ""
    print(f"   ok  {c['name']:<26} dual {Dd:11.4f}  outside {c['out']:>2}  slack {c['slack']:7.2f}  SSE {c['sse']:9.1f}{extra}")
print("all checks passed")
