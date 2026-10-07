#!/usr/bin/env bash
# After the measurement of text_jit_lam4_long: 6,000 more steps of the same training, then its measurement.
set -u
cd "$(dirname "$0")"
until grep -q "text final done" logs_text_final.txt 2>/dev/null; do sleep 30; done
n=text_jit_lam4_long2
[ -f results/$n.json ] || .venv/bin/python finetune_text.py text_jit_lam4_long $n 6000 4 0.5 >> logs/$n.log 2>&1 || { echo "FAILED $n"; exit 1; }
[ -f results/measure_$n.json ] || THREADS=2 .venv/bin/python measure_text.py $n joint_detached_s0 ft_slope >> logs/measure_$n.log 2>&1 || echo "FAILED measure $n"
echo "text long2 done"
