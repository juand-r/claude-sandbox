"""Step 3 analysis — does the Claude signature replicate vs MODERN models, and
does the GPT-excess vocabulary appear (GPT-side) in this essay/instruction genre?

Corpus: AlpacaEval track. Claude (self-gen) vs 6 reused modern-ish models
(gpt-4-turbo, gpt-4o, gemini-pro, deepseek-67b, Qwen2-72B, Llama-3-70B).
No human cell (by design).

Writes reports/alpaca_track.md.
"""
from __future__ import annotations

import glob
import os
import re
from collections import Counter

import pandas as pd

from schema import read_records, CORPUS_DIR, REPO
from features import features, STYLE_FEATURES
from analyze_ablation import strip_markdown
from analyze_pilot import cohens_d
from ngram_signature import tokenize, group_counts, fightin_words

CLAUDE = "claude-opus-4-8"
REPORTS = os.path.join(REPO, "reports")
WORD = re.compile(r"[a-z']+")
GPT_EXCESS = ["delve", "delves", "delving", "intricate", "crucial", "pivotal",
              "comprehensive", "meticulous", "realm", "robust", "seamless",
              "underscore", "showcase", "essential", "nuanced", "leverage"]
FORMATTING = {"md_header_per100w", "md_bullet_per100w", "md_bold_per100w",
              "md_code_per100w", "emoji_per100"}
PROSE = [f for f in STYLE_FEATURES if f not in FORMATTING]


def load():
    rows = []
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, "alpaca_*.jsonl"))):
        rows += read_records(p)
    return pd.DataFrame(rows)


def main():
    os.makedirs(REPORTS, exist_ok=True)
    df = load()
    gens = sorted(df["generator"].unique())
    counts = df["generator"].value_counts()

    # prose features (markdown stripped)
    prose = df["completion"].apply(lambda t: features(strip_markdown(t)))
    fdf = pd.concat([df[["generator"]], prose.apply(pd.Series)], axis=1)
    cl = fdf[fdf["generator"] == CLAUDE]
    others = fdf[fdf["generator"] != CLAUDE]

    # (A) Claude vs pooled modern others — prose effect sizes
    eff = pd.DataFrame(index=PROSE)
    eff["d_vs_pooled_modern"] = [cohens_d(cl[f], others[f]) for f in PROSE]
    eff["claude_mean"] = [cl[f].mean() for f in PROSE]
    eff["others_mean"] = [others[f].mean() for f in PROSE]
    eff = eff.reindex(eff["d_vs_pooled_modern"].abs().sort_values(ascending=False).index)

    # (B) GPT-excess vocabulary by source (per 1000 words) in THIS genre
    tot = {g: 0 for g in gens}
    wc = {g: Counter() for g in gens}
    for _, r in df.iterrows():
        toks = WORD.findall((r["completion"] or "").lower())
        wc[r["generator"]].update(toks)
        tot[r["generator"]] += len(toks)
    voc_rows = []
    for w in GPT_EXCESS:
        voc_rows.append({"term": w, **{g: round(1000 * wc[g][w] / max(tot[g], 1), 3)
                                       for g in gens}})
    voc = pd.DataFrame(voc_rows)

    # (C) n-gram signature: Claude vs pooled modern others
    cl_docs = [tokenize(t) for t in df[df.generator == CLAUDE]["completion"]]
    ot_docs = [tokenize(t) for t in df[df.generator != CLAUDE]["completion"]]
    sig = {}
    for n in (1, 2, 3):
        d = fightin_words(group_counts(cl_docs, n), group_counts(ot_docs, n))
        sig[n] = d

    lines = ["# Step 3 — AlpacaEval modern-model track\n",
             f"Records: {len(df)} across {len(gens)} sources "
             "(Claude self-gen vs 6 reused modern-ish models; no human).\n",
             "```", counts.to_string(), "```\n",
             "## (A) Claude vs pooled modern models — prose effect sizes "
             "(markdown stripped)\n",
             "Does the HC3-track signature replicate against modern models?\n",
             eff.head(12).round(2).to_markdown() + "\n",
             "## (B) GPT-excess vocabulary by source (per 1000 words), essay genre\n",
             "Where do delve/crucial/intricate land now that the genre fits them?\n",
             voc.round(3).to_markdown(index=False) + "\n",
             "## (C) Claude n-gram signature vs pooled modern models\n"]
    for n in (1, 2, 3):
        top = sig[n].head(15)[["term", "z", "claude_ct", "other_ct"]]
        lines.append(f"\n### {n}-gram — most Claude-like\n")
        lines.append(top.round(2).to_markdown(index=False) + "\n")

    with open(os.path.join(REPORTS, "alpaca_track.md"), "w") as f:
        f.write("\n".join(lines))

    print("records:\n", counts.to_string())
    print("\n(A) prose effects vs modern:\n", eff.head(10).round(2).to_string())
    print("\n(B) GPT-excess vocab:\n", voc.round(3).to_string(index=False))
    print("\n(C) top Claude 3-grams:",
          ", ".join(sig[3].head(12)["term"]))
    print("\nwrote reports/alpaca_track.md")


if __name__ == "__main__":
    main()
