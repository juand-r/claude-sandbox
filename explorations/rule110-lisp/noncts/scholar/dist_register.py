"""Distance registers from class-dependent crossing displacements.

Ebar crosses a C1 in two classes with different displacements (collider:
class 1 -> C1 moves (2, +13), class 2 -> C1 moves (0, +7)). A packet that
crosses the two markers of a register in DIFFERENT classes changes their
distance (by +-6 cells); in the same class it leaves it unchanged.
Here: two C1 markers (gap m tiles) and one Ebar; for each configuration in
which the Ebar crosses both, measure both markers' displacements exactly
(anchors via locate.find) and report the change of the gap."""
from collections import Counter
import r110check as r, locate as L

T = 1800
out = Counter()
examples = {}
for m in range(3, 9):
    for y in [k for k in r.PHASES if k.startswith("E-(")]:
        spec = f"C1(A,f1_1)-{m}e-C1(A,f1_1)-9e-{y}"
        row, s0 = r.build(spec, pad=260)
        h = r.evolve(row, T)
        e, l, _ = r.outcome(spec, T=T, pad=260)
        if sorted(l) != ["C1", "C1", "E-"] or e != l:
            continue
        before = sorted(L.find(h, 0, "C1", s0 - 30, s0 + 14 * m + 60), key=lambda a: a[1])
        after = sorted(L.find(h, T - 7, "C1", s0 - 60, s0 + 14 * m + 120), key=lambda a: a[1])
        if len(before) != 2 or len(after) != 2:
            continue
        # anchors: (t mod 7 phase, x); compare x shifts and time-phase shifts
        d = tuple(((a[0] - b[0]) % 7, a[1] - b[1]) for a, b in zip(after, before))
        gap_change = d[1][1] - d[0][1]
        key = (d, gap_change)
        out[key] += 1
        examples.setdefault(key, spec)
for k, v in sorted(out.items(), key=lambda kv: -kv[1]):
    print(f"n={v:3d} marker shifts (dt mod 7, dx) left,right = {k[0]}  gap change {k[1]:+d}  e.g. {examples[k]}")
