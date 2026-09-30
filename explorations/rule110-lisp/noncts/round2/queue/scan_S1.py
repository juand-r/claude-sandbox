"""Screen: one Ebar inserted just before the second leader K."""
import sys
from splice import *
T = 16000
out = open("scan_S1.log", "w")
for tape in ("YN", "NY"):
    m = Machine(tape, ["YNNNNN"], T)
    o = m.origin
    c = ether_cut(m.row, o + 3847)
    base = m.run(m.row, T, 1100, 7400)
    print(tape, "base", sum(1 for x, y, k in base if x >= 3823 and k == "E"), file=out, flush=True)
    for k in range(30):
        for oo in (0, 14, 28):
            new = insert_items(m.row, c, [(k, oo)])
            cs = m.run(new, T, 1100, 7400)
            print(tape, k, oo, sum(1 for x, y, kk in cs if x < 3823 and kk == "E"),
                  sum(1 for x, y, kk in cs if x >= 3823 and kk == "E"),
                  [f"{kk}{x}" for x, y, kk in cs if kk != "E"], file=out, flush=True)
