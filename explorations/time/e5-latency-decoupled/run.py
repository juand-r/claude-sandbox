"""E5 — Latency-decoupled probe.

Tests whether E1/E2's "models estimate their own latency well" survives when wall-clock
latency is DECOUPLED from output length. Three task families:

  Type A (reasoning-decoupled): short fixed output, varying difficulty. Latency varies via
      hidden reasoning (matters for reasoning models).
  Type B (input-decoupled): fixed one-word output, varying INPUT length. Latency varies via
      prefill.
  Type C (output-driven control): output length varies (E1-style). Positive control.

For each (model, task, trial): PRE seconds-estimate, then GEN (record actual latency,
output_tokens, input_tokens). Resumable + single-writer safe via load_done().

Prediction: rho(estimate, actual) stays high in C, drops in A and B -> confirms models
track length they can see, not latency they cannot.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import call  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

# Reasoning models essential for Type A; non-reasoning for B/C calibration.
ROSTER = ["haiku", "sonnet", "gpt4o", "gpt5.2", "o4-mini"]
N_TRIALS = 3

# A ~20-token sentence used to build controlled-size input filler for Type B.
_FILLER_SENT = ("The quarterly logistics report notes that shipments moved through the "
                "regional depot without any recorded incident during the period. ")


def _filler(approx_tokens):
    # ~ -1 token per 0.75 words; sentence ~ 20 tokens. Repeat to reach target.
    reps = max(1, round(approx_tokens / 20))
    return _FILLER_SENT * reps


# Type A: short fixed output, varying reasoning difficulty (one number / one word).
TYPE_A = [
    ("A_triv_add", "What is 2 + 2? Answer with just the number, nothing else."),
    ("A_easy_even", "Is 10 an even number? Answer with exactly one word: YES or NO."),
    ("A_mul", "What is 17 * 23? Answer with just the number, nothing else."),
    ("A_units", "What is the units digit of 7^100? Answer with just the single digit."),
    ("A_prime", "Is 7919 a prime number? Answer with exactly one word: YES or NO."),
    ("A_derange", "In how many ways can the numbers 1..8 be arranged so that no number "
                  "is in its own position (a derangement of 8 elements)? Answer with just "
                  "the number, nothing else."),
]

# Type C: output length varies (positive control).
TYPE_C = [
    ("C_word", "Reply with exactly one word: yes."),
    ("C_sentence", "Write exactly one sentence about the ocean."),
    ("C_paragraph", "Write a short paragraph (3-4 sentences) about the ocean."),
    ("C_essay200", "Write about the ocean in approximately 200 words."),
    ("C_essay600", "Write about the ocean in approximately 600 words."),
]

# Type B: fixed one-word output, varying input length. Built dynamically.
# Larger sizes give a clearer prefill-latency gradient; output is pinned to one word so
# latency varies by INPUT length only. Instruction is placed first AND repeated at the end
# so the model reliably emits a single token regardless of the filler in between.
B_SIZES = [100, 1000, 8000, 30000]


def type_b_tasks():
    out = []
    for n in B_SIZES:
        prompt = (
            "You are a text-processing harness. Below is a block of REFERENCE TEXT. Do NOT "
            "read, summarize, or respond to its contents. Your entire reply must be exactly "
            "one word: DONE\n\n"
            "REFERENCE TEXT:\n" + _filler(n) +
            "\n\nEND OF REFERENCE TEXT. Now reply with exactly one word and nothing else: DONE"
        )
        out.append((f"B_in{n}", prompt))
    return out


def all_tasks():
    tasks = []
    for tid, p in TYPE_A:
        tasks.append(("A", tid, p))
    for tid, p in type_b_tasks():
        tasks.append(("B", tid, p))
    for tid, p in TYPE_C:
        tasks.append(("C", tid, p))
    return tasks


PRE_TMPL = (
    "You are about to receive a task. Estimate how many SECONDS it will take YOU to "
    "generate your full response to it (wall-clock time). Consider how much work and how "
    "long an output it requires. Reply with just a single number of seconds, nothing else.\n\n"
    "TASK:\n{task}"
)


def parse_number(text):
    if not text:
        return None
    t = text.strip().lower().replace("approximately", " ").replace("about", " ").replace("~", " ")
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
            if not line.strip():
                continue
            r = json.loads(line)
            done.add((r["model"], r["task_id"], r["trial"], r["condition"]))
    return done


def run(models=ROSTER, n_trials=N_TRIALS):
    tasks = all_tasks()
    done = load_done()
    n_calls = 0
    for model in models:
        for ttype, task_id, prompt in tasks:
            for trial in range(n_trials):
                # PRE
                k = (model, task_id, trial, "pre")
                if k not in done:
                    r = call(model, PRE_TMPL.format(task=prompt), max_tokens=512)
                    if not r.ok:
                        raise RuntimeError(f"PRE failed {k}: {r.error}")
                    append_record({
                        "model": model, "type": ttype, "task_id": task_id, "trial": trial,
                        "condition": "pre", "parsed_estimate_s": parse_number(r.text),
                        "response_text": r.text[:500], "latency_s": r.latency_s,
                        "output_tokens": r.output_tokens, "input_tokens": r.input_tokens,
                    })
                    n_calls += 1
                # GEN
                k = (model, task_id, trial, "gen")
                if k not in done:
                    r = call(model, prompt, max_tokens=1500)
                    if not r.ok:
                        raise RuntimeError(f"GEN failed {k}: {r.error}")
                    append_record({
                        "model": model, "type": ttype, "task_id": task_id, "trial": trial,
                        "condition": "gen", "parsed_estimate_s": None,
                        "response_text": r.text[:500], "latency_s": r.latency_s,
                        "output_tokens": r.output_tokens, "input_tokens": r.input_tokens,
                    })
                    n_calls += 1
            print(f"done {model} / {task_id}")
    print(f"\nNew calls this run: {n_calls} -> {RESULTS}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dryrun":
        run(models=["haiku"], n_trials=1)
    else:
        run()
