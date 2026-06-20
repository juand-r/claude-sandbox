"""Analysis of a recorded Ring System run.

Computes the discriminating metrics from RESEARCH_PLAN.md section 3 --- the
ones that separate genuine self-organization from high-entropy churn ---
from a history .npz (bits, occ, ids, births).

Usage:
    python3 analyze.py out/history.npz
"""

from __future__ import annotations

import sys
import zlib

import numpy as np

import ring_system as rs


def _genotype_keys(bits_t, occ_t):
    """Bytes key per occupied ring at one tick (packed 36-bit genome)."""
    rows = bits_t[occ_t]
    if rows.shape[0] == 0:
        return []
    packed = np.packbits(rows, axis=1)
    return [r.tobytes() for r in packed]


# -- metrics ---------------------------------------------------------------

def turnover(occ, births):
    """Mean turnover = (births+deaths)/pop per tick, over the run."""
    T = occ.shape[0]
    pop = occ.sum(axis=1)
    b = np.zeros(T, dtype=float)
    if births.shape[0]:
        for t in births[:, 0]:
            if 0 <= t < T:
                b[t] += 1
    # deaths[t] = pop[t-1] + births[t] - pop[t]
    d = np.zeros(T, dtype=float)
    d[1:] = pop[:-1] + b[1:] - pop[1:]
    with np.errstate(divide="ignore", invalid="ignore"):
        rate = np.where(pop > 0, (b + d) / pop, 0.0)
    return float(np.mean(rate[1:])), float(np.mean(pop[1:]))


def concentration(bits, occ):
    """Mean over ticks of the largest genotype's population share."""
    T = occ.shape[0]
    shares = []
    for t in range(T):
        keys = _genotype_keys(bits[t], occ[t])
        if not keys:
            continue
        counts = {}
        for k in keys:
            counts[k] = counts.get(k, 0) + 1
        shares.append(max(counts.values()) / len(keys))
    return float(np.mean(shares)) if shares else 0.0


def persistence(bits, occ):
    """Longest consecutive-tick run for any genotype, and #genotypes that
    persist > 5 and > 20 ticks."""
    T = occ.shape[0]
    cur = {}      # key -> current run length
    best = {}     # key -> best run length
    prev = set()
    for t in range(T):
        keys = set(_genotype_keys(bits[t], occ[t]))
        for k in keys:
            cur[k] = cur[k] + 1 if k in prev else 1
            if cur[k] > best.get(k, 0):
                best[k] = cur[k]
        for k in prev - keys:
            cur[k] = 0
        prev = keys
    if not best:
        return 0, 0, 0
    vals = np.array(list(best.values()))
    return int(vals.max()), int((vals > 5).sum()), int((vals > 20).sum())


def compressibility(bits, occ, ticks, rng):
    """gzip size of the living population / gzip size of a same-shape random
    matrix, averaged over the given ticks. < 1 means structure."""
    ratios = []
    for t in ticks:
        rows = bits[t][occ[t]]
        if rows.shape[0] < 2:
            continue
        real = len(zlib.compress(np.packbits(rows, axis=1).tobytes(), 9))
        rand = rng.integers(0, 2, size=rows.shape, dtype=np.uint8)
        ref = len(zlib.compress(np.packbits(rand, axis=1).tobytes(), 9))
        ratios.append(real / ref)
    return float(np.mean(ratios)) if ratios else float("nan")


def _on_cycle_fraction(targets, nodes):
    """Fraction of nodes lying on a directed cycle of a functional graph
    (each node has at most one out-edge given by targets[node] or None)."""
    state = {}      # 0 visiting, 1 done
    on_cycle = set()
    for start in nodes:
        if start in state:
            continue
        path = []
        node = start
        while node is not None and node not in state:
            state[node] = 0
            path.append(node)
            node = targets.get(node)
        if node is not None and state.get(node) == 0:
            # found a new cycle: from `node` to the end of path
            i = path.index(node)
            for c in path[i:]:
                on_cycle.add(c)
        for n in path:
            state[n] = 1
    return len(on_cycle) / len(nodes) if nodes else 0.0


def graph_stats(bits, occ, tick):
    """Push-graph in-degree and cycle structure at one tick, with a
    random functional-graph null for comparison."""
    o = occ[tick]
    nodes = list(np.where(o)[0])
    if len(nodes) < 2:
        return None
    push = rs.get_field(bits[tick], rs.PUSH)
    targets = {}
    indeg = {n: 0 for n in nodes}
    for s in nodes:
        t = int(push[s])
        if t < o.shape[0] and o[t]:
            targets[s] = t
            indeg[t] += 1
    deg = np.array(list(indeg.values()))
    real = dict(max_indeg=int(deg.max()), frac_indeg0=float((deg == 0).mean()),
                frac_on_cycle=_on_cycle_fraction(targets, nodes))
    # random null: each node points to a uniformly random node
    rng = np.random.default_rng(0)
    nn = len(nodes); idx = {n: i for i, n in enumerate(nodes)}
    null_max, null0, nullc = [], [], []
    for _ in range(20):
        tg = {}; ind = np.zeros(nn, dtype=int)
        tgt = rng.integers(0, nn, size=nn)
        for i, n in enumerate(nodes):
            tg[n] = nodes[tgt[i]]; ind[tgt[i]] += 1
        null_max.append(ind.max()); null0.append((ind == 0).mean())
        nullc.append(_on_cycle_fraction(tg, nodes))
    null = dict(max_indeg=float(np.mean(null_max)),
                frac_indeg0=float(np.mean(null0)),
                frac_on_cycle=float(np.mean(nullc)))
    return real, null


def lineage_stats(occ, ids, births):
    """Founder concentration: at the final tick, share of the population
    descending from the single most successful founder."""
    if births.shape[0] == 0:
        return None
    parent = {int(c): int(p) for _, c, p in births}

    def founder(i):
        seen = 0
        while i in parent and parent[i] != 0 and seen < 10000:
            i = parent[i]; seen += 1
        return i

    final = ids[-1][occ[-1]]
    if final.size == 0:
        return dict(founder_share=0.0, n_founders=0)
    counts = {}
    for i in final:
        f = founder(int(i))
        counts[f] = counts.get(f, 0) + 1
    top = max(counts.values()) / final.size
    return dict(founder_share=float(top), n_founders=len(counts))


def key_share_series(bits, occ, span, code):
    """Per-tick fraction of living rings whose key (field `span`) == code.
    The direct selection signal for the H2 trigger experiment."""
    lo, hi = span
    weights = 1 << np.arange(hi - lo - 1, -1, -1)
    out = []
    for t in range(occ.shape[0]):
        o = occ[t]
        if not o.any():
            out.append(0.0); continue
        keys = bits[t][o][:, lo:hi] @ weights
        out.append(float((keys == code).mean()))
    return np.array(out)


def spatial_moran(bits, occ, tick, side, span=rs.RULE):
    """Moran's I of a field over the torus grid at one tick (occupied slots,
    Moore neighbours). >0 = spatial clustering, ~0 = no structure."""
    o = occ[tick]
    idx = np.where(o)[0]
    if len(idx) < 3:
        return float("nan")
    vals = rs.get_field(bits[tick], span).astype(float)
    xbar = vals[o].mean()
    num = 0.0; W = 0
    for s in idx:
        x, y = s % side, s // side
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                n = ((y + dy) % side) * side + (x + dx) % side
                if o[n]:
                    num += (vals[s] - xbar) * (vals[n] - xbar); W += 1
    den = ((vals[o] - xbar) ** 2).sum()
    if den == 0 or W == 0:
        return float("nan")
    return (len(idx) / W) * (num / den)


def self_preservation_series(bits, occ, ticks=None):
    """Mean fraction of bits each occupied ring leaves unchanged under its own
    rule, per tick. The emergent-selection signal for self-templating (E6)."""
    T = occ.shape[0]
    ticks = ticks if ticks is not None else range(T)
    out = []
    for t in ticks:
        o = occ[t]; idx = np.where(o)[0]
        if len(idx) == 0:
            out.append(float("nan")); continue
        rules = rs.get_field(bits[t], rs.RULE)
        tot = 0.0
        for s in idx:
            pred = rs.apply_rule(int(rules[s]), bits[t][s])
            tot += np.mean(pred == bits[t][s])
        out.append(tot / len(idx))
    return np.array(out)


def summarize(path, label=None):
    d = np.load(path)
    bits, occ = d["bits"], d["occ"]
    ids = d["ids"] if "ids" in d else None
    births = d["births"] if "births" in d else np.zeros((0, 3), np.int64)
    T = occ.shape[0]
    rng = np.random.default_rng(0)
    sample_ticks = list(range(max(1, T - 50), T))   # last ~50 ticks

    turn, meanpop = turnover(occ, births)
    conc = concentration(bits, occ)
    pmax, p5, p20 = persistence(bits, occ)
    comp = compressibility(bits, occ, sample_ticks, rng)
    g = graph_stats(bits, occ, T - 1)
    side = int(round(occ.shape[1] ** 0.5))
    moran = (spatial_moran(bits, occ, T - 1, side)
             if side * side == occ.shape[1] else float("nan"))
    lin = lineage_stats(occ, ids, births) if ids is not None else None

    name = label or path
    print(f"\n=== {name} ===")
    print(f"  mean population        {meanpop:7.1f}")
    print(f"  mean turnover          {turn:7.3f}   (frac of pop replaced/tick)")
    print(f"  genotype concentration {conc:7.3f}   (top-genotype pop share)")
    print(f"  persistence (max run)  {pmax:7d}   ticks")
    print(f"  genotypes >5 / >20 tk  {p5:5d} / {p20:<5d}")
    print(f"  compressibility ratio  {comp:7.3f}   (<1 = structure vs random)")
    print(f"  spatial Moran's I      {moran:7.3f}   (>0 = spatial domains)")
    if g:
        real, null = g
        print(f"  push-graph  max in-deg {real['max_indeg']:4d}  "
              f"(null {null['max_indeg']:.1f})   "
              f"on-cycle {real['frac_on_cycle']:.3f} "
              f"(null {null['frac_on_cycle']:.3f})")
    if lin:
        print(f"  top-founder share      {lin['founder_share']:7.3f}   "
              f"({lin['n_founders']} founders alive)")
    return dict(meanpop=meanpop, turnover=turn, concentration=conc,
                persistence_max=pmax, compressibility=comp, moran=moran)


if __name__ == "__main__":
    for p in sys.argv[1:] or ["out/history.npz"]:
        summarize(p)
