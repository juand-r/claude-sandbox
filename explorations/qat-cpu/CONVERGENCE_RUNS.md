# Convergence Experiment Runs

## Goal

Compare QAT vs FP32 training convergence at batch sizes 8 and 16, dim=1024.
We want to see if QAT reaches the same perplexity as FP32 (and how fast).

## Status of all 4 runs

| Run | Batch Size | Mode | TRAIN_MODE | CSV file | Status |
|-----|-----------|------|------------|----------|--------|
| BS=8 QAT | 8 | QAT (INT8 fwd, FP32 bwd) | 2 | `converge_bs8.csv` | DONE (300 steps, final PPL=12.39) |
| BS=8 FP32 | 8 | FP32 only | 1 | `converge_bs8_fp32.csv` | DONE (300 steps, final PPL=12.52) |
| BS=16 QAT | 16 | QAT | 2 | `converge_bs16_qat.csv` | DONE (300 steps, final PPL=12.16) |
| BS=16 FP32 | 16 | FP32 only | 1 | `converge_bs16_fp32.csv` | DONE (300 steps, final PPL=12.13) |
| BS=8 INT8bwd | 8 | QAT+INT8 backward | 3 | `converge_bs8_int8bwd.csv` | DONE (300 steps, final PPL=12.70) |
| BS=8 BF16bwd | 8 | QAT+BF16 backward | 2 | `converge_bs8_bf16bwd.csv` | DONE (300 steps, final PPL=12.57) |

## Results

### Model config (all runs)

```
DIM=1024  N_LAYERS=6  N_HEADS=16  HIDDEN_DIM=4096
SEQ_LEN=128  MAX_SEQ_LEN=256  LR=0.000300
N_STEPS=300  EVAL_EVERY=50  76M params
```

### BS=8 comparison (QAT vs FP32)

| Step | QAT PPL | FP32 PPL | QAT BPB | FP32 BPB | QAT ms/step | FP32 ms/step | QAT tok/s | FP32 tok/s | QAT elapsed | FP32 elapsed |
|------|---------|----------|---------|----------|-------------|-------------|-----------|------------|-------------|--------------|
| 0    | 93.27   | 93.08    | 6.543   | 6.540    | 4591        | 6710        | 223       | 153        | 13s         | 16s          |
| 50   | 26.76   | 26.76    | 4.742   | 4.742    | 4261        | 5407        | 240       | 189        | 216s        | 297s         |
| 100  | 17.79   | 18.42    | 4.153   | 4.203    | 4015        | 5384        | 255       | 190        | 423s        | 580s         |
| 150  | 13.78   | 13.77    | 3.785   | 3.784    | 4038        | 5282        | 254       | 194        | 634s        | 864s         |
| 200  | 12.96   | 13.02    | 3.697   | 3.703    | 4057        | 5381        | 252       | 190        | 848s        | 1147s        |
| 250  | 12.92   | 12.94    | 3.692   | 3.694    | 3849        | 5889        | 266       | 174        | 1062s       | 1430s        |
| 300  | 12.39   | 12.52    | 3.631   | 3.647    | 3761        | 5552        | 272       | 184        | 1280s       | 1721s        |

**Final PPL ratio**: 12.39 / 12.52 = 0.990 (QAT is *better*, likely noise)
**Avg speedup** (excluding step 0): 5503 / 4032 = **1.36x** (QAT faster)
**Total time**: QAT 1280 sec vs FP32 1721 sec (7.3 min saved)

### BS=16 comparison (QAT vs FP32)

| Step | QAT PPL | FP32 PPL | QAT BPB | FP32 BPB | QAT ms/step | FP32 ms/step | QAT tok/s | FP32 tok/s | QAT elapsed | FP32 elapsed |
|------|---------|----------|---------|----------|-------------|-------------|-----------|------------|-------------|--------------|
| 0    | 88.62   | 88.52    | 6.469   | 6.468    | 11870       | 19666       | 173       | 104        | 24s         | 39s          |
| 50   | 26.59   | 26.59    | 4.733   | 4.733    | 10304       | 10438       | 199       | 196        | 541s        | 605s         |
| 100  | 17.08   | 16.54    | 4.094   | 4.048    | 9441        | 10958       | 217       | 187        | 1066s       | 1141s        |
| 150  | 13.09   | 13.09    | 3.710   | 3.710    | 9217        | 10054       | 222       | 204        | 1572s       | 1683s        |
| 200  | 12.68   | 12.55    | 3.664   | 3.650    | 10029       | 10957       | 204       | 187        | 2081s       | 2250s        |
| 250  | 12.35   | 12.28    | 3.626   | 3.619    | 9811        | 10614       | 209       | 193        | 2581s       | 2809s        |
| 300  | 12.16   | 12.13    | 3.604   | 3.601    | 9289        | 10932       | 220       | 187        | 3072s       | 3353s        |

**Final PPL ratio**: 12.16 / 12.13 = 1.002 (essentially identical)
**Avg speedup** (excluding step 0): 10667 / 9832 = **1.08x** (QAT slightly faster)
**Total time**: QAT 3072 sec vs FP32 3353 sec (4.7 min saved)

### BS=8 INT8 backward (QAT+INT8bwd vs QAT vs FP32)

| Step | INT8bwd PPL | QAT PPL | FP32 PPL | INT8bwd BPB | QAT BPB | FP32 BPB | INT8bwd ms/step | QAT ms/step | FP32 ms/step |
|------|-------------|---------|----------|-------------|---------|----------|-----------------|-------------|-------------|
| 0    | 89.87       | 93.27   | 93.08    | 6.490       | 6.543   | 6.540    | 5198            | 4591        | 6710        |
| 50   | 26.91       | 26.76   | 26.76    | 4.750       | 4.742   | 4.742    | 4126            | 4261        | 5407        |
| 100  | 20.51       | 17.79   | 18.42    | 4.359       | 4.153   | 4.203    | 4206            | 4015        | 5384        |
| 150  | 14.53       | 13.78   | 13.77    | 3.861       | 3.785   | 3.784    | 4135            | 4038        | 5282        |
| 200  | 13.52       | 12.96   | 13.02    | 3.757       | 3.697   | 3.703    | 3982            | 4057        | 5381        |
| 250  | 13.27       | 12.92   | 12.94    | 3.730       | 3.692   | 3.694    | 4389            | 3849        | 5889        |
| 300  | 12.70       | 12.39   | 12.52    | 3.667       | 3.631   | 3.647    | 4102            | 3761        | 5552        |

**INT8bwd vs FP32**: ppl 12.70 vs 12.52 (ratio 1.014), 1305s vs 1721s = **1.32x faster**
**INT8bwd vs QAT**: ppl 12.70 vs 12.39 (ratio 1.025), 1305s vs 1280s = **0.98x** (2% slower)
**Quality**: INT8bwd tracks convergence but finishes ~0.3 ppl points behind QAT.
Gradient quantization noise has a small but real quality cost at 300 steps.

### BS=8 BF16 backward (QAT+BF16bwd vs QAT vs FP32)

| Step | BF16bwd PPL | QAT PPL | FP32 PPL | BF16bwd BPB | QAT BPB | FP32 BPB | BF16bwd ms/step | QAT ms/step | FP32 ms/step |
|------|-------------|---------|----------|-------------|---------|----------|-----------------|-------------|-------------|
| 0    | 93.78       | 93.27   | 93.08    | 6.551       | 6.543   | 6.540    | 4664            | 4591        | 6710        |
| 50   | 26.75       | 26.76   | 26.76    | 4.741       | 4.742   | 4.742    | 4392            | 4261        | 5407        |
| 100  | 20.69       | 17.79   | 18.42    | 4.371       | 4.153   | 4.203    | 4142            | 4015        | 5384        |
| 150  | 14.41       | 13.78   | 13.77    | 3.849       | 3.785   | 3.784    | 4110            | 4038        | 5282        |
| 200  | 13.28       | 12.96   | 13.02    | 3.732       | 3.697   | 3.703    | 4058            | 4057        | 5381        |
| 250  | 13.06       | 12.92   | 12.94    | 3.707       | 3.692   | 3.694    | 4008            | 3849        | 5889        |
| 299  | 12.57       | 12.39   | 12.52    | 3.652       | 3.631   | 3.647    | 4239            | 3761        | 5552        |

**BF16bwd vs QAT**: ppl 12.57 vs 12.39 (ratio 1.015), 1301s vs 1280s = **0.98x** (2% slower)
**BF16bwd vs FP32**: ppl 12.57 vs 12.52 (ratio 1.004), 1301s vs 1721s = **1.32x faster**
**Verdict**: BF16 backward is slower than FP32 backward and slightly degrades quality.
The on-the-fly FP32→BF16 conversion overhead negates the VDPBF16PS compute advantage
at these matrix sizes. The 8-bit mantissa also adds gradient noise (0.18 ppl vs QAT).
**Recommendation**: Revert to FP32 backward (the original QAT mode).

### Cross-batch comparison

| Metric | BS=8 QAT | BS=8 FP32 | BS=16 QAT | BS=16 FP32 |
|--------|----------|-----------|-----------|------------|
| Final PPL | 12.39 | 12.52 | 12.16 | 12.13 |
| Final BPB | 3.631 | 3.647 | 3.604 | 3.601 |
| Avg ms/step | ~4032 | ~5503 | ~9832 | ~10667 |
| Final tok/s | 272 | 184 | 220 | 187 |
| Total time | 1280s (21m) | 1721s (29m) | 3072s (51m) | 3353s (56m) |
| Total tokens | 308K | 307K | 614K | 614K |
| QAT speedup | 1.36x | -- | 1.08x | -- |
| QAT time saved | 7.3 min | -- | 4.7 min | -- |
| QAT PPL ratio | 0.990 | -- | 1.002 | -- |

## Analysis

### Quality: QAT matches FP32

At both batch sizes, QAT converges to essentially the same perplexity as FP32.
The PPL ratios are 0.990 (BS=8) and 1.002 (BS=16) -- within noise. The
convergence curves track each other almost exactly at every checkpoint.

This confirms the finding from the earlier dim=512 experiments: INT8 quantization
noise in the forward pass (with STE for gradients) does not degrade training
quality at dim=1024 either.

### Speed: QAT advantage shrinks with batch size

At BS=8, QAT is 1.36x faster. At BS=16, only 1.08x faster. This matches the
pattern from the dim=512 experiments:

- BS=1 (dim=512): 1.56x speedup
- BS=8 (dim=512, 2L): 0.98x (no advantage)
- BS=8 (dim=512, 4L): 1.18x
- BS=8 (dim=1024, 6L): 1.36x
- BS=16 (dim=1024, 6L): 1.08x

The trend is clear: larger batch sizes shrink QAT's advantage because the
FP32 backward pass (identical in both modes) benefits equally from larger
GEMM sizes and takes a bigger share of total time.

However, at dim=1024 with 6 layers, QAT retains some speed advantage even
at BS=16. This is because the forward pass is a larger fraction of total
compute with more layers (6 layers x 6 projections = 36 QATLinear forward
calls vs the same in backward).

### BS=16 gives slightly better final PPL than BS=8

BS=16 reached PPL 12.13-12.16 vs BS=8's 12.39-12.52, despite seeing 2x as
many tokens (614K vs 308K). More tokens per step helps, though 300 steps is
too few for convergence -- the curves are still dropping.

## How to reproduce

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

The `rm -f train.o` is essential -- `train.c` must be recompiled because the
config is baked in via `-D` defines. The other `.o` files don't change.

### CSV files

- `converge_bs8.csv` -- BS=8 QAT (complete, 7 data rows)
- `converge_bs8_fp32.csv` -- BS=8 FP32 (complete, 7 data rows)
- `converge_bs16_qat.csv` -- BS=16 QAT (complete, 7 data rows)
- `converge_bs16_fp32.csv` -- BS=16 FP32 (complete, 7 data rows)

- `converge_bs8_int8bwd.csv` -- BS=8 QAT+INT8bwd (complete, 7 data rows)
- `converge_bs8_bf16bwd.csv` -- BS=8 QAT+BF16bwd (complete, 7 data rows)

Note: `converge_bs8_qat.csv` is an earlier partial run (died at step 200).
The complete BS=8 QAT data is in `converge_bs8.csv`.
