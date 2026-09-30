"""Crossing-only counter: two F's (T front, P back) and sequences of
Ebar packets that cross both and change their distance D by a fixed
lattice vector, returning the phase residue (found by winding3.find_cycles).
Built with exact relative placements and verified by full Rule 110
simulation (collider's simulate on library gliders)."""
import sys
from rx import run, G as GL
from m1_predict import norm_seed

INC = [('Ebar@(0,0)+Ebar@(-26,27)', -1, 45), ('Ebar@(0,0)+Ebar@(-11,37)', -16, 63),
       ('Ebar@(0,0)+Ebar@(-1,25)', -12, 61)]      # net D (-24,12): P moves ~9.33 left
DEC = [('Ebar@(0,0)+Ebar@(-26,27)', -1, 45), ('Ebar@(0,0)+Ebar@(-4,23)', -15, 59),
       ('Ebar', -14, 55)]                         # net D (-12,-8): P moves ~9.33 right
PFv = (36, -4)


def schedule(T0, P0, ops, gap_periods=20):
    """Place the movers of `ops` (a list of packet sequences) one after the
    other. Each mover's event is relative to T's CURRENT seed, predicted by
    winding3.apply-style bookkeeping; consecutive movers are separated by
    whole F periods (keeps every class). Returns placements and predicted
    final (T, P)."""
    from winding3 import cross, lateral
    T, P = T0, P0
    placements = [("F",) + T0, ("F",) + P0]
    delay = 0
    for seq in ops:
        for name, t, x in seq:
            delay += gap_periods
            ev = (T[0] + t + delay * PFv[0], T[1] + x + delay * PFv[1])
            # predicted effect (relative to current T and P)
            r = cross(T, (name,) + ev)
            assert r is not None, ("T crossing not clean", name, ev)
            T, outs = r
            for o in sorted(outs, key=lateral):
                rr = cross(P, o)
                assert rr is not None, ("P crossing not clean", o)
                P = rr[0]
            placements.append((name,) + ev)
    return placements, T, P


def check(ops, label):
    T0, P0 = (0, 0), (0, -43)
    pl, T, P = schedule(T0, P0, ops)
    # the scheduled movers start far in the future at the right; shift all
    # movers so the row at time 0 is valid: movers seeded with large t are
    # fine (state_at handles any seed)
    prods = run(pl, 36 * 20 * len(pl) + 6000)
    fs = sorted([norm_seed(n, t, x) for n, t, x in prods if n == "F"], key=lambda s: s[1])
    others = sorted(n for n, t, x in prods if n != "F")
    exp = sorted([norm_seed("F", *P), norm_seed("F", *T)], key=lambda s: s[1])
    D = (T[0] - P[0], T[1] - P[1])
    print(f"{label}: predicted D {D}, F's {exp}; simulated F's {fs}; "
          f"{'MATCH' if fs == exp else 'MISMATCH'}; other products {len(others)}")
    return fs == exp


if __name__ == "__main__" and len(sys.argv) == 1:
    check([INC], "INC x1")
    check([DEC], "DEC x1")
    check([INC, INC, INC], "INC x3")
    check([INC, INC, DEC, INC, DEC, DEC], "INC,INC,DEC,INC,DEC,DEC")


def full_check(ops, label):
    """Simulate, then check: the two F's are exactly where predicted and
    every other product is an Ebar-speed glider (movers only, no junk)."""
    from winding3 import EBAR_SPEED
    T0, P0 = (0, 0), (0, -43)
    pl, T, P = schedule(T0, P0, ops)
    prods = run(pl, 36 * 20 * len(pl) + 6000)
    fs = sorted([norm_seed(n, t, x) for n, t, x in prods if n == "F"], key=lambda s: s[1])
    exp = sorted([norm_seed("F", *P), norm_seed("F", *T)], key=lambda s: s[1])
    from rx import LIB
    from fractions import Fraction
    junk = [p for p in prods if p[0] != "F" and LIB.gliders[p[0]].velocity != Fraction(-4, 15)]
    gap = (T[1] - P[1]) + (T[0] - P[0]) / 9      # spatial gap at equal time
    ok = fs == exp and not junk
    print(f"{label}: gap {gap:.2f} cells, F's {'MATCH' if fs == exp else 'MISMATCH'}, "
          f"junk {junk}, {'OK' if ok else 'FAIL'}", flush=True)
    return ok


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "long":
    seqs = [[INC] * k for k in range(1, 7)] + [[INC] * 6 + [DEC] * k for k in range(1, 7)]
    res = [full_check(s, f"INC^{min(len(s),6)} DEC^{max(0,len(s)-6)}") for s in seqs]
    print(f"{sum(res)}/{len(res)} OK")
