"""Register rigidity: how much does a source change its style across contexts?

For each track with a natural grouping axis and >=2 sources, we ask, per source:
what fraction of its style variation is explained by the task/context grouping?
We use eta-squared = between-group variance / total variance over standardized
style features. LOW eta^2 = the context barely moves the style = a RIGID,
context-invariant voice; HIGH eta^2 = the source adapts its style to the context.

Axes per track:
  - HC3        : domain  (cs_ai, finance, general, medicine)        [human + 2 models + Claude]
  - AlpacaEval : domain  (helpful_base, koala, oasst, selfinst, vicuna) [Claude + 6 models]
  - NoRobots   : task_type (10 task types)                           [human + Claude]

Two feature sets: ALL style features, and PROSE-only (markdown stripped + format
features dropped) -- the contrast isolates "adapts formatting" vs "adapts voice".
Optional length control: residualize each feature on z(log n_words) first.
Within a track, all sources share the same grouping and standardization, and (for
AlpacaEval/NoRobots) the same per-group sample sizes, so eta^2 is directly
comparable across sources. Bootstrap CIs included. No API calls.
"""
from __future__ import annotations

import glob
import os
import numpy as np
import pandas as pd

from schema import read_records, CORPUS_DIR, REPO
from features import features, STYLE_FEATURES
from analyze_ablation import strip_markdown

REPORTS = os.path.join(REPO, "reports")
FORMATTING = {"md_header_per100w", "md_bullet_per100w", "md_bold_per100w",
              "md_code_per100w", "emoji_per100"}
PROSE_FEATURES = [f for f in STYLE_FEATURES if f not in FORMATTING]
SEED = 42

# track -> (filename glob, grouping field)
TRACKS = {
    "HC3":        ("pilot_*.jsonl",   "domain"),
    "AlpacaEval": ("alpaca_*.jsonl",  "domain"),
    "NoRobots":   ("norobots_*.jsonl", "task_type"),
}


def load(track_glob):
    rows = []
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, track_glob))):
        rows += read_records(p)
    return rows


def feature_frame(recs, prose, length_control):
    cols = PROSE_FEATURES if prose else STYLE_FEATURES
    feats, nwords, gen, grp = [], [], [], []
    for r in recs:
        txt = strip_markdown(r["completion"]) if prose else r["completion"]
        f = features(txt)
        feats.append([f[c] for c in cols])
        nwords.append(max(f["n_words"], 1.0))
        gen.append(r["generator"])
        grp.append(r.get(GROUP_FIELD))
    X = np.asarray(feats, float)
    # standardize across the whole track
    mu, sd = X.mean(0), X.std(0); sd[sd == 0] = 1
    Z = (X - mu) / sd
    if length_control:
        lw = np.log(np.asarray(nwords))
        lwz = (lw - lw.mean()) / (lw.std() or 1)
        A = np.column_stack([np.ones_like(lwz), lwz])
        beta, *_ = np.linalg.lstsq(A, Z, rcond=None)
        Z = Z - A @ beta            # residualize every feature on log-length
    return Z, np.asarray(gen), np.asarray(grp)


def eta_squared(Z, groups):
    """Fraction of total variance (summed over features) explained by groups."""
    gc = Z.mean(0)
    total = ((Z - gc) ** 2).sum()
    between = 0.0
    for g in np.unique(groups):
        idx = groups == g
        between += idx.sum() * ((Z[idx].mean(0) - gc) ** 2).sum()
    return between / total if total else float("nan")


def bootstrap_eta(Z, groups, reps=300):
    rng = np.random.default_rng(SEED)
    n = len(Z)
    vals = []
    for _ in range(reps):
        samp = rng.integers(0, n, n)
        try:
            vals.append(eta_squared(Z[samp], groups[samp]))
        except Exception:
            pass
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return lo, hi


def run_track(name, recs, prose, length_control):
    Z, gen, grp = feature_frame(recs, prose, length_control)
    rows = []
    for s in sorted(set(gen)):
        idx = gen == s
        Zs, gs = Z[idx], grp[idx]
        if len(np.unique(gs)) < 2:
            continue
        e = eta_squared(Zs, gs)
        lo, hi = bootstrap_eta(Zs, gs)
        rows.append({"track": name, "source": s, "eta2": round(e, 3),
                     "ci_lo": round(lo, 3), "ci_hi": round(hi, 3),
                     "n": int(idx.sum()), "groups": len(np.unique(gs))})
    return rows


GROUP_FIELD = None  # set per track in main()


def main():
    global GROUP_FIELD
    os.makedirs(REPORTS, exist_ok=True)
    lines = ["# Register rigidity (reproducible: src/analyze_rigidity.py)\n",
             "eta^2 = fraction of a source's style variance explained by the "
             "task/context grouping. **Lower eta^2 = more rigid** (context barely "
             "moves the style); higher = adapts style to context. Style features "
             "standardized within each track; CIs are 95% bootstrap.\n"]
    all_rows = []
    for prose in (True, False):
        for lc in (True, False):
            tag = f"{'PROSE-only' if prose else 'ALL style feats'}" \
                  f"{', length-controlled' if lc else ''}"
            block = []
            for name, (g, field) in TRACKS.items():
                GROUP_FIELD = field
                recs = load(g)
                block += run_track(name, recs, prose, lc)
                for r in block:
                    r["variant"] = tag
            df = pd.DataFrame(block)
            all_rows += block
            lines.append(f"\n## {tag}\n")
            for name in TRACKS:
                sub = df[df["track"] == name].sort_values("eta2")
                if len(sub):
                    lines.append(f"\n**{name}** (axis: {TRACKS[name][1]}, "
                                 f"{sub['groups'].iloc[0]} groups) — sorted by "
                                 f"rigidity (lowest eta^2 = most rigid):\n")
                    lines.append(sub[["source", "eta2", "ci_lo", "ci_hi", "n"]]
                                 .to_markdown(index=False) + "\n")
            print(f"=== {tag} ===")
            print(df[["track", "source", "eta2", "ci_lo", "ci_hi"]].to_string(index=False))
    pd.DataFrame(all_rows).to_csv(os.path.join(CORPUS_DIR, "rigidity.csv"), index=False)
    with open(os.path.join(REPORTS, "rigidity.md"), "w") as f:
        f.write("\n".join(lines))
    print(f"\nwrote {os.path.join(REPORTS, 'rigidity.md')} and data/corpus/rigidity.csv")


if __name__ == "__main__":
    main()
