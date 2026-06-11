"""E5 analysis. For each task TYPE (A reasoning-decoupled, B input-decoupled, C output
control), measure how well the PRE seconds-estimate tracks actual latency:
Spearman rho and geometric-mean ratio, per model and pooled. Also report the actual-latency
spread per type/model (was there variation to track?). Prediction: rho high in C, low in A/B.
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
TYPES = ["A", "B", "C"]
TYPE_LABEL = {"A": "A: reasoning-decoupled", "B": "B: input-decoupled",
              "C": "C: output-driven (control)"}


def gmean(xs):
    xs = [x for x in xs if x and x > 0]
    return float(np.exp(np.mean(np.log(xs)))) if xs else float("nan")


def load():
    rows = [json.loads(l) for l in open(RESULTS) if l.strip()]
    est, act, typ = {}, {}, {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "pre":
            est[k] = r["parsed_estimate_s"]
        elif r["condition"] == "gen":
            act[k] = r["latency_s"]
        typ[(r["model"], r["task_id"])] = r["type"]
    recs = []
    for k, a in act.items():
        e = est.get(k)
        recs.append(dict(model=k[0], task_id=k[1], trial=k[2],
                         type=typ[(k[0], k[1])], est=e, actual=a))
    return recs


def stats_for(recs):
    pairs = [(r["actual"], r["est"]) for r in recs if r["est"] and r["actual"]]
    if len(pairs) < 3:
        return None
    a = [p[0] for p in pairs]
    e = [p[1] for p in pairs]
    rho, p = spearmanr(a, e)
    ratio = gmean([ei / ai for ai, ei in pairs])
    lat_spread = max(a) / min(a) if min(a) > 0 else float("nan")
    return dict(n=len(pairs), rho=rho, p=p, ratio=ratio, lat_spread=lat_spread)


def main():
    recs = load()
    models = sorted(set(r["model"] for r in recs))
    print(f"Loaded {len(recs)} (model,task,trial) units; models={models}\n")

    # Per type: pooled + per model
    print("=" * 78)
    print(f"{'type':<28}{'scope':<12}{'rho':>7}{'p':>8}{'gm(est/act)':>13}"
          f"{'lat_spread':>12}{'n':>5}")
    print("-" * 78)
    rho_by_type_model = defaultdict(dict)
    for t in TYPES:
        tr = [r for r in recs if r["type"] == t]
        s = stats_for(tr)
        if s:
            print(f"{TYPE_LABEL[t]:<28}{'POOLED':<12}{s['rho']:>7.3f}{s['p']:>8.3f}"
                  f"{s['ratio']:>13.2f}{s['lat_spread']:>12.1f}{s['n']:>5}")
        for m in models:
            mr = [r for r in tr if r["model"] == m]
            sm = stats_for(mr)
            if sm:
                rho_by_type_model[t][m] = sm["rho"]
                print(f"{'':<28}{m:<12}{sm['rho']:>7.3f}{sm['p']:>8.3f}"
                      f"{sm['ratio']:>13.2f}{sm['lat_spread']:>12.1f}{sm['n']:>5}")
        print("-" * 78)

    # Headline
    print("\nHEADLINE: pooled rho by type (prediction: C high, A & B low)")
    for t in TYPES:
        s = stats_for([r for r in recs if r["type"] == t])
        if s:
            print(f"  {TYPE_LABEL[t]:<30} rho={s['rho']:.3f}  gm={s['ratio']:.2f}  "
                  f"actual-latency spread {s['lat_spread']:.1f}x")

    # Figure 1: rho by type x model
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(TYPES))
    w = 0.8 / max(1, len(models))
    for i, m in enumerate(models):
        vals = [rho_by_type_model[t].get(m, np.nan) for t in TYPES]
        ax.bar(x + i * w, vals, w, label=m)
    ax.set_xticks(x + 0.4 - w / 2)
    ax.set_xticklabels([TYPE_LABEL[t] for t in TYPES], fontsize=8)
    ax.set_ylabel("Spearman rho(estimate, actual latency)")
    ax.set_title("E5: self-estimate vs actual latency, by task type")
    ax.axhline(0, color="k", lw=0.5)
    ax.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "rho_by_type.png"), dpi=110)
    print("\nwrote rho_by_type.png")

    # Figure 2: scatter est vs actual, colored by type
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    for ax, t in zip(axes, TYPES):
        tr = [r for r in recs if r["type"] == t and r["est"] and r["actual"]]
        ax.scatter([r["actual"] for r in tr], [r["est"] for r in tr], s=14, alpha=0.6)
        ax.set_xscale("log"); ax.set_yscale("log")
        lim = [0.3, 60]
        ax.plot(lim, lim, "k--", lw=0.6)
        ax.set_title(TYPE_LABEL[t], fontsize=9)
        ax.set_xlabel("actual latency (s)")
    axes[0].set_ylabel("estimated latency (s)")
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "scatter_by_type.png"), dpi=110)
    print("wrote scatter_by_type.png")


if __name__ == "__main__":
    main()
