"""Composability of the R2 -> R1 channel with R1's own right stream.
Branch A: R1 = E^3 (two GB5's), R2 = E gets Z_L at zero -> A -> R1 = E^2.
Branch C: R1 = E^3, R2 = E^2 (Z_L just decrements it), and R1 is brought to
E^2 by a right-stream DEC (GB3) instead.
Probe afterwards on the right: GB3 (-> R1 = 0) then gate's J (zero class
emits a Bbar).  Scan the probe phase (42) and compare, per branch, which
phases give the zero-J Bbar outcome.  Same set => R1's right end is in the
same class after the left signal as after a right-stream DEC."""
import sys
from collections import defaultdict
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()

D = 600
XZ = -6000
T1 = 2          # clean class of the Z_L answer at R1 (t2_r2r1.py)
XPR = D + 150 + 110 * 3 + 2400   # probe far right so it arrives last


def run(branch, tp):
    r2 = [("E", 0, 0)] if branch == "A" else [("E^2", 0, 0)]
    right = r2 + [("E", T1, D)] + AC.parts("I", T1, D + 150) + AC.parts("I", T1, D + 260)
    if branch == "C":
        right += AC.parts("D", T1, D + 370)
    right += AC.parts("D", tp, XPR) + AC.parts("J", tp, XPR + 140)
    items = [("ZL", 0, XZ)] + right
    c0 = (L.C_E - vlib.LIB["ZL"].w) % 14
    T = 15 * (XPR - D + 400) + 6000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return " + ".join(v3.base(n) for n, x, w, k in vlib.identify(r, org, T=T))


if __name__ == "__main__":
    for b in "AC":
        out = defaultdict(list)
        for tp in range(42):
            out[run(b, tp)].append(tp)
        print(f"branch {b}:")
        for k, v in out.items():
            print(f"   {k:34s} {v}")
