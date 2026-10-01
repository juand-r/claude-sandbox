"""Soft-leader screen: P = two Ebars (slip 0) inserted right before the
first raw leader K, the rest re-attached with a machine symmetry shift
(splice.valid_shifts), so P is the only change. Rejector tape NYYN:
a soft leader would let the rejector delete appendant 1 (region1 -> ~0;
the unmodified machine accepts it: 24). Resumable: skips logged combos."""
import json, os, sys
from splice import *
T = 40000
LOG = "scan_pair.jsonl"
done = set()
if os.path.exists(LOG):
    for line in open(LOG):
        done.add(tuple(json.loads(line)["P"]))
tapes = sys.argv[1:] or ["NYYN"]
M = {t: Machine(t, ["YNNNNN"], T, left_periods=4, right_periods=3) for t in tapes}
SH = valid_shifts(600)
def first_offset(k, c, cph, lo):
    arr, cl, cr = ebar_tiles()[k]
    x = c + lo
    return lo + (cl - x - cph) % TILE
out = open(LOG, "a")
m0 = M[tapes[0]]
K0 = [a for n, a, b in m0.blocks if n == "K"]
c = ether_cut(m0.row, m0.origin + K0[0], search=10, tight=True)
cph0 = phase_at(m0.row, c)
for k1 in range(30):
    o1 = first_offset(k1, c, cph0, 0)
    arr1, cl1, cr1 = ebar_tiles()[k1]
    cph1 = (cr1 - (c + o1)) % TILE
    for k2 in range(30):
        base2 = o1 + len(arr1)
        o2a = first_offset(k2, c, cph1, base2)
        for o2 in (o2a, o2a + 14):
            P = (int(k1), int(o1), int(k2), int(o2))
            if P in done:
                continue
            res = {}
            for t, m in M.items():
                K = [a for n, a, b in m.blocks if n == "K"]
                cc = ether_cut(m.row, m.origin + K[0], search=10, tight=True)
                row = None
                for s, D in SH:
                    row = insert_exact(m.row, cc, [(k1, o1), (k2, o2)], s, D)
                    if row is not None:
                        break
                if row is None:
                    res[t] = None
                    continue
                cs = m.run(row, T, 1100, K[2] + 300)
                res[t] = ([sum(1 for x, y, k in cs if lo <= x < hi and k == "E")
                           for lo, hi in [(1100, K[0]), (K[0], K[1]), (K[1], K[2])]],
                          [f"{k}{x}" for x, y, k in cs if k != "E"], (int(s), int(D)))
            out.write(json.dumps({"P": P, "r": res}) + "\n")
            out.flush()
