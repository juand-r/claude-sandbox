"""Plant the left-moving E-bg domain wall (lab velocity -3/5, found by the
cone SAT) inside an E^N rod and watch what happens at the rod's front.

Scene at time 0 (rod coordinates): cells left of the wall come from the rod R
at time 0, cells right of it from R' = R at time 3 translated by +5 (the
domain behind the wall is the E-bg at time offset 3, shift 5), and the wall
itself is cut from the cone witness.
Usage: python3 plant_wall.py N wall_pos_from_front T"""
import sys
import numpy as np
import cone
import objlib as O

N, WPOS, TT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
bg = cone.Background(O.EBG)

# -- the wall, from the cone witness (bg coordinates, time 600 = phase 0)
T = 90
m = cone.ConeModel(bg, 0, 0, T, T)
x, w0 = m.extreme("left")
TW = 600
pad = 2 * TW + 50
lo = m.a - pad
full = np.array([m.bgbit(0, y) for y in range(lo, m.b + pad)], np.uint8)
full[m.a - lo:m.b - lo] = w0
rW = O.evolve(full, TW)              # covers [lo+TW, ...)
xsW = lo + TW
bgr = np.array([bg.bit(TW, y) for y in range(xsW, xsW + len(rW))], np.uint8)
wl = xsW + int(np.nonzero(rW != bgr)[0][0])     # leftmost deviation
SEG = (wl - 30, wl + 40)
seg = rW[SEG[0] - xsW:SEG[1] - xsW]
# check right part of seg is the (3,5) domain
r35 = bg.row_at(TW + 3)
assert all(seg[i] == r35[(SEG[0] + i - 5) % 10] for i in range(45, 70)), "right domain"

# -- the rod
b, l, r = O.en_bits(N)
row, x0, objs, c = O.build([("raw", b, l, r, 0, f"E^{N}")], pad=2 * TT + 400)
s_front = objs[0][1]
rowR3 = O.evolve(row, 3)             # covers [x0+3, ...)
# align bg coordinates with rod coordinates: find r0 with interior == bg row shifted
mid = s_front + len(b) // 2
r0 = None
for cand in range(10):
    if all(row[y - x0] == bg.bit(0, y - cand) for y in range(mid - 15, mid + 15)):
        r0 = cand
assert r0 is not None
# wall placed at rod column WP = s_front + WPOS, congruent to wl + r0 mod 10
WP = s_front + WPOS
WP += (wl + r0 - WP) % 10
shift = WP - wl                       # rod col = bg col + shift
scene = row.copy()
# right part from R' : cell y = R(3)[y - 5]
for y in range(SEG[0] + shift, x0 + len(row)):
    i = y - 5 - (x0 + 3)
    if 0 <= i < len(rowR3):
        scene[y - x0] = rowR3[i]
for i, v in enumerate(seg):
    scene[SEG[0] + shift + i - x0] = v
# sanity: left edge of seg agrees with rod interior
assert all(scene[SEG[0] + shift + i - x0] == row[SEG[0] + shift + i - x0] for i in range(0, 20))

H = O.history(scene, TT)
Hr = O.history(row, TT)
print(f"E^{N}: front at {s_front}, wall planted at {WP} ({WP - s_front} cells behind the front)")
for t in range(0, TT + 1, max(1, TT // 40)):
    a, ar = H[t], Hr[t]
    xs = x0 + t
    cf = s_front + int(round(-4 * t / 15))
    w_lo, w_hi = cf - 120, cf + 120
    def cell(y):
        v, vr = a[y - xs], ar[y - xs]
        if v != vr:
            return "X" if v else "o"
        return "1" if v else "_"
    print(f"{t:5d} " + "".join(cell(y) for y in range(w_lo, w_hi)))
np.save("plant_wall_last.npy", H[TT])
print("final types:", O.types_rods(H[TT], x0 + TT))
print("reference   :", O.types_rods(Hr[TT], x0 + TT))
