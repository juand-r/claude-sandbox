"""Physics control for the fixed stream: same balanced program, but every
mover of slot 1 shifted by (1,-4) (ether-compatible, not in L_FE), i.e.
slot 1 in the wrong collision class. Must not give the intended gaps."""
from fractions import Fraction
import fixed_stream as F
import tworeg_abs as T2
from rx import run, LIB
from range_check import f_seeds
prog = ["UP2", "DN2", "UP2"]
pl = F.build(prog)
n0 = 3 + len(F.STD[prog[0]][0])
n1 = n0 + len(F.STD[prog[1]][0])
pl = pl[:n0] + [(n, t + 1, x - 4) for n, t, x in pl[n0:n1]] + pl[n1:]
res = run(pl, 36 * F.SLOT * (len(prog) + 1) + 8000, must_settle=False)
fs = f_seeds(res)
junk = sorted({p[0] for p in res if not p[0].startswith("F") and (p[0] not in LIB.gliders or LIB.gliders[p[0]].velocity != Fraction(-4, 15))})
got = [round(g, 2) for g in T2.gaps_of(fs)]
want = [round(g, 2) for g in T2.predicted_gaps(prog)]
print("control slot-1 shift (1,-4):", "F's", len(fs), got, "want", want, "junk", junk,
      "-> fails (good)" if got != want or junk else "-> still OK (BAD control)")
