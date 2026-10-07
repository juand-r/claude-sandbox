#!/usr/bin/env bash
# After run_after_phase2.sh: continue the best phase-1 model with the slope loss added.
set -u
cd "$(dirname "$0")"
until grep -q "after phase 2 done" logs_after_phase2.txt 2>/dev/null; do sleep 30; done
[ -f results/ft_slope.json ] || .venv/bin/python finetune.py ft_lam4_jit ft_slope 3000 4 0.5 0.0002 1.0 >> logs/ft_slope.log 2>&1 || echo "FAILED ft_slope"
echo "slope done"
