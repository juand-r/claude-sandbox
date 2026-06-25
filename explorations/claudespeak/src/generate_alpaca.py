"""Generate Claude Opus 4.8 over the AlpacaEval pilot manifest (Step 3).
Same config as the HC3 track (effort=high, max_tokens 8000) for comparability.
Resumable / crash-safe (immediate append, skip done). GPT contrast is already
covered by the two reused GPT models, so we self-generate Claude only here.
"""
from __future__ import annotations

import json
import os
import sys
import time

from schema import read_records, append_records, CORPUS_DIR, REPO
from generate import generate_claude

MANIFEST = os.path.join(REPO, "data", "sources", "alpaca_pilot_manifest.jsonl")
OUT = os.path.join(CORPUS_DIR, "alpaca_generated.jsonl")
GEN = "claude-opus-4-8"


def done() -> set:
    if not os.path.exists(OUT):
        return set()
    return {(r["prompt_id"], r["generator"]) for r in read_records(OUT)}


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        prompts = [json.loads(l) for l in f if l.strip()]
    have = done()
    todo = [p for p in prompts if (p["prompt_id"], GEN) not in have]
    print(f"{len(prompts)} prompts; {len(have)} done; {len(todo)} to generate.")
    ok = 0
    for i, item in enumerate(todo, 1):
        for attempt in range(4):
            try:
                rec = generate_claude(
                    item["prompt"], item["prompt_id"], model=GEN,
                    effort="high", max_tokens=8000,
                    prompt_source=item["prompt_source"],
                    domain=item["domain"], task_type=item["task_type"])
                append_records(OUT, [rec])
                ok += 1
                break
            except Exception as e:
                w = 2 ** (attempt + 1)
                print(f"  [{i}/{len(todo)}] {item['prompt_id']} err "
                      f"{type(e).__name__}: {str(e)[:100]} -> {w}s", file=sys.stderr)
                time.sleep(w)
        if i % 25 == 0:
            print(f"  ...{i}/{len(todo)} ({ok} ok)")
    print(f"finished: {ok}/{len(todo)} -> {OUT}")


if __name__ == "__main__":
    main()
