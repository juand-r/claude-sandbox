#!/usr/bin/env bash
# Runs with fresh data seeds (finetune.data_offset), after the review found that chained continuations replayed
# their parent's data:
# 1. text_jit_lam4_long2: 6,000 more text steps from text_jit_lam4_long, then its measurement;
# 2. then a clean comparison of the slope loss: from ft_lam4_jit, 3,000 steps, λ = 4, perturbed questions,
#    without (fresh_noslope) and with (fresh_slope) the slope loss; both with new data. Then full measurements.
set -u
cd "$(dirname "$0")"
n=text_jit_lam4_long2
[ -f results/$n.json ] || .venv/bin/python finetune_text.py text_jit_lam4_long $n 6000 4 0.5 >> logs/$n.log 2>&1 || echo "FAILED $n"
( [ -f results/measure_$n.json ] || THREADS=2 .venv/bin/python measure_text.py $n joint_detached_s0 ft_slope >> logs/measure_$n.log 2>&1 || echo "FAILED measure $n" ) &
( [ -f results/fresh_noslope.json ] || .venv/bin/python finetune.py ft_lam4_jit fresh_noslope 3000 4 0.5 0.0002 0 >> logs/fresh_noslope.log 2>&1 || echo "FAILED fresh_noslope" ) &
wait
( [ -f results/fresh_slope.json ] || .venv/bin/python finetune.py ft_lam4_jit fresh_slope 3000 4 0.5 0.0002 1.0 >> logs/fresh_slope.log 2>&1 || echo "FAILED fresh_slope" ) &
( [ -f results/measure_fresh_noslope.json ] || THREADS=2 .venv/bin/python measure.py fresh_noslope >> logs/measure_fresh_noslope.log 2>&1 || echo "FAILED measure fresh_noslope" ) &
wait
[ -f results/measure_fresh_slope.json ] || THREADS=4 .venv/bin/python measure.py fresh_slope >> logs/measure_fresh_slope.log 2>&1 || echo "FAILED measure fresh_slope"
echo "fresh done"
