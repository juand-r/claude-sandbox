"""Enumerate FRONT terminations of the E^n crystal: (15,-4)-periodic rows
   ether(phi) | D (unknown, cells [c0 - wD, c0)) | rod crystal (bg, x >= c0)
by incremental SAT with blocking. The standard E^n front is one of them.
Each solution is checked periodic by exact simulation and deduplicated
up to crystal translations k*u, u = (5,2) (a front moved by k units).
Usage: python fronts.py wD c0 [N] -> fronts_wD_c0.jsonl"""
import sys
import json
sys.dont_write_bytecode = True
import numpy as np
from rod import TILE, ether_bit, simulate, SYNTH  # noqa
from pert import BG, Pert
from r110sat import CNF  # noqa

P_T, P_X = 15, -4


def enum_fronts(bg, wD, c0, phi, maxn=10000):
    cnf = CNF()
    T = P_T
    ulo, uhi = c0 - wD, c0
    init_const = lambda x: ether_bit(phi, 0, x) if x < ulo else bg(0, x)
    P = Pert(cnf, T, ulo, uhi, init_const, lambda t, x: ether_bit(phi, t, x),
             lambda t, x: bg(t, x), lambda t: (ulo - t, uhi + t))
    for x in range(ulo - T - 2, uhi + T + 2):
        cnf.equal(P.lit(T, x + P_X), P.lit(0, x))
    s = cnf.solver()
    sols = []
    while len(sols) < maxn and s.solve():
        m = set(l for l in s.get_model() if l > 0)
        row = [int(P.lit(0, x) in m) for x in range(ulo, uhi)]
        sols.append(row)
        s.add_clause([-P.lit(0, x) if row[i] else P.lit(0, x) for i, x in enumerate(range(ulo, uhi))])
    s.delete()
    return sols


def full_row(bg, row, ulo, phi, lo, hi):
    return np.array([ether_bit(phi, 0, x) if x < ulo else
                     (row[x - ulo] if x < ulo + len(row) else bg(0, x)) for x in range(lo, hi)], np.uint8)


if __name__ == "__main__":
    wD, c0 = int(sys.argv[1]), int(sys.argv[2])
    N = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    bg = BG(N, 200, -400, 400)
    lo, hi = -300, 300
    found = []
    for phi in range(TILE):
        for row in enum_fronts(bg, wD, c0, phi):
            r0 = full_row(bg, row, c0 - wD, phi, lo, hi)
            h = simulate(r0, 2 * P_T)
            a, b = 2 * P_T + 5, len(r0) - 2 * P_T - 5
            ok = np.array_equal(h[P_T, a + P_X:b + P_X], h[0, a:b])
            assert ok, "front not periodic"
            # first non-ether cell
            f = next(x for x in range(lo, hi) if r0[x - lo] != ether_bit(phi, 0, x))
            found.append(dict(phi=phi, row="".join(map(str, row)), first=f, h=h))
    # dedupe up to k*u shifts: compare spacetime rows 0..14 over the
    # region [first-5, c0+40) with the other shifted by (5k, 2k)
    types = []
    for fr in found:
        h = fr["h"]
        dup = False
        for ty in types:
            g = ty["h"]
            for k in range(-6, 7):
                dt, dx = 5 * k, 2 * k
                # compare h(t, x) with g(t - dt, x - dx) for t in [20, 30)
                same = True
                for t in range(P_T + 5, 2 * P_T):
                    tt = t - dt
                    while tt < 0:
                        tt += P_T; dx2 = dx  # noqa
                    tq, xs = tt, 0
                    # move along the period: (tt) -> reduce to [0, 2P) keeping x offset
                    q = 0
                    while tq >= 2 * P_T:
                        tq -= P_T; q += 1
                    while tq < 0:
                        tq += P_T; q -= 1
                    shift = dx + q * (-P_X) * 0
                    xa = range(fr["first"] - 10 - lo, c0 + 30 - lo)
                    # g at (tq, x - dx - q*P_X) since g(t) = g(t - P_T) shifted
                    for xi in xa:
                        xg = xi - dx + q * P_X * -1
                        if not (0 <= xg < g.shape[1]) or h[t, xi] != g[tq, xg]:
                            same = False
                            break
                    if not same:
                        break
                if same:
                    dup = True
                    break
            if dup:
                break
        if not dup:
            types.append(fr)
    with open(f"fronts_{wD}_{c0}.jsonl", "w") as fh:
        for ty in types:
            fh.write(json.dumps(dict(phi=ty["phi"], row=ty["row"], first=ty["first"], wD=wD, c0=c0, N=N)) + "\n")
    print("solutions", len(found), "types", len(types))
    for ty in types:
        print(ty["phi"], ty["first"], ty["row"])
