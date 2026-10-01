"""Rods with a non-standard back: E^8 + (Ebar or E) placed so close that
they form one co-moving compound '?' (unknown to my typer).  Apply front
ops (I_L, Z_L, A) in all 3 x 14 placements and look for outcomes with a
right-mover (A family) besides co-moving/stationary objects: candidates
for theory's wall converter (s.6.5)."""
from collections import defaultdict
import t1lib as L
import v3, vlib, engine
L.register_IL()
T = 2500
RIGHT = {"A", "A^2", "A^3", "A^4", "D1", "D2"}

comps = []
seen = set()
for obj in ("Ebar", "E"):
    for t0 in range(vlib.LIB[obj].P):
        for gap in range(0, 40):
            try:
                o0, r, org, placed = v3.run([("E^8", 0, 0), (obj, t0, gap)], T)
            except ValueError:
                continue
            if v3.names(o0) == ["?"]:
                key = o0[0][0] if False else tuple(o0[0][2:])  # charge only
                k2 = (obj, placed[1][1], placed[1][2])
                if k2 not in seen:
                    seen.add(k2)
                    comps.append((obj, placed[1][1], placed[1][2]))
print(len(comps), "compound placements")
res = defaultdict(list)
for obj, t0, x in comps:
    for P in ("IL", "ZL", "A"):
        pseen = set()
        for tp in range(3):
            for dx in range(14):
                items = [(P, tp, -70 - dx), ("E^8", 0, 0), (obj, t0, x)]
                try:
                    _, _, pl = vlib.build_right(items, c_right=0, pad=50)
                except ValueError:
                    continue
                if (pl[0][1], pl[0][2]) in pseen:
                    continue
                pseen.add((pl[0][1], pl[0][2]))
                o, *_ = v3.run(items, T)
                nm = v3.names(o)
                if any(b in RIGHT for b in nm) and len(nm) <= 3:
                    res[(P, " + ".join(nm))].append((obj, t0, x, tp, dx))
for k, v in sorted(res.items(), key=lambda kv: -len(kv[1]))[:25]:
    print(k, len(v), v[:3])
