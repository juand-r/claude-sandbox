# Time Perception

A subjective sense of time built out of interacting oscillations, as a
self-contained dynamical system (no LLM). One oscillator engine, three read-outs:
prospective felt time, retrospective load, and recency/coherence.

**Start with `REPORT.md`** for the full write-up of results. `NOTES.md` is the
running findings log; `plan.md` is the design and staging.

## Run

```bash
pip install numpy matplotlib
python experiments.py            # Stage 1: the dissociation + self-reg + scalar
python experiments_stage1b.py    # Stage 1b: SBF substrate vs log observer
python experiments_stage2.py     # Stage 2: coupling (recency vs code collapse)
python experiments_cascade.py    # nested-loop cascade vs incommensurate bank
python robustness.py             # robustness of the dissociation
```
Each writes a `*_results.png` and prints a summary.

## Files

- `oscillators.py` — Stage 1 engine (`TimePerceptionSystem`, `Params`).
- `readouts.py`    — SBF coincidence substrate + log observer (Stage 1b).
- `coupling.py`    — Kuramoto-coupled bank (Stage 2).
- `cascade.py`     — hierarchical odometer cascade (nested loops).
- `experiments*.py`, `robustness.py` — experiments.

## Headline findings

- **Holiday paradox** reproduced and robust: idle drags in the moment, busy is
  remembered as longer. Monotonic across event rate; not a knife-edge.
- **Scalar property** needs *common-mode* (global) rate noise; independent
  per-oscillator noise degrades the code instead.
- **Geometric-mean bisection and Vierordt** come from a *log/ratio observer*, not
  from the oscillator kernel. Oscillations necessary, not sufficient.
- **Coupling** helps recency only in a narrow weak window (K~6-8); past the
  synchronization transition it collapses the multi-scale code.
- **Cascade vs bank**: compact+exact+brittle vs robust+bounded — capacity trades
  off against robustness.
