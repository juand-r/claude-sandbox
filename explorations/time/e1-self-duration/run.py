"""E1 — Self-duration calibration.

Tests whether models can estimate their own wall-clock generation time.

For each (model x task x trial):
  PRE   : ask the model to predict, in seconds, how long its answer will take.
  TASK  : send the actual task; record true latency_s and output_tokens.
  POST  : fresh call with task + its own response; ask how long that took.

Every raw call is appended to results.jsonl. analyze.py reads that file and
never re-calls the API.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import call, MODELS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

# --- Roster (representative; controls cost) ---------------------------------
ROSTER = ["haiku", "sonnet", "opus", "gpt4o-mini", "gpt4o", "gpt5.2"]

N_TRIALS = 3

# --- Tasks: ~12 spanning short -> long expected outputs ----------------------
TASKS = [
    ("oneword_capital", "Answer in one word: what is the capital of France?"),
    ("yesno", "Answer with only 'yes' or 'no': is the sky blue on a clear day?"),
    ("arith", "What is 17 multiplied by 23? Give only the number."),
    ("list3", "List three primary colors, comma-separated. Nothing else."),
    ("define_word", "Define the word 'ephemeral' in a single sentence."),
    ("haiku", "Write a haiku about the ocean."),
    ("explain_short", "In 2-3 sentences, explain what photosynthesis is."),
    ("steps_tea", "List the steps to make a cup of tea, as a short numbered list."),
    ("paragraph", "Write one paragraph (about 100 words) about the history of the bicycle."),
    ("story", "Write a short story (about 200 words) about a lighthouse keeper."),
    ("essay", "Write a 500-word essay on the importance of curiosity in science."),
    ("code", "Write a Python function that returns the nth Fibonacci number, with a short docstring and an example usage comment."),
]

PRE_TEMPLATE = (
    "You are about to be asked to perform a task. Before you do it, estimate how "
    "many seconds it will take YOU (this AI model) to generate your full response "
    "to it, measured as wall-clock time for the generation.\n\n"
    "The task will be:\n\"\"\"\n{task}\n\"\"\"\n\n"
    "Respond with ONLY a single number: your best estimate of the generation time "
    "in seconds. No words, no units, just the number."
)

POST_TEMPLATE = (
    "Below is a task that was given to you (an AI model) and the response YOU "
    "generated for it.\n\n"
    "TASK:\n\"\"\"\n{task}\n\"\"\"\n\n"
    "YOUR RESPONSE:\n\"\"\"\n{response}\n\"\"\"\n\n"
    "Estimate how many seconds of wall-clock time it took YOU to generate that "
    "response.\n\n"
    "Respond with ONLY a single number: the generation time in seconds. No words, "
    "no units, just the number."
)


def parse_seconds(text):
    """Robustly pull a single seconds estimate out of a model response.

    Handles plain numbers, ranges ("3-5" -> midpoint), and embedded numbers with
    optional 'seconds'/'s' units. Returns float or None if nothing parseable.
    """
    if not text:
        return None
    t = text.strip().lower()
    # strip common wrappers
    t = t.replace("approximately", " ").replace("about", " ").replace("~", " ")
    # range like "3-5" or "3 to 5" -> midpoint
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)", t)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2.0
    # first standalone number
    m = re.search(r"(\d+(?:\.\d+)?)", t)
    if m:
        return float(m.group(1))
    return None


def append_record(rec):
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def load_done():
    """Return set of (model, task_id, trial, condition) already recorded, for resume."""
    done = set()
    if not os.path.exists(RESULTS):
        return done
    with open(RESULTS) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            done.add((r["model"], r["task_id"], r["trial"], r["condition"]))
    return done


def run(models=None, tasks=None, n_trials=N_TRIALS):
    models = models or ROSTER
    tasks = tasks or TASKS
    done = load_done()
    n_calls = 0

    for model in models:
        for task_id, task_prompt in tasks:
            for trial in range(n_trials):
                # --- PRE ---
                key = (model, task_id, trial, "pre")
                if key not in done:
                    pre_prompt = PRE_TEMPLATE.format(task=task_prompt)
                    r = call(model, pre_prompt, max_tokens=512)
                    if not r.ok:
                        raise RuntimeError(f"PRE call failed {key}: {r.error}")
                    est = parse_seconds(r.text)
                    append_record({
                        "model": model, "task_id": task_id, "trial": trial,
                        "condition": "pre", "prompt": pre_prompt,
                        "response_text": r.text, "parsed_estimate_s": est,
                        "latency_s": r.latency_s, "output_tokens": r.output_tokens,
                        "input_tokens": r.input_tokens,
                    })
                    n_calls += 1
                    if est is None:
                        print(f"  WARN: PRE unparsed {key}: {r.text!r}")

                # --- TASK (actual generation) ---
                key = (model, task_id, trial, "task")
                task_resp_text = None
                if key not in done:
                    r = call(model, task_prompt, max_tokens=1024)
                    if not r.ok:
                        raise RuntimeError(f"TASK call failed {key}: {r.error}")
                    task_resp_text = r.text
                    append_record({
                        "model": model, "task_id": task_id, "trial": trial,
                        "condition": "task", "prompt": task_prompt,
                        "response_text": r.text, "parsed_estimate_s": None,
                        "latency_s": r.latency_s, "output_tokens": r.output_tokens,
                        "input_tokens": r.input_tokens,
                    })
                    n_calls += 1
                else:
                    # need the response text for POST; pull it from file
                    task_resp_text = _lookup_task_text(model, task_id, trial)

                # --- POST ---
                key = (model, task_id, trial, "post")
                if key not in done:
                    if task_resp_text is None:
                        task_resp_text = _lookup_task_text(model, task_id, trial)
                    post_prompt = POST_TEMPLATE.format(
                        task=task_prompt, response=task_resp_text or "")
                    r = call(model, post_prompt, max_tokens=512)
                    if not r.ok:
                        raise RuntimeError(f"POST call failed {key}: {r.error}")
                    est = parse_seconds(r.text)
                    append_record({
                        "model": model, "task_id": task_id, "trial": trial,
                        "condition": "post", "prompt": post_prompt,
                        "response_text": r.text, "parsed_estimate_s": est,
                        "latency_s": r.latency_s, "output_tokens": r.output_tokens,
                        "input_tokens": r.input_tokens,
                    })
                    n_calls += 1
                    if est is None:
                        print(f"  WARN: POST unparsed {key}: {r.text!r}")

            print(f"done {model} / {task_id}")
    print(f"\nTotal new calls this run: {n_calls}")


def _lookup_task_text(model, task_id, trial):
    with open(RESULTS) as f:
        for line in f:
            r = json.loads(line)
            if (r["model"], r["task_id"], r["trial"], r["condition"]) == \
               (model, task_id, trial, "task"):
                return r["response_text"]
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dryrun":
        print("DRY RUN: haiku x oneword_capital x 1 trial")
        run(models=["haiku"], tasks=[TASKS[0]], n_trials=1)
    else:
        run()
