"""Run Ebar-pair prefixes P (before the first K, symmetry-shift attached)
on the four tapes; print 2-read outcome letters and garbage counts."""
import sys, json
from splice import *
T = 60000
TAPES = ("YYNN", "YNYN", "NYYN", "NNYY")
M = {t: Machine(t, ["YNNNNN"], T, left_periods=4, right_periods=3) for t in TAPES}
SH = valid_shifts(600)
def l0(c): return "Y" if 22 <= c <= 28 else "N" if c <= 5 else "?"
def l1(c): return "Y" if 20 <= c <= 28 else "N" if c <= 3 else "?"
for P in json.loads(sys.argv[1]):
    out = {}
    for t, m in M.items():
        K = [a for n, a, b in m.blocks if n == "K"]
        cc = ether_cut(m.row, m.origin + K[0], search=10, tight=True)
        for s, D in SH:
            row = insert_exact(m.row, cc, [tuple(P[:2]), tuple(P[2:])], s, D)
            if row is not None:
                break
        cs = m.run(row, T, 1100, K[2] + 300)
        c0, c1 = [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in [(1100, K[0]), (K[0], K[1])]]
        out[t] = l0(c0) + l1(c1) + f"/{len([1 for x, y, k in cs if k != 'E'])}"
    print(P, out, flush=True)
