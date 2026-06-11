"""Deduplicate an experiment's results.jsonl by its logical key, keeping the last occurrence.

Needed because collection is append-only with a load_done() resume scheme that is NOT safe
against concurrent writers (see SUMMARY.md process note): if two run.py processes for the same
experiment overlap, duplicate rows appear. This utility makes the data canonical before
analysis. analyze.py scripts also tolerate duplicates, but running this first guarantees exact
counts.

Usage:
    python dedup.py                 # dedup all known experiments
    python dedup.py e5-latency-decoupled   # dedup one

Logical keys per experiment are (model, task/scenario id, trial, condition); E3/E4 use their
own id/gap fields. Edit KEYS if you add an experiment.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

KEYS = {
    "e1-self-duration": ("model", "task_id", "trial", "condition"),
    "e2-token-time": ("model", "task_id", "trial", "condition"),
    "e3-log-gap-probe": ("model", "scenario_id", "gap_label", "trial"),
    "e4-harness-clock": ("model", "scenario_id", "gap_seconds", "condition", "trial"),
    "e5-latency-decoupled": ("model", "task_id", "trial", "condition"),
    "e6-length-bias": ("model", "task_id", "trial", "condition"),
    "e10-reasoning-tokens": ("model", "task_id", "trial", "condition"),
}


def dedup(exp):
    key = KEYS[exp]
    path = os.path.join(HERE, exp, "results.jsonl")
    if not os.path.exists(path):
        print(f"{exp}: no results.jsonl")
        return
    rows = [json.loads(l) for l in open(path) if l.strip()]
    seen = {}
    for r in rows:
        seen[tuple(r.get(k) for k in key)] = r  # keep last
    with open(path, "w") as f:
        for r in seen.values():
            f.write(json.dumps(r) + "\n")
    print(f"{exp}: {len(rows)} -> {len(seen)} rows ({len(rows) - len(seen)} dups removed)")


if __name__ == "__main__":
    targets = sys.argv[1:] or list(KEYS)
    for exp in targets:
        if exp not in KEYS:
            raise SystemExit(f"unknown experiment {exp!r}; pick from {list(KEYS)}")
        dedup(exp)
