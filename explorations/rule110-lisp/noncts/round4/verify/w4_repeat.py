"""W4 repetition: a right stream of N identical blocks (Bbar + k B's at
spacing s; block period P cells) on a rod E^m. For each block period P and
each Bbar class of the FIRST block, the value after N blocks (rodval, clean
rod in the whole light cone) for N = 1..NMAX, i.e. the per-block value
changes. A 'mode' = a P where the per-block change is constant in a class.
python3 w4_repeat.py k s m NMAX P1 P2 [step]"""
import sys

import hrun
import rodval

vlib = hrun.vlib


def run(m, t0, k, s, P, N, d0=60, dT=0):
    items = [(f"E^{m}", 0, 0)]
    for j in range(N):
        b = d0 + j * P
        items.append(("Bbar", t0 + j * dT, b))
        items += [("B", 0, b + 30 + s * (i + 1)) for i in range(k)]
    row, org, placed = vlib.build(items, pad=400)
    T = (d0 + N * P + 30 + s * k) * 30 // 7 + 1500   # B-speed blocks close on the rod at 1/2 - 4/15 = 7/30
    return rodval.value(row, org, T), placed


if __name__ == "__main__":
    k, s, m, NMAX, P1, P2 = map(int, sys.argv[1:7])
    step = int(sys.argv[7]) if len(sys.argv) > 7 else 2
    for P in range(P1, P2 + 1, step):
        for dT in range(12):
            line = []
            for t0 in (0, 1, 2):
                vals = [m]
                for N in range(1, NMAX + 1):
                    v, placed = run(m, t0, k, s, P, N, dT=dT)
                    vals.append(v)
                    if v is None:
                        break
                d = [None if (a is None or b is None) else b - a for a, b in zip(vals, vals[1:])]
                line.append(d)
            # block-to-block seed vector actually placed (after snapping)
            bb = [q for q in placed if q[0] == "Bbar"]
            V = (bb[1][1] - bb[0][1], bb[1][2] - bb[0][2]) if len(bb) > 1 else None
            print(f"P={P} dT={dT} V={V}: per-block changes, first block t0 = 0,1,2: {line}", flush=True)
