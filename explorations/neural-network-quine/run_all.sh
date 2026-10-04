#!/usr/bin/env bash
# Reproduce every experiment. Runs jobs 4 at a time; each job uses one thread.
# Logs go to logs/, results to results/.
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python
mkdir -p logs
SEEDS="0 1 2"

jobs() {
  # Batch 2. Long jobs first so they start immediately.
  # E3 at full length (paper: 10,000 epochs), two noise levels from the sweep
  echo "hill --sigma 3e-5 --epochs 10000 --log-every 50 --seed 0"
  echo "hill --sigma 1e-5 --epochs 10000 --log-every 50 --seed 0"
  # E4: hill-climbing from the SGD (10 epochs) and Adamax (100 epochs) solutions
  echo "hill --sigma 3e-5 --epochs 1000 --log-every 10 --start results/opt_sgd_10ep_seed0.pt --seed 0"
  echo "hill --sigma 3e-5 --epochs 1000 --log-every 10 --start results/opt_adamax_100ep_seed0.pt --seed 0"
  echo "hill --sigma 1e-5 --epochs 1000 --log-every 10 --start results/opt_sgd_10ep_seed0.pt --seed 0"
  echo "hill --sigma 1e-5 --epochs 1000 --log-every 10 --start results/opt_adamax_100ep_seed0.pt --seed 0"
  # Literal He init, Adamax, 1,000 epochs, 3 seeds: where does R^2 converge?
  for s in $SEEDS; do echo "optimizer --optimizer adamax --epochs 1000 --seed $s --init-literal-he"; done
  # E2 under the paper's literal initialization (100 Adamax epochs)
  echo "optimizer --optimizer adamax --epochs 100 --seed 0 --init-literal-he"
  # Sensitivity to the two main unforced choices (PLAN.md items 3 and 5)
  for flag in --init-literal-he --out-selu; do
    echo "optimizer --optimizer adamax --epochs 30 --seed 0 $flag"
    echo "regen --T 1 --generations 10 --seed 0 $flag"
  done
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

# A job whose log already ends in "wrote results/..." is skipped, so the script can be rerun
# after an interruption. A failing job prints FAILED; the others still run.
jobs | xargs -P 4 -I{} sh -c 'log=logs/$(echo "{}" | tr " /" "__" | tr -d "-").log;
  grep -q "^wrote results" "$log" 2>/dev/null && exit 0;
  '"$PY"' experiments.py {} > "$log" 2>&1 || { echo "FAILED: {}"; exit 1; }' \
  || { echo "some jobs FAILED"; exit 1; }
echo "all jobs done"
