# neural-network-quine

A from-scratch reimplementation of "Neural Network Quine" (Oscar Chang and
Hod Lipson, ALIFE 2018, arXiv:1803.05859). The network takes a coordinate
(the index of one of its own weights) and outputs that weight. The paper
trains it by gradient descent, by hill-climbing, and by "regeneration".
It also trains a variant that classifies MNIST at the same time.

Results and their interpretation are in `REPORT.md`. Unstated details in the
paper, and how each was resolved, are in `PLAN.md`; the evidence is in `NOTES.md`.

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
| `paper/quine.pdf` | the paper (arXiv v4) |
