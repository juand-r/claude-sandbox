"""Measurements on a model that answers questions about its own embedding.

1. R²: answers against the current embedding values, for training tokens and
   held-out tokens (never asked about in training).
2. Follow test. For each token t: change the embedding row E[t] to E[t] + δ (δ
   random, |δ| = size · |E[t]|), ask all DIM questions about t again, and
   restore the row.
       follow ratio  = ⟨Δanswers, δ⟩ / |δ|²       1: answers moved with the change
                                                  0: answers ignored it
       other movement = |Δanswers − ratio · δ| / |δ|   movement not along δ
   Also R² of the answers after the change against the changed values.
3. Brand-new tokens: content vectors that were never rows of E, drawn from
   N(0, 1) and from a normal distribution matched (per coordinate) to the
   current training rows. R² of the answers against those vectors.

The canaries (canaries.py) have known results and go through the same code;
`check_canaries` fails loudly if the code does not reproduce them.

Usage: python follow_test.py            (all results/*.pt, canaries, untrained baselines)
Writes results/follow_test.json.
"""
import json
from pathlib import Path

import torch

import canaries as C
import model as M
import train as T

SIZES = (0.1, 1.0)       # |δ| / |E[t]|
N_DRAWS = 4              # random δ per token and size
N_NEW = 1024             # brand-new content vectors
RESULTS = Path(__file__).parent / "results"


def all_questions(t, dim):
    return torch.full((dim,), t, dtype=torch.long), torch.arange(dim)


@torch.no_grad()
def follow(model, tokens, size, gen):
    dim = model.E.shape[1]
    ratios, others, after_all, target_all = [], [], [], []
    for t in tokens.tolist():
        tt, ii = all_questions(t, dim)
        original = model.E[t].clone()
        before = model(tt, ii)
        for _ in range(N_DRAWS):
            delta = torch.randn(dim, generator=gen)
            delta *= size * original.norm() / delta.norm()
            model.E[t] = original + delta
            after = model(tt, ii)
            model.E[t] = original
            change = after - before
            r = (change @ delta / (delta @ delta)).item()
            ratios.append(r)
            others.append(((change - r * delta).norm() / delta.norm()).item())
            after_all.append(after)
            target_all.append(original + delta)
    ratios = torch.tensor(ratios)
    return {"follow_ratio_mean": ratios.mean().item(), "follow_ratio_sd": ratios.std().item(),
            "other_movement_mean": sum(others) / len(others),
            "r2_after_change": M.r2(torch.cat(after_all), torch.cat(target_all))}


@torch.no_grad()
def r2_new(model, x):
    dim = x.shape[1]
    xs = x.repeat_interleave(dim, dim=0)
    i = torch.arange(dim).repeat(len(x))
    return M.r2(model.answer(xs, i), xs[torch.arange(len(xs)), i])


@torch.no_grad()
def measure(model, train_tokens, held_out, seed=0):
    """All measurements for one model. Leaves model.E exactly as it found it."""
    E_before = model.E.detach().clone()
    gen = torch.Generator().manual_seed(seed)
    out = {}
    for name, toks in (("train", train_tokens), ("held_out", held_out)):
        t, i = M.all_pairs(toks, model.E.shape[1])
        out[f"r2_{name}"] = M.r2(model(t, i), model.E[t, i])
        for size in SIZES:
            for k, v in follow(model, toks, size, gen).items():
                out[f"{name}_{size:g}_{k}"] = v
    dim = model.E.shape[1]
    out["r2_new_standard"] = r2_new(model, torch.randn(N_NEW, dim, generator=gen))
    rows = model.E[train_tokens]
    out["r2_new_matched"] = r2_new(model, rows.mean(0) + rows.std(0) * torch.randn(N_NEW, dim, generator=gen))
    out["E_rms_train"] = rows.pow(2).mean().sqrt().item()
    if not torch.equal(model.E, E_before):
        raise RuntimeError("measure() changed the embedding table")
    return out


def check_canaries(seed=0):
    """Run both canaries through measure(); raise if a known result is not reproduced."""
    torch.manual_seed(seed)
    E = torch.randn(M.N_TOKENS, M.DIM)
    train_tokens, held_out = M.split_tokens(seed)
    reader = measure(C.perfect_reader(E), train_tokens, held_out, seed)
    memo = measure(C.Memorizer(E, train_tokens), train_tokens, held_out, seed)
    tol = 1e-4
    checks = [("reader R² train = 1", abs(reader["r2_train"] - 1) < tol),
              ("reader R² held-out = 1", abs(reader["r2_held_out"] - 1) < tol),
              ("reader R² new = 1", abs(reader["r2_new_standard"] - 1) < tol and abs(reader["r2_new_matched"] - 1) < tol)]
    for name in ("train", "held_out"):
        for size in SIZES:
            p = f"{name}_{size:g}_"
            checks += [(f"reader follow ratio = 1 ({p})", abs(reader[p + "follow_ratio_mean"] - 1) < tol),
                       (f"reader other movement = 0 ({p})", reader[p + "other_movement_mean"] < tol),
                       (f"reader R² after change = 1 ({p})", abs(reader[p + "r2_after_change"] - 1) < tol)]
    checks += [("memorizer R² train = 1", memo["r2_train"] == 1.0),
               ("memorizer R² held-out < 0.5", memo["r2_held_out"] < 0.5),
               ("memorizer R² new < 0.5", memo["r2_new_standard"] < 0.5),
               ("memorizer follow ratio = 0 for 10% changes (train)", abs(memo["train_0.1_follow_ratio_mean"]) < 1e-6)]
    failed = [name for name, ok in checks if not ok]
    if failed:
        raise AssertionError(f"canary checks failed: {failed}\nreader: {reader}\nmemorizer: {memo}")
    return {"perfect_reader": reader, "memorizer": memo}


def main():
    torch.set_num_threads(4)
    out = {"canaries": check_canaries()}
    print("canaries: all known results reproduced")
    for path in sorted(RESULTS.glob("*.pt")):
        m, s = T.load(path)
        train_tokens, held_out = M.split_tokens(s["seed"])
        out[path.stem] = {"settings": s, **measure(m, train_tokens, held_out, s["seed"])}
        torch.manual_seed(s["seed"])
        base = M.SelfReporter()                    # same initialization as the run, untrained
        out[f"untrained_seed{s['seed']}"] = measure(base, train_tokens, held_out, s["seed"])
        print(path.stem, {k: round(v, 4) for k, v in out[path.stem].items() if isinstance(v, float)}, flush=True)
    (RESULTS / "follow_test.json").write_text(json.dumps(out, indent=1))
    print("wrote results/follow_test.json")


if __name__ == "__main__":
    main()
