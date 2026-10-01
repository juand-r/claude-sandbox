"""Milestone check 1: Z = Ebar(k2,x2) + Ebar(k1,x1) inserted in front of
P_1 at t_in = 31500 makes read 1 a forced N; do later reads stay correct?
    python t_forced1.py TAPE NREAD [k2 x2 k1 x1]"""
import sys
from reads import *
tape, nread = sys.argv[1], int(sys.argv[2])
k2, x2, k1, x1 = map(int, sys.argv[3:7]) if len(sys.argv) > 6 else (0, -73, 14, -4)
apps = ["YNNNNN"]
E = ebar_tiles()
class Surg:
    t_in = 31500
    def __call__(self, m, row):
        K0 = [a for n, a, b in m.blocks if n == "K"][0]
        return rewrite(row, m.origin, self.t_in, K0 - 345, K0 + 37,
                       [(E, k2, K0 + x2), (E, k1, K0 + x1)])
for label, surg, kinds in (("plain", None, "K" * nread), ("Z", Surg(), "KF" + "K" * nread)):
    got, times, m = check(tape, apps, nread, surg)
    ref = reference(tape, apps, kinds, nread)
    print(f"{tape} {label}: observed {got} reference {ref} {'MATCH' if got == ref else 'DIFFER'}", times, flush=True)
