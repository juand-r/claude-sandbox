"""Sweep of fullstop.py: v1 = 0 (R1's zero sends B^3) over 30 arrival shifts
(14 cells each, ~60 steps of arrival time); controls v1 = 1, 2 (no B^3:
the window must keep walking, 40 x 11.2 = 448) and K3 placed in R1-class 1
(catalog: E + K3 #1 -> Ebar + D1 + D1, no B^3). Exact CA. Writes the
t = 0 object states and run length of every scene to fullstop_scenes.json
(states are (bits, lph, rph, start) in collider r110lib conventions; build
with r110lib.build_row and run T steps)."""
import json
import fullstop
from fullstop import *  # noqa

recs = []


def go(v1, shift, cls=0):
    items = r1_program("T", [cls])
    old = fullstop.r1_program
    fullstop.r1_program = lambda a, b: items
    states, ref = scene(v1, 40, 20, 1200, shift)
    fullstop.r1_program = old
    row, x0 = build_row(states, pad=200)
    st = sorted(states, key=lambda s: s[3])
    w = Window(row, x0, (st[0][1] - st[0][3]) % TILE, (st[-1][2] - st[-1][3]) % TILE)
    T = int(15 * (states[-1][3] + 3000))
    w.run(T)
    ok, prods = ident(w)
    out = [(p[0], round(float(lat(p) - ref), 2)) if p[1] is not None else (p[0],) for p in prods]
    recs.append({"v1": v1, "shift": shift, "k3class": cls, "T": T, "wl_ref": float(ref),
                 "states": [[s[0], int(s[1]), int(s[2]), int(s[3])] for s in states], "products": out})
    print(v1, shift, cls, out, flush=True)
    return out


for sh in range(0, 30):
    go(0, sh)
for sh in (0, 1, 7, 13):
    go(1, sh)
    go(2, sh)
for sh in (1, 2, 3):
    go(0, sh, cls=1)
json.dump(recs, open(os.path.join(HERE, "fullstop_scenes.json"), "w"))
