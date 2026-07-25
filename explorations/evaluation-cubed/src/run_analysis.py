"""
Stage 5: run every Eval-cubed experiment and dump results/analysis.json.

E1  judge error decomposition (validity ratio, style preference)
E2  H1: does meta-evaluation accuracy predict downstream ranking fidelity?
E3  H2: how much does a judge's fidelity move across system populations?
E4  H4/L3: protocol regret -- which meta-evaluation protocol selects the better judge?
E5  the perturbation certificate: coverage and correctness
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analysis import (  # noqa: E402
    KS, STYLES, all_style_assignments, anova_decomposition, certificate,
    homogeneous_populations, kendall_fidelity, load_scores, protocol_scores,
    sra, system_means, true_quality,
)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

FULL_GRID = [f"k{k}_{st}" for k in KS for st in STYLES]

# Protocols where a *higher* score means "better judge".
HIGHER_BETTER = {
    "P1_pair_acc": True, "P2_item_rho": True, "P3_dev_sra": True,
    "P4a_style_spread": False, "P4b_style_bias": False,
    "P4c_sep_over_bias": True, "P4d_monotonicity": True,
}
GOLD_PROTOCOLS = ["P1_pair_acc", "P2_item_rho", "P3_dev_sra"]
FREE_PROTOCOLS = ["P4a_style_spread", "P4b_style_bias", "P4c_sep_over_bias", "P4d_monotonicity"]


def main() -> None:
    answers = json.load(open(os.path.join(DATA, "answers.json")))
    items = sorted({a["item_id"] for a in answers})
    scores = load_scores()
    judges = sorted(scores)
    print(f"{len(judges)} judges, {len(items)} items, {len(FULL_GRID)} systems")

    # keep only judges with (near) complete coverage of the grid
    complete = []
    for j in judges:
        need = len(items) * len(FULL_GRID)
        have = sum(1 for (it, s) in scores[j] if s in FULL_GRID)
        if have >= 0.98 * need:
            complete.append(j)
        else:
            print(f"  dropping {j}: {have}/{need} cells")
    judges = complete
    out: dict = {"judges": judges, "n_items": len(items), "systems": FULL_GRID}

    # ---------------------------------------------------------------- E1
    print("\n=== E1  judge error decomposition ===")
    sysm = {j: system_means(scores[j], items) for j in judges}
    dec = {j: anova_decomposition(sysm[j]) for j in judges}
    out["decomposition"] = dec
    out["system_means"] = {j: sysm[j] for j in judges}

    print(f"{'judge':<28} {'V':>6} {'Qrange':>7} {'Srange':>7} {'slope':>7} "
          f"{'SRA_all':>8}  style preference")
    rows = []
    for j in judges:
        d = dec[j]
        s_all = sra(sysm[j], FULL_GRID)
        pref = " ".join(f"{st[:4]}={d['style_pref'][st]:.3f}" for st in STYLES)
        rows.append((d["validity_ratio"], j, d, s_all, pref))
    for v, j, d, s_all, pref in sorted(rows, reverse=True):
        print(f"{j:<28} {v:6.3f} {d['quality_range']:7.3f} {d['style_range']:7.3f} "
              f"{d['quality_slope']:7.3f} {s_all:8.3f}  {pref}")

    # ---------------------------------------------------------------- populations
    pops = all_style_assignments()
    homo = homogeneous_populations()
    fid = {j: np.array([sra(sysm[j], p) for _, p in pops]) for j in judges}
    out["population_fidelity"] = {j: fid[j].tolist() for j in judges}
    out["population_combos"] = ["-".join(c) for c, _ in pops]

    # ---------------------------------------------------------------- E3
    print("\n=== E3  fidelity across the 243 equal-truth populations ===")
    print("(every population has the identical true ranking k0>k1>k2>k3>k4;")
    print(" they differ only in which quality-preserving style each level wears)")
    print(f"{'judge':<28} {'mean':>6} {'sd':>6} {'min':>6} {'max':>6} {'P(<=.5)':>8}")
    e3 = {}
    for j in judges:
        f = fid[j]
        e3[j] = {"mean": float(f.mean()), "sd": float(f.std()), "min": float(f.min()),
                 "max": float(f.max()), "p_chance": float((f <= 0.5).mean()),
                 "homogeneous": {n: sra(sysm[j], p) for n, p in homo.items()}}
        print(f"{j:<28} {f.mean():6.3f} {f.std():6.3f} {f.min():6.3f} {f.max():6.3f} "
              f"{(f <= 0.5).mean():8.3f}")
    out["E3"] = e3

    best_per_pop = [judges[int(np.argmax([fid[j][i] for j in judges]))] for i in range(len(pops))]
    from collections import Counter
    out["E3_best_judge_counts"] = dict(Counter(best_per_pop))
    print("\nidentity of the best judge, across the 243 populations:")
    for j, c in Counter(best_per_pop).most_common():
        print(f"  {j:<28} best on {c:>3}/{len(pops)} populations")

    # ---------------------------------------------------------------- protocol scores
    print("\ncomputing protocol scores on every population ...")
    proto = {}  # (judge, pop_index) -> dict
    for j in judges:
        for i, (_, p) in enumerate(pops):
            proto[(j, i)] = protocol_scores(scores[j], items, p)
    out["protocol_scores_full_grid"] = {
        j: protocol_scores(scores[j], items, FULL_GRID) for j in judges}

    # ---------------------------------------------------------------- E2
    print("\n=== E2  does meta-evaluation accuracy predict ranking fidelity? ===")
    e2 = {}
    for name in GOLD_PROTOCOLS + FREE_PROTOCOLS:
        # in-distribution: protocol and fidelity on the same population
        rs_in, rs_tr = [], []
        for i in range(len(pops)):
            x = [proto[(j, i)][name] for j in judges]
            y = [fid[j][i] for j in judges]
            if np.std(x) > 0:
                rs_in.append(stats.spearmanr(x, y).statistic)
        # transfer: protocol on population i, fidelity on population i' != i
        rng = np.random.default_rng(0)
        for _ in range(2000):
            i, i2 = rng.integers(0, len(pops), 2)
            if i == i2:
                continue
            x = [proto[(j, int(i))][name] for j in judges]
            y = [fid[j][int(i2)] for j in judges]
            if np.std(x) > 0:
                rs_tr.append(stats.spearmanr(x, y).statistic)
        sgn = 1 if HIGHER_BETTER[name] else -1
        e2[name] = {
            "rho_in_distribution": float(sgn * np.nanmean(rs_in)),
            "rho_transfer": float(sgn * np.nanmean(rs_tr)),
            "rho_transfer_sd": float(np.nanstd(rs_tr)),
        }
        print(f"  {name:<20} rho(in-dist)={e2[name]['rho_in_distribution']:+.3f}   "
              f"rho(transfer)={e2[name]['rho_transfer']:+.3f} "
              f"(sd {e2[name]['rho_transfer_sd']:.3f})")
    out["E2"] = e2

    # ---------------------------------------------------------------- E4
    print("\n=== E4  judge-selection regret (level-3 metric) ===")
    print("select a judge using protocol P, then measure realised fidelity on target T")
    rng = np.random.default_rng(1)
    trials = [(int(a), int(b)) for a, b in rng.integers(0, len(pops), (4000, 2)) if a != b]
    e4 = {}

    def regret_for(select_idx_fn, name):
        regs, fids = [], []
        for d, t in trials:
            j = select_idx_fn(d, t)
            best = max(fid[jj][t] for jj in judges)
            regs.append(best - fid[j][t])
            fids.append(fid[j][t])
        e4[name] = {"mean_regret": float(np.mean(regs)), "mean_fidelity": float(np.mean(fids)),
                    "p_below_chance": float(np.mean(np.array(fids) <= 0.5))}
        print(f"  {name:<34} regret={np.mean(regs):.4f}  fidelity={np.mean(fids):.4f}  "
              f"P(fid<=.5)={np.mean(np.array(fids) <= 0.5):.3f}")

    for name in GOLD_PROTOCOLS:
        sgn = 1 if HIGHER_BETTER[name] else -1
        regret_for(lambda d, t, n=name, s=sgn:
                   max(judges, key=lambda j: s * proto[(j, d)][n]), f"{name} @dev  (realistic)")
    for name in GOLD_PROTOCOLS:
        sgn = 1 if HIGHER_BETTER[name] else -1
        regret_for(lambda d, t, n=name, s=sgn:
                   max(judges, key=lambda j: s * proto[(j, t)][n]),
                   f"{name} @target (label oracle)")
    for name in FREE_PROTOCOLS:
        sgn = 1 if HIGHER_BETTER[name] else -1
        regret_for(lambda d, t, n=name, s=sgn:
                   max(judges, key=lambda j: s * proto[(j, t)][n]), f"{name} @target (label-free)")
    regret_for(lambda d, t: judges[int(np.argmax([fid[j][t] for j in judges]))], "ORACLE")
    rngc = np.random.default_rng(2)
    regret_for(lambda d, t: judges[int(rngc.integers(0, len(judges)))], "random judge")
    out["E4"] = e4

    # ---------------------------------------------------------------- E5
    print("\n=== E5  perturbation certificate ===")
    print(f"{'judge':<28} {'bias B':>8} {'cover':>7} {'cert.acc':>9} {'raw acc':>8}")
    e5 = {}
    for j in judges:
        ps = protocol_scores(scores[j], items, FULL_GRID)
        c = certificate(sysm[j], ps["P4b_style_bias"], FULL_GRID)
        e5[j] = {**c, "bias": ps["P4b_style_bias"]}
        print(f"{j:<28} {ps['P4b_style_bias']:8.4f} {c['coverage']:7.3f} "
              f"{c['certified_acc']:9.3f} {c['uncert_acc']:8.3f}")
    cov = np.mean([e5[j]["coverage"] for j in judges])
    cacc = np.nanmean([e5[j]["certified_acc"] for j in judges])
    racc = np.mean([e5[j]["uncert_acc"] for j in judges])
    print(f"{'MEAN':<28} {'':>8} {cov:7.3f} {cacc:9.3f} {racc:8.3f}")
    out["E5"] = e5
    out["E5_summary"] = {"coverage": float(cov), "certified_acc": float(cacc),
                         "raw_acc": float(racc)}

    with open(os.path.join(RESULTS, "analysis.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nwrote {os.path.join(RESULTS, 'analysis.json')}")


if __name__ == "__main__":
    main()
