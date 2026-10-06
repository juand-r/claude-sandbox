#!/usr/bin/env bash
# Replication: joint run with seed 1 (different initialization and held-out tokens), started
# when the language-model-only run frees its cores; then its measurements.
set -u
cd "$(dirname "$0")"
until grep -q "wrote results" logs/lmonly_s0.log; do sleep 20; done
[ -f results/joint_s1.json ] || .venv/bin/python train.py joint_s1 1.0 1 >> logs/joint_s1.log 2>&1 || echo "FAILED joint_s1"
THREADS=2 .venv/bin/python measure.py joint_s1 > logs/measure_s1.log 2>&1 || echo "FAILED measure s1"
echo "seed1 done"
