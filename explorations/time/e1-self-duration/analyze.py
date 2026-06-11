"""E1 analysis. Reads results.jsonl ONLY — never calls the API.

Metrics:
  - estimate/actual ratio (geometric mean per model + overall), PRE and POST
  - Spearman rho(estimate, actual) per model and overall
  - ordering accuracy on task pairs (does predicted order match actual latency order)
  - PRE vs POST divergence
Figures (PNG):
  - scatter estimate vs actual on log-log (PRE), colored by model
  - bar of geometric-mean ratios per model (PRE and POST)
  - latency-noise distribution per task (CV) to document wall-clock noise
"""

import json
import os
from collections import defaultdict
from itertools import combinations

import numpy as np
from scipy.stats import spearmanr

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

PRICES = {  # per 1M tokens (input, output), approximate 2026
    "haiku": (1, 5), "sonnet": (3, 15), "opus": (15, 75),
    "gpt4o-mini": (0.15, 0.6), "gpt4o": (2.5, 10),
    "gpt5": (1.25, 10), "gpt5.2": (1.25, 10), "o4-mini": (1.1, 4.4),
}


def load():
    rows = []
    with open(RESULTS) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def gmean(xs):
    xs = [x for x in xs if x is not None and x > 0]
    if not xs:
        return float("nan")
    return float(np.exp(np.mean(np.log(xs))))


def build_records(rows):
    """Per (model,task,trial): actual latency from 'task', pre & post estimates."""
    actual = {}   # (model,task,trial) -> latency_s, output_tokens
    pre = {}      # (model,task,trial) -> estimate
    post = {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "task":
            actual[k] = (r["latency_s"], r["output_tokens"])
        elif r["condition"] == "pre":
            pre[k] = r["parsed_estimate_s"]
        elif r["condition"] == "post":
            post[k] = r["parsed_estimate_s"]
    recs = []
    for k, (lat, otok) in actual.items():
        recs.append({
            "model": k[0], "task_id": k[1], "trial": k[2],
            "actual_s": lat, "output_tokens": otok,
            "pre_s": pre.get(k), "post_s": post.get(k),
        })
    return recs


def ordering_accuracy(pairs_actual, pairs_est):
    """Given dict task->mean_value for actual and estimate, fraction of task pairs
    whose estimated order matches actual order (ties excluded)."""
    tasks = sorted(set(pairs_actual) & set(pairs_est))
    correct = total = 0
    for a, b in combinations(tasks, 2):
        da = pairs_actual[a] - pairs_actual[b]
        de = pairs_est[a] - pairs_est[b]
        if da == 0 or de == 0:
            continue
        total += 1
        if (da > 0) == (de > 0):
            correct += 1
    return (correct / total if total else float("nan")), total


def main():
    rows = load()
    recs = build_records(rows)
    models = sorted({r["model"] for r in recs})

    print(f"Loaded {len(rows)} raw calls; {len(recs)} (model,task,trial) units.\n")

    # ---- Ratios & Spearman per model ----
    print("=" * 78)
    print(f"{'model':<11} {'n':>3} {'gm_ratio_PRE':>13} {'gm_ratio_POST':>14} "
          f"{'rho_PRE':>9} {'p_PRE':>8} {'rho_POST':>9}")
    print("-" * 78)
    summary = {}
    all_pre_pairs = []   # (actual, est) for global scatter/spearman
    for m in models:
        mr = [r for r in recs if r["model"] == m]
        pre_ratio = gmean([r["pre_s"] / r["actual_s"] for r in mr
                           if r["pre_s"] and r["actual_s"]])
        post_ratio = gmean([r["post_s"] / r["actual_s"] for r in mr
                            if r["post_s"] and r["actual_s"]])
        pre_pairs = [(r["actual_s"], r["pre_s"]) for r in mr
                     if r["pre_s"] and r["actual_s"]]
        post_pairs = [(r["actual_s"], r["post_s"]) for r in mr
                      if r["post_s"] and r["actual_s"]]
        all_pre_pairs += pre_pairs
        if len(pre_pairs) >= 3:
            rho_pre, p_pre = spearmanr([a for a, _ in pre_pairs],
                                       [e for _, e in pre_pairs])
        else:
            rho_pre, p_pre = float("nan"), float("nan")
        if len(post_pairs) >= 3:
            rho_post, _ = spearmanr([a for a, _ in post_pairs],
                                    [e for _, e in post_pairs])
        else:
            rho_post = float("nan")
        summary[m] = dict(n=len(mr), pre_ratio=pre_ratio, post_ratio=post_ratio,
                          rho_pre=rho_pre, p_pre=p_pre, rho_post=rho_post)
        print(f"{m:<11} {len(mr):>3} {pre_ratio:>13.2f} {post_ratio:>14.2f} "
              f"{rho_pre:>9.3f} {p_pre:>8.3f} {rho_post:>9.3f}")

    # ---- Overall ----
    overall_pre = gmean([r["pre_s"] / r["actual_s"] for r in recs
                         if r["pre_s"] and r["actual_s"]])
    overall_post = gmean([r["post_s"] / r["actual_s"] for r in recs
                          if r["post_s"] and r["actual_s"]])
    if len(all_pre_pairs) >= 3:
        rho_all, p_all = spearmanr([a for a, _ in all_pre_pairs],
                                   [e for _, e in all_pre_pairs])
    else:
        rho_all, p_all = float("nan"), float("nan")
    print("-" * 78)
    print(f"{'OVERALL':<11} {len(recs):>3} {overall_pre:>13.2f} {overall_post:>14.2f} "
          f"{rho_all:>9.3f} {p_all:>8.3f}")
    print("=" * 78)

    # ---- Ordering accuracy per model (mean over trials) ----
    print("\nOrdering accuracy (predicted task order vs actual latency order):")
    ord_results = {}
    for m in models:
        mr = [r for r in recs if r["model"] == m]
        act_mean, pre_mean = defaultdict(list), defaultdict(list)
        for r in mr:
            if r["actual_s"]:
                act_mean[r["task_id"]].append(r["actual_s"])
            if r["pre_s"]:
                pre_mean[r["task_id"]].append(r["pre_s"])
        act_m = {t: np.mean(v) for t, v in act_mean.items()}
        pre_m = {t: np.mean(v) for t, v in pre_mean.items()}
        acc, npair = ordering_accuracy(act_m, pre_m)
        ord_results[m] = (acc, npair)
        print(f"  {m:<11} {acc:.3f}  ({npair} pairs)")

    # ---- PRE vs POST divergence ----
    print("\nPRE vs POST divergence (geometric mean of pre/post per model):")
    for m in models:
        mr = [r for r in recs if r["model"] == m]
        div = gmean([r["pre_s"] / r["post_s"] for r in mr
                     if r["pre_s"] and r["post_s"]])
        print(f"  {m:<11} pre/post gmean = {div:.2f}")

    # ---- Wall-clock noise: CV of actual latency per (model,task) ----
    print("\nWall-clock noise (median CV of actual latency across trials, per model):")
    noise = {}
    for m in models:
        cvs = []
        bytask = defaultdict(list)
        for r in recs:
            if r["model"] == m and r["actual_s"]:
                bytask[r["task_id"]].append(r["actual_s"])
        for t, v in bytask.items():
            if len(v) >= 2 and np.mean(v) > 0:
                cvs.append(np.std(v) / np.mean(v))
        med_cv = float(np.median(cvs)) if cvs else float("nan")
        noise[m] = med_cv
        print(f"  {m:<11} median CV = {med_cv:.3f}  (n_tasks={len(cvs)})")

    # ---- Spend estimate ----
    print("\n" + "=" * 50)
    print("SPEND ESTIMATE (approximate 2026 prices)")
    tok = defaultdict(lambda: [0, 0])
    for r in rows:
        tok[r["model"]][0] += r.get("input_tokens", 0) or 0
        tok[r["model"]][1] += r.get("output_tokens", 0) or 0
    total_anthropic = total_openai = 0.0
    anthropic_models = {"haiku", "sonnet", "opus"}
    for m in sorted(tok):
        intok, outtok = tok[m]
        pin, pout = PRICES[m]
        cost = intok / 1e6 * pin + outtok / 1e6 * pout
        if m in anthropic_models:
            total_anthropic += cost
        else:
            total_openai += cost
        print(f"  {m:<11} in={intok:>7} out={outtok:>7}  ${cost:.4f}")
    print(f"  {'-'*40}")
    print(f"  Anthropic total: ${total_anthropic:.3f}")
    print(f"  OpenAI total:    ${total_openai:.3f}")
    print(f"  GRAND TOTAL:     ${total_anthropic + total_openai:.3f}")
    print("=" * 50)

    make_figures(recs, models, summary, ord_results, noise)
    print("\nFigures written: fig_scatter.png, fig_ratios.png, fig_noise.png")


def make_figures(recs, models, summary, ord_results, noise):
    cmap = plt.get_cmap("tab10")
    color = {m: cmap(i % 10) for i, m in enumerate(models)}

    # Fig 1: scatter estimate vs actual (log-log), PRE
    plt.figure(figsize=(7, 6))
    for m in models:
        xs = [r["actual_s"] for r in recs if r["model"] == m and r["pre_s"] and r["actual_s"]]
        ys = [r["pre_s"] for r in recs if r["model"] == m and r["pre_s"] and r["actual_s"]]
        plt.scatter(xs, ys, s=28, alpha=0.6, color=color[m], label=m)
    lo, hi = 0.05, 200
    plt.plot([lo, hi], [lo, hi], "k--", lw=1, label="perfect (y=x)")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("actual latency (s)"); plt.ylabel("PRE estimate (s)")
    plt.title("E1: PRE self-duration estimate vs actual latency")
    plt.legend(fontsize=8); plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout(); plt.savefig(os.path.join(HERE, "fig_scatter.png"), dpi=130)
    plt.close()

    # Fig 2: bar of geometric-mean ratios per model (PRE & POST)
    plt.figure(figsize=(8, 5))
    x = np.arange(len(models)); w = 0.38
    pre_r = [summary[m]["pre_ratio"] for m in models]
    post_r = [summary[m]["post_ratio"] for m in models]
    plt.bar(x - w / 2, pre_r, w, label="PRE", color="#4477aa")
    plt.bar(x + w / 2, post_r, w, label="POST", color="#cc6677")
    plt.axhline(1.0, color="k", ls="--", lw=1, label="calibrated (ratio=1)")
    plt.yscale("log")
    plt.xticks(x, models, rotation=30, ha="right")
    plt.ylabel("geometric-mean estimate/actual ratio")
    plt.title("E1: overestimation factor per model (>1 = overshoot)")
    plt.legend(); plt.grid(True, axis="y", which="both", alpha=0.3)
    plt.tight_layout(); plt.savefig(os.path.join(HERE, "fig_ratios.png"), dpi=130)
    plt.close()

    # Fig 3: wall-clock noise (median CV per model)
    plt.figure(figsize=(7, 4.5))
    ms = list(noise.keys())
    plt.bar(range(len(ms)), [noise[m] for m in ms], color="#999933")
    plt.xticks(range(len(ms)), ms, rotation=30, ha="right")
    plt.ylabel("median CV of actual latency (across trials)")
    plt.title("E1 threat-to-validity: wall-clock noise per model")
    plt.grid(True, axis="y", alpha=0.3)
    plt.tight_layout(); plt.savefig(os.path.join(HERE, "fig_noise.png"), dpi=130)
    plt.close()


if __name__ == "__main__":
    main()
