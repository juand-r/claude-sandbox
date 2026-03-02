"""
Run the predictive features experiment.

Trains a small character-level transformer with multiple hyperparameter configs,
logging features at each PPL milestone. The output is a JSON-lines file where
each record is (config, stage, features, time_to_next_milestone).

Usage:
    python run_experiment.py [--quick]        # Quick smoke test (2 configs)
    python run_experiment.py [--workers 12]   # Parallel across 12 CPU cores
"""

import argparse
import json
import math
import multiprocessing as mp
import os
import sys
import time
import urllib.request
from pathlib import Path
from itertools import cycle

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from milestone_features import compute_all_features


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

DATA_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
DATA_DIR = Path(__file__).parent / "data"


def download_data() -> str:
    """Download tiny shakespeare if not present, return text."""
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / "shakespeare.txt"
    if not path.exists():
        print(f"Downloading tiny shakespeare to {path}...")
        urllib.request.urlretrieve(DATA_URL, path)
    return path.read_text()


class CharDataset:
    """Character-level dataset. Produces (input, target) pairs of token IDs."""

    def __init__(self, text: str, seq_len: int = 64):
        chars = sorted(set(text))
        self.stoi = {c: i for i, c in enumerate(chars)}
        self.itos = {i: c for c, i in self.stoi.items()}
        self.vocab_size = len(chars)
        self.data = torch.tensor([self.stoi[c] for c in text], dtype=torch.long)
        self.seq_len = seq_len

    def batch_iter(self, batch_size: int, shuffle: bool = True):
        """Yield (input, target) batches indefinitely."""
        n = len(self.data) - self.seq_len - 1
        indices = list(range(n))
        while True:
            if shuffle:
                np.random.shuffle(indices)
            for start in range(0, len(indices) - batch_size, batch_size):
                batch_idx = indices[start : start + batch_size]
                x = torch.stack([self.data[i : i + self.seq_len] for i in batch_idx])
                y = torch.stack([self.data[i + 1 : i + self.seq_len + 1] for i in batch_idx])
                yield x, y


# ---------------------------------------------------------------------------
# Model: small GPT-2 style transformer
# ---------------------------------------------------------------------------

class CausalSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, seq_len: int):
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.qkv = nn.Linear(d_model, 3 * d_model)
        self.proj = nn.Linear(d_model, d_model)
        # Causal mask
        self.register_buffer(
            "mask",
            torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0).unsqueeze(0),
        )

    def forward(self, x):
        B, T, C = x.shape
        qkv = self.qkv(x).reshape(B, T, 3, self.n_heads, self.head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)  # (3, B, H, T, D)
        q, k, v = qkv[0], qkv[1], qkv[2]

        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        att = att.masked_fill(self.mask[:, :, :T, :T] == 0, float("-inf"))
        att = F.softmax(att, dim=-1)
        out = (att @ v).transpose(1, 2).reshape(B, T, C)
        return self.proj(out)


class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, seq_len: int):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = CausalSelfAttention(d_model, n_heads, seq_len)
        self.ln2 = nn.LayerNorm(d_model)
        self.mlp = nn.Sequential(
            nn.Linear(d_model, 4 * d_model),
            nn.GELU(),
            nn.Linear(4 * d_model, d_model),
        )

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        x = x + self.mlp(self.ln2(x))
        return x


class SmallGPT(nn.Module):
    def __init__(self, vocab_size: int, d_model: int = 128, n_heads: int = 4,
                 n_layers: int = 4, seq_len: int = 64):
        super().__init__()
        self.tok_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(seq_len, d_model)
        self.blocks = nn.Sequential(*[
            TransformerBlock(d_model, n_heads, seq_len) for _ in range(n_layers)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)
        self.seq_len = seq_len

    def forward(self, idx):
        B, T = idx.shape
        tok = self.tok_emb(idx)
        pos = self.pos_emb(torch.arange(T, device=idx.device))
        x = self.blocks(tok + pos)
        x = self.ln_f(x)
        return self.head(x)

    def param_count(self):
        return sum(p.numel() for p in self.parameters())


# ---------------------------------------------------------------------------
# Training logic
# ---------------------------------------------------------------------------

def make_loss_fn(model_forward=None):
    """Return a loss function with signature loss_fn(model, batch) -> scalar."""
    def loss_fn(model, batch):
        x, y = batch
        logits = model(x)
        return F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
    return loss_fn


def train_one_config(
    config: dict,
    dataset: CharDataset,
    milestones: list,
    max_steps: int = 10000,
    expensive_features: bool = True,
    log_every: int = 10,
) -> list:
    """Train a model with given config, log features at each PPL milestone.

    Returns list of milestone records:
        [{"config": ..., "stage": ..., "features": ..., "ppl_at_milestone": ...,
          "steps_at_milestone": ..., "wall_time_at_milestone": ...}, ...]
    """
    seed = config["seed"]
    torch.manual_seed(seed)
    np.random.seed(seed)

    model = SmallGPT(
        vocab_size=dataset.vocab_size,
        d_model=config.get("d_model", 128),
        n_heads=config.get("n_heads", 4),
        n_layers=config.get("n_layers", 4),
        seq_len=config.get("seq_len", 64),
    )
    print(f"  Model params: {model.param_count():,}")

    optimizer = torch.optim.Adam(model.parameters(), lr=config["lr"])
    loss_fn = make_loss_fn()

    # Save initial weights for distance-from-init feature
    initial_weights = {name: p.data.clone() for name, p in model.named_parameters()}

    # Training state
    data_iter = dataset.batch_iter(config["batch_size"])
    history = {"loss": [], "ppl": [], "timestamps": []}
    milestone_records = []
    current_milestone_idx = 0
    t0 = time.time()
    model.train()

    for step in range(1, max_steps + 1):
        batch = next(data_iter)
        optimizer.zero_grad()
        loss = loss_fn(model, batch)
        loss.backward()
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

        loss_val = loss.item()
        ppl = math.exp(min(loss_val, 20.0))  # clip to avoid overflow
        elapsed = time.time() - t0

        history["loss"].append(loss_val)
        history["ppl"].append(ppl)
        history["timestamps"].append(elapsed)

        if log_every > 0 and step % log_every == 0:
            print(f"    step {step:5d} | loss {loss_val:.4f} | ppl {ppl:.2f} | {elapsed:.1f}s")

        # Check if we hit a milestone
        if current_milestone_idx < len(milestones) and ppl <= milestones[current_milestone_idx]:
            stage = current_milestone_idx
            print(f"  ** Milestone {stage}: PPL {milestones[stage]} reached at step {step} ({elapsed:.1f}s)")

            # Create a separate data iterator for feature computation
            feature_data_iter = dataset.batch_iter(config["batch_size"], shuffle=True)
            # Get a single batch for sharpness/hessian
            feature_batch = next(feature_data_iter)

            features = compute_all_features(
                model=model,
                optimizer=optimizer,
                loss_fn=loss_fn,
                initial_weights=initial_weights,
                history=history,
                config=config,
                stage=stage,
                steps=step,
                wall_time=elapsed,
                data_iter=feature_data_iter,
                data_batch=feature_batch,
                expensive=expensive_features,
            )

            milestone_records.append({
                "config": config,
                "stage": stage,
                "milestone_ppl": milestones[stage],
                "features": features,
                "steps_at_milestone": step,
                "wall_time_at_milestone": elapsed,
            })

            current_milestone_idx += 1
            if current_milestone_idx >= len(milestones):
                print(f"  All milestones reached at step {step}.")
                break

    if current_milestone_idx < len(milestones):
        print(f"  WARNING: Only reached {current_milestone_idx}/{len(milestones)} milestones "
              f"in {max_steps} steps. Final PPL: {ppl:.2f}")

    return milestone_records


def add_time_to_next(records: list) -> list:
    """For each milestone record, compute time/steps to the next milestone.

    Records from the same config are consecutive. The last milestone for each
    config gets time_to_next = None (no next milestone).
    """
    # Group by config_id
    by_config = {}
    for r in records:
        cid = config_id(r["config"])
        if cid not in by_config:
            by_config[cid] = []
        by_config[cid].append(r)

    enriched = []
    for cid, recs in by_config.items():
        recs.sort(key=lambda r: r["stage"])
        for i, r in enumerate(recs):
            if i + 1 < len(recs):
                r["time_to_next"] = recs[i + 1]["wall_time_at_milestone"] - r["wall_time_at_milestone"]
                r["steps_to_next"] = recs[i + 1]["steps_at_milestone"] - r["steps_at_milestone"]
            else:
                r["time_to_next"] = None
                r["steps_to_next"] = None
            enriched.append(r)

    return enriched


def config_id(config: dict) -> str:
    return f"lr{config['lr']}_bs{config['batch_size']}_seed{config['seed']}"


# ---------------------------------------------------------------------------
# Multiprocessing worker
# ---------------------------------------------------------------------------

def _worker_init():
    """Pin each worker to 1 thread so they don't compete for cores."""
    torch.set_num_threads(1)


def _worker_run(args_tuple):
    """Run a single config in a worker process.

    Takes (config, milestones, max_steps, expensive_features, text, seq_len)
    and returns the milestone records list.
    """
    config, milestones, max_steps, expensive_features, text, seq_len = args_tuple

    torch.set_num_threads(1)
    dataset = CharDataset(text, seq_len=seq_len)

    cid = config_id(config)
    # Minimal per-worker logging (only milestone hits)
    records = train_one_config(
        config=config,
        dataset=dataset,
        milestones=milestones,
        max_steps=max_steps,
        expensive_features=expensive_features,
        log_every=0,  # suppress per-step logging in workers
    )
    n_milestones = len(records)
    print(f"  [{cid}] done: {n_milestones}/{len(milestones)} milestones reached")
    return records


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Predictive features experiment")
    parser.add_argument("--quick", action="store_true", help="Quick smoke test (2 configs)")
    parser.add_argument("--no-expensive", action="store_true", help="Skip expensive features")
    parser.add_argument("--max-steps", type=int, default=10000, help="Max training steps per config")
    parser.add_argument("--workers", type=int, default=0,
                        help="Number of parallel workers (0 = sequential, default; -1 = all cores)")
    args = parser.parse_args()

    # Download data
    text = download_data()
    dataset = CharDataset(text, seq_len=64)
    print(f"Dataset: {len(text):,} chars, vocab size: {dataset.vocab_size}")

    # Config grid
    seeds_full = [42, 123, 271, 314, 512, 619, 777, 888, 1024, 1337]
    if args.quick:
        configs = [
            {"lr": 1e-3, "batch_size": 32, "seed": 42},
            {"lr": 3e-3, "batch_size": 32, "seed": 42},
        ]
    else:
        configs = [
            {"lr": lr, "batch_size": bs, "seed": seed}
            for lr in [3e-4, 1e-3, 3e-3]
            for bs in [16, 32, 64]
            for seed in seeds_full
        ]

    # PPL milestones (character-level, initial PPL ≈ vocab_size ≈ 65)
    milestones = [50, 30, 20, 15, 12, 10, 8]
    seq_len = 64
    expensive = not args.no_expensive

    n_workers = args.workers
    if n_workers == -1:
        n_workers = mp.cpu_count()

    print(f"Running {len(configs)} configs, milestones: {milestones}")
    print(f"Max steps per config: {args.max_steps}")
    print(f"Workers: {n_workers if n_workers > 0 else 'sequential'}")
    print()

    all_records = []
    t_start = time.time()

    # Incremental output: write raw records as each config finishes, so
    # partial results survive if the session is interrupted.
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    raw_path = results_dir / "milestone_features_raw.jsonl"
    progress_path = results_dir / "progress.log"

    # Clear previous raw output
    raw_path.write_text("")

    def _save_records(records, f_raw, completed, total):
        """Append records to the raw JSONL file and update progress."""
        for r in records:
            f_raw.write(json.dumps(r, default=str) + "\n")
        f_raw.flush()
        elapsed = time.time() - t_start
        msg = f"[{completed}/{total}] +{len(records)} records, {elapsed:.0f}s elapsed"
        print(msg)
        with open(progress_path, "a") as pf:
            pf.write(msg + "\n")

    completed = 0
    with open(raw_path, "a") as f_raw:
        if n_workers > 0:
            # Parallel execution with incremental saving
            worker_args = [
                (config, milestones, args.max_steps, expensive, text, seq_len)
                for config in configs
            ]
            with mp.Pool(n_workers, initializer=_worker_init) as pool:
                for records in pool.imap_unordered(_worker_run, worker_args):
                    all_records.extend(records)
                    completed += 1
                    _save_records(records, f_raw, completed, len(configs))
        else:
            # Sequential execution (original behavior)
            for i, config in enumerate(configs):
                cid = config_id(config)
                print(f"[{i+1}/{len(configs)}] Config: {cid}")
                records = train_one_config(
                    config=config,
                    dataset=dataset,
                    milestones=milestones,
                    max_steps=args.max_steps,
                    expensive_features=expensive,
                )
                all_records.extend(records)
                completed += 1
                _save_records(records, f_raw, completed, len(configs))
                print()

    elapsed = time.time() - t_start
    print(f"\nAll configs done in {elapsed:.1f}s")

    # Add time_to_next for each record
    all_records = add_time_to_next(all_records)

    # Save final enriched results (with time_to_next computed)
    out_path = results_dir / "milestone_features.jsonl"

    with open(out_path, "w") as f:
        for r in all_records:
            f.write(json.dumps(r, default=str) + "\n")

    n_with_target = sum(1 for r in all_records if r["time_to_next"] is not None)
    print(f"Saved {len(all_records)} milestone records ({n_with_target} with time_to_next) to {out_path}")


if __name__ == "__main__":
    main()
