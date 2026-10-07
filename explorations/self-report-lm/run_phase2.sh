#!/usr/bin/env bash
# Stage 1 phase 2 and stage 2, in parallel (2 threads each), then their measurements.
# - control_jit_s0: control setting + perturbed questions (jitter_max 0.5), λ = 1, from scratch.
# - text_s0: answers written as text (train_text.py), control setting, λ = 1, from scratch.
set -u
cd "$(dirname "$0")"
[ -f results/control_jit_s0.json ] || .venv/bin/python train.py control_jit_s0 1.0 0 15000 detach 0.5 >> logs/control_jit_s0.log 2>&1 || echo "FAILED control_jit_s0" &
[ -f results/text_s0.json ] || .venv/bin/python train_text.py text_s0 1.0 0 >> logs/text_s0.log 2>&1 || echo "FAILED text_s0" &
wait
THREADS=2 .venv/bin/python measure.py control_jit_s0 > logs/measure_control_jit.log 2>&1 || echo "FAILED measure control_jit" &
THREADS=2 .venv/bin/python measure_text.py text_s0 joint_detached_s0 > logs/measure_text.log 2>&1 || echo "FAILED measure text" &
wait
.venv/bin/python analyze_review.py control_jit_s0 lmonly_s0 > logs/review_checks_control_jit.log 2>&1 || echo "FAILED checks control_jit"
echo "phase 2 done"
