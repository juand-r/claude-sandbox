"""Measurements on a trained SelfReportLM (PLAN.md, "Measurements").

Notation: for token t, a(x) ∈ ℝ^DIM are the model's answers to the DIM questions
"coordinate 0..DIM-1 of t" when the vector at t's position is x; J = ∂a/∂x at
x = E[t]; x̂ = E[t] / |E[t]|.

  follow           tr(J) / DIM                               (1: reading, 0: memorizing)
  other movement   |J − follow·I|_F / √DIM                     (0 for reading)
  follow, length   x̂ᵀ J x̂: response to a change along E[t]
  follow, direction (tr(J) − x̂ᵀ J x̂) / (DIM − 1): average response to changes across E[t]
  finite follow    Δa·δ / |δ|², for δ in a random direction with |δ| = 10% of |E[t]|

Edit test: E[t] ← E[t] + δ in the model itself (so the language model sees the
change too, at input and output); report the finite follow of the self-report
and the KL divergence between next-token distributions before and after the
edit, at positions in validation text right after t and at all other positions.

Usage: python measure.py <name> [<name> ...]   writes results/measure_<name>.json
"""
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from tokenizers import Tokenizer

import lm
import train as T

HERE = Path(__file__).parent
N_JAC_TRAIN = 512           # training tokens used for Jacobian measures (all held-out tokens are used)
N_RANDOM = 1024             # random vectors for R²
FINITE_SIZE = 0.10
N_EDIT_TOKENS = 20          # most frequent held-out tokens in the validation windows
N_VALID_BATCHES = 100       # validation loss on 100 × 32 windows
GEN_PROMPT, GEN_TOKENS, N_STORIES = "Once upon a time", 120, 3


def answers_for(model, x):
    d = x.shape[0]
    return model.answer(x.unsqueeze(0).expand(d, d), torch.arange(d))


def jacobian_measures(model, tokens):
    d = model.E.shape[1]
    rows = {"follow": [], "other": [], "follow_length": [], "follow_direction": []}
    with torch.enable_grad():
        for t in tokens.tolist():
            x = model.E[t].detach().clone()
            J = torch.autograd.functional.jacobian(lambda v: answers_for(model, v), x)
            f = J.trace().item() / d
            xh = x / x.norm()
            radial = (xh @ J @ xh).item()
            rows["follow"].append(f)
            rows["other"].append(((J - f * torch.eye(d)).norm() / d ** 0.5).item())
            rows["follow_length"].append(radial)
            rows["follow_direction"].append((J.trace().item() - radial) / (d - 1))
    return {k: float(np.mean(v)) for k, v in rows.items()} | {"follow_sd": float(np.std(rows["follow"]))}


@torch.no_grad()
def finite_follow(model, tokens, size, gen):
    d = model.E.shape[1]
    ratios = []
    for t in tokens.tolist():
        original = model.E[t].clone()
        before = answers_for(model, original)
        delta = torch.randn(d, generator=gen)
        delta *= size * original.norm() / delta.norm()
        model.E[t] = original + delta
        after = answers_for(model, model.E[t])
        model.E[t] = original
        ratios.append(((after - before) @ delta / (delta @ delta)).item())
    return float(np.median(ratios)), ratios


@torch.no_grad()
def r2_set(model, tokens):
    t = tokens.repeat_interleave(model.dim)
    i = torch.arange(model.dim).repeat(len(tokens))
    out = []
    for s in range(0, len(t), 32768):
        out.append(model.report(t[s:s + 32768], i[s:s + 32768]))
    return lm.r2(torch.cat(out), model.E[t, i])


@torch.no_grad()
def r2_random(model, gen):
    rows = model.E[:model.n_text]
    x = rows.mean(0) + rows.std(0) * torch.randn(N_RANDOM, model.dim, generator=gen)
    xs = x.repeat_interleave(model.dim, dim=0)
    i = torch.arange(model.dim).repeat(N_RANDOM)
    return lm.r2(model.answer(xs, i), xs[torch.arange(len(xs)), i])


@torch.no_grad()
def edit_test(model, valid_batches, held_out, gen):
    """Edit the embedding vectors of the N_EDIT_TOKENS most frequent held-out tokens, one at a time."""
    xs = torch.cat([x for x, _ in valid_batches])
    counts = torch.bincount(xs.flatten(), minlength=model.n_text)
    tokens = held_out[counts[held_out].argsort(descending=True)[:N_EDIT_TOKENS]]
    base_logp = torch.cat([F.log_softmax(model.lm_logits(x), -1) for x, _ in valid_batches])
    rows = []
    for t in tokens.tolist():
        original = model.E[t].clone()
        before = answers_for(model, original)
        delta = torch.randn(model.dim, generator=gen)
        delta *= FINITE_SIZE * original.norm() / delta.norm()
        model.E[t] = original + delta
        after = answers_for(model, model.E[t])
        logp = torch.cat([F.log_softmax(model.lm_logits(x), -1) for x, _ in valid_batches])
        model.E[t] = original
        kl = (logp.exp() * (logp - base_logp)).sum(-1)              # KL(edited ‖ original) per position
        after_t = xs == t
        rows.append({"token": t, "count": int(counts[t]),
                     "report_follow": ((after - before) @ delta / (delta @ delta)).item(),
                     "kl_after_t": kl[after_t].mean().item(), "kl_elsewhere": kl[~after_t].mean().item()})
    return rows


@torch.no_grad()
def generate(model, tok, gen):
    stories = []
    for _ in range(N_STORIES):
        ids = torch.tensor([tok.encode(GEN_PROMPT).ids])
        for _ in range(GEN_TOKENS):
            logits = model.lm_logits(ids[:, -model.ctx:])[0, -1] / 0.8
            nxt = torch.multinomial(F.softmax(logits, -1), 1, generator=gen)
            ids = torch.cat([ids, nxt.view(1, 1)], dim=1)
        stories.append(tok.decode(ids[0].tolist()))
    return stories


def load(name):
    d = torch.load(HERE / "results" / f"{name}.pt")
    s = d["settings"]
    m = lm.SelfReportLM(s["n_text"], s["dim"], s["n_layers"], s["n_heads"], s["ctx"])
    m.load_state_dict(d["model"])
    return m.eval(), s


def measure(name):
    m, s = load(name)
    gen = torch.Generator().manual_seed(s["seed"])
    train_tokens, held_out = lm.split_tokens(s["seed"])
    valid = T.load_tokens("valid")
    vgen = torch.Generator().manual_seed(4321)
    valid_batches = [T.lm_batch(valid, T.LM_BATCH, vgen) for _ in range(N_VALID_BATCHES)]
    E_before = m.E.detach().clone()
    out = {"settings": s}
    with torch.no_grad():
        out["valid_loss"] = float(np.mean([T.lm_loss(m, x, y).item() for x, y in valid_batches]))
    out["r2_train"] = r2_set(m, train_tokens)
    out["r2_held_out"] = r2_set(m, held_out)
    out["r2_random"] = r2_random(m, gen)
    jac_train = train_tokens[torch.randperm(len(train_tokens), generator=gen)[:N_JAC_TRAIN]]
    out["jacobian_train"] = jacobian_measures(m, jac_train)
    out["jacobian_held_out"] = jacobian_measures(m, held_out)
    for nm, toks in (("train", jac_train), ("held_out", held_out)):
        med, _ = finite_follow(m, toks, FINITE_SIZE, gen)
        out[f"finite_follow_median_{nm}"] = med
    out["edit_test"] = edit_test(m, valid_batches[:20], held_out, gen)
    out["stories"] = generate(m, Tokenizer.from_file(str(T.DATA / "tokenizer.json")), gen)
    if not torch.equal(m.E.detach(), E_before):
        raise RuntimeError("measurement changed the embedding table")
    return out


def main():
    torch.set_num_threads(4)
    for name in sys.argv[1:]:
        out = measure(name)
        (HERE / "results" / f"measure_{name}.json").write_text(json.dumps(out, indent=1))
        print(name, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items()
                     if k not in ("stories", "edit_test", "settings")}, flush=True)


if __name__ == "__main__":
    main()
