"""Figures for REPORT.md, read from results/*.json, written to figures/."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
RESULTS, FIGURES = HERE / "results", HERE / "figures"

# Reference categorical palette (dataviz skill), fixed order.
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2, "axes.grid": True, "grid.color": GRID,
    "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 2,
    "font.size": 10, "legend.frameon": False,
})


def load(name):
    return json.loads((RESULTS / f"{name}.json").read_text())["log"]


def col(log, key, phase=None):
    rows = [r for r in log if phase is None or r.get("phase") in (phase, "init")]
    return [r["epoch"] for r in rows], [r[key] for r in rows]


def finish(fig, name):
    FIGURES.mkdir(exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIGURES / f"{name}.png", dpi=140)
    plt.close(fig)
    print(f"wrote figures/{name}.png")


def zero_line(ax):
    ax.axhline(1.0, color=INK2, lw=1, ls="--")
    ax.annotate("predicting 0 everywhere", (0.98, 1.0), xycoords=("axes fraction", "data"),
                ha="right", va="bottom", color=INK2, fontsize=8)


def fig_optimizers(seed=0):
    names = [("sgd", "SGD", 30), ("sgd_momentum", "SGD + momentum", 30), ("adam", "Adam", 30),
             ("adagrad", "Adagrad", 30), ("adamax", "Adamax", 100), ("rmsprop", "RMSprop", 30)]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    for i, (key, label, ep) in enumerate(names):
        log = load(f"opt_{key}_{ep}ep_seed{seed}")[:31]
        for ax, k in zip(axes, ["L_SR", "theta_rms", "rel_error"]):
            ax.plot(*col(log, k), color=C[i], label=label)
    axes[0].set(title="Test loss L_SR (log scale)", xlabel="epoch", yscale="log")
    axes[1].set(title="Weight RMS", xlabel="epoch")
    axes[2].set(title="Relative error L_SR / Σθ²", xlabel="epoch", ylim=(0, 2))
    zero_line(axes[2])
    axes[0].legend(fontsize=8)
    fig.suptitle(f"E1: gradient-based optimizers, vanilla quine (seed {seed})")
    finish(fig, "e1_optimizers")


def fig_regeneration(seeds=(0, 1, 2)):
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    for j, (T, label) in enumerate([(1, "T = 1 (Adamax epoch, then regenerate)"), (0, "T = 0 (regenerate only)")]):
        for s in seeds:
            log = load(f"regen_T{T}_G10_seed{s}")
            for ax, k in zip(axes, ["L_SR", "theta_rms", "rel_error"]):
                ax.plot(*col(log, k, "after_regen"), color=C[j], alpha=0.85,
                        label=label if s == seeds[0] else None, marker="o", ms=4)
    axes[0].set(title="Test loss L_SR (log scale)", xlabel="generation", yscale="log")
    axes[1].set(title="Weight RMS (log scale)", xlabel="generation", yscale="log")
    axes[2].set(title="Relative error L_SR / Σθ²", xlabel="generation", ylim=(0, 2))
    zero_line(axes[2])
    axes[0].legend(fontsize=8)
    fig.suptitle(f"E5/E6: regeneration, measured after each regeneration ({len(seeds)} seeds each)")
    finish(fig, "e5_regeneration")


def fig_aux(seed=0):
    q, base = load(f"aux_quine_30ep_seed{seed}"), load(f"aux_taskonly_30ep_seed{seed}")
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    for i, (k, label) in enumerate([("L_aux", "L_Aux"), ("L_SR", "L_SR"), ("lam_L_task", "λ·L_Task")]):
        axes[0].plot(*col(q, k), color=C[i], label=label)
    axes[0].set(title="Auxiliary quine: test losses", xlabel="epoch")
    axes[0].legend(fontsize=8)
    axes[1].plot(*col(q, "rel_error"), color=C[0])
    axes[1].set(title="Auxiliary quine: L_SR / Σθ²", xlabel="epoch")
    zero_line(axes[1])
    for i, (log, label) in enumerate([(q, "quine (L_SR + λ·L_Task)"), (base, "classifier only (λ·L_Task)")]):
        axes[2].plot(*col(log, "accuracy"), color=C[i], label=label)
    axes[2].set(title="Test accuracy", xlabel="epoch", ylim=(0.6, 1.0))
    axes[2].legend(fontsize=8)
    fig.suptitle(f"E7/E8: auxiliary quine on MNIST, Adamax (seed {seed})")
    finish(fig, "e7_auxiliary")


def fig_hill_sweep(sigmas=("1e-05", "3e-05", "0.0001", "0.0003", "0.001", "0.003")):
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for i, s in enumerate(sigmas):
        log = load(f"hill_sigma{s}_50ep_from-init_seed0")
        axes[0].plot(*col(log, "L_SR"), color=C[i], label=f"σ = {float(s):g}")
        axes[1].plot(*col(log, "rel_error"), color=C[i])
    axes[0].set(title="Test loss L_SR (log scale)", xlabel="epoch", yscale="log")
    axes[1].set(title="Relative error L_SR / Σθ²", xlabel="epoch")
    zero_line(axes[1])
    axes[0].legend(fontsize=8)
    fig.suptitle("E3: hill-climbing noise sweep, 50 epochs (seed 0)")
    finish(fig, "e3_hill_sweep")


if __name__ == "__main__":
    fig_optimizers()
    fig_regeneration()
    fig_aux()
    fig_hill_sweep()
