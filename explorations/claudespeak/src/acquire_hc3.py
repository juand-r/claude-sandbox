"""Build the pilot prompt manifest + reused human/ChatGPT cells from HC3.

HC3 (Hello-SimpleAI/HC3) gives, per question: human_answers[] and
chatgpt_answers[] (GPT-3.5 era, early 2023), across 5 domains. We:
  1. stratified-sample 200 questions (40/domain, fixed seed) -> manifest,
  2. emit *reused* Records for the human answer and the old-ChatGPT answer,
  3. leave Claude/GPT-4o generation to generate_pilot.py (same questions).

This gives a topic-matched parallel corpus with a real human anchor.
"""
from __future__ import annotations

import json
import os
import random

from huggingface_hub import hf_hub_download

from schema import Record, append_records, CORPUS_DIR, REPO

DOMAINS = ["reddit_eli5", "finance", "open_qa", "medicine", "wiki_csai"]
PER_DOMAIN = 40
SEED = 42

# domain -> (our domain label, task_type)
DOMAIN_MAP = {
    "reddit_eli5": ("general", "explanation"),
    "finance": ("finance", "qa"),
    "open_qa": ("general", "qa"),
    "medicine": ("medicine", "qa"),
    "wiki_csai": ("cs_ai", "qa"),
}

MANIFEST = os.path.join(REPO, "data", "sources", "hc3_pilot_manifest.jsonl")
CORPUS = os.path.join(CORPUS_DIR, "pilot_hc3.jsonl")
HC3_VERSION = "Hello-SimpleAI/HC3@all.jsonl"


def load_hc3() -> list[dict]:
    p = hf_hub_download("Hello-SimpleAI/HC3", "all.jsonl", repo_type="dataset")
    rows = []
    with open(p, encoding="utf-8") as f:
        for pos, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            r["_rowpos"] = pos
            rows.append(r)
    return rows


def sample(rows: list[dict]) -> list[dict]:
    rng = random.Random(SEED)
    by_dom: dict[str, list[dict]] = {d: [] for d in DOMAINS}
    for r in rows:
        if (r.get("source") in by_dom
                and r.get("human_answers") and r.get("chatgpt_answers")
                and r["human_answers"][0].strip()
                and r["chatgpt_answers"][0].strip()):
            by_dom[r["source"]].append(r)
    picked = []
    for d in DOMAINS:
        pool = by_dom[d]
        rng.shuffle(pool)
        picked.extend(pool[:PER_DOMAIN])
    return picked


def build():
    rows = load_hc3()
    picked = sample(rows)
    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)

    manifest_lines = []
    records: list[Record] = []
    for r in picked:
        src = r["source"]
        domain, task_type = DOMAIN_MAP[src]
        pid = f"hc3-{src}-{r['_rowpos']}"
        question = r["question"]
        prompt_source = {"dataset": "HC3", "dataset_version": HC3_VERSION,
                         "original_id": r["_rowpos"], "split": src}

        manifest_lines.append(json.dumps({
            "prompt_id": pid, "prompt": question,
            "domain": domain, "task_type": task_type,
            "prompt_source": prompt_source,
        }, ensure_ascii=False))

        # reused: human anchor (first human answer)
        records.append(Record(
            prompt=question, prompt_id=pid,
            generator="human", generator_family="human", generator_version=None,
            source_type="human", completion=r["human_answers"][0],
            provenance="reused", prompt_source=prompt_source,
            reuse_source={"dataset": "HC3", "dataset_version": HC3_VERSION,
                          "original_id": r["_rowpos"], "field": "human_answers[0]",
                          "url": "https://huggingface.co/datasets/Hello-SimpleAI/HC3"},
            domain=domain, task_type=task_type,
            notes="Human answer scraped in HC3 (pre-2023); prompt-matched anchor.",
        ))
        # reused: old ChatGPT (GPT-3.5 era)
        records.append(Record(
            prompt=question, prompt_id=pid,
            generator="chatgpt-hc3", generator_family="openai",
            generator_version="gpt-3.5 (HC3, early 2023)",
            source_type="model", completion=r["chatgpt_answers"][0],
            provenance="reused", prompt_source=prompt_source,
            reuse_source={"dataset": "HC3", "dataset_version": HC3_VERSION,
                          "original_id": r["_rowpos"], "field": "chatgpt_answers[0]",
                          "url": "https://huggingface.co/datasets/Hello-SimpleAI/HC3"},
            domain=domain, task_type=task_type,
            notes="GPT-3.5-era ChatGPT answer from HC3; old-model baseline.",
        ))

    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest_lines) + "\n")
    append_records(CORPUS, records)
    print(f"manifest: {len(manifest_lines)} prompts -> {MANIFEST}")
    print(f"reused records: {len(records)} -> {CORPUS}")
    from collections import Counter
    print("by domain:", Counter(json.loads(l)["domain"] for l in manifest_lines))


if __name__ == "__main__":
    build()
