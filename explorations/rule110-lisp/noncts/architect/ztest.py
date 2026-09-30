"""Search for a zero-test mover for the crossing counter (xcounter.py).
Value n <-> D = (0,43) + n*(-24,12), gap 43 + 9.33 n. Candidates: movers
(single Ebar or catalog Ebar pairs, all classes vs T) that are predicted to
cross the register as an identity on D (D unchanged). Each is simulated
at n = 0, 1, 2. We want: n >= 1 exactly as predicted (identity), n = 0
something different and clean (a messenger, register intact or rebuilt)."""
import sys
from winding3 import movers, apply, cross, lateral
from rx import run, LIB
from m1_predict import norm_seed
from fractions import Fraction

U = (-24, 12)


def place(n, mv):
    T = (0, 0)
    D = (0 + n * U[0], 43 + n * U[1])
    P = (-D[0], -D[1])
    name, t, x = mv
    ev = (t + 10 * 36, x - 10 * 4)       # delay by 10 F periods (same class)
    return [("F",) + T, ("F",) + P, (name,) + ev], D


def outcome(n, mv):
    pl, D = place(n, mv)
    try:
        prods = run(pl, 5000)
    except RuntimeError as e:
        return None, "unsettled"
    return prods, None


if __name__ == "__main__":
    cands = [mv for mv in movers() if apply(mv, (0, 43)) == (0, 43)]
    print("identity candidates:", len(cands), flush=True)
    for mv in cands:
        p0, e0 = outcome(0, mv)
        p1, e1 = outcome(1, mv)
        f0 = sorted(norm_seed(*p) for p in p0 if p[0] == "F") if p0 else None
        f1 = sorted(norm_seed(*p) for p in p1 if p[0] == "F") if p1 else None
        n0 = sorted(p[0] for p in p0) if p0 else e0
        n1 = sorted(p[0] for p in p1) if p1 else e1
        # expected at n=1: two F's and only -4/15 movers
        ok1 = p1 is not None and len(f1) == 2 and all(
            p[0] == "F" or LIB.gliders[p[0]].velocity == Fraction(-4, 15) for p in p1)
        diff0 = p0 is not None and (len(f0) != 2 or any(
            p[0] != "F" and LIB.gliders[p[0]].velocity != Fraction(-4, 15) for p in p0))
        tag = "ZTEST?" if ok1 and diff0 else ""
        print(mv, "| n=0:", n0, "| n=1 ok" if ok1 else f"| n=1: {n1}", tag, flush=True)
