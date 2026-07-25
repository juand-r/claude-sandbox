"""
Stage 5d: does the label-free certificate work where it matters?

On the coarse grid (quality gaps of 1-4 of 6 claims) raw ranking accuracy is already 0.977,
so a certificate has little room to help. The regime that matters is the one leaderboards
live in: system pairs separated by small margins, rendered in whatever style each system
happens to produce.

So we draw random system pairs from the continuous mixture family -- random quality gap,
random (independent) style for each side -- and ask, for each judge:

  raw          how often the judge's ordering is correct if you simply trust it
  coverage     what fraction of pairs the certificate is willing to certify
  certified    how often the ordering is correct ON the certified pairs
  abstained    how often it is correct on the pairs the certificate refuses

The certificate rule is Theorem 2: certify the pair iff |Qhat(s) - Qhat(s')| > R_J, where
R_J is the judge's style-induced score range -- measured with no quality labels at all.

Outputs: results/certificate_eval.json
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis import KS, STYLES, load_scores  # noqa: E402
from resolution import build_cube, mixture_scores, quality_slope, style_range  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

N_CLAIMS = 6
N_PAIRS = 4000
MAX_GAP_CLAIMS = 1.0   # leaderboard regime: at most 1 of 6 claims apart (<=16.7%)
SPLIT_HALF = True      # estimate R_J on one half of the items, evaluate on the other


def main() -> None:
    scores = load_scores()
    judges = sorted(scores)
    items = sorted({it for j in judges for (it, _) in scores[j]})
    judges = [j for j in judges if len(scores[j]) >= 0.98 * len(items) * 15]
    S = build_cube(scores, judges, items)

    rng = np.random.default_rng(23)
    out = {"judges": judges, "n_pairs": N_PAIRS, "max_gap_claims": MAX_GAP_CLAIMS,
           "per_judge": {}}

    # Split-half: the threshold R_J must be estimated from data, so estimating it on the
    # same items used to evaluate the certificate would flatter it. We estimate on a random
    # half of the items and evaluate on the held-out half.
    n_items = S.shape[1]
    perm = rng.permutation(n_items)
    est_idx, ev_idx = perm[: n_items // 2], perm[n_items // 2:]

    def run(split_half: bool, label: str) -> dict:
      print(f"\n--- {label} ---")
      print(f"{'judge':<28} {'R_J':>7} {'raw':>7} {'cover':>7} {'certified':>10} "
            f"{'abstained':>10}")
      agg = {"raw": [], "cov": [], "cert": [], "abst": []}
      per = {}
      for jx, j in enumerate(judges):
        S_j = S[jx]
        if split_half:
            # threshold estimated on items disjoint from those used to evaluate it
            R = style_range(S_j[est_idx])
            S_j = S_j[ev_idx]
        else:
            R = style_range(S_j)          # label-free
        n_ok = n_cert = n_cert_ok = n_abst = n_abst_ok = 0
        for _ in range(N_PAIRS):
            mA = rng.uniform(0, 4 - MAX_GAP_CLAIMS)
            gap = rng.uniform(0.05, MAX_GAP_CLAIMS)
            mB = mA + gap
            sA, sB = rng.integers(0, len(STYLES), 2)
            qa = mixture_scores(S_j[:, :, sA], mA, rng, 1)[0]
            qb = mixture_scores(S_j[:, :, sB], mB, rng, 1)[0]
            correct = qa > qb            # A is better (less corrupted)
            n_ok += correct
            if abs(qa - qb) > R:
                n_cert += 1
                n_cert_ok += correct
            else:
                n_abst += 1
                n_abst_ok += correct
        res = {
            "style_range_R": float(R),
            "raw_acc": n_ok / N_PAIRS,
            "coverage": n_cert / N_PAIRS,
            "certified_acc": n_cert_ok / n_cert if n_cert else float("nan"),
            "abstained_acc": n_abst_ok / n_abst if n_abst else float("nan"),
        }
        per[j] = res
        agg["raw"].append(res["raw_acc"])
        agg["cov"].append(res["coverage"])
        agg["cert"].append(res["certified_acc"])
        agg["abst"].append(res["abstained_acc"])
        print(f"{j:<28} {R:7.4f} {res['raw_acc']:7.3f} {res['coverage']:7.3f} "
              f"{res['certified_acc']:10.3f} {res['abstained_acc']:10.3f}")
      summary = {k: float(np.nanmean(v)) for k, v in agg.items()}
      summary["worst_raw"] = float(np.min(agg["raw"]))
      summary["worst_certified"] = float(np.nanmin(agg["cert"]))
      summary["n_eval_items"] = len(ev_idx) if split_half else S.shape[1]
      print(f"{'MEAN':<28} {'':>7} {summary['raw']:7.3f} {summary['cov']:7.3f} "
            f"{summary['cert']:10.3f} {summary['abst']:10.3f}")
      return {"per_judge": per, "summary": summary}

    # Two configurations. `full_sample` uses all 85 items for both estimating R and
    # evaluating; `split_half` estimates R on 42 items and evaluates on the disjoint 43.
    # Note the split-half run also *halves the evaluation set*, which independently adds
    # sampling noise to every system mean and so lowers raw accuracy too -- the two effects
    # are reported together, not disentangled.
    full = run(False, "full sample (85 items for both)")
    half = run(True, "split half (R on 42 items, evaluated on the disjoint 43)")
    out["full_sample"], out["split_half"] = full, half
    out["per_judge"] = full["per_judge"]
    out["summary"] = full["summary"]
    out["summary_split_half"] = half["summary"]

    with open(os.path.join(RESULTS, "certificate_eval.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {os.path.join(RESULTS, 'certificate_eval.json')}")


if __name__ == "__main__":
    main()
