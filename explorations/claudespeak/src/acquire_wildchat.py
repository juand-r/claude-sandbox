"""Diversity track: sample real, diverse single-turn prompts from WildChat-1M.

WildChat is real user<->ChatGPT logs. We take the first USER message as the
prompt and reuse the assistant (GPT-4-0314) reply as a free contrast cell; Claude
is generated separately (generate_wildchat.py). Filters: English, single-turn,
non-toxic, non-redacted, sensible length, deduped. This buys prompt diversity and
scale that HC3/AlpacaEval lack.
"""
from __future__ import annotations

import json
import os
import random

from huggingface_hub import hf_hub_download
import pandas as pd

from schema import Record, append_records, CORPUS_DIR, REPO

N = 1500
SEED = 42
GPT_MODEL = "gpt-4-0314"
SHARDS = ["data/train-00000-of-00014.parquet", "data/train-00001-of-00014.parquet"]
MANIFEST = os.path.join(REPO, "data", "sources", "wildchat_manifest.jsonl")
CORPUS = os.path.join(CORPUS_DIR, "wildchat_reused.jsonl")
DSV = "allenai/WildChat-1M"


def first_exchange(conv):
    """Return (user_prompt, assistant_reply) from the first turn, or None."""
    if conv is None or len(conv) < 2:
        return None
    u, a = conv[0], conv[1]
    if u.get("role") != "user" or a.get("role") != "assistant":
        return None
    return u.get("content", ""), a.get("content", "")


def build():
    frames = []
    for sh in SHARDS:
        p = hf_hub_download("allenai/WildChat-1M", sh, repo_type="dataset")
        frames.append(pd.read_parquet(p, columns=[
            "conversation_hash", "model", "conversation", "turn",
            "language", "toxic", "redacted", "country"]))
    df = pd.concat(frames, ignore_index=True)
    df = df[(df.language == "English") & (df.model == GPT_MODEL)
            & (~df.toxic) & (~df.redacted) & (df.turn == 1)]
    print(f"after filters: {len(df)} candidate conversations")

    seen, pool = set(), []
    for _, r in df.iterrows():
        ex = first_exchange(r["conversation"])
        if not ex:
            continue
        prompt, reply = ex
        prompt = (prompt or "").strip()
        reply = (reply or "").strip()
        key = prompt.lower()
        if not (10 <= len(prompt) <= 2000) or not reply or key in seen:
            continue
        seen.add(key)
        pool.append((r["conversation_hash"], prompt, reply, r["model"]))
    print(f"unique usable prompts: {len(pool)}")

    rng = random.Random(SEED)
    rng.shuffle(pool)
    picked = pool[:N]

    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    manifest, records = [], []
    for chash, prompt, reply, model in picked:
        pid = f"wildchat-{chash[:16]}"
        psrc = {"dataset": "WildChat", "dataset_version": DSV,
                "original_id": chash, "split": "train"}
        manifest.append(json.dumps({"prompt_id": pid, "prompt": prompt,
                                    "domain": None, "task_type": None,
                                    "prompt_source": psrc}, ensure_ascii=False))
        records.append(Record(
            prompt=prompt, prompt_id=pid,
            generator="gpt-4-0314", generator_family="openai",
            generator_version=model, source_type="model", completion=reply,
            provenance="reused", prompt_source=psrc,
            reuse_source={"dataset": "WildChat", "dataset_version": DSV,
                          "original_id": chash, "field": "conversation[1]",
                          "url": "https://huggingface.co/datasets/allenai/WildChat-1M"},
            notes="WildChat assistant reply (GPT-4-0314, 2023); reused contrast."))

    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest) + "\n")
    append_records(CORPUS, records)
    print(f"manifest: {len(manifest)} prompts -> {MANIFEST}")
    print(f"reused GPT cells: {len(records)} -> {CORPUS}")


if __name__ == "__main__":
    build()
