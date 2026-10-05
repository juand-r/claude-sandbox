#!/usr/bin/env bash
# Vocabulary sweep: V = 256, 1024, 4096 tokens (a quarter held out), 2 conditions x 3 seeds,
# each with the same 72,000 optimizer steps as the V = 64 runs; 4 runs at a time; then the
# measurements (results/follow_test.json, skipping runs already measured).
set -u
cd "$(dirname "$0")"
mkdir -p logs results
for V in 4096 1024 256; do for c in fixed trained; do for s in 0 1 2; do echo "$c $s $V"; done; done; done |
  xargs -P 4 -L 1 bash -c '[ -f results/${0}_V${2}_seed${1}.json ] || .venv/bin/python train.py $0 $1 $2 > logs/${0}_V${2}_seed${1}.log 2>&1 || echo "FAILED $0 $1 $2"'
.venv/bin/python follow_test.py > logs/follow_test_vocab.log 2>&1 || echo "FAILED follow_test"
echo "all done"
