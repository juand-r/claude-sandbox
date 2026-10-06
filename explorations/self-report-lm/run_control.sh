#!/usr/bin/env bash
# Control: joint training with the self-report's input detached (seed 0, same text order),
# then its measurements and review checks.
set -u
cd "$(dirname "$0")"
[ -f results/joint_detached_s0.json ] || .venv/bin/python train.py joint_detached_s0 1.0 0 15000 detach >> logs/joint_detached_s0.log 2>&1 || echo "FAILED control"
THREADS=2 .venv/bin/python measure.py joint_detached_s0 > logs/measure_control.log 2>&1 || echo "FAILED measure control"
.venv/bin/python analyze_review.py joint_detached_s0 lmonly_s0 > logs/review_checks_control.log 2>&1 || echo "FAILED checks control"
echo "control done"
