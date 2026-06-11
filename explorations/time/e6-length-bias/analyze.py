"""E6 analysis. For each estimate condition (bare / anchors / self_revise), measure
calibration of predicted OUTPUT TOKENS vs same-trial actual: geometric-mean ratio
(pred/actual; 1.0 = perfect, <1 = undershoot) and Spearman rho. Headline: does an
in-context intervention move the gm ratio toward 1.0 from the bare ~2x undershoot?
"""
import json
import os
from collections import defaultdict

import numpy as np
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")
CONDS = ["bare", "anchors", "self_revise"]


def gmean(xs):
    xs = [x for x in xs if x and x > 0]
    return float(np.exp(np.mean(np.log(xs)))) if xs else float("nan")


def load():
    rows = [json.loads(l) for l in open(RESULTS) if l.strip()]
    actual = {}
    est = defaultdict(dict)  # (model,task,trial) -> {cond: estimate}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            actual[k] = r["actual_output_tokens"]
        else:
            est[k][r["condition"]] = r["parsed_estimate_tok"]
    recs = []
    for k, a in actual.items():
        recs.append(dict(model=k[0], task_id=k[1], trial=k[2], actual=a, **est.get(k, {})))
    return recs


def cond_stats(recs, cond):
    pairs = [(r["actual"], r.get(cond)) for r in recs
             if r.get(cond) and r["actual"]]
    if len(pairs) < 3:
        return None
    a = [p[0] for p in pairs]
    e = [p[1] for p in pairs]
    rho, _ = spearmanr(a, e)
    return dict(n=len(pairs), rho=rho, ratio=gmean([ei / ai for ai, ei in pairs]))


def main():
    recs = load()
    models = sorted(set(r["model"] for r in recs))
    print(f"Loaded {len(recs)} (model,task,trial) units; models={models}\n")

    print("=" * 70)
    print(f"{'condition':<14}{'scope':<12}{'gm(pred/act)':>13}{'rho':>8}{'n':>6}")
    print("-" * 70)
    ratio_by_cond_model = defaultdict(dict)
    for c in CONDS:
        s = cond_stats(recs, c)
        if s:
            print(f"{c:<14}{'POOLED':<12}{s['ratio']:>13.2f}{s['rho']:>8.3f}{s['n']:>6}")
        for m in models:
            sm = cond_stats([r for r in recs if r["model"] == m], c)
            if sm:
                ratio_by_cond_model[c][m] = sm["ratio"]
                print(f"{'':<14}{m:<12}{sm['ratio']:>13.2f}{sm['rho']:>8.3f}{sm['n']:>6}")
        print("-" * 70)

    print("\nHEADLINE (pooled gm ratio; 1.0 = calibrated, <1 = undershoot):")
    base = cond_stats(recs, "bare")
    for c in CONDS:
        s = cond_stats(recs, c)
        if s:
            d = "" if c == "bare" else f"  (vs bare: {s['ratio'] - base['ratio']:+.2f})"
            print(f"  {c:<12} gm={s['ratio']:.2f}  rho={s['rho']:.3f}{d}")

    # Figure: gm ratio by condition x model
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(CONDS))
    w = 0.8 / max(1, len(models))
    for i, m in enumerate(models):
        vals = [ratio_by_cond_model[c].get(m, np.nan) for c in CONDS]
        ax.bar(x + i * w, vals, w, label=m)
    ax.axhline(1.0, color="k", lw=1, ls="--", label="calibrated")
    ax.set_xticks(x + 0.4 - w / 2)
    ax.set_xticklabels(CONDS)
    ax.set_ylabel("gm(predicted / actual output tokens)")
    ax.set_title("E6: length-estimate calibration by condition (1.0 = perfect)")
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "ratio_by_condition.png"), dpi=110)
    print("\nwrote ratio_by_condition.png")


if __name__ == "__main__":
    main()
