"""E10 - Reasoning-model hidden-token probe.

Every prior experiment isolated the SAME boundary: reasoning models cannot account for the
tokens they spend on hidden reasoning (E1 gpt5.2 0.32x, E2 o4-mini token ratio 0.10, E5 type A
rho ~0, E6 o4-mini stuck). E10 attacks it head-on: can a reasoning model predict its OWN
reasoning length?

Design. Tasks span a wide reasoning-difficulty gradient but all have SHORT final answers, so
the variable is internal reasoning, not output. For each (model x task x trial):
  pre_tokens : estimate, WITHOUT solving, how many internal reasoning tokens it will need
  pre_effort : rate 1-10 how much step-by-step thinking the problem needs
  gen        : actually solve; record ACTUAL reasoning_tokens (from usage)
Compare estimates to actual reasoning_tokens (Spearman rho, ordering accuracy, gm ratio).

Models: o4-mini, gpt5 -- the OpenAI reasoning models whose reasoning_tokens vary with
difficulty and are exposed in usage. (gpt5.2 does not engage reasoning by default -> excluded.)

Resumable + single-writer safe via load_done().
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import call  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

ROSTER = ["o4-mini", "gpt5"]
N_TRIALS = 3

# Short-answer problems across a reasoning-difficulty gradient (trivial -> very hard).
TASKS = [
    ("triv_add",   "What is 2 + 2? Reply with just the number."),
    ("triv_cap",   "What is the capital of France? Reply with just the city name."),
    ("easy_even",  "Is 10 an even number? Reply with just YES or NO."),
    ("easy_mul",   "What is 17 * 23? Reply with just the number."),
    ("easy_rev",   "Reverse the word 'reason'. Reply with just the reversed word."),
    ("med_units",  "What is the units digit of 7^100? Reply with just the single digit."),
    ("med_word",   "A train travels 90 miles in 1.5 hours. What is its average speed in mph? "
                   "Reply with just the number."),
    ("med_gcd",    "What is the greatest common divisor of 4181 and 6765? Reply with just the number."),
    ("hard_prime", "Is 7919 a prime number? Reply with just YES or NO."),
    ("hard_d6",    "How many derangements are there of 6 elements (permutations with no fixed "
                   "point)? Reply with just the number."),
    ("hard_mod",   "What is 3^200 mod 100? Reply with just the number."),
    ("vhard_d9",   "How many derangements are there of 9 elements (permutations with no fixed "
                   "point)? Reply with just the number."),
    ("vhard_logic","Five people A,B,C,D,E finish a race. A is not last. B beats D and E. C is "
                   "immediately after A. E is not first or last. D is not adjacent to B. What is "
                   "the finishing order? Reply with just the 5 letters in order."),
    ("vhard_count","How many integers between 1 and 1000 inclusive are divisible by neither 6, "
                   "10, nor 15? Reply with just the number."),
]

PRE_TOKENS = (
    "You are about to be asked to solve a problem. Do NOT solve it now. Instead, estimate how "
    "many tokens of internal step-by-step reasoning you will need in order to solve it. Reply "
    "with only a single number (your estimated reasoning-token count), nothing else.\n\n"
    "PROBLEM:\n{task}"
)
PRE_EFFORT = (
    "You are about to be asked to solve a problem. Do NOT solve it. On a scale of 1 (trivial, "
    "no thinking) to 10 (extremely hard, very long deliberation), rate how much internal "
    "step-by-step reasoning this problem will require. Reply with only a single integer 1-10.\n\n"
    "PROBLEM:\n{task}"
)


def parse_number(text):
    if not text:
        return None
    t = text.strip().lower().replace("approximately", " ").replace("about", " ").replace("~", " ")
    t = t.replace(",", "")
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)", t)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2.0
    m = re.search(r"(\d+(?:\.\d+)?)", t)
    return float(m.group(1)) if m else None


def append_record(rec):
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def load_done():
    done = set()
    if os.path.exists(RESULTS):
        for line in open(RESULTS):
            if line.strip():
                r = json.loads(line)
                done.add((r["model"], r["task_id"], r["trial"], r["condition"]))
    return done


def run(models=ROSTER, n_trials=N_TRIALS):
    done = load_done()
    n = 0
    for model in models:
        for task_id, task in TASKS:
            for trial in range(n_trials):
                for cond, tmpl in [("pre_tokens", PRE_TOKENS), ("pre_effort", PRE_EFFORT)]:
                    if (model, task_id, trial, cond) in done:
                        continue
                    r = call(model, tmpl.format(task=task), max_tokens=4000)
                    if not r.ok:
                        raise RuntimeError(f"{cond} failed {model}/{task_id}: {r.error}")
                    append_record({
                        "model": model, "task_id": task_id, "trial": trial, "condition": cond,
                        "parsed_estimate": parse_number(r.text), "response_text": r.text[:200],
                        "latency_s": r.latency_s, "output_tokens": r.output_tokens,
                        "reasoning_tokens": r.reasoning_tokens,
                    })
                    n += 1
                if (model, task_id, trial, "gen") not in done:
                    r = call(model, task, max_tokens=8000)
                    if not r.ok:
                        raise RuntimeError(f"gen failed {model}/{task_id}: {r.error}")
                    append_record({
                        "model": model, "task_id": task_id, "trial": trial, "condition": "gen",
                        "parsed_estimate": None, "response_text": r.text[:200],
                        "latency_s": r.latency_s, "output_tokens": r.output_tokens,
                        "reasoning_tokens": r.reasoning_tokens,  # ACTUAL
                    })
                    n += 1
            print(f"done {model} / {task_id}")
    print(f"\nNew calls this run: {n} -> {RESULTS}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dryrun":
        run(models=["o4-mini"], n_trials=1)
    else:
        run()
