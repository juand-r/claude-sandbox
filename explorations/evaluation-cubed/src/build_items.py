"""
Stage 1: build the item pool.

Each item is an open-ended factual question plus N=6 *atomic* claims that a good answer
should contain. For every claim we also generate a minimally-corrupted variant that is
plausible but false (a wrong number, date, name, or reversed relation).

Why this shape: it lets us construct systems whose true quality is known by construction
(swap k claims for their corrupted variants) rather than known by annotation. That removes
the human-label bottleneck that makes level-2 and level-3 studies impractical.

Output: data/items.json
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm import Job, chat, extract_json, run_many, usage_report  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

GEN_MODEL = "gpt-5.4"
N_CLAIMS = 6

TOPICS = [
    "classical and medieval history", "20th century political history",
    "physical geography", "human geography and demographics",
    "cell biology", "evolutionary biology", "human physiology",
    "classical mechanics", "thermodynamics", "electromagnetism",
    "astronomy and planetary science", "geology and earth science",
    "inorganic chemistry", "organic chemistry",
    "computer architecture", "algorithms and data structures",
    "computer networking", "cryptography",
    "macroeconomics", "microeconomics",
    "music theory and music history", "art history",
    "linguistics", "philosophy of science",
    "statistics and probability", "number theory",
    "materials science", "aviation and aerospace",
    "medicine and pharmacology", "ecology and climate",
    "world literature", "architecture and civil engineering",
]

PROMPT = """You are building a benchmark of factual questions with decomposable answers.

Topic: {topic}
Produce {n_items} DISTINCT items on this topic.

For each item:
1. Write an open-ended question that invites a short expository answer (2-5 sentences),
   the kind a person would ask an assistant. Not a yes/no question.
2. Write exactly {n_claims} atomic claims that a good answer to that question should
   contain. Each claim must be:
   - a single, self-contained, indisputably TRUE statement of well-established fact,
   - specific: it should pin down a number, date, name, mechanism, or relation,
   - independently checkable, and not entailed by any other claim in the list,
   - one sentence, no more than about 25 words.
3. For each claim write a CORRUPTED variant. The corruption must be:
   - MINIMAL: change one number, date, name, direction, or relation,
   - PLAUSIBLE: a well-read non-expert should not immediately notice it is wrong,
   - definitely FALSE,
   - the same length and register as the original, and it must still read as a confident
     factual assertion. Do not add hedging words.
   Label each corruption with its type, one of:
   "quantity" (a number or magnitude), "date", "entity" (a name, place, or agent),
   "relation" (direction of a causal or logical relation, or which of two things does
   what), "mechanism" (the stated process is replaced by a different one).
   ACROSS the {n_claims} claims of an item, use at least THREE different corruption types.
   Do not make an item whose corruptions are all dates or all quantities.

Avoid anything contested, recent (post-2020), or subject to reasonable disagreement.

Return ONLY a JSON array, no prose:
[
  {{"question": "...",
    "claims": [{{"true": "...", "false": "...", "type": "date"}}, ... {n_claims} of them]}},
  ...
]"""

VERIFY_PROMPT = """You are a meticulous fact checker. For each numbered pair below, decide
whether statement A is true and statement B is false.

{pairs}

Return ONLY a JSON array with one object per pair:
[{{"i": 1, "a_true": true/false, "b_false": true/false, "note": "<=15 words"}}, ...]"""


def gen_topic(topic: str, n_items: int) -> list[dict]:
    txt = chat(
        GEN_MODEL,
        [{"role": "user", "content": PROMPT.format(topic=topic, n_items=n_items, n_claims=N_CLAIMS)}],
        max_tokens=8000,
        reasoning_effort="medium",
    )
    out = extract_json(txt)
    keep = []
    for it in out:
        if not isinstance(it, dict):
            continue
        cl = it.get("claims", [])
        if len(cl) != N_CLAIMS:
            continue
        if not all(isinstance(c, dict) and c.get("true") and c.get("false") for c in cl):
            continue
        it["topic"] = topic
        keep.append(it)
    return keep


def verify_item(item: dict) -> list[dict]:
    """Independent check that each `true` claim is true and each `false` claim is false."""
    pairs = "\n".join(
        f"{i+1}. A: {c['true']}\n   B: {c['false']}" for i, c in enumerate(item["claims"])
    )
    txt = chat(
        "gpt-5.4",
        [{"role": "user", "content": VERIFY_PROMPT.format(pairs=pairs)}],
        max_tokens=4000,
        reasoning_effort="medium",
    )
    return extract_json(txt)


def main(items_per_topic: int = 2, n_topics: int = 32) -> None:
    topics = TOPICS[:n_topics]
    print(f"generating {items_per_topic} items x {len(topics)} topics ...")
    jobs = [Job(fn=(lambda t=t: gen_topic(t, items_per_topic))) for t in topics]
    batches = run_many(jobs, workers=16, desc="gen")

    items = []
    for b in batches:
        items.extend(b)
    for i, it in enumerate(items):
        it["id"] = f"it{i:04d}"
    print(f"generated {len(items)} raw items")

    print("verifying claim polarity ...")
    vjobs = [Job(fn=(lambda it=it: verify_item(it))) for it in items]
    verdicts = run_many(vjobs, workers=16, desc="verify")

    clean, dropped_claims, dropped_items = [], 0, 0
    for it, ver in zip(items, verdicts):
        ok = {v["i"] - 1 for v in ver if v.get("a_true") and v.get("b_false")}
        kept = [c for j, c in enumerate(it["claims"]) if j in ok]
        dropped_claims += len(it["claims"]) - len(kept)
        if len(kept) < N_CLAIMS:
            dropped_items += 1
            continue  # keep only items where all 6 claim pairs survive verification
        it["claims"] = kept
        clean.append(it)

    for i, it in enumerate(clean):
        it["id"] = f"it{i:04d}"

    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, "items.json")
    with open(path, "w") as f:
        json.dump(clean, f, indent=1, ensure_ascii=False)
    print(f"kept {len(clean)} items ({dropped_items} items dropped, "
          f"{dropped_claims} claim-pairs failed verification) -> {path}")
    print(usage_report())


if __name__ == "__main__":
    n_per = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    n_top = int(sys.argv[2]) if len(sys.argv) > 2 else 32
    main(n_per, n_top)
