"""Generate Claude over MT-Bench (multi-turn track, Exp C1).

For each of the 80 MT-Bench questions we generate Claude's turn-1 answer, then its
turn-2 answer conditioned on the real follow-up. This lets us ask whether the
fingerprint (burstiness, density, em-dash, offer-closer, etc.) intensifies,
attenuates, or shifts from turn 1 to turn 2 -- the offer-to-continue closer in
particular is a turn-final move whose role may change across turns.

Records share conversation_id = prompt_id with turn_index 0 (first answer) and 1
(follow-up answer); the reasoning trace is captured per turn (thinking_text).
Concurrent across questions, sequential within a question, resumable. NEEDS API
CREDITS. Cost (rough): 80 x 2 = 160 Claude calls with thinking on.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from schema import read_records, append_records, CORPUS_DIR, REPO
from generate import generate_claude_chat, _anthropic

MANIFEST = os.path.join(REPO, "data", "sources", "mtbench_manifest.jsonl")
OUT = os.path.join(CORPUS_DIR, "mtbench_generated.jsonl")
MODEL = "claude-opus-4-8"
EFFORT = "high"
MAX_TOKENS = 4096
WORKERS = 6

_lock = threading.Lock()


def done() -> dict:
    if not os.path.exists(OUT):
        return {}
    counts = {}
    for r in read_records(OUT):
        counts[r["conversation_id"]] = counts.get(r["conversation_id"], 0) + 1
    return counts


def _gen(messages, q, turn):
    for attempt in range(4):
        try:
            return generate_claude_chat(
                messages, prompt_id=f"{q['prompt_id']}-t{turn}",
                model=MODEL, effort=EFFORT, max_tokens=MAX_TOKENS,
                conversation_id=q["prompt_id"], turn_index=turn,
                prompt_source=q["prompt_source"], domain="mtbench",
                task_type=q["category"], notes=f"MT-Bench turn {turn}")
        except Exception as e:
            time.sleep(2 ** (attempt + 1))
            if attempt == 3:
                print(f"  GAVE UP {q['prompt_id']} t{turn}: {type(e).__name__} "
                      f"{str(e)[:100]}", file=sys.stderr)
    return None


def work(q) -> bool:
    """Generate both turns for one question; append atomically per turn."""
    t1, t2 = q["turns"][0], q["turns"][1]
    r0 = _gen([{"role": "user", "content": t1}], q, 0)
    if r0 is None:
        return False
    with _lock:
        append_records(OUT, [r0])
    msgs = [{"role": "user", "content": t1},
            {"role": "assistant", "content": r0.completion},
            {"role": "user", "content": t2}]
    r1 = _gen(msgs, q, 1)
    if r1 is None:
        return False
    with _lock:
        append_records(OUT, [r1])
    return True


def main():
    qs = [json.loads(l) for l in open(MANIFEST, encoding="utf-8") if l.strip()]
    have = done()
    todo = [q for q in qs if have.get(q["prompt_id"], 0) < 2]
    print(f"{len(qs)} questions; {len(qs) - len(todo)} complete; {len(todo)} to "
          f"generate ({WORKERS} workers, 2 turns each).")
    _anthropic()
    ok = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(work, q): q for q in todo}
        for i, fut in enumerate(as_completed(futs), 1):
            if fut.result():
                ok += 1
            if i % 20 == 0:
                print(f"  ...{i}/{len(todo)} questions done ({ok} ok)")
    print(f"finished: {ok}/{len(todo)} -> {OUT}")


if __name__ == "__main__":
    main()
