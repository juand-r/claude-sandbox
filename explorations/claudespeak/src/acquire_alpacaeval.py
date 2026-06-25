"""Step 3 — AlpacaEval modern-model track.

Reuse published AlpacaEval completions for several models on the *same*
instructions (keyed by instruction TEXT — the per-model files are NOT in a shared
row order), then generate Claude on the same prompts (generate step separate).

Models reused (vintage noted; these are the AlpacaEval-published outputs, so
"modern-ish" rather than absolute latest):
  gpt-4-turbo-2024-04-09, gpt-4o-2024-05-13 (openai),
  gemini-pro (google), deepseek-llm-67b-chat (deepseek),
  Qwen2-72B-Instruct (qwen), Meta-Llama-3-70B-Instruct (meta).

No human cell in this track (AlpacaEval has none) — by design; HC3 track carries
the human anchor.
"""
from __future__ import annotations

import hashlib
import json
import os
import random

import requests

from schema import Record, append_records, CORPUS_DIR, REPO

RAW = "https://raw.githubusercontent.com/tatsu-lab/alpaca_eval/main/results/{}/model_outputs.json"
MODELS = {
    "gpt-4-turbo-2024-04-09": "openai",
    "gpt-4o-2024-05-13": "openai",
    "gemini-pro": "google",
    "deepseek-llm-67b-chat": "deepseek",
    "Qwen2-72B-Instruct": "qwen",
    "Meta-Llama-3-70B-Instruct": "meta",
}
N = 200
SEED = 42
MANIFEST = os.path.join(REPO, "data", "sources", "alpaca_pilot_manifest.jsonl")
CORPUS = os.path.join(CORPUS_DIR, "alpaca_reused.jsonl")
DSV = "tatsu-lab/alpaca_eval@results (github main)"


def fetch(model: str) -> dict:
    r = requests.get(RAW.format(model), timeout=120)
    r.raise_for_status()
    return {row["instruction"]: row for row in r.json()}


def pid(instruction: str) -> str:
    return "alpaca-" + hashlib.md5(instruction.encode()).hexdigest()[:10]


def build():
    per_model = {m: fetch(m) for m in MODELS}
    # instructions present in ALL models (key by text)
    common = set.intersection(*(set(d) for d in per_model.values()))
    common = sorted(common)
    rng = random.Random(SEED)
    rng.shuffle(common)
    picked = common[:N]
    print(f"common instructions: {len(common)}; sampling {len(picked)}")

    os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
    manifest, records = [], []
    for inst in picked:
        p = pid(inst)
        # AlpacaEval 'dataset' tag (helpful_base/koala/oasst/selfinstruct/vicuna)
        tag = per_model[next(iter(MODELS))][inst].get("dataset", "alpaca_eval")
        prompt_source = {"dataset": "AlpacaEval", "dataset_version": DSV,
                         "original_id": p, "split": tag}
        manifest.append(json.dumps({
            "prompt_id": p, "prompt": inst, "domain": tag,
            "task_type": "instruction", "prompt_source": prompt_source},
            ensure_ascii=False))
        for model, family in MODELS.items():
            row = per_model[model][inst]
            records.append(Record(
                prompt=inst, prompt_id=p,
                generator=model, generator_family=family,
                generator_version=row.get("generator", model),
                source_type="model", completion=row["output"],
                provenance="reused", prompt_source=prompt_source,
                reuse_source={"dataset": "AlpacaEval", "dataset_version": DSV,
                              "model_dir": model, "field": "output",
                              "url": RAW.format(model)},
                domain=tag, task_type="instruction",
                notes="AlpacaEval-published output; reused (vintage per model dir)."))

    with open(MANIFEST, "w", encoding="utf-8") as f:
        f.write("\n".join(manifest) + "\n")
    append_records(CORPUS, records)
    print(f"manifest: {len(manifest)} prompts -> {MANIFEST}")
    print(f"reused records: {len(records)} ({len(MODELS)} models) -> {CORPUS}")


if __name__ == "__main__":
    build()
