"""Dashboard viewer for the Adaptive Ring System.

Renders a recorded run (the .npz history written by Universe.save_history)
into:

  * an animated GIF of the universe evolving (universe grid + genome raster +
    live metric traces), and
  * a static summary figure of the whole run's metrics.

Metrics are recomputed from the saved bit history so the viewer is
self-contained and you can re-render without re-simulating.

Usage:
    python3 viz.py history.npz --gif evolution.gif --summary summary.png
"""

from __future__ import annotations

import argparse

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter

import ring_system as rs

# Field-boundary positions for the genome raster (between consecutive fields).
FIELD_BOUNDS = [8, 16, 24, 32, 33, 34]
FIELD_LABELS = [("RULE", 4), ("PULL", 12), ("PUSH", 20), ("ORD", 28),
                ("S", 32), ("D", 33), ("M", 35)]


def load(path: str):
    d = np.load(path)
    return d["bits"], d["occ"]   # (T, N, 36) uint8, (T, N) bool


def compute_metrics(bits, occ):
    """Per-tick metric arrays recomputed from the history."""
    T = bits.shape[0]
    pop = occ.sum(axis=1)
    uniq = np.zeros(T, dtype=int)
    rules = np.zeros(T, dtype=int)
    mutlvl = np.zeros(T)
    activity = np.zeros(T, dtype=int)
    for t in range(T):
        o = occ[t]
        if o.any():
            rows = bits[t][o]
            uniq[t] = np.unique(rows, axis=0).shape[0]
            rules[t] = np.unique(rs.get_field(rows, rs.RULE)).shape[0]
            mutlvl[t] = np.mean([rs.mut_level(r) for r in rows])
        if t > 0:
            # bits changed among slots occupied in both frames (transform proxy)
            common = occ[t] & occ[t - 1]
            if common.any():
                activity[t] = int(np.sum(bits[t][common] != bits[t - 1][common]))
    return dict(pop=pop, uniq=uniq, rules=rules, mut=mutlvl, activity=activity)


def grid_image(bits_t, occ_t, side):
    """Universe as a side x side grid coloured by RULE; empties are -1."""
    n = side * side
    img = np.full(n, -1.0)
    rule = rs.get_field(bits_t, rs.RULE)
    img[occ_t] = rule[occ_t]
    return img.reshape(side, side)


def _setup_axes(fig):
    gs = fig.add_gridspec(2, 2, width_ratios=[1, 1.3], height_ratios=[1, 1],
                          hspace=0.35, wspace=0.3)
    ax_grid = fig.add_subplot(gs[0, 0])
    ax_raster = fig.add_subplot(gs[:, 1])
    ax_pop = fig.add_subplot(gs[1, 0])
    return ax_grid, ax_raster, ax_pop


def render_gif(bits, occ, metrics, path, side, fps, max_frames):
    T, N = occ.shape
    # subsample frames if the run is long
    step = max(1, T // max_frames)
    frames = list(range(0, T, step))

    fig = plt.figure(figsize=(11, 6))
    ax_grid, ax_raster, ax_pop = _setup_axes(fig)

    cmap_grid = plt.cm.viridis.copy()
    cmap_grid.set_under("#15161a")  # empty slots (value -1)

    # colorbar for the RULE scale (added once; ax_grid.clear() leaves it).
    sm = plt.cm.ScalarMappable(cmap=cmap_grid, norm=plt.Normalize(0, 255))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax_grid, fraction=0.046, pad=0.04)
    cbar.set_label("RULE (0--255); dark = empty", fontsize=7)
    cbar.ax.tick_params(labelsize=6)

    writer = PillowWriter(fps=fps)
    with writer.saving(fig, path, dpi=90):
        for t in frames:
            ax_grid.clear(); ax_raster.clear(); ax_pop.clear()

            # universe grid
            g = grid_image(bits[t], occ[t], side)
            ax_grid.imshow(g, cmap=cmap_grid, vmin=0, vmax=255,
                           interpolation="nearest")
            ax_grid.set_title(f"slots (colour = RULE)  t={t}", fontsize=10)
            ax_grid.set_xticks([]); ax_grid.set_yticks([])

            # genome raster: occupied rings stacked, 36 bits wide
            o = occ[t]
            raster = bits[t][o] if o.any() else np.zeros((1, rs.N_BITS))
            ax_raster.imshow(raster, cmap="gray_r", aspect="auto",
                             interpolation="nearest")
            for b in FIELD_BOUNDS:
                ax_raster.axvline(b - 0.5, color="#e06c3a", lw=0.8)
            ax_raster.set_xticks([p for _, p in FIELD_LABELS])
            ax_raster.set_xticklabels([lab for lab, _ in FIELD_LABELS],
                                      fontsize=7)
            ax_raster.set_ylabel("occupied rings")
            ax_raster.set_title(f"genomes ({int(o.sum())} rings x 36 bits)",
                                fontsize=10)

            # population trace up to t
            ax_pop.plot(metrics["pop"][: t + 1], color="#2a7", label="pop")
            ax_pop.plot(metrics["uniq"][: t + 1], color="#27a", lw=0.9,
                        label="unique")
            ax_pop.set_xlim(0, T)
            ax_pop.set_ylim(0, max(1, N))
            ax_pop.set_title("population / unique genotypes", fontsize=10)
            ax_pop.legend(fontsize=7, loc="upper right")
            ax_pop.set_xlabel("tick")

            writer.grab_frame()
    plt.close(fig)
    return path


def render_summary(metrics, path):
    T = len(metrics["pop"])
    x = np.arange(T)
    fig, axes = plt.subplots(2, 2, figsize=(11, 6))
    fig.suptitle("Adaptive Ring System --- run summary", fontsize=12)

    axes[0, 0].plot(x, metrics["pop"], color="#2a7")
    axes[0, 0].set_title("population"); axes[0, 0].set_xlabel("tick")

    axes[0, 1].plot(x, metrics["uniq"], color="#27a", label="unique genotypes")
    axes[0, 1].plot(x, metrics["rules"], color="#a72", label="distinct rules")
    axes[0, 1].set_title("diversity"); axes[0, 1].legend(fontsize=8)
    axes[0, 1].set_xlabel("tick")

    axes[1, 0].plot(x, metrics["activity"], color="#722")
    axes[1, 0].set_title("activity (bits changed / tick)")
    axes[1, 0].set_xlabel("tick")

    axes[1, 1].plot(x, metrics["mut"], color="#666")
    axes[1, 1].set_title("mean mutation level (0--3)")
    axes[1, 1].set_ylim(0, 3); axes[1, 1].set_xlabel("tick")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=110)
    plt.close(fig)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("history", help="path to history .npz")
    ap.add_argument("--gif", default="evolution.gif")
    ap.add_argument("--summary", default="summary.png")
    ap.add_argument("--side", type=int, default=16, help="universe grid side")
    ap.add_argument("--fps", type=int, default=10)
    ap.add_argument("--max-frames", type=int, default=200)
    args = ap.parse_args()

    bits, occ = load(args.history)
    metrics = compute_metrics(bits, occ)
    render_summary(metrics, args.summary)
    render_gif(bits, occ, metrics, args.gif, args.side, args.fps,
               args.max_frames)
    print(f"wrote {args.summary} and {args.gif}")


if __name__ == "__main__":
    main()
