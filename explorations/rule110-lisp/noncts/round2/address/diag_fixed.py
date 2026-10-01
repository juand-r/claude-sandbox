"""Diagnose the failing fixed-stream program by prefixes (full simulation,
F compounds split as in range_check)."""
import sys
from fractions import Fraction
import fixed_stream as F
import tworeg_abs as T2
from rx import run, LIB
from range_check import f_seeds
prog = sys.argv[1].split(",")
pl = F.build(prog)
res = run(pl, 36 * F.SLOT * (len(prog) + 1) + 8000, must_settle=False)
fs = f_seeds(res)
junk = sorted({p[0] for p in res if not p[0].startswith("F") and (p[0] not in LIB.gliders or LIB.gliders[p[0]].velocity != Fraction(-4, 15))})
print(prog, "F's", len(fs), [round(g, 2) for g in T2.gaps_of(fs)], "want", [round(g, 2) for g in T2.predicted_gaps(prog)], "junk", junk)
