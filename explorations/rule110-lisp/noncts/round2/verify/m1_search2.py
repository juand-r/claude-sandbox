"""Redo of m1_search.py with a RIGID, right-anchored stream and the counter
set by the program itself: fresh E, [GB5]*v, GB3 test, G conv (+35,+62),
then X collector at (dt, dx) relative to the G. Want: every v in 0..4 ends
with ONE counter and nothing else; report m(v)."""
import sys
import vlib, libgen
libgen.load()
SP = 70
def val(nm):
    if nm == "E": return 0
    if nm.startswith("E^"): return int(nm[2:]) - 1
    return None
def scene(v, X, dt, dx):
    items = [("E", 0, 0)]
    x = 60
    for i in range(v):
        items.append(("GB5", 0, x)); x += SP
    items += [("GB3", 1, x + 30), ("G", 36, x + 84), (X, 36 + dt, x + 84 + dx)]
    return items
hits = 0
for X in sys.argv[1].split(","):
    for dt in range(42):
        for dx in range(28, 170, 14):
            ms = []
            for v in (0, 2, 3, 4):
                T = 4000 + 1100 * v + 16 * dx
                try:
                    row, org, placed = vlib.build_right(scene(v, X, dt, dx), T=T)
                except ValueError:
                    ms = None; break
                r = vlib.evolve(row, T)
                ids = [n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T)]
                if len(ids) != 1 or val(ids[0]) is None:
                    ms = None; break
                ms.append((v, val(ids[0])))
            if ms:
                hits += 1
                print(X, dt, dx, placed[-1], sorted(ms), flush=True)
print("hits", hits, flush=True)
