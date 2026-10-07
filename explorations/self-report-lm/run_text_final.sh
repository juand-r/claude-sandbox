#!/usr/bin/env bash
# After text_jit_lam4_long: full text measurement, compared with the number-head control and ft_slope.
set -u
cd "$(dirname "$0")"
until grep -q "text next done" logs_text_next.txt 2>/dev/null; do sleep 30; done
[ -f results/measure_text_jit_lam4_long.json ] || THREADS=2 .venv/bin/python measure_text.py text_jit_lam4_long joint_detached_s0 ft_slope >> logs/measure_text_jit_lam4_long.log 2>&1 || echo "FAILED measure text_jit_lam4_long"
echo "text final done"
