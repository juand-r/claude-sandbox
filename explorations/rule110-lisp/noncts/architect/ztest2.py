"""Zero-test search, stage 2: two-mover sequences (m, m2) whose predicted
net effect on the register is the identity (same exact D) but where m
first moves P closer to T. Simulated at n = 0 and n = 1 (relative
placement: each mover placed w.r.t. T's current seed, 20 F periods apart,
as in xcounter.schedule)."""
import sys
from fractions import Fraction
from winding3 import movers, apply
from xcounter import schedule
from rx import run, LIB
from m1_predict import norm_seed

U = (-24, 12)


def gap(D):
    return D[1] + D[0] / 9


def sim(n, seq):
    D = (n * U[0], 43 + n * U[1])
    try:
        pl, T, P = schedule((0, 0), (-D[0], -D[1]), [list(seq)])
    except AssertionError:
        return None, None
    try:
        prods = run(pl, 36 * 20 * len(pl) + 6000)
    except RuntimeError:
        return "unsettled", (T, P)
    return prods, (T, P)


def clean(prods, TP):
    if not isinstance(prods, list):
        return False
    fs = sorted(norm_seed(*p) for p in prods if p[0] == "F")
    exp = sorted([norm_seed("F", *TP[0]), norm_seed("F", *TP[1])])
    return fs == exp and all(p[0] == "F" or LIB.gliders[p[0]].velocity ==
                             Fraction(-4, 15) for p in prods)


if __name__ == "__main__":
    MV = movers()
    D0 = (0, 43)
    closer = []
    for m in MV:
        D1 = apply(m, D0)
        if D1 is not None and gap(D1) < gap(D0) - 1:
            closer.append((m, D1))
    print("movers that bring P closer:", len(closer), flush=True)
    tried = 0
    for m, D1 in closer:
        for m2 in MV:
            if apply(m2, D1) != D0:
                continue
            tried += 1
            p1, tp1 = sim(1, (m, m2))
            if not clean(p1, tp1):
                continue
            p0, tp0 = sim(0, (m, m2))
            c0 = clean(p0, tp0)
            names0 = sorted(p[0] for p in p0) if isinstance(p0, list) else p0
            print(("SAME " if c0 else "DIFF ") , m, m2, "gap after m: %.2f" % gap(D1),
                  "| n=0 ->", names0, flush=True)
    print("tried", tried)
