"""
Stage 5b: the resolution-limit analysis. This is the core experiment.

WHY THIS REPLACED THE ORIGINAL DESIGN
-------------------------------------
The first design compared systems at corruption levels k=0..4, i.e. true quality gaps of
up to 4 of 6 atomic claims. At that separation almost every judge ranks perfectly
(SRA = 1.000 for 18 of 24 judge configurations). That is a real result, but it is the
uninteresting regime: no leaderboard decision turns on a system that is 67% less accurate.

Real leaderboards separate systems by small margins. So we need arbitrarily fine quality
gaps. We get them for free: a "system" need not corrupt every item equally. Define a
system by the *mean* corruption level m over items, realised by giving a fraction of items
k = floor(m) and the rest k = ceil(m). Its true quality is (6 - m)/6, and its judge score
is the mean of already-collected per-cell scores. So the entire continuous quality axis
costs zero additional API calls.

THE QUANTITY THIS EXPERIMENT ESTIMATES
--------------------------------------
    delta_style(J) = (range of J's score across quality-preserving restylings)
                     / (J's score change per unit of true quality)

Numerator and denominator are both estimable without any quality labels: the numerator
from restyling, the denominator from applying a *known* degradation. delta_style is
therefore a label-free quantity, and it has units of true quality ("claims of factual
content"). It is the true quality difference that a judge's style preference can
counterfeit -- the judge's **resolution limit**.

Prediction from Proposition 1: system pairs separated by less than delta_style can be
ordered wrongly by an adversarial style assignment; pairs separated by more cannot.

Outputs: results/resolution.json
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis import KS, STYLES, load_scores  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

N_CLAIMS = 6
M_CENTRE = 2.0              # centre the sweep away from the k=0 and k=4 edges
N_ASSIGN = 400              # random item->level assignments per configuration
GAPS = np.concatenate([np.arange(0.05, 1.0, 0.05), np.arange(1.0, 3.05, 0.25)])


def build_cube(scores, judges, items):
    """S[judge, item, k, style]."""
    S = np.full((len(judges), len(items), len(KS), len(STYLES)), np.nan)
    ii = {it: a for a, it in enumerate(items)}
    for jx, j in enumerate(judges):
        for (it, sysname), v in scores[j].items():
            k = int(sysname[1])
            st = sysname.split("_", 1)[1]
            if it in ii and st in STYLES:
                S[jx, ii[it], k, STYLES.index(st)] = v
    return S


def mixture_scores(S_js, m, rng, n_assign):
    """Mean judge score of a system with mean corruption level m, in one style.

    S_js: (items, k) slice for one judge and one style.
    Returns an array of n_assign realisations (the item->level assignment is random)."""
    n_items = S_js.shape[0]
    lo, hi = int(np.floor(m)), int(np.ceil(m))
    if lo == hi:
        return np.full(n_assign, np.nanmean(S_js[:, lo]))
    frac_hi = m - lo
    n_hi = int(round(frac_hi * n_items))
    out = np.empty(n_assign)
    base = S_js[:, lo]
    delta = S_js[:, hi] - S_js[:, lo]
    for r in range(n_assign):
        idx = rng.choice(n_items, n_hi, replace=False)
        out[r] = np.nanmean(base) + np.nansum(delta[idx]) / n_items
    return out


def quality_slope(S_j):
    """Judge score change per unit of TRUE quality, estimated from the known degradation.

    Label-free: it uses only the fact that level k has k of 6 claims corrupted, which is a
    property of the transformation we applied, not an annotation of any output."""
    per_k = np.nanmean(S_j, axis=(0, 2))              # mean over items and styles -> (k,)
    q = np.array([(N_CLAIMS - k) / N_CLAIMS for k in KS])
    return float(np.polyfit(q, per_k, 1)[0])


def style_range(S_j):
    """Range of the judge's mean score across quality-preserving restylings. Label-free."""
    per_style = np.nanmean(S_j, axis=(0, 1))          # -> (style,)
    return float(per_style.max() - per_style.min())


def main() -> None:
    scores = load_scores()
    judges = sorted(scores)
    items = sorted({it for j in judges for (it, _) in scores[j]})
    judges = [j for j in judges if len(scores[j]) >= 0.98 * len(items) * 15]
    S = build_cube(scores, judges, items)
    print(f"cube: {S.shape} (judge, item, k, style); NaNs {np.isnan(S).mean():.4f}")

    rng = np.random.default_rng(3)
    out = {"judges": judges, "gaps": GAPS.tolist(), "n_assign": N_ASSIGN,
           "styles": STYLES, "per_judge": {}}

    print(f"\n{'judge':<28} {'slope':>7} {'R_style':>8} {'delta_style':>12} "
          f"{'pref+':>9} {'pref-':>9}")
    for jx, j in enumerate(judges):
        S_j = S[jx]
        slope = quality_slope(S_j)
        R = style_range(S_j)
        d_style = R / slope if slope > 1e-9 else float("inf")
        per_style = np.nanmean(S_j, axis=(0, 1))
        best_st = STYLES[int(np.argmax(per_style))]
        worst_st = STYLES[int(np.argmin(per_style))]
        out["per_judge"][j] = {
            "quality_slope": slope, "style_range": R, "delta_style": d_style,
            "preferred_style": best_st, "dispreferred_style": worst_st,
            "style_means": {s: float(v) for s, v in zip(STYLES, per_style)},
        }
        print(f"{j:<28} {slope:7.3f} {R:8.4f} {d_style:12.4f} "
              f"{best_st:>9} {worst_st:>9}")

    # ---- fidelity as a function of the true quality gap ----------------------
    # Three style regimes:
    #   matched     : both systems in the same style (no confound)
    #   adversarial : the WORSE system wears the judge's preferred style
    #   random      : style drawn independently per system
    print("\nsweeping quality gaps ...")
    for jx, j in enumerate(judges):
        S_j = S[jx]
        info = out["per_judge"][j]
        b = STYLES.index(info["preferred_style"])
        w = STYLES.index(info["dispreferred_style"])
        curves = {"matched": [], "adversarial": [], "random": []}
        for gap in GAPS:
            mA, mB = M_CENTRE - gap / 2, M_CENTRE + gap / 2   # A is better (less corrupt)
            if mA < 0 or mB > 4:
                for c in curves:
                    curves[c].append(float("nan"))
                continue
            # matched: both in the dispreferred style (arbitrary; same-style is the point)
            a = mixture_scores(S_j[:, :, w], mA, rng, N_ASSIGN)
            bb = mixture_scores(S_j[:, :, w], mB, rng, N_ASSIGN)
            curves["matched"].append(float(np.mean(a > bb) + 0.5 * np.mean(a == bb)))
            # adversarial: better system in the dispreferred style, worse in preferred
            a = mixture_scores(S_j[:, :, w], mA, rng, N_ASSIGN)
            bb = mixture_scores(S_j[:, :, b], mB, rng, N_ASSIGN)
            curves["adversarial"].append(float(np.mean(a > bb) + 0.5 * np.mean(a == bb)))
            # random style assignment
            hits = []
            for _ in range(4):
                s1, s2 = rng.integers(0, len(STYLES), 2)
                a = mixture_scores(S_j[:, :, s1], mA, rng, N_ASSIGN // 4)
                bb = mixture_scores(S_j[:, :, s2], mB, rng, N_ASSIGN // 4)
                hits.append(np.mean(a > bb) + 0.5 * np.mean(a == bb))
            curves["random"].append(float(np.mean(hits)))
        info["curves"] = curves

        # observed resolution limit: smallest gap beyond which the adversarial curve
        # stays above 0.95 for every larger gap tested
        adv = np.array(curves["adversarial"], dtype=float)
        good = adv >= 0.95
        limit = float("nan")
        for gi in range(len(GAPS)):
            if np.all(good[gi:][~np.isnan(adv[gi:])]):
                limit = float(GAPS[gi]) / N_CLAIMS
                break
        info["observed_resolution_limit"] = limit

    print(f"\n{'judge':<28} {'predicted d_style':>18} {'observed limit':>15} "
          f"{'matched@0.05':>13}")
    for j in judges:
        i = out["per_judge"][j]
        m0 = i["curves"]["matched"][0]
        print(f"{j:<28} {i['delta_style']:18.4f} {i['observed_resolution_limit']:15.4f} "
              f"{m0:13.3f}")

    pred = np.array([out["per_judge"][j]["delta_style"] for j in judges])
    obs = np.array([out["per_judge"][j]["observed_resolution_limit"] for j in judges])
    ok = np.isfinite(pred) & np.isfinite(obs)
    from scipy import stats as st
    out["prediction_check"] = {
        "spearman": float(st.spearmanr(pred[ok], obs[ok]).statistic),
        "pearson": float(st.pearsonr(pred[ok], obs[ok]).statistic),
        "n": int(ok.sum()),
        "mean_pred": float(pred[ok].mean()), "mean_obs": float(obs[ok].mean()),
    }
    print(f"\nlabel-free prediction vs observed resolution limit: "
          f"rho={out['prediction_check']['spearman']:.3f}, "
          f"r={out['prediction_check']['pearson']:.3f}, n={int(ok.sum())}")

    with open(os.path.join(RESULTS, "resolution.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {os.path.join(RESULTS, 'resolution.json')}")


if __name__ == "__main__":
    main()
