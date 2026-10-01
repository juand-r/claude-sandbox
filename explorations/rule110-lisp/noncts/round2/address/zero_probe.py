"""What happens when a register is driven below its last clean value?
DN1^k and DN2^k from the standard start (gaps ~119), simulated directly
(placements from the catalog prediction where it exists; once the
prediction fails we place the remaining movers as if the markers had
followed the prediction of the last clean state, i.e. a fixed stream)."""
import sys
from fractions import Fraction
import gen
gen.ABSORB = True
from gen import cross_chain, LIB
from rx import run, norm
import tworeg_abs as T2

PF = (36, -4)


def sched(prog):
    m = T2.start_markers()
    pl = [("F",) + x for x in m]
    delay, clean = 0, True
    for op in prog:
        for name, t, x in T2.OPS[op]:
            delay += T2.GAP
            T = m[0]
            ev = (T[0] + t + delay * PF[0], T[1] + x + delay * PF[1])
            pl.append((name,) + ev)
            if clean:
                r = cross_chain(["F"] * 3, m, (name,) + ev)
                if r is None:
                    clean = False
                else:
                    m = r[0]
    return pl, delay, clean


for op in ("DN1", "DN2"):
    for k in range(5, 9):
        pl, delay, clean = sched([op] * k)
        prods = run(pl, 36 * (delay + 40) + 6000, must_settle=False)
        names = [p[0] for p in prods]
        fs = sorted((norm(*p) for p in prods if p[0] == "F"), key=T2.xpos)
        other = sorted({n for n in names if n != "F" and LIB.gliders[n].velocity != Fraction(-4, 15)} if all(n in LIB.gliders for n in names) else names)
        print(op, k, "catalog-clean" if clean else "prediction fails", "F's", len(fs),
              "gaps", [round(g, 2) for g in T2.gaps_of(fs)], "non-Ebar-speed:", other, flush=True)
