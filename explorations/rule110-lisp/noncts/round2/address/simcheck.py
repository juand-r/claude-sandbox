"""Full Rule 110 simulation checks of catalog-level predictions for
multi-marker F lanes (collider's simulate = exact engine + glider typing).

schedule(): movers placed relative to the CURRENT front marker (predicted),
GAP F-periods apart (as architect's xcounter.schedule). The prediction
uses cross_chain; the simulation must reproduce the F positions exactly
and leave only Ebar-speed debris."""
import sys
from fractions import Fraction
import lane
from lane import cross_chain
from rx import run, LIB, norm

PF = (36, -4)
GAP = 20


def schedule(markers, seq, gap=GAP):
    pl = [("F",) + m for m in markers]
    delay = 0
    ok = True
    for name, t, x in seq:
        delay += gap
        T = markers[0]
        ev = (T[0] + t + delay * PF[0], T[1] + x + delay * PF[1])
        pl.append((name,) + ev)
        r = cross_chain(markers, (name,) + ev)
        if r is None:
            ok = False
            continue
        markers = r[0]
    return pl, (markers if ok else None)


def simulate(markers, seq):
    pl, pred = schedule(markers, seq)
    prods = run(pl, 36 * GAP * (len(seq) + 2) + 8000)
    fs = sorted((norm(*p) for p in prods if p[0] == "F"), key=lambda s: s[2] - Fraction(s[1], 9))
    junk = sorted({p[0] for p in prods if p[0] != "F" and LIB.gliders[p[0]].velocity != Fraction(-4, 15)})
    exp = None if pred is None else sorted((norm("F", *m) for m in pred), key=lambda s: s[2] - Fraction(s[1], 9))
    return fs, exp, junk


def gaps(fs):
    """spatial gaps between consecutive F's (left to right) at equal time."""
    xs = [s[2] - Fraction(s[1], 9) for s in fs]
    return [float(b - a) for a, b in zip(xs, xs[1:])]


INC = [('Ebar@(0,0)+Ebar@(-26,27)', -1, 45), ('Ebar@(0,0)+Ebar@(-11,37)', -16, 63),
       ('Ebar@(0,0)+Ebar@(-1,25)', -12, 61)]

if __name__ == "__main__":
    # 1. positive control: architect INC on a lone pair (gap 43)
    fs, exp, junk = simulate([(0, 0), (0, -43)], INC)
    print("control INC on 2 F:", "MATCH" if fs == exp else "MISMATCH", gaps(fs), "junk", junk)
    # 2. same INC with a third F behind (D2 = (0,43) and (7,43))
    for D2 in [(0, 43), (7, 43), (21, 43)]:
        fs, exp, junk = simulate([(0, 0), (0, -43), (-D2[0], -43 - D2[1])], INC)
        print("INC with 3rd F, D2", D2, ": predicted", "clean" if exp else "NOT clean",
              "| sim F count", len(fs), "gaps", gaps(fs), "junk", junk)
    # 3. single-mover INC1 at node D1=D2=(35,43) (graph self-loop (-2,0)), applied 3x
    mv = ('Ebar@(0,0)+Ebar@(-11,37)', -16, 63)
    m0 = [(0, 0), (-35, -43), (-70, -86)]
    for k in (1, 3):
        fs, exp, junk = simulate(m0, [mv] * k)
        print(f"mover x{k} on 3 F (35,43)/(35,43):", "MATCH" if fs == exp else "MISMATCH",
              "gaps", gaps(fs), "junk", junk)
    # negative control for 3: shift the mover by (3,2) (non-lattice)
    fs, exp, junk = simulate(m0, [(mv[0], mv[1] + 3, mv[2] + 2)])
    print("control shifted mover:", "pred clean" if exp else "pred NOT clean", "gaps", gaps(fs), "junk", junk)
