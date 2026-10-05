"""Train one SelfReporter to answer "coordinate i of your embedding of token t".

Conditions:
  fixed    the content-token embedding E stays at its random initial values
  trained  E is trained together with the rest of the model

In both, the target is the current value E[t, i], with no gradient through it:
the answer is pulled toward the weight, never the weight toward the answer.
The loss is the batch's squared error divided by the batch's target variance,
which equals 1 − R² of the batch.

Usage: python train.py <fixed|trained> <seed> [epochs]
Writes results/<condition>_seed<seed>.pt (weights and settings) and .json (log).
"""
import json
import math
import sys
import time
from pathlib import Path

import torch

import model as M

EPOCHS = 3000
BATCH = 64
LR = 1e-3
LOG_EVERY = 100
N_NEW = 256              # brand-new content vectors used for monitoring
RESULTS = Path(__file__).parent / "results"
CONDITIONS = ("fixed", "trained")


def loss_fn(answer, target):
    """Squared error / target variance = 1 − R² of the batch."""
    return ((answer - target) ** 2).mean() / target.var(unbiased=False)


@torch.no_grad()
def evaluate(m, train_tokens, held_out, new_vectors):
    t, i = M.all_pairs(train_tokens)
    th, ih = M.all_pairs(held_out)
    x = new_vectors.repeat_interleave(M.DIM, dim=0)
    inew = torch.arange(M.DIM).repeat(len(new_vectors))
    return {"r2_train": M.r2(m(t, i), m.E[t, i]),
            "r2_held_out": M.r2(m(th, ih), m.E[th, ih]),
            "r2_new": M.r2(m.answer(x, inew), x[torch.arange(len(x)), inew]),
            "E_rms_train": m.E[train_tokens].pow(2).mean().sqrt().item()}


def train(condition, seed, epochs=EPOCHS, log_every=LOG_EVERY, verbose=True):
    if condition not in CONDITIONS:
        raise ValueError(f"condition must be one of {CONDITIONS}, got {condition!r}")
    torch.manual_seed(seed)
    m = M.SelfReporter()
    m.E.requires_grad_(condition == "trained")
    train_tokens, held_out = M.split_tokens(seed)
    t_all, i_all = M.all_pairs(train_tokens)
    new_vectors = torch.randn(N_NEW, M.DIM, generator=torch.Generator().manual_seed(10_000 + seed))

    opt = torch.optim.Adam([p for p in m.parameters() if p.requires_grad], lr=LR)
    steps = epochs * math.ceil(len(t_all) / BATCH)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    gen = torch.Generator().manual_seed(seed)

    log = [{"epoch": 0, "loss": None, **evaluate(m, train_tokens, held_out, new_vectors)}]
    t0 = time.time()
    for epoch in range(1, epochs + 1):
        perm = torch.randperm(len(t_all), generator=gen)
        total = 0.0
        for s in range(0, len(perm), BATCH):
            idx = perm[s:s + BATCH]
            t, i = t_all[idx], i_all[idx]
            loss = loss_fn(m(t, i), m.E[t, i].detach())
            opt.zero_grad()
            loss.backward()
            opt.step()
            sched.step()
            total += loss.item() * len(idx)
        if not math.isfinite(total):
            raise FloatingPointError(f"loss not finite at epoch {epoch}")
        if epoch % log_every == 0 or epoch == epochs:
            row = {"epoch": epoch, "loss": total / len(perm), **evaluate(m, train_tokens, held_out, new_vectors)}
            log.append(row)
            if verbose:
                print(f"epoch {epoch:5d}  loss {row['loss']:.5f}  R² train {row['r2_train']:.5f}  "
                      f"held-out {row['r2_held_out']:.5f}  new {row['r2_new']:.5f}  "
                      f"E rms {row['E_rms_train']:.3f}  ({time.time() - t0:.0f} s)", flush=True)
    settings = {"condition": condition, "seed": seed, "epochs": epochs, "batch": BATCH, "lr": LR,
                "n_tokens": M.N_TOKENS, "dim": M.DIM, "n_layers": M.N_LAYERS, "n_heads": M.N_HEADS,
                "mlp_width": M.MLP_WIDTH, "n_held_out": M.N_HELD_OUT}
    return m, settings, log


def load(path):
    """A trained SelfReporter and its settings."""
    d = torch.load(path)
    s = d["settings"]
    m = M.SelfReporter(s["n_tokens"], s["dim"], s["n_layers"], s["n_heads"], s["mlp_width"])
    m.load_state_dict(d["state_dict"])
    return m, s


def main():
    condition, seed = sys.argv[1], int(sys.argv[2])
    epochs = int(sys.argv[3]) if len(sys.argv) > 3 else EPOCHS
    torch.set_num_threads(1)
    m, settings, log = train(condition, seed, epochs)
    RESULTS.mkdir(exist_ok=True)
    name = f"{condition}_seed{seed}" + ("" if epochs == EPOCHS else f"_{epochs}ep")
    torch.save({"state_dict": m.state_dict(), "settings": settings}, RESULTS / f"{name}.pt")
    (RESULTS / f"{name}.json").write_text(json.dumps({"settings": settings, "log": log}, indent=1))
    print(f"wrote results/{name}.pt and .json")


if __name__ == "__main__":
    main()
