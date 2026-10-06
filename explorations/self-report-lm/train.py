"""Joint training: language modelling on TinyStories + self-report of embedding coordinates.

Each step: one language-modelling batch (LM_BATCH windows of CTX + 1 tokens from
train.bin) and, if lam > 0, one self-report batch (REPORT_BATCH random
(training token, coordinate) questions). Loss = cross-entropy + lam · (1 − R² of
the self-report batch). The correct answer E[t, i] is taken with no gradient.

AdamW, linear warm-up then cosine decay to LR_MIN; weight decay on the matrices
of the blocks and the number head only (not on E, P, biases, LayerNorm): decay
on E would shrink the very values being reported. Gradient norm clipped at 1.

Checkpoints (model, optimizer, step, log) are written at every evaluation to
results/<name>_ckpt.pt, and training resumes from there if it exists, so a
container restart loses at most EVAL_EVERY steps. The final model is
results/<name>.pt with its log in results/<name>.json.

Control (review of REPORT.md): with detach_input, the self-report sees E[t] with its
gradient blocked, so it trains the reader but cannot move the embedding table, which is
then shaped by language modelling alone.

Usage: python train.py <name> <lam> <seed> [steps] [detach]
"""
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

import lm

HERE = Path(__file__).parent
DATA, RESULTS = HERE / "data", HERE / "results"
STEPS = 15000
LM_BATCH = 32
REPORT_BATCH = 256
LR, LR_MIN, WARMUP = 2e-3, 2e-4, 200
BETAS = (0.9, 0.95)
WEIGHT_DECAY = 0.1
CLIP = 1.0
EVAL_EVERY = 250
EVAL_LM_BATCHES = 20          # validation loss on 20 × 32 fixed windows
EVAL_REPORT_TOKENS = 256      # self-report R² on 256 tokens × all coordinates, per set


def lr_at(step, steps):
    if step < WARMUP:
        return LR * (step + 1) / WARMUP
    frac = (step - WARMUP) / max(1, steps - WARMUP)
    return LR_MIN + 0.5 * (LR - LR_MIN) * (1 + math.cos(math.pi * frac))


def load_tokens(name):
    return np.fromfile(DATA / f"{name}.bin", dtype=np.uint16)


def lm_batch(tokens, n, gen):
    starts = torch.randint(0, len(tokens) - lm.CTX, (n,), generator=gen).numpy()   # windows of CTX + 1 tokens
    win = torch.from_numpy(np.stack([tokens[s:s + lm.CTX + 1] for s in starts]).astype(np.int64))
    return win[:, :-1], win[:, 1:]


def lm_loss(m, x, y):
    return F.cross_entropy(m.lm_logits(x).reshape(-1, m.n_text), y.reshape(-1))


def report_loss(m, t, i, detach_input=False):
    a = m.answer(m.E[t].detach(), i) if detach_input else m.report(t, i)
    target = m.E[t, i].detach()
    return ((a - target) ** 2).mean() / target.var(unbiased=False)


@torch.no_grad()
def evaluate(m, valid_batches, train_tokens, held_out):
    out = {"valid_loss": sum(lm_loss(m, x, y).item() for x, y in valid_batches) / len(valid_batches)}
    for name, toks in (("train", train_tokens[:EVAL_REPORT_TOKENS]), ("held_out", held_out[:EVAL_REPORT_TOKENS])):
        t = toks.repeat_interleave(m.dim)
        i = torch.arange(m.dim).repeat(len(toks))
        out[f"r2_{name}"] = lm.r2(m.report(t, i), m.E[t, i])
    out["E_rms_text"] = m.E[:m.n_text].pow(2).mean().sqrt().item()
    return out


def make_optimizer(m):
    decay = [p for n, p in m.named_parameters() if p.dim() == 2 and n.startswith(("blocks", "number_head"))]
    rest = [p for n, p in m.named_parameters() if not (p.dim() == 2 and n.startswith(("blocks", "number_head")))]
    return torch.optim.AdamW([{"params": decay, "weight_decay": WEIGHT_DECAY},
                              {"params": rest, "weight_decay": 0.0}], lr=LR, betas=BETAS)


def train(name, lam, seed, steps=STEPS, verbose=True, detach_input=False):
    RESULTS.mkdir(exist_ok=True)
    ckpt_path = RESULTS / f"{name}_ckpt.pt"
    settings = {"name": name, "lam": lam, "seed": seed, "steps": steps, "detach_input": detach_input, "lm_batch": LM_BATCH,
                "report_batch": REPORT_BATCH, "lr": LR, "lr_min": LR_MIN, "warmup": WARMUP,
                "weight_decay": WEIGHT_DECAY, "betas": list(BETAS), "clip": CLIP, "eval_every": EVAL_EVERY,
                "n_text": lm.N_TEXT, "dim": lm.DIM, "n_layers": lm.N_LAYERS, "n_heads": lm.N_HEADS, "ctx": lm.CTX}
    torch.manual_seed(seed)
    m = lm.SelfReportLM()
    opt = make_optimizer(m)
    train_tokens, held_out = lm.split_tokens(seed)
    gen_lm = torch.Generator().manual_seed(seed)              # text windows: the same for every lam
    gen_rep = torch.Generator().manual_seed(seed + 10_000)    # self-report questions
    start, log, seconds0 = 0, [], 0.0
    if ckpt_path.exists():
        ck = torch.load(ckpt_path)
        ck["settings"].setdefault("detach_input", False)       # checkpoints written before the option existed
        if ck["settings"] != settings:
            raise RuntimeError(f"{ckpt_path} has different settings: {ck['settings']}")
        m.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        gen_lm.set_state(ck["gen_lm"])
        gen_rep.set_state(ck["gen_rep"])
        start, log = ck["step"], ck["log"]
        seconds0 = log[-1]["seconds"] if log else 0.0
        print(f"resumed at step {start}", flush=True)
    train_data, valid_data = load_tokens("train"), load_tokens("valid")
    vgen = torch.Generator().manual_seed(1234)                 # same validation windows for every run
    valid_batches = [lm_batch(valid_data, LM_BATCH, vgen) for _ in range(EVAL_LM_BATCHES)]
    # random subsets for monitoring (held_out is sorted; its first ids are mostly rare byte tokens)
    eval_train = train_tokens[torch.randperm(len(train_tokens), generator=torch.Generator().manual_seed(99))]
    eval_held_out = held_out[torch.randperm(len(held_out), generator=torch.Generator().manual_seed(98))]

    t0 = time.time()
    for step in range(start, steps):
        for g in opt.param_groups:
            g["lr"] = lr_at(step, steps)
        x, y = lm_batch(train_data, LM_BATCH, gen_lm)
        loss_lm = lm_loss(m, x, y)
        loss = loss_lm
        if lam > 0:
            t = train_tokens[torch.randint(0, len(train_tokens), (REPORT_BATCH,), generator=gen_rep)]
            i = torch.randint(0, m.dim, (REPORT_BATCH,), generator=gen_rep)
            loss_rep = report_loss(m, t, i, detach_input)
            loss = loss + lam * loss_rep
        if not torch.isfinite(loss):
            raise FloatingPointError(f"loss not finite at step {step}")
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), CLIP)
        opt.step()
        if (step + 1) % EVAL_EVERY == 0 or step + 1 == steps:
            row = {"step": step + 1, "train_lm_loss": loss_lm.item(),
                   "train_report_loss": loss_rep.item() if lam > 0 else None,
                   **evaluate(m, valid_batches, eval_train, eval_held_out), "seconds": seconds0 + time.time() - t0}
            log.append(row)
            tmp = ckpt_path.with_suffix(".tmp")                # atomic: a kill mid-write keeps the old checkpoint
            torch.save({"model": m.state_dict(), "opt": opt.state_dict(), "gen_lm": gen_lm.get_state(),
                        "gen_rep": gen_rep.get_state(), "step": step + 1, "log": log, "settings": settings}, tmp)
            os.replace(tmp, ckpt_path)
            if verbose:
                print(f"step {step + 1:5d}  valid loss {row['valid_loss']:.4f}  R² train {row['r2_train']:.4f}  "
                      f"held-out {row['r2_held_out']:.4f}  E rms {row['E_rms_text']:.4f}  "
                      f"({row['seconds']:.0f} s)", flush=True)
    return m, settings, log


def main():
    name, lam, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    steps = int(sys.argv[4]) if len(sys.argv) > 4 else STEPS
    detach_input = len(sys.argv) > 5 and sys.argv[5] == "detach"
    torch.set_num_threads(2)
    m, settings, log = train(name, lam, seed, steps, detach_input=detach_input)
    torch.save({"model": m.state_dict(), "settings": settings}, RESULTS / f"{name}.pt")
    (RESULTS / f"{name}.json").write_text(json.dumps({"settings": settings, "log": log}, indent=1))
    print(f"wrote results/{name}.pt and .json")


if __name__ == "__main__":
    main()
