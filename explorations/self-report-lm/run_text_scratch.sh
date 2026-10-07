#!/usr/bin/env bash
# Text answers from scratch with perturbed questions (0.5) and λ = 4; then the full text measurement,
# compared with the number-head control, ft_slope and control_slope_s0.
set -u
cd "$(dirname "$0")"
n=text_scratch_jit
[ -f results/$n.json ] || .venv/bin/python train_text.py $n 4 0 15000 0.5 >> logs/$n.log 2>&1 || { echo "FAILED $n"; exit 1; }
[ -f results/measure_$n.json ] || THREADS=2 .venv/bin/python measure_text.py $n joint_detached_s0 ft_slope control_slope_s0 >> logs/measure_$n.log 2>&1 || echo "FAILED measure $n"
echo "text scratch done"
