"""Zero test, stage 3. Value 0 := n = -1 (gap 33.67). DEC at value 0
leaves the two F's as a close compound (F_19_F, gap 19) with only
Ebar-speed debris. Search a PROBE mover that turns this abnormal state
into two separate F's plus a stationary messenger (C1/C2/C3), with only
Ebar-speed leftovers. (Identity on normal states is checked afterwards.)
Slot layout as in xstream.py; the probe goes in the slot after the
second DEC, at each mover's class relative to the assumed T."""
import sys
from fractions import Fraction
from xstream import STD, DELTA, SLOT_LEN, PF
from winding3 import movers
from rx import run, LIB


def scenario(mv, n0=0, decs=2):
    D = (0, 43)
    pl = [("F", 0, 0), ("F", -D[0], -D[1])]
    j = 0
    for j in range(decs):
        base = (j * DELTA[0] + j * SLOT_LEN * PF[0], j * DELTA[1] + j * SLOT_LEN * PF[1])
        for name, dt, dx in STD["DEC"][0]:
            pl.append((name, base[0] + dt, base[1] + dx))
    j = decs
    base = (j * DELTA[0] + j * SLOT_LEN * PF[0], j * DELTA[1] + j * SLOT_LEN * PF[1])
    name, t, x = mv
    pl.append((name, base[0] + t + 20 * PF[0], base[1] + x + 20 * PF[1]))
    return pl


def classify(prods):
    v = lambda n: LIB.gliders[n].velocity
    Fs = [p for p in prods if p[0] == "F"]
    Cs = [p for p in prods if p[0] in ("C1", "C2", "C3")]
    rest = [p for p in prods if p[0] != "F" and p[0] not in ("C1", "C2", "C3")]
    ok_rest = all(v(p[0]) == Fraction(-4, 15) for p in rest)
    return len(Fs), [c[0] for c in Cs], ok_rest, sorted(p[0] for p in prods)


if __name__ == "__main__":
    MV = movers()
    lo, hi = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, len(MV))
    T = 36 * (3 * SLOT_LEN + 20) + 8000
    for i, mv in enumerate(MV[lo:hi], lo):
        try:
            prods = run(scenario(mv), T)
        except RuntimeError:
            print(i, mv, "unsettled", flush=True)
            continue
        nF, Cs, ok_rest, names = classify(prods)
        tag = "HIT" if nF == 2 and len(Cs) == 1 and ok_rest else ""
        if tag or i % 50 == 0:
            print(i, mv, nF, Cs, ok_rest, names if tag else "", tag, flush=True)
