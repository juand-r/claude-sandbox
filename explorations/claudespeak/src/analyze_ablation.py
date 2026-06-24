"""Markdown-stripped ablation: is Claude still identifiable from RAW PROSE,
once its formatting scaffolding (headers, bullets, bold, code) is removed?

This separates "voice" from "formatting habit" (PLAN.md S3 guard). We strip
markdown markup, keep the underlying words, recompute features, and re-rank
Claude-vs-rest effect sizes. Writes reports/pilot_ablation_markdown.md.
"""
from __future__ import annotations

import os
import re

import pandas as pd

from analyze_pilot import load_corpus_raw, cohens_d  # reuse loaders
from features import features, STYLE_FEATURES
from schema import REPO

CLAUDE = "claude-opus-4-8"
REPORTS = os.path.join(REPO, "reports")

# structural/formatting features to drop from the prose-only ranking
FORMATTING = {"md_header_per100w", "md_bullet_per100w", "md_bold_per100w",
              "md_code_per100w", "emoji_per100"}
PROSE_FEATURES = [f for f in STYLE_FEATURES if f not in FORMATTING]


def strip_markdown(t: str) -> str:
    t = re.sub(r"(?m)^\s{0,3}#{1,6}\s*", "", t)            # headers
    t = re.sub(r"(?m)^\s*([-*+]|\d+\.)\s+", "", t)          # bullet/number markers
    t = re.sub(r"```.*?```", " ", t, flags=re.S)            # code fences
    t = re.sub(r"`([^`]*)`", r"\1", t)                      # inline code
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)                # bold
    t = re.sub(r"\*([^*]+)\*", r"\1", t)                    # italics
    t = re.sub(r"__([^_]+)__", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)          # links -> text
    t = re.sub(r"[ \t]+", " ", t)
    return t.strip()


def main():
    os.makedirs(REPORTS, exist_ok=True)
    df = load_corpus_raw()  # has 'completion'
    df["stripped"] = df["completion"].apply(strip_markdown)
    feat = df["stripped"].apply(features).apply(pd.Series)
    df = pd.concat([df[["generator"]], feat], axis=1)

    gens = sorted(df["generator"].unique())
    others = [g for g in gens if g != CLAUDE]
    cl = df[df["generator"] == CLAUDE]
    eff = pd.DataFrame(index=PROSE_FEATURES)
    for o in others:
        od = df[df["generator"] == o]
        eff[f"d_vs_{o}"] = [cohens_d(cl[f], od[f]) for f in PROSE_FEATURES]
    eff["mean_abs_d"] = eff.abs().mean(axis=1)
    eff = eff.sort_values("mean_abs_d", ascending=False)

    means = df.groupby("generator")[PROSE_FEATURES].mean().T.loc[eff.index]

    lines = ["# Pilot ablation — Claude identifiability from RAW PROSE "
             "(markdown stripped)\n",
             "Formatting features (headers/bullets/bold/code/emoji) are removed "
             "and markup is stripped from the text. If Claude still separates, "
             "the voice is more than a formatting habit.\n",
             "## Prose-only distinguishing features (mean |Cohen's d|)\n",
             "Positive d = Claude MORE than comparison.\n",
             eff.head(15).round(2).to_markdown() + "\n",
             "## Mean prose-feature values by source\n",
             means.head(15).round(2).to_markdown() + "\n"]
    with open(os.path.join(REPORTS, "pilot_ablation_markdown.md"), "w") as f:
        f.write("\n".join(lines))

    print("=== Prose-only (markdown stripped) Claude separation ===")
    print(eff.head(15).round(2).to_string())
    print(f"\nwrote {os.path.join(REPORTS, 'pilot_ablation_markdown.md')}")


if __name__ == "__main__":
    main()
