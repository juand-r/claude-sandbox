"""Recompute every number in the midterm problems (standard library only).

Usage: python3 check_numbers.py   (ends with "all checks passed")
"""


def check(got, want, what, tol=1e-9):
    assert abs(got - want) <= tol, f"{what}: {got} vs {want}"
    print(f"ok  {what}: {got:.4g}")


# ---------------------------------------------------------------- practice: mine-detection rat (rates given)
squares, mines = 1000, 40
rat_recall, rat_fpr = 0.95, 0.05            # indicates 95% of mine squares, 5% of mine-free squares
clear = squares - mines
tp = rat_recall * mines; fn = mines - tp; fp = rat_fpr * clear; tn = clear - fp
for v, w, s in [(tp, 38, "rat TP"), (fn, 2, "rat FN"), (fp, 48, "rat FP"), (tn, 912, "rat TN")]:
    check(v, w, s)
check(tp / (tp + fp), 38 / 86, "rat precision"); check(round(tp / (tp + fp), 2), 0.44, "rat precision (2 d.p.)")
check(tp / mines, 0.95, "rat recall")
check((tp + tn) / squares, 0.95, "rat accuracy")
check(clear / squares, 0.96, "accuracy of a rat that never indicates")
check(fp / (tp + fp), 48 / 86, "share of rat digs that are wasted"); check(round(fp / (tp + fp), 2), 0.56, "  (2 d.p.)")
det_recall, det_fpr = 1.0, 0.30             # metal detector: every mine, and 30% of mine-free squares (scrap metal)
dtp = det_recall * mines; dfn = mines - dtp; dfp = det_fpr * clear; dtn = clear - dfp
for v, w, s in [(dtp, 40, "detector TP"), (dfn, 0, "detector FN"), (dfp, 288, "detector FP"), (dtn, 672, "detector TN")]:
    check(v, w, s)
check(round(dtp / (dtp + dfp), 2), 0.12, "detector precision (40/328, 2 d.p.)")
check(dtp / mines, 1.0, "detector recall")
check((dtp + dtn) / squares, 0.712, "detector accuracy")
check(round(dfp / (dtp + dfp), 2), 0.88, "share of detector digs that are wasted")
check(fn, 2, "rat first, dig only rat-flagged squares: mines left in the field")

# ---------------------------------------------------------------- exam: AI-text detector (counts given)
essays, ai, flagged, flagged_ai = 400, 60, 50, 45
tp = flagged_ai; fp = flagged - flagged_ai; fn = ai - tp; tn = essays - ai - fp
for v, w, s in [(tp, 45, "AI TP"), (fp, 5, "AI FP"), (fn, 15, "AI FN"), (tn, 335, "AI TN")]:
    check(v, w, s)
check(tp / (tp + fp), 0.90, "AI precision"); check(tp / ai, 0.75, "AI recall")
check((tp + tn) / essays, 0.95, "AI accuracy"); check((essays - ai) / essays, 0.85, "accuracy of flagging nothing")
check(fp / flagged, 0.10, "share of accused students who wrote their own essay")
# ---------------------------------------------------------------- ROC / AUC parts (no tied scores)
def roc(pos, neg):
    """(FPR, TPR) points as the threshold sweeps down past each score, from (0, 0) to (1, 1)."""
    assert not set(pos) & set(neg), "no ties between a positive and a negative"
    items = sorted([(x, 1) for x in pos] + [(x, 0) for x in neg], reverse=True)
    pts, tp, fp = [(0.0, 0.0)], 0, 0
    for _, y in items:
        tp += y; fp += 1 - y; pts.append((fp / len(neg), tp / len(pos)))
    return pts


def area(pts):
    """Area under a staircase or piecewise-linear curve (trapezoids; exact for a staircase)."""
    return sum((x1 - x0) * (y0 + y1) / 2 for (x0, y0), (x1, y1) in zip(pts, pts[1:]))


# practice: metal-detector signal strength on 10 squares (5 with a mine, 5 without)
mine = [9.1, 8.3, 6.0, 5.2, 2.5]; clean = [7.4, 4.8, 3.9, 2.0, 1.1]
pts = roc(mine, clean); print("    practice ROC points:", [(round(x, 1), round(y, 1)) for x, y in pts])
check(area(pts), 0.80, "practice AUC")
check(area(roc([-x for x in mine], [-x for x in clean])), 0.20, "practice AUC after s -> -s")
check(area(roc([x ** 0.5 for x in mine], [x ** 0.5 for x in clean])), 0.80, "practice AUC after s -> sqrt(s)")
# lowest threshold that still flags every mine is 2.5: then 3 of 5 clean squares (7.4, 4.8, 3.9) are flagged
check(sum(c >= 2.5 for c in clean) / 5, 0.6, "practice FPR at TPR = 1")
check(sum(m > 7.4 for m in mine) / 5, 0.4, "practice TPR at FPR = 0")
# practice (final version): TB rats, pause times on 10 samples (5 TB, 5 not)
samples, tb = 1000, 100
tp = 0.8 * tb; fn = tb - tp; fp = 0.1 * (samples - tb); tn = samples - tb - fp
for v, w, what in [(tp, 80, "TB TP"), (fn, 20, "TB FN"), (fp, 90, "TB FP"), (tn, 810, "TB TN")]:
    check(v, w, what)
check(round(tp / (tp + fp), 2), 0.47, "TB precision"); check(tp / tb, 0.80, "TB recall")
pause = dict(A=2.6, B=0.6, C=4.6, D=2.0, E=1.3, F=3.7, G=4.2, H=1.0, I=3.0, J=2.4)
has_tb = set("ACEGI")
pts = roc([pause[k] for k in has_tb], [pause[k] for k in pause if k not in has_tb])
want = [(0, 0), (0, .2), (0, .4), (.2, .4), (.2, .6), (.2, .8), (.4, .8), (.6, .8), (.6, 1), (.8, 1), (1, 1)]
assert all(abs(x - a) < 1e-9 and abs(y - b) < 1e-9 for (x, y), (a, b) in zip(pts, want)) and len(pts) == len(want), pts
print("ok  TB ROC points match the solution")
check(area(pts), 0.80, "TB AUC")
# exam: AI-detector scores on 8 essays (4 AI, 4 human)
ai_s = [0.95, 0.85, 0.60, 0.40]; hu_s = [0.70, 0.50, 0.30, 0.10]
pts = roc(ai_s, hu_s); print("    exam ROC points:", [(round(x, 2), round(y, 2)) for x, y in pts])
check(area(pts), 13 / 16, "exam AUC"); check(round(area(pts), 2), 0.81, "exam AUC (2 d.p.)")
check(area(roc([100 * x for x in ai_s], [100 * x for x in hu_s])), 13 / 16, "exam AUC after s -> 100 s")
check(area(roc([x ** 2 for x in ai_s], [x ** 2 for x in hu_s])), 13 / 16, "exam AUC after s -> s^2")
check(area(roc([1 - x for x in ai_s], [1 - x for x in hu_s])), 3 / 16, "exam AUC after s -> 1 - s")
# exam version 2 (final_midterm2.tex): 1.4 asks for the three points after (0, 0); 1.5 flips an AUC of 0.3
for k, (x, y) in enumerate([(0.0, 0.25), (0.0, 0.5), (0.25, 0.5)], 1):
    check(pts[k][0], x, f"exam v2 1.4: ROC point {k} after (0, 0), FPR"); check(pts[k][1], y, "  TPR")
check(area(roc([1 - x for x in ai_s], [1 - x for x in hu_s])), 1 - area(pts), "flipping the scores turns AUC a into 1 - a (so 0.3 -> 0.7)")
check(sum(a > 0.70 for a in ai_s) / 4, 0.5, "exam TPR at FPR = 0 (threshold above 0.70)")
check(0.5 ** 2, 0.25, "exam: threshold 0.5 becomes 0.25 after squaring")
# two crossing ROC curves, straight lines between the given points
A = [(0, 0), (0, .5), (.2, .7), (.4, .8), (.6, 1), (1, 1)]
B = [(0, 0), (.1, .3), (.2, .6), (.3, 1), (1, 1)]
check(area(A), 0.85, "curve A AUC"); check(area(B), 0.84, "curve B AUC")
# ---------------------------------------------------------------- SVM: a trained soft-margin SVC (practice and exam)
import math
for ver, w, b, pts, want in [
        ("practice", (4, 3), -12, [((3, 1), 1), ((1, 2), -1), ((2.5, 1), 1), ((1, 2.5), -1), ((3, 0.5), -1)],
         dict(f=[3, -2, 1, -0.5, 1.5], dist=[0.6, 0.4, 0.2, 0.1, 0.3], margin=0.4)),
        ("exam", (6, 8), -20, [((3, 1), 1), ((1, 1), -1), ((1.5, 1.5), 1), ((1.25, 1.5), -1), ((3, 0.5), -1)],
         dict(f=[6, -6, 1, -0.5, 2], dist=[0.6, 0.6, 0.1, 0.05, 0.2], margin=0.2))]:
    nw = math.hypot(*w); check(2 / nw, want["margin"], f"{ver} SVM margin width")
    fs = [w[0] * x[0] + w[1] * x[1] + b for x, _ in pts]
    for k, (f, (x, y)) in enumerate(zip(fs, pts)):
        check(f, want["f"][k], f"{ver} SVM f(point {'ABCDE'[k]})"); check(abs(f) / nw, want["dist"][k], f"  distance")
    yf = [y * f for f, (_, y) in zip(fs, pts)]
    assert [k for k, v in enumerate(yf) if v <= 1] == [2, 3, 4]; assert yf[2] == 1 and 0 < yf[3] < 1 and yf[4] < 0
    print(f"ok  {ver} SVM: support vectors C, D, E; C on the margin, D inside it, E misclassified")
# ---------------------------------------------------------------- nonlinear regression
# exam 3.1: kNN regression at x = 4.4
xs, ys, x0 = [1, 2, 4, 5, 7, 8], [3, 6, 4, 8, 10, 12], 4.4
order = sorted(range(len(xs)), key=lambda i: abs(xs[i] - x0))
assert len({abs(xs[i] - x0) for i in order[:4]}) == 4, "no ties among the nearest points"
check(ys[order[0]], 4, "exam kNN k = 1 prediction")
check(sum(ys[i] for i in order[:3]) / 3, 6, "exam kNN k = 3 prediction (x = 4, 5, 2)")
# practice 3.1: the regression-tree split x < 3.5
ys = [1, 3, 2, 7, 9, 8]; left, right = ys[:3], ys[3:]
ml, mr = sum(left) / 3, sum(right) / 3
check(ml, 2, "practice tree: left leaf"); check(mr, 8, "practice tree: right leaf")
check(sum((v - ml) ** 2 for v in left) + sum((v - mr) ** 2 for v in right), 4, "practice tree: SSE")
# ---------------------------------------------------------------- ensembles
from math import comb
def vote_error(n, e):
    """Error of a majority vote of n independent classifiers, each with error e (n odd)."""
    return sum(comb(n, k) * e**k * (1 - e)**(n - k) for k in range(n // 2 + 1, n + 1))
check(round(vote_error(25, 0.35), 2), 0.06, "practice 5.2: vote of 25 at error 0.35")
check(round(vote_error(25, 0.6), 2), 0.85, "exam 5.2: vote of 25 at error 0.6")
# practice 5.1(c): every class on the predicted side A gets one vote
sides = [{"oak", "maple"}, {"maple", "pine"}, {"maple", "birch", "willow"}]
votes = {c: sum(c in a for a in sides) for c in ["oak", "maple", "pine", "birch", "willow"]}
assert votes == {"oak": 1, "maple": 3, "pine": 1, "birch": 1, "willow": 1}, votes
print(f"ok  practice 5.1(c) votes: {votes}")
check(comb(5, 2), 10, "practice 5.1(b): one-vs-one SVMs"); check(comb(4, 2), 6, "exam 5.1(c): one-vs-one SVMs")
# ---------------------------------------------------------------- exam v2 4.1: forward pass, ReLU hidden layer, linear outputs
x41, W1e, b1e, W2e, b2e = [4, 2], [[0.5, -0.5], [-0.3, 0.4]], [0.5, -0.2], [[0.6, 0.8], [-0.2, -0.9]], [-0.4, 0.6]
lin = lambda W, b, v: [sum(w * u for w, u in zip(r, v)) + c for r, c in zip(W, b)]
zB = lin(W1e, b1e, x41); Bv = [max(0.0, z) for z in zB]; Cv = lin(W2e, b2e, Bv)
for got, want, what in [(zB[0], 1.5, "zB1"), (zB[1], -0.6, "zB2"), (Bv[1], 0.0, "B2 = ReLU(-0.6)"), (Cv[0], 0.5, "out1"), (Cv[1], 0.3, "out2")]:
    check(got, want, f"exam v2 4.1: {what}")
assert Cv[0] > Cv[1], "exam v2 4.1: Class A"
Cn = lin(W2e, b2e, zB)   # a student who forgets the ReLU
check(Cn[0], 0.02, "exam v2 4.1 without the ReLU: out1"); check(Cn[1], 0.84, "  out2 (so Class B, the wrong answer)")
# ---------------------------------------------------------------- exam v2 4.2: backprop, sigmoid hidden and output, cross-entropy
sg = lambda z: 1 / (1 + math.exp(-z))
A42, W1b, b1b, W2b, b2b, Y42 = [2, 1], [[0.5, -1.0], [1.5, 0.5]], [0.5, -1.0], [1.0, -2.0], 0.5, 1
zB42 = lin(W1b, b1b, A42); B42 = [sg(z) for z in zB42]; p42 = sg(lin([W2b], [b2b], B42)[0])
check(round(B42[0], 2), 0.62, "exam v2 4.2: given B1"); check(round(B42[1], 2), 0.92, "  given B2"); check(round(p42, 2), 0.33, "  given p")
# the solution works from the given (rounded) node values
Br, pr = 0.62, 0.33
gW2 = (pr - Y42) * Br; gW1 = (pr - Y42) * W2b[0] * Br * (1 - Br) * A42[0]
check(round(gW2, 3), -0.415, "exam v2 4.2(a): dE/dW2_11 from the given values"); check(round(1.0 - gW2, 3), 1.415, "  updated W2_11")
check(round((pr - Y42) * W2b[0] * Br * (1 - Br), 3), -0.158, "exam v2 4.2(b): dE/dz_B1"); check(round(gW1, 3), -0.316, "  dE/dW1_11")
check(round(0.5 - gW1, 3), 0.816, "  updated W1_11")
# unrounded, and against a numerical derivative of the loss
def E42(w1, w2):
    B = [sg(z) for z in lin([[w1, W1b[0][1]], W1b[1]], b1b, A42)]
    return -math.log(sg(lin([[w2, W2b[1]]], [b2b], B)[0]))
h = 1e-6
nW1 = (E42(0.5 + h, 1.0) - E42(0.5 - h, 1.0)) / (2 * h); nW2 = (E42(0.5, 1.0 + h) - E42(0.5, 1.0 - h)) / (2 * h)
check(nW1, (p42 - 1) * 1.0 * B42[0] * (1 - B42[0]) * 2, "exam v2 4.2: chain rule = numerical derivative (W1_11)", 1e-8)
check(nW2, (p42 - 1) * B42[0], "  (W2_11)", 1e-8)
check(round(1.0 - nW2, 3), 1.419, "  unrounded updated W2_11"); check(round(0.5 - nW1, 3), 0.817, "  unrounded updated W1_11")
# exam v2 4.3(c): gradient steps in 5 epochs over 1,000 records
for size, want, what in [(1000, 5, "batch"), (1, 5000, "stochastic"), (50, 100, "mini-batches of 50")]:
    check(5 * (1000 // size), want, f"exam v2 4.3(c): steps with {what}")
print("all checks passed")
