"""Verify every number that appears on the slides (datasets, rates, AUCs).

Run: python3 check_numbers.py   (standard library only)
"""
from math import erf, sqrt

# Running example used on slides 3-7: 10 positives, 10 negatives, distinct scores.
POS = [0.95, 0.91, 0.86, 0.80, 0.74, 0.69, 0.62, 0.55, 0.43, 0.31]
NEG = [0.88, 0.71, 0.58, 0.50, 0.46, 0.38, 0.29, 0.22, 0.15, 0.07]


def rates(pos, neg, t):
    """Predict positive when score >= t. Return TP, FN, FP, TN, TPR, FPR."""
    tp = sum(s >= t for s in pos)
    fp = sum(s >= t for s in neg)
    fn, tn = len(pos) - tp, len(neg) - fp
    return tp, fn, fp, tn, tp / len(pos), fp / len(neg)


def auc_pairs(pos, neg):
    """Fraction of (positive, negative) pairs ranked correctly; ties count 1/2."""
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins, wins / (len(pos) * len(neg))


def auc_trapezoid(pos, neg):
    """Area under the ROC curve traced by sweeping t over every score."""
    ts = sorted(set(pos + neg), reverse=True)
    pts = [(0.0, 0.0)] + [(rates(pos, neg, t)[5], rates(pos, neg, t)[4]) for t in ts]
    return sum((x1 - x0) * (y0 + y1) / 2 for (x0, y0), (x1, y1) in zip(pts, pts[1:]))


def Phi(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


if __name__ == "__main__":
    assert len(set(POS + NEG)) == len(POS + NEG), "scores must be distinct"
    print("running example: AUC by pairs =", auc_pairs(POS, NEG),
          " by area =", round(auc_trapezoid(POS, NEG), 6))
    for t in (0.50, 0.65, 0.40):
        print(f"  t={t}: TP,FN,FP,TN,TPR,FPR =", rates(POS, NEG, t))

    # Exercise slide
    EX_POS, EX_NEG = [0.9, 0.8, 0.6], [0.7, 0.4, 0.2]
    print("exercise: t=0.5 ->", rates(EX_POS, EX_NEG, 0.5),
          " AUC =", auc_pairs(EX_POS, EX_NEG), round(auc_trapezoid(EX_POS, EX_NEG), 6))

    # Binormal model: negatives ~ N(0,1), positives ~ N(d,1). AUC = Phi(d / sqrt 2).
    for d in (0, 0.5, 1, 2, 3, -1):
        print(f"binormal d={d}: AUC = {Phi(d / sqrt(2)):.3f}")

    # Imbalance slide: fixed operating point, vary negatives per positive (r = N/P).
    TPR, FPR, P = 0.9, 0.01, 100
    for r in (1, 10, 100, 1000, 10000):
        N = r * P
        tp, fp = TPR * P, FPR * N
        print(f"r={r:>5}: TP={tp:.0f} FP={fp:.0f} precision={tp / (tp + fp):.3f}")
