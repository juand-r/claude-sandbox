#!/usr/bin/env bash
# Stage 1, phase 1: continue the control model (joint_detached_s0) for 3,000 steps under four
# variants, two at a time (2 threads each). See PLAN.md.
set -u
cd "$(dirname "$0")"
run() { [ -f results/$1.json ] || .venv/bin/python finetune.py joint_detached_s0 "$@" >> logs/$1.log 2>&1 || echo "FAILED $1"; }
run ft_more 3000 1 0 &
run ft_lam4 3000 4 0 &
wait
run ft_jit 3000 1 0.5 &
run ft_lam4_jit 3000 4 0.5 &
wait
echo "phase 1 done"
