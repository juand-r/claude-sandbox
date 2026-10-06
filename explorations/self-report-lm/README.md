# Self-report in a small language model

A small GPT-style model trained on TinyStories that also answers "what is
coordinate i of the embedding vector of token t?" with a number head. Tests
whether the answers follow changes of the embedding (reading) and what the
self-report costs the language model. Follows `../self-report-embeddings/`.

Plan and roadmap: PLAN.md. Log: NOTES.md. Results: REPORT.md and REPORT.pdf.

Run: `.venv/bin/python prepare.py` (downloads must be in data/, see NOTES.md),
then `./run_all.sh` (joint and language-model-only runs, seed 0), `./run_seed1.sh`,
`./run_control.sh`; analyses: `analyze_frequency.py`, `analyze_review.py`, `summarize.py`. Tests: `.venv/bin/python -m pytest -q tests`.
