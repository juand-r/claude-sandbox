"""Stage 2 (PLAN.md): joint training with the answer written as text (textanswer.py).

Same as train.py (same model, data, optimizer, schedule, step count), except that the
self-report loss is the cross-entropy of the five answer tokens, in the control setting
(the self-report task cannot change the token embedding vectors; textanswer.py). The 13
answer characters are not asked about. Checkpoints and resume as in train.py.

With jitter_max > 0: perturbed questions (textanswer.text_report_loss).

Usage: python train_text.py <name> <lam> <seed> [steps] [jitter_max]
"""
import json
import os
import sys
import time

import numpy as np
import torch

import lm
import textanswer as TA
import train as T

EVAL_TOKENS = 64          # monitoring: centred R² on 64 asked-about and 64 never-asked tokens


@torch.no_grad()
def evaluate(m, fmt, valid_batches, eval_asked, eval_never):
    out = {"valid_loss": float(np.mean([T.lm_loss(m, x, y).item() for x, y in valid_batches]))}
    for name, toks in (("asked", eval_asked), ("never", eval_never)):
        t = toks.repeat_interleave(m.dim)
        i = torch.arange(m.dim).repeat(len(toks))
        a = TA.text_answers(m, m.E[t], i, fmt).view(len(toks), m.dim)
        y = m.E[toks]
        out[f"r2c_{name}"] = 1 - (a - y).pow(2).sum().item() / (y - y.mean(0)).pow(2).sum().item()
    out["E_rms_text"] = m.E[:m.n_text].pow(2).mean().sqrt().item()
    return out


def train(name, lam, seed, steps=T.STEPS, verbose=True, jitter_max=0.0):
    T.RESULTS.mkdir(exist_ok=True)
    ckpt_path = T.RESULTS / f"{name}_ckpt.pt"
    settings = {"name": name, "answer": "text", "lam": lam, "seed": seed, "steps": steps, "detach_input": True, "jitter_max": jitter_max,
                "lm_batch": T.LM_BATCH, "report_batch": T.REPORT_BATCH, "lr": T.LR, "lr_min": T.LR_MIN,
                "warmup": T.WARMUP, "weight_decay": T.WEIGHT_DECAY, "betas": list(T.BETAS), "clip": T.CLIP,
                "eval_every": T.EVAL_EVERY, "n_text": lm.N_TEXT, "dim": lm.DIM, "n_layers": lm.N_LAYERS,
                "n_heads": lm.N_HEADS, "ctx": lm.CTX}
    fmt = TA.Format(T.DATA / "tokenizer.json")
    torch.manual_seed(seed)
    m = lm.SelfReportLM()
    opt = T.make_optimizer(m)
    asked, never = lm.split_tokens(seed)
    asked, never = TA.question_tokens(asked, fmt), TA.question_tokens(never, fmt)
    gen_lm = torch.Generator().manual_seed(seed)
    gen_rep = torch.Generator().manual_seed(seed + 10_000)
    start, log, seconds0 = 0, [], 0.0
    if ckpt_path.exists():
        ck = torch.load(ckpt_path)
        ck["settings"].setdefault("jitter_max", 0.0)     # checkpoints written before this option existed
        if ck["settings"] != settings:
            raise RuntimeError(f"{ckpt_path} has different settings: {ck['settings']}")
        m.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        gen_lm.set_state(ck["gen_lm"])
        gen_rep.set_state(ck["gen_rep"])
        start, log = ck["step"], ck["log"]
        seconds0 = log[-1]["seconds"] if log else 0.0
        print(f"resumed at step {start}", flush=True)
    train_data, valid_data = T.load_tokens("train"), T.load_tokens("valid")
    vgen = torch.Generator().manual_seed(1234)
    valid_batches = [T.lm_batch(valid_data, T.LM_BATCH, vgen) for _ in range(T.EVAL_LM_BATCHES)]
    eval_asked = asked[torch.randperm(len(asked), generator=torch.Generator().manual_seed(99))[:EVAL_TOKENS]]
    eval_never = never[torch.randperm(len(never), generator=torch.Generator().manual_seed(98))[:EVAL_TOKENS]]

    t0 = time.time()
    for step in range(start, steps):
        for g in opt.param_groups:
            g["lr"] = T.lr_at(step, steps)
        x, y = T.lm_batch(train_data, T.LM_BATCH, gen_lm)
        loss_lm = T.lm_loss(m, x, y)
        loss, loss_rep = loss_lm, torch.tensor(float("nan"))
        if lam > 0:
            t = asked[torch.randint(0, len(asked), (T.REPORT_BATCH,), generator=gen_rep)]
            i = torch.randint(0, m.dim, (T.REPORT_BATCH,), generator=gen_rep)
            loss_rep = TA.text_report_loss(m, t, i, fmt, jitter_max=jitter_max, gen=gen_rep)
            loss = loss_lm + lam * loss_rep
        if not torch.isfinite(loss):
            raise FloatingPointError(f"loss not finite at step {step}")
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), T.CLIP)
        opt.step()
        if (step + 1) % T.EVAL_EVERY == 0 or step + 1 == steps:
            m.eval()
            row = {"step": step + 1, "train_lm_loss": loss_lm.item(), "train_report_loss": loss_rep.item(),
                   **evaluate(m, fmt, valid_batches, eval_asked, eval_never), "seconds": seconds0 + time.time() - t0}
            m.train()
            log.append(row)
            tmp = ckpt_path.with_suffix(".tmp")
            torch.save({"model": m.state_dict(), "opt": opt.state_dict(), "gen_lm": gen_lm.get_state(),
                        "gen_rep": gen_rep.get_state(), "step": step + 1, "log": log, "settings": settings}, tmp)
            os.replace(tmp, ckpt_path)
            if verbose:
                print(f"step {step + 1:5d}  valid loss {row['valid_loss']:.4f}  answer loss {row['train_report_loss']:.3f}  "
                      f"R²c asked {row['r2c_asked']:.4f}  never {row['r2c_never']:.4f}  ({row['seconds']:.0f} s)", flush=True)
    return m.eval(), settings, log


def main():
    name, lam, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    steps = int(sys.argv[4]) if len(sys.argv) > 4 else T.STEPS
    jitter_max = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    torch.set_num_threads(2)
    m, settings, log = train(name, lam, seed, steps, jitter_max=jitter_max)
    torch.save({"model": m.state_dict(), "settings": settings}, T.RESULTS / f"{name}.pt")
    (T.RESULTS / f"{name}.json").write_text(json.dumps({"settings": settings, "log": log}, indent=1))
    print(f"wrote results/{name}.pt and .json")


if __name__ == "__main__":
    main()
