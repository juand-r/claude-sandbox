"""Continue training a text-answer model (stage 2) with perturbed questions (stage 1's method).

Starts from results/<source>.pt (a train_text.py run) with a new AdamW optimizer at a constant
learning rate, and trains next-token prediction plus the text self-report loss
(textanswer.text_report_loss, control setting) with perturbed questions: the vector at
position 2 is x = E[t] + δ, |δ| = s·|E[t]|, s uniform in [0, jitter_max], and the target is
x_i written as text.

Every EVAL_EVERY steps: validation loss (train.py's 20 × 32 windows), centred R² on
train_text.py's 64 + 64 monitoring tokens, and finite-change follow at measure_text.FINITE_SIZE
on N_FOLLOW asked-about and N_FOLLOW never-asked tokens (the same tokens and directions each time).

Writes results/<name>.pt and results/<name>.json.

Usage: python finetune_text.py <source> <name> <steps> <lam> <jitter_max> [lr]
"""
import json
import sys
import time

import numpy as np
import torch

import lm
import finetune as Fn
import measure as Ms
import measure_text as MT
import textanswer as TA
import train as T
import train_text as TT

EVAL_EVERY = 1000
N_FOLLOW = 64


@torch.no_grad()
def evaluate(m, fmt, valid_batches, eval_asked, eval_never, follow_asked, follow_never):
    out = TT.evaluate(m, fmt, valid_batches, eval_asked, eval_never)
    for k, (name, toks) in enumerate((("asked", follow_asked), ("never", follow_never))):
        out[f"follow_mean_{name}"], out[f"follow_median_{name}"] = \
            MT.finite_follow_text(m, fmt, toks, torch.Generator().manual_seed(1000 + k))
    return out


def fmt_row(r):
    return (f"valid {r['valid_loss']:.3f}  R²c {r['r2c_asked']:.3f}/{r['r2c_never']:.3f}  "
            f"follow (30%) mean {r['follow_mean_asked']:.3f}/{r['follow_mean_never']:.3f}  "
            f"median {r['follow_median_asked']:.3f}/{r['follow_median_never']:.3f}")


def finetune(source, name, steps, lam, jitter_max, lr=T.LR_MIN):
    fmt = TA.Format(T.DATA / "tokenizer.json")
    m, s = Ms.load(source)
    if s.get("answer") != "text":
        raise ValueError(f"{source} is not a text-answer run")
    offset, gen_lm, gen_rep = Fn.generators(s)
    settings = {**s, "data_offset": offset, "name": name, "source": source, "finetune_steps": steps, "lam": lam,
                "jitter_max": jitter_max, "finetune_lr": lr}
    opt = T.make_optimizer(m)
    for g in opt.param_groups:
        g["lr"] = lr
    asked, never = lm.split_tokens(s["seed"], s["n_text"])
    asked, never = TA.question_tokens(asked, fmt), TA.question_tokens(never, fmt)
    train_data, valid_data = T.load_tokens("train"), T.load_tokens("valid")
    vgen = torch.Generator().manual_seed(1234)
    valid_batches = [T.lm_batch(valid_data, T.LM_BATCH, vgen) for _ in range(T.EVAL_LM_BATCHES)]
    eval_asked = asked[torch.randperm(len(asked), generator=torch.Generator().manual_seed(99))[:TT.EVAL_TOKENS]]
    eval_never = never[torch.randperm(len(never), generator=torch.Generator().manual_seed(98))[:TT.EVAL_TOKENS]]
    fgen = torch.Generator().manual_seed(4242)
    follow_asked = asked[torch.randperm(len(asked), generator=fgen)[:N_FOLLOW]]
    follow_never = never[torch.randperm(len(never), generator=fgen)[:N_FOLLOW]]
    ev = lambda: evaluate(m.eval(), fmt, valid_batches, eval_asked, eval_never, follow_asked, follow_never)

    log = [{"step": 0, **ev()}]
    print(f"step 0  {fmt_row(log[-1])}", flush=True)
    m.train()
    t0 = time.time()
    for step in range(steps):
        x, y = T.lm_batch(train_data, T.LM_BATCH, gen_lm)
        t = asked[torch.randint(0, len(asked), (T.REPORT_BATCH,), generator=gen_rep)]
        i = torch.randint(0, m.dim, (T.REPORT_BATCH,), generator=gen_rep)
        loss = T.lm_loss(m, x, y) + lam * TA.text_report_loss(m, t, i, fmt, jitter_max=jitter_max, gen=gen_rep)
        if not torch.isfinite(loss):
            raise FloatingPointError(f"loss not finite at step {step}")
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), T.CLIP)
        opt.step()
        if (step + 1) % EVAL_EVERY == 0 or step + 1 == steps:
            log.append({"step": step + 1, **ev(), "seconds": time.time() - t0})
            m.train()
            print(f"step {step + 1}  {fmt_row(log[-1])}  ({time.time() - t0:.0f} s)", flush=True)
    return m.eval(), settings, log


def main():
    source, name, steps, lam, jitter_max = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    lr = float(sys.argv[6]) if len(sys.argv) > 6 else T.LR_MIN
    torch.set_num_threads(2)
    m, settings, log = finetune(source, name, steps, lam, jitter_max, lr)
    torch.save({"model": m.state_dict(), "settings": settings}, T.RESULTS / f"{name}.pt")
    (T.RESULTS / f"{name}.json").write_text(json.dumps({"settings": settings, "log": log}, indent=1))
    print(f"wrote results/{name}.pt and .json")


if __name__ == "__main__":
    main()
