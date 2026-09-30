"""Exactness check for the YB wiring layer: the final seed event of every
glider must equal its initial seed plus the sum of its single-crossing
displacements (one per partner it crossed), independently of the order of
the crossings. Also runs the project's glider census (../../census.py) on
the final row to check every defect is a single typed glider."""
import sys
import numpy as np
sys.path.insert(0, "../..")
from census import census, MAX_DT
from m1_yb import design, build, M, kMF, kFS, kMS
from yb import disp
from rx import *


def norm_seed(name, t0, x0):
    g = G[name]
    q, r = divmod(t0, g.p)
    return (r, x0 - q * g.d)


def predicted(pl):
    cF, fC = disp(M, "F", kMF)
    fE, eF = disp("F", "Ebar", kFS)
    cE, eC = disp(M, "Ebar", kMS)
    nF = sum(1 for p in pl if p[0] == "F")
    nE = sum(1 for p in pl if p[0] == "Ebar")
    out = []
    for n, t, x in pl:
        if n == M:
            d = (nF * cF[0] + nE * cE[0], nF * cF[1] + nE * cE[1])
        elif n == "F":
            d = (fC[0] + nE * fE[0], fC[1] + nE * fE[1])
        else:
            d = (eC[0] + nF * eF[0], eC[1] + nF * eF[1])
        out.append((n,) + norm_seed(n, t + d[0], x + d[1]))
    return sorted(out)


if __name__ == "__main__":
    Gv, S = design()
    for a in [0, 20, 38]:
        pl = build(Gv, S, a)
        got = sorted((n,) + norm_seed(n, t, x) for n, t, x in run(pl, 12000))
        exp = predicted(pl)
        print("a", a, "exact match" if got == exp else f"MISMATCH\n{got}\n{exp}")
    # census on the final row of one run
    H, x0 = history(build(Gv, S, 20), 9000)
    assert 9000 > 36 + MAX_DT
    cs = census(H[-(MAX_DT + 1):])
    kinds = sorted(k for _, _, k in cs)
    print("census kinds at t=9000:", {k: kinds.count(k) for k in set(kinds)})
    # census.py knows only C, A, E families; check the '?' defects are F's:
    # invariant under F's period (36, -4)
    last, then = H[-1], H[-1 - 36]
    for a_, b_, k in cs:
        if k == "?":
            lo, hi = a_ - 2, b_ + 2
            assert np.array_equal(last[lo:hi], then[lo + 4:hi + 4]), (a_, b_)
    print("all '?' defects are (36,-4)-invariant (F gliders)")
