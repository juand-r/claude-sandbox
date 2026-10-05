"""Measurements on a model that answers questions about its own embedding.

Notation: for a content token t, a(x) is the vector of the model's DIM answers
("coordinate 0 of t", ..., "coordinate DIM−1 of t") when the embedding row of t
is x. A perfect reader has a(x) = x.

1. R²: answers against the current embedding values, for training tokens and
   held-out tokens (never asked about in training). Also a centred R², with
   each coordinate's mean over the token set removed from both answers and
   values, so that a model answering only the average of coordinate i gets 0.
2. Local follow test (exact, no random changes). J = ∂a/∂x at x = E[t], a
   DIM × DIM matrix, from autograd. A perfect reader has J = I.
       local follow  = trace(J) / DIM     (expected follow ratio of a small random change)
       local other   = |J − local follow · I|_F / √DIM   (expected other movement of a small change)
3. Follow test with finite changes. For each token t: set E[t] ← E[t] + δ (δ
   random, |δ| = size · |E[t]|), ask the DIM questions again, restore the row.
       follow ratio   = ⟨Δa, δ⟩ / |δ|²            1: answers moved with the change; 0: ignored it
       other movement = |Δa − ratio · δ| / |δ|     movement not along δ
       R² of the change = 1 − Σ|Δa − δ|² / Σ|δ − mean δ|²   (pooled over draws)
       jumps = fraction of draws with |Δa| > 3 |δ|
   The mean follow ratio can be dominated by rare jumps (review finding: a
   nearest-row memorizer scores 0.35-0.6 on held-out tokens at 10% changes
   while its median is 0), so the median and the jump fraction are reported too.
   Changes of 100% mislead even more: the memorizer's held-out median is then
   about 0.26, because a large change lands near another stored row that lies
   along δ. The local measure (item 2) is the one to trust.
4. Brand-new tokens: content vectors that were never rows of E, drawn from
   N(0, 1) and from a normal distribution matched (per coordinate) to the
   current training rows. R² of the answers against those vectors.

Note: E enters the computation only as the input vector at position 0, so items
2-4 all measure how the learned map x -> a(x) behaves away from the training
rows. In the fixed condition held-out rows and N(0, 1) vectors have the same
distribution; in the trained condition the training rows drift during training
while held-out rows stay at their initial values.

The canaries (canaries.py) have known results and go through the same code;
`check_canaries` fails loudly if the code does not reproduce them.

Usage: python follow_test.py   (runs results/<condition>_seed<k>.pt, canaries, untrained baselines)
Writes results/follow_test.json.
"""
import json
import re
from pathlib import Path

import torch

import canaries as C
import model as M
import train as T

SIZES = (0.01, 0.1, 1.0)   # |δ| / |E[t]|
N_DRAWS = 4                # random δ per token and size
N_NEW = 1024               # brand-new content vectors
JUMP = 3.0                 # a draw is a jump if |Δa| > JUMP · |δ|
RESULTS = Path(__file__).parent / "results"
RUN_NAME = re.compile(r"^(fixed|trained)_seed\d+$")    # main runs only; trial runs carry an "_<n>ep" suffix


def all_questions(t, dim):
    return torch.full((dim,), t, dtype=torch.long), torch.arange(dim)


def answers_for(model, x):
    """a(x): the DIM answers about a content token whose embedding row is x."""
    dim = x.shape[0]
    return model.answer(x.unsqueeze(0).expand(dim, dim), torch.arange(dim))


def local_follow(model, tokens):
    dim = model.E.shape[1]
    follows, others = [], []
    with torch.enable_grad():
        for t in tokens.tolist():
            x = model.E[t].detach().clone()
            J = torch.autograd.functional.jacobian(lambda v: answers_for(model, v), x)
            f = J.trace().item() / dim
            follows.append(f)
            others.append(((J - f * torch.eye(dim)).norm() / dim ** 0.5).item())
    follows = torch.tensor(follows)
    return {"local_follow_mean": follows.mean().item(), "local_follow_sd": follows.std().item(),
            "local_other_mean": sum(others) / len(others)}


@torch.no_grad()
def follow(model, tokens, size, gen):
    dim = model.E.shape[1]
    ratios, others, changes, deltas, jumps = [], [], [], [], 0
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
            jumps += int(change.norm() > JUMP * delta.norm())
            changes.append(change)
            deltas.append(delta)
    ratios = torch.tensor(ratios)
    return {"follow_ratio_mean": ratios.mean().item(), "follow_ratio_median": ratios.median().item(),
            "follow_ratio_sd": ratios.std().item(), "other_movement_mean": sum(others) / len(others),
            "r2_of_change": M.r2(torch.cat(changes), torch.cat(deltas)), "jump_fraction": jumps / len(ratios)}


@torch.no_grad()
def r2_new(model, x):
    dim = x.shape[1]
    xs = x.repeat_interleave(dim, dim=0)
    i = torch.arange(dim).repeat(len(x))
    return M.r2(model.answer(xs, i), xs[torch.arange(len(xs)), i])


@torch.no_grad()
def r2_sets(model, tokens):
    """(R², centred R²) of the answers about the given tokens."""
    dim = model.E.shape[1]
    t, i = M.all_pairs(tokens, dim)
    a = model(t, i).view(len(tokens), dim)
    y = model.E[tokens]
    centred = 1 - ((a - y) - (a - y).mean(0)).pow(2).sum().item() / (y - y.mean(0)).pow(2).sum().item()
    return M.r2(a.flatten(), y.flatten()), centred


@torch.no_grad()
def measure(model, train_tokens, held_out, seed=0):
    """All measurements for one model. Leaves model.E exactly as it found it."""
    E_before = model.E.detach().clone()
    gen = torch.Generator().manual_seed(seed)
    out = {}
    for name, toks in (("train", train_tokens), ("held_out", held_out)):
        out[f"r2_{name}"], out[f"r2_{name}_centred"] = r2_sets(model, toks)
        for k, v in local_follow(model, toks).items():
            out[f"{name}_{k}"] = v
        for size in SIZES:
            for k, v in follow(model, toks, size, gen).items():
                out[f"{name}_{size:g}_{k}"] = v
    dim = model.E.shape[1]
    out["r2_new_standard"] = r2_new(model, torch.randn(N_NEW, dim, generator=gen))
    rows = model.E[train_tokens]
    out["r2_new_matched"] = r2_new(model, rows.mean(0) + rows.std(0) * torch.randn(N_NEW, dim, generator=gen))
    out["E_rms_train"] = rows.pow(2).mean().sqrt().item()
    out["E_rms_held_out"] = model.E[held_out].pow(2).mean().sqrt().item()
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
    checks = [("reader R² new = 1", abs(reader["r2_new_standard"] - 1) < tol and abs(reader["r2_new_matched"] - 1) < tol)]
    for name in ("train", "held_out"):
        checks += [(f"reader R² {name} = 1", abs(reader[f"r2_{name}"] - 1) < tol),
                   (f"reader centred R² {name} = 1", abs(reader[f"r2_{name}_centred"] - 1) < tol),
                   (f"reader local follow = 1 ({name})", abs(reader[f"{name}_local_follow_mean"] - 1) < tol),
                   (f"reader local other = 0 ({name})", reader[f"{name}_local_other_mean"] < tol),
                   (f"memorizer local follow = 0 ({name})", memo[f"{name}_local_follow_mean"] == 0.0),
                   (f"memorizer local other = 0 ({name})", memo[f"{name}_local_other_mean"] == 0.0)]
        for size in SIZES:
            p = f"{name}_{size:g}_"
            checks += [(f"reader follow ratio = 1 ({p})", abs(reader[p + "follow_ratio_mean"] - 1) < tol),
                       (f"reader median follow ratio = 1 ({p})", abs(reader[p + "follow_ratio_median"] - 1) < tol),
                       (f"reader other movement = 0 ({p})", reader[p + "other_movement_mean"] < 1e-3),   # float32 rounding / small |δ|
                       (f"reader R² of change = 1 ({p})", abs(reader[p + "r2_of_change"] - 1) < 1e-3),
                       (f"reader no jumps ({p})", reader[p + "jump_fraction"] == 0.0)]
            if size < 1:   # a 100% change moves a held-out row toward a stored row along δ: median ~0.26
                checks.append((f"memorizer median follow ratio = 0 ({p})", memo[p + "follow_ratio_median"] == 0.0))
    checks += [("memorizer R² train = 1", memo["r2_train"] == 1.0),
               ("memorizer R² held-out < 0.5", memo["r2_held_out"] < 0.5),
               ("memorizer R² new < 0.5", memo["r2_new_standard"] < 0.5),
               ("memorizer follow ratio = 0 for 1% and 10% changes (train)",
                memo["train_0.01_follow_ratio_mean"] == 0.0 and memo["train_0.1_follow_ratio_mean"] == 0.0),
               ("memorizer R² of change <= 0 (train, 10%)", memo["train_0.1_r2_of_change"] <= 0.0)]
    failed = [name for name, ok in checks if not ok]
    if failed:
        raise AssertionError(f"canary checks failed: {failed}\nreader: {reader}\nmemorizer: {memo}")
    return {"perfect_reader": reader, "memorizer": memo}


def main():
    torch.set_num_threads(4)
    out = {"canaries": check_canaries()}
    print("canaries: all known results reproduced", flush=True)
    for path in sorted(p for p in RESULTS.glob("*.pt") if RUN_NAME.match(p.stem)):
        m, s = T.load(path)
        train_tokens, held_out = M.split_tokens(s["seed"])
        out[path.stem] = {"settings": s, **measure(m, train_tokens, held_out, s["seed"])}
        print(path.stem, {k: round(v, 4) for k, v in out[path.stem].items() if isinstance(v, float)}, flush=True)
        base_name = f"untrained_seed{s['seed']}"
        if base_name not in out:
            torch.manual_seed(s["seed"])           # same initialization as the run (train.train), untrained
            base = M.SelfReporter(s["n_tokens"], s["dim"], s["n_layers"], s["n_heads"], s["mlp_width"])
            out[base_name] = measure(base, train_tokens, held_out, s["seed"])
    (RESULTS / "follow_test.json").write_text(json.dumps(out, indent=1))
    print("wrote results/follow_test.json")


if __name__ == "__main__":
    main()
