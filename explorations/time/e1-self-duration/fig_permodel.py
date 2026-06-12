"""E1 figure: one log-log scatter per model of predicted vs actual generation latency,
with the y=x reference line and the per-model geometric-mean ratio annotated. Pooling models
into one panel (the old figure) hid the per-model structure and overlapped points; this
facets them.
"""
import json
import os
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
rows = [json.loads(l) for l in open(os.path.join(HERE, "results.jsonl")) if l.strip()]

act, pre = {}, {}
for r in rows:
    k = (r["model"], r["task_id"], r["trial"])
    if r["condition"] == "task":
        act[k] = r["latency_s"]
    elif r["condition"] == "pre":
        pre[k] = r["parsed_estimate_s"]

bym = defaultdict(list)
for k in act:
    if k in pre and pre[k] and act[k]:
        bym[k[0]].append((act[k], pre[k]))

# fixed, sensible model order (small -> large within provider)
order = ["haiku", "sonnet", "opus", "gpt4o-mini", "gpt4o", "gpt5.2"]
models = [m for m in order if m in bym] + [m for m in bym if m not in order]

fig, axes = plt.subplots(2, 3, figsize=(12, 7.5), sharex=True, sharey=True)
lim = [0.3, 60]
for ax, m in zip(axes.flat, models):
    pts = bym[m]
    a = np.array([p[0] for p in pts]); e = np.array([p[1] for p in pts])
    gm = float(np.exp(np.mean(np.log(e / a))))
    ax.scatter(a, e, s=26, alpha=0.65, edgecolor="none")
    ax.plot(lim, lim, "k--", lw=0.8)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_title(f"{m}   (gm ratio = {gm:.2f})", fontsize=11)
    ax.grid(True, which="major", ls=":", lw=0.4, alpha=0.5)
for ax in axes[-1, :]:
    ax.set_xlabel("actual latency (s)")
for ax in axes[:, 0]:
    ax.set_ylabel("predicted latency (s)")
fig.suptitle("E1: predicted vs. actual generation latency, per model "
             "(dashed line = perfect calibration)", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.97])
out = os.path.join(HERE, "fig_scatter_permodel.png")
fig.savefig(out, dpi=120)
print("wrote", out)
