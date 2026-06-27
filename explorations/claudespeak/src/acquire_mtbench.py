"""Acquire the 80 MT-Bench questions (two turns each) as a prompt manifest.

MT-Bench (Zheng et al., 2023) is the standard multi-turn probe: 80 questions
across 8 categories, each with a first turn and a scripted follow-up. We only need
the questions here (no API); Claude is generated separately (generate_mtbench.py).
Writes data/sources/mtbench_manifest.jsonl with {prompt_id, category, turns:[t1,t2]}.
"""
from __future__ import annotations

import json
import os

from schema import REPO

MANIFEST = os.path.join(REPO, "data", "sources", "mtbench_manifest.jsonl")


def _normalize(row):
    """Return (qid, category, [turn1, turn2]) from whatever schema the source uses."""
    qid = row.get("question_id") or row.get("id") or row.get("prompt_id")
    cat = row.get("category") or row.get("cluster") or "unknown"
    turns = row.get("turns") or row.get("prompt") or row.get("conversation")
    if isinstance(turns, str):
        turns = [turns]
    # some variants store turns as list of {"content":...}
    turns = [t["content"] if isinstance(t, dict) else t for t in turns]
    return qid, cat, turns


def load_rows():
    """Try known HF sources in order; return list of normalized rows."""
    from datasets import load_dataset
    last = None
    for name, split in [("HuggingFaceH4/mt_bench_prompts", "train"),
                        ("philschmid/mt-bench", "train"),
                        ("lmsys/mt_bench_human_judgments", "human")]:
        try:
            ds = load_dataset(name, split=split)
            rows = [_normalize(r) for r in ds]
            rows = [r for r in rows if r[2] and len(r[2]) >= 1]
            if rows:
                print(f"loaded {len(rows)} rows from {name}:{split}")
                # de-dup by question text (the judgments set repeats questions)
                seen, uniq = set(), []
                for qid, cat, turns in rows:
                    key = turns[0][:120]
                    if key in seen:
                        continue
                    seen.add(key)
                    uniq.append((qid, cat, turns))
                return uniq
        except Exception as e:  # noqa: BLE001 -- probing multiple sources
            last = f"{name}: {type(e).__name__} {str(e)[:120]}"
            print("  miss", last)
    raise RuntimeError(f"no MT-Bench source loaded; last error: {last}")


def build():
    rows = load_rows()
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    n = 0
    with open(MANIFEST, "w", encoding="utf-8") as f:
        for qid, cat, turns in rows:
            pid = f"mtbench-{qid}"
            f.write(json.dumps({"prompt_id": pid, "category": cat,
                                "turns": turns[:2],
                                "prompt_source": {"dataset": "MT-Bench",
                                                  "original_id": qid,
                                                  "category": cat}},
                               ensure_ascii=False) + "\n")
            n += 1
    print(f"wrote {n} MT-Bench prompts -> {MANIFEST}")
    by_cat = {}
    for _, cat, _ in rows:
        by_cat[cat] = by_cat.get(cat, 0) + 1
    print("by category:", by_cat)


if __name__ == "__main__":
    build()
