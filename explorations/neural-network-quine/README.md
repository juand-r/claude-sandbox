# neural-network-quine

A from-scratch reimplementation of "Neural Network Quine" (Oscar Chang and
Hod Lipson, ALIFE 2018, arXiv:1803.05859). The network takes a coordinate
(the index of one of its own weights) and outputs that weight. The paper
trains it by gradient descent, by hill-climbing, and by "regeneration".
It also trains a variant that classifies MNIST at the same time.

## Documents

| file | contents |
|---|---|
| `REPORT.md` | findings: Part I reproduces the paper, Part II makes the quine copy itself (best R² 0.987) |
| `EXPERIMENTS.md` | definitions of every variant, and a generated registry of every run with its settings and results |
| `IDEAS.md` | ideas and plans, with results recorded as they came in |
| `PLAN.md` | the paper's unstated details and how each was resolved |
| `NOTES.md` | working log, including mistakes and lost runs |

Trained networks are in `results/weights/` (load with `quine.load_weights`).

## Run

    python3 -m venv .venv
    .venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
    .venv/bin/pip install numpy matplotlib pytest
    # MNIST: the four *-ubyte.gz files into data/mnist/
    #   (e.g. from https://ossci-datasets.s3.amazonaws.com/mnist/)
    .venv/bin/python -m pytest tests
    ./run_all.sh                 # all experiments, 4 jobs at a time, CPU only
    .venv/bin/python plots.py    # figures/

`requirements.txt` pins the versions used.

## Files

| file | contents |
|---|---|
| `quine.py` | model, losses, the three training methods, MNIST loader |
| `experiments.py` | one subcommand per experiment; writes `results/*.json` |
| `run_all.sh` | every run reported in REPORT.md |
| `plots.py` | figures from `results/` |
| `tests/test_quine.py` | coordinate mapping, forward pass vs explicit one-hot, loss vs brute force, regeneration, hill-climbing acceptance, snapshot targets |
| `newton.py` | pure and damped Newton (Levenberg–Marquardt) on the quine equations |
| `export_weights.py` | compact, verified checkpoints in `results/weights/` |
| `registry.py` | the run registry in `EXPERIMENTS.md` |
| `diag_*.py` | diagnostics referenced in `REPORT.md` |
| `paper/quine.pdf` | the paper (arXiv v4) |
