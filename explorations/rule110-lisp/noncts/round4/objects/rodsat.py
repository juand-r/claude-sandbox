"""SAT: an extendable rod with interior background X moving with period (P, D):
ether (phase 0) | front | K tiles of X | back | ether (phase solver-chosen),
the whole row periodic: row P [x + D] == row 0 [x]. Every solution is
re-simulated, then lengthened by splicing extra X tiles (as E^n is spliced)
and checked stable for several lengths.
Usage: python3 rodsat.py TILE P D K WF WB"""
import sys
import numpy as np
from pysat.solvers import Solver
import cone
import objlib as O

ETHB = [int(c) for c in O.ETHER]


def eth(ph, t, x):
    return ETHB[(x + 4 * t + ph) % 14]


def rod_sat(tile, P, D, K, WF, WB, avoid=()):
    bg = cone.Background(tile)
    pX = bg.p
    W = WF + K * pX + WB
    # spacetime: t = 0..P, x in [-P-2, W+P+2) (light cone of the row); cells
    # outside [0, W) at t = 0 are ether: left phase 0, right phase rp (vars)
    nv = [0]
    def new():
        nv[0] += 1
        return nv[0]
    cl = []
    rsel = [new() for _ in range(14)]
    cl.append(rsel[:])
    for a in range(14):
        for b in range(a + 1, 14):
            cl.append([-rsel[a], -rsel[b]])
    lo, hi = -2 * P - 4, W + 2 * P + 4
    V = {}
    for t in range(P + 1):
        for x in range(lo + t, hi - t):
            V[(t, x)] = new()
    # t = 0 boundary: left ether phase 0 for x < 0; right ether phase rp
    for x in range(lo, 0):
        v = V[(0, x)]
        cl.append([v] if eth(0, 0, x) else [-v])
    for x in range(W, hi):
        v = V[(0, x)]
        for ph in range(14):
            cl.append([-rsel[ph], v] if eth(ph, 0, x) else [-rsel[ph], -v])
    for t in range(1, P + 1):
        for x in range(lo + t, hi - t):
            l, c, r, n = V[(t - 1, x - 1)], V[(t - 1, x)], V[(t - 1, x + 1)], V[(t, x)]
            cl += [[-n, c, r], [-n, -l, -c, -r], [-c, r, n], [c, -r, n], [l, -c, -r, n]]
    # periodicity on the object and a margin
    for x in range(-P, W + P):
        if (P, x + D) in V and (0, x) in V:
            a, b = V[(P, x + D)], V[(0, x)]
            cl += [[-a, b], [a, -b]]
    # interior: K tiles of X in some phase
    inds = []
    seen = []
    for tt in range(bg.tper):
        rr = bg.row_at(tt)
        for s in range(pX):
            pat = [int(rr[(i - s) % pX]) for i in range(K * pX)]
            if pat in seen:
                continue
            seen.append(pat)
            m = new()
            for i, b in enumerate(pat):
                v = V[(0, WF + i)]
                cl.append([-m, v] if b else [-m, -v])
            inds.append(m)
    cl.append(inds)
    for row in avoid:
        cl.append([(-V[(0, x)] if row[x] else V[(0, x)]) for x in range(W)])
    with Solver(name="cadical153", bootstrap_with=cl) as s:
        if not s.solve():
            return None
        M = set(l for l in s.get_model() if l > 0)
    row = np.array([1 if V[(0, x)] in M else 0 for x in range(W)], np.uint8)
    rp = [ph for ph in range(14) if rsel[ph] in M][0]
    return row, rp


def stable(row, rp, P, D, reps=3):
    """simulate the row embedded in ether; periodic with (P, D) for reps periods?"""
    W = len(row)
    pad = 2 * P * reps + 40
    full = np.concatenate([O.ether(0, -pad, 0), row, O.ether(rp, W, W + pad)])
    h = O.history(full, P * reps)
    for k in range(1, reps + 1):
        t = P * k
        for x in range(-P, W + P):
            # cell (t, x + k D) == cell (0, x)
            i_t = x + k * D - (-pad + t)
            i_0 = x + pad
            if h[t][i_t] != h[0][i_0]:
                return False
    return True


if __name__ == "__main__":
    tile, P, D, K, WF, WB = sys.argv[1], *map(int, sys.argv[2:7])
    res = rod_sat(tile, P, D, K, WF, WB)
    if res is None:
        print("UNSAT")
        sys.exit()
    row, rp = res
    s = "".join(map(str, row))
    print("rod", s, "right phase", rp, "stable", stable(row, rp, P, D))
    # splice: insert extra tiles (find a period of the tile inside)
    pX = len(tile)
    i = s.find(s[WF:WF + pX] * 2)
    per = s[WF:WF + pX]
    for j in (1, 2, 5, 10):
        s2 = s[:WF] + per * j + s[WF:]
        rp2 = (rp - pX * j) % 14
        r2 = np.array([int(c) for c in s2], np.uint8)
        print(" +", j, "tiles: stable", stable(r2, rp2, P, D))
