# PyTorch Tokenization Experiment

PyTorch reimplementation of `train_tok.c` — same architecture, portable (runs on CPU, CUDA, MPS).

## Usage

```bash
# Single run (default: char mode)
python train_tok.py --mode char

# With factored embeddings
python train_tok.py --mode binary --d_in 8 --d_out 128

# Sweep d_in for binary
python sweep.py --phase din --mode binary

# Use GPU
python train_tok.py --mode binary --device cuda
```

## Architecture

Matches the C version exactly:
- Pre-norm transformer (RMSNorm) with GeLU FFN (not SwiGLU)
- Learned absolute positional embeddings (no RoPE)
- No biases anywhere
- ALBERT-style factored embeddings (optional d_in, d_out projections)
- Adam with weight decay, cosine LR with warmup
