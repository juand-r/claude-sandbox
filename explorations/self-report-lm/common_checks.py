"""Two checks added after the second report review (NOTES.md, 2026-10-07 evening).

1. Rescaling score at fixed norms. analyze_review.py grows frequent never-asked vectors to the
   run's own mean rare-token norm, which differs between runs (3.7 to 4.4), so its scores are
   not comparable across runs. Here every run's frequent never-asked vectors are grown to the
   same norms FIXED_NORMS; the score is analyze_review's (1 − mean squared error per vector /
   mean squared distance of the run's never-asked vectors from their coordinate means).
2. Clip factor min(1, CLIP / |g|) of the gradient g, for the next-token loss alone and for the
   training loss of the run (next-token + λ·self-report [+ slope loss]), over N_BATCHES training
   batches, without perturbed questions (the slope loss uses the run's setting).

Writes results/common_checks.json.
Usage: python common_checks.py
"""
import json

import numpy as np
import torch

import analyze_review as AR
import lm
import measure as Ms
import textanswer as TA
import train as T

FIXED_NORMS = (3.0, 4.0, 5.0)
RUNS = ["joint_detached_s0", "control_jit_s0", "ft2_lam4_jit", "ft_slope", "control_slope_s0", "control_slope_lam1_s0"]
CLIP_RUNS = ["joint_detached_s0", "control_slope_s0", "text_jit_lam4_long2"]
N_BATCHES = 5


@torch.no_grad()
def rescaling_at_fixed_norms(m, s, counts):
    _, ho = lm.split_tokens(s["seed"], s["n_text"])
    c = counts[ho.numpy()]
    Yf = m.E[ho[torch.from_numpy(c >= 10_000)]].detach()
    Yall = m.E[ho].detach()
    spread = (Yall - Yall.mean(0)).pow(2).sum(1).mean().item()
    out = {}
    for L in FIXED_NORMS:
        Z = Yf / Yf.norm(dim=1, keepdim=True) * L
        out[str(L)] = 1 - (AR.answers(m, Z) - Z).pow(2).sum(1).mean().item() / spread
    return out


def grad_norm(m, loss):
    m.zero_grad()
    loss.backward()
    return torch.sqrt(sum(p.grad.pow(2).sum() for p in m.parameters() if p.grad is not None)).item()


def clip_factors(m, s, data, fmt):
    m.train()
    asked, _ = lm.split_tokens(s["seed"], s["n_text"])
    if s.get("answer") == "text":
        asked = TA.question_tokens(asked, fmt)
    g = torch.Generator().manual_seed(5)
    alone, combined = [], []
    for _ in range(N_BATCHES):
        x, y = T.lm_batch(data, T.LM_BATCH, g)
        t = asked[torch.randint(0, len(asked), (T.REPORT_BATCH,), generator=g)]
        i = torch.randint(0, m.dim, (T.REPORT_BATCH,), generator=g)
        a = grad_norm(m, T.lm_loss(m, x, y))
        if s.get("answer") == "text":
            rep = TA.text_report_loss(m, t, i, fmt)
        else:
            rep = T.report_loss(m, t, i, detach_input=True)
            if s.get("slope_weight", 0) > 0:
                rep = rep + s["slope_weight"] / s["lam"] * T.slope_loss(m, t, i, g)
        b = grad_norm(m, T.lm_loss(m, x, y) + s["lam"] * rep)
        alone.append(min(1.0, T.CLIP / a))
        combined.append(min(1.0, T.CLIP / b))
    m.eval()
    return {"lm_alone": alone, "combined": combined}


def main():
    torch.set_num_threads(4)
    counts = np.bincount(np.fromfile(T.DATA / "train.bin", dtype=np.uint16), minlength=lm.N_TEXT)
    out = {"fixed_norms": FIXED_NORMS, "rescaling_fixed_norms": {}, "clip_factors": {}}
    for r in RUNS:
        m, s = Ms.load(r)
        out["rescaling_fixed_norms"][r] = rescaling_at_fixed_norms(m, s, counts)
        print(r, {k: round(v, 3) for k, v in out["rescaling_fixed_norms"][r].items()}, flush=True)
    data, fmt = T.load_tokens("train"), TA.Format(T.DATA / "tokenizer.json")
    for r in CLIP_RUNS:
        m, s = Ms.load(r)
        out["clip_factors"][r] = clip_factors(m, s, data, fmt)
        print(r, {k: [round(v, 2) for v in vs] for k, vs in out["clip_factors"][r].items()}, flush=True)
    (Ms.HERE / "results" / "common_checks.json").write_text(json.dumps(out, indent=1))
    print("wrote results/common_checks.json")


if __name__ == "__main__":
    main()
