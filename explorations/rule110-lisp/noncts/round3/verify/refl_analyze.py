"""Summarise refl_brute.log: per train (pair, rel, t0 class), the set of n
with a flagged outcome; re-run flagged cases and velocity-type the '?'
objects (my vlib.velocity_type) to see whether they are left-movers."""
import re
from collections import defaultdict
import t1lib as L
import v3, vlib
L.register_IL()

flags = defaultdict(dict)
for line in open("refl_brute.log"):
    m = re.match(r"FLAG (\S+) rel=\((-?\d+), (-?\d+)\) n=(\d+) t0=(\d+) ox=(\d+): (.*)", line)
    if m:
        key, dt, dx, n, t0, ox, out = m.groups()
        flags[(key, int(dt), int(dx), int(t0))][int(n)] = (int(ox), out)
multi = {k: v for k, v in flags.items() if len(v) >= 2}
print(f"{len(flags)} flagged (train, class); {len(multi)} with >= 2 values of n")
for k, v in sorted(flags.items(), key=lambda kv: -len(kv[1]))[:40]:
    key, dt, dx, t0 = k
    p1, p2 = key.split("|")
    desc = []
    for n, (ox, out) in sorted(v.items()):
        items = [(p2, t0 + dt, -100 - ox + dx), (p1, t0, -100 - ox), (f"E^{n}", 0, 0)]
        objs, r, org, placed = v3.run(items, 2500)
        vt = vlib.velocity_type(r[2516:len(r) - 2516]) if False else None
        desc.append(f"n={n}: {out}")
    print(k, "; ".join(desc))
