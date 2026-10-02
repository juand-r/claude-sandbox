"""W4 (lead 00:41, route 23): a right-stream BLOCK whose net effect on R1's
back is clean (nothing left in the stream) and depends on the back's class.

Candidate blocks: Bbar followed by k B's (spacing s cells). E^m + Bbar emits
A's to the right in every clean class (r3 #26); A + B -> nothing and
B + E^m -> E^(m+1) are single-class, so trailing B's can eat the A's and
the surplus B's add to the rod. The block's outcome can depend only on the
Bbar's class against the rod (3 classes: det((12,-6),(15,-4))/14 = 3).

For each (k, s), rod E^m (m = 5..9), Bbar seeds over 12 time phases (all 3
classes, each class reached several times: asserted one outcome per class),
run T steps (hrun), read: rod value (rodval: one clean rod in the whole
light cone) or 'dirty'. Report per (k, s) the value change per class.

python3 w4_scan.py [kmax]"""
import sys
from fractions import Fraction

import hrun
import pairscan
import rodval

vlib = hrun.vlib
T = 2500


def outcome(m, t0, k, s, d0=60):
    nm = f"E^{m}"
    items = [(nm, 0, 0), ("Bbar", t0, d0)] + [("B", 0, d0 + 30 + s * (i + 1)) for i in range(k)]
    row, org, placed = vlib.build(items, pad=400)
    v = rodval.value(row, org, T)
    G1, G2 = vlib.LIB[nm], vlib.LIB["Bbar"]
    (_, tx, xx), (_, ty, xy) = placed[0], placed[1]
    cls = pairscan.cls_key((G1.P, G1.D), (G2.P, G2.D), ty - tx, xy - xx)
    return v, cls


def table(k, s, ms=range(5, 10)):
    res = {}
    for m in ms:
        per = {}
        for t0 in range(12):
            v, cls = outcome(m, t0, k, s)
            dv = None if v is None else v - m
            per.setdefault(cls, set()).add(dv)
        res[m] = per
    return res


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for k in range(0, kmax + 1):
        for s in (40, 80, 160):
            res = table(k, s)
            # summarise: per class (sorted keys), the set of value changes over m
            keys = sorted({c for m in res for c in res[m]})
            summ = []
            for c in keys:
                vals = [res[m].get(c, {None}) for m in res]
                flat = set().union(*vals)
                summ.append(sorted(flat, key=lambda x: (x is None, x)))
            consistent = all(len(res[m][c]) == 1 for m in res for c in res[m])
            print(f"k={k} s={s}: per class value change over m=5..9: {summ} "
                  f"(one outcome per class: {consistent})", flush=True)
