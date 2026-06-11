# Time Perception

A subjective sense of time built out of interacting oscillations, as a
self-contained dynamical system (no LLM). One oscillator engine, three read-outs:
prospective felt time, retrospective load, and recency/coherence.

## Run

```bash
pip install numpy matplotlib
python experiments.py   # writes stage1_results.png, prints summary
```

## Files

- `oscillators.py` — the engine (`TimePerceptionSystem`, `Params`).
- `experiments.py` — Stage 1 demos + validation.
- `plan.md` — design, staging, and the reasoning behind it.

## Stage 1 results

- **Holiday paradox** reproduced: idle time *drags* in the moment (prospective)
  yet busy time is remembered as *longer* (retrospective). The two read-outs
  disagree by construction of opposite gates — that is the point.
- **Idle detection**: a check-in fires when *felt* idle time crosses a threshold.
- **Scalar property**: SD of estimates is linear in duration (CV flat ~0.15).
  Note: this is *injected* via per-trial rate jitter, not emergent — as expected.

See `plan.md` for what Stage 1b (central tendency, bisection) and Stage 2
(coupling / nested loops) will add.
