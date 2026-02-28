#!/bin/bash
# run_converge_all.sh — Run convergence experiments for all BS/mode combos
#
# dim=1024, 6 layers, seq=128, 600 steps max, early stop at PPL<10
# Sequential execution (one at a time for accurate measurement)

set -e
cd "$(dirname "$0")"

DIM=1024
N_LAYERS=6
N_HEADS=16
HIDDEN_DIM=4096
SEQ_LEN=128
MAX_SEQ_LEN=256
N_STEPS=600
EVAL_EVERY=50
LR="0.000300"
EARLY_STOP_PPL="10.0"

COMMON="-DDIM=$DIM -DN_LAYERS=$N_LAYERS -DN_HEADS=$N_HEADS -DHIDDEN_DIM=$HIDDEN_DIM \
        -DSEQ_LEN=$SEQ_LEN -DMAX_SEQ_LEN=$MAX_SEQ_LEN -DN_STEPS=$N_STEPS \
        -DEVAL_EVERY=$EVAL_EVERY -DGEN_EVERY=999999 -DLR=${LR}f \
        -DEARLY_STOP_PPL=${EARLY_STOP_PPL}f"

echo "============================================"
echo "Convergence Experiment (all combos)"
echo "dim=$DIM, layers=$N_LAYERS, seq=$SEQ_LEN"
echo "Steps: $N_STEPS max, Early stop: PPL<$EARLY_STOP_PPL"
echo "Started: $(date)"
echo "============================================"
echo ""

run_one() {
    local label=$1
    local bs=$2
    local mode=$3
    local csv_prefix=$4

    echo "=== $label (BS=$bs, mode=$mode) ==="
    echo "Start: $(date)"
    rm -f train.o
    make train_qat -s TRAIN_CFLAGS="$COMMON -DBATCH_SIZE=$bs -DTRAIN_MODE=$mode -DCSV_PREFIX=$csv_prefix"
    ./train_qat 2>&1 | tail -30
    echo "End: $(date)"
    echo ""
}

# BS=8 QAT (mode=2)
run_one "BS=8 QAT" 8 2 "converge_bs8_qat"

# BS=8 FP32 (mode=1)
run_one "BS=8 FP32" 8 1 "converge_bs8_fp32"

# BS=16 QAT (mode=2)
run_one "BS=16 QAT" 16 2 "converge_bs16_qat"

# BS=16 FP32 (mode=1)
run_one "BS=16 FP32" 16 1 "converge_bs16_fp32"

echo "============================================"
echo "All runs complete: $(date)"
echo "============================================"

# Summary
python3 -c "
import os
os.chdir(os.path.dirname(os.path.abspath('$0')) or '.')

def parse(f):
    rows = []
    if not os.path.exists(f):
        return rows
    with open(f) as fh:
        for line in fh.readlines()[1:]:
            p = line.strip().split(',')
            if len(p) < 10: continue
            rows.append({'step': int(p[1]), 'ppl': float(p[5]), 'bpb': float(p[6]),
                         'tps': float(p[8]), 'elapsed': float(p[9]), 'tokens': int(p[2])})
    return rows

thresholds = [80, 40, 20, 15, 12, 10]
configs = [
    ('BS=8 QAT',   'converge_bs8_qat.csv'),
    ('BS=8 FP32',  'converge_bs8_fp32.csv'),
    ('BS=16 QAT',  'converge_bs16_qat.csv'),
    ('BS=16 FP32', 'converge_bs16_fp32.csv'),
]

print()
print('=== TIME-TO-PERPLEXITY (seconds) ===')
print(f'{\"Config\":<14}', end='')
for t in thresholds:
    print(f'  ppl<{t:>2}', end='')
print(f'  {\"final_ppl\":>10}  {\"final_bpb\":>10}  {\"tok/s\":>6}  {\"steps\":>5}')
print('-' * 110)

for label, f in configs:
    rows = parse(f)
    if not rows:
        continue
    print(f'{label:<14}', end='')
    for t in thresholds:
        hit = next((r['elapsed'] for r in rows if r['ppl'] < t), None)
        print(f'  {hit:>5.0f}s' if hit else '    ---', end='')
    avg_tps = sum(r['tps'] for r in rows[1:]) / max(len(rows)-1, 1)
    print(f'  {rows[-1][\"ppl\"]:>10.2f}  {rows[-1][\"bpb\"]:>10.3f}  {avg_tps:>6.0f}  {rows[-1][\"step\"]:>5}')
"
