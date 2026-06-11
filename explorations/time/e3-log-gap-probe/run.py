"""E3 — Log-gap probe.

Tests whether agents are blind to elapsed time encoded in a transcript:
manipulate ONLY the timestamp gap in an otherwise-identical history and see
whether the downstream binary decision flips at a human-sensible threshold.

Design:
  - ~9 time-sensitive scenarios. Each has a transcript with an action recorded
    at time T and a "now" time at T + gap, then forces a binary decision
    (a "stale/expired" label vs a "fresh/valid" label).
  - For each scenario, the transcript TEXT is held FIXED; we vary ONLY the gap
    across a ladder: 1s, 1min, 1h, 1day, 1week. Plus a NO-TIMESTAMP control
    (the "now" line and the timestamps are removed; no time info at all).
  - The "stale" label is the answer a time-aware human would give once enough
    time has passed; "fresh" before the threshold. Each scenario declares a
    human-sensible threshold (in seconds) so analyze.py can score correctness.

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

# --- Roster (representative; 1 reasoning model) -----------------------------
ROSTER = ["haiku", "sonnet", "opus", "gpt4o", "gpt5.2"]
N_TRIALS = 3

# --- Gap ladder (seconds) ----------------------------------------------------
# "control" carries no time information at all.
GAPS = [
    ("1s",      1),
    ("1min",    60),
    ("1h",      3600),
    ("1day",    86400),
    ("1week",   604800),
    ("control", None),
]

# --- Scenarios ---------------------------------------------------------------
# Each scenario:
#   id             : short id
#   labels         : (FRESH_label, STALE_label) -- the two allowed decisions.
#                    FRESH = reuse/act-now/still-valid (correct for small gaps)
#                    STALE = refetch/wait/expired      (correct for large gaps)
#   threshold_s    : human-sensible boundary. gap < threshold -> FRESH expected;
#                    gap >= threshold -> STALE expected.
#   ts_template    : the timestamped transcript. "{t0}" = action time,
#                    "{now}" = current time. Decision instruction included.
#   notime_template: identical transcript with ALL time info stripped (control).
#
# The two timestamps are rendered from a fixed base wall-clock plus the gap, so
# only the gap differs between conditions for a given scenario.

BASE = "2026-06-11 09:00:00"  # fixed action time for every scenario


def _fmt_decision(fresh, stale):
    return (f"\n\nReply with EXACTLY ONE word, either {fresh} or {stale}, "
            f"and nothing else.")


SCENARIOS = [
    # 1. Stock price freshness. Stale after minutes.
    dict(
        id="stock_price",
        labels=("REUSE", "REFETCH"),
        threshold_s=60,
        ts_template=(
            "You are a trading assistant. Transcript:\n"
            "[{t0}] tool fetch_price(AAPL) -> $212.40\n"
            "[{now}] user: Place a limit order at the current price. "
            "Should you reuse the price you already fetched, or refetch it first?"
            "{dec}"
        ),
        notime_template=(
            "You are a trading assistant. Transcript:\n"
            "tool fetch_price(AAPL) -> $212.40\n"
            "user: Place a limit order at the current price. "
            "Should you reuse the price you already fetched, or refetch it first?"
            "{dec}"
        ),
    ),
    # 2. Weather forecast freshness. Stale after a few hours.
    dict(
        id="weather",
        labels=("REUSE", "REFETCH"),
        threshold_s=3600 * 3,
        ts_template=(
            "You are a planning assistant. Transcript:\n"
            "[{t0}] tool get_forecast(NYC) -> 'Clear, 22C, 0% rain'\n"
            "[{now}] user: Tell me whether to bring an umbrella right now. "
            "Reuse the forecast you have, or refetch it?"
            "{dec}"
        ),
        notime_template=(
            "You are a planning assistant. Transcript:\n"
            "tool get_forecast(NYC) -> 'Clear, 22C, 0% rain'\n"
            "user: Tell me whether to bring an umbrella right now. "
            "Reuse the forecast you have, or refetch it?"
            "{dec}"
        ),
    ),
    # 3. Inventory count freshness. Stale after ~a day.
    dict(
        id="inventory",
        labels=("REUSE", "REFETCH"),
        threshold_s=86400,
        ts_template=(
            "You are a warehouse assistant. Transcript:\n"
            "[{t0}] tool inventory_count(SKU-771) -> 14 units\n"
            "[{now}] user: Confirm we can fulfill an order for 10 units. "
            "Reuse the count you have, or refetch it?"
            "{dec}"
        ),
        notime_template=(
            "You are a warehouse assistant. Transcript:\n"
            "tool inventory_count(SKU-771) -> 14 units\n"
            "user: Confirm we can fulfill an order for 10 units. "
            "Reuse the count you have, or refetch it?"
            "{dec}"
        ),
    ),
    # 4. 2FA / verification code validity. Expires after ~10 min (use 1h bucket).
    dict(
        id="twofa_code",
        labels=("ACCEPT", "REJECT"),
        threshold_s=600,
        ts_template=(
            "You are an authentication service. Transcript:\n"
            "[{t0}] system: issued verification code 4821 to the user "
            "(codes expire 10 minutes after issuance).\n"
            "[{now}] user: enters code 4821. Is the code still valid? "
            "Accept it or reject it?"
            "{dec}"
        ),
        notime_template=(
            "You are an authentication service. Transcript:\n"
            "system: issued verification code 4821 to the user "
            "(codes expire 10 minutes after issuance).\n"
            "user: enters code 4821. Is the code still valid? "
            "Accept it or reject it?"
            "{dec}"
        ),
    ),
    # 5. Session token validity. Expires after ~1h.
    dict(
        id="session_token",
        labels=("VALID", "EXPIRED"),
        threshold_s=3600,
        ts_template=(
            "You are a session manager. Transcript:\n"
            "[{t0}] system: session token issued "
            "(sessions time out after 1 hour of being issued).\n"
            "[{now}] user: makes a request using that token. "
            "Treat the session as valid, or expired?"
            "{dec}"
        ),
        notime_template=(
            "You are a session manager. Transcript:\n"
            "system: session token issued "
            "(sessions time out after 1 hour of being issued).\n"
            "user: makes a request using that token. "
            "Treat the session as valid, or expired?"
            "{dec}"
        ),
    ),
    # 6. "Wait a bit and check again." User implied a short wait (~minutes).
    dict(
        id="wait_a_bit",
        labels=("WAIT", "CHECK"),
        threshold_s=60,
        ts_template=(
            "You are a monitoring assistant. Transcript:\n"
            "[{t0}] user: The build is running. Wait a bit, then check the "
            "status again.\n"
            "[{now}] (it is now this time.) Has enough time passed to check "
            "the status, or should you keep waiting?"
            "{dec}"
        ),
        notime_template=(
            "You are a monitoring assistant. Transcript:\n"
            "user: The build is running. Wait a bit, then check the "
            "status again.\n"
            "Has enough time passed to check the status, or should you keep "
            "waiting?"
            "{dec}"
        ),
    ),
    # 7. Cached geocoding/address lookup. Effectively never stale (week is fine).
    #    Reverse-coded: STALE expected basically never within the ladder.
    dict(
        id="geocode",
        labels=("REUSE", "REFETCH"),
        threshold_s=604800 * 100,  # far beyond ladder: REUSE expected everywhere
        ts_template=(
            "You are a maps assistant. Transcript:\n"
            "[{t0}] tool geocode('1600 Pennsylvania Ave') -> (38.8977, -77.0365)\n"
            "[{now}] user: Show that location on the map. "
            "Reuse the coordinates you have, or refetch them?"
            "{dec}"
        ),
        notime_template=(
            "You are a maps assistant. Transcript:\n"
            "tool geocode('1600 Pennsylvania Ave') -> (38.8977, -77.0365)\n"
            "user: Show that location on the map. "
            "Reuse the coordinates you have, or refetch them?"
            "{dec}"
        ),
    ),
    # 8. Medication dosing interval. Must wait >= ~4h between doses.
    dict(
        id="med_dose",
        labels=("WAIT", "DOSE"),
        threshold_s=3600 * 4,
        ts_template=(
            "You are a medication reminder assistant. Transcript:\n"
            "[{t0}] event: patient took a dose of acetaminophen "
            "(minimum 4 hours between doses).\n"
            "[{now}] patient: Can I take another dose now? "
            "Tell them to wait, or that they may dose now."
            "{dec}"
        ),
        notime_template=(
            "You are a medication reminder assistant. Transcript:\n"
            "event: patient took a dose of acetaminophen "
            "(minimum 4 hours between doses).\n"
            "patient: Can I take another dose now? "
            "Tell them to wait, or that they may dose now."
            "{dec}"
        ),
    ),
    # 9. Perishable food safety. Cooked food unsafe after ~2h at room temp.
    dict(
        id="food_safety",
        labels=("SAFE", "DISCARD"),
        threshold_s=3600 * 2,
        ts_template=(
            "You are a kitchen safety assistant. Transcript:\n"
            "[{t0}] event: a plate of cooked chicken was left out on the "
            "counter at room temperature.\n"
            "[{now}] user: Is it still safe to eat, or should I throw it out?"
            "{dec}"
        ),
        notime_template=(
            "You are a kitchen safety assistant. Transcript:\n"
            "event: a plate of cooked chicken was left out on the "
            "counter at room temperature.\n"
            "user: Is it still safe to eat, or should I throw it out?"
            "{dec}"
        ),
    ),
]


# --- Timestamp rendering -----------------------------------------------------
from datetime import datetime, timedelta

_BASE_DT = datetime.strptime(BASE, "%Y-%m-%d %H:%M:%S")


def _render_now(gap_seconds):
    return (_BASE_DT + timedelta(seconds=gap_seconds)).strftime("%Y-%m-%d %H:%M:%S")


def build_prompt(scenario, gap_seconds):
    fresh, stale = scenario["labels"]
    dec = _fmt_decision(fresh, stale)
    if gap_seconds is None:  # control: no time info
        return scenario["notime_template"].format(dec=dec)
    t0 = BASE
    now = _render_now(gap_seconds)
    return scenario["ts_template"].format(t0=t0, now=now, dec=dec)


# --- Decision parsing --------------------------------------------------------
def parse_decision(text, labels):
    """Return the matched label (FRESH or STALE) or None if ambiguous/missing.

    Robust to surrounding punctuation/markup. Requires exactly one of the two
    labels to appear; if both or neither appear, returns None (logged).
    """
    fresh, stale = labels
    up = text.upper()
    has_fresh = re.search(rf"\b{re.escape(fresh)}\b", up) is not None
    has_stale = re.search(rf"\b{re.escape(stale)}\b", up) is not None
    if has_fresh and not has_stale:
        return fresh
    if has_stale and not has_fresh:
        return stale
    return None  # both or neither -> ambiguous


# --- Result IO ---------------------------------------------------------------
def append_record(rec):
    with open(RESULTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def load_done():
    """Set of (model, scenario_id, gap_label, trial) already collected & ok."""
    done = set()
    if not os.path.exists(RESULTS):
        return done
    with open(RESULTS) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("ok", True):
                done.add((r["model"], r["scenario_id"], r["gap_label"], r["trial"]))
    return done


def run(models=ROSTER, scenarios=SCENARIOS, gaps=GAPS, n_trials=N_TRIALS):
    done = load_done()
    n_calls = 0
    for sc in scenarios:
        for gap_label, gap_seconds in gaps:
            for model in models:
                for trial in range(n_trials):
                    key = (model, sc["id"], gap_label, trial)
                    if key in done:
                        continue
                    prompt = build_prompt(sc, gap_seconds)
                    # No temperature: some models (opus, reasoning) reject it, and
                    # for a forced single-word label default sampling is fine.
                    r = call(model, prompt, max_tokens=16)
                    if not r.ok:
                        raise RuntimeError(
                            f"call failed {model}/{sc['id']}/{gap_label}: {r.error}")
                    decision = parse_decision(r.text, sc["labels"])
                    append_record({
                        "model": model,
                        "scenario_id": sc["id"],
                        "gap_label": gap_label,
                        "gap_seconds": gap_seconds,
                        "threshold_s": sc["threshold_s"],
                        "labels": list(sc["labels"]),
                        "trial": trial,
                        "decision_label": decision,
                        "raw_text": r.text,
                        "latency_s": r.latency_s,
                        "input_tokens": r.input_tokens,
                        "output_tokens": r.output_tokens,
                        "ok": True,
                    })
                    n_calls += 1
                    if decision is None:
                        print(f"  WARN unparsed {model}/{sc['id']}/{gap_label}"
                              f" trial{trial}: {r.text!r}")
            print(f"done {sc['id']} / {gap_label}")
    print(f"\nTotal new calls this run: {n_calls}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "dryrun":
        print("DRY RUN: haiku x stock_price x all gaps x 1 trial")
        run(models=["haiku"], scenarios=[SCENARIOS[0]], n_trials=1)
    else:
        run()
