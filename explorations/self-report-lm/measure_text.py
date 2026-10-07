"""Measurements for stage 2 (text answers; PLAN.md, textanswer.py).

- validation loss on 100 × 32 windows (as measure.py);
- centred R² of the decoded answers (greedy, restricted to valid characters) over all
  asked-about and all never-asked tokens (the 13 answer characters excluded);
- valid-format rate without the restriction, on N_FMT tokens × all coordinates;
- finite-change follow at FINITE_SIZE (30% of |E[t]|; the answers move in steps of 0.01, so
  small changes would mostly round away): mean and median over N_FOLLOW tokens per set.
  The same measure for a number-head model given as reference, for comparison;
- three stories.

Usage: python measure_text.py <text run> [<number-head reference run>]
Writes results/measure_<text run>.json
"""
import json
import os
import sys

import numpy as np
import torch
from tokenizers import Tokenizer

import lm
import measure as Ms
import textanswer as TA
import train as T

FINITE_SIZE = 0.30
N_FOLLOW = 256
N_FMT = 64


@torch.no_grad()
def centred_r2(m, fmt, toks):
    t = toks.repeat_interleave(m.dim)
    i = torch.arange(m.dim).repeat(len(toks))
    a = TA.text_answers(m, m.E[t], i, fmt).view(len(toks), m.dim)
    y = m.E[toks]
    return 1 - (a - y).pow(2).sum().item() / (y - y.mean(0)).pow(2).sum().item()


@torch.no_grad()
def finite_follow_text(m, fmt, toks, gen):
    d, ratios = m.dim, []
    i = torch.arange(d)
    for t in toks.tolist():
        x = m.E[t].clone()
        delta = torch.randn(d, generator=gen)
        delta *= FINITE_SIZE * x.norm() / delta.norm()
        before = TA.text_answers(m, x.expand(d, d), i, fmt)
        after = TA.text_answers(m, (x + delta).expand(d, d), i, fmt)
        ratios.append(((after - before) @ delta / (delta @ delta)).item())
    return float(np.mean(ratios)), float(np.median(ratios))


@torch.no_grad()
def finite_follow_number(m, toks, gen):
    d, ratios = m.dim, []
    for t in toks.tolist():
        x = m.E[t].clone()
        delta = torch.randn(d, generator=gen)
        delta *= FINITE_SIZE * x.norm() / delta.norm()
        before, after = Ms.answers_for(m, x), Ms.answers_for(m, x + delta)
        ratios.append(((after - before) @ delta / (delta @ delta)).item())
    return float(np.mean(ratios)), float(np.median(ratios))


@torch.no_grad()
def valid_format_rate(m, fmt, toks):
    t = toks.repeat_interleave(m.dim)
    i = torch.arange(m.dim).repeat(len(toks))
    return float((~torch.isnan(TA.text_answers(m, m.E[t], i, fmt, constrained=False))).float().mean())


def main():
    name = sys.argv[1]
    ref = sys.argv[2] if len(sys.argv) > 2 else None
    torch.set_num_threads(int(os.environ.get("THREADS", "4")))
    fmt = TA.Format(T.DATA / "tokenizer.json")
    m, s = Ms.load(name)
    asked, never = lm.split_tokens(s["seed"], s["n_text"])
    asked, never = TA.question_tokens(asked, fmt), TA.question_tokens(never, fmt)
    gen = torch.Generator().manual_seed(s["seed"] + 555)
    valid = T.load_tokens("valid")
    vgen = torch.Generator().manual_seed(4321)
    out = {"settings": s, "finite_size": FINITE_SIZE}
    with torch.no_grad():
        out["valid_loss"] = float(np.mean([T.lm_loss(m, x, y).item()
                                           for x, y in (T.lm_batch(valid, T.LM_BATCH, vgen) for _ in range(Ms.N_VALID_BATCHES))]))
    pick = lambda toks, n: toks[torch.randperm(len(toks), generator=gen)[:n]]
    for set_name, toks in (("asked", asked), ("never", never)):
        out[f"r2c_{set_name}"] = centred_r2(m, fmt, toks)
        out[f"valid_format_rate_{set_name}"] = valid_format_rate(m, fmt, pick(toks, N_FMT))
        ft = pick(toks, N_FOLLOW)
        out[f"finite_follow_mean_{set_name}"], out[f"finite_follow_median_{set_name}"] = finite_follow_text(m, fmt, ft, gen)
        if ref:
            mr, _ = Ms.load(ref)
            out[f"ref_{ref}_finite_follow_mean_{set_name}"], out[f"ref_{ref}_finite_follow_median_{set_name}"] = \
                finite_follow_number(mr, ft, torch.Generator().manual_seed(s["seed"] + 556))
        print(set_name, {k: round(v, 4) for k, v in out.items() if isinstance(v, float)}, flush=True)
    out["stories"] = Ms.generate(m, Tokenizer.from_file(str(T.DATA / "tokenizer.json")), gen)
    (Ms.HERE / "results" / f"measure_{name}.json").write_text(json.dumps(out, indent=1))
    print("wrote", f"results/measure_{name}.json")


if __name__ == "__main__":
    main()
