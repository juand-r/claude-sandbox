"""Negative controls for tworeg_abs.py: the same programs with ONE mover
moved to a different collision class (shift by one Ebar-compatible step
that is NOT in the lattice <P_F, P_Ebar>). The prediction then either
fails or differs; the simulation must not reproduce the intended gaps."""
from fractions import Fraction
import tworeg_abs as T2
from rx import run, norm, LIB

def run_shifted(prog, idx, shift):
    pl, pred, delay = T2.schedule(prog)
    name, t, x = pl[3 + idx]
    pl[3 + idx] = (name, t + shift[0], x + shift[1])
    prods = run(pl, 36 * (delay + 40) + 6000, must_settle=False)
    fs = sorted((norm(*p) for p in prods if p[0] == "F"), key=T2.xpos)
    junk = sorted({p[0] for p in prods if p[0] != "F" and LIB.gliders[p[0]].velocity != Fraction(-4, 15)})
    return T2.gaps_of(fs), len(fs), junk

for prog in (["DN2"], ["UP1"]):
    want = [round(g, 2) for g in T2.predicted_gaps(prog)]
    for shift in [(1, -4), (0, 14), (2, -8)]:     # ether-compatible offsets (x + 4t = 0 mod 14)
        g, nf, junk = run_shifted(prog, 0, shift)
        g = [round(v, 2) for v in g]
        print(prog, "mover 0 shifted", shift, "F count", nf, "gaps", g, "intended", want,
              "-> control", "FAILS (good)" if g != want or junk else "still matches (bad control)", junk)
