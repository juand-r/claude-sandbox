"""Checks prompted by the review of REPORT.md (NOTES.md). Writes results/review_checks_<name>.json.

1. The direction block 0 cannot see: u = c/|c| with c = (E[t] + P[2]) − mean(E[t] + P[2])·1
   (LayerNorm at block 0 removes the mean and divides by the standard deviation, so scaling c
   changes nothing it sees). Response uᵀJu, against x̂ᵀJx̂ (length) and cos(E[t], c).
2. Follow and centred R² by frequency bin, with each bin's own coordinate means as the baseline,
   and the mean pairwise cosine of the vectors in each bin.
3. Rescaling test: rare held-out vectors rescaled to the mean length of frequent ones, and
   frequent held-out vectors rescaled to the mean length of rare ones; centred R² (bin's own
   means) before and after.
4. Linear probe: ridge regression from the pre-final-LayerNorm state at t's position of a
   one-token sequence [t] ... here the state at t's position of the question layout with the
   language-model-only model, to E[t]; fitted on training tokens, centred R² on held-out tokens.
5. Centred R² on random vectors.
6. Edit test: pooled KL ratio over positions, and how many tokens have a ratio above 1.
7. Number of tokens that never occur in train.bin, per set.

Usage: python analyze_review.py <joint run> <lm-only run>
"""
import json
import sys

import numpy as np
import torch

import lm
import measure as Ms

BINS = ((0, 100), (100, 10_000), (10_000, 10**12))
N_PER_BIN = 64      # tokens per bin for Jacobian measures (all if fewer)


def answers(m, X):
    """Answers to all DIM questions for each row of X: (n, DIM)."""
    d = m.dim
    out = []
    with torch.no_grad():
        for k in range(0, len(X), 256):
            x = X[k:k + 256]
            xs = x.repeat_interleave(d, dim=0)
            out.append(m.answer(xs, torch.arange(d).repeat(len(x))).view(len(x), d))
    return torch.cat(out)


def centred_r2_own(a, y):
    return 1 - (a - y).pow(2).sum().item() / (y - y.mean(0)).pow(2).sum().item()


def mean_pairwise_cos(Y):
    Z = Y / Y.norm(dim=1, keepdim=True)
    C = Z @ Z.T
    n = len(Y)
    return ((C.sum() - n) / (n * (n - 1))).item() if n > 1 else float("nan")


def main():
    joint, base = sys.argv[1], sys.argv[2]
    torch.set_num_threads(2)
    m, s = Ms.load(joint)
    mb, _ = Ms.load(base)
    tr, ho = lm.split_tokens(s["seed"], s["n_text"])
    counts = np.bincount(np.fromfile(Ms.T.DATA / "train.bin", dtype=np.uint16), minlength=s["n_text"])
    gen = torch.Generator().manual_seed(7)
    out = {}

    # 1. blind direction of block 0
    rows = []
    for set_name, toks in (("train", tr), ("held_out", ho)):
        for t in toks[torch.randperm(len(toks), generator=gen)[:64]].tolist():
            x = m.E[t].detach()
            J = Ms.jacobian(m, x)
            v = x + m.P[2].detach()
            c = v - v.mean()
            u, xh = c / c.norm(), x / x.norm()
            rows.append({"set": set_name, "blind": (u @ J @ u).item(), "length": (xh @ J @ xh).item(),
                         "cos_x_c": (xh @ u).item()})
    out["blind_direction"] = {sn: {k: float(np.mean([r[k] for r in rows if r["set"] == sn]))
                                   for k in ("blind", "length", "cos_x_c")} for sn in ("train", "held_out")}
    out["P2_length"] = m.P[2].norm().item()

    # 2. by frequency bin, own baseline
    bins = []
    for set_name, toks in (("train", tr), ("held_out", ho)):
        c = counts[toks.numpy()]
        for lo, hi in BINS:
            sel = toks[torch.from_numpy((c >= lo) & (c < hi))]
            if len(sel) == 0:
                continue
            Y = m.E[sel].detach()
            A = answers(m, Y)
            jt = sel[torch.randperm(len(sel), generator=gen)[:N_PER_BIN]]
            jm = Ms.jacobian_measures(m, jt)
            bins.append({"set": set_name, "count_from": lo, "count_below": hi, "n_tokens": len(sel),
                         "centred_r2_own_means": centred_r2_own(A, Y), "follow": jm["follow"],
                         "other": jm["other"], "mean_length": Y.norm(dim=1).mean().item(),
                         "mean_pairwise_cos": mean_pairwise_cos(Y)})
    out["bins"] = bins

    # 3. rescaling test on held-out tokens
    c = counts[ho.numpy()]
    rare, freq = ho[torch.from_numpy(c < 100)], ho[torch.from_numpy(c >= 10_000)]
    Yr, Yf = m.E[rare].detach(), m.E[freq].detach()
    Lr, Lf = Yr.norm(dim=1).mean(), Yf.norm(dim=1).mean()
    # error relative to the spread of all held-out embedding vectors around their coordinate means
    # (a bin's own spread is useless here: the rare held-out vectors are nearly identical)
    Yall = m.E[ho].detach()
    spread = (Yall - Yall.mean(0)).pow(2).sum(1).mean().item()
    def rel_r2(Y, L=None):
        Z = Y if L is None else Y / Y.norm(dim=1, keepdim=True) * L
        return 1 - (answers(m, Z) - Z).pow(2).sum(1).mean().item() / spread
    out["rescaling"] = {"baseline": "1 - mean squared error per vector / mean squared distance of held-out vectors from their coordinate means",
                        "rare_mean_length": Lr.item(), "frequent_mean_length": Lf.item(),
                        "rare_as_is": rel_r2(Yr), "rare_shrunk_to_frequent_length": rel_r2(Yr, Lf),
                        "frequent_as_is": rel_r2(Yf), "frequent_grown_to_rare_length": rel_r2(Yf, Lr)}

    # 4. linear probe on the language-model-only model: state at t's position (question layout,
    #    coordinate token 0) -> E[t]; ridge fitted on training tokens, centred R² on held-out tokens
    with torch.no_grad():
        def states(toks):
            n = len(toks)
            emb = torch.stack([mb.E[mb.query_id].expand(n, -1), mb.E[mb.coord_id(torch.zeros(n, dtype=torch.long))],
                               mb.E[toks]], dim=1)
            return mb.residual(emb)[:, -1]
        Htr, Hho = states(tr), states(ho)
        Ytr, Yho = mb.E[tr], mb.E[ho]
        X = torch.cat([Htr, torch.ones(len(Htr), 1)], 1).double()
        W = torch.linalg.solve(X.T @ X + 1e-3 * torch.eye(X.shape[1], dtype=torch.float64), X.T @ Ytr.double())
        pred = (torch.cat([Hho, torch.ones(len(Hho), 1)], 1).double() @ W).float()
    out["linear_probe_lm_only_centred_r2_held_out"] = centred_r2_own(pred, Yho)

    # 5. centred R² on random vectors (matched distribution)
    rows_all = m.E[:m.n_text].detach()
    Xr = rows_all.mean(0) + rows_all.std(0) * torch.randn(1024, m.dim, generator=gen)
    out["random_vectors_centred_r2"] = centred_r2_own(answers(m, Xr), Xr)

    # 6. edit test summary
    meas = json.loads((Ms.HERE / "results" / f"measure_{joint}.json").read_text())
    et = meas["edit_test"]
    kl_at = sum(r["kl_at_t"] for r in et) / len(et)
    kl_no = sum(r["kl_no_t"] for r in et) / len(et)
    out["edit_test"] = {"ratio_of_token_means": kl_at / kl_no,
                        "mean_of_token_ratios": float(np.mean([r["kl_at_t"] / r["kl_no_t"] for r in et])),
                        "pooled_kl_at_t": sum(r["kl_at_t"] * r["count"] for r in et) / sum(r["count"] for r in et),
                        "tokens_with_ratio_above_1": sum(r["kl_at_t"] > r["kl_no_t"] for r in et),
                        "n_tokens": len(et)}
    out["edit_test"]["pooled_ratio"] = out["edit_test"]["pooled_kl_at_t"] / kl_no

    # 7. tokens never seen in train.bin
    out["zero_count_tokens"] = {"train": int((counts[tr.numpy()] == 0).sum()), "held_out": int((counts[ho.numpy()] == 0).sum())}

    (Ms.HERE / "results" / f"review_checks_{joint}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
