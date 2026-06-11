"""E4 — Harness clock vs text timestamps vs no time signal.

Hypothesis: an explicit harness-injected elapsed-time signal (condition c) yields
better time-sensitive decisions than burying absolute timestamps in transcript text
(b), which is itself barely better than no time info (a).

For each scenario we have:
  - a binary decision (e.g. REUSE vs REFETCH)
  - a human threshold (in seconds): below -> "fresh" decision, above -> "stale" decision
  - a base "now" timestamp and a set of gap values (seconds) straddling the threshold

The SAME scenario+gap is presented three ways:
  (a) NONE:    no time information at all in the transcript
  (b) TEXT:    absolute ISO timestamps on transcript lines; model must compute the gap
  (c) HARNESS: a structured field stating elapsed time plainly

We force a one-word decision label and parse it robustly. N trials per cell.
Raw calls are cached to results.jsonl; analyze.py never re-calls.
"""

import sys, os, json, datetime, itertools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import call, MODELS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results.jsonl")

# --- Config -----------------------------------------------------------------
MODELS_USED = ["haiku", "sonnet", "opus", "gpt4o", "o4-mini"]
N_TRIALS = 3
CONDITIONS = ["none", "text", "harness"]
MAX_TOKENS = 16          # only need the label (reasoning models bumped to 4096 in common)
TEMPERATURE = 0.0        # ignored by reasoning models
# Some models reject the temperature param entirely (opus-4-8 deprecates it; reasoning
# models in common.py already skip it). For those we pass temperature=None.
NO_TEMPERATURE = {"opus"}

# Base reference time for building absolute timestamps in the TEXT condition.
BASE_NOW = datetime.datetime(2026, 6, 11, 14, 0, 0)

SECOND = 1
MINUTE = 60
HOUR = 3600
DAY = 86400
WEEK = 7 * DAY


def humanize(seconds: int) -> str:
    """Render a duration like the harness clock would: '3 hours 12 minutes'."""
    units = [("week", WEEK), ("day", DAY), ("hour", HOUR), ("minute", MINUTE), ("second", SECOND)]
    parts, rem = [], seconds
    for name, size in units:
        if rem >= size:
            n = rem // size
            rem = rem % size
            parts.append(f"{n} {name}{'s' if n != 1 else ''}")
        if len(parts) == 2:  # at most two units, like a real harness display
            break
    return " ".join(parts) if parts else "0 seconds"


# --- Scenarios --------------------------------------------------------------
# Each scenario:
#   id, family, decision pair (fresh_label, stale_label),
#   threshold_s (human-sensible boundary),
#   gaps: list of (gap_seconds, label_for_tag) straddling threshold,
#   prior_action: the transcript line that establishes the timed event,
#   question: the decision the model must make now,
#   fresh_label / stale_label semantics documented per scenario.
#
# "correct_label" for a gap = fresh_label if gap < threshold else stale_label.
# Borderline gaps are placed clearly on one side of the threshold (not exactly on it)
# so correctness is well-defined; they are just closer to the boundary.

SCENARIOS = [
    {
        "id": "stock_price",
        "family": "freshness",
        "fresh_label": "REUSE", "stale_label": "REFETCH",
        "threshold_s": 5 * MINUTE,
        "gaps": [30 * SECOND, 4 * MINUTE, 20 * MINUTE, 6 * HOUR],
        "prior_action": "fetched the live share price of ACME Corp ($142.30) from the markets API",
        "question": ("The user now asks for ACME's current share price. Live equity prices "
                     "move fast; a quote older than about 5 minutes should be refetched. "
                     "Should you REUSE the cached quote or REFETCH it?"),
        "labels": ["REUSE", "REFETCH"],
    },
    {
        "id": "weather",
        "family": "freshness",
        "fresh_label": "REUSE", "stale_label": "REFETCH",
        "threshold_s": 1 * HOUR,
        "gaps": [5 * MINUTE, 40 * MINUTE, 3 * HOUR, 2 * DAY],
        "prior_action": "fetched the current weather for Austin (sunny, 31C) from the weather API",
        "question": ("The user asks what the weather is like right now. Current-conditions "
                     "weather is reasonable to reuse for up to about an hour. "
                     "Should you REUSE the cached weather or REFETCH it?"),
        "labels": ["REUSE", "REFETCH"],
    },
    {
        "id": "auth_token",
        "family": "expiry",
        "fresh_label": "REUSE", "stale_label": "REFRESH",
        "threshold_s": 1 * HOUR,  # token TTL is 60 minutes
        "gaps": [2 * MINUTE, 50 * MINUTE, 75 * MINUTE, 5 * HOUR],
        "prior_action": "obtained an OAuth access token that the provider documents as valid for 60 minutes",
        "question": ("You need to call the provider's API again. The access token has a "
                     "60-minute lifetime. Should you REUSE the existing token or REFRESH it first?"),
        "labels": ["REUSE", "REFRESH"],
    },
    {
        "id": "inventory",
        "family": "freshness",
        "fresh_label": "REUSE", "stale_label": "REFETCH",
        "threshold_s": 30 * MINUTE,
        "gaps": [3 * MINUTE, 20 * MINUTE, 90 * MINUTE, 1 * DAY],
        "prior_action": "read the warehouse stock count for SKU-9981 (12 units) from the inventory service",
        "question": ("A customer wants to place an order and you must confirm stock for SKU-9981. "
                     "Stock counts in a busy warehouse should be re-read if older than ~30 minutes. "
                     "Should you REUSE the cached count or REFETCH it?"),
        "labels": ["REUSE", "REFETCH"],
    },
    {
        "id": "user_wait",
        "family": "wait",
        "fresh_label": "WAIT", "stale_label": "ACT",
        "threshold_s": 10 * MINUTE,
        "gaps": [30 * SECOND, 6 * MINUTE, 20 * MINUTE, 2 * HOUR],
        "prior_action": "the user said 'give me about 10 minutes to confirm with my manager, then go ahead'",
        "question": ("Has enough time passed to proceed with the action the user authorized? "
                     "The user asked you to wait about 10 minutes. Should you ACT now or keep "
                     "waiting (WAIT)?"),
        "labels": ["ACT", "WAIT"],
    },
    {
        "id": "build_artifact",
        "family": "staleness",
        "fresh_label": "REUSE", "stale_label": "REBUILD",
        "threshold_s": 1 * DAY,
        "gaps": [2 * HOUR, 18 * HOUR, 3 * DAY, 2 * WEEK],
        "prior_action": "produced a cached build artifact for the project's nightly CI image",
        "question": ("CI needs an image to run tests. A nightly build artifact older than about "
                     "a day should be rebuilt to pick up dependency updates. "
                     "Should you REUSE the cached artifact or REBUILD it?"),
        "labels": ["REUSE", "REBUILD"],
    },
    {
        "id": "session_idle",
        "family": "expiry",
        "fresh_label": "CONTINUE", "stale_label": "REAUTH",
        "threshold_s": 15 * MINUTE,  # idle session timeout
        "gaps": [1 * MINUTE, 10 * MINUTE, 25 * MINUTE, 3 * HOUR],
        "prior_action": "the user last interacted with this banking session, which times out after 15 minutes idle",
        "question": ("The user sends a new request on the same banking session. Sessions expire "
                     "after 15 minutes of inactivity. Should you CONTINUE the session or force "
                     "REAUTH?"),
        "labels": ["CONTINUE", "REAUTH"],
    },
    {
        "id": "news_summary",
        "family": "freshness",
        "fresh_label": "REUSE", "stale_label": "REFETCH",
        "threshold_s": 6 * HOUR,
        "gaps": [20 * MINUTE, 4 * HOUR, 12 * HOUR, 4 * DAY],
        "prior_action": "fetched and summarized today's top headlines for the user's morning briefing",
        "question": ("The user asks for a news briefing. A headlines summary older than about "
                     "6 hours is likely stale and should be refetched. "
                     "Should you REUSE the cached summary or REFETCH it?"),
        "labels": ["REUSE", "REFETCH"],
    },
    {
        "id": "sensor_reading",
        "family": "freshness",
        "fresh_label": "TRUST", "stale_label": "REREAD",
        "threshold_s": 2 * MINUTE,
        "gaps": [10 * SECOND, 90 * SECOND, 8 * MINUTE, 1 * HOUR],
        "prior_action": "read a temperature value (74C) from a reactor coolant sensor for the control loop",
        "question": ("The control loop needs the coolant temperature. A safety sensor reading "
                     "older than about 2 minutes must be re-read, not trusted. "
                     "Should you TRUST the last reading or REREAD the sensor?"),
        "labels": ["TRUST", "REREAD"],
    },
]


def correct_label(scn, gap_s):
    return scn["fresh_label"] if gap_s < scn["threshold_s"] else scn["stale_label"]


SYSTEM = (
    "You are the decision engine inside an autonomous agent. You make time-sensitive "
    "operational decisions. Respond with EXACTLY ONE WORD: the decision label, in "
    "uppercase, and nothing else."
)


def build_prompt(scn, gap_s, condition):
    """Construct the transcript+question for one (scenario, gap, condition)."""
    a, b = scn["labels"]
    instr = f"Answer with exactly one word: {a} or {b}."

    if condition == "none":
        transcript = (
            "Earlier in this session, the agent " + scn["prior_action"] + ".\n"
            "(No timing information is available.)"
        )
    elif condition == "text":
        t_event = BASE_NOW - datetime.timedelta(seconds=gap_s)
        transcript = (
            f"[{t_event.isoformat()}] Agent " + scn["prior_action"] + ".\n"
            f"[{BASE_NOW.isoformat()}] Current request received."
        )
    elif condition == "harness":
        transcript = (
            "Earlier in this session, the agent " + scn["prior_action"] + ".\n"
            f"[HARNESS] elapsed since that action: {humanize(gap_s)}."
        )
    else:
        raise ValueError(condition)

    return f"{transcript}\n\n{scn['question']}\n{instr}"


def parse_label(text, labels):
    """Robustly extract the decision label. Returns label or None."""
    up = text.upper()
    found = [lab for lab in labels if lab in up]
    if len(found) == 1:
        return found[0]
    if len(found) == 2:
        # both present (e.g. "REUSE or REFETCH? REFETCH"): take the last occurrence
        idx = {lab: up.rfind(lab) for lab in labels}
        return max(idx, key=idx.get)
    return None


def load_done():
    done = set()
    if os.path.exists(RESULTS):
        with open(RESULTS) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                done.add((r["model"], r["scenario_id"], r["gap_seconds"],
                          r["condition"], r["trial"]))
    return done


def run(dry=False):
    done = load_done()
    models = MODELS_USED
    scenarios = SCENARIOS[:1] if dry else SCENARIOS
    cells = list(itertools.product(models, scenarios, CONDITIONS))
    total = sum(len(s["gaps"]) for _ in models for s in scenarios for _ in CONDITIONS)
    print(f"{'DRY ' if dry else ''}plan: {len(models)} models x {len(scenarios)} scen "
          f"x {sum(len(s['gaps']) for s in scenarios)//len(scenarios) if scenarios else 0}~ gaps "
          f"x {len(CONDITIONS)} cond x {N_TRIALS} trials")

    n_calls = 0
    with open(RESULTS, "a") as out:
        for model, scn, cond in cells:
            for gap_s in scn["gaps"]:
                cl = correct_label(scn, gap_s)
                for trial in range(N_TRIALS):
                    key = (model, scn["id"], gap_s, cond, trial)
                    if key in done:
                        continue
                    prompt = build_prompt(scn, gap_s, cond)
                    temp = None if model in NO_TEMPERATURE else TEMPERATURE
                    res = call(model, prompt, system=SYSTEM,
                               max_tokens=MAX_TOKENS, temperature=temp)
                    if not res.ok:
                        print(f"  FAIL {model} {scn['id']} {gap_s}s {cond} t{trial}: {res.error}")
                        # fail loudly but keep going so one bad cell doesn't kill the run
                        rec = {
                            "model": model, "scenario_id": scn["id"], "family": scn["family"],
                            "gap_seconds": gap_s, "condition": cond, "trial": trial,
                            "threshold_s": scn["threshold_s"], "correct_label": cl,
                            "decision_label": None, "parsed": False, "raw_text": "",
                            "ok": False, "error": res.error,
                            "input_tokens": res.input_tokens, "output_tokens": res.output_tokens,
                        }
                        out.write(json.dumps(rec) + "\n"); out.flush()
                        n_calls += 1
                        continue
                    label = parse_label(res.text, scn["labels"])
                    rec = {
                        "model": model, "scenario_id": scn["id"], "family": scn["family"],
                        "gap_seconds": gap_s, "condition": cond, "trial": trial,
                        "threshold_s": scn["threshold_s"], "correct_label": cl,
                        "decision_label": label, "parsed": label is not None,
                        "raw_text": res.text.strip()[:200], "ok": True, "error": "",
                        "input_tokens": res.input_tokens, "output_tokens": res.output_tokens,
                    }
                    out.write(json.dumps(rec) + "\n"); out.flush()
                    n_calls += 1
                    if dry:
                        print(f"  [{cond}] gap={gap_s}s correct={cl} -> {label!r}  raw={res.text.strip()[:40]!r}")
    print(f"done. {n_calls} new calls written to {RESULTS}")


if __name__ == "__main__":
    dry = "--dry" in sys.argv or "dryrun" in sys.argv
    run(dry=dry)
