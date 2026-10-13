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
print("all checks passed")
