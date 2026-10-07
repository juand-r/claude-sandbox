#!/usr/bin/env bash
# After the full measurement of ft2_lam4_jit: continue the text-answer run with perturbed questions.
set -u
cd "$(dirname "$0")"
until [ -f results/measure_ft2_lam4_jit.json ] || grep -q "Traceback" logs/measure_ft2_lam4_jit.log 2>/dev/null; do sleep 30; done
[ -f results/text_jit.json ] || .venv/bin/python finetune_text.py text_s0 text_jit 3000 1 0.5 >> logs/text_jit.log 2>&1 || echo "FAILED text_jit"
echo "text_jit done"
