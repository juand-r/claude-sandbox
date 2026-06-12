"""Raw-data views for the report: per-run scatter plots (one dot per trial, faceted by model)
and per-task raw-number tables (LaTeX fragments). Complements the aggregate tables/figures by
showing the underlying runs. The complete per-trial data is in each results.jsonl; this script
derives both the figures and the per-task summary tables from those files.

Outputs:
  e{2,5,6,10}-*/scatter_perrun.png          per-run predicted-vs-actual facets
  raw_tables/e{1,2,5,6,10}_pertask.tex       per-task LaTeX longtable fragments

Run: python raw_views.py
"""
import json
import os
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "raw_tables")
os.makedirs(OUT, exist_ok=True)

MODEL_ORDER = ["haiku", "sonnet", "opus", "gpt4o-mini", "gpt4o", "gpt5.2", "gpt5", "o4-mini"]


def load(exp):
    return [json.loads(l) for l in open(os.path.join(HERE, exp, "results.jsonl")) if l.strip()]


def gm(rs):
    rs = [x for x in rs if x and x > 0]
    return float(np.exp(np.mean(np.log(rs)))) if rs else float("nan")


def order_models(ms):
    return [m for m in MODEL_ORDER if m in ms] + [m for m in ms if m not in MODEL_ORDER]


# ---------- per-run scatter facets ------------------------------------------
def scatter_facets(exp, points_by_model, xlabel, ylabel, title, lim, fname):
    """points_by_model: model -> list of (actual, predicted) at the TRIAL level."""
    models = order_models(list(points_by_model))
    ncol = min(3, len(models))
    nrow = int(np.ceil(len(models) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 3.7 * nrow),
                             squeeze=False, sharex=True, sharey=True)
    for ax in axes.flat:
        ax.set_visible(False)
    for ax, m in zip(axes.flat, models):
        ax.set_visible(True)
        pts = [(a, p) for a, p in points_by_model[m] if a and p and a > 0 and p > 0]
        a = np.array([x[0] for x in pts]); p = np.array([x[1] for x in pts])
        ax.scatter(a, p, s=24, alpha=0.6, edgecolor="none")
        ax.plot(lim, lim, "k--", lw=0.8)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlim(lim); ax.set_ylim(lim)
        ax.set_title(f"{m}  (gm {gm(list(p / a)):.2f}, n={len(pts)})", fontsize=10)
        ax.grid(True, which="major", ls=":", lw=0.4, alpha=0.5)
    for ax in axes[-1, :]:
        if ax.get_visible():
            ax.set_xlabel(xlabel)
    for ax in axes[:, 0]:
        ax.set_ylabel(ylabel)
    fig.suptitle(title, fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    path = os.path.join(HERE, exp, fname)
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print("wrote", path)


def e2_scatter():
    rows = load("e2-token-time")
    act, est = {}, {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            act[k] = r["output_tokens"]
        elif r["condition"] == "cond_tokens":
            est[k] = r.get("parsed_estimate")
    bym = defaultdict(list)
    for k in act:
        if k in est:
            bym[k[0]].append((act[k], est[k]))
    scatter_facets("e2-token-time", bym, "actual output tokens", "predicted tokens",
                   "E2: predicted vs. actual output tokens per run (token condition)",
                   [1, 2000], "scatter_perrun.png")


def e5_scatter():
    rows = load("e5-latency-decoupled")
    act, pre, typ = {}, {}, {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            act[k] = r["latency_s"]
        elif r["condition"] == "pre":
            pre[k] = r["parsed_estimate_s"]
        typ[(r["model"], r["task_id"])] = r["type"]
    # facet by model, color by type
    models = order_models(list({k[0] for k in act}))
    types = ["A", "B", "C"]; colors = {"A": "tab:red", "B": "tab:orange", "C": "tab:green"}
    ncol = min(3, len(models)); nrow = int(np.ceil(len(models) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 3.7 * nrow),
                             squeeze=False, sharex=True, sharey=True)
    for ax in axes.flat:
        ax.set_visible(False)
    for ax, m in zip(axes.flat, models):
        ax.set_visible(True)
        for t in types:
            pts = [(act[k], pre[k]) for k in act
                   if k[0] == m and k in pre and pre[k] and act[k] and typ[(k[0], k[1])] == t]
            if pts:
                ax.scatter([x[0] for x in pts], [x[1] for x in pts], s=24, alpha=0.6,
                           color=colors[t], label=f"type {t}", edgecolor="none")
        ax.plot([0.3, 60], [0.3, 60], "k--", lw=0.8)
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim([0.3, 60]); ax.set_ylim([0.3, 60])
        ax.set_title(m, fontsize=10); ax.grid(True, ls=":", lw=0.4, alpha=0.5)
        ax.legend(fontsize=7, loc="upper left")
    for ax in axes[-1, :]:
        if ax.get_visible():
            ax.set_xlabel("actual latency (s)")
    for ax in axes[:, 0]:
        ax.set_ylabel("predicted latency (s)")
    fig.suptitle("E5: predicted vs. actual latency per run, by model and task type", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    p = os.path.join(HERE, "e5-latency-decoupled", "scatter_perrun.png")
    fig.savefig(p, dpi=120); plt.close(fig); print("wrote", p)


def e6_scatter():
    rows = load("e6-length-bias")
    act, est = {}, defaultdict(dict)
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            act[k] = r["actual_output_tokens"]
        else:
            est[k][r["condition"]] = r["parsed_estimate_tok"]
    # facet by condition, color by model
    conds = ["bare", "anchors", "self_revise"]
    models = order_models(list({k[0] for k in act}))
    cmap = plt.cm.tab10(np.linspace(0, 1, len(models)))
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.3), sharex=True, sharey=True)
    for ax, c in zip(axes, conds):
        for mi, m in enumerate(models):
            pts = [(act[k], est[k][c]) for k in act
                   if k[0] == m and c in est.get(k, {}) and est[k][c] and act[k]]
            if pts:
                ax.scatter([x[0] for x in pts], [x[1] for x in pts], s=20, alpha=0.6,
                           color=cmap[mi], label=m, edgecolor="none")
        ax.plot([1, 1500], [1, 1500], "k--", lw=0.8)
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim([1, 1500]); ax.set_ylim([1, 1500])
        ax.set_title(c, fontsize=11); ax.set_xlabel("actual output tokens")
        ax.grid(True, ls=":", lw=0.4, alpha=0.5)
    axes[0].set_ylabel("predicted tokens")
    axes[-1].legend(fontsize=7, loc="lower right")
    fig.suptitle("E6: predicted vs. actual output tokens per run, by condition", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    p = os.path.join(HERE, "e6-length-bias", "scatter_perrun.png")
    fig.savefig(p, dpi=120); plt.close(fig); print("wrote", p)


def e10_scatter():
    rows = load("e10-reasoning-tokens")
    act, est = {}, {}
    for r in rows:
        k = (r["model"], r["task_id"], r["trial"])
        if r["condition"] == "gen":
            act[k] = r["reasoning_tokens"]
        elif r["condition"] == "pre_tokens":
            est[k] = r["parsed_estimate"]
    bym = defaultdict(list)
    for k in act:
        if k in est:
            bym[k[0]].append((max(act[k], 1), est[k]))  # clamp 0 -> 1 for log axis
    scatter_facets("e10-reasoning-tokens", bym, "actual reasoning tokens (0 shown as 1)",
                   "predicted reasoning tokens",
                   "E10: predicted vs. actual reasoning tokens per run",
                   [1, 200000], "scatter_perrun.png")


# ---------- per-task raw-number tables (LaTeX longtable fragments) ----------
def write_table(fname, header, rows, caption, label):
    cols = "@{}l" + "r" * (len(header) - 1) + "@{}"
    lines = [f"\\begin{{longtable}}{{{cols}}}",
             f"\\caption{{{caption}}}\\label{{{label}}}\\\\",
             "\\toprule",
             " & ".join(header) + " \\\\", "\\midrule", "\\endfirsthead",
             "\\toprule", " & ".join(header) + " \\\\", "\\midrule", "\\endhead"]
    for r in rows:
        lines.append(" & ".join(str(x) for x in r) + " \\\\")
    lines += ["\\bottomrule", "\\end{longtable}"]
    with open(os.path.join(OUT, fname), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("wrote", os.path.join(OUT, fname))


def tex_id(s):
    return "\\code{" + s.replace("_", "\\_") + "}"


def e1_table():
    rows = load("e1-self-duration")
    act, pre = defaultdict(list), defaultdict(list)
    for r in rows:
        k = (r["model"], r["task_id"])
        if r["condition"] == "task":
            act[k].append(r["latency_s"])
        elif r["condition"] == "pre":
            pre[k].append(r["parsed_estimate_s"])
    tasks = sorted({k[1] for k in act})
    models = order_models(list({k[0] for k in act}))
    out = []
    for t in tasks:
        meanact = np.mean([np.mean(act[(m, t)]) for m in models if act[(m, t)]])
        row = [tex_id(t), f"{meanact:.1f}"]
        for m in models:
            e = pre[(m, t)]
            row.append(f"{np.mean(e):.0f}" if e else "--")
        out.append(row)
    header = ["task", "actual\\,(s)"] + [m.replace("gpt", "g").replace("-mini", "m")
                                         for m in models]
    write_table("e1_pertask.tex", header, out,
                "E1 per-task raw numbers: mean actual latency (s), pooled over models, and the "
                "mean pre-estimate (s) for each model (each averaged over 3 trials). Full "
                "per-trial data is in \\code{e1-self-duration/results.jsonl}.", "tab:e1raw")


def e10_table():
    rows = load("e10-reasoning-tokens")
    act, tok, eff = defaultdict(list), defaultdict(list), defaultdict(list)
    for r in rows:
        k = (r["model"], r["task_id"])
        if r["condition"] == "gen":
            act[k].append(r["reasoning_tokens"])
        elif r["condition"] == "pre_tokens" and r["parsed_estimate"] is not None:
            tok[k].append(r["parsed_estimate"])
        elif r["condition"] == "pre_effort" and r["parsed_estimate"] is not None:
            eff[k].append(r["parsed_estimate"])
    tasks = sorted({k[1] for k in act}, key=lambda t: np.mean(act[("o4-mini", t)] or [0]))
    out = []
    for t in tasks:
        for m in ["o4-mini", "gpt5", "fable"]:
            a = np.mean(act[(m, t)]) if act[(m, t)] else float("nan")
            tk = f"{np.mean(tok[(m, t)]):.0f}" if tok[(m, t)] else "--"
            ef = f"{np.mean(eff[(m, t)]):.1f}" if eff[(m, t)] else "--"
            out.append([tex_id(t), m, f"{a:.0f}", tk, ef])
    write_table("e10_pertask.tex",
                ["task", "model", "actual reas.", "tok.\\,est", "effort"], out,
                "E10 per-task raw numbers: mean actual reasoning tokens, mean reasoning-token "
                "estimate, and mean 1--10 effort rating, each averaged over 3 trials. A `--' "
                "for the token estimate means the model gave no parseable number.", "tab:e10raw")


if __name__ == "__main__":
    e2_scatter(); e5_scatter(); e6_scatter(); e10_scatter()
    e1_table(); e10_table()
