"""Which spacetime shifts of (K and everything after) keep reads 0 and 1
correct? Cut right after the last component Ebar."""
from splice import *
T = 60000
TAPES = ("YYNN", "YNYN", "NYYN", "NNYY")
M = {t: Machine(t, ["YNNNNN"], T, left_periods=4, right_periods=3) for t in TAPES}
def counts(m, row):
    K = [a for n, a, b in m.blocks if n == "K"]
    cs = m.run(row, T, 1100, K[2] + 300)
    return [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in
            [(1100, K[0]), (K[0], K[1])]], len([1 for x, y, k in cs if k != "E"])
for s in range(30):
    for mm in (0, 1):
        out = []
        for t, m in M.items():
            K = [a for n, a, b in m.blocks if n == "K"][0]
            c = ether_cut(m.row, m.origin + K, search=10, tight=True)
            row, d = shift_remainder(m.row, c, s, mm)
            out.append(counts(m, row))
        print(s, mm, d, out, flush=True)
