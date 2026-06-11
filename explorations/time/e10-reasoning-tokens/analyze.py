"""E10 analysis. Can a reasoning model predict its OWN reasoning length?

Per (model, task): mean over trials of the pre-solve token estimate, the 1-10 effort rating,
and the ACTUAL reasoning_tokens used on the solve. Report, per model and pooled:
  rho(token_estimate, actual_reasoning)   -- does the predicted count track reality?
  rho(effort_rating,  actual_reasoning)   -- does even an ordinal effort sense track it?
  ordering accuracy                        -- task-pair ordering vs actual reasoning order
  gm(token_estimate / actual)              -- bias (actual>0 only)
Prediction: rho ~ 0 (the recurring boundary) -- the model is blind to its own reasoning cost.
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


def gmean(xs):
    xs = [x for x in xs if x and x > 0]
    return float(np.exp(np.mean(np.log(xs)))) if xs else float("nan")


def load():
    rows = [json.loads(l) for l in open(RESULTS) if l.strip()]
    tok, eff, act = defaultdict(list), defaultdict(list), defaultdict(list)
    for r in rows:
        k = (r["model"], r["task_id"])
        if r["condition"] == "pre_tokens" and r["parsed_estimate"] is not None:
            tok[k].append(r["parsed_estimate"])
        elif r["condition"] == "pre_effort" and r["parsed_estimate"] is not None:
            eff[k].append(r["parsed_estimate"])
        elif r["condition"] == "gen":
            act[k].append(r["reasoning_tokens"])
    recs = []
    for k in act:
        recs.append(dict(model=k[0], task=k[1],
                         tok=np.mean(tok[k]) if tok[k] else None,
                         eff=np.mean(eff[k]) if eff[k] else None,
                         act=np.mean(act[k])))
    return recs


def ordering_acc(points):
    """points: list of (predicted, actual). Fraction of pairs ordered correctly (ties skip)."""
    n = len(points); ok = tot = 0
    for i in range(n):
        for j in range(i + 1, n):
            da = points[i][1] - points[j][1]; dp = points[i][0] - points[j][0]
            if da == 0 or dp == 0:
                continue
            tot += 1; ok += (da > 0) == (dp > 0)
    return ok / tot if tot else float("nan")


def stats(recs, key):
    P = [(r[key], r["act"]) for r in recs if r[key] is not None]
    if len(P) < 3:
        return None
    a = [x[1] for x in P]; p = [x[0] for x in P]
    rho = spearmanr(a, p)[0] if len(set(p)) > 1 else float("nan")
    return dict(n=len(P), rho=rho, order=ordering_acc(P),
                gm=gmean([pe / ac for pe, ac in P if ac > 0]),
                act_spread=(max(a) / min(a) if min(a) > 0 else float("inf")))


def main():
    recs = load()
    models = sorted(set(r["model"] for r in recs))
    print(f"Loaded {len(recs)} (model,task) units; models={models}\n")

    print("=" * 74)
    print(f"{'model':<10}{'predictor':<14}{'rho':>8}{'order_acc':>11}{'gm(est/act)':>13}"
          f"{'n':>5}")
    print("-" * 74)
    for m in models + ["POOLED"]:
        mr = recs if m == "POOLED" else [r for r in recs if r["model"] == m]
        for key, label in [("tok", "token_est"), ("eff", "effort_1-10")]:
            s = stats(mr, key)
            if s:
                print(f"{m:<10}{label:<14}{s['rho']:>8.3f}{s['order']:>11.3f}"
                      f"{s['gm']:>13.2f}{s['n']:>5}")
        print("-" * 74)

    # actual reasoning-token spread, to show there is a real gradient to predict
    print("\nActual reasoning_tokens range (the thing being predicted):")
    for m in models:
        acts = sorted(r["act"] for r in recs if r["model"] == m)
        print(f"  {m:<10} min={acts[0]:.0f} max={acts[-1]:.0f} "
              f"({acts[-1] / max(acts[0], 1):.0f}x spread)")

    # Figure: token estimate vs actual reasoning (log-log), per model
    fig, axes = plt.subplots(1, len(models), figsize=(5.5 * len(models), 4.3), squeeze=False)
    for ax, m in zip(axes[0], models):
        mr = [r for r in recs if r["model"] == m and r["tok"] is not None]
        ax.scatter([max(r["act"], 1) for r in mr], [r["tok"] for r in mr], s=28, alpha=0.7)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.plot([1, 10000], [1, 10000], "k--", lw=0.6, label="perfect")
        ax.set_title(f"{m}: token estimate vs actual reasoning")
        ax.set_xlabel("actual reasoning_tokens"); ax.set_ylabel("estimated reasoning tokens")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "estimate_vs_actual.png"), dpi=110)
    print("\nwrote estimate_vs_actual.png")


if __name__ == "__main__":
    main()
