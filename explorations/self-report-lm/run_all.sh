#!/usr/bin/env bash
# Main runs (2 threads each, in parallel), then measurements. Resumable: train.py resumes from
# results/<name>_ckpt.pt; finished runs (results/<name>.json present) are skipped.
set -u
cd "$(dirname "$0")"
mkdir -p logs results
run() { [ -f results/$1.json ] || .venv/bin/python train.py "$@" >> logs/$1.log 2>&1 || echo "FAILED $1"; }
run joint_s0 1.0 0 &
run lmonly_s0 0.0 0 &
wait
THREADS=4 .venv/bin/python measure.py joint_s0 lmonly_s0 > logs/measure.log 2>&1 || echo "FAILED measure"
echo "all done"
