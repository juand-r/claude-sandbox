"""Phase 1 descriptive stylometry on the pilot corpus.

Loads all corpus JSONL, computes features per record, aggregates by generator,
and ranks features by Claude-vs-comparison effect size (Cohen's d). Writes:
  - data/corpus/pilot_features.csv      (per-record features, for downstream use)
  - reports/pilot_stylometry.md         (human-readable summary + Claudeisms)

Checkpoint question (PLAN.md Phase 1): is there a visible, real Claude signal?
"""
from __future__ import annotations

import glob
import os

import numpy as np
import pandas as pd

from schema import read_records, CORPUS_DIR, REPO
from features import features, STYLE_FEATURES

REPORTS = os.path.join(REPO, "reports")
FEATS_CSV = os.path.join(CORPUS_DIR, "pilot_features.csv")
CLAUDE = "claude-opus-4-8"


def load_corpus_raw() -> pd.DataFrame:
    """All records as a DataFrame, keeping the raw 'completion' column."""
    rows = []
    for path in sorted(glob.glob(os.path.join(CORPUS_DIR, "pilot_*.jsonl"))):
        for r in read_records(path):
            rows.append(r)
    return pd.DataFrame(rows)


def load_corpus() -> pd.DataFrame:
    df = load_corpus_raw()
    feat = df["completion"].apply(features).apply(pd.Series)
    return pd.concat([df.drop(columns=["completion"]), feat], axis=1)


def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    va, vb = a.var(ddof=1), b.var(ddof=1)
    pooled = (((na - 1) * va + (nb - 1) * vb) / (na + nb - 2)) ** 0.5
    return float((a.mean() - b.mean()) / pooled) if pooled else 0.0


def main():
    os.makedirs(REPORTS, exist_ok=True)
    df = load_corpus()
    df.to_csv(FEATS_CSV, index=False)

    gens = sorted(df["generator"].unique())
    print("records per generator:")
    print(df["generator"].value_counts().to_string())

    # mean of each style feature by generator
    means = df.groupby("generator")[STYLE_FEATURES].mean().T

    # effect sizes: Claude vs each other source
    others = [g for g in gens if g != CLAUDE]
    claude_df = df[df["generator"] == CLAUDE]
    eff = pd.DataFrame(index=STYLE_FEATURES)
    for o in others:
        od = df[df["generator"] == o]
        eff[f"d_vs_{o}"] = [cohens_d(claude_df[f], od[f]) for f in STYLE_FEATURES]

    # rank by mean |d| across comparisons (the "Claudeisms")
    eff["mean_abs_d"] = eff.abs().mean(axis=1)
    eff_sorted = eff.sort_values("mean_abs_d", ascending=False)

    # write report
    lines = ["# Pilot stylometry — Claude vs human / GPT-4o / old-ChatGPT\n",
             f"Corpus: {len(df)} records across {len(gens)} sources "
             f"(HC3 pilot, 200 prompts).\n",
             "## Records per source\n",
             "```", df["generator"].value_counts().to_string(), "```\n",
             "## Top distinguishing features (ranked by mean |Cohen's d|, "
             "Claude vs others)\n",
             "Positive d = Claude uses it MORE than the comparison source.\n"]
    top = eff_sorted.head(18).copy()
    top_md = top.round(2).to_markdown()
    lines.append(top_md + "\n")

    lines.append("## Mean feature values by source (top 18 features)\n")
    means_top = means.loc[top.index]
    lines.append(means_top.round(2).to_markdown() + "\n")

    report = "\n".join(lines)
    with open(os.path.join(REPORTS, "pilot_stylometry.md"), "w") as f:
        f.write(report)

    print("\n=== Top Claude-distinguishing features (mean |d|) ===")
    print(eff_sorted.head(18).round(2).to_string())
    print(f"\nwrote {FEATS_CSV}")
    print(f"wrote {os.path.join(REPORTS, 'pilot_stylometry.md')}")


if __name__ == "__main__":
    main()
