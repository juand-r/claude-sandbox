"""
Stage 7: figures. Each figure makes exactly one point, stated in its caption.

F1  resolution limits span ~60x across judges, and meta-evaluation accuracy compresses
    that range into ~20 accuracy points
F2  fidelity as a function of the true quality gap, under matched / random / adversarial
    style assignment -- the shape that defines a resolution limit
F3  calibration: the label-free predictor recovers the limit; gold-label accuracy does not
F4  the certificate in the leaderboard regime
F5  where a judge's between-system variance comes from (ANOVA decomposition)
"""

from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")
FIGS = os.path.join(HERE, "..", "figures")

plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8.5,
    "xtick.labelsize": 6.5, "ytick.labelsize": 7, "legend.fontsize": 6.8,
    "figure.dpi": 200, "savefig.dpi": 200, "savefig.bbox": "tight",
    "axes.spines.top": False, "axes.spines.right": False,
    "font.family": "serif", "font.serif": ["DejaVu Serif"], "mathtext.fontset": "dejavuserif",
})

CQ, CS, CI_ = "#0F7B6C", "#D4762A", "#B0A8A0"
CGOLD, CFREE = "#7C3AED", "#0E7490"
FAMCOL = {"5.4": "#0F7B6C", "5-": "#0E7490", "4.1": "#D4762A", "4o": "#A03030"}


def fam(j):
    m = j.split("::")[0]
    if "5.4" in m:
        return "5.4"
    if m.startswith("gpt-5"):
        return "5-"
    if "4o" in m:
        return "4o"
    return "4.1"


def short(j):
    m, p = j.split("::")
    m = m.replace("gpt-", "").replace("-nano", "-n").replace("-mini", "-m")
    return f"{m}/{p[:4]}"


def load():
    R = json.load(open(os.path.join(RESULTS, "resolution.json")))
    C = json.load(open(os.path.join(RESULTS, "composition.json")))
    E = json.load(open(os.path.join(RESULTS, "certificate_eval.json")))
    A = json.load(open(os.path.join(RESULTS, "analysis.json")))
    return R, C, E, A


def f1_limits(R, C):
    judges = R["judges"]
    lim = np.array([R["per_judge"][j]["observed_resolution_limit"] for j in judges])
    acc = np.array([C["compositions"]["full"]["accuracy"][j] for j in judges])
    o = np.argsort(lim)
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.9),
                             gridspec_kw={"width_ratios": [1.55, 1]})
    ax = axes[0]
    y = np.arange(len(o))
    ax.barh(y, lim[o] * 100, color=[FAMCOL[fam(judges[i])] for i in o], height=0.72)
    ax.set_yticks(y)
    ax.set_yticklabels([short(judges[i]) for i in o], fontsize=5.6)
    ax.invert_yaxis()
    ax.set_xlabel("measured resolution limit $L_J$ (% of factual content)")
    ax.set_title("(a) what quality gap a judge can actually resolve")
    ax.text(0.97, 0.06, f"{lim.max()/lim.min():.0f}$\\times$ spread", transform=ax.transAxes,
            ha="right", fontsize=8, color="#444")

    ax = axes[1]
    ax.scatter(acc * 100, lim * 100, s=24,
               color=[FAMCOL[fam(j)] for j in judges], zorder=3)
    ax.set_xlabel("meta-evaluation accuracy (%)")
    ax.set_ylabel("measured resolution limit $L_J$ (%)")
    ax.set_title("(b) accuracy compresses the difference")
    ax.annotate("", xy=(acc.min() * 100, 1), xytext=(acc.max() * 100, 1),
                arrowprops=dict(arrowstyle="<->", color="#888", lw=0.8))
    ax.text((acc.min() + acc.max()) * 50, 2.5,
            f"{(acc.max()-acc.min())*100:.0f} accuracy points", fontsize=6.2,
            ha="center", color="#666")
    fig.savefig(os.path.join(FIGS, "f1_limits.pdf"))
    plt.close(fig)


def f2_curves(R):
    gaps = np.array(R["gaps"]) / 6.0
    picks = ["gpt-5.4-mini::rubric", "gpt-4.1::direct",
             "gpt-4.1-mini::cot", "gpt-4o-mini::direct", "gpt-4.1-nano::direct"]
    picks = [p for p in picks if p in R["per_judge"]]
    fig, axes = plt.subplots(1, len(picks), figsize=(6.9, 1.95), sharey=True)
    for ax, j in zip(axes, picks):
        c = R["per_judge"][j]["curves"]
        ax.plot(gaps * 100, c["matched"], color="#333", lw=1.3, label="matched style")
        ax.plot(gaps * 100, c["random"], color=CFREE, lw=1.3, ls="-.", label="random style")
        ax.plot(gaps * 100, c["adversarial"], color=CS, lw=1.3, label="adversarial style")
        ax.axhline(0.5, color="crimson", lw=0.6, ls=":")
        lim = R["per_judge"][j]["observed_resolution_limit"] * 100
        ax.axvline(lim, color="#888", lw=0.8, ls="--")
        ax.set_xscale("log")
        ax.set_title(short(j), fontsize=6.8)
        ax.set_xlabel("true gap (%)", fontsize=6.8)
        ax.set_ylim(0.15, 1.03)
    axes[0].set_ylabel("P(correct order)")
    axes[0].legend(frameon=False, loc="lower right", fontsize=5.6)
    fig.savefig(os.path.join(FIGS, "f2_curves.pdf"))
    plt.close(fig)


def f3_calibration(R, C):
    judges = R["judges"]
    lim = np.array([R["per_judge"][j]["observed_resolution_limit"] for j in judges])
    ds = np.array([R["per_judge"][j]["delta_style"] for j in judges])
    acc = np.array([C["compositions"]["clearcut+matched"]["accuracy"][j] for j in judges])
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.7))

    ax = axes[0]
    ax.scatter(ds * 100, lim * 100, s=26, color=CFREE, zorder=3)
    b, a = np.polyfit(ds, lim, 1)
    xs = np.linspace(0, ds.max(), 50)
    ax.plot(xs * 100, (a + b * xs) * 100, color="#444", lw=0.9)
    ax.plot([0, ds.max() * 100], [0, ds.max() * 100], color="#BBB", lw=0.8, ls=":")
    r2 = C["calibration"]["delta_style"]["r2"]
    sd = C["calibration"]["delta_style"]["resid_sd_claims"]
    ax.set_xlabel(r"label-free predictor: bias-equivalent gap $\gamma_J$ (%)")
    ax.set_ylabel("measured resolution limit $L_J$ (%)")
    ax.set_title(f"(a) label-free: $R^2$={r2:.3f}, resid {np.floor(sd*1000+0.5)/10:.1f}%")

    ax = axes[1]
    ax.scatter(acc * 100, lim * 100, s=26, color=CGOLD, zorder=3)
    b2, a2 = np.polyfit(acc, lim, 1)
    xs = np.linspace(acc.min(), acc.max(), 50)
    ax.plot(xs * 100, (a2 + b2 * xs) * 100, color="#444", lw=0.9)
    r2b = C["calibration"]["clearcut+matched"]["r2"]
    sdb = C["calibration"]["clearcut+matched"]["resid_sd_claims"]
    ax.set_xlabel("gold-label meta-evaluation accuracy (%)")
    ax.set_ylabel("measured resolution limit $L_J$ (%)")
    ax.set_title(f"(b) gold-label: $R^2$={r2b:.3f}, resid {np.floor(sdb*1000+0.5)/10:.1f}%")
    fig.savefig(os.path.join(FIGS, "f3_calibration.pdf"))
    plt.close(fig)


def f4_certificate(E):
    judges = E["judges"]
    raw = np.array([E["per_judge"][j]["raw_acc"] for j in judges])
    cov = np.array([E["per_judge"][j]["coverage"] for j in judges])
    cer = np.array([E["per_judge"][j]["certified_acc"] for j in judges])
    abst = np.array([E["per_judge"][j]["abstained_acc"] for j in judges])
    fig, axes = plt.subplots(1, 2, figsize=(6.9, 2.7))

    ax = axes[0]
    o = np.argsort(raw)
    x = np.arange(len(o))
    ax.plot(x, raw[o] * 100, "o-", ms=3, lw=1, color="#888", label="trust the judge")
    ax.plot(x, cer[o] * 100, "o-", ms=3, lw=1, color=CFREE, label="certified pairs only")
    ax.plot(x, abst[o] * 100, "o-", ms=3, lw=1, color=CS, label="pairs it abstains on")
    ax.set_xticks(x)
    ax.set_xticklabels([short(judges[i]) for i in o], rotation=90, fontsize=4.8)
    ax.set_ylabel("ranking accuracy (%)")
    ax.set_title("(a) the certificate separates trustworthy claims")
    ax.legend(frameon=False, loc="lower right", fontsize=6)

    ax = axes[1]
    ax.scatter(cov * 100, cer * 100, s=26, color=CFREE, zorder=3, label="certified")
    ax.scatter(cov * 100, raw * 100, s=18, color="#BBB", zorder=2, label="raw")
    for c, a, b in zip(cov, raw, cer):
        ax.plot([c * 100, c * 100], [a * 100, b * 100], color="#DDD", lw=0.6, zorder=1)
    ax.set_xlabel("coverage (% of pairs certified)")
    ax.set_ylabel("ranking accuracy (%)")
    ax.set_title("(b) coverage / soundness trade-off")
    ax.legend(frameon=False, loc="lower right", fontsize=6)
    fig.savefig(os.path.join(FIGS, "f4_certificate.pdf"))
    plt.close(fig)


def f5_decomposition(A):
    judges = A["judges"]
    q = np.array([A["decomposition"][j]["ss_quality"] for j in judges])
    s = np.array([A["decomposition"][j]["ss_style"] for j in judges])
    i = np.array([A["decomposition"][j]["ss_inter"] for j in judges])
    tot = q + s + i
    o = np.argsort(-(q / tot))
    fig, ax = plt.subplots(figsize=(6.9, 2.3))
    x = np.arange(len(o))
    ax.bar(x, (q / tot)[o], color=CQ, label="quality (valid signal)")
    ax.bar(x, (s / tot)[o], bottom=(q / tot)[o], color=CS, label="style (pure bias)")
    ax.bar(x, (i / tot)[o], bottom=((q + s) / tot)[o], color=CI_,
           label=r"quality$\times$style (pure bias)")
    ax.set_xticks(x)
    ax.set_xticklabels([short(judges[k]) for k in o], rotation=90, fontsize=5)
    ax.set_ylabel("share of between-system\nvariance")
    ax.set_ylim(0, 1)
    ax.legend(ncol=3, frameon=False, loc="lower left", fontsize=6.2)
    fig.savefig(os.path.join(FIGS, "f5_decomposition.pdf"))
    plt.close(fig)


def main():
    os.makedirs(FIGS, exist_ok=True)
    R, C, E, A = load()
    f1_limits(R, C)
    f2_curves(R)
    f3_calibration(R, C)
    f4_certificate(E)
    f5_decomposition(A)
    for f in sorted(os.listdir(FIGS)):
        print("  ", f)


if __name__ == "__main__":
    main()
