"""Check the logistic regression deck: its fits against scikit-learn, and the numbers on the slides and in the notes.

Run (from this folder):
    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # once
    (cd tests && NODE_PATH=$(npm root -g) node export.js)                # writes tests/deck_outputs.json
    .venv/bin/python check_numbers.py

Every check raises AssertionError on failure; the script prints what it verified.
"""
import json
import math
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

OUT = json.loads((Path(__file__).parent / "tests" / "deck_outputs.json").read_text())
hx, hy = np.array(OUT["HOURS"]["x"], float)[:, None], np.array(OUT["HOURS"]["y"])
SX, SY = np.array(OUT["SOFT"]["X"], float), np.array(OUT["SOFT"]["y"])

print("1. fits vs scikit-learn")
m = LogisticRegression(C=np.inf, tol=1e-12, max_iter=10000).fit(hx, hy)          # no ½‖w‖² term
d = OUT["hours"]
assert np.allclose(d["w"], m.coef_[0], atol=1e-6) and abs(d["b"] - m.intercept_[0]) < 1e-6, (d, m.coef_, m.intercept_)
print(f"   ok  hours, unpenalized: w = {d['w'][0]:.4f}, b = {d['b']:.4f}")
m = LogisticRegression(C=1, tol=1e-12, max_iter=10000).fit(SX, SY)               # ½‖w‖² + C Σ log loss, b not penalized
d = OUT["softLR"]
assert np.allclose(d["w"], m.coef_[0], atol=1e-6) and abs(d["b"] - m.intercept_[0]) < 1e-6, (d, m.coef_, m.intercept_)
print(f"   ok  SOFT, logistic regression C = 1: w = ({d['w'][0]:.4f}, {d['w'][1]:.4f}), b = {d['b']:.4f}")
s = SVC(kernel="linear", C=1, tol=1e-10).fit(SX, SY)
d = OUT["softSVM"]
assert np.allclose(d["w"], s.coef_[0], atol=2e-3) and abs(d["b"] - s.intercept_[0]) < 5e-3, (d, s.coef_, s.intercept_)
print(f"   ok  SOFT, linear SVM C = 1: w = ({d['w'][0]:.4f}, {d['w'][1]:.4f}), b = {d['b']:.4f}")
# the two lines really differ (slide 6)
a1 = math.degrees(math.atan2(OUT["softLR"]["w"][1], OUT["softLR"]["w"][0]))
a2 = math.degrees(math.atan2(d["w"][1], d["w"][0]))
assert abs(a1 - a2) > 5, (a1, a2)
print(f"   ok  the normals differ by {abs(a1 - a2):.1f} degrees")

print("2. numbers on the slides and in the notes")
neg, pos = hx[hy < 0, 0], hx[hy > 0, 0]
assert len(neg) == len(pos) == 10 and pos.min() == 3.3 and neg.max() == 7.4
w, b = OUT["hours"]["w"][0], OUT["hours"]["b"]
assert abs(-b / w - 5.4) < 0.05
print(f"   ok  hours: classes overlap from {pos.min()} to {neg.max()}; p = 0.5 at {-b / w:.2f} h")
p = 1 / (1 + np.exp(-(w * hx[:, 0] + b)))
for r in OUT["thr"]:
    tp, fp = int(((p > r["t"]) & (hy > 0)).sum()), int(((p > r["t"]) & (hy < 0)).sum())
    assert (tp, fp) == (r["tp"], r["fp"]), r
    assert abs(1 / (1 + math.exp(-(w * r["xs"] + b))) - r["t"]) < 1e-9
print("   ok  thresholds:", ", ".join(f"t = {r['t']:.2f} → x = {r['xs']:.1f} h, TPR {r['tp']}/10, FPR {r['fp']}/10" for r in OUT["thr"]))
sig = lambda z: 1 / (1 + math.exp(-z))
assert f"{sig(2):.2f}" == "0.88" and f"{sig(-2):.2f}" == "0.12" and sig(0) == 0.5
for z in [-3, -1, 0, 0.5, 2]:
    assert abs(math.log(1 + math.exp(-z)) + math.log(sig(z))) < 1e-12   # log loss = −log σ(y f)
assert abs(-math.log(0.01) - 4.6) < 0.01
print("   ok  σ(−2), σ(0), σ(2) = 0.12, 0.50, 0.88; log(1 + e^−z) = −log σ(z); −log 0.01 = 4.61")
for f in [-3.0, -0.4, 0.0, 1.7, 5.0]:   # slide 7, step by step
    assert abs((1 - sig(f)) - math.exp(-f) / (1 + math.exp(-f))) < 1e-12 and abs(math.exp(-f) / (1 + math.exp(-f)) - 1 / (math.exp(f) + 1)) < 1e-12
    assert abs(1 / (math.exp(f) + 1) - sig(-f)) < 1e-12
for p in [0.01, 0.2, 0.5, 0.9]:
    z = math.log(p / (1 - p))
    assert abs(sig(z) - p) < 1e-12 and abs(math.exp(-z) - (1 - p) / p) < 1e-12
assert abs(math.exp(1) - 2.7) < 0.02
print("   ok  1 − σ(f) = e^−f/(1 + e^−f) = 1/(e^f + 1) = σ(−f); σ(log(p/(1 − p))) = p; e ≈ 2.7")
# far on the wrong side both losses have slope −1
z = -30.0
assert abs((math.log(1 + math.exp(-z)) - math.log(1 + math.exp(-(z - 1)))) - (-1)) < 1e-6
print("   ok  log loss grows linearly (slope −1) far on the wrong side, like the hinge")
print("all checks passed")
