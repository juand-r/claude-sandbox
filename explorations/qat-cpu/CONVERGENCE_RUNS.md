# Convergence Experiment Runs

## Goal

Compare QAT vs FP32 training convergence at batch sizes 8 and 16, dim=1024.
We want to see if QAT reaches the same perplexity as FP32 (and how fast).

## 4 Runs (2x2 grid)

| Run | Batch Size | Mode | TRAIN_MODE | CSV file | Status |
|-----|-----------|------|------------|----------|--------|
| BS=8 QAT | 8 | QAT (INT8 fwd, FP32 bwd) | 2 | `converge_bs8_qat.csv` | DONE (300 steps, PPL=12.39) |
| BS=8 FP32 | 8 | FP32 only | 1 | `converge_bs8_fp32.csv` | PARTIAL (step 50, PPL=26.76, process died) |
| BS=16 QAT | 16 | QAT | 2 | `converge_bs16_qat.csv` | NOT STARTED |
| BS=16 FP32 | 16 | FP32 only | 1 | `converge_bs16_fp32.csv` | NOT STARTED |

## How to run

All runs use the same model config. The only variables are batch size and TRAIN_MODE.

### Shared config (compile-time flags)

```
DIM=1024  N_LAYERS=6  N_HEADS=16  HIDDEN_DIM=4096
SEQ_LEN=128  MAX_SEQ_LEN=256
N_STEPS=300  EVAL_EVERY=50  GEN_EVERY=999999
LR=0.000300  EARLY_STOP_PPL=10.0
```

### TRAIN_MODE values

- `1` = FP32 only
- `2` = QAT only (INT8 forward, FP32 backward)
- `3` = QAT with INT8 backward (not used here)

### Running a single experiment

From `explorations/qat-cpu/`:

```bash
rm -f train.o
make train_qat -s TRAIN_CFLAGS="-DDIM=1024 -DN_LAYERS=6 -DN_HEADS=16 \
    -DHIDDEN_DIM=4096 -DSEQ_LEN=128 -DMAX_SEQ_LEN=256 -DN_STEPS=300 \
    -DEVAL_EVERY=50 -DGEN_EVERY=999999 -DLR=0.000300f \
    -DEARLY_STOP_PPL=10.0f -DBATCH_SIZE=8 -DTRAIN_MODE=1 \
    -DCSV_PREFIX=converge_bs8_fp32"
./train_qat
```

The `rm -f train.o` is essential — `train.c` must be recompiled because the
config is baked in via `-D` defines. The other `.o` files don't change.

Output goes to `<CSV_PREFIX>.csv` in the current directory.

### Running all remaining experiments

`run_remaining.sh` runs the 3 incomplete experiments sequentially:

```bash
cd explorations/qat-cpu
nohup bash run_remaining.sh > run_remaining.log 2>&1 &
```

It runs BS=8 FP32, BS=16 QAT, BS=16 FP32 in order. Each takes ~20-25 min
(300 steps at ~4-5 sec/step). Total ~60-75 min.

**Warning**: The BS=8 FP32 CSV already has 2 rows (steps 0 and 50). Running
`run_remaining.sh` will overwrite the CSV because train.c opens it with `"w"`.
This is fine — it will regenerate from step 0. If you want to avoid rerunning
the QAT experiment that's already done, edit the script to remove that line.

### Known issue: process getting killed

The BS=8 QAT run died at step 200 on a prior attempt (then succeeded on a
later attempt with 300 steps). The BS=8 FP32 run died at step 50. Likely OOM
or timeout. The model at dim=1024 uses significant memory. Monitor with:

```bash
tail -f run_remaining.log
# or check if it's still alive:
ps aux | grep train_qat
```

### What "done" looks like

Each CSV should have rows at steps 0, 50, 100, 150, 200, 250, 300 (7 rows
plus header), unless early stopping triggers (PPL < 10.0), which would end
the run early.

## Existing results

### BS=8 QAT (converge_bs8_qat.csv) — COMPLETE

```
Step   0: PPL=93.27, 5650 ms/step
Step  50: PPL=26.76, 5341 ms/step
Step 100: PPL=17.79, 5055 ms/step
Step 150: PPL=13.78, 4911 ms/step
Step 200: PPL=12.96, 5076 ms/step
Step 250: PPL=12.92, 3849 ms/step
Step 300: PPL=12.39, 3761 ms/step
```

### BS=8 QAT (converge_bs8.csv) — longer run, also complete

Same config but from `run_convergence.sh` (same 300 steps, slightly different
timings due to different run). Final PPL=12.39.

### BS=8 FP32 (converge_bs8_fp32.csv) — INCOMPLETE

```
Step   0: PPL=93.08, 6340 ms/step
Step  50: PPL=26.76, 4990 ms/step
```
Process died after step 50.
