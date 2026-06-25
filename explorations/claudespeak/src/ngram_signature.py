"""Step 1 — data-driven Claude n-gram signature.

Which 1/2/3-grams are genuinely over-represented in Claude vs others?
Method: Monroe, Colaresi & Quinn (2008) "Fightin' Words" — log-odds ratio with
an informative Dirichlet prior, z-scored. The prior (background = pooled corpus)
regularizes rare terms so the ranking isn't dominated by hapax noise.

z_w = delta_w / sqrt(var_w), where
  delta_w = log[(y_A+a_w)/(n_A+a0-y_A-a_w)] - log[(y_B+a_w)/(n_B+a0-y_B-a_w)]
  var_w   = 1/(y_A+a_w) + 1/(y_B+a_w)
  a_w     = kappa * p_background(w),  a0 = sum_w a_w = kappa

Positive z = more Claude-like. We report top/bottom terms per n and per contrast.
Run on markdown-stripped prose by default (lexical voice, not formatting).
"""
from __future__ import annotations

import glob
import math
import os
import re
from collections import Counter

import pandas as pd

from schema import read_records, CORPUS_DIR, REPO
from analyze_ablation import strip_markdown

WORD = re.compile(r"[a-z']+")
REPORTS = os.path.join(REPO, "reports")
CLAUDE = "claude-opus-4-8"
KAPPA = 500.0          # total prior mass
MIN_TOTAL = 5          # ignore n-grams seen < this many times overall


def tokenize(text: str) -> list[str]:
    return WORD.findall(strip_markdown(text or "").lower())


def ngrams(tokens: list[str], n: int) -> list[str]:
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def group_counts(docs: list[list[str]], n: int) -> Counter:
    c = Counter()
    for toks in docs:
        c.update(ngrams(toks, n))
    return c


def fightin_words(ca: Counter, cb: Counter, n_min_total: int = MIN_TOTAL):
    bg = ca + cb
    bg = Counter({w: v for w, v in bg.items() if v >= n_min_total})
    total_bg = sum(bg.values())
    a0 = KAPPA
    na = sum(ca[w] for w in bg)
    nb = sum(cb[w] for w in bg)
    rows = []
    for w, tot in bg.items():
        a_w = a0 * (tot / total_bg)
        ya, yb = ca.get(w, 0), cb.get(w, 0)
        la = math.log((ya + a_w) / (na + a0 - ya - a_w))
        lb = math.log((yb + a_w) / (nb + a0 - yb - a_w))
        delta = la - lb
        var = 1.0 / (ya + a_w) + 1.0 / (yb + a_w)
        z = delta / math.sqrt(var)
        rows.append((w, z, ya, yb, tot))
    df = pd.DataFrame(rows, columns=["term", "z", "claude_ct", "other_ct", "total_ct"])
    return df.sort_values("z", ascending=False)


def load_docs():
    by_gen = {}
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, "pilot_*.jsonl"))):
        for r in read_records(p):
            by_gen.setdefault(r["generator"], []).append(tokenize(r["completion"]))
    return by_gen


def main():
    os.makedirs(REPORTS, exist_ok=True)
    by_gen = load_docs()
    claude = by_gen[CLAUDE]
    pooled_others = [d for g, docs in by_gen.items() if g != CLAUDE for d in docs]
    gpt4o = by_gen.get("gpt-4o", [])

    contrasts = {
        "claude_vs_pooled": (claude, pooled_others),
        "claude_vs_gpt4o": (claude, gpt4o),
    }
    out_lines = ["# Step 1 — Claude n-gram signature (Fightin' Words log-odds)\n",
                 "Markdown stripped; z>0 = more Claude. Prior kappa="
                 f"{KAPPA:.0f}, min total count {MIN_TOTAL}.\n"]
    all_csv = []
    for cname, (A, B) in contrasts.items():
        out_lines.append(f"\n## Contrast: {cname}\n")
        for n in (1, 2, 3):
            ca = group_counts(A, n)
            cb = group_counts(B, n)
            df = fightin_words(ca, cb)
            df["contrast"], df["n"] = cname, n
            all_csv.append(df)
            top = df.head(20)[["term", "z", "claude_ct", "other_ct"]]
            bot = df.tail(12)[["term", "z", "claude_ct", "other_ct"]].iloc[::-1]
            out_lines.append(f"\n### {n}-gram — most Claude-like\n")
            out_lines.append(top.round(2).to_markdown(index=False) + "\n")
            out_lines.append(f"\n### {n}-gram — least Claude-like (anti-signature)\n")
            out_lines.append(bot.round(2).to_markdown(index=False) + "\n")
            print(f"[{cname} {n}-gram] top:",
                  ", ".join(top["term"].head(10)))

    pd.concat(all_csv).to_csv(
        os.path.join(CORPUS_DIR, "ngram_signature_scores.csv"), index=False)
    with open(os.path.join(REPORTS, "claude_ngram_signature.md"), "w") as f:
        f.write("\n".join(out_lines))
    print("\nwrote reports/claude_ngram_signature.md + ngram_signature_scores.csv")


if __name__ == "__main__":
    main()
