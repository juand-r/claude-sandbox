"""Experiments of the paper (E1-E8 in PLAN.md). Each writes results/<name>.json.

Usage:  python experiments.py <experiment> [--seed S] [options]
"""

import argparse
import json
import time
from pathlib import Path

import torch

import quine as q

RESULTS = Path(__file__).parent / "results"
OPTIMIZERS = ("sgd", "sgd_momentum", "adam", "adagrad", "adamax", "rmsprop")


def save(name, config, log, model=None):
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / f"{name}.json").write_text(json.dumps({"config": config, "log": log}, indent=1))
    if model is not None:
        torch.save(model.state_dict(), RESULTS / f"{name}.pt")
    print(f"wrote results/{name}.json")


def record(log, epoch, model, images=None, **extra):
    row = {"epoch": epoch, **q.replication_stats(model, images), **extra}
    log.append(row)
    print(f"  epoch {epoch:5d}  L_SR {row['L_SR']:10.4f}  theta_rms {row['theta_rms']:.4f}"
          f"  pred_rms {row['pred_rms']:.4f}  rel_err {row['rel_error']:.4f}"
          + "".join(f"  {k} {v:.4g}" if isinstance(v, float) else f"  {k} {v}" for k, v in extra.items()), flush=True)


def load_model(path, **kw):
    m = q.Quine(**kw)
    m.load_state_dict(torch.load(path))
    return m


def model_kwargs(a):
    kw = {"seed": a.seed, "out_selu": a.out_selu, "embed_selu": not a.no_embed_selu, "n_layers": a.n_layers}
    if a.init_literal_he:      # the paper's text, taken literally (PLAN.md item 5)
        kw.update(init="he_normal", proj_std=1.0)
    if a.init is not None:     # set weight init and P scale separately (IDEAS.md idea 1)
        kw["init"] = a.init
    if a.proj_std is not None:
        kw["proj_std"] = a.proj_std
    return kw


def tag(a):
    return (f"seed{a.seed}" + ("_outselu" if a.out_selu else "") + ("_noembedselu" if a.no_embed_selu else "")
            + ("_he" if a.init_literal_he else "")
            + (f"_init-{a.init}" if a.init is not None else "")
            + (f"_proj{a.proj_std:g}" if a.proj_std is not None else "")
            + (f"_L{a.n_layers}" if a.n_layers != 2 else ""))


# -- E1/E2: gradient-based optimizers ---------------------------------------
def optimizer_run(a):
    m = load_model(a.start, **model_kwargs(a)) if a.start else q.Quine(**model_kwargs(a))
    opt = q.make_optimizer(a.optimizer, m.parameters(), lr=a.lr)
    gen = torch.Generator().manual_seed(a.seed)
    log = []
    record(log, 0, m)
    for t in range(1, a.epochs + 1):
        q.grad_epoch(m, opt, gen)
        record(log, t, m)
    lr = f"_lr{a.lr:g}" if a.lr is not None else ""
    start = f"_from-{Path(a.start).stem}" if a.start else ""
    save(f"opt_{a.optimizer}_{a.epochs}ep_{tag(a)}{lr}{start}", vars(a), log, m)


# -- E3/E4: hill-climbing -----------------------------------------------------
def hill_climb_run(a):
    m = load_model(a.start, **model_kwargs(a)) if a.start else q.Quine(**model_kwargs(a))
    gen = torch.Generator().manual_seed(a.seed + 1000)
    log = []
    record(log, 0, m)
    t0 = time.time()
    for t in range(1, a.epochs + 1):
        acc = q.hill_climb_epoch(m, a.sigma, gen)
        if t % a.log_every == 0 or t == a.epochs:
            record(log, t, m, accept=acc, minutes=(time.time() - t0) / 60)
    start = Path(a.start).stem if a.start else "init"
    save(f"hill_sigma{a.sigma:g}_{a.epochs}ep_from-{start}_{tag(a)}", vars(a), log, m)


# -- E5/E6: regeneration --------------------------------------------------------
def regeneration_run(a):
    m = q.Quine(**model_kwargs(a))
    opt = q.make_optimizer("adamax", m.parameters())
    gen = torch.Generator().manual_seed(a.seed)
    log = []
    record(log, 0, m, phase="init")
    for g in range(1, a.generations + 1):
        for _ in range(a.T):
            q.grad_epoch(m, opt, gen)
        if a.T:
            record(log, g, m, phase="after_opt")
        q.regenerate(m)
        if not torch.isfinite(m.theta).all():
            print(f"  generation {g}: weights are no longer finite; stopping", flush=True)
            log.append({"epoch": g, "phase": "diverged"})
            break
        record(log, g, m, phase="after_regen")
    save(f"regen_T{a.T}_G{a.generations}_{tag(a)}", vars(a), log, m)


# -- E7/E8: auxiliary quine -----------------------------------------------------
def aux_run(a):
    tx, ty, vx, vy = q.load_mnist()
    m = q.Quine(aux=True, **model_kwargs(a))
    opt = q.make_optimizer("adamax", m.parameters())
    gen = torch.Generator().manual_seed(a.seed)
    sr_images = q.test_pairing_images(m, vx)
    log = []

    def rec(t):
        task, acc = q.classification_eval(m, vx, vy)
        row_extra = {"lam_L_task": q.LAMBDA * task, "accuracy": acc}
        record(log, t, m, sr_images, **row_extra)
        log[-1]["L_aux"] = log[-1]["L_SR"] + log[-1]["lam_L_task"]

    rec(0)
    for t in range(1, a.epochs + 1):
        q.grad_epoch(m, opt, gen, tx, ty, task_only=a.task_only)
        rec(t)
    save(f"aux_{'taskonly' if a.task_only else 'quine'}_{a.epochs}ep_{tag(a)}", vars(a), log, m)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("experiment", choices=["optimizer", "hill", "regen", "aux"])
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--epochs", type=int, default=30)
    p.add_argument("--optimizer", choices=OPTIMIZERS, default="adamax")
    p.add_argument("--sigma", type=float, default=1e-3, help="hill-climbing noise std")
    p.add_argument("--start", default=None, help="hill-climbing or optimizer: .pt file to start from")
    p.add_argument("--lr", type=float, default=None, help="optimizer learning rate (default: torch default)")
    p.add_argument("--log-every", type=int, default=1)
    p.add_argument("--generations", type=int, default=10)
    p.add_argument("--T", type=int, default=1, help="optimization epochs per generation")
    p.add_argument("--task-only", action="store_true", help="aux: drop L_SR (baseline E8)")
    p.add_argument("--out-selu", action="store_true", help="SELU on the weight output")
    p.add_argument("--init", choices=q.INIT_SCHEMES, default=None, help="weight initialization")
    p.add_argument("--n-layers", type=int, default=2, choices=(1, 2), help="trainable hidden 100x100 layers")
    p.add_argument("--proj-std", type=float, default=None, help="std of the entries of P")
    p.add_argument("--no-embed-selu", action="store_true",
                   help="no SELU on the looked-up projection row (treat P as a plain embedding table)")
    p.add_argument("--init-literal-he", action="store_true",
                   help="He-normal weights and N(0,1) projection, instead of the defaults matched to the paper")
    a = p.parse_args()
    torch.set_num_threads(1)
    torch.manual_seed(a.seed)
    {"optimizer": optimizer_run, "hill": hill_climb_run,
     "regen": regeneration_run, "aux": aux_run}[a.experiment](a)


if __name__ == "__main__":
    main()
