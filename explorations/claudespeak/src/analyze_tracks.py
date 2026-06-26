"""Cross-track fingerprint replication.

The pilot established a Claude fingerprint on HC3. This asks: does the SAME
fingerprint hold across four corpora with different prompt distributions and
different contrast sources?
  - HC3        : Claude vs {human, GPT-4o, GPT-3.5-era ChatGPT}
  - AlpacaEval : Claude vs six modern models (no human)
  - WildChat   : Claude vs GPT-4-0314 (real user prompts)
  - NoRobots   : Claude vs human (diverse task types)

For each track we pool the non-Claude sources and report Claude-vs-pooled
Cohen's d on the headline style features. A consistent sign (and rough
magnitude) across tracks is the generalization result. No API calls.
"""
from __future__ import annotations

import glob
import os

import numpy as np
import pandas as pd

from schema import read_records, CORPUS_DIR, REPO
from features import features
from analyze_pilot import cohens_d

REPORTS = os.path.join(REPO, "reports")
CLAUDE = "claude-opus-4-8"
TRACK_ORDER = ["HC3", "AlpacaEval", "WildChat", "NoRobots"]

# Headline features that define "Claudespeak" (sign noted for reading the table).
HEADLINE = [
    ("sentence_burstiness", "rhythm: std/mean sentence length (Claude higher)"),
    ("function_word_rate", "content density: function-word fraction (Claude lower)"),
    ("emdash_per100", "em-dash rate /100w (Claude higher)"),
    ("md_bullet_per100w", "markdown bullets /100w"),
    ("md_header_per100w", "markdown headers /100w"),
    ("md_bold_per100w", "markdown bold /100w"),
    ("question_per100", "questions /100w (offer-to-continue proxy)"),
    ("colon_per100", "colon rate /100w (scaffolding)"),
    ("ttr", "type-token ratio"),
]


def track_of(rec) -> str:
    return (rec.get("prompt_source") or {}).get("dataset") or "?"


def load_all() -> pd.DataFrame:
    rows = []
    for path in sorted(glob.glob(os.path.join(CORPUS_DIR, "*.jsonl"))):
        for r in read_records(path):
            r["_track"] = track_of(r)
            rows.append(r)
    df = pd.DataFrame(rows)
    feat = df["completion"].apply(features).apply(pd.Series)
    return pd.concat([df.drop(columns=["completion"]), feat], axis=1)


def main():
    os.makedirs(REPORTS, exist_ok=True)
    df = load_all()
    tracks = [t for t in TRACK_ORDER if t in set(df["_track"])]

    # provenance counts per track
    counts = (df.groupby(["_track", "generator"]).size()
              .rename("n").reset_index())

    feat_names = [f for f, _ in HEADLINE]
    eff = pd.DataFrame(index=feat_names)
    nrec = {}
    for t in tracks:
        sub = df[df["_track"] == t]
        claude = sub[sub["generator"] == CLAUDE]
        others = sub[sub["generator"] != CLAUDE]
        nrec[t] = (len(claude), len(others))
        if len(claude) < 2 or len(others) < 2:
            eff[t] = [float("nan")] * len(feat_names)
            continue
        eff[t] = [cohens_d(claude[f].values, others[f].values) for f in feat_names]

    # consistency: sign agreement across tracks per feature
    def sign_agree(row):
        signs = [np.sign(v) for v in row if not np.isnan(v)]
        if not signs:
            return "-"
        pos = sum(1 for s in signs if s > 0)
        neg = sum(1 for s in signs if s < 0)
        return f"{max(pos, neg)}/{len(signs)}"

    eff_disp = eff.copy()
    eff_disp["sign_agree"] = eff.apply(sign_agree, axis=1)
    eff_disp.insert(0, "feature_meaning", [m for _, m in HEADLINE])

    lines = ["# Cross-track fingerprint replication "
             "(reproducible: src/analyze_tracks.py)\n",
             "Claude vs pooled non-Claude sources, Cohen's d, per track. "
             "Positive d = Claude uses it MORE.\n",
             "## Records per track and source\n",
             counts.pivot(index="generator", columns="_track", values="n")
             .fillna(0).astype(int).to_markdown() + "\n",
             "## Claude-vs-pooled effect sizes (headline features)\n",
             "n (Claude, others) per track: "
             + ", ".join(f"{t}={nrec[t]}" for t in tracks) + "\n",
             eff_disp.round(2).to_markdown() + "\n",
             "`sign_agree` = how many tracks share the majority sign "
             "(higher = more consistent fingerprint).\n"]

    with open(os.path.join(REPORTS, "cross_track_fingerprint.md"), "w") as f:
        f.write("\n".join(lines))

    print("records per track:")
    print(counts.pivot(index="generator", columns="_track", values="n")
          .fillna(0).astype(int).to_string())
    print("\n=== Claude-vs-pooled Cohen's d by track ===")
    print(eff_disp.drop(columns="feature_meaning").round(2).to_string())
    print(f"\nwrote {os.path.join(REPORTS, 'cross_track_fingerprint.md')}")


if __name__ == "__main__":
    main()
