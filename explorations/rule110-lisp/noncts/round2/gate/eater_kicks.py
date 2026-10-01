"""Can the C1-neutral eaters act as F-lane register movers? For each eater
type and each of its 12 classes vs the front F (T), run it through address's
three F's (start markers, plus a few other register states) at catalog level
(gen.cross_chain, absorption allowed) and print gap changes."""
import os
import sys
ADDR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "address")
sys.path.insert(0, ADDR)
_cwd = os.getcwd()
os.chdir(ADDR)
import gen  # noqa: E402
import tworeg_abs as T2  # noqa: E402
from collide import canonical_reps  # noqa: E402
os.chdir(_cwd)
gen.ABSORB = True
from fractions import Fraction  # noqa: E402

PF = (36, -4)
EATERS = ["Ebar@(0,0)+Ebar@(-4,23)", "Ebar@(0,0)+Ebar@(-22,39)"]
states = {"start": T2.start_markers()}
for prog in (["UP1"], ["UP2"], ["UP1", "UP2"], ["DN1"], ["DN2"]):
    pl, m, _ = T2.schedule(prog)
    states["+".join(prog)] = m


def xg(ms):
    xs = [Fraction(s[1]) + Fraction(s[0], 9) for s in ms]
    return [float(xs[0] - xs[1]), float(xs[1] - xs[2])]


for name in EATERS:
    for st_name, ms in states.items():
        T = ms[0]
        for k, rep in enumerate(canonical_reps(gen.LIB, "F", name)):
            mv = (name, T[0] + rep[0] + 20 * PF[0], T[1] + rep[1] + 20 * PF[1])
            r = gen.cross_chain(["F"] * 3, ms, mv)
            if r is None:
                continue
            new, outs = r
            g0, g1 = xg(ms), xg(new)
            print(f"{name[-8:]} state {st_name:8s} class {k:2d}: dgap(reg1,reg2) = "
                  f"({g1[0]-g0[0]:+.2f}, {g1[1]-g0[1]:+.2f}) outs {[o[0] for o in outs]}")
