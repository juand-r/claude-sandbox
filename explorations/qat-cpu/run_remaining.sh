#!/bin/bash
# Run remaining convergence combos: BS=8 FP32, BS=16 QAT, BS=16 FP32
# BS=8 QAT already done.

set -e
cd "$(dirname "$0")"

DIM=1024
N_LAYERS=6
N_HEADS=16
HIDDEN_DIM=4096
SEQ_LEN=128
MAX_SEQ_LEN=256
N_STEPS=300
EVAL_EVERY=50
LR="0.000300"
EARLY_STOP_PPL="10.0"

COMMON="-DDIM=$DIM -DN_LAYERS=$N_LAYERS -DN_HEADS=$N_HEADS -DHIDDEN_DIM=$HIDDEN_DIM \
        -DSEQ_LEN=$SEQ_LEN -DMAX_SEQ_LEN=$MAX_SEQ_LEN -DN_STEPS=$N_STEPS \
        -DEVAL_EVERY=$EVAL_EVERY -DGEN_EVERY=999999 -DLR=${LR}f \
        -DEARLY_STOP_PPL=${EARLY_STOP_PPL}f"

run_one() {
    local label=$1
    local bs=$2
    local mode=$3
    local csv_prefix=$4

    echo ""
    echo "=== $label (BS=$bs, mode=$mode) ==="
    echo "Start: $(date)"
    rm -f train.o
    make train_qat -s TRAIN_CFLAGS="$COMMON -DBATCH_SIZE=$bs -DTRAIN_MODE=$mode -DCSV_PREFIX=$csv_prefix"
    ./train_qat 2>&1 | tail -30
    echo "End: $(date)"
    echo ""
}

echo "Started: $(date)"

run_one "BS=8 FP32"  8  1 "converge_bs8_fp32"
run_one "BS=16 QAT"  16 2 "converge_bs16_qat"
run_one "BS=16 FP32" 16 1 "converge_bs16_fp32"

echo "All done: $(date)"
