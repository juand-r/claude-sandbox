"""Train one SelfReporter to answer "coordinate i of your embedding of token t".

Conditions:
  fixed    the content-token embedding E stays at its random initial values
  trained  E is trained together with the rest of the model

In both, the target is the current value E[t, i], with no gradient through it.
In the trained condition E still gets a gradient through its other role, as the
input at position 0: E[t] is moved so that the answers a(E[t]) come closer to
the current E[t]. Nothing anchors the scale of E, so its RMS is logged.
The loss is the batch's squared error divided by the batch's target variance,
which equals 1 − R² of the batch. (With the target detached, the division does
not guard against shrinking E; it only rescales each batch.)

Vocabulary size V (number of content tokens) is a setting; a quarter of the
tokens are held out. Runs with different V get the same number of optimizer
steps (TOTAL_STEPS, the 72,000 steps of the original V = 64 runs), so a larger
vocabulary means fewer epochs.

Usage: python train.py <fixed|trained> <seed> [n_tokens] [epochs]
Writes results/<condition>_seed<seed>.pt for V = 64 (the original runs) and
results/<condition>_V<V>_seed<seed>.pt otherwise, plus a .json log; a run with
a non-default number of epochs gets the suffix _<epochs>ep.
"""
import json
import math
import sys
import time
from pathlib import Path

import torch

import model as M

EPOCHS = 3000            # for V = 64
BATCH = 64
TOTAL_STEPS = 72_000     # = EPOCHS · 24 batches, the step budget of the V = 64 runs
N_LOGS = 30              # about this many evaluations per run
LR = 1e-3
N_NEW = 256              # brand-new content vectors used for monitoring
RESULTS = Path(__file__).parent / "results"
CONDITIONS = ("fixed", "trained")


def loss_fn(answer, target):
    """Squared error / target variance = 1 − R² of the batch."""
    return ((answer - target) ** 2).mean() / target.var(unbiased=False)


def batch_loss(m, t, i):
    """The training loss for questions (t, i); no gradient through the target."""
    return loss_fn(m(t, i), m.E[t, i].detach())


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


def epochs_for(n_tokens):
    """Epochs giving about TOTAL_STEPS optimizer steps for a vocabulary of n_tokens."""
    n_train = n_tokens - n_tokens // 4
    return max(1, round(TOTAL_STEPS / math.ceil(n_train * M.DIM / BATCH)))


def train(condition, seed, epochs=None, log_every=None, verbose=True, n_tokens=M.N_TOKENS):
    if condition not in CONDITIONS:
        raise ValueError(f"condition must be one of {CONDITIONS}, got {condition!r}")
    if n_tokens % 4:
        raise ValueError(f"n_tokens must be divisible by 4, got {n_tokens}")
    epochs = epochs_for(n_tokens) if epochs is None else epochs
    log_every = max(1, epochs // N_LOGS) if log_every is None else log_every
    n_held_out = n_tokens // 4
    torch.manual_seed(seed)
    m = M.SelfReporter(n_tokens=n_tokens)
    m.E.requires_grad_(condition == "trained")
    train_tokens, held_out = M.split_tokens(seed, n_tokens, n_held_out)
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
            loss = batch_loss(m, t, i)
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
    settings = {"condition": condition, "seed": seed, "epochs": epochs, "steps": steps, "batch": BATCH,
                "lr": LR, "n_tokens": n_tokens, "dim": M.DIM, "n_layers": M.N_LAYERS, "n_heads": M.N_HEADS,
                "mlp_width": M.MLP_WIDTH, "n_held_out": n_held_out}
    return m, settings, log


def load(path):
    """A trained SelfReporter and its settings."""
    d = torch.load(path)
    s = d["settings"]
    m = M.SelfReporter(s["n_tokens"], s["dim"], s["n_layers"], s["n_heads"], s["mlp_width"])
    m.load_state_dict(d["state_dict"])
    return m, s


def run_name(condition, seed, n_tokens, epochs):
    vocab = "" if n_tokens == M.N_TOKENS else f"_V{n_tokens}"
    suffix = "" if epochs == epochs_for(n_tokens) else f"_{epochs}ep"
    return f"{condition}{vocab}_seed{seed}{suffix}"


def main():
    condition, seed = sys.argv[1], int(sys.argv[2])
    n_tokens = int(sys.argv[3]) if len(sys.argv) > 3 else M.N_TOKENS
    epochs = int(sys.argv[4]) if len(sys.argv) > 4 else epochs_for(n_tokens)
    torch.set_num_threads(1)
    m, settings, log = train(condition, seed, epochs, n_tokens=n_tokens)
    RESULTS.mkdir(exist_ok=True)
    name = run_name(condition, seed, n_tokens, epochs)
    torch.save({"state_dict": m.state_dict(), "settings": settings}, RESULTS / f"{name}.pt")
    (RESULTS / f"{name}.json").write_text(json.dumps({"settings": settings, "log": log}, indent=1))
    print(f"wrote results/{name}.pt and .json")


if __name__ == "__main__":
    main()
