#!/usr/bin/env bash
# All runs of the first version: 2 conditions x 3 seeds, 4 at a time, then the measurements.
# Logs in logs/; results in results/. Skips runs whose results already exist.
set -u
cd "$(dirname "$0")"
mkdir -p logs results
for c in fixed trained; do for s in 0 1 2; do echo "$c $s"; done; done |
  xargs -P 4 -L 1 bash -c '[ -f results/${0}_seed${1}.json ] || .venv/bin/python train.py $0 $1 > logs/${0}_seed${1}.log 2>&1 || echo "FAILED $0 $1"'
.venv/bin/python follow_test.py > logs/follow_test.log 2>&1 || echo "FAILED follow_test"
echo "all done"
