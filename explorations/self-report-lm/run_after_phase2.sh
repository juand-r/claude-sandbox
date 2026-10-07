#!/usr/bin/env bash
# After phase 2 finishes: continue the from-scratch perturbed-question model for 3,000 steps with
# perturbed questions (λ = 1), to compare with ft_jit (the same continuation from the control).
set -u
cd "$(dirname "$0")"
until grep -q "phase 2 done" logs_phase2.txt; do sleep 30; done
[ -f results/ft_jit_from_jit.json ] || .venv/bin/python finetune.py control_jit_s0 ft_jit_from_jit 3000 1 0.5 >> logs/ft_jit_from_jit.log 2>&1 || echo "FAILED ft_jit_from_jit"
echo "after phase 2 done"
