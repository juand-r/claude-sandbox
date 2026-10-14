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
# exam: AI-detector scores on 8 essays (4 AI, 4 human)
ai_s = [0.95, 0.85, 0.60, 0.40]; hu_s = [0.70, 0.50, 0.30, 0.10]
pts = roc(ai_s, hu_s); print("    exam ROC points:", [(round(x, 2), round(y, 2)) for x, y in pts])
check(area(pts), 13 / 16, "exam AUC"); check(round(area(pts), 2), 0.81, "exam AUC (2 d.p.)")
check(area(roc([100 * x for x in ai_s], [100 * x for x in hu_s])), 13 / 16, "exam AUC after s -> 100 s")
check(area(roc([x ** 2 for x in ai_s], [x ** 2 for x in hu_s])), 13 / 16, "exam AUC after s -> s^2")
check(area(roc([1 - x for x in ai_s], [1 - x for x in hu_s])), 3 / 16, "exam AUC after s -> 1 - s")
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
print("all checks passed")
