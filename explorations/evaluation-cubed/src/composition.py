"""
Stage 5c: does the *composition* of the meta-benchmark decide whether it is informative?

Motivation. The first pass found that pooled meta-evaluation accuracy, computed over our
whole grid, correlates with a judge's resolution limit (rho = -0.875). So the blunt claim
"agreement is uninformative" is false, and we do not make it.

But that pooled accuracy was computed over a set that happens to contain (a) many
near-tie quality pairs and (b) systematic style variation. Real meta-benchmarks are not
built that way. They are typically built from *clear-cut* preference pairs -- that is the
explicit design goal of a preference benchmark, since ambiguous pairs are unreliable to
annotate -- and their two sides are often stylistically similar.

So we ablate the composition of the meta-benchmark and ask, each time: does the resulting
accuracy still tell you what the judge can resolve?

  full        every pair of answers to the same item, any quality gap, any style pair
  clearcut    only pairs with a large true quality gap (|dk| >= 3), the standard design
  matched     only pairs whose two sides share a style (no style variation to detect)
  clearcut+matched   both restrictions, i.e. a clean, well-annotated, stylistically
                     homogeneous meta-benchmark -- the thing the field aims to build

Outputs: results/composition.json
"""

from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis import KS, STYLES, load_scores, true_quality  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

FULL_GRID = [f"k{k}_{st}" for k in KS for st in STYLES]

COMPOSITIONS = {
    "full": lambda dk, same: True,
    "clearcut": lambda dk, same: dk >= 3,
    "matched": lambda dk, same: same,
    "clearcut+matched": lambda dk, same: dk >= 3 and same,
    "neartie": lambda dk, same: dk == 1,
}


def pair_accuracy(scores, items, keep) -> float:
    """Pooled item-level pairwise agreement with gold, over pairs passing `keep`."""
    ok, tot = 0.0, 0.0
    for it in items:
        for a, b in itertools.combinations(FULL_GRID, 2):
            ka, kb = int(a[1]), int(b[1])
            if ka == kb:
                continue
            if not keep(abs(ka - kb), a.split("_", 1)[1] == b.split("_", 1)[1]):
                continue
            va, vb = scores.get((it, a)), scores.get((it, b))
            if va is None or vb is None:
                continue
            tot += 1
            qa, qb = true_quality(ka), true_quality(kb)
            if va == vb:
                ok += 0.5
            elif (va > vb) == (qa > qb):
                ok += 1
    return ok / tot if tot else float("nan")


def main() -> None:
    res = json.load(open(os.path.join(RESULTS, "resolution.json")))
    judges = res["judges"]
    scores = load_scores()
    items = sorted({it for j in judges for (it, _) in scores[j]})

    limit = np.array([res["per_judge"][j]["observed_resolution_limit"] for j in judges])
    dstyle = np.array([res["per_judge"][j]["delta_style"] for j in judges])

    out = {"judges": judges, "compositions": {}}
    acc_by_comp = {}
    for name, keep in COMPOSITIONS.items():
        acc = np.array([pair_accuracy(scores[j], items, keep) for j in judges])
        acc_by_comp[name] = acc
        rho = stats.spearmanr(acc, limit).statistic
        r = stats.pearsonr(acc, limit).statistic
        out["compositions"][name] = {
            "accuracy": {j: float(a) for j, a in zip(judges, acc)},
            "mean_accuracy": float(np.nanmean(acc)),
            "sd_accuracy": float(np.nanstd(acc)),
            "range_accuracy": float(np.nanmax(acc) - np.nanmin(acc)),
            "spearman_with_limit": float(rho), "pearson_with_limit": float(r),
        }
        print(f"{name:<18} mean acc {np.nanmean(acc):.3f}  sd {np.nanstd(acc):.4f}  "
              f"range {np.nanmax(acc)-np.nanmin(acc):.3f}   "
              f"rho(acc, limit) = {rho:+.3f}   r = {r:+.3f}")

    rho_free = stats.spearmanr(dstyle, limit).statistic
    r_free = stats.pearsonr(dstyle, limit).statistic
    out["label_free"] = {"spearman_with_limit": float(rho_free),
                         "pearson_with_limit": float(r_free),
                         "delta_style": {j: float(d) for j, d in zip(judges, dstyle)}}
    print(f"\n{'delta_style (label-free)':<18} "
          f"rho = {rho_free:+.3f}   r = {r_free:+.3f}")

    # Calibration: can the meta-benchmark score be turned into a *number of claims*?
    # Fit limit ~ a + b*x and report the residual spread in quality units.
    print(f"\n{'predictor':<20} {'R^2':>7} {'resid sd (claims)':>18}")
    out["calibration"] = {}
    for name, acc in list(acc_by_comp.items()) + [("delta_style", dstyle)]:
        m = np.isfinite(acc) & np.isfinite(limit)
        b, a = np.polyfit(acc[m], limit[m], 1)
        pred = a + b * acc[m]
        ss_res = float(((limit[m] - pred) ** 2).sum())
        ss_tot = float(((limit[m] - limit[m].mean()) ** 2).sum())
        r2 = 1 - ss_res / ss_tot
        resid_sd = float(np.sqrt(ss_res / (m.sum() - 2)))
        out["calibration"][name] = {"r2": r2, "resid_sd_claims": resid_sd}
        print(f"{name:<20} {r2:7.3f} {resid_sd:18.4f}")

    with open(os.path.join(RESULTS, "composition.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {os.path.join(RESULTS, 'composition.json')}")


if __name__ == "__main__":
    main()
