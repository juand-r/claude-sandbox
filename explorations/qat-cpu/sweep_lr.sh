#!/bin/bash
# sweep_lr.sh — Test different LR strategies at BS=32 and BS=64
# Compare: base LR (3e-4), sqrt scaling, linear scaling
#
# Usage: ./sweep_lr.sh [n_steps] [eval_every]

set -e

N_STEPS=${1:-20}
EVAL_EVERY=${2:-5}

DIM=1024
N_LAYERS=6
N_HEADS=16
HIDDEN_DIM=4096
SEQ_LEN=128
MAX_SEQ_LEN=256

echo "============================================"
echo "LR Scaling Sweep"
echo "Steps: $N_STEPS, Eval every: $EVAL_EVERY"
echo "============================================"
echo ""

rm -f sweep_lr_*.csv sweep_lr_*.log

# Test configs: (batch_size, lr, label)
CONFIGS=(
    "8,0.000300,bs8_base"
    "16,0.000300,bs16_base"
    "16,0.000424,bs16_sqrt"
    "32,0.000300,bs32_base"
    "32,0.000600,bs32_sqrt"
    "32,0.001200,bs32_linear"
    "64,0.000300,bs64_base"
    "64,0.000849,bs64_sqrt"
    "64,0.002400,bs64_linear"
)

for CFG in "${CONFIGS[@]}"; do
    IFS=',' read -r BS LR LABEL <<< "$CFG"
    PREFIX="sweep_lr_${LABEL}"
    echo "--- $LABEL: BS=$BS, LR=$LR ---"

    rm -f train.o
    make train_qat -s TRAIN_CFLAGS="\
        -DDIM=$DIM \
        -DN_LAYERS=$N_LAYERS \
        -DN_HEADS=$N_HEADS \
        -DHIDDEN_DIM=$HIDDEN_DIM \
        -DSEQ_LEN=$SEQ_LEN \
        -DMAX_SEQ_LEN=$MAX_SEQ_LEN \
        -DBATCH_SIZE=$BS \
        -DN_STEPS=$N_STEPS \
        -DEVAL_EVERY=$EVAL_EVERY \
        -DGEN_EVERY=999999 \
        -DTRAIN_MODE=2 \
        -DLR=${LR}f \
        -DCSV_PREFIX=$PREFIX"

    echo "  Running..."
    ./train_qat 2>&1 | grep -E "Step|Training complete|Final val|Throughput" || true
    echo ""
done

echo "============================================"
echo "=== Results Summary ==="
echo "============================================"
echo ""
printf "%-15s %6s %8s %8s %8s %8s\n" "Config" "BS" "LR" "BPB" "tok/s" "elapsed"
echo "-----------------------------------------------------------"
for CFG in "${CONFIGS[@]}"; do
    IFS=',' read -r BS LR LABEL <<< "$CFG"
    CSV="sweep_lr_${LABEL}.csv"
    if [ -f "$CSV" ]; then
        LAST=$(tail -1 "$CSV")
        BPB=$(echo "$LAST" | cut -d, -f7)
        TOKS=$(echo "$LAST" | cut -d, -f9)
        ELAPSED=$(echo "$LAST" | cut -d, -f10)
        printf "%-15s %6s %8s %8s %8s %8s\n" "$LABEL" "$BS" "$LR" "$BPB" "$TOKS" "$ELAPSED"
    fi
done
