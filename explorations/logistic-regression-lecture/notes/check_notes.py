"""Compute every number quoted in logistic_regression_notes.tex, so none is typed in by hand.

    python3 notes/check_notes.py        (from the lecture folder; standard library only)

The hours-of-study fit is read from tests/deck_outputs.json, which tests/export.js writes from the
deck's own fitting code (and check_numbers.py compares with scikit-learn).
"""
import json
import math
from pathlib import Path

here = Path(__file__).parent
sig = lambda z: 1 / (1 + math.exp(-z))
hinge = lambda m: max(0.0, 1 - m)
logloss = lambda m: math.log(1 + math.exp(-m))

# ---- the five-point example used for all three losses
EX = [(+1, 2.0), (+1, -0.5), (-1, -1.5), (-1, 0.8), (+1, 0.3)]
print('five-point example: i, y, f, m = y f, 0-1, hinge, p(true) = sigma(m), log loss')
tot = [0, 0.0, 0.0]
for i, (y, f) in enumerate(EX, 1):
    m = y * f
    z1, h, l = int(m <= 0), hinge(m), logloss(m)
    assert abs(l + math.log(sig(m))) < 1e-12          # log loss = -log p(true class)
    tot[0] += z1; tot[1] += h; tot[2] += l
    print(f'  {i}  {y:+d}  {f:+.1f}  {m:+.1f}  {z1}  {h:.1f}  {sig(m):.3f}  {l:.3f}')
print(f'  totals: 0-1 = {tot[0]}, hinge = {tot[1]:.1f}, log loss = {tot[2]:.3f}')

# ---- curves at a few margins
print('m, 0-1, hinge, log loss:', [(m, int(m <= 0), hinge(m), round(logloss(m), 3)) for m in [-2, -1, 0, 0.5, 1, 2, 4]])
print('log loss far on the wrong side vs -m:', [(m, round(logloss(m), 4)) for m in [-5, -10]])
print('sigmoid at -2, 0, 2:', [round(sig(z), 2) for z in [-2, 0, 2]])
print('-log p for p = 0.99, 0.9, 0.5, 0.1, 0.01:', [round(-math.log(p), 2) for p in [0.99, 0.9, 0.5, 0.1, 0.01]])
for z in [-1.3, 0.4, 2.0]:
    assert abs(1 - sig(z) - sig(-z)) < 1e-12 and abs(math.log(sig(z) / (1 - sig(z))) - z) < 1e-12
print('odds: p = 0.8 ->', round(0.8 / 0.2, 2), '; score 1 -> odds e =', round(math.e, 2), ', p =', round(sig(1), 3))

# ---- hours of study
D = json.loads((here / '../tests/deck_outputs.json').read_text())
w, b = D['hours']['w'][0], D['hours']['b']
X, Y = D['HOURS']['x'], D['HOURS']['y']
print(f'hours fit: w = {w:.3f}, b = {b:.3f}; boundary at {-b / w:.2f} h')
for x in [3.0, 5.4, 7.0]:
    print(f'  x = {x} h: f = {w * x + b:+.2f}, p(pass) = {sig(w * x + b):.2f}')
mist = [(x, y) for x, y in zip(X, Y) if y * (w * x + b) <= 0]
print('  mistakes at the 0.5 threshold:', len(mist), sorted(mist), f'-> error rate {len(mist) / len(X):.0%}')
near = sorted(X, key=lambda x: abs(x + b / w))[:2]
print('  training points nearest the boundary:', sorted(near))
for t in [0.3, 0.7]:
    print(f'  threshold p > {t}: f > log(t/(1-t)) = {math.log(t / (1 - t)):+.3f}, x > {(math.log(t / (1 - t)) - b) / w:.2f} h')
print(f'  odds multiply by e^w = {math.exp(w):.2f} per extra hour')
f7, f8 = w * 7 + b, w * 8 + b
print(f'  odds at 7 h = {math.exp(f7):.2f}, at 8 h = {math.exp(f8):.2f}, ratio {math.exp(f8) / math.exp(f7):.2f}')
