# Next Experiment: Binary d_in Sweep (3000 steps)

## What to do

Run the factored embedding d_in sweep for **binary mode only**, at 3000 steps.
This tests whether reducing the input embedding dimension (ALBERT-style factorization)
helps binary tokenization, which was catastrophically bad at d_in=DIM=128 (BPC=4.836).

### Command

```bash
cd /home/user/claude-sandbox/explorations/tokenization
OMP_NUM_THREADS=2 ./sweep_factored.sh din binary
```

This will run 6 experiments sequentially:
- d_in = 4, 8, 16, 32, 64, 128 (with d_out=128 fixed)
- 3000 steps each
- Binary mode only (TOKENIZE_MODE=0, vocab=2, 7 tokens/char, seq_len=896)

Results go to `factored_results/` directory:
- Per-run CSV: `factored_results/binary_din{N}_dout128.csv`
- Per-run log: `factored_results/binary_din{N}_dout128.txt`
- Summary: `factored_results/summary.csv`

### Time estimate

Binary at 3000 steps takes ~20 min per run. 6 runs = ~2 hours total.
Use `OMP_NUM_THREADS=2` to keep memory low on the remote VM.

### Important: bash timeout

The user's local `~/.claude/settings.json` should have:
```json
{
  "env": {
    "BASH_DEFAULT_TIMEOUT_MS": "54400000",
    "BASH_MAX_TIMEOUT_MS": "54400000"
  },
  "permissions": {
    "allow": ["Bash(*)", "Edit(*)", "Write(*)", "Read(*)"]
  }
}
```

If bash timeout is too short, the long-running sweep will be killed.
Alternatively, run in background or use tmux.

---

## Model config for these experiments

All experiments use the **tokenization model** (small model), NOT the QAT model:

```
DIM           = 128
N_LAYERS      = 4
N_HEADS       = 4
HIDDEN_DIM    = 512
BATCH_SIZE    = 4
CHAR_CONTEXT  = 128 chars
SEQ_LEN       = 896 tokens (= 128 chars * 7 tokens/char for binary)
MAX_SEQ_LEN   = 1024
N_STEPS       = 3000
EVAL_EVERY    = 500
LR            = 3e-4 with warmup(20) + cosine decay to 3e-5
WEIGHT_DECAY  = 0.01
FP32 only (no QAT)
```

The **only variable** is D_IN (input embedding dimension):
- Token embeddings: [VOCAB_SIZE=2 x D_IN]
- Position embeddings: [MAX_SEQ_LEN=1024 x D_IN]
- When D_IN != DIM: adds a projection layer [D_IN -> DIM=128]
- D_OUT is fixed at DIM=128 (no output factorization)

Total params ~919K (varies slightly with D_IN, but the embedding is tiny for vocab=2).

---

## Previous results summary

### Tokenization comparison (3000 steps, d_in=d_out=DIM=128)

| Mode    | Vocab  | BPC   | Time (s) | Winner? |
|---------|--------|-------|----------|---------|
| Bigram  | 16384  | 2.771 | 477      | Best BPC |
| Char    | 128    | 2.827 | 153      | Best efficiency |
| Nibble  | 16     | 3.040 | 238      | |
| Base-4  | 4      | 3.707 | 542      | |
| Binary  | 2      | 4.836 | 1177     | Worst (catastrophic) |

### Previous d_in sweep (1000 steps only, incomplete)

From `factored_results_1k/summary.csv` — binary barely moved at 1k steps:

| d_in | BPC (binary) | Converging? |
|------|-------------|-------------|
| 1    | 6.996       | No (random) |
| 2    | 6.997       | No (random) |
| 4    | 6.928       | Barely      |

Binary needs more steps to see any effect. That's why we're running 3000 steps now.

### Best hyperparams from QAT experiments (the "big model")

From `explorations/qat-cpu/CONVERGENCE_RUNS.md`:

```
DIM=1024  N_LAYERS=6  N_HEADS=16  HIDDEN_DIM=4096
SEQ_LEN=128  MAX_SEQ_LEN=256
BATCH_SIZE=8 or 16
LR=3e-4 with warmup(20) + cosine decay to 3e-5
76M params
```

Key findings:
- **QAT matches FP32 quality** (PPL 12.39 vs 12.52 at BS=8, 12.16 vs 12.13 at BS=16)
- **QAT is 1.36x faster** at BS=8, 1.08x at BS=16
- **LR schedule (warmup+cosine) gives 6.7% lower PPL** vs constant LR (11.56 vs 12.39)
- **INT8 backward degrades quality slightly** (12.70 vs 12.39). Not worth it.
- **BF16 backward also not worth it** (12.57 vs 12.39, no speed gain).
- **Best config**: QAT forward + FP32 backward + warmup+cosine LR schedule.

---

## After the sweep

1. Check `factored_results/summary.csv` for the results table
2. Update `RESULTS.md` with findings
3. Commit and push to branch `claude/pull-quantized-cpu-branch-cfgO1`
