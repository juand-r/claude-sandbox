#!/usr/bin/env bash
# After the review checks on ft2_lam4_jit: full measurement and review checks on ft_slope.
set -u
cd "$(dirname "$0")"
until grep -q "review ft2 done" logs_review_ft2.txt 2>/dev/null; do sleep 30; done
[ -f results/measure_ft_slope.json ] || THREADS=2 .venv/bin/python measure.py ft_slope >> logs/measure_ft_slope.log 2>&1 || echo "FAILED measure ft_slope"
[ -f results/review_checks_ft_slope.json ] || .venv/bin/python analyze_review.py ft_slope lmonly_s0 >> logs/review_ft_slope.log 2>&1 || echo "FAILED review ft_slope"
echo "slope measurements done"
