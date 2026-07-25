"""
Stage 6b: does any of this survive on real systems?

The synthetic grid buys exact ground truth by constructing its systems. The obvious
objection is that constructed systems are not real ones. Here the systems are five actual
models answering freely, and their quality is **measured** (fraction of the item's six
reference claims supported minus contradicted) rather than designed.

Two things carry over unchanged:

  * the perturbation family -- we restyle each real answer into the same three styles, so
    the label-free style range R_J and the resolution limit delta_style are computable on
    real outputs exactly as before, with no quality labels;
  * the continuous quality axis -- mixing two models' answers item-by-item at rate p gives
    a system of quality (1-p)Q_A + p Q_B, so arbitrarily fine gaps come free again.

Outputs: results/real_analysis.json
"""

from __future__ import annotations

import itertools
import json
import os
import sys
from collections import defaultdict

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

STYLES = ["plain", "polished", "padded"]
N_PAIRS = 3000


def main() -> None:
    recs = json.load(open(os.path.join(DATA, "real_answers.json")))
    rows = [json.loads(l) for l in open(os.path.join(RESULTS, "real_pointwise.jsonl"))]

    models = sorted({r["model"] for r in recs})
    items = sorted({r["item_id"] for r in recs})
    judges = sorted({r["judge"] for r in rows})
    ii = {it: a for a, it in enumerate(items)}
    mi = {m: a for a, m in enumerate(models)}

    # ---- measured true quality of each real model (native style) -------------
    Q = np.full((len(models), len(items)), np.nan)
    for r in recs:
        if r["style"] == "native":
            Q[mi[r["model"]], ii[r["item_id"]]] = r["quality"]
    Qm = np.nanmean(Q, axis=1)
    print("measured quality of the real systems:")
    for m in models:
        print(f"  {m:<16} Q = {Qm[mi[m]]:.4f}")

    # restyling drift: how far measured quality moves when we restyle
    drift = [abs(r["quality_after_restyle"] - r["quality"])
             for r in recs if r["style"] != "native" and "quality_after_restyle" in r]
    print(f"restyle quality drift: mean {np.mean(drift):.4f}, "
          f"p95 {np.percentile(drift, 95):.4f} (in units of claim fraction)")

    # ---- judge scores S[judge, item, model, style] ---------------------------
    S = np.full((len(judges), len(items), len(models), len(STYLES)), np.nan)
    ji = {j: a for a, j in enumerate(judges)}
    for r in rows:
        if r["score"] is None or r["style"] == "native":
            continue
        S[ji[r["judge"]], ii[r["item_id"]], mi[r["model_under_test"]],
          STYLES.index(r["style"])] = (r["score"] - 1.0) / 9.0

    out = {"models": models, "judges": judges,
           "measured_quality": {m: float(Qm[mi[m]]) for m in models},
           "restyle_drift_mean": float(np.mean(drift)), "per_judge": {}}

    rng = np.random.default_rng(31)
    print(f"\n{'judge':<26} {'R_J':>7} {'slope':>7} {'d_style':>9} {'raw':>7} "
          f"{'cover':>7} {'certif':>8} {'abst':>7}")
    for j in judges:
        S_j = S[ji[j]]                                     # items x models x styles
        per_style = np.nanmean(S_j, axis=(0, 1))
        R = float(per_style.max() - per_style.min())       # label-free
        # slope of judge score on measured quality, across models (style-averaged)
        per_model = np.nanmean(S_j, axis=(0, 2))
        slope = float(np.polyfit(Qm, per_model, 1)[0])
        d_style = R / slope if slope > 1e-9 else float("inf")

        # continuous pairs: mix two models at rate p, assign styles independently
        n_ok = n_cert = n_cert_ok = n_abst = n_abst_ok = 0
        for _ in range(N_PAIRS):
            a, b = rng.choice(len(models), 2, replace=False)
            pa, pb = rng.uniform(0, 1), rng.uniform(0, 1)
            qa = (1 - pa) * Qm[a] + pa * Qm[b]
            qb = (1 - pb) * Qm[a] + pb * Qm[b]
            if abs(qa - qb) < 1e-6:
                continue
            sa, sb = rng.integers(0, len(STYLES), 2)
            maskA = rng.random(len(items)) < pa
            maskB = rng.random(len(items)) < pb
            va = float(np.nanmean(np.where(maskA, S_j[:, b, sa], S_j[:, a, sa])))
            vb = float(np.nanmean(np.where(maskB, S_j[:, b, sb], S_j[:, a, sb])))
            correct = (va > vb) == (qa > qb)
            n_ok += correct
            if abs(va - vb) > R:
                n_cert += 1
                n_cert_ok += correct
            else:
                n_abst += 1
                n_abst_ok += correct
        tot = n_cert + n_abst
        res = {
            "style_range_R": R, "quality_slope": slope, "delta_style": d_style,
            "raw_acc": n_ok / tot, "coverage": n_cert / tot,
            "certified_acc": n_cert_ok / n_cert if n_cert else float("nan"),
            "abstained_acc": n_abst_ok / n_abst if n_abst else float("nan"),
            "style_means": {s: float(v) for s, v in zip(STYLES, per_style)},
            "preferred_style": STYLES[int(np.argmax(per_style))],
            "model_ranking_correct": float(stats.spearmanr(Qm, per_model).statistic),
        }
        out["per_judge"][j] = res
        print(f"{j:<26} {R:7.4f} {slope:7.3f} {d_style:9.4f} {res['raw_acc']:7.3f} "
              f"{res['coverage']:7.3f} {res['certified_acc']:8.3f} "
              f"{res['abstained_acc']:7.3f}")

    agg = lambda k: float(np.nanmean([out["per_judge"][j][k] for j in judges]))
    out["summary"] = {k: agg(k) for k in
                      ("raw_acc", "coverage", "certified_acc", "abstained_acc", "delta_style")}
    print(f"\n{'MEAN':<26} {'':>7} {'':>7} {out['summary']['delta_style']:9.4f} "
          f"{out['summary']['raw_acc']:7.3f} {out['summary']['coverage']:7.3f} "
          f"{out['summary']['certified_acc']:8.3f} {out['summary']['abstained_acc']:7.3f}")

    pref = defaultdict(int)
    for j in judges:
        pref[out["per_judge"][j]["preferred_style"]] += 1
    out["style_preference_counts"] = dict(pref)
    print("preferred style:", dict(pref))

    with open(os.path.join(RESULTS, "real_analysis.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {os.path.join(RESULTS, 'real_analysis.json')}")


if __name__ == "__main__":
    main()
