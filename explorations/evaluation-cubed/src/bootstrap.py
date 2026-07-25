"""
Bootstrap confidence intervals for the headline quantities.

The construct-validity audit of LLM benchmarks found that only 16% of benchmark papers
report uncertainty estimates. Every headline number in this paper gets a CI.

Resampling unit: the **item**. Items are the independent replicates here (systems and
judges are fixed factors, fully crossed), so resampling items with replacement and
recomputing the whole pipeline propagates sampling error into every derived statistic,
including the level-3 regret figures.

Implementation note: everything runs off a dense array S[judge, item, system] so a
bootstrap replicate is a single fancy-index plus a mean, rather than a re-parse.
"""

from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis import KS, STYLES, load_scores, true_quality  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")

FULL_GRID = [f"k{k}_{st}" for k in KS for st in STYLES]
B_DEFAULT = 400


def build_array(scores, judges, items, systems):
    """S[j, i, s] with NaN for missing cells."""
    S = np.full((len(judges), len(items), len(systems)), np.nan)
    ii = {it: a for a, it in enumerate(items)}
    ss = {s: a for a, s in enumerate(systems)}
    for jx, j in enumerate(judges):
        for (it, s), v in scores[j].items():
            if it in ii and s in ss:
                S[jx, ii[it], ss[s]] = v
    return S


def pair_index(systems, population):
    """Indices of comparable system pairs (differing true quality) within a population."""
    idx = {s: a for a, s in enumerate(systems)}
    a_i, b_i, sign = [], [], []
    for a, b in itertools.combinations(population, 2):
        qa, qb = true_quality(int(a[1])), true_quality(int(b[1]))
        if qa == qb:
            continue
        a_i.append(idx[a])
        b_i.append(idx[b])
        sign.append(1.0 if qa > qb else -1.0)
    return np.array(a_i), np.array(b_i), np.array(sign)


def sra_vec(M, pidx):
    """M[..., systems] of system means -> SRA. Vectorised over leading axes."""
    a_i, b_i, sign = pidx
    d = (M[..., a_i] - M[..., b_i]) * sign
    return np.where(d > 0, 1.0, np.where(d == 0, 0.5, 0.0)).mean(axis=-1)


def validity_ratio_vec(M, systems):
    """Two-way ANOVA validity ratio from system means. M[..., systems]."""
    idx = {s: a for a, s in enumerate(systems)}
    grid = np.array([[idx[f"k{k}_{st}"] for st in STYLES] for k in KS])  # 5 x 3
    G = M[..., grid]                                    # (..., 5, 3)
    grand = G.mean(axis=(-2, -1), keepdims=True)
    row = G.mean(axis=-1, keepdims=True)
    col = G.mean(axis=-2, keepdims=True)
    ss_q = G.shape[-1] * ((row - grand) ** 2).sum(axis=(-2, -1))
    ss_s = G.shape[-2] * ((col - grand) ** 2).sum(axis=(-2, -1))
    pred = grand + (row - grand) + (col - grand)
    ss_i = ((G - pred) ** 2).sum(axis=(-2, -1))
    tot = ss_q + ss_s + ss_i
    return np.where(tot > 0, ss_q / np.where(tot > 0, tot, 1), np.nan), ss_q, ss_s, ss_i


def style_bias_vec(M, systems, population):
    """Label-free style-bias range R for each judge, given a population's quality levels."""
    idx = {s: a for a, s in enumerate(systems)}
    ks = sorted({int(s[1]) for s in population})
    per_style = np.stack(
        [M[..., [idx[f"k{k}_{st}"] for k in ks]].mean(axis=-1) for st in STYLES], axis=-1)
    return per_style.max(axis=-1) - per_style.min(axis=-1)


def main(B: int = B_DEFAULT) -> None:
    scores = load_scores()
    judges = sorted(scores)
    items = sorted({it for j in judges for (it, _) in scores[j]})
    # keep judges with complete coverage
    judges = [j for j in judges
              if sum(1 for (it, s) in scores[j] if s in FULL_GRID) >= 0.98 * len(items) * 15]
    S = build_array(scores, judges, items, FULL_GRID)
    nJ, nI, nS = S.shape
    print(f"bootstrap: {nJ} judges x {nI} items x {nS} systems, B={B}")

    pops = [[f"k{k}_{st}" for k, st in zip(KS, combo)]
            for combo in itertools.product(STYLES, repeat=len(KS))]
    pidx_full = pair_index(FULL_GRID, FULL_GRID)
    pidx_pops = [pair_index(FULL_GRID, p) for p in pops]

    rng = np.random.default_rng(7)
    boot_sra = np.zeros((B, nJ))
    boot_vr = np.zeros((B, nJ))
    boot_popfid = np.zeros((B, nJ, len(pops)))
    boot_bias = np.zeros((B, nJ))

    for b in range(B):
        sel = rng.integers(0, nI, nI)
        M = np.nanmean(S[:, sel, :], axis=1)          # judges x systems
        boot_sra[b] = sra_vec(M, pidx_full)
        boot_vr[b] = validity_ratio_vec(M, FULL_GRID)[0]
        boot_bias[b] = style_bias_vec(M, FULL_GRID, FULL_GRID)
        for pi, pidx in enumerate(pidx_pops):
            boot_popfid[b, :, pi] = sra_vec(M, pidx)
        if (b + 1) % 100 == 0:
            print(f"  {b+1}/{B}")

    def ci(a, axis=0):
        return (np.nanpercentile(a, 2.5, axis=axis), np.nanpercentile(a, 97.5, axis=axis))

    point_M = np.nanmean(S, axis=1)
    out = {"judges": judges, "B": B, "n_items": nI}
    lo, hi = ci(boot_sra)
    vlo, vhi = ci(boot_vr)
    blo, bhi = ci(boot_bias)
    out["per_judge"] = {}
    print(f"\n{'judge':<28} {'SRA_full':>20} {'validity ratio':>22} {'style bias R':>20}")
    for jx, j in enumerate(judges):
        s = sra_vec(point_M[jx], pidx_full)
        v = validity_ratio_vec(point_M[jx], FULL_GRID)[0]
        r = style_bias_vec(point_M[jx], FULL_GRID, FULL_GRID)
        out["per_judge"][j] = {
            "sra": float(s), "sra_ci": [float(lo[jx]), float(hi[jx])],
            "validity_ratio": float(v), "vr_ci": [float(vlo[jx]), float(vhi[jx])],
            "style_bias": float(r), "bias_ci": [float(blo[jx]), float(bhi[jx])],
            "pop_fid_mean": float(np.mean([sra_vec(point_M[jx], p) for p in pidx_pops])),
            "pop_fid_min": float(np.min([sra_vec(point_M[jx], p) for p in pidx_pops])),
            "pop_fid_max": float(np.max([sra_vec(point_M[jx], p) for p in pidx_pops])),
        }
        print(f"{j:<28} {s:6.3f} [{lo[jx]:.3f},{hi[jx]:.3f}]  "
              f"{v:6.3f} [{vlo[jx]:.3f},{vhi[jx]:.3f}]   "
              f"{r:6.3f} [{blo[jx]:.3f},{bhi[jx]:.3f}]")

    # spread of a judge's fidelity across the 243 equal-truth populations, with CI
    spread = boot_popfid.max(axis=2) - boot_popfid.min(axis=2)
    slo, shi = ci(spread)
    for jx, j in enumerate(judges):
        out["per_judge"][j]["pop_fid_spread_ci"] = [float(slo[jx]), float(shi[jx])]

    with open(os.path.join(RESULTS, "bootstrap.json"), "w") as f:
        json.dump(out, f, indent=1)
    np.save(os.path.join(RESULTS, "boot_popfid.npy"), boot_popfid)
    print(f"\nwrote {os.path.join(RESULTS, 'bootstrap.json')}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else B_DEFAULT)
