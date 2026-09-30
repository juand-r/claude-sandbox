"""Screen for a soft leader: material P inserted just before the first
raw leader K. Want: acc (read0=Y) -> K still prepared, reads symbol 1
(YNYN: region1 rejected, like base); rej (read0=N) -> passes, deletes
appendant 1 (NYYN: region1 ~ empty instead of accepted)."""
import sys, json
from splice import *
T = int(sys.argv[2]) if len(sys.argv) > 2 else 60000
mode = sys.argv[1]
M = {tape: Machine(tape, ["YNNNNN"], T, left_periods=4, right_periods=3)
     for tape in ("YNYN", "NYYN")}
def cands():
    if mode == "single":
        for k in range(30):
            for o in (0, 14, 28, 42):
                yield [(k, o)]
    elif mode == "comp":            # a whole I block, lattice-shifted
        yield None
def evaluate(P):
    res = {}
    for tape, m in M.items():
        K = [a for n, a, b in m.blocks if n == "K"]
        c = ether_cut(m.row, m.origin + K[0] - 24, search=10)
        row = insert_items(m.row, c, P)
        if row is None:
            return None
        cs = m.run(row, T, 1100, K[2] + 300)
        res[tape] = ([sum(1 for x, y, k in cs if lo <= x < hi and k == "E")
                      for lo, hi in [(1100, K[0]), (K[0], K[1]), (K[1], K[2])]],
                     [f"{k}{x}" for x, y, k in cs if k != "E"])
    return res
for P in cands():
    r = evaluate(P)
    print(json.dumps({"P": P, "r": r}), flush=True)
