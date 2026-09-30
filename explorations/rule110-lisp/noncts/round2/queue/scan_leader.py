"""Scan: translate the raw leader K (and everything after it) by spacetime
lattice shifts (s, m); does the acceptor / rejector still get absorbed?"""
from splice import *
T = 16000
res = {}
for tape in ("YN", "NY"):
    m = Machine(tape, ["YNNNNN"], T)
    o = m.origin
    c = ether_cut(m.row, o + 3847)
    base = m.run(m.row, T, 1100, 7400)
    cnt = lambda cs: (sum(1 for x, y, k in cs if x < 3823 and k == "E"),
                      sum(1 for x, y, k in cs if x >= 3823 and k == "E"),
                      tuple(f"{k}{x}" for x, y, k in cs if k != "E"))
    print(tape, "base", cnt(base))
    for s in range(30):
        for mm in range(0, 2):
            new, d = shift_remainder(m.row, c, s, mm)
            r = cnt(m.run(new, T, 1100, 7400))
            res[(tape, s, mm)] = r
            print(tape, s, mm, d, r, flush=True)
