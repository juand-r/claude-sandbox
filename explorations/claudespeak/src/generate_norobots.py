"""Generate Claude Opus 4.8 over the No Robots diversity manifest.
Concurrent (thread pool), resumable, thread-safe appends.
Same config as other tracks (effort=high, max_tokens 8000) for comparability.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from schema import read_records, append_records, CORPUS_DIR, REPO
from generate import generate_claude, _anthropic

MANIFEST = os.path.join(REPO, "data", "sources", "norobots_manifest.jsonl")
OUT = os.path.join(CORPUS_DIR, "norobots_generated.jsonl")
GEN = "claude-opus-4-8"
WORKERS = 8

_lock = threading.Lock()


def done() -> set:
    if not os.path.exists(OUT):
        return set()
    return {(r["prompt_id"], r["generator"]) for r in read_records(OUT)}


def work(item) -> bool:
    for attempt in range(4):
        try:
            rec = generate_claude(item["prompt"], item["prompt_id"], model=GEN,
                                  effort="high", max_tokens=8000,
                                  prompt_source=item["prompt_source"])
            with _lock:
                append_records(OUT, [rec])
            return True
        except Exception as e:
            time.sleep(2 ** (attempt + 1))
            if attempt == 3:
                print(f"  GAVE UP {item['prompt_id']}: {type(e).__name__} "
                      f"{str(e)[:100]}", file=sys.stderr)
    return False


def main():
    with open(MANIFEST, encoding="utf-8") as f:
        prompts = [json.loads(l) for l in f if l.strip()]
    have = done()
    todo = [p for p in prompts if (p["prompt_id"], GEN) not in have]
    print(f"{len(prompts)} prompts; {len(have)} done; {len(todo)} to generate "
          f"({WORKERS} workers).")
    _anthropic()
    ok = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(work, p): p for p in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            if fut.result():
                ok += 1
            if i % 100 == 0:
                print(f"  ...{i}/{len(todo)} done ({ok} ok)")
    print(f"finished: {ok}/{len(todo)} -> {OUT}")


if __name__ == "__main__":
    main()
