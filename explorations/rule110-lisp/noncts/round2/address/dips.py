"""Intermediate dips: for each (padded) instruction, the smallest gaps
(reg1, reg2) reached between movers, relative to the start gaps (catalog
prediction). A register at value v is safe for an instruction if
gap(v) + dip >= the multi-body threshold (~25 cells measured)."""
import gen
gen.ABSORB = True
from gen import cross_chain
import tworeg_abs as T2
import fixed_stream as F
from rx import norm

PF = (36, -4)


def gaps(m):
    return T2.gaps_of([norm("F", *x) for x in m])     # [reg2, reg1]


for label, table in (("base", T2.OPS), ("padded", {o: F.padded(o, F.PADS) for o in T2.OPS})):
    for op, seq in table.items():
        m = T2.start_markers()
        g0 = gaps(m)
        lo = [0.0, 0.0]
        delay = 0
        for name, t, x in seq:
            delay += T2.GAP
            T = m[0]
            m = cross_chain(["F"] * 3, m, (name, T[0] + t + delay * PF[0], T[1] + x + delay * PF[1]))[0]
            g = gaps(m)
            lo = [min(lo[0], g[0] - g0[0]), min(lo[1], g[1] - g0[1])]
        print(label, op, "dip reg2 %.2f reg1 %.2f" % tuple(lo))
