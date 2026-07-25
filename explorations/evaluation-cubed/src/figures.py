"""
Stage 7: figures. Every figure has one stated takeaway (see the caption in the paper).

Style: no seaborn, no gridlines fighting the data, colourblind-safe palette, and the
same judge ordering everywhere so the eye can track a judge across panels.
"""

from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")
FIGS = os.path.join(HERE, "..", "figures")

plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "figure.dpi": 200, "savefig.dpi": 200, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
})

C = {"quality": "#0F7B6C", "style": "#D4762A", "inter": "#B0A8A0",
     "gold": "#7C3AED", "free": "#0E7490", "oracle": "#111111", "rand": "#999999"}


def short(j: str) -> str:
    m, p = j.split("::")
    m = (m.replace("gpt-", "").replace("-nano", "n").replace("-mini", "m")
          .replace("4.1", "41").replace("4o", "4o").replace("5.4", "54"))
    return f"{m}/{p[:4]}"


def load():
    A = json.load(open(os.path.join(RESULTS, "analysis.json")))
    B = json.load(open(os.path.join(RESULTS, "bootstrap.json")))
    return A, B


def fig_decomposition(A, B, judges):
    """F2: where a judge's between-system variance actually comes from."""
    fig, ax = plt.subplots(figsize=(6.6, 2.5))
    q = np.array([A["decomposition"][j]["ss_quality"] for j in judges])
    s = np.array([A["decomposition"][j]["ss_style"] for j in judges])
    i = np.array([A["decomposition"][j]["ss_inter"] for j in judges])
    tot = q + s + i
    x = np.arange(len(judges))
    ax.bar(x, q / tot, color=C["quality"], label="quality (valid signal)")
    ax.bar(x, s / tot, bottom=q / tot, color=C["style"], label="style (pure bias)")
    ax.bar(x, i / tot, bottom=(q + s) / tot, color=C["inter"],
           label="quality$\\times$style (pure bias)")
    ax.set_xticks(x)
    ax.set_xticklabels([short(j) for j in judges], rotation=60, ha="right")
    ax.set_ylabel("share of between-system variance")
    ax.set_ylim(0, 1)
    ax.axhline(0.5, color="k", lw=0.5, ls=":")
    ax.legend(ncol=3, frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.28))
    fig.savefig(os.path.join(FIGS, "f2_decomposition.pdf"))
    plt.close(fig)


def fig_gap(A, judges):
    """F1: meta-benchmark accuracy against realised ranking fidelity."""
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.6))
    fid = {j: np.array(A["population_fidelity"][j]) for j in judges}
    pf = A["protocol_scores_full_grid"]
    x = np.array([pf[j]["P1_pair_acc"] for j in judges])

    ax = axes[0]
    y = np.array([fid[j].mean() for j in judges])
    lo = np.array([fid[j].min() for j in judges])
    hi = np.array([fid[j].max() for j in judges])
    ax.vlines(x, lo, hi, color="#BBBBBB", lw=1.2, zorder=1)
    ax.scatter(x, y, s=22, color=C["gold"], zorder=2)
    ax.axhline(0.5, color="k", lw=0.6, ls="--")
    ax.set_xlabel("meta-evaluation accuracy $P_1$ (pooled, gold labels)")
    ax.set_ylabel("system ranking accuracy")
    ax.set_title("(a) accuracy vs. fidelity\n(bars = range over 243 populations)")

    ax = axes[1]
    e2 = A["E2"]
    names = ["P1_pair_acc", "P2_item_rho", "P3_dev_sra",
             "P4a_style_spread", "P4c_sep_over_bias", "P4d_monotonicity"]
    lab = ["$P_1$ pair acc", "$P_2$ item $\\rho$", "$P_3$ dev SRA",
           "$P_4^a$ style spread", "$P_4^c$ sep/bias", "$P_4^d$ monotonicity"]
    xx = np.arange(len(names))
    ind = [e2[n]["rho_in_distribution"] for n in names]
    tra = [e2[n]["rho_transfer"] for n in names]
    cols = [C["gold"]] * 3 + [C["free"]] * 3
    ax.bar(xx - 0.2, ind, 0.38, color=cols, alpha=0.45, label="same population")
    ax.bar(xx + 0.2, tra, 0.38, color=cols, label="transfer to a new population")
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(xx)
    ax.set_xticklabels(lab, rotation=45, ha="right")
    ax.set_ylabel(r"$\rho$ with realised fidelity")
    ax.set_title("(b) does the protocol predict fidelity?")
    ax.legend(frameon=False, loc="lower left")
    fig.savefig(os.path.join(FIGS, "f1_gap.pdf"))
    plt.close(fig)


def fig_populations(A, judges):
    """F3: a judge's fidelity is not a number, it is a range."""
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    data = [np.array(A["population_fidelity"][j]) for j in judges]
    order = np.argsort([d.mean() for d in data])[::-1]
    data = [data[i] for i in order]
    js = [judges[i] for i in order]
    parts = ax.violinplot(data, showextrema=False, widths=0.85)
    for pc in parts["bodies"]:
        pc.set_facecolor(C["free"])
        pc.set_alpha(0.55)
        pc.set_edgecolor("none")
    for i, d in enumerate(data):
        ax.plot([i + 1], [d.mean()], marker="o", ms=3, color="k", zorder=3)
    ax.axhline(0.5, color="crimson", lw=0.8, ls="--")
    ax.text(len(data) + 0.4, 0.5, "chance", color="crimson", va="center", fontsize=6.5)
    ax.set_xticks(np.arange(1, len(js) + 1))
    ax.set_xticklabels([short(j) for j in js], rotation=60, ha="right")
    ax.set_ylabel("system ranking accuracy")
    ax.set_title("fidelity across the 243 populations with identical true ranking")
    fig.savefig(os.path.join(FIGS, "f3_populations.pdf"))
    plt.close(fig)


def fig_regret(A):
    """F4: the level-3 metric. Which protocol picks a judge that actually ranks well?"""
    e4 = A["E4"]
    keys = [k for k in e4 if k not in ("ORACLE", "random judge")]
    gold_dev = [k for k in keys if "@dev" in k]
    gold_tgt = [k for k in keys if "label oracle" in k]
    free = [k for k in keys if "label-free" in k]
    order = gold_dev + gold_tgt + free
    vals = [e4[k]["mean_regret"] for k in order]
    cols = ([C["gold"]] * len(gold_dev) + ["#B39DDB"] * len(gold_tgt)
            + [C["free"]] * len(free))
    fig, ax = plt.subplots(figsize=(6.6, 2.6))
    y = np.arange(len(order))
    ax.barh(y, vals, color=cols)
    ax.set_yticks(y)
    ax.set_yticklabels([k.replace("_", " ") for k in order], fontsize=6.5)
    ax.invert_yaxis()
    ax.axvline(e4["random judge"]["mean_regret"], color=C["rand"], ls="--", lw=1)
    ax.text(e4["random judge"]["mean_regret"], -0.8, " random judge",
            color=C["rand"], fontsize=6.5, va="bottom")
    ax.set_xlabel("mean judge-selection regret on the target population (lower is better)")
    for yi, v in zip(y, vals):
        ax.text(v + 0.002, yi, f"{v:.3f}", va="center", fontsize=6.5)
    fig.savefig(os.path.join(FIGS, "f4_regret.pdf"))
    plt.close(fig)


def fig_certificate(A, judges):
    """F5: the certificate trades coverage for soundness, and the soundness holds."""
    e5 = A["E5"]
    fig, ax = plt.subplots(figsize=(3.3, 2.6))
    cov = np.array([e5[j]["coverage"] for j in judges])
    cac = np.array([e5[j]["certified_acc"] for j in judges])
    raw = np.array([e5[j]["uncert_acc"] for j in judges])
    ax.scatter(cov, raw, s=20, color="#BBBBBB", label="all pairs (uncertified)")
    ax.scatter(cov, cac, s=22, color=C["free"], label="certified pairs only")
    for c, a, b in zip(cov, raw, cac):
        ax.plot([c, c], [a, b], color="#DDDDDD", lw=0.6, zorder=0)
    ax.axhline(1.0, color="k", lw=0.5, ls=":")
    ax.set_xlabel("coverage (fraction of pairs certified)")
    ax.set_ylabel("ranking accuracy")
    ax.legend(frameon=False, loc="lower right", fontsize=6.5)
    fig.savefig(os.path.join(FIGS, "f5_certificate.pdf"))
    plt.close(fig)


def main():
    os.makedirs(FIGS, exist_ok=True)
    A, B = load()
    judges = A["judges"]
    fig_decomposition(A, B, judges)
    fig_gap(A, judges)
    fig_populations(A, judges)
    fig_regret(A)
    fig_certificate(A, judges)
    print("wrote figures to", FIGS)
    for f in sorted(os.listdir(FIGS)):
        print("  ", f)


if __name__ == "__main__":
    main()
