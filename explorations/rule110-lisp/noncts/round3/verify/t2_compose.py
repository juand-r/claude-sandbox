"""Composability of the R1 -> R2 coupling with R2's own left stream.
R2 = E raised to value 4 by the first 4 slots of a fixed left program
(t1_IIIIII.json).  Branch A: R1 = E with J, I behind it in the clean class
(Bbar -> R2 += 2, echo A -> R1 back to 0).  Branch B: the same without J, I.
Afterwards a probe A (DEC from the left) arrives at R2 from far left; scan
its 3 x 14 placements and report, per branch, which placements DEC R2
cleanly.  If the DEC placements coincide, the Bbar event leaves R2's left
end in the same class, and a fixed left program can continue after a
data-dependent coupling event."""
import sys, json
from collections import defaultdict
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()

D = 600
T1 = int(sys.argv[1]) if len(sys.argv) > 1 else 0     # clean R1 phase class (t2_class: 0 for R2 >= 2)
XP = -10500
slots = [tuple(s) for s in json.load(open("t1_IIIIII.json"))["slots"]][:4]
prog = [(L.OPS[o], t, x) for o, t, x in slots][::-1]


def run(branch, tp, dp):
    right = [("E", 0, 0), ("E", T1, D)]
    if branch == "A":
        right += AC.parts("J", 5 + T1, D + 447) + AC.parts("I", 5 + T1, D + 447 + 110)
    items = [("A", tp, XP - dp)] + prog + right
    c0 = (L.C_E - sum(vlib.LIB[n].w for n, _, _ in items[:-len(right)])) % 14
    T = 16000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return " + ".join(v3.base(n) for n, x, w, k in vlib.identify(r, org, T=T)), placed[0]


if __name__ == "__main__":
    for branch in "AB":
        out = defaultdict(list)
        for tp in range(3):
            for dp in range(14):
                o, p = run(branch, tp, dp)
                out[o].append((p[1], p[2]))
        print(f"branch {branch}:")
        for k, v in out.items():
            print(f"   {k:30s} {sorted(set(v))}")
