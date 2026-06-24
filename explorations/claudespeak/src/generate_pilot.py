"""Generate the self-produced pilot cells (Claude Opus 4.8 + GPT-4o) over the
HC3 pilot manifest. Crash-safe and resumable: each successful generation is
appended immediately, and already-completed (prompt_id, generator) pairs are
skipped on rerun. Safe against the ephemeral environment being reclaimed.

Cost note (logged before running): 200 prompts x 2 models. Claude high-effort
~$10, GPT-4o ~$1-2. See PLAN.md S9.
"""
from __future__ import annotations

import json
import os
import sys
import time

from schema import read_records, append_records, CORPUS_DIR, REPO
from generate import generate_claude, generate_openai

MANIFEST = os.path.join(REPO, "data", "sources", "hc3_pilot_manifest.jsonl")
OUT = os.path.join(CORPUS_DIR, "pilot_generated.jsonl")

# (generator label, callable) — the cells we self-generate.
TARGETS = [
    ("claude-opus-4-8", lambda p, pid, ps, dom, tt: generate_claude(
        p, pid, model="claude-opus-4-8", effort="high", max_tokens=8000,
        prompt_source=ps, domain=dom, task_type=tt)),
    ("gpt-4o", lambda p, pid, ps, dom, tt: generate_openai(
        p, pid, model="gpt-4o", temperature=1.0, max_tokens=2048,
        prompt_source=ps, domain=dom, task_type=tt)),
]


def done_pairs() -> set[tuple[str, str]]:
    if not os.path.exists(OUT):
        return set()
    return {(r["prompt_id"], r["generator"]) for r in read_records(OUT)}


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        prompts = [json.loads(l) for l in f if l.strip()]
    done = done_pairs()
    todo = [(item, gen, fn) for item in prompts for (gen, fn) in TARGETS
            if (item["prompt_id"], gen) not in done]
    print(f"{len(prompts)} prompts x {len(TARGETS)} models; "
          f"{len(done)} already done; {len(todo)} to generate.")

    n_ok = 0
    for i, (item, gen, fn) in enumerate(todo, 1):
        pid = item["prompt_id"]
        for attempt in range(4):
            try:
                rec = fn(item["prompt"], pid, item["prompt_source"],
                         item["domain"], item["task_type"])
                append_records(OUT, [rec])  # immediate persist
                n_ok += 1
                break
            except Exception as e:
                wait = 2 ** (attempt + 1)
                print(f"  [{i}/{len(todo)}] {gen} {pid} error: "
                      f"{type(e).__name__}: {str(e)[:120]} -> retry in {wait}s",
                      file=sys.stderr)
                time.sleep(wait)
        else:
            print(f"  GAVE UP on {gen} {pid}", file=sys.stderr)
        if i % 20 == 0:
            print(f"  ...{i}/{len(todo)} done ({n_ok} ok)")
    print(f"finished: {n_ok}/{len(todo)} new records -> {OUT}")


if __name__ == "__main__":
    main()
