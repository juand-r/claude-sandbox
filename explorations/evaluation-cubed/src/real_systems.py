"""
Stage 6 (ecological validity): repeat the study on *real* systems.

The synthetic grid buys exact ground truth at the cost of realism: its systems are
constructed, and its style factor is imposed. This stage checks that the phenomena survive
when the systems are actual models answering freely.

Design:
  * 5 real models answer the same 85 questions with no claim list and no style instruction.
  * True quality is *measured*, not constructed: a checker decides, for each of the item's
    6 reference claims, whether the answer supports it, contradicts it, or omits it.
    Quality = (supported - contradicted) / 6. This is a narrow entailment check against a
    given claim, not a holistic quality judgement, and it is the only place in the project
    where ground truth is estimated rather than constructed.
  * Each real answer is then restyled into the same three styles. Restyling is
    quality-preserving by intent; we verify it by comparing the claim profile before and
    after. This gives the perturbation family needed for the label-free certificate on a
    population nobody has labelled.

Outputs: data/real_answers.json, results/real_pointwise.jsonl
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_systems import STYLES  # noqa: E402
from judges import (  # noqa: E402
    MAX_TOK, MAX_TOK_REASONING, POINTWISE_PROTOCOLS, judge_id, parse_score,
)
from llm import Job, chat, extract_json, is_reasoning_model, run_many, usage_report  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

# The systems under evaluation (deliberately spanning a wide capability range).
REAL_MODELS = [
    ("gpt-4.1-nano", None),
    ("gpt-4o-mini", None),
    ("gpt-4.1-mini", None),
    ("gpt-5-nano", "minimal"),
    ("gpt-4.1", None),
]

# A judge subset; the full 24-cell grid is already covered by the synthetic study.
REAL_JUDGES = [
    ("gpt-4.1-nano", None, "direct"),
    ("gpt-4.1-nano", None, "rubric"),
    ("gpt-4o-mini", None, "direct"),
    ("gpt-4.1-mini", None, "direct"),
    ("gpt-4.1-mini", None, "cot"),
    ("gpt-4.1", None, "rubric"),
    ("gpt-5-mini", "minimal", "rubric"),
    ("gpt-5.4-mini", "low", "rubric"),
]

CHECK_MODEL = "gpt-5.4-mini"

ANSWER_PROMPT = """{question}

Answer in a few sentences."""

RESTYLE_PROMPT = """Rewrite the following answer in a different style.

CRITICAL: preserve the factual content exactly. Every factual assertion in the original
must appear in the rewrite, with the same meaning. Add no new facts. Correct nothing,
even if something looks wrong to you. Only the surface form may change.

Style to use: {style}

Original answer:
{answer}

Output only the rewritten answer."""

FACT_PROMPT = """Below is an ANSWER to a question, and {n} reference CLAIMS that a correct
answer would contain. For each claim decide what the answer does with it:

  "support"     - the answer asserts something consistent with the claim
  "contradict"  - the answer asserts something incompatible with the claim
  "absent"      - the answer neither asserts nor contradicts it

QUESTION: {question}

ANSWER:
{answer}

CLAIMS:
{claims}

Return ONLY JSON: [{{"i": 1, "verdict": "support"}}, ...]"""


def get_answer(model: str, effort: str | None, question: str) -> str:
    return chat(model, [{"role": "user", "content": ANSWER_PROMPT.format(question=question)}],
                max_tokens=1500, temperature=0.0, reasoning_effort=effort)


def restyle(answer: str, style: str) -> str:
    return chat("gpt-4.1-mini",
                [{"role": "user", "content": RESTYLE_PROMPT.format(
                    style=STYLES[style], answer=answer)}],
                max_tokens=1500, temperature=0.0)


def fact_check(item: dict, answer: str) -> list[dict]:
    claims = "\n".join(f"{i+1}. {c['true']}" for i, c in enumerate(item["claims"]))
    txt = chat(CHECK_MODEL,
               [{"role": "user", "content": FACT_PROMPT.format(
                   n=len(item["claims"]), question=item["question"],
                   answer=answer, claims=claims)}],
               max_tokens=2000, reasoning_effort="low")
    return extract_json(txt)


def quality_from_check(verdicts: list[dict], n: int) -> float:
    sup = sum(1 for v in verdicts if v.get("verdict") == "support")
    con = sum(1 for v in verdicts if v.get("verdict") == "contradict")
    return (sup - con) / n


def main() -> None:
    items = json.load(open(os.path.join(DATA, "items.json")))
    n_claims = len(items[0]["claims"])

    # ---- 1. real answers -----------------------------------------------------
    cells = [(m, e, it) for m, e in REAL_MODELS for it in items]
    print(f"generating {len(cells)} real answers")
    raw = run_many([Job(fn=(lambda m=m, e=e, it=it: get_answer(m, e, it["question"])))
                    for m, e, it in cells], workers=24, desc="answer")

    base = []
    for (m, _, it), txt in zip(cells, raw):
        base.append({"item_id": it["id"], "question": it["question"], "model": m,
                     "style": "native", "system": m, "answer": txt})

    # ---- 2. measured quality -------------------------------------------------
    by_id = {it["id"]: it for it in items}
    print("fact-checking real answers against reference claims")
    checks = run_many([Job(fn=(lambda r=r: fact_check(by_id[r["item_id"]], r["answer"])))
                       for r in base], workers=24, desc="factcheck")
    for r, ch in zip(base, checks):
        r["quality"] = quality_from_check(ch, n_claims)
        r["verdicts"] = [c.get("verdict") for c in sorted(ch, key=lambda x: x.get("i", 0))]

    # ---- 3. quality-preserving restyling -------------------------------------
    print(f"restyling into {len(STYLES)} styles")
    rjobs = [(r, st) for r in base for st in STYLES]
    styled = run_many([Job(fn=(lambda r=r, st=st: restyle(r["answer"], st)))
                       for r, st in rjobs], workers=24, desc="restyle")

    records = []
    for (r, st), txt in zip(rjobs, styled):
        records.append({**{k: v for k, v in r.items() if k != "answer"},
                        "style": st, "system": f"{r['model']}__{st}",
                        "answer": txt, "n_words": len(txt.split())})

    # ---- 4. verify restyling preserved content -------------------------------
    print("verifying restyling is quality-preserving")
    vchecks = run_many([Job(fn=(lambda r=r: fact_check(by_id[r["item_id"]], r["answer"])))
                        for r in records], workers=24, desc="verify-restyle")
    drift = []
    for r, ch in zip(records, vchecks):
        q2 = quality_from_check(ch, n_claims)
        r["quality_after_restyle"] = q2
        drift.append(abs(q2 - r["quality"]))
    print(f"restyle quality drift: mean {sum(drift)/len(drift):.4f} claims-fraction, "
          f"max {max(drift):.3f}")

    all_records = base + records
    with open(os.path.join(DATA, "real_answers.json"), "w") as f:
        json.dump(all_records, f, indent=1, ensure_ascii=False)

    print("\nmeasured quality of the real systems (native style):")
    for m, _ in REAL_MODELS:
        sub = [r for r in base if r["model"] == m]
        w = [len(r["answer"].split()) for r in sub]
        print(f"  {m:<16} Q={sum(r['quality'] for r in sub)/len(sub):.4f}  "
              f"mean words {sum(w)/len(w):.0f}")

    # ---- 5. judge them --------------------------------------------------------
    tasks = []
    for model, effort, proto in REAL_JUDGES:
        tmpl = POINTWISE_PROTOCOLS[proto]
        cap = (MAX_TOK_REASONING if is_reasoning_model(model) else MAX_TOK)[proto]
        for r in all_records:
            prompt = tmpl.format(question=r["question"], answer=r["answer"])
            tasks.append({
                "judge": judge_id(model, proto), "item_id": r["item_id"],
                "system": r["system"], "model_under_test": r["model"], "style": r["style"],
                "quality": r["quality"],
                "fn": (lambda m=model, p=prompt, c=cap, e=effort:
                       chat(m, [{"role": "user", "content": p}], max_tokens=c,
                            temperature=0.0, reasoning_effort=e)),
            })
    print(f"\njudging: {len(tasks)} calls")
    texts = run_many([Job(fn=t["fn"]) for t in tasks], workers=32, desc="real-judge")

    n_bad = 0
    with open(os.path.join(RESULTS, "real_pointwise.jsonl"), "w") as f:
        for t, txt in zip(tasks, texts):
            s = parse_score(txt)
            n_bad += s is None
            row = {k: t[k] for k in
                   ("judge", "item_id", "system", "model_under_test", "style", "quality")}
            row["score"] = s
            f.write(json.dumps(row) + "\n")
    print(f"done, {n_bad}/{len(tasks)} unparseable")
    print(usage_report())


if __name__ == "__main__":
    main()
