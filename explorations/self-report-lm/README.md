# Self-report in a small language model

A small GPT-style model trained on TinyStories that also answers "what is
coordinate i of the embedding vector of token t?", first with a number head,
later as text written by the model. Tests whether the answers follow changes of
the embedding vector, and what the self-report costs the language model.
Follows `../self-report-embeddings/`.

Plan and roadmap: PLAN.md. Log: NOTES.md. Results: REPORT.md and REPORT.pdf.

Run (in order of the report):
- `.venv/bin/python prepare.py` (downloads must be in data/, see NOTES.md).
- Sections 4 to 9: `./run_all.sh` (joint and language-model-only runs, seed 0),
  `./run_seed1.sh`, `./run_control.sh`; analyses `measure.py <run>`,
  `analyze_frequency.py`, `analyze_review.py <run> lmonly_s0`, `summarize.py`.
- Section 10 (raising follow): continuations with `finetune.py <source> <name>
  <steps> <lam> <jitter_max> [lr] [slope_weight]` (scripts `run_stage1.sh`,
  `run_fresh.sh`); from scratch with `train.py <name> <lam> <seed> [steps]
  [detach|joint] [jitter_max] [slope_weight]` (`run_phase2.sh`,
  `run_slope_scratch.sh`, `run_slope_lam1.sh`).
- Section 11 (answers as text): `train_text.py`, `finetune_text.py`,
  `measure_text.py <text run> [<number-head reference> ...]` (`run_text_*.sh`).

Tests: `.venv/bin/python -m pytest -q tests`.
