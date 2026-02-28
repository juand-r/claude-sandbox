#!/bin/bash
# Sweep batch sizes at dim=1024 to find where INT8 backward breaks even.
# 10 steps per config: enough for stable timing.

set -e

COMMON="-DDIM=1024 -DN_HEADS=16 -DHIDDEN_DIM=4096 -DN_STEPS=10 -DEVAL_EVERY=9 -DGEN_EVERY=9999 -DSEQ_LEN=64"

echo "========================================"
echo "Batch Size Sweep (dim=1024, 10 steps)"
echo "========================================"

for BS in 8 16 32 64; do
    echo ""
    echo "======== BATCH_SIZE=$BS ========"
    rm -f train.o  # force recompile to pick up new -D flags
    make -s train_qat TRAIN_CFLAGS="$COMMON -DBATCH_SIZE=$BS" 2>&1
    ./train_qat 2>&1 | grep -E "^(Batch:|COMPARISON|---|----|  |Val |Total |ms/step|Tokens|Effective|QAT)" || true
    echo ""
done
