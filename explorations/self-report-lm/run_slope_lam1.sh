#!/usr/bin/env bash
# Ablation of control_slope_s0: the same from-scratch recipe with λ = 1 instead of 4
# (perturbed questions 0.5, slope loss 1). Then the full measurement and review checks.
set -u
cd "$(dirname "$0")"
n=control_slope_lam1_s0
[ -f results/$n.json ] || .venv/bin/python train.py $n 1 0 15000 detach 0.5 1 >> logs/$n.log 2>&1 || { echo "FAILED $n"; exit 1; }
[ -f results/measure_$n.json ] || THREADS=2 .venv/bin/python measure.py $n >> logs/measure_$n.log 2>&1 || echo "FAILED measure $n"
[ -f results/review_checks_$n.json ] || .venv/bin/python analyze_review.py $n lmonly_s0 >> logs/review_$n.log 2>&1 || echo "FAILED review $n"
echo "slope lam1 done"
