"""A-bursts: R2 = E held at zero by a blind left stream of Z_L's (one A
per Z_L), R1 = E^(v1+1) to the right (input prefix, no right program).
Does every A of the burst DEC R1 cleanly (same class)? Scan the left
stream's packet spacing (time, steps). Glider level, then exact CA for
the hits. Usage: python burst.py [v1] [Lmax]"""
from dl import *  # noqa
import sys

GAP = 1200


def scene(v1, L, sp, r2t0=0):
    pre = input_prefix(v1)
    r2 = ("E",) + place_left_of(pre, "E", -GAP, r2t0)
    t0 = 7000 * (v1 + 1) + 2000
    ls = left_stream("z" * L, r2[1:], t0=t0, gap=sp)
    T = t0 + sp * L + 15 * 3000
    return ls + [r2] + pre, T


def outcome(st):
    es = [g for g in st if g[0] in CHAIN]
    if len(es) != 2 or len(st) != 2:
        return None
    a, b = sorted(es, key=lambda g: pos(g, 0))
    return CHAIN.index(a[0]), CHAIN.index(b[0])


if __name__ == "__main__":
    v1 = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    Lmax = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    for r2t0 in (0, 1, 2):
        for sp in range(120, 400, 15):
            res = []
            for L in range(1, Lmax + 1):
                sc, T = scene(v1, L, sp, r2t0)
                sim, err = run(sc, T)
                res.append(outcome(sim.state()) if err is None else "3body")
            good = all(r == (0, v1 - L) for r in res)
            print(f"r2t0={r2t0} sp={sp} good={good} {res}", flush=True)
