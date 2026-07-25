"""
Stage 4: the Eval-cubed analysis.

Vocabulary used throughout:

  L1  a judge scores answers; averaging over items gives a system score  Qhat_J(s)
  L2  a *meta-evaluation protocol* scores a judge
  L3  we score the protocols, by asking whether the judge they select actually ranks
      a held-out population of systems correctly

Key structural fact exploited everywhere below: the system grid is a balanced
5 (quality k) x 3 (style) design in which style is quality-preserving *by construction*.
So the between-system variance of any judge's scores splits, by two-way ANOVA, into
  SS_quality  -- variance the judge is *supposed* to have  (valid signal)
  SS_style    -- variance across quality-preserving restylings  (pure bias)
  SS_inter    -- quality x style interaction                   (pure bias)

Outputs: results/analysis.json  and printed tables.
"""

from __future__ import annotations

import itertools
import json
import os
import sys
from collections import defaultdict

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
RESULTS = os.path.join(HERE, "..", "results")

KS = [0, 1, 2, 3, 4]
STYLES = ["plain", "polished", "padded"]
N_CLAIMS = 6
ANCHOR = "k2_plain"


def true_quality(k: int) -> float:
    """True quality of a level-k system: fraction of the 6 atomic claims that are true."""
    return (N_CLAIMS - k) / N_CLAIMS


# ------------------------------------------------------------------ loading
def load_scores() -> dict[str, dict[tuple[str, str], float]]:
    """judge -> (item_id, system) -> score in [0,1]. Pointwise and pairwise unified."""
    out: dict[str, dict[tuple[str, str], float]] = defaultdict(dict)

    p = os.path.join(RESULTS, "pointwise.jsonl")
    if os.path.exists(p):
        for line in open(p):
            r = json.loads(line)
            if r["score"] is None:
                continue
            out[r["judge"]][(r["item_id"], r["system"])] = (r["score"] - 1.0) / 9.0

    p = os.path.join(RESULTS, "pairwise.jsonl")
    if os.path.exists(p):
        acc: dict[str, dict[tuple[str, str], list[int]]] = defaultdict(lambda: defaultdict(list))
        for line in open(p):
            r = json.loads(line)
            if r["cand_win"] is None:
                continue
            acc[r["judge"]][(r["item_id"], r["system"])].append(r["cand_win"])
        for j, d in acc.items():
            for key, wins in d.items():
                out[j][key] = float(np.mean(wins))
            # the anchor never competes against itself; by definition its win rate is 0.5
            for it in {k[0] for k in d}:
                out[j][(it, ANCHOR)] = 0.5
    return dict(out)


def system_means(scores: dict[tuple[str, str], float], items: list[str]) -> dict[str, float]:
    """Mean judge score per system, over the given item set."""
    agg: dict[str, list[float]] = defaultdict(list)
    for (it, s), v in scores.items():
        if it in items:
            agg[s].append(v)
    return {s: float(np.mean(v)) for s, v in agg.items()}


# ------------------------------------------------------------------ fidelity
def sra(sys_scores: dict[str, float], population: list[str]) -> float:
    """System Ranking Accuracy: over all *comparable* system pairs in the population
    (those whose true qualities differ), the fraction the judge orders correctly.
    Judge ties score 0.5. This is the quantity a leaderboard user actually cares about."""
    pop = [s for s in population if s in sys_scores]
    tot, ok = 0.0, 0.0
    for a, b in itertools.combinations(pop, 2):
        qa, qb = true_quality(int(a[1])), true_quality(int(b[1]))
        if qa == qb:
            continue
        tot += 1
        da, db = sys_scores[a], sys_scores[b]
        if da == db:
            ok += 0.5
        elif (da > db) == (qa > qb):
            ok += 1
    return ok / tot if tot else float("nan")


def kendall_fidelity(sys_scores: dict[str, float], population: list[str]) -> float:
    pop = [s for s in population if s in sys_scores]
    q = [true_quality(int(s[1])) for s in pop]
    z = [sys_scores[s] for s in pop]
    if len(set(q)) < 2:
        return float("nan")
    return float(stats.kendalltau(q, z, variant="b").statistic)


# ------------------------------------------------------------------ populations
def homogeneous_populations(styles: list[str] | None = None) -> dict[str, list[str]]:
    return {f"all-{st}": [f"k{k}_{st}" for k in KS] for st in (styles or STYLES)}


def all_style_assignments(styles: list[str] | None = None
                          ) -> list[tuple[tuple[str, ...], list[str]]]:
    """The 3^5 = 243 populations that contain exactly one system per quality level.

    Every one of these has the SAME true ranking (k=0 > 1 > 2 > 3 > 4). They differ only
    in which quality-preserving style each level is rendered in. So any variation in a
    judge's fidelity across them is caused entirely by judge error, never by the task."""
    out = []
    for combo in itertools.product(styles or STYLES, repeat=len(KS)):
        pop = [f"k{k}_{st}" for k, st in zip(KS, combo)]
        out.append((combo, pop))
    return out


# ------------------------------------------------------------------ decomposition
def anova_decomposition(sys_scores: dict[str, float],
                        styles: list[str] | None = None) -> dict[str, float]:
    """Two-way ANOVA on the cell means of the balanced quality x style grid.

    Returns sums of squares and the validity ratio
        V = SS_quality / (SS_quality + SS_style + SS_inter),
    i.e. the share of a judge's between-system variance that reflects real quality
    differences rather than reaction to quality-preserving surface form.

    `styles` restricts the transformation family. Passing ["plain", "polished"] gives the
    length-matched family, used to show the results do not hinge on the verbose condition
    (whose quality-preservation a reader might reasonably dispute)."""
    STYLES = styles or globals()["STYLES"]
    M = np.array([[sys_scores[f"k{k}_{st}"] for st in STYLES] for k in KS])
    grand = M.mean()
    row = M.mean(axis=1)     # quality marginals
    col = M.mean(axis=0)     # style marginals
    nk, ns = M.shape
    ss_q = ns * float(((row - grand) ** 2).sum())
    ss_s = nk * float(((col - grand) ** 2).sum())
    pred = grand + (row[:, None] - grand) + (col[None, :] - grand)
    ss_i = float(((M - pred) ** 2).sum())
    tot = ss_q + ss_s + ss_i
    return {
        "ss_quality": ss_q, "ss_style": ss_s, "ss_inter": ss_i,
        "validity_ratio": ss_q / tot if tot > 0 else float("nan"),
        "quality_range": float(row.max() - row.min()),
        "style_range": float(col.max() - col.min()),
        "style_pref": {st: float(c) for st, c in zip(STYLES, col)},
        "quality_slope": float(np.polyfit([true_quality(k) for k in KS], row, 1)[0]),
    }


# ------------------------------------------------------------------ L2 protocols
def protocol_scores(scores: dict[tuple[str, str], float], items: list[str],
                    population: list[str],
                    styles: list[str] | None = None) -> dict[str, float]:
    """Compute every level-2 meta-evaluation protocol's score for one judge, using only
    data from `population` (the 'development' systems) and `items`.

    Gold-label protocols (P1-P3) use the true quality of the dev systems.
    Label-free protocols (P4*) use only the knowledge that the style transform preserves
    quality and that increasing k degrades it -- properties of the *transformations*,
    which require no annotation of any system's outputs.

    `styles` restricts the perturbation family (see anova_decomposition)."""
    STYLES = styles or globals()["STYLES"]
    pop = set(population)

    # ---- P1: pooled item-level pairwise agreement with gold. The standard meta-eval
    # metric (MT-Bench / RewardBench style): show the judge two answers to the same
    # question with different true quality, ask which it prefers, score agreement.
    ok, tot = 0.0, 0.0
    for it in items:
        cells = [(s, scores.get((it, s))) for s in pop]
        cells = [(s, v) for s, v in cells if v is not None]
        for (a, va), (b, vb) in itertools.combinations(cells, 2):
            qa, qb = true_quality(int(a[1])), true_quality(int(b[1]))
            if qa == qb:
                continue
            tot += 1
            if va == vb:
                ok += 0.5
            elif (va > vb) == (qa > qb):
                ok += 1
    p1 = ok / tot if tot else float("nan")

    # ---- P2: pooled item-level Spearman between judge score and true quality.
    xs, ys = [], []
    for it in items:
        for s in pop:
            v = scores.get((it, s))
            if v is not None:
                xs.append(true_quality(int(s[1])))
                ys.append(v)
    p2 = float(stats.spearmanr(xs, ys).statistic) if len(set(ys)) > 1 else 0.0

    # ---- P3: system-level fidelity on the dev population (gold labels needed).
    sm = system_means({k: v for k, v in scores.items() if k[1] in pop}, items)
    p3 = sra(sm, population)

    # ---- P4a: style sensitivity. LABEL-FREE. For each item and quality level present in
    # the dev population, the spread of judge scores across the three quality-preserving
    # restylings of identical content. Any spread is judge error, by construction.
    spreads = []
    ks_in_pop = sorted({int(s[1]) for s in pop})
    for it in items:
        for k in ks_in_pop:
            vals = [scores.get((it, f"k{k}_{st}")) for st in STYLES]
            vals = [v for v in vals if v is not None]
            if len(vals) == len(STYLES):
                spreads.append(max(vals) - min(vals))
    p4_style = float(np.mean(spreads)) if spreads else float("nan")

    # ---- P4b: system-level style bias B. LABEL-FREE. How far a *system score* moves
    # when the system's outputs are restyled. This is the quantity the certificate uses.
    per_style = {}
    for st in STYLES:
        vals = []
        for k in ks_in_pop:
            v = [scores.get((it, f"k{k}_{st}")) for it in items]
            v = [x for x in v if x is not None]
            if v:
                vals.append(np.mean(v))
        per_style[st] = float(np.mean(vals)) if vals else float("nan")
    p4_sysbias = float(max(per_style.values()) - min(per_style.values()))

    # ---- P4c: separation-to-bias ratio. LABEL-FREE. Judge score spread across the
    # systems under test, divided by the style bias. Large = rankings are trustworthy.
    seps = [np.mean([scores[(it, s)] for it in items if (it, s) in scores]) for s in pop]
    separation = float(max(seps) - min(seps)) if seps else 0.0
    p4_ratio = separation / p4_sysbias if p4_sysbias > 1e-9 else float("inf")

    # ---- P4d: degradation monotonicity. Uses only the construction-known fact that
    # corrupting more claims cannot improve an answer. No quality labels.
    ok_m, tot_m = 0.0, 0.0
    for it in items:
        for st in STYLES:
            for ka, kb in itertools.combinations(ks_in_pop, 2):
                va = scores.get((it, f"k{ka}_{st}"))
                vb = scores.get((it, f"k{kb}_{st}"))
                if va is None or vb is None:
                    continue
                tot_m += 1
                ok_m += 1.0 if va > vb else (0.5 if va == vb else 0.0)
    p4_mono = ok_m / tot_m if tot_m else float("nan")

    return {
        "P1_pair_acc": p1, "P2_item_rho": p2, "P3_dev_sra": p3,
        "P4a_style_spread": p4_style, "P4b_style_bias": p4_sysbias,
        "P4c_sep_over_bias": p4_ratio, "P4d_monotonicity": p4_mono,
        "separation": separation,
    }


# ------------------------------------------------------------------ certificate
def certificate(sys_scores: dict[str, float], style_bias: float,
                population: list[str]) -> dict[str, float]:
    """Perturbation certificate. Declare the ordering of a pair certified iff the judge
    score gap exceeds the label-free bias bound. Report coverage and correctness."""
    pop = [s for s in population if s in sys_scores]
    cert, cert_ok, tot, tot_ok = 0, 0, 0, 0
    for a, b in itertools.combinations(pop, 2):
        qa, qb = true_quality(int(a[1])), true_quality(int(b[1]))
        if qa == qb:
            continue
        tot += 1
        correct = (sys_scores[a] > sys_scores[b]) == (qa > qb)
        tot_ok += int(correct)
        if abs(sys_scores[a] - sys_scores[b]) > style_bias:
            cert += 1
            cert_ok += int(correct)
    return {
        "n_pairs": tot, "uncert_acc": tot_ok / tot if tot else float("nan"),
        "n_certified": cert, "coverage": cert / tot if tot else float("nan"),
        "certified_acc": cert_ok / cert if cert else float("nan"),
    }
