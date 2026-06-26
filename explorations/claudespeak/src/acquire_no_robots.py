"""Diversity track 2: No Robots (HuggingFaceH4/no_robots).

Human-written prompts AND human-written answers across 10 explicit categories
(Generation, Brainstorm, Open/Closed QA, Rewrite, Summarize, Coding, Classify,
Extract, Chat). Adds a HUMAN anchor on diverse task types (HC3 only had it for
informational QA). We take the first user->assistant exchange (single-turn),
stratify across categories, reuse the human answer, and queue Claude generation.
"""
from __future__ import annotations

import json
import os
import random
from collections import defaultdict

from huggingface_hub import hf_hub_download
import pandas as pd

from schema import Record, append_records, CORPUS_DIR, REPO

PER_CATEGORY_CAP = 150     # balance categories (take all of small ones)
SEED = 42
MANIFEST = os.path.join(REPO, "data", "sources", "norobots_manifest.jsonl")
CORPUS = os.path.join(CORPUS_DIR, "norobots_reused.jsonl")
DSV = "HuggingFaceH4/no_robots@train"


def first_exchange(messages):
    user, asst = None, None
    for m in messages:
        if m.get("role") == "user" and user is None:
            user = m.get("content", "")
        elif m.get("role") == "assistant" and user is not None:
            asst = m.get("content", "")
            break
    return user, asst


def build():
    p = hf_hub_download("HuggingFaceH4/no_robots",
                        "data/train-00000-of-00001.parquet", repo_type="dataset")
    df = pd.read_parquet(p)
    by_cat = defaultdict(list)
    seen = set()
    for _, r in df.iterrows():
        u, a = first_exchange(r["messages"])
        u = (u or "").strip(); a = (a or "").strip()
        if not u or not a or len(u) > 3000 or u.lower() in seen:
            continue
        seen.add(u.lower())
        by_cat[r["category"]].append((r["prompt_id"], u, a, r["category"]))

    rng = random.Random(SEED)
    picked = []
    for cat, items in by_cat.items():
        rng.shuffle(items)
        picked.extend(items[:PER_CATEGORY_CAP])
    rng.shuffle(picked)
    print("per-category picked:",
          {c: min(len(v), PER_CATEGORY_CAP) for c, v in by_cat.items()},
          "total", len(picked))

    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    manifest, records = [], []
    for pid_raw, prompt, answer, cat in picked:
        pid = f"norobots-{pid_raw[:16]}"
        psrc = {"dataset": "NoRobots", "dataset_version": DSV,
                "original_id": pid_raw, "split": "train"}
        manifest.append(json.dumps({"prompt_id": pid, "prompt": prompt,
                                    "domain": cat, "task_type": cat.lower(),
                                    "prompt_source": psrc}, ensure_ascii=False))
        records.append(Record(
            prompt=prompt, prompt_id=pid,
            generator="human", generator_family="human", generator_version=None,
            source_type="human", completion=answer, provenance="reused",
            prompt_source=psrc, domain=cat, task_type=cat.lower(),
            reuse_source={"dataset": "NoRobots", "dataset_version": DSV,
                          "original_id": pid_raw, "field": "messages.assistant[0]",
                          "url": "https://huggingface.co/datasets/HuggingFaceH4/no_robots"},
            notes="Human-written answer (No Robots annotator); diverse task type."))

    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest) + "\n")
    append_records(CORPUS, records)
    print(f"manifest: {len(manifest)} prompts -> {MANIFEST}")
    print(f"reused human cells: {len(records)} -> {CORPUS}")


if __name__ == "__main__":
    build()
