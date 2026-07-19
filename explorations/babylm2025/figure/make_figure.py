"""
BLiMP vs (Super)GLUE spread across BabyLM 2025 systems.
Data compiled from the primary submission papers (each point internally consistent,
from a single source). NOT the official leaderboard (gated). Values as-reported,
including author reproductions; GLUE vs SuperGLUE averaging conventions vary slightly.
Outputs a vector PDF for LaTeX inclusion.
"""
import csv, os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "blimp_glue_data.csv"))))
for r in rows:
    r["blimp"] = float(r["blimp"]); r["glue"] = float(r["glue"])
    r["is_baseline"] = r["is_baseline"] == "1"

# Colour by track; baselines drawn as a black-edged star.
track_color = {
    "strict": "#1f77b4",
    "strict-small": "#d62728",
    "interaction": "#2ca02c",
    "multimodal": "#9467bd",
}
track_label = {
    "strict": "Strict (100M)",
    "strict-small": "Strict-Small (10M)",
    "interaction": "Interaction",
    "multimodal": "Multimodal",
}

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 5.0), gridspec_kw={"width_ratios": [1.55, 1]})

# ---------- Panel A: scatter BLiMP vs GLUE ----------
ax = axL
ax.axvline(50, ls=":", lw=1, color="grey")
ax.text(50.4, 51.2, "BLiMP chance", rotation=90, va="bottom", ha="left", fontsize=7.5, color="grey")

for r in rows:
    c = track_color[r["track"]]
    if r["is_baseline"]:
        ax.scatter(r["blimp"], r["glue"], s=230, marker="*", color=c,
                   edgecolor="black", linewidth=1.1, zorder=5)
    else:
        ax.scatter(r["blimp"], r["glue"], s=70, color=c, edgecolor="white", linewidth=0.6, zorder=4)

# Label points (small offsets to reduce overlap)
offsets = {
    "GPT-BERT (baseline)": (-6.6, 1.5), "Simple-Diffusion": (-7.9, 1.5),
    "Once Upon a Time": (-9.0, 1.3), "BLaLM (strict)": (0.7, 0.5),
    "Syntactic-Curriculum": (-8.7, 0.8), "Batchwise-Convergent": (0.8, 0.2),
    "AMLM-Hard-Decay": (-7.2, 1.4), "AMLM-n-hot": (0.7, 0.4),
    "BLaLM (small)": (-6.4, -1.9), "Multi-Token-Prediction": (0.7, 0.4),
    "LLM-StudyPlans (human)": (-9.7, -1.9), "LLM-StudyPlans (synth)": (0.7, 0.4),
    "BitMar": (0.8, 0.3),
}
for r in rows:
    dx, dy = offsets.get(r["system"], (0.6, 0.5))
    ax.annotate(r["system"], (r["blimp"], r["glue"]), (r["blimp"]+dx, r["glue"]+dy),
                fontsize=7.0, color="#222")

ax.set_xlabel("BLiMP accuracy (%)")
ax.set_ylabel("(Super)GLUE average (%)")
ax.set_title("A. BLiMP vs (Super)GLUE across systems", fontsize=11, loc="left")
ax.set_xlim(45, 84)
ax.set_ylim(50, 75)
ax.grid(True, ls="--", lw=0.4, alpha=0.5)

legend_elems = [
    Line2D([0],[0], marker="o", color="w", markerfacecolor=track_color[t], markersize=8, label=track_label[t])
    for t in ["strict","strict-small","interaction","multimodal"]
]
legend_elems.append(Line2D([0],[0], marker="*", color="w", markerfacecolor="grey",
                    markeredgecolor="black", markersize=14, label="baseline (GPT-BERT)"))
ax.legend(handles=legend_elems, fontsize=7.7, loc="lower left", framealpha=0.95)

# ---------- Panel B: 1-D spread of each metric ----------
ax = axR
import numpy as np
blimp = np.array([r["blimp"] for r in rows])
glue  = np.array([r["glue"] for r in rows])
cols  = [track_color[r["track"]] for r in rows]

def strip(xpos, vals, colors):
    rng = np.random.default_rng(0)
    jit = (rng.random(len(vals)) - 0.5) * 0.28
    ax.scatter(np.full(len(vals), xpos) + jit, vals, c=colors, s=48,
               edgecolor="white", linewidth=0.5, zorder=3)
    # mean bar
    ax.plot([xpos-0.22, xpos+0.22], [vals.mean(), vals.mean()], color="black", lw=2, zorder=4)
    # min-max whisker
    ax.plot([xpos, xpos], [vals.min(), vals.max()], color="#555", lw=1, zorder=1)

strip(0, blimp, cols)
strip(1, glue, cols)
ax.axhline(50, ls=":", lw=1, color="grey")
ax.text(1.45, 50.3, "chance (BLiMP)", fontsize=7, color="grey", ha="right")
ax.set_xticks([0,1]); ax.set_xticklabels(["BLiMP", "(Super)GLUE"])
ax.set_ylabel("score (%)")
ax.set_xlim(-0.5, 1.5); ax.set_ylim(44, 84)
ax.set_title("B. Spread of each metric", fontsize=11, loc="left")
ax.grid(True, axis="y", ls="--", lw=0.4, alpha=0.5)
# annotate ranges
ax.annotate(f"range\n{blimp.min():.0f}-{blimp.max():.0f}", (0, 82), fontsize=7.5, ha="center", color="#333")
ax.annotate(f"range\n{glue.min():.0f}-{glue.max():.0f}", (1, 82), fontsize=7.5, ha="center", color="#333")

fig.tight_layout()
out = os.path.join(HERE, "blimp_glue_spread.pdf")
fig.savefig(out, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=160, bbox_inches="tight")
print("wrote", out)
print(f"BLiMP: min {blimp.min()} max {blimp.max()} mean {blimp.mean():.1f} sd {blimp.std():.1f}")
print(f"GLUE : min {glue.min()} max {glue.max()} mean {glue.mean():.1f} sd {glue.std():.1f}")
# correlation
print("Pearson r(BLiMP,GLUE) =", np.corrcoef(blimp, glue)[0,1].round(2))
