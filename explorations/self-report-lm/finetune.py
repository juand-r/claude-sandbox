"""Continue training a finished model under variants meant to raise follow (PLAN.md, stage 1).

Starts from the weights in results/<source>.pt with a new AdamW optimizer at a constant
learning rate, and trains next-token prediction plus the self-report task exactly as
train.py does in the control setting (the self-report gradient is stopped at the token
embedding vectors), with two possible changes:

- lam: the self-report loss coefficient λ;
- jitter_max: perturbed questions. Each question (t, i) uses x = E[t] + δ in place of E[t],
  with δ in a random direction and |δ| = s·|E[t]|, s drawn uniformly from [0, jitter_max];
  the target is x_i. With jitter_max = 0 this is the ordinary task. Perturbed questions ask
  the model to answer correctly near each embedding vector, not only at it, which is what
  follow measures.

Writes results/<name>.pt and results/<name>.json (settings and the quick measurements of
quick_measure.py at the start and every EVAL_EVERY steps).

Usage: python finetune.py <source> <name> <steps> <lam> <jitter_max> [lr]
"""
import json
import sys
import time
from pathlib import Path

import torch

import lm
import measure as Ms
import quick_measure as Q
import train as T

HERE = Path(__file__).parent
EVAL_EVERY = 1000
DATA_SEED_OFFSET = 777            # text windows and questions differ from the source run's


def jittered_report_loss(m, t, i, jitter_max, gen):
    """Self-report loss (1 − uncentred R² of the batch) on perturbed copies of E[t];
    the gradient is stopped at E[t] (control setting)."""
    x = m.E[t].detach()
    if jitter_max > 0:
        d = torch.randn(x.shape, generator=gen)
        s = torch.rand(len(t), 1, generator=gen) * jitter_max
        x = x + d / d.norm(dim=1, keepdim=True) * s * x.norm(dim=1, keepdim=True)
    target = x[torch.arange(len(t)), i]
    a = m.answer(x, i)
    return ((a - target) ** 2).mean() / target.var(unbiased=False)


def finetune(source, name, steps, lam, jitter_max, lr=T.LR_MIN, verbose=True):
    m, s = Ms.load(source)
    m.train()
    settings = {**s, "name": name, "source": source, "finetune_steps": steps, "lam": lam,
                "jitter_max": jitter_max, "finetune_lr": lr, "detach_input": True}
    opt = T.make_optimizer(m)
    for g in opt.param_groups:
        g["lr"] = lr
    train_tokens, held_out = lm.split_tokens(s["seed"], s["n_text"])
    gen_lm = torch.Generator().manual_seed(s["seed"] + DATA_SEED_OFFSET)
    gen_rep = torch.Generator().manual_seed(s["seed"] + DATA_SEED_OFFSET + 10_000)
    train_data = T.load_tokens("train")
    log = [{"step": 0, **Q.quick_measure(m, s["seed"])}]
    if verbose:
        print(f"step 0  {Q.fmt(log[-1])}", flush=True)
    t0 = time.time()
    for step in range(steps):
        x, y = T.lm_batch(train_data, T.LM_BATCH, gen_lm)
        t = train_tokens[torch.randint(0, len(train_tokens), (T.REPORT_BATCH,), generator=gen_rep)]
        i = torch.randint(0, m.dim, (T.REPORT_BATCH,), generator=gen_rep)
        loss = T.lm_loss(m, x, y) + lam * jittered_report_loss(m, t, i, jitter_max, gen_rep)
        if not torch.isfinite(loss):
            raise FloatingPointError(f"loss not finite at step {step}")
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(m.parameters(), T.CLIP)
        opt.step()
        if (step + 1) % EVAL_EVERY == 0 or step + 1 == steps:
            m.eval()
            log.append({"step": step + 1, **Q.quick_measure(m, s["seed"]), "seconds": time.time() - t0})
            m.train()
            if verbose:
                print(f"step {step + 1}  {Q.fmt(log[-1])}  ({time.time() - t0:.0f} s)", flush=True)
    return m.eval(), settings, log


def main():
    source, name, steps, lam, jitter_max = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
    lr = float(sys.argv[6]) if len(sys.argv) > 6 else T.LR_MIN
    torch.set_num_threads(2)
    m, settings, log = finetune(source, name, steps, lam, jitter_max, lr)
    torch.save({"model": m.state_dict(), "settings": settings}, HERE / "results" / f"{name}.pt")
    (HERE / "results" / f"{name}.json").write_text(json.dumps({"settings": settings, "log": log}, indent=1))
    print(f"wrote results/{name}.pt and .json")


if __name__ == "__main__":
    main()
