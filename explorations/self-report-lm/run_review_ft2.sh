#!/usr/bin/env bash
# After ft_slope and text_jit finish: review checks (follow by frequency, gains along u, ...) on ft2_lam4_jit.
set -u
cd "$(dirname "$0")"
until grep -q "slope done" logs_slope.txt 2>/dev/null && grep -q "text_jit done" logs_text_jit.txt 2>/dev/null; do sleep 30; done
[ -f results/review_checks_ft2_lam4_jit.json ] || THREADS=4 .venv/bin/python analyze_review.py ft2_lam4_jit lmonly_s0 >> logs/review_ft2_lam4_jit.log 2>&1 || echo "FAILED review ft2"
echo "review ft2 done"
