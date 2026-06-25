"""Lexical reconciliation: who actually uses the "LLM tic" words?

Motivated by the apparent contradiction in the pilot ("lexical tics don't
separate Claude"). The literature attributes the famous tic vocabulary
(delve, crucial, intricate, ...) to ChatGPT/GPT, not Claude. This script
measures, per source, the frequency of:
  (A) GPT/ChatGPT-associated "excess vocabulary" (Kobak et al. 2024), and
  (B) Claude-associated subjective/casual markers (Trial-Error-Explain ICL, 2025).

Writes data/corpus/lexicon_by_source.csv and prints both tables.
"""
from __future__ import annotations

import glob
import os
import re
from collections import Counter, defaultdict

import pandas as pd

from schema import read_records, CORPUS_DIR

WORD = re.compile(r"[a-z']+")

# (A) Kobak et al. 2024 "excess vocabulary" — ChatGPT-associated style words.
GPT_EXCESS = ["delve", "delves", "delving", "intricate", "showcasing",
              "showcase", "underscore", "underscores", "crucial", "pivotal",
              "comprehensive", "meticulous", "meticulously", "notably",
              "realm", "robust", "seamless", "leverage", "essential", "potential"]

# (B) Claude-associated subjective/casual markers (per the Claude-vs-GPT-4o study)
#     plus discourse markers we saw lead in the pilot.
CLAUDE_CASUAL = ["believe", "feel", "think", "actually", "really", "probably"]
CLAUDE_PHRASES = ["it's worth", "kind of", "things like", "feel that", "a bit"]


def main():
    counts = defaultdict(Counter)
    tot = defaultdict(int)
    txt = defaultdict(str)
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, "pilot_*.jsonl"))):
        for r in read_records(p):
            g = r["generator"]
            t = (r["completion"] or "").lower()
            toks = WORD.findall(t)
            counts[g].update(toks)
            tot[g] += len(toks)
            txt[g] += " " + t
    gens = sorted(counts)

    rows = []
    for w in GPT_EXCESS:
        rows.append({"set": "GPT-excess (Kobak)", "term": w,
                     **{g: round(1000 * counts[g][w] / tot[g], 3) for g in gens}})
    for w in CLAUDE_CASUAL:
        rows.append({"set": "Claude-casual", "term": w,
                     **{g: round(1000 * counts[g][w] / tot[g], 3) for g in gens}})
    for ph in CLAUDE_PHRASES:
        rows.append({"set": "Claude-casual", "term": ph,
                     **{g: round(1000 * txt[g].count(ph) / tot[g], 3) for g in gens}})

    df = pd.DataFrame(rows)
    out = os.path.join(CORPUS_DIR, "lexicon_by_source.csv")
    df.to_csv(out, index=False)
    pd.set_option("display.width", 140)
    print("per-1000-words frequency by source:\n")
    print(df.to_string(index=False))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
