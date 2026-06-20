#!/bin/bash
# run_convergence.sh — Long convergence runs to measure time-to-low-perplexity
#
# BS=8 and BS=16 head-to-head, 2000 steps each.
# dim=1024, layers=6, seq_len=128, base LR=3e-4
#
# Expected runtime: ~8 hours total (sequential)

set -e

DIM=1024
N_LAYERS=6
N_HEADS=16
HIDDEN_DIM=4096
SEQ_LEN=128
MAX_SEQ_LEN=256
N_STEPS=2000
EVAL_EVERY=50
LR="0.000300"

COMMON="-DDIM=$DIM -DN_LAYERS=$N_LAYERS -DN_HEADS=$N_HEADS -DHIDDEN_DIM=$HIDDEN_DIM \
        -DSEQ_LEN=$SEQ_LEN -DMAX_SEQ_LEN=$MAX_SEQ_LEN -DN_STEPS=$N_STEPS \
        -DEVAL_EVERY=$EVAL_EVERY -DGEN_EVERY=999999 -DTRAIN_MODE=2 -DLR=${LR}f"

echo "============================================"
echo "Convergence Experiment"
echo "dim=$DIM, layers=$N_LAYERS, seq=$SEQ_LEN"
echo "Steps: $N_STEPS, Eval every: $EVAL_EVERY, LR: $LR"
echo "Started: $(date)"
echo "============================================"
echo ""

# --- BS=8 ---
echo "=== BS=8 ==="
echo "Start: $(date)"
rm -f train.o
make train_qat -s TRAIN_CFLAGS="$COMMON -DBATCH_SIZE=8 -DCSV_PREFIX=converge_bs8"
./train_qat 2>&1 | tee converge_bs8.log
echo "End: $(date)"
echo ""

# --- BS=16 ---
echo "=== BS=16 ==="
echo "Start: $(date)"
rm -f train.o
make train_qat -s TRAIN_CFLAGS="$COMMON -DBATCH_SIZE=16 -DCSV_PREFIX=converge_bs16"
./train_qat 2>&1 | tee converge_bs16.log
echo "End: $(date)"
echo ""

echo "============================================"
echo "Done: $(date)"
echo "============================================"

# Quick comparison
python3 -c "
import os
os.chdir(os.path.dirname(os.path.abspath('$0')) or '.')

def parse(f):
    rows = []
    with open(f) as fh:
        for line in fh.readlines()[1:]:
            p = line.strip().split(',')
            rows.append({'step': int(p[-9]), 'ppl': float(p[-5]), 'bpb': float(p[-4]),
                         'tps': float(p[-2]), 'elapsed': float(p[-1]), 'tokens': int(float(p[-8]))})
    return rows

thresholds = [80, 40, 20, 15, 10, 8, 7]
print()
print('=== TIME-TO-PERPLEXITY (seconds) ===')
print(f'{\"Config\":<12}', end='')
for t in thresholds:
    print(f'  ppl<{t:>2}', end='')
print(f'  {\"final_ppl\":>10}  {\"final_bpb\":>10}')
print('-' * 100)

for bs, f in [(8, 'converge_bs8.csv'), (16, 'converge_bs16.csv')]:
    if not os.path.exists(f):
        continue
    rows = parse(f)
    print(f'BS={bs:<9}', end='')
    for t in thresholds:
        hit = next((r['elapsed'] for r in rows if r['ppl'] < t), None)
        print(f'  {hit:>5.0f}s' if hit else '    ---', end='')
    print(f'  {rows[-1][\"ppl\"]:>10.2f}  {rows[-1][\"bpb\"]:>10.3f}')
"
