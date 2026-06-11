"""E6 — Length-estimation bias correction.

E2 found a systematic ~2x undershoot when models predict their own OUTPUT TOKEN count.
E6 tests whether that bias closes with cheap IN-CONTEXT interventions (no training):

  (a) bare         : predict output tokens, no help [E2 baseline]
  (b) anchors      : predict after few-shot token-count calibration anchors
  (c) self_revise  : predict, then reconsider over/under-estimation, give FINAL

For each (model, task, trial): one GEN (actual output_tokens) + three estimate calls.
Compare each estimate to the SAME-trial actual. Resumable + single-writer safe.

Payoff: if anchors/revision move gm(pred/actual) toward 1.0, length self-estimation needs
no fine-tuning (relevant to direction-train-it-in.md, Target 1).
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import call  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

ROSTER = ["haiku", "sonnet", "opus", "gpt4o-mini", "gpt4o", "o4-mini"]
N_TRIALS = 3

# Output-length-varying tasks (short -> long).
TASKS = [
    ("t_word", "Reply with exactly one word: yes."),
    ("t_capital", "What is the capital of France? Answer in one short sentence."),
    ("t_sentence", "Write exactly one sentence about coffee."),
    ("t_haiku", "Write a haiku about winter."),
    ("t_list", "List three uses for a paperclip, one per line."),
    ("t_paragraph", "Write a short paragraph (3-4 sentences) about the history of clocks."),
    ("t_explain", "Explain how a bicycle stays upright, in about 100 words."),
    ("t_essay200", "Write about the ocean in approximately 200 words."),
    ("t_steps", "Give detailed step-by-step instructions for making bread, with at least 8 steps."),
    ("t_essay600", "Write an essay about the importance of sleep in approximately 600 words."),
]

BARE = ("Estimate how many TOKENS your response to the task below will contain (roughly 0.75 "
        "tokens per word). Reply with just a single number, nothing else.\n\nTASK:\n{task}")

ANCHORS = (
    "Calibration anchors for response length, in tokens:\n"
    "  'yes'                          -> ~1 token\n"
    "  one short sentence (~15 words) -> ~20 tokens\n"
    "  a haiku                        -> ~25 tokens\n"
    "  a short paragraph (~60 words)  -> ~85 tokens\n"
    "  a 100-word explanation         -> ~135 tokens\n"
    "  a 200-word essay               -> ~270 tokens\n"
    "  a 600-word essay               -> ~800 tokens\n"
    "Using these anchors, estimate how many TOKENS your response to the task below will "
    "contain. Reply with just a single number, nothing else.\n\nTASK:\n{task}")

SELF_REVISE = (
    "Estimate how many TOKENS your response to the task below will contain.\n"
    "1) Give an initial estimate.\n"
    "2) Reconsider: models systematically UNDER-estimate their own output length. Adjust if "
    "needed.\n"
    "3) On the last line, output exactly 'FINAL: <number>'.\n\nTASK:\n{task}")

COND = {"bare": BARE, "anchors": ANCHORS, "self_revise": SELF_REVISE}


def parse_number(text, prefer_final=False):
    if not text:
        return None
    t = text.strip()
    if prefer_final:
        m = re.search(r"final\s*[:=]\s*(\d+(?:\.\d+)?)", t, re.IGNORECASE)
        if m:
            return float(m.group(1))
        # else fall back to LAST number in the text
        nums = re.findall(r"(\d+(?:\.\d+)?)", t)
        return float(nums[-1]) if nums else None
    tl = t.lower().replace("approximately", " ").replace("about", " ").replace("~", " ")
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)", tl)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2.0
    m = re.search(r"(\d+(?:\.\d+)?)", tl)
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
    done = load_done()
    n_calls = 0
    for model in models:
        for task_id, task in TASKS:
            for trial in range(n_trials):
                # GEN actual length
                k = (model, task_id, trial, "gen")
                if k not in done:
                    r = call(model, task, max_tokens=1500)
                    if not r.ok:
                        raise RuntimeError(f"GEN failed {k}: {r.error}")
                    append_record({
                        "model": model, "task_id": task_id, "trial": trial,
                        "condition": "gen", "parsed_estimate_tok": None,
                        "actual_output_tokens": r.output_tokens,
                        "response_text": r.text[:300], "latency_s": r.latency_s,
                    })
                    n_calls += 1
                # estimate conditions
                for cond, tmpl in COND.items():
                    k = (model, task_id, trial, cond)
                    if k in done:
                        continue
                    r = call(model, tmpl.format(task=task), max_tokens=1024)
                    if not r.ok:
                        raise RuntimeError(f"{cond} failed {k}: {r.error}")
                    est = parse_number(r.text, prefer_final=(cond == "self_revise"))
                    append_record({
                        "model": model, "task_id": task_id, "trial": trial,
                        "condition": cond, "parsed_estimate_tok": est,
                        "actual_output_tokens": None,
                        "response_text": r.text[:300], "latency_s": r.latency_s,
                    })
                    n_calls += 1
            print(f"done {model} / {task_id}")
    print(f"\nNew calls this run: {n_calls} -> {RESULTS}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dryrun":
        run(models=["haiku"], n_trials=1)
    else:
        run()
