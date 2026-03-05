"""
train_tok.py - Tokenization strategy comparison experiment (PyTorch)

Reimplementation of train_tok.c with identical architecture.
Runs on CPU, CUDA, or MPS.

Tokenization modes:
  0: Binary  (vocab=2,     7 tokens/char)
  1: Base-4  (vocab=4,     4 tokens/char)
  2: Nibble  (vocab=16,    2 tokens/char)
  3: Char    (vocab=128,   1 token/char)  [baseline]
  4: Bigram  (vocab=16384, 0.5 tokens/char)
"""

import argparse
import math
import os
import sys
import time
from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F


# ========================================================================
# Tokenization
# ========================================================================

MODE_CONFIG = {
    "binary": {"id": 0, "vocab": 2, "tpc_int": 7, "tpc_f": 7.0},
    "base4":  {"id": 1, "vocab": 4, "tpc_int": 4, "tpc_f": 4.0},
    "nibble": {"id": 2, "vocab": 16, "tpc_int": 2, "tpc_f": 2.0},
    "char":   {"id": 3, "vocab": 128, "tpc_int": 1, "tpc_f": 1.0},
    "bigram": {"id": 4, "vocab": 16384, "tpc_int": None, "tpc_f": 0.5},
}


def encode_text(text_bytes, mode):
    """Encode bytes (7-bit ASCII) into token list."""
    tokens = []
    if mode == "binary":
        for b in text_bytes:
            c = b & 0x7F
            for bit in range(7):
                tokens.append((c >> (6 - bit)) & 1)
    elif mode == "base4":
        for b in text_bytes:
            c = b & 0x7F
            tokens.append((c >> 6) & 3)
            tokens.append((c >> 4) & 3)
            tokens.append((c >> 2) & 3)
            tokens.append(c & 3)
    elif mode == "nibble":
        for b in text_bytes:
            c = b & 0x7F
            tokens.append((c >> 4) & 0xF)
            tokens.append(c & 0xF)
    elif mode == "char":
        for b in text_bytes:
            tokens.append(b & 0x7F)
    elif mode == "bigram":
        n = len(text_bytes) // 2
        for i in range(n):
            c1 = text_bytes[2 * i] & 0x7F
            c2 = text_bytes[2 * i + 1] & 0x7F
            tokens.append(c1 * 128 + c2)
    else:
        raise ValueError(f"Unknown mode: {mode}")
    return tokens


def decode_tokens(tokens, mode):
    """Decode tokens back to string."""
    chars = []
    if mode == "binary":
        for i in range(0, len(tokens) - 6, 7):
            c = 0
            for b in range(7):
                c = (c << 1) | (tokens[i + b] & 1)
            chars.append(chr(c) if 32 <= c < 127 else "?")
    elif mode == "base4":
        for i in range(0, len(tokens) - 3, 4):
            c = ((tokens[i] & 3) << 6) | ((tokens[i+1] & 3) << 4) | \
                ((tokens[i+2] & 3) << 2) | (tokens[i+3] & 3)
            chars.append(chr(c) if 32 <= c < 127 else "?")
    elif mode == "nibble":
        for i in range(0, len(tokens) - 1, 2):
            c = ((tokens[i] & 0xF) << 4) | (tokens[i+1] & 0xF)
            chars.append(chr(c) if 32 <= c < 127 else "?")
    elif mode == "char":
        for t in tokens:
            chars.append(chr(t) if 32 <= t < 127 else "?")
    elif mode == "bigram":
        for t in tokens:
            c1 = t // 128
            c2 = t % 128
            chars.append(chr(c1) if 32 <= c1 < 127 else "?")
            chars.append(chr(c2) if 32 <= c2 < 127 else "?")
    return "".join(chars)


def get_seq_len(mode, char_context):
    """Token sequence length for a given character context window."""
    cfg = MODE_CONFIG[mode]
    if mode == "bigram":
        return char_context // 2
    return char_context * cfg["tpc_int"]


def loss_to_bpc(mean_ce_nats, mode):
    """Convert mean cross-entropy (nats/token) to bits per character."""
    return mean_ce_nats * MODE_CONFIG[mode]["tpc_f"] / math.log(2.0)


def random_baseline_bpc(mode):
    """BPC if predicting uniform over vocab at each position."""
    cfg = MODE_CONFIG[mode]
    return math.log(cfg["vocab"]) * cfg["tpc_f"] / math.log(2.0)


# ========================================================================
# Model
# ========================================================================

class RMSNorm(nn.Module):
    def __init__(self, dim, eps=1e-5):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x):
        rms = torch.sqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return x * self.weight / rms


class Attention(nn.Module):
    def __init__(self, dim, n_heads):
        super().__init__()
        self.dim = dim
        self.n_heads = n_heads
        self.head_dim = dim // n_heads
        assert dim % n_heads == 0

        self.wq = nn.Linear(dim, dim, bias=False)
        self.wk = nn.Linear(dim, dim, bias=False)
        self.wv = nn.Linear(dim, dim, bias=False)
        self.wo = nn.Linear(dim, dim, bias=False)

    def forward(self, x):
        B, T, C = x.shape
        q = self.wq(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        k = self.wk(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)
        v = self.wv(x).view(B, T, self.n_heads, self.head_dim).transpose(1, 2)

        # Scaled dot-product attention with causal mask
        scale = 1.0 / math.sqrt(self.head_dim)
        scores = (q @ k.transpose(-2, -1)) * scale
        causal_mask = torch.triu(
            torch.ones(T, T, device=x.device, dtype=torch.bool), diagonal=1
        )
        scores.masked_fill_(causal_mask, float("-inf"))
        attn = F.softmax(scores, dim=-1)

        out = (attn @ v).transpose(1, 2).contiguous().view(B, T, C)
        return self.wo(out)


class FFN(nn.Module):
    """GeLU feedforward (not SwiGLU), matching the C implementation."""
    def __init__(self, dim, hidden_dim):
        super().__init__()
        self.up = nn.Linear(dim, hidden_dim, bias=False)
        self.down = nn.Linear(hidden_dim, dim, bias=False)

    def forward(self, x):
        return self.down(F.gelu(self.up(x)))


class TransformerBlock(nn.Module):
    def __init__(self, dim, hidden_dim, n_heads):
        super().__init__()
        self.norm1 = RMSNorm(dim)
        self.attn = Attention(dim, n_heads)
        self.norm2 = RMSNorm(dim)
        self.ffn = FFN(dim, hidden_dim)

    def forward(self, x):
        x = x + self.attn(self.norm1(x))
        x = x + self.ffn(self.norm2(x))
        return x


class GPTModel(nn.Module):
    def __init__(self, vocab_size, dim, n_layers, n_heads, hidden_dim,
                 max_seq_len, d_in=None, d_out=None):
        super().__init__()
        self.vocab_size = vocab_size
        self.dim = dim
        self.max_seq_len = max_seq_len
        d_in = d_in or dim
        d_out = d_out or dim
        self.d_in = d_in
        self.d_out = d_out

        # Input embeddings in d_in space
        self.token_emb = nn.Embedding(vocab_size, d_in)
        self.pos_emb = nn.Embedding(max_seq_len, d_in)

        # Factored input projection: d_in -> dim
        self.emb_proj = nn.Linear(d_in, dim, bias=False) if d_in != dim else None

        self.blocks = nn.ModuleList([
            TransformerBlock(dim, hidden_dim, n_heads)
            for _ in range(n_layers)
        ])
        self.final_norm = RMSNorm(dim)

        # Factored output projection: dim -> d_out
        self.head_proj = nn.Linear(dim, d_out, bias=False) if d_out != dim else None

        # Output head: d_out -> vocab
        self.output_head = nn.Linear(d_out, vocab_size, bias=False)

        self._init_weights()

    def _init_weights(self):
        """Match C initialization: uniform [-0.02, 0.02] for embeddings,
        default PyTorch init for linear layers."""
        nn.init.uniform_(self.token_emb.weight, -0.02, 0.02)
        nn.init.uniform_(self.pos_emb.weight, -0.02, 0.02)

    def count_params(self):
        return sum(p.numel() for p in self.parameters())

    def count_embedding_params(self):
        """Embedding + pos_emb + emb_proj (if any)."""
        n = self.token_emb.weight.numel() + self.pos_emb.weight.numel()
        if self.emb_proj is not None:
            n += self.emb_proj.weight.numel()
        return n

    def count_head_params(self):
        """Output head + head_proj (if any)."""
        n = self.output_head.weight.numel()
        if self.head_proj is not None:
            n += self.head_proj.weight.numel()
        return n

    def forward(self, tokens):
        """
        tokens: (B, T) long tensor of token indices
        Returns: (B, T, vocab_size) logits
        """
        B, T = tokens.shape
        assert T <= self.max_seq_len

        pos = torch.arange(T, device=tokens.device)
        x = self.token_emb(tokens) + self.pos_emb(pos)

        if self.emb_proj is not None:
            x = self.emb_proj(x)

        for block in self.blocks:
            x = block(x)

        x = self.final_norm(x)

        if self.head_proj is not None:
            x = self.head_proj(x)

        logits = self.output_head(x)
        return logits


# ========================================================================
# LR Schedule
# ========================================================================

def get_lr(step, total_steps, lr_max, lr_min, warmup_steps):
    if warmup_steps > 0 and step < warmup_steps:
        return lr_max * (step + 1) / warmup_steps
    if total_steps <= warmup_steps:
        return lr_max
    progress = (step - warmup_steps) / (total_steps - warmup_steps)
    progress = min(progress, 1.0)
    return lr_min + 0.5 * (lr_max - lr_min) * (1.0 + math.cos(math.pi * progress))


# ========================================================================
# Training
# ========================================================================

@dataclass
class TrainConfig:
    mode: str = "char"
    dim: int = 128
    n_layers: int = 4
    n_heads: int = 4
    hidden_dim: int = 512
    char_context: int = 128
    max_seq_len: int = 1024
    batch_size: int = 4
    n_steps: int = 3000
    eval_every: int = 500
    gen_every: int = 1500
    gen_chars: int = 100
    lr: float = 3e-4
    lr_warmup: int = 20
    weight_decay: float = 0.01
    gen_temp: float = 0.8
    d_in: int = 0   # 0 = use dim
    d_out: int = 0  # 0 = use dim
    device: str = "cpu"
    data_path: str = "shakespeare.txt"
    seed: int = 42
    csv_path: str = ""  # auto-generated if empty


def load_data(path):
    """Load text file as bytes (7-bit ASCII)."""
    with open(path, "rb") as f:
        data = f.read()
    # Mask to 7-bit ASCII
    return bytes(b & 0x7F for b in data)


def make_batches(data_tokens, seq_len, batch_size, device, rng):
    """Sample a random batch of (input, target) token sequences."""
    data_len = len(data_tokens)
    input_ids = torch.zeros(batch_size, seq_len, dtype=torch.long, device=device)
    target_ids = torch.zeros(batch_size, seq_len, dtype=torch.long, device=device)
    for b in range(batch_size):
        start = rng.randint(0, data_len - seq_len - 2)
        input_ids[b] = data_tokens[start:start + seq_len]
        target_ids[b] = data_tokens[start + 1:start + 1 + seq_len]
    return input_ids, target_ids


@torch.no_grad()
def evaluate(model, val_tokens, seq_len, vocab_size, device, mode):
    """Evaluate on validation set. Returns (loss, bpc, ppl)."""
    model.eval()
    n_seqs = len(val_tokens) // (seq_len + 1)
    n_seqs = min(n_seqs, 50)
    if n_seqs == 0:
        return 99.0, 99.0, 999.0

    total_loss = 0.0
    for s in range(n_seqs):
        start = s * (seq_len + 1)
        inp = val_tokens[start:start + seq_len].unsqueeze(0).to(device)
        tgt = val_tokens[start + 1:start + 1 + seq_len].unsqueeze(0).to(device)
        logits = model(inp)
        loss = F.cross_entropy(logits.view(-1, vocab_size), tgt.view(-1))
        total_loss += loss.item()

    avg_loss = total_loss / n_seqs
    bpc = loss_to_bpc(avg_loss, mode)
    ppl = math.exp(avg_loss)
    model.train()
    return avg_loss, bpc, ppl


@torch.no_grad()
def generate_text(model, prompt, gen_chars, mode, temperature, device, rng):
    """Generate text autoregressively."""
    model.eval()
    prompt_bytes = prompt.encode("ascii", errors="replace")
    prompt_tokens = encode_text(prompt_bytes, mode)

    cfg = MODE_CONFIG[mode]
    if mode == "bigram":
        gen_tokens = gen_chars // 2
    else:
        gen_tokens = gen_chars * cfg["tpc_int"]

    max_seq = model.max_seq_len
    total_len = len(prompt_tokens) + gen_tokens
    if total_len > max_seq:
        total_len = max_seq
    gen_tokens = total_len - len(prompt_tokens)
    if gen_tokens <= 0:
        model.train()
        return ""

    tokens = list(prompt_tokens)
    for _ in range(gen_tokens):
        inp = torch.tensor([tokens], dtype=torch.long, device=device)
        logits = model(inp)
        next_logits = logits[0, -1, :]
        if temperature < 1e-6:
            next_tok = next_logits.argmax().item()
        else:
            probs = F.softmax(next_logits / temperature, dim=-1)
            next_tok = torch.multinomial(probs, 1, generator=rng).item()
        tokens.append(next_tok)

    text = decode_tokens(tokens, mode)
    model.train()
    return text


def train(cfg: TrainConfig):
    """Full training run. Returns (final_bpc, final_loss, final_ppl, total_time)."""

    device = torch.device(cfg.device)
    torch.manual_seed(cfg.seed)
    rng = torch.Generator(device=device)
    rng.manual_seed(cfg.seed + 1)
    rng_gen = torch.Generator(device=device)
    rng_gen.manual_seed(12345)

    mode = cfg.mode
    mcfg = MODE_CONFIG[mode]
    vocab_size = mcfg["vocab"]
    seq_len = get_seq_len(mode, cfg.char_context)

    # Resolve d_in / d_out
    d_in = cfg.d_in if cfg.d_in > 0 else cfg.dim
    d_out = cfg.d_out if cfg.d_out > 0 else cfg.dim

    print("=" * 40)
    print(f"Tokenization Experiment: {mode}")
    print("=" * 40)

    # Load and split data
    text_bytes = load_data(cfg.data_path)
    text_len = len(text_bytes)
    print(f"\nData: {text_len} chars loaded")

    train_char_len = text_len * 9 // 10
    if mode == "bigram":
        train_char_len &= ~1
    val_char_len = text_len - train_char_len
    if mode == "bigram":
        val_char_len &= ~1

    train_tokens = torch.tensor(
        encode_text(text_bytes[:train_char_len], mode), dtype=torch.long
    )
    val_tokens = torch.tensor(
        encode_text(text_bytes[train_char_len:train_char_len + val_char_len], mode),
        dtype=torch.long,
    )

    print(f"Train: {train_char_len} chars -> {len(train_tokens)} tokens "
          f"({len(train_tokens)/train_char_len:.1f} tok/char)")
    print(f"Val:   {val_char_len} chars -> {len(val_tokens)} tokens")

    # Create model
    model = GPTModel(
        vocab_size=vocab_size,
        dim=cfg.dim,
        n_layers=cfg.n_layers,
        n_heads=cfg.n_heads,
        hidden_dim=cfg.hidden_dim,
        max_seq_len=cfg.max_seq_len,
        d_in=d_in,
        d_out=d_out,
    ).to(device)

    n_params = model.count_params()
    emb_params = model.count_embedding_params()
    head_params = model.count_head_params()
    body_params = n_params - emb_params - head_params

    print(f"\nMode: {mode} (vocab={vocab_size}, seq_len={seq_len} tokens, "
          f"{cfg.char_context} chars context)")
    print(f"Model: {cfg.n_layers} layers, dim={cfg.dim}, heads={cfg.n_heads}, "
          f"hidden={cfg.hidden_dim}")
    if d_in != cfg.dim or d_out != cfg.dim:
        print(f"Factored: d_in={d_in}, d_out={d_out}")
    print(f"Parameters: {n_params} ({n_params/1e3:.1f}K)")
    print(f"  Embedding: {emb_params} ({emb_params/1e3:.1f}K) = "
          f"{100.0*emb_params/n_params:.1f}% of total"
          + (f" [factored: V*{d_in} + {d_in}*{cfg.dim}]" if d_in != cfg.dim else ""))
    print(f"  Output head: {head_params} ({head_params/1e3:.1f}K) = "
          f"{100.0*head_params/n_params:.1f}% of total"
          + (f" [factored: {cfg.dim}*{d_out} + {d_out}*V]" if d_out != cfg.dim else ""))
    print(f"  Transformer body: {body_params} ({body_params/1e3:.1f}K) = "
          f"{100.0*body_params/n_params:.1f}% of total")
    print(f"Random baseline BPC: {random_baseline_bpc(mode):.2f}")
    print(f"Device: {device}")

    if mode == "bigram" and d_out < vocab_size:
        print(f"NOTE: softmax bottleneck -- vocab={vocab_size} > d_out={d_out} "
              f"(rank limited)")

    # CSV log
    if not cfg.csv_path:
        if d_in != cfg.dim or d_out != cfg.dim:
            cfg.csv_path = f"{mode}_din{d_in}_dout{d_out}.csv"
        else:
            cfg.csv_path = f"{mode}.csv"
    csv_file = open(cfg.csv_path, "w")
    csv_file.write("mode,step,chars_seen,loss,smooth_loss,"
                   "bpc,val_loss,val_ppl,"
                   "ms_per_step,chars_per_sec,elapsed_sec,lr\n")
    print(f"CSV log: {cfg.csv_path}")

    # Optimizer
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=cfg.lr, betas=(0.9, 0.999),
        eps=1e-8, weight_decay=cfg.weight_decay,
    )

    lr_min = cfg.lr * 0.1

    # Training loop
    print(f"\n--- Training ---")
    print(f"Steps: {cfg.n_steps}, seq_len: {seq_len} tokens ({cfg.char_context} chars), "
          f"batch: {cfg.batch_size}, lr: {cfg.lr:.6f}")

    t_start = time.time()
    smooth_loss = 0.0

    for step in range(cfg.n_steps):
        # LR schedule
        lr = get_lr(step, cfg.n_steps, cfg.lr, lr_min, cfg.lr_warmup)
        for pg in optimizer.param_groups:
            pg["lr"] = lr

        # Train step
        step_t0 = time.time()
        inp, tgt = make_batches(
            train_tokens, seq_len, cfg.batch_size, device,
            torch.Generator().manual_seed(step * 137 + cfg.seed),
        )
        logits = model(inp)
        loss = F.cross_entropy(logits.view(-1, vocab_size), tgt.view(-1))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        step_time = time.time() - step_t0
        loss_val = loss.item()

        if step == 0:
            smooth_loss = loss_val
        else:
            smooth_loss = 0.95 * smooth_loss + 0.05 * loss_val

        # Eval
        if step % cfg.eval_every == 0 or step == cfg.n_steps - 1:
            val_loss, val_bpc, val_ppl = evaluate(
                model, val_tokens, seq_len, vocab_size, device, mode
            )
            chars_per_step = cfg.batch_size * cfg.char_context
            chars_per_sec = chars_per_step / step_time if step_time > 0 else 0

            print(f"  Step {step:4d}/{cfg.n_steps}: loss={loss_val:.4f} "
                  f"smooth={smooth_loss:.4f} | "
                  f"val_bpc={val_bpc:.3f} val_loss={val_loss:.4f} "
                  f"val_ppl={val_ppl:.2f} | "
                  f"lr={lr:.6f} {step_time*1000:.1f}ms/step "
                  f"{chars_per_sec:.0f} char/s")

            elapsed = time.time() - t_start
            chars_seen = (step + 1) * cfg.batch_size * cfg.char_context
            csv_file.write(
                f"{mode},{step},{chars_seen},{loss_val:.4f},{smooth_loss:.4f},"
                f"{val_bpc:.3f},{val_loss:.4f},{val_ppl:.2f},"
                f"{step_time*1000:.1f},{chars_per_sec:.0f},{elapsed:.1f},{lr:.6f}\n"
            )
            csv_file.flush()

        # Generate sample
        if step > 0 and step % cfg.gen_every == 0:
            rng_gen.manual_seed(12345)
            sample = generate_text(
                model, "The ", cfg.gen_chars, mode, cfg.gen_temp, device, rng_gen
            )
            print(f"  [Sample] {sample}")

    total_time = time.time() - t_start
    ms_per_step = (total_time / cfg.n_steps) * 1000.0

    # Final eval
    final_loss, final_bpc, final_ppl = evaluate(
        model, val_tokens, seq_len, vocab_size, device, mode
    )

    print(f"\nTraining complete: {total_time:.1f} sec ({ms_per_step:.1f} ms/step)")
    print(f"Final val BPC:  {final_bpc:.3f}")
    print(f"Final val loss: {final_loss:.4f} nats/token")
    print(f"Final val PPL:  {final_ppl:.2f} (per-token)")

    # Final generation
    prompts = ["The ", "KING:\n", "To be"]
    print("\n--- Generated Samples ---")
    for p in prompts:
        rng_gen.manual_seed(42 + prompts.index(p))
        sample = generate_text(
            model, p, cfg.gen_chars, mode, cfg.gen_temp, device, rng_gen
        )
        print(f'  [Prompt: "{p}"]')
        print(f"  {sample}\n")

    csv_file.close()

    # Machine-readable summary
    print(f"\nSUMMARY:{mode},{vocab_size},{MODE_CONFIG[mode]['tpc_f']:.1f},"
          f"{seq_len},{d_in},{d_out},{n_params},"
          f"{final_bpc:.3f},{final_loss:.4f},{final_ppl:.2f},"
          f"{total_time:.1f},{random_baseline_bpc(mode):.2f}")

    return final_bpc, final_loss, final_ppl, total_time


# ========================================================================
# CLI
# ========================================================================

def main():
    parser = argparse.ArgumentParser(description="Tokenization experiment (PyTorch)")
    parser.add_argument("--mode", type=str, default="char",
                        choices=list(MODE_CONFIG.keys()))
    parser.add_argument("--dim", type=int, default=128)
    parser.add_argument("--n_layers", type=int, default=4)
    parser.add_argument("--n_heads", type=int, default=4)
    parser.add_argument("--hidden_dim", type=int, default=512)
    parser.add_argument("--char_context", type=int, default=128)
    parser.add_argument("--max_seq_len", type=int, default=1024)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--n_steps", type=int, default=3000)
    parser.add_argument("--eval_every", type=int, default=500)
    parser.add_argument("--gen_every", type=int, default=1500)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--lr_warmup", type=int, default=20)
    parser.add_argument("--weight_decay", type=float, default=0.01)
    parser.add_argument("--d_in", type=int, default=0, help="0 = use dim")
    parser.add_argument("--d_out", type=int, default=0, help="0 = use dim")
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--data_path", type=str, default="shakespeare.txt")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--csv_path", type=str, default="")
    args = parser.parse_args()

    cfg = TrainConfig(**vars(args))
    train(cfg)


if __name__ == "__main__":
    main()
