"""Leader variants: shift E2 and everything after it by machine-symmetry
vectors V relative to E5 (changes only the inside of K)."""
from splice import *
T = 60000
TAPES = ("YYNN", "YNYN", "NYYN", "NNYY")
M = {t: Machine(t, ["YNNNNN"], T, left_periods=4, right_periods=3) for t in TAPES}
def l0(c): return "Y" if 22 <= c <= 28 else "N" if c <= 5 else "?"
def l1(c): return "Y" if 20 <= c <= 28 else "N" if c <= 3 else "?"
for s, D in valid_shifts(80):
    out = {}
    for t, m in M.items():
        K = [a for n, a, b in m.blocks if n == "K"]
        c = m.origin + K[0] + 41
        row = replace_exact(m.row, c, c, [], s, D)
        if row is None:
            out = None
            break
        cs = m.run(row, T, 1100, K[2] + 300)
        c0, c1 = [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in [(1100, K[0]), (K[0], K[1])]]
        out[t] = l0(c0) + l1(c1) + f"/{len([1 for x, y, k in cs if k != 'E'])}"
    print(s, D, out, flush=True)
