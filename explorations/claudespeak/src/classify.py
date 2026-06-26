"""Step 4 — interpretable classifier: how separable is Claude, and on what?

Logistic regression (Claude vs not-Claude) on the interpretable feature set,
standardized, class-balanced. 5-fold stratified CV → ROC-AUC. Two conditions:
  - with_formatting: all features on raw text (includes markdown features)
  - prose_only: markdown stripped + formatting features dropped (voice, not layout)
Run per corpus track (HC3, AlpacaEval) so genre is held constant within each fit.
Coefficients (standardized) name which features carry the signal.

Writes reports/pilot_classifier.md.
"""
from __future__ import annotations

import glob
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from schema import read_records, CORPUS_DIR, REPO
from features import features, STYLE_FEATURES
from analyze_ablation import strip_markdown

CLAUDE = "claude-opus-4-8"
REPORTS = os.path.join(REPO, "reports")
FORMATTING = {"md_header_per100w", "md_bullet_per100w", "md_bold_per100w",
              "md_code_per100w", "emoji_per100"}
PROSE_FEATURES = [f for f in STYLE_FEATURES if f not in FORMATTING]


def load(track_glob: str) -> pd.DataFrame:
    rows = []
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, track_glob))):
        rows += read_records(p)
    return pd.DataFrame(rows)


def feat_matrix(df: pd.DataFrame, prose_only: bool):
    if prose_only:
        fr = df["completion"].apply(lambda t: features(strip_markdown(t)))
        cols = PROSE_FEATURES
    else:
        fr = df["completion"].apply(features)
        cols = STYLE_FEATURES
    X = fr.apply(pd.Series)[cols]
    y = (df["generator"] == CLAUDE).astype(int).to_numpy()
    return X[cols], y, cols


def evaluate(df: pd.DataFrame, prose_only: bool):
    X, y, cols = feat_matrix(df, prose_only)
    clf = make_pipeline(StandardScaler(),
                        LogisticRegression(class_weight="balanced", max_iter=2000))
    cv = StratifiedKFold(5, shuffle=True, random_state=42)
    proba = cross_val_predict(clf, X, y, cv=cv, method="predict_proba")[:, 1]
    auc = roc_auc_score(y, proba)
    acc = accuracy_score(y, (proba > 0.5).astype(int))
    # fit on all for coefficients (standardized)
    clf.fit(X, y)
    coef = clf.named_steps["logisticregression"].coef_[0]
    coefs = pd.Series(coef, index=cols).sort_values(key=abs, ascending=False)
    return auc, acc, coefs, int(y.sum()), len(y)


def main():
    os.makedirs(REPORTS, exist_ok=True)
    tracks = {"HC3 (human-anchored)": "pilot_*.jsonl",
              "AlpacaEval (modern models)": "alpaca_*.jsonl",
              "WildChat (vs GPT-4-0314)": "wildchat_*.jsonl",
              "NoRobots (vs human)": "norobots_*.jsonl"}
    lines = ["# Step 4 — interpretable classifier (Claude vs not-Claude)\n",
             "Logistic regression, standardized features, class-balanced, "
             "5-fold stratified CV. AUC=1.0 perfect, 0.5 chance.\n"]
    summary = []
    for tname, g in tracks.items():
        df = load(g)
        for prose_only in (False, True):
            cond = "prose_only" if prose_only else "with_formatting"
            auc, acc, coefs, npos, n = evaluate(df, prose_only)
            summary.append({"track": tname, "condition": cond,
                            "AUC": round(auc, 3), "acc": round(acc, 3),
                            "n_claude": npos, "n_total": n})
            lines.append(f"\n## {tname} — {cond} (AUC={auc:.3f}, acc={acc:.3f})\n")
            top = coefs.head(10)
            tbl = pd.DataFrame({"feature": top.index, "std_coef": top.values.round(2)})
            lines.append("Top features (|standardized coef|); + = pushes toward "
                         "Claude:\n")
            lines.append(tbl.to_markdown(index=False) + "\n")
            print(f"{tname:30s} {cond:16s} AUC={auc:.3f} acc={acc:.3f} "
                  f"(claude {npos}/{n})")

    sm = pd.DataFrame(summary)
    lines.insert(2, "## Summary\n\n" + sm.to_markdown(index=False) + "\n")
    with open(os.path.join(REPORTS, "pilot_classifier.md"), "w") as f:
        f.write("\n".join(lines))
    print("\nwrote reports/pilot_classifier.md")


if __name__ == "__main__":
    main()
