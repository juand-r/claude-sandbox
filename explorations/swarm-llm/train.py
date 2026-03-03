"""
Swarm LLM: Can a swarm of small communicating transformers match a single larger one?

Experiment: character-level language modeling on Shakespeare.
- Baseline: single ~800K param transformer
- Swarm: 5 x ~120K param transformers with learned message passing

Usage:
    python train.py --mode baseline --n_steps 500
    python train.py --mode swarm --n_steps 500
"""

import argparse
import json
import math
import os
import time

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader


# ============================================================================
# Data
# ============================================================================

class CharDataset(Dataset):
    """Character-level dataset. Returns (input, target) chunks."""

    def __init__(self, text, context_len, char2idx):
        self.data = torch.tensor([char2idx[c] for c in text], dtype=torch.long)
        self.context_len = context_len

    def __len__(self):
        return max(0, len(self.data) - self.context_len)

    def __getitem__(self, idx):
        chunk = self.data[idx : idx + self.context_len + 1]
        return chunk[:-1], chunk[1:]


def load_shakespeare(context_len):
    """Load Shakespeare data, split 90/10, return datasets + vocab size."""
    for path in [
        "data/shakespeare.txt",
        "../distributed-llm-training/experiments/predictive_features/data/shakespeare.txt",
    ]:
        if os.path.exists(path):
            with open(path, "r") as f:
                text = f.read()
            break
    else:
        raise FileNotFoundError("shakespeare.txt not found. Place it in data/")

    chars = sorted(set(text))
    char2idx = {c: i for i, c in enumerate(chars)}
    vocab_size = len(chars)

    split = int(0.9 * len(text))
    train_ds = CharDataset(text[:split], context_len, char2idx)
    val_ds = CharDataset(text[split:], context_len, char2idx)

    print(f"Vocab size: {vocab_size}, Train: {split} chars, Val: {len(text) - split} chars")
    return train_ds, val_ds, vocab_size


# ============================================================================
# Model components
# ============================================================================

class TransformerBlock(nn.Module):
    def __init__(self, embed_dim, n_heads, ffn_dim, dropout=0.1):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim, n_heads, dropout=dropout, batch_first=True)
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, ffn_dim),
            nn.GELU(),
            nn.Linear(ffn_dim, embed_dim),
        )
        self.ln1 = nn.LayerNorm(embed_dim)
        self.ln2 = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        T = x.shape[1]
        # Causal mask: True = masked (can't attend)
        causal_mask = torch.triu(torch.ones(T, T, device=x.device), diagonal=1).bool()
        normed = self.ln1(x)
        attn_out, _ = self.attn(normed, normed, normed, attn_mask=causal_mask)
        x = x + self.dropout(attn_out)
        x = x + self.dropout(self.ffn(self.ln2(x)))
        return x


class SmallTransformer(nn.Module):
    """A small transformer for character-level LM."""

    def __init__(self, vocab_size, embed_dim, n_layers, n_heads, ffn_dim, context_len, dropout=0.1):
        super().__init__()
        self.embed_dim = embed_dim
        self.context_len = context_len

        self.tok_emb = nn.Embedding(vocab_size, embed_dim)
        self.pos_emb = nn.Embedding(context_len + 32, embed_dim)  # +32 for prefix room
        self.blocks = nn.ModuleList([
            TransformerBlock(embed_dim, n_heads, ffn_dim, dropout)
            for _ in range(n_layers)
        ])
        self.ln_final = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, vocab_size, bias=False)
        # Weight tying
        self.head.weight = self.tok_emb.weight

        self._init_weights()

    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def forward(self, idx, prefix_embeds=None):
        """
        idx: (B, T) token indices
        prefix_embeds: optional (B, P, D) to prepend as message tokens
        Returns: (logits (B, T, V), hidden (B, P+T, D))
        """
        B, T = idx.shape
        tok = self.tok_emb(idx)

        if prefix_embeds is not None:
            P = prefix_embeds.shape[1]
            prefix_pos = self.pos_emb(torch.arange(P, device=idx.device))
            tok_pos = self.pos_emb(torch.arange(P, P + T, device=idx.device))
            x = torch.cat([prefix_embeds + prefix_pos, tok + tok_pos], dim=1)
        else:
            P = 0
            pos = self.pos_emb(torch.arange(T, device=idx.device))
            x = tok + pos

        for block in self.blocks:
            x = block(x)

        x = self.ln_final(x)
        logits = self.head(x[:, P:, :])  # only token positions
        return logits, x


# ============================================================================
# Baseline: single larger transformer
# ============================================================================

class BaselineModel(nn.Module):
    def __init__(self, vocab_size, context_len):
        super().__init__()
        self.model = SmallTransformer(
            vocab_size=vocab_size,
            embed_dim=128,
            n_layers=4,
            n_heads=4,
            ffn_dim=512,
            context_len=context_len,
        )

    def forward(self, idx):
        logits, _ = self.model(idx)
        return logits


# ============================================================================
# Swarm: N small transformers with message passing
# ============================================================================

class SwarmModel(nn.Module):
    """
    N small transformers that communicate via learned continuous messages.

    Each round:
    - Each model processes input (+ messages from others as prefix tokens)
    - Produces a message vector (mean-pooled hidden states -> linear)
    - Messages are exchanged for next round

    Final output: learned weighted sum of all models' logits.
    """

    def __init__(self, vocab_size, context_len, n_models=5, msg_dim=64, n_rounds=2):
        super().__init__()
        self.n_models = n_models
        self.n_rounds = n_rounds
        self.msg_dim = msg_dim

        embed_dim = 64

        self.models = nn.ModuleList([
            SmallTransformer(
                vocab_size=vocab_size,
                embed_dim=embed_dim,
                n_layers=2,
                n_heads=2,
                ffn_dim=256,
                context_len=context_len,
            )
            for _ in range(n_models)
        ])

        # Message extraction: hidden -> message
        self.msg_encoders = nn.ModuleList([
            nn.Linear(embed_dim, msg_dim) for _ in range(n_models)
        ])

        # Message injection: message -> prefix embedding
        self.msg_projectors = nn.ModuleList([
            nn.Linear(msg_dim, embed_dim) for _ in range(n_models)
        ])

        # Residual connection layer norms for messages
        self.msg_layer_norms = nn.ModuleList([
            nn.LayerNorm(msg_dim) for _ in range(n_models)
        ])

        # Learned output aggregation weights
        self.agg_weights = nn.Parameter(torch.zeros(n_models))

    def forward(self, idx):
        B, T = idx.shape

        # Initialize messages as zeros
        messages = [torch.zeros(B, self.msg_dim, device=idx.device) for _ in range(self.n_models)]

        all_logits = None

        for round_idx in range(self.n_rounds + 1):
            new_messages = []
            round_logits = []

            for i in range(self.n_models):
                # Build prefix from other models' messages
                if round_idx == 0:
                    prefix = None
                else:
                    other_msgs = [messages[j] for j in range(self.n_models) if j != i]
                    other_msgs = torch.stack(other_msgs, dim=1)  # (B, n-1, msg_dim)
                    prefix = self.msg_projectors[i](other_msgs)  # (B, n-1, embed_dim)

                logits, hidden = self.models[i](idx, prefix_embeds=prefix)
                round_logits.append(logits)

                # Extract message from token hidden states (mean pool)
                n_prefix = 0 if prefix is None else prefix.shape[1]
                token_hidden = hidden[:, n_prefix:, :]  # (B, T, D)
                pooled = token_hidden.mean(dim=1)  # (B, D)
                new_msg = self.msg_encoders[i](pooled)  # (B, msg_dim)

                # Residual on messages (after round 0)
                if round_idx > 0:
                    new_msg = self.msg_layer_norms[i](messages[i] + new_msg)

                new_messages.append(new_msg)

            messages = new_messages
            all_logits = round_logits

        # Weighted sum of final-round logits
        weights = F.softmax(self.agg_weights, dim=0)
        stacked = torch.stack(all_logits, dim=0)  # (n_models, B, T, V)
        combined = (stacked * weights.view(-1, 1, 1, 1)).sum(dim=0)

        return combined


# ============================================================================
# Training
# ============================================================================

def count_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


@torch.no_grad()
def evaluate(model, dataloader, device):
    model.eval()
    total_loss = 0.0
    total_tokens = 0
    for x, y in dataloader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), y.reshape(-1))
        total_loss += loss.item() * y.numel()
        total_tokens += y.numel()
    model.train()
    avg_loss = total_loss / total_tokens
    return avg_loss, math.exp(avg_loss)


def train(args):
    device = torch.device("cpu")

    train_ds, val_ds, vocab_size = load_shakespeare(args.context_len)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, drop_last=True)

    if args.mode == "baseline":
        model = BaselineModel(vocab_size, args.context_len)
    elif args.mode == "swarm":
        model = SwarmModel(
            vocab_size, args.context_len,
            n_models=args.n_models,
            msg_dim=args.msg_dim,
            n_rounds=args.n_rounds,
        )
    else:
        raise ValueError(f"Unknown mode: {args.mode}")

    model = model.to(device)
    n_params = count_params(model)
    print(f"Mode: {args.mode}, Parameters: {n_params:,}")

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)

    # LR schedule: linear warmup then cosine decay
    warmup_steps = min(200, args.n_steps // 10)

    def lr_schedule(step):
        if step < warmup_steps:
            return step / warmup_steps
        progress = (step - warmup_steps) / max(1, args.n_steps - warmup_steps)
        return 0.5 * (1.0 + math.cos(math.pi * progress))

    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_schedule)

    print(f"\nTraining for {args.n_steps} steps...")
    print(f"{'Step':>6} {'TrainLoss':>10} {'ValLoss':>10} {'ValPPL':>10} {'s/step':>8}")
    print("-" * 50)

    step = 0
    train_loss_accum = 0.0
    results = []
    start_time = time.time()

    while step < args.n_steps:
        for x, y in train_loader:
            if step >= args.n_steps:
                break

            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), y.reshape(-1))

            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()

            train_loss_accum += loss.item()
            step += 1

            if step % args.log_interval == 0:
                avg_train = train_loss_accum / args.log_interval
                train_loss_accum = 0.0
                val_loss, val_ppl = evaluate(model, val_loader, device)
                elapsed = time.time() - start_time

                results.append({
                    "step": step,
                    "train_loss": avg_train,
                    "val_loss": val_loss,
                    "val_ppl": val_ppl,
                    "elapsed": elapsed,
                })

                print(f"{step:>6} {avg_train:>10.4f} {val_loss:>10.4f} {val_ppl:>10.2f} {elapsed/step:>7.2f}s")

    total_time = time.time() - start_time
    final_val_loss, final_val_ppl = evaluate(model, val_loader, device)

    print(f"\nDone. {total_time:.1f}s total.")
    print(f"Final val loss: {final_val_loss:.4f}, val PPL: {final_val_ppl:.2f}")

    # Save results
    os.makedirs("results", exist_ok=True)
    with open(f"results/{args.mode}_results.json", "w") as f:
        json.dump({
            "mode": args.mode,
            "n_params": n_params,
            "total_time": total_time,
            "final_val_loss": final_val_loss,
            "final_val_ppl": final_val_ppl,
            "steps": results,
            "args": vars(args),
        }, f, indent=2)

    if args.mode == "swarm":
        weights = F.softmax(model.agg_weights, dim=0)
        print(f"Aggregation weights: {[f'{w:.3f}' for w in weights.tolist()]}")

    # Save checkpoint
    os.makedirs("checkpoints", exist_ok=True)
    ckpt_path = f"checkpoints/{args.mode}.pt"
    torch.save({
        "model_state_dict": model.state_dict(),
        "vocab_size": vocab_size,
        "args": vars(args),
    }, ckpt_path)
    print(f"Checkpoint saved to {ckpt_path}")

    return model, vocab_size, final_val_loss, final_val_ppl


# ============================================================================
# Text generation
# ============================================================================

@torch.no_grad()
def generate(model, idx, max_new_tokens, context_len, temperature=0.8, top_k=40):
    """Autoregressive generation. idx is (1, T) starting context."""
    model.eval()
    for _ in range(max_new_tokens):
        # Crop to context window
        idx_cond = idx[:, -context_len:]
        logits = model(idx_cond)
        # Take logits at last position
        logits = logits[:, -1, :] / temperature
        # Top-k filtering
        if top_k > 0:
            v, _ = torch.topk(logits, top_k)
            logits[logits < v[:, [-1]]] = float("-inf")
        probs = F.softmax(logits, dim=-1)
        next_tok = torch.multinomial(probs, num_samples=1)
        idx = torch.cat([idx, next_tok], dim=1)
    return idx


def run_generate(args):
    """Load checkpoint and generate text."""
    device = torch.device("cpu")

    # Load vocab
    for path in [
        "data/shakespeare.txt",
        "../distributed-llm-training/experiments/predictive_features/data/shakespeare.txt",
    ]:
        if os.path.exists(path):
            with open(path, "r") as f:
                text = f.read()
            break
    else:
        raise FileNotFoundError("shakespeare.txt not found")

    chars = sorted(set(text))
    char2idx = {c: i for i, c in enumerate(chars)}
    idx2char = {i: c for c, i in char2idx.items()}
    vocab_size = len(chars)

    # Load checkpoint
    ckpt_path = f"checkpoints/{args.mode}.pt"
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    saved_args = ckpt["args"]

    if args.mode == "baseline":
        model = BaselineModel(vocab_size, saved_args["context_len"])
    elif args.mode == "swarm":
        model = SwarmModel(
            vocab_size, saved_args["context_len"],
            n_models=saved_args["n_models"],
            msg_dim=saved_args["msg_dim"],
            n_rounds=saved_args["n_rounds"],
        )

    model.load_state_dict(ckpt["model_state_dict"])
    model = model.to(device)
    model.eval()

    # Encode prompt
    prompt = args.prompt
    prompt_idx = torch.tensor([[char2idx[c] for c in prompt]], dtype=torch.long, device=device)

    print(f"--- {args.mode} (prompt: '{prompt}') ---")
    t0 = time.time()
    output_idx = generate(model, prompt_idx, args.gen_length, saved_args["context_len"],
                          temperature=args.temperature)
    elapsed = time.time() - t0
    output_text = "".join(idx2char[i] for i in output_idx[0].tolist())
    print(output_text)
    print(f"--- ({elapsed:.1f}s for {args.gen_length} chars, {args.gen_length/elapsed:.1f} char/s) ---")


def main():
    parser = argparse.ArgumentParser(description="Swarm LLM experiment")
    sub = parser.add_subparsers(dest="command")

    # Train subcommand
    train_p = sub.add_parser("train")
    train_p.add_argument("--mode", type=str, required=True, choices=["baseline", "swarm"])
    train_p.add_argument("--context_len", type=int, default=128)
    train_p.add_argument("--batch_size", type=int, default=64)
    train_p.add_argument("--lr", type=float, default=3e-3)
    train_p.add_argument("--n_steps", type=int, default=2000)
    train_p.add_argument("--log_interval", type=int, default=100)
    train_p.add_argument("--n_models", type=int, default=5)
    train_p.add_argument("--msg_dim", type=int, default=64)
    train_p.add_argument("--n_rounds", type=int, default=2)

    # Generate subcommand
    gen_p = sub.add_parser("generate")
    gen_p.add_argument("--mode", type=str, required=True, choices=["baseline", "swarm"])
    gen_p.add_argument("--prompt", type=str, default="ROMEO:\n")
    gen_p.add_argument("--gen_length", type=int, default=500)
    gen_p.add_argument("--temperature", type=float, default=0.8)

    args = parser.parse_args()

    if args.command == "train":
        train(args)
    elif args.command == "generate":
        run_generate(args)
    else:
        # Legacy: support --mode directly for backward compat
        parser.print_help()


if __name__ == "__main__":
    main()
