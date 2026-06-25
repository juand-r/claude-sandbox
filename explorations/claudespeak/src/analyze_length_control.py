"""Step 2 — length-stratified robustness.

Threat: Claude writes longer answers, so length-normalized prose features
(sentence burstiness, function-word density, em-dash rate) might still be length
artifacts. Two controls, on markdown-stripped prose:

  (1) Within-quartile Cohen's d: bin all records by word-count quartile, recompute
      Claude-vs-pooled-others d *inside* each bin. If the effect holds in every
      bin, it is not a length artifact.
  (2) Length-controlled OLS: feature ~ 1 + is_claude + zscore(n_words). The
      is_claude coefficient (with t-stat) is the Claude effect holding length
      fixed.

Writes reports/pilot_length_control.md.
"""
from __future__ import annotations

import os

import numpy as np
import pandas as pd

from analyze_pilot import load_corpus_raw, cohens_d
from analyze_ablation import strip_markdown
from features import features
from schema import REPO

CLAUDE = "claude-opus-4-8"
REPORTS = os.path.join(REPO, "reports")
KEY = ["sentence_burstiness", "function_word_rate", "emdash_per100",
       "colon_per100", "question_per100", "ttr", "hapax_rate"]


def ols_claude_effect(df: pd.DataFrame, feat: str):
    """Return (beta_is_claude, t_stat) for feat ~ 1 + is_claude + z(n_words)."""
    y = df[feat].to_numpy(float)
    is_cl = (df["generator"] == CLAUDE).to_numpy(float)
    nw = df["n_words"].to_numpy(float)
    nwz = (nw - nw.mean()) / (nw.std() + 1e-9)
    X = np.column_stack([np.ones_like(y), is_cl, nwz])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    dof = len(y) - X.shape[1]
    sigma2 = (resid @ resid) / dof
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    return beta[1], beta[1] / se[1]


def main():
    os.makedirs(REPORTS, exist_ok=True)
    df = load_corpus_raw()
    prose = df["completion"].apply(lambda t: features(strip_markdown(t)))
    feat = prose.apply(pd.Series)
    df = pd.concat([df[["generator"]], feat], axis=1)

    # length bins (global word-count quartiles)
    df["lenq"] = pd.qcut(df["n_words"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

    # (1) within-quartile Cohen's d
    rows = []
    for f in KEY:
        rec = {"feature": f}
        for q in ["Q1", "Q2", "Q3", "Q4"]:
            sub = df[df["lenq"] == q]
            cl = sub[sub["generator"] == CLAUDE][f]
            ot = sub[sub["generator"] != CLAUDE][f]
            rec[q] = round(cohens_d(cl, ot), 2)
        rows.append(rec)
    within = pd.DataFrame(rows).set_index("feature")

    # (2) length-controlled OLS
    ols_rows = []
    for f in KEY:
        b, t = ols_claude_effect(df, f)
        ols_rows.append({"feature": f, "is_claude_beta": round(b, 3),
                         "t_stat": round(t, 1)})
    ols = pd.DataFrame(ols_rows).set_index("feature")

    # length by source (context)
    lentab = df.groupby("generator")["n_words"].agg(["mean", "median"]).round(1)
    qcounts = df.groupby(["lenq", "generator"], observed=True).size().unstack(fill_value=0)

    lines = ["# Step 2 — length-stratified robustness (markdown-stripped prose)\n",
             "## Answer length by source (words)\n",
             lentab.to_markdown() + "\n",
             "## Claude share across length quartiles (sanity: is Claude just the long bin?)\n",
             qcounts.to_markdown() + "\n",
             "## (1) Claude-vs-others Cohen's d WITHIN each length quartile\n",
             "If the effect holds across Q1–Q4, it is not a length artifact.\n",
             within.to_markdown() + "\n",
             "## (2) Length-controlled OLS: feature ~ is_claude + z(n_words)\n",
             "is_claude_beta = Claude effect holding length fixed; |t|>~2 is significant.\n",
             ols.to_markdown() + "\n"]
    with open(os.path.join(REPORTS, "pilot_length_control.md"), "w") as f:
        f.write("\n".join(lines))

    print("Length by source:\n", lentab.to_string())
    print("\nWithin-quartile Cohen's d:\n", within.to_string())
    print("\nLength-controlled OLS (is_claude effect):\n", ols.to_string())
    print("\nwrote reports/pilot_length_control.md")


if __name__ == "__main__":
    main()
