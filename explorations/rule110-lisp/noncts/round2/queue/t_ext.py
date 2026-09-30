"""Extend the leader's E_n gliders with B's (B + E_n -> E_{n+1}, single
class) and see how acc / rej prepare the modified leader, and whether the
next read works. Tapes YYNN, YNYN, NYYN, NNYY cover all (read0, read1)."""
import sys
from splice import *
T = 60000
def variant(m, rel, nB, k0=0):
    K = [a for n, a, b in m.blocks if n == "K"][0]
    c = ether_cut(m.row, m.origin + K + rel, search=6)
    items = [(k0, 2 + 20 * i, "B(f1_1)", 4) for i in range(nB)]
    return insert_items(m.row, c, items)
VARS = [("base", None, 0)] + [(f"after{rel}+{n}", rel, n) for rel, n in [(100, 1), (100, 2), (100, 3), (155, 1)]]
for label, rel, nB in VARS:
    for tape in ("YYNN", "YNYN", "NYYN", "NNYY"):
        m = Machine(tape, ["YNNNNN"], T, left_periods=4, right_periods=3)
        K = [a for n, a, b in m.blocks if n == "K"]
        row = m.row if rel is None else variant(m, rel, nB)
        early = m.run(row, 2400, K[0] - 60, K[0] + 400)
        cs = m.run(row, T, 1100, K[2] + 300)
        print(label, tape, " ".join(f"{k}{x - K[0]}" for x, y, k in early),
              "|", [sum(1 for x, y, k in cs if lo <= x < hi and k == "E") for lo, hi in [(1100, K[0]), (K[0], K[1]), (K[1], K[2])]],
              [f"{k}{x}" for x, y, k in cs if k != "E"], flush=True)
