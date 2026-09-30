"""SAT enumeration of Rule 110 gliders (periodic defects in ether).

A glider with period (P, D) satisfies cell(t + P, x + D) = cell(t, x) on
the whole line. Ether must be invariant under the same shift on both sides,
so (P, D) lies in the ether lattice: 4P + D == 0 (mod 14).

For each (P, D) and width W we ask: is there a row, ether(phase 0) left of
0, unknown on [0, W), ether(phase pR, solver's choice) right of W, that
reappears shifted by D after P steps, and is not pure ether? Solutions are
blocked together with all their time phases and admissible translates, so
each hit is a new periodic defect (possibly a bundle of gliders, or a
longer-period multiple of a smaller glider: flagged in post-processing).

Each hit is verified by forward simulation with ../../engine.py.

Usage: python gliders.py PMAX W [MAXPER]
"""

import json
import sys
import time

import numpy as np

from r110sat import Model, ether_bit, run_embedded, TILE


def lattice_points(pmax, pmin=1):
    for P in range(pmin, pmax + 1):
        for D in range(-P, P + 1):
            if (4 * P + D) % TILE == 0:
                yield P, D


def defect_extent(row, x0, lp, rp, t):
    """First x differing from left ether, last+1 x differing from right
    ether (row[i] = cell x0 + i at time t)."""
    xs = np.arange(x0, x0 + len(row))
    le = np.array([ether_bit(lp, t, x) for x in xs])
    re = np.array([ether_bit(rp, t, x) for x in xs])
    dl = np.nonzero(row != le)[0]
    dr = np.nonzero(row != re)[0]
    a = x0 + (dl[0] if len(dl) else len(row))
    b = x0 + (dr[-1] + 1 if len(dr) else 0)
    return int(a), int(b)


def orbit(seg, pR, P, D, W):
    """Simulate the found segment for P steps; verify periodicity; return
    the list of rows (as dicts) needed for blocking and canonical form."""
    hist, x0 = run_embedded(seg, 0, 0, pR, 2 * P, margin=W)
    n = hist.shape[1]
    # verify (P, D) periodicity away from the seams
    lo = 2 * P + W + 5
    hi = n - lo
    for t in range(P + 1):
        a = hist[t + P, lo + D:hi + D] if D >= 0 else hist[t + P, lo + D:hi + D]
        b = hist[t, lo:hi]
        if not np.array_equal(a, b):
            raise AssertionError("SAT glider is not periodic in simulation")
    rows = []
    for tau in range(P):
        row = hist[tau]
        a, b = defect_extent(row[lo:hi], x0 + lo, 0, pR, tau)
        rows.append((tau, row, a, b))
    return hist, x0, rows


def placements(rows, x0, pR, W):
    """All row0 patterns on [0, W) (left phase 0) equivalent to the glider."""
    out = []
    for tau, row, a, b in rows:
        # shift s must satisfy s == 4 tau (mod 14), a + s >= 0, b + s <= W
        s = -a + ((4 * tau + a) % TILE)          # smallest s>=-a, s==4tau mod14
        while b + s <= W:
            if a + s >= 0:
                seg = row[0 - s - x0: W - s - x0]
                out.append(seg.copy())
            s += TILE
    return out


def canonical(rows, x0, pR):
    best = None
    for tau, row, a, b in rows:
        if b <= a:
            seg = ""
            key = (0, "", tau)
        else:
            s = -a + ((4 * tau + a) % TILE)
            seg = "".join(map(str, row[a - x0: b - x0]))
            key = (b - a, seg)
        best = key if best is None or key[:2] < best[:2] else best
    return best


def minimal_period(hist, P, D, lo, hi):
    """Smallest (p, d) with p | P, d = D p / P reproducing the rows."""
    for p in range(1, P + 1):
        if P % p or (D * p) % P:
            continue
        d = D * p // P
        if all(np.array_equal(hist[t + p, lo + d:hi + d], hist[t, lo:hi])
               for t in range(P)):
            return p, d
    return P, D


def n_clusters(hist, x0, P, W):
    """Max over one period of the number of census clusters (defect regions
    separated by ether) in the glider's rows."""
    sys.path.insert(0, "../..")
    from census import clusters
    lo = 2 * P + W + 5
    return max(len(clusters(hist[t, lo:hist.shape[1] - lo])) for t in range(P))


def xor_var(m, a, b):
    """Fresh var v <-> (a xor b); a, b literals or constants."""
    N = m.neg
    v = m.new_var()
    m.add([-v, a, b])
    m.add([-v, N(a), N(b)])
    m.add([v, N(a), b])
    m.add([v, a, N(b)])
    return v


def forbid_subperiods(m, P, D, W):
    """Require that (P, D) is the minimal period: for every proper p | P
    with d = D p / P integral and (p, d) in the ether lattice, some cell of
    row p differs from row 0 shifted by d."""
    for p in range(1, P):
        if P % p or (D * p) % P:
            continue
        d = D * p // P
        if (4 * p + d) % TILE:
            continue
        m.add([xor_var(m, m.lit(p, x), m.lit(0, x - d))
               for x in range(-p, W + p)])


BUDGET = 200000      # conflicts per SAT call; exceeded -> UNKNOWN
UNKNOWN = []


def search(P, D, wmax, maxper=40):
    """Incremental in width: at width W only gliders that do not fit in a
    smaller width appear (earlier ones are blocked in all placements)."""
    found = []
    for W in range(1, wmax + 1):
        m = Model(P, 0, W, left_phase=0, right_phase=None)
        for x in range(-P, W + P):
            m.equal(m.lit(P, x), m.lit(0, x - D))
        m.add([-m.sel[0]] + [m.neg(m.lit(0, x)) if ether_bit(0, 0, x)
                             else m.lit(0, x) for x in range(W)])
        forbid_subperiods(m, P, D, W)

        def block(s, rows, x0, pR):
            for pat in placements(rows, x0, pR, W):
                cl = [-m.sel[pR]]
                for x in range(W):
                    l = m.lit(0, x)
                    cl.append(-l if pat[x] else l)
                s.add_clause(cl)

        with m.solver() as s:
            for g in found:
                block(s, g["_rows"], g["_x0"], g["pR"])
            while len(found) < maxper:
                s.conf_budget(BUDGET)
                r = s.solve_limited()
                if r is None:
                    UNKNOWN.append((P, D, W))
                    print(f"    UNKNOWN (budget) at P={P} D={D} W={W}",
                          flush=True)
                    break
                if not r:
                    break
                model = set(l for l in s.get_model() if l > 0)
                seg = np.array([int(m.lit(0, x) in model) for x in range(W)],
                               dtype=np.uint8)
                pR = [k for k in range(TILE) if m.sel[k] in model][0]
                hist, x0, rows = orbit(seg, pR, P, D, W)
                lo = 2 * P + W + 5
                p, d = minimal_period(hist, P, D, lo, hist.shape[1] - lo)
                can = canonical(rows, x0, pR)
                found.append({"P": P, "D": D, "pR": pR, "minP": p, "minD": d,
                              "width": can[0], "pattern": can[1], "W": W,
                              "clusters": n_clusters(hist, x0, P, W),
                              "_rows": rows, "_x0": x0})
                block(s, rows, x0, pR)
        if len(found) >= maxper:
            return found, True
    return found, False


if __name__ == "__main__":
    PMAX, W = int(sys.argv[1]), int(sys.argv[2])
    PMIN = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    MAXPER = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    allg = []
    for P, D in lattice_points(PMAX, PMIN):
        t0 = time.time()
        f, trunc = search(P, D, W, MAXPER)
        prim = [g for g in f if (g["minP"], g["minD"]) == (P, D)]
        if f:
            print(f"(P={P:3d}, D={D:4d}) found {len(f):3d} "
                  f"primitive {len(prim):3d}{' TRUNCATED' if trunc else ''} "
                  f"[{time.time()-t0:.1f}s]", flush=True)
            for g in prim:
                print(f"    W={g['W']:3d} w={g['width']:3d} pR={g['pR']:2d} "
                      f"clusters={g['clusters']} {g['pattern']}", flush=True)
        allg.extend({k: v for k, v in g.items() if not k.startswith("_")}
                    for g in f)
    with open(f"gliders_P{PMIN}-{PMAX}_W{W}.json", "w") as fh:
        json.dump({"gliders": allg, "unknown": UNKNOWN}, fh)
    print("UNKNOWN (budget exceeded):", UNKNOWN)
