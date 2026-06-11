# time

Exploration of **LLM perception of time** — temporal self-awareness, duration
estimation, time-aware agents, and continuity over long horizons.

## Contents

- `research-notes.md` — Compiled literature notes and reading list (the seed doc).
- `experiments.md` — The four-experiment scoping plan.
- `SUMMARY.md` — **Cross-experiment synthesis and recommendation. Start here for results.**
- `direction-train-it-in.md` — Counterpoint direction: treat E4's sensor as a *ceiling* and
  train the time skill in; measure how much of the gap the model internalizes.
- `common.py` — Shared LLM-call helper (unified Anthropic/OpenAI, latency + token usage).
- `e1-self-duration/` — Can a model estimate its own generation time? (lane: self-perception)
- `e2-token-time/` — Is length-space better-calibrated than second-space? (self-perception)
- `e3-log-gap-probe/` — Are agents blind to timestamp gaps? (lane: time-aware agency)
- `e4-harness-clock/` — Does an injected elapsed-time field beat text timestamps? (agency)

Each `eN-*/` has `run.py` (collect → `results.jsonl`), `analyze.py` (stats + PNG figures),
and `REPORT.md` (findings + verdict).

## Headline

LLMs have **no internal clock** — they have an output-length estimator (E1, E2), and they
act on elapsed time only when it is supplied explicitly (E3, E4). The harness clock lifts
correct time-sensitive decisions from 0.49 → 0.96. **Recommendation: pursue lane 3
(time-aware agency); the fix is a sensor, not training.** See `SUMMARY.md`.

## Running

`.venv/` has the deps (anthropic, openai, numpy, pandas, scipy, matplotlib). Needs
`ANTHROPIC_API_KEY` and `OPENAI_API_KEY`. From an experiment dir:
`../.venv/bin/python run.py` (resumes from existing `results.jsonl`), then `analyze.py`.

## Status

All four experiments complete. See `SUMMARY.md`.
