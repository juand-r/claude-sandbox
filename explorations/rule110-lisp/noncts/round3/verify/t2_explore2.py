"""Scan the R2-R1 distance D (gate's J-at-zero class fixed: J at my seed
(5, 447) relative to R1 = E at (0, D)), then an I (GB5) GI cells behind.
Report outcomes by D."""
import sys
from collections import defaultdict
import v3, vlib
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC

v2 = int(sys.argv[1]) if len(sys.argv) > 1 else 4
GI = int(sys.argv[2]) if len(sys.argv) > 2 else 110
res = defaultdict(list)
for D, t1 in [(D, t1) for D in (250, 264, 278) for t1 in range(15)]:
    T = 15 * (D + 600) + 6 * D + 3000
    items = [(f"E^{v2 + 1}", 0, 0), ("E", t1, D)] + AC.parts("J", 5 + t1, D + 447) + AC.parts("I", 5 + t1, D + 447 + GI)
    objs, r, org, placed = v3.run(items, T, right=False)
    # check the R1-J relation is gate's: snapped E x and J x differ by 447
    ex = placed[1][2]; jx = placed[2][2]
    res[" + ".join(v3.names(objs))].append((D, t1, jx - ex))
for k, v in sorted(res.items(), key=lambda kv: -len(kv[1])):
    print(f"{k:50s} {v}")
