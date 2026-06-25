"""Step 5 (finale) — rusty-dawg / suffix-automaton mining.

Uses AI2's rusty-dawg (pip rusty_dawg) to build a DAWG over a reference token
stream and query arbitrary-length spans in O(len). Two analyses, per corpus track
(markdown-stripped prose, word-level tokens):

  (1) n-gram NOVELTY curves (leave-one-source-out): for each source S, build a
      DAWG over the pooled OTHER sources, then measure the fraction of S's n-grams
      (n=1..10) absent from that reference. Tracks how much each source recombines
      vs. invents spans (cf. Liu et al. 2024, "n-gram novelty via Rusty-DAWG").

  (2) Characteristic LONG spans (arbitrary-length Claudeisms): within each track,
      build a DAWG over pooled non-Claude prose, enumerate Claude's frequent
      4-8-grams, and surface those Claude repeats often but that NEVER occur in
      the reference — the exact multi-word templates unique to Claude.

Span membership uses the suffix-automaton rule: walking transition_and_count from
the initial state, the matched length must equal i+1 at step i (a string is a
substring iff its longest-suffix match spans its whole length).

Writes reports/ngram_dawg.md.
"""
from __future__ import annotations

import glob
import os
import random
import re
from collections import Counter

import pandas as pd
import rusty_dawg as rd

from schema import read_records, CORPUS_DIR, REPO
from analyze_ablation import strip_markdown

WORD = re.compile(r"[a-z']+")
REPORTS = os.path.join(REPO, "reports")
CLAUDE = "claude-opus-4-8"
SEP = 0                      # reserved doc separator (real tokens are >=1)
SAMPLE = 6000              # cap n-grams per (source,n) for novelty timing
RNG = random.Random(42)


def tok(text: str) -> list[str]:
    return WORD.findall(strip_markdown(text or "").lower())


def load_track(track_glob: str) -> dict[str, list[list[str]]]:
    by_gen: dict[str, list[list[str]]] = {}
    for p in sorted(glob.glob(os.path.join(CORPUS_DIR, track_glob))):
        for r in read_records(p):
            by_gen.setdefault(r["generator"], []).append(tok(r["completion"]))
    return by_gen


def build_dawg(docs_ids: list[list[int]]) -> rd.Dawg:
    stream = []
    for d in docs_ids:
        stream.extend(d)
        stream.append(SEP)
    d = rd.Dawg()
    d.build(stream)
    # NOTE: recompute_lengths() segfaults on large DAWGs and is NOT needed for
    # counting — get_count is correct after build() alone (verified on a toy
    # corpus: [2,3]->2, [2]->2, absent->0).
    return d


def span_count(dawg: rd.Dawg, span: list[int]) -> int:
    s, L = dawg.get_initial(), 0
    for i, t in enumerate(span):
        s, L = dawg.transition_and_count(s, t, L)
        if L != i + 1:
            return 0
    return dawg.get_count(s)


def ngrams(ids: list[int], n: int):
    return (tuple(ids[i:i + n]) for i in range(len(ids) - n + 1))


def novelty_curve(src_docs, ref_dawg, ns=(1, 2, 3, 4, 5, 6, 8, 10)) -> dict:
    out = {}
    for n in ns:
        grams = [g for d in src_docs for g in ngrams(d, n)]
        if not grams:
            out[n] = float("nan"); continue
        if len(grams) > SAMPLE:
            grams = RNG.sample(grams, SAMPLE)
        novel = sum(1 for g in grams if span_count(ref_dawg, list(g)) == 0)
        out[n] = novel / len(grams)
    return out


def run_track(name: str, by_gen: dict, vocab: dict):
    gens = sorted(by_gen)
    ids = {g: [[vocab[w] for w in doc] for doc in docs] for g, docs in by_gen.items()}

    # (1) leave-one-source-out novelty
    nov_rows = []
    for s in gens:
        ref_docs = [d for g in gens if g != s for d in ids[g]]
        ref = build_dawg(ref_docs)
        cur = novelty_curve(ids[s], ref)
        nov_rows.append({"source": s, **{f"n{n}": round(v, 3) for n, v in cur.items()}})
    nov = pd.DataFrame(nov_rows).set_index("source")

    # (2) characteristic long Claude spans vs pooled non-Claude reference
    ref_docs = [d for g in gens if g != CLAUDE for d in ids[g]]
    ref = build_dawg(ref_docs)
    inv = {v: k for k, v in vocab.items()}
    spans = []
    for n in (4, 5, 6, 7, 8):
        c = Counter(g for d in ids[CLAUDE] for g in ngrams(d, n))
        for span, ct in c.most_common(60):
            if ct >= 3 and span_count(ref, list(span)) == 0:
                spans.append((n, ct, " ".join(inv[t] for t in span)))
    spans.sort(key=lambda x: (-x[1], -x[0]))
    return nov, spans[:25]


def main():
    os.makedirs(REPORTS, exist_ok=True)
    tracks = {"HC3 (human-anchored)": "pilot_*.jsonl",
              "AlpacaEval (modern models)": "alpaca_*.jsonl"}
    lines = ["# Step 5 — rusty-dawg / suffix-automaton n-gram mining\n",
             "Markdown-stripped prose, word-level tokens. Built with AI2 "
             "rusty-dawg (pip rusty_dawg 0.2.2).\n"]
    for tname, g in tracks.items():
        by_gen = load_track(g)
        vocab = {}
        for docs in by_gen.values():
            for doc in docs:
                for w in doc:
                    if w not in vocab:
                        vocab[w] = len(vocab) + 1   # 0 reserved for SEP
        nov, spans = run_track(tname, by_gen, vocab)
        lines.append(f"\n## {tname}\n")
        lines.append("### n-gram novelty by source "
                     "(fraction of source n-grams absent from pooled others)\n")
        lines.append("Lower = more recombined-from-others; higher = more novel spans.\n")
        lines.append(nov.to_markdown() + "\n")
        lines.append("### Characteristic long Claude spans "
                     "(Claude count >=3, ZERO occurrences in pooled non-Claude)\n")
        sp = pd.DataFrame(spans, columns=["n", "claude_count", "span"])
        lines.append(sp.to_markdown(index=False) + "\n")
        print(f"\n=== {tname} ===")
        print("novelty:\n", nov.to_string())
        print("top characteristic Claude spans:")
        for n, ct, s in spans[:12]:
            print(f"  [{n}-gram x{ct}] {s}")

    with open(os.path.join(REPORTS, "ngram_dawg.md"), "w") as f:
        f.write("\n".join(lines))
    print("\nwrote reports/ngram_dawg.md")


if __name__ == "__main__":
    main()
