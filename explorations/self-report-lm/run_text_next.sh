#!/usr/bin/env bash
# After text_jit_lam4: full text measurement of it (paired with the number-head control),
# and in parallel 6,000 more steps of the same training (text_jit_lam4_long).
set -u
cd "$(dirname "$0")"
until grep -q "text_jit_lam4 done" logs_text_jit_lam4.txt 2>/dev/null; do sleep 30; done
( [ -f results/measure_text_jit_lam4.json ] || THREADS=2 .venv/bin/python measure_text.py text_jit_lam4 joint_detached_s0 >> logs/measure_text_jit_lam4.log 2>&1 || echo "FAILED measure text_jit_lam4" ) &
( [ -f results/text_jit_lam4_long.json ] || .venv/bin/python finetune_text.py text_jit_lam4 text_jit_lam4_long 6000 4 0.5 >> logs/text_jit_lam4_long.log 2>&1 || echo "FAILED text_jit_lam4_long" ) &
wait
echo "text next done"
