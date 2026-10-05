# Self-report of embedding weights

Can a small transformer learn to answer "what is coordinate i of your embedding
of token t?", and when an embedding row is changed after training, do its
answers change with it? Follows on from `../neural-network-quine/`, where the
network's answers about its own weights did not follow changes.

Status: code reviewed and tested; experiments running. See PLAN.md and NOTES.md.

Run: `./run_all.sh` (6 training runs, then `follow_test.py`). Tests: `.venv/bin/python -m pytest -q tests`.
