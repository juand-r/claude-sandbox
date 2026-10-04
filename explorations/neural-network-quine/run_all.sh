#!/usr/bin/env bash
# Reproduce every experiment. Runs jobs 4 at a time; each job uses one thread.
# Logs go to logs/, results to results/.
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python
mkdir -p logs
SEEDS="0 1 2"

jobs() {
  for s in $SEEDS; do
    # E1 (30 epochs) and E2 (Adamax, 100 epochs; its first 30 epochs are E1's Adamax curve)
    for o in sgd sgd_momentum adam adagrad rmsprop; do echo "optimizer --optimizer $o --epochs 30 --seed $s"; done
    echo "optimizer --optimizer adamax --epochs 100 --seed $s"
    echo "optimizer --optimizer sgd --epochs 10 --seed $s"            # start point for E4
    # E5, E6
    echo "regen --T 1 --generations 10 --seed $s"
    echo "regen --T 0 --generations 10 --seed $s"
    # E7, E8
    echo "aux --epochs 30 --seed $s"
    echo "aux --epochs 30 --task-only --seed $s"
  done
  # E3 sigma sweep (seed 0, 50 epochs)
  for sig in 1e-5 3e-5 1e-4 3e-4 1e-3 3e-3; do echo "hill --sigma $sig --epochs 50 --seed 0"; done
}

jobs | xargs -P 4 -I{} sh -c 'log=logs/$(echo "{}" | tr " " "_" | tr -d "-").log; '"$PY"' experiments.py {} > "$log" 2>&1 || { echo "FAILED: {}"; exit 255; }'
echo "batch 1 done"
