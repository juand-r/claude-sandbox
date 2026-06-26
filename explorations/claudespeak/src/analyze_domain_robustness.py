"""Per-domain robustness: does the prose fingerprint hold WITHIN each domain,
or is it driven by one topic? Reviewer pre-emption for "it's a topic artifact."

For each HC3 domain (and each AlpacaEval sub-source), compute Claude-vs-pooled-
others Cohen's d on the headline prose features (markdown stripped). If the sign
and magnitude persist across domains, the fingerprint is not a topic artifact.

Writes reports/domain_robustness.md.
"""
from __future__ import annotations

import glob
import os
import pandas as pd

from schema import read_records, CORPUS_DIR, REPO
from features import features
from analyze_ablation import strip_markdown
from analyze_pilot import cohens_d

CLAUDE = "claude-opus-4-8"
REPORTS = os.path.join(REPO, "reports")
KEY = ["sentence_burstiness", "function_word_rate", "emdash_per100",
       "question_per100"]
LABEL = {"sentence_burstiness": "burstiness", "function_word_rate": "func-word",
         "emdash_per100": "em-dash", "question_per100": "question"}


def load(track_glob):
    rows = []
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, track_glob))):
        rows += read_records(p)
    df = pd.DataFrame(rows)
    feat = df["completion"].apply(lambda t: features(strip_markdown(t))).apply(pd.Series)
    return pd.concat([df[["generator", "domain"]], feat], axis=1)


def per_domain(df, track):
    rows = []
    for dom in sorted(df["domain"].dropna().unique()):
        sub = df[df["domain"] == dom]
        cl = sub[sub["generator"] == CLAUDE]
        ot = sub[sub["generator"] != CLAUDE]
        n_prompts = sub["generator"].eq(CLAUDE).sum()
        rec = {"track": track, "domain": dom, "n_prompts": int(n_prompts)}
        for f in KEY:
            rec[LABEL[f]] = round(cohens_d(cl[f], ot[f]), 2)
        rows.append(rec)
    return rows


def main():
    os.makedirs(REPORTS, exist_ok=True)
    rows = []
    rows += per_domain(load("pilot_*.jsonl"), "HC3")
    rows += per_domain(load("alpaca_*.jsonl"), "AlpacaEval")
    tab = pd.DataFrame(rows)

    lines = ["# Per-domain robustness (Claude vs.\\ pooled others, prose only)\n",
             "Cohen's $d$ within each domain for the headline prose features. "
             "Positive = Claude higher (for func-word, negative = Claude denser, "
             "as expected). Stable sign/magnitude across domains ⇒ not a topic "
             "artifact.\n",
             tab.to_markdown(index=False) + "\n"]
    with open(os.path.join(REPORTS, "domain_robustness.md"), "w") as f:
        f.write("\n".join(lines))
    print(tab.to_string(index=False))
    print("\nwrote reports/domain_robustness.md")


if __name__ == "__main__":
    main()
