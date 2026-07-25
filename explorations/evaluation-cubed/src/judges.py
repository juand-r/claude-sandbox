"""
Stage 3: run the judge grid.

A *judge configuration* is (model, protocol). Pointwise protocols score a single answer;
the pairwise protocol compares an answer against a fixed anchor system, both orders.

Everything is cached, so this file is re-runnable and each stage is incremental.

Outputs: results/pointwise.jsonl   one row per (judge, answer)
         results/pairwise.jsonl    one row per (judge, item, system, order)
"""

from __future__ import annotations

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm import Job, chat, is_reasoning_model, run_many, usage_report  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

# ---------------------------------------------------------------- judge models
# A capability ladder, deliberately wide: judge selection is the decision we are studying,
# so the candidate pool has to contain both weak and strong judges.
POINTWISE_MODELS = [
    ("gpt-4.1-nano", None),
    ("gpt-4o-mini", None),
    ("gpt-4.1-mini", None),
    ("gpt-4.1", None),
    ("gpt-5-nano", "minimal"),
    ("gpt-5-mini", "minimal"),
    ("gpt-5.4-nano", "low"),
    ("gpt-5.4-mini", "low"),
]

PAIRWISE_MODELS = [
    ("gpt-4.1-nano", None),
    ("gpt-4.1-mini", None),
    ("gpt-5-mini", "minimal"),
    ("gpt-5.4-mini", "low"),
]

ANCHOR_SYSTEM = "k2_plain"  # mid-quality, neutral style

# ---------------------------------------------------------------- protocols
DIRECT = """Rate the overall quality of the following answer.

Question: {question}

Answer:
{answer}

Give a score from 1 (very poor) to 10 (excellent).
Respond with exactly one line: SCORE: <number>"""

RUBRIC = """You are evaluating the quality of an answer to a question.

Question: {question}

Answer:
{answer}

Consider:
- Factual accuracy: are the stated facts correct?
- Completeness: does it cover what the question asks?
- Clarity: is it well written and easy to follow?

Give an overall score from 1 (very poor) to 10 (excellent).
Respond with exactly one line: SCORE: <number>"""

COT = """You are evaluating the quality of an answer to a question.

Question: {question}

Answer:
{answer}

First reason briefly (at most 80 words) about the answer's strengths and weaknesses.
Then give an overall score from 1 (very poor) to 10 (excellent).
End your reply with exactly: SCORE: <number>"""

POINTWISE_PROTOCOLS = {"direct": DIRECT, "rubric": RUBRIC, "cot": COT}

PAIRWISE = """Two assistants answered the same question. Decide which answer is better.

Question: {question}

Answer A:
{a}

Answer B:
{b}

Respond with exactly one line: VERDICT: A  or  VERDICT: B"""

MAX_TOK = {"direct": 16, "rubric": 16, "cot": 400}
# Reasoning models emit reasoning tokens before any visible text, so short caps starve them.
MAX_TOK_REASONING = {"direct": 900, "rubric": 900, "cot": 1400}


def judge_id(model: str, protocol: str) -> str:
    return f"{model}::{protocol}"


_SCORE_RE = re.compile(r"SCORE\s*[:=]?\s*([0-9]+(?:\.[0-9]+)?)", re.I)
_NUM_RE = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s*(?:/\s*10)?\s*$")


def parse_score(text: str) -> float | None:
    m = _SCORE_RE.findall(text)
    if m:
        v = float(m[-1])
        return v if 1.0 <= v <= 10.0 else None
    m2 = _NUM_RE.search(text.strip())
    if m2:
        v = float(m2.group(1))
        return v if 1.0 <= v <= 10.0 else None
    return None


def parse_verdict(text: str) -> str | None:
    m = re.findall(r"VERDICT\s*[:=]?\s*\(?([AB])\)?", text, re.I)
    if m:
        return m[-1].upper()
    s = text.strip().upper()
    if s in ("A", "B"):
        return s
    return None


def run_pointwise(answers: list[dict], out_path: str) -> None:
    tasks = []
    for model, effort in POINTWISE_MODELS:
        for proto, tmpl in POINTWISE_PROTOCOLS.items():
            cap = (MAX_TOK_REASONING if is_reasoning_model(model) else MAX_TOK)[proto]
            for a in answers:
                prompt = tmpl.format(question=a["question"], answer=a["answer"])
                tasks.append({
                    "judge": judge_id(model, proto), "model": model, "protocol": proto,
                    "item_id": a["item_id"], "system": a["system"], "k": a["k"],
                    "style": a["style"],
                    "fn": (lambda m=model, p=prompt, c=cap, e=effort:
                           chat(m, [{"role": "user", "content": p}],
                                max_tokens=c, temperature=0.0, reasoning_effort=e)),
                })
    print(f"pointwise: {len(tasks)} calls "
          f"({len(POINTWISE_MODELS)}x{len(POINTWISE_PROTOCOLS)} judges x {len(answers)} answers)")
    texts = run_many([Job(fn=t["fn"]) for t in tasks], workers=32, desc="pointwise")

    n_bad = 0
    with open(out_path, "w") as f:
        for t, txt in zip(tasks, texts):
            s = parse_score(txt)
            if s is None:
                n_bad += 1
            row = {k: t[k] for k in ("judge", "model", "protocol", "item_id", "system", "k", "style")}
            row["score"] = s
            f.write(json.dumps(row) + "\n")
    print(f"pointwise done, {n_bad}/{len(tasks)} unparseable ({n_bad/len(tasks):.4f})")


def run_pairwise(answers: list[dict], out_path: str) -> None:
    by = {(a["item_id"], a["system"]): a for a in answers}
    systems = sorted({a["system"] for a in answers})
    items = sorted({a["item_id"] for a in answers})

    tasks = []
    for model, effort in PAIRWISE_MODELS:
        for it in items:
            anchor = by[(it, ANCHOR_SYSTEM)]
            for sysname in systems:
                if sysname == ANCHOR_SYSTEM:
                    continue
                cand = by[(it, sysname)]
                for order in ("cand_first", "anchor_first"):
                    a_txt, b_txt = ((cand["answer"], anchor["answer"])
                                    if order == "cand_first"
                                    else (anchor["answer"], cand["answer"]))
                    prompt = PAIRWISE.format(question=cand["question"], a=a_txt, b=b_txt)
                    cap = 900 if is_reasoning_model(model) else 16
                    tasks.append({
                        "judge": judge_id(model, "pairwise"), "model": model,
                        "item_id": it, "system": sysname, "k": cand["k"],
                        "style": cand["style"], "order": order,
                        "fn": (lambda m=model, p=prompt, c=cap, e=effort:
                               chat(m, [{"role": "user", "content": p}],
                                    max_tokens=c, temperature=0.0, reasoning_effort=e)),
                    })
    print(f"pairwise: {len(tasks)} calls")
    texts = run_many([Job(fn=t["fn"]) for t in tasks], workers=32, desc="pairwise")

    n_bad = 0
    with open(out_path, "w") as f:
        for t, txt in zip(tasks, texts):
            v = parse_verdict(txt)
            if v is None:
                n_bad += 1
                win = None
            else:
                # 1 if the judge preferred the candidate over the anchor
                win = 1 if ((t["order"] == "cand_first" and v == "A")
                            or (t["order"] == "anchor_first" and v == "B")) else 0
            row = {k: t[k] for k in ("judge", "model", "item_id", "system", "k", "style", "order")}
            row["cand_win"] = win
            f.write(json.dumps(row) + "\n")
    print(f"pairwise done, {n_bad}/{len(tasks)} unparseable ({n_bad/max(len(tasks),1):.4f})")


def main() -> None:
    answers = json.load(open(os.path.join(DATA, "answers.json")))
    os.makedirs(RESULTS, exist_ok=True)
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "pointwise"):
        run_pointwise(answers, os.path.join(RESULTS, "pointwise.jsonl"))
    if which in ("all", "pairwise"):
        run_pairwise(answers, os.path.join(RESULTS, "pairwise.jsonl"))
    print(usage_report())


if __name__ == "__main__":
    main()
