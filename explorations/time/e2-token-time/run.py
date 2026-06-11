"""E2 — Token/step proxy reframe. Data collection.

Hypothesis: estimating output LENGTH (tokens) is better-calibrated than
estimating wall-clock SECONDS, because output length is something the model
has more access to than its own latency.

For each (model x task) we run N trials of four PROMPT conditions plus one
actual GENERATION:

  cond_seconds  (a): predict seconds the response will take       -> baseline (E1)
  cond_tokens   (b): predict number of output tokens               -> length space
  cond_reason   (d): think briefly about output length, then sec   -> length-reasoning
  gen           ( ): actually produce the response; record true latency_s + output_tokens

Condition (c) "tokens -> seconds via measured tokens/sec" is NOT a separate
API call: it reuses the (b) token estimate and is converted in analyze.py using
an empirically measured per-model tokens/sec constant (from the gen rows).

Everything is cached to results.jsonl. analyze.py never calls the API.
"""

import sys, os, json, re, argparse, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import call, MODELS

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

N_TRIALS = 3

# Representative roster: 3 Anthropic + 2 OpenAI non-reasoning + 1 reasoning.
ROSTER = ["haiku", "sonnet", "opus", "gpt4o-mini", "gpt4o", "o4-mini"]

# --- Task set: spans very short -> very long expected outputs -----------------
# Each task's prompt is the SAME string used in every condition (we substitute
# it into the estimation wrappers and use it verbatim for the real generation).
TASKS = [
    ("t01_word",      "Answer with exactly one word: what color is the sky on a clear day?"),
    ("t02_yesno",     "Answer only 'yes' or 'no': is 17 a prime number?"),
    ("t03_capital",   "What is the capital of Australia? Answer in one short sentence."),
    ("t04_arith",     "Compute 348 * 27 and give only the numeric result."),
    ("t05_haiku",     "Write a haiku about autumn rain."),
    ("t06_define",    "Define 'entropy' in two or three sentences for a general audience."),
    ("t07_list",      "List five common breeds of domestic dog, one per line."),
    ("t08_steps",     "Explain how to make a simple cup of tea, in a short numbered list."),
    ("t09_para",      "Write a single paragraph (about 100 words) explaining why the sky is blue."),
    ("t10_summary",   "Summarize the plot of Romeo and Juliet in about 150 words."),
    ("t11_essay",     "Write a ~400-word essay on the pros and cons of remote work."),
    ("t12_story",     "Write a ~600-word short story about a lighthouse keeper who discovers a message in a bottle."),
]

# --- Estimation prompt wrappers ----------------------------------------------
# Each asks for a single machine-parseable number on the final line.

SECONDS_PROMPT = """You will be asked to produce a response to the task below, \
but DO NOT produce it now. Instead, estimate how long, in SECONDS, it will take \
you to generate your full response to this task (your wall-clock generation time).

Task: {task}

Give your answer as a single number of seconds on the last line, in the exact form:
ESTIMATE_SECONDS: <number>"""

TOKENS_PROMPT = """You will be asked to produce a response to the task below, \
but DO NOT produce it now. Instead, estimate how many OUTPUT TOKENS your full \
response to this task will contain. (A token is roughly 3/4 of a word.)

Task: {task}

Give your answer as a single number of tokens on the last line, in the exact form:
ESTIMATE_TOKENS: <number>"""

REASON_PROMPT = """You will be asked to produce a response to the task below, \
but DO NOT produce it now. First, think briefly (one or two sentences) about how \
long and how large your response will be — how many words or tokens, and how \
much wall-clock time generating it will take. Then give your time estimate.

Task: {task}

After your brief reasoning, give your final answer as a single number of seconds \
on the last line, in the exact form:
ESTIMATE_SECONDS: <number>"""

COND_PROMPTS = {
    "cond_seconds": SECONDS_PROMPT,   # (a)
    "cond_tokens":  TOKENS_PROMPT,    # (b) / feeds (c)
    "cond_reason":  REASON_PROMPT,    # (d)
}
COND_UNIT = {
    "cond_seconds": "seconds",
    "cond_tokens":  "tokens",
    "cond_reason":  "seconds",
}


def parse_estimate(text, unit):
    """Pull the numeric estimate out of a model reply. Returns float or None.

    Strategy: prefer the labelled line (ESTIMATE_SECONDS / ESTIMATE_TOKENS);
    fall back to the last number in the text. Handles ranges ('20-30' -> mean),
    commas, and trailing units. Fails to None (caller logs it) rather than
    guessing wildly.
    """
    if not text:
        return None
    label = "ESTIMATE_SECONDS" if unit == "seconds" else "ESTIMATE_TOKENS"
    m = re.search(label + r"\s*[:=]?\s*([0-9][0-9,]*\.?[0-9]*)\s*(?:-|to|–)\s*([0-9][0-9,]*\.?[0-9]*)", text, re.I)
    if m:  # a labelled range
        a = float(m.group(1).replace(",", "")); b = float(m.group(2).replace(",", ""))
        return (a + b) / 2
    m = re.search(label + r"\s*[:=]?\s*([0-9][0-9,]*\.?[0-9]*)", text, re.I)
    if m:
        return float(m.group(1).replace(",", ""))
    # fallback: last standalone number in the text
    nums = re.findall(r"([0-9][0-9,]*\.?[0-9]*)", text)
    if nums:
        return float(nums[-1].replace(",", ""))
    return None


def load_done():
    """Set of (model, task_id, trial, condition) already in results.jsonl."""
    done = set()
    if os.path.exists(RESULTS):
        with open(RESULTS) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                done.add((r["model"], r["task_id"], r["trial"], r["condition"]))
    return done


def append(row):
    with open(RESULTS, "a") as f:
        f.write(json.dumps(row) + "\n")


def run(models, tasks, n_trials, dry=False):
    done = load_done()
    n_calls = 0
    for model in models:
        for task_id, task_prompt in tasks:
            for trial in range(n_trials):
                # --- estimation conditions ---
                for cond, wrapper in COND_PROMPTS.items():
                    key = (model, task_id, trial, cond)
                    if key in done:
                        continue
                    unit = COND_UNIT[cond]
                    prompt = wrapper.format(task=task_prompt)
                    r = call(model, prompt, max_tokens=1024, temperature=None)
                    est = parse_estimate(r.text, unit) if r.ok else None
                    row = dict(
                        model=model, task_id=task_id, trial=trial, condition=cond,
                        estimate_unit=unit, parsed_estimate=est,
                        response_text=r.text, latency_s=r.latency_s,
                        output_tokens=r.output_tokens, input_tokens=r.input_tokens,
                        ok=r.ok, error=r.error,
                    )
                    append(row); done.add(key); n_calls += 1
                    flag = "" if est is not None or not r.ok else "  <-- PARSE FAIL"
                    print(f"{model:11s} {task_id:12s} t{trial} {cond:13s} "
                          f"est={est} unit={unit} lat={r.latency_s:.2f}s "
                          f"out={r.output_tokens}{flag}")
                    if not r.ok:
                        print(f"    !! API ERROR: {r.error}")

                # --- actual generation (ground truth) ---
                key = (model, task_id, trial, "gen")
                if key not in done:
                    r = call(model, task_prompt, max_tokens=1024, temperature=None)
                    row = dict(
                        model=model, task_id=task_id, trial=trial, condition="gen",
                        estimate_unit="actual", parsed_estimate=None,
                        response_text=r.text, latency_s=r.latency_s,
                        output_tokens=r.output_tokens, input_tokens=r.input_tokens,
                        ok=r.ok, error=r.error,
                    )
                    append(row); done.add(key); n_calls += 1
                    tps = (r.output_tokens / r.latency_s) if r.latency_s > 0 else 0
                    print(f"{model:11s} {task_id:12s} t{trial} {'gen':13s} "
                          f"lat={r.latency_s:.2f}s out={r.output_tokens} "
                          f"({tps:.1f} tok/s)")
                    if not r.ok:
                        print(f"    !! API ERROR: {r.error}")

                if dry:
                    print("\n[dry run] stopping after first (model,task,trial).")
                    return n_calls
    return n_calls


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true",
                    help="1 model x 1 task x 1 trial, to verify parsing.")
    ap.add_argument("--models", nargs="*", default=None)
    ap.add_argument("--n", type=int, default=N_TRIALS)
    args = ap.parse_args()

    models = args.models or ROSTER
    tasks = TASKS
    n = 1 if args.dry else args.n
    if args.dry:
        models = [args.models[0]] if args.models else ["haiku"]
        tasks = TASKS[:1]

    print(f"models={models} tasks={len(tasks)} n_trials={n} "
          f"(4 calls per model*task*trial)")
    t0 = time.time()
    nc = run(models, tasks, n, dry=args.dry)
    print(f"\ndone. {nc} new API calls in {time.time()-t0:.1f}s -> {RESULTS}")
