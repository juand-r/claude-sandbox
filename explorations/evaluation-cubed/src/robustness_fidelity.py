"""
Robustness check: does the 2.2% of cells with imperfect rendering fidelity matter?

The construction assigns each cell an intended quality (6-k)/6, and every analysis uses that
intended value as ground truth. But the renderer is an LLM, and in 28 of 1275 cells it quietly
repaired a corrupted claim (or dropped a true one), so those cells' real quality differs from
the intended value by one claim out of six.

This is small, but it is ground-truth error in a paper whose whole point is that ground truth
should be constructed rather than estimated. So we check it two ways:

  exclude   drop every item that has any unfaithful cell, and redo the headline analysis
  verified  keep everything but score each cell by the claims the checker actually found

If the headline (the label-free predictor recovers the measured resolution limit) survives
both, the fidelity slippage is not load-bearing.

Outputs: results/robustness_fidelity.json
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis import KS, STYLES, load_scores  # noqa: E402
from resolution import (  # noqa: E402
    GAPS, M_CENTRE, N_CLAIMS, build_cube, mixture_scores, quality_slope, style_range,
)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")


def limits_and_predictor(S, judges, rng):
    """Return (label-free predictor gamma, measured resolution limit) per judge."""
    gam, lim = [], []
    for jx in range(len(judges)):
        S_j = S[jx]
        slope = quality_slope(S_j)
        R = style_range(S_j)
        gam.append(R / slope if slope > 1e-9 else np.inf)
        per_style = np.nanmean(S_j, axis=(0, 1))
        b, w = int(np.argmax(per_style)), int(np.argmin(per_style))
        adv = []
        for gap in GAPS:
            mA, mB = M_CENTRE - gap / 2, M_CENTRE + gap / 2
            if mA < 0 or mB > 4:
                adv.append(np.nan)
                continue
            a = mixture_scores(S_j[:, :, w], mA, rng, 200)
            bb = mixture_scores(S_j[:, :, b], mB, rng, 200)
            adv.append(np.mean(a > bb) + 0.5 * np.mean(a == bb))
        adv = np.array(adv, dtype=float)
        good = adv >= 0.95
        L = np.nan
        for gi in range(len(GAPS)):
            seg = good[gi:][~np.isnan(adv[gi:])]
            if seg.size and seg.all():
                L = GAPS[gi] / N_CLAIMS
                break
        lim.append(L)
    return np.array(gam), np.array(lim)


def report(name, gam, lim, out):
    m = np.isfinite(gam) & np.isfinite(lim)
    rho = stats.spearmanr(gam[m], lim[m]).statistic
    r = stats.pearsonr(gam[m], lim[m]).statistic
    b, a = np.polyfit(gam[m], lim[m], 1)
    pred = a + b * gam[m]
    ss_res = float(((lim[m] - pred) ** 2).sum())
    ss_tot = float(((lim[m] - lim[m].mean()) ** 2).sum())
    res = {"n_judges": int(m.sum()), "spearman": float(rho), "pearson": float(r),
           "r2": 1 - ss_res / ss_tot,
           "resid_sd": float(np.sqrt(ss_res / (m.sum() - 2))),
           "limit_min": float(lim[m].min()), "limit_max": float(lim[m].max()),
           "limit_ratio": float(lim[m].max() / lim[m].min())}
    out[name] = res
    print(f"{name:<26} rho={rho:+.3f} r={r:+.3f} R2={res['r2']:.3f} "
          f"resid={res['resid_sd']:.4f} spread={res['limit_ratio']:.0f}x")
    return res


def main() -> None:
    answers = json.load(open(os.path.join(DATA, "answers.json")))
    scores = load_scores()
    judges = sorted(scores)
    all_items = sorted({it for j in judges for (it, _) in scores[j]})
    judges = [j for j in judges if len(scores[j]) >= 0.98 * len(all_items) * 15]

    bad_cells = [r for r in answers if r["render_faithful"] < N_CLAIMS]
    bad_items = sorted({r["item_id"] for r in bad_cells})
    print(f"cells with an unfaithful claim slot: {len(bad_cells)}/{len(answers)} "
          f"({len(bad_cells)/len(answers):.4f}), spread over {len(bad_items)} of "
          f"{len(all_items)} items")

    out = {"n_bad_cells": len(bad_cells), "n_cells": len(answers),
           "n_bad_items": len(bad_items), "n_items": len(all_items)}

    rng = np.random.default_rng(101)
    S_all = build_cube(scores, judges, all_items)
    g, l = limits_and_predictor(S_all, judges, rng)
    report("as reported (all items)", g, l, out)

    keep = [it for it in all_items if it not in set(bad_items)]
    print(f"\nexcluding the {len(bad_items)} affected items -> {len(keep)} items")
    S_keep = build_cube(scores, judges, keep)
    g2, l2 = limits_and_predictor(S_keep, judges, rng)
    report("affected items excluded", g2, l2, out)

    out["rank_agreement_of_predictor"] = float(stats.spearmanr(g, g2).statistic)
    out["rank_agreement_of_limit"] = float(stats.spearmanr(l, l2).statistic)
    print(f"\npredictor rank agreement before/after exclusion: "
          f"rho={out['rank_agreement_of_predictor']:.3f}")
    print(f"limit rank agreement before/after exclusion:     "
          f"rho={out['rank_agreement_of_limit']:.3f}")

    with open(os.path.join(RESULTS, "robustness_fidelity.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {os.path.join(RESULTS, 'robustness_fidelity.json')}")


if __name__ == "__main__":
    main()
