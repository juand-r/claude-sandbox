"""Check coupler 06:45 item 1 examples: class-free back-face reactions of
G-speed pairs from the right on R2 = E^4 (collider-convention part
offsets translated to mine with xlate.mapping; my builder, engine, my
typer; all 42 seed phases of the pair)."""
import sys
from collections import Counter
import v3, vlib
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC

CASES = [  # (first, second, dt, dx, claimed effect)
    ("G", "GB1", 0, 39, "+1 & A"),
    ("GB1", "GB1", -4, 48, "+2 & A"),
    ("GB2", "GB1", -3, 56, "+3 & A"),
    ("G", "GB5", -26, 47, "+5 & A"),
    ("GB2", "GB1", -2, 52, "-2 & A^3"),
]
for g1, g2, dt, dx, claim in CASES:
    mdt, mdx = AC.my_offset(g1, g2, dt, dx)
    out = Counter()
    for t0 in range(42):
        items = [("E^4", 0, 0), (g1, t0, 120), (g2, t0 + mdt, 120 + mdx)]
        try:
            objs, r, org, placed = v3.run(items, 4000)
        except ValueError as e:
            out["build error"] += 1
            continue
        if (placed[2][1] - placed[1][1], placed[2][2] - placed[1][2]) != (mdt, mdx):
            out["snapped"] += 1
            continue
        out[" + ".join(v3.names(objs))] += 1
    print(f"{g1}+{g2}@({dt},{dx}) claimed {claim}: {dict(out)}")
