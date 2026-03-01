#!/bin/bash
# sweep_batch.sh — Batch size sweep for dim=1024, layers=6, seq_len=128
#
# Measures throughput and convergence for QAT mode at batch sizes 8, 16, 32, 64.
# Produces CSV files: sweep_qat_bs{N}.csv
#
# Usage: ./sweep_batch.sh [n_steps] [eval_every]
#   Defaults: n_steps=200, eval_every=20

set -e

N_STEPS=${1:-200}
EVAL_EVERY=${2:-20}

# Fixed model config
DIM=1024
N_LAYERS=6
N_HEADS=16
HIDDEN_DIM=4096
SEQ_LEN=128
MAX_SEQ_LEN=256

# LR scaling: base LR=3e-4 at batch_size=8, linear scaling
BASE_LR="3e-4"
BASE_BS=8

echo "============================================"
echo "Batch Size Sweep: dim=$DIM, layers=$N_LAYERS, seq=$SEQ_LEN"
echo "Steps: $N_STEPS, Eval every: $EVAL_EVERY"
echo "============================================"
echo ""

# Clean up old CSV files
rm -f sweep_qat_bs*.csv sweep_qat_bs*.log

for BS in 8 16 32 64; do
    # Linear LR scaling: lr = base_lr * (bs / base_bs)
    LR=$(python3 -c "print(f'{$BASE_LR * $BS / $BASE_BS:.6f}')")

    PREFIX="sweep_qat_bs${BS}"
    echo "--- Batch size $BS (LR=$LR) ---"

    # Only recompile train.o (other objects unchanged)
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

    echo "  Running $N_STEPS steps..."
    START=$(date +%s)
    ./train_qat 2>&1 | tee "${PREFIX}.log"
    END=$(date +%s)
    echo "  Done in $((END - START)) seconds"
    echo ""
done

echo "============================================"
echo "Sweep complete. CSV files:"
ls -la sweep_qat_bs*.csv 2>/dev/null
echo ""

# Quick summary
echo "=== Throughput Summary ==="
for BS in 8 16 32 64; do
    LOG="sweep_qat_bs${BS}.log"
    if [ -f "$LOG" ]; then
        TOKPS=$(grep "Throughput:" "$LOG" | tail -1 | awk '{print $2}')
        BPB=$(grep "Final val BPB:" "$LOG" | tail -1 | awk '{print $4}')
        echo "  BS=$BS: $TOKPS tok/s, final BPB=$BPB"
    fi
done
