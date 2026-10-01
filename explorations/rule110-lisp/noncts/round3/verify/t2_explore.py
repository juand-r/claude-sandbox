"""T2 exploration (mine): R2 = E^(v2+1) (left), R1 = E (value 0) at distance
D to its right, right stream: J (gate's GB1+GB1) then I (GB5).  Expected
chain: J at zero -> Bbar -> R2 + Bbar -> E^(v2+3) + A (one class) ->
A reaches R1 after the I made it E^2 -> A + E^2 -> E (all classes).
Scan the J phase t0 (42) and report end products (exact CA, my typer)."""
import sys
from collections import defaultdict
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC

v2 = int(sys.argv[1]) if len(sys.argv) > 1 else 4
D = int(sys.argv[2]) if len(sys.argv) > 2 else 300
GI = int(sys.argv[3]) if len(sys.argv) > 3 else 110
T = 15 * (D + 400) + 6 * D + 3000
res = defaultdict(list)
for t0 in range(42):
    for tI in (0,):
        items = [(f"E^{v2 + 1}", 0, 0), ("E", 0, D)] + AC.parts("J", t0, D + 150) + AC.parts("I", tI, D + 150 + GI)
        objs, r, org, placed = v3.run(items, T)
        res[" + ".join(v3.names(objs))].append(t0)
for k, v in sorted(res.items(), key=lambda kv: -len(kv[1])):
    print(f"{k:60s} t0={v}")
