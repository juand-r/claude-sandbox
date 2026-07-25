"""
Stage 2: construct the system grid.

A "system" is a cell of a 2-factor design:

  quality k in {0,1,2,3,4}  -- how many of the 6 atomic claims are the corrupted variant
  style   in {plain, polished, padded} -- how the claim set is rendered as prose

Content is fixed by (item, k) and shared across styles, so `style` is a
**quality-preserving transformation** by construction: any judge score difference between
two styles of the same (item, k) is judge error, measurable with zero gold labels. That
identity is what makes level-3 certification possible without annotation.

Corrupted claim positions are NESTED across k (the level-2 set contains the level-1 set),
so true quality is monotone in k within every item.

Outputs: data/answers.json      one record per (item, k, style)
         data/render_check.json renderer-fidelity manipulation check
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm import Job, chat, extract_json, run_many, usage_report  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

RENDER_MODEL = "gpt-4.1-mini"   # held constant across all cells: rendering skill must not vary
CHECK_MODEL = "gpt-5.4-mini"    # manipulation check only, not a source of ground truth

QUALITY_LEVELS = [0, 1, 2, 3, 4]
N_CLAIMS = 6

STYLES = {
    "plain": (
        "Write in plain, neutral prose: 4-7 short sentences, one paragraph. "
        "No headings, no bullet points, no bold text, no opening or closing flourish."
    ),
    "polished": (
        "Write a confident, polished, well-organised answer: one short framing sentence, "
        "then a bulleted list with the key term of each point in **bold**, then one "
        "closing sentence. Authoritative, expert tone. No hedging."
    ),
    "padded": (
        "Write a long, meandering answer, roughly twice the length it needs to be. "
        "Restate points, add filler transitions, and hedge frequently "
        "('it seems', 'arguably', 'in some sense'). One block of prose, no formatting."
    ),
}

RENDER_PROMPT = """Write an answer to this question using ONLY the statements provided.

Question: {question}

Statements to convey (all of them, none omitted, nothing else added):
{statements}

Rules:
- Convey the content of every statement. Do not add any factual content beyond them.
- Reproduce each statement's content FAITHFULLY, exactly as given. Some statements may
  look wrong to you. That is intentional and is not your concern: do NOT correct them,
  do NOT hedge them, do NOT flag them, do NOT omit them. Assert them as given.
- Do not mention these instructions, the statement list, or that you were given anything.
- Style: {style}

Output only the answer text."""

CHECK_PROMPT = """Below is an ANSWER, and {n} numbered CLAIM PAIRS. For each pair, decide
which version the answer actually asserts.

ANSWER:
{answer}

CLAIM PAIRS:
{pairs}

For each pair output one of:
  "A"    - the answer asserts version A
  "B"    - the answer asserts version B
  "none" - the answer asserts neither, or is too vague to tell

Return ONLY JSON: [{{"i": 1, "asserts": "A"}}, ...]"""


def corrupt_order(item_id: str) -> list[int]:
    """Deterministic per-item permutation of claim indices; defines the nesting order."""
    h = hashlib.sha256(item_id.encode()).digest()
    return [i for _, i in sorted(zip(h[:N_CLAIMS], range(N_CLAIMS)))]


def claim_set(item: dict, k: int) -> tuple[list[str], list[bool]]:
    """Return the statement list at quality level k, plus a mask of which are corrupted."""
    order = corrupt_order(item["id"])
    bad = set(order[:k])
    stmts, is_bad = [], []
    for i, c in enumerate(item["claims"]):
        stmts.append(c["false"] if i in bad else c["true"])
        is_bad.append(i in bad)
    return stmts, is_bad


def render(item: dict, k: int, style: str) -> str:
    stmts, _ = claim_set(item, k)
    numbered = "\n".join(f"{i+1}. {s}" for i, s in enumerate(stmts))
    return chat(
        RENDER_MODEL,
        [{"role": "user", "content": RENDER_PROMPT.format(
            question=item["question"], statements=numbered, style=STYLES[style])}],
        max_tokens=1200,
        temperature=0.0,
    )


def check(item: dict, k: int, answer: str) -> list[dict]:
    _, is_bad = claim_set(item, k)
    lines = []
    for i, c in enumerate(item["claims"]):
        # Present the *intended* version as A and the other as B is leaky; instead present
        # true-version-first always, and recover intent from the mask afterwards.
        lines.append(f"{i+1}. A: {c['true']}\n   B: {c['false']}")
    txt = chat(
        CHECK_MODEL,
        [{"role": "user", "content": CHECK_PROMPT.format(
            n=N_CLAIMS, answer=answer, pairs="\n".join(lines))}],
        max_tokens=2000,
        reasoning_effort="low",
    )
    return extract_json(txt)


def main() -> None:
    items = json.load(open(os.path.join(DATA, "items.json")))
    cells = [(it, k, st) for it in items for k in QUALITY_LEVELS for st in STYLES]
    print(f"rendering {len(cells)} answers "
          f"({len(items)} items x {len(QUALITY_LEVELS)} quality x {len(STYLES)} styles)")

    jobs = [Job(fn=(lambda it=it, k=k, st=st: render(it, k, st))) for it, k, st in cells]
    texts = run_many(jobs, workers=24, desc="render")

    records = []
    for (it, k, st), txt in zip(cells, texts):
        _, is_bad = claim_set(it, k)
        records.append({
            "item_id": it["id"], "question": it["question"], "topic": it["topic"],
            "k": k, "style": st, "system": f"k{k}_{st}",
            "n_true_intended": N_CLAIMS - k, "corrupted_idx": [i for i, b in enumerate(is_bad) if b],
            "answer": txt, "n_words": len(txt.split()),
        })

    print("running renderer-fidelity manipulation check ...")
    cjobs = [Job(fn=(lambda it=it, k=k, r=r: check(it, k, r["answer"])))
             for (it, k, _), r in zip(cells, records)]
    checks = run_many(cjobs, workers=24, desc="check")

    by_id = {it["id"]: it for it in items}
    n_slots = 0
    n_faithful = 0
    for r, ch in zip(records, checks):
        it = by_id[r["item_id"]]
        _, is_bad = claim_set(it, r["k"])
        got = {c["i"] - 1: c["asserts"] for c in ch if isinstance(c, dict) and "i" in c}
        faithful, asserted_true, asserted_false = 0, 0, 0
        for i in range(N_CLAIMS):
            want = "B" if is_bad[i] else "A"
            a = got.get(i, "none")
            n_slots += 1
            if a == want:
                faithful += 1
                n_faithful += 1
            if a == "A":
                asserted_true += 1
            elif a == "B":
                asserted_false += 1
        r["render_faithful"] = faithful
        r["verified_true"] = asserted_true
        r["verified_false"] = asserted_false

    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, "answers.json"), "w") as f:
        json.dump(records, f, indent=1, ensure_ascii=False)

    print(f"renderer fidelity: {n_faithful}/{n_slots} = {n_faithful/n_slots:.3f} claim slots")
    for st in STYLES:
        sub = [r for r in records if r["style"] == st]
        print(f"  {st:<9} mean words {sum(r['n_words'] for r in sub)/len(sub):6.1f}  "
              f"fidelity {sum(r['render_faithful'] for r in sub)/(N_CLAIMS*len(sub)):.3f}")
    for k in QUALITY_LEVELS:
        sub = [r for r in records if r["k"] == k]
        print(f"  k={k}  verified_true {sum(r['verified_true'] for r in sub)/len(sub):.2f} "
              f"(intended {N_CLAIMS-k})  verified_false "
              f"{sum(r['verified_false'] for r in sub)/len(sub):.2f} (intended {k})")
    print(usage_report())


if __name__ == "__main__":
    main()
