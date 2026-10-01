"""Two-rod dump test: R2 = E^m (left), gap, D1, R1 = E^n (right).
D1 dumps R1 into a B-train that then hits R2's back. Products listed."""
import sys, json
sys.dont_write_bytecode = True
import numpy as np
from frontsim import placements, BG, run_row, lib, ether_bit
from collide import products_of
from rod import GL, TILE, build_rod, embed, rod_piece

X = sys.argv[1]; k = int(sys.argv[2]); m = int(sys.argv[3])
GAP2 = int(sys.argv[4]) if len(sys.argv) > 4 else 200
T = 2500
Gj = {g['name']: g for g in json.load(open('../../collider/gliders.json'))['gliders']}
g = Gj[X]; gl = GL[X]
bits, lph, rph, off = gl.phases[0]
row = [ether_bit(0, 0, x) for x in range(lph % TILE)] + [int(c) for c in bits]
pR = (rph - lph) % TILE
r2 = build_rod(m)
for n in range(3, 13):
    bg = BG(n, 10, -2 * T - 2 * GAP2 - 800, 2 * T + 600)
    lo_x, seg, phiL, offc = placements(row, pR, g['p'], g['d'], bg.phi_left, -40)[k]
    # R2 placed left with right ether phase phiL, ending ~GAP2 left of lo_x
    x2 = lo_x - GAP2 - r2["W"]
    while (r2["pr"] - x2) % TILE != phiL:
        x2 -= 1
    pl2 = (r2["pl"] - x2) % TILE
    span_lo, span_hi = x2 - 2 * T - 200, bg.W + 2 * T + 200
    xs = np.arange(span_lo, span_hi)
    r0 = np.array([ether_bit(pl2, 0, x) if x < x2 else
                   (r2["seg"][x - x2] if x < x2 + r2["W"] else
                    (ether_bit(phiL, 0, x) if x < lo_x else
                     (seg[x - lo_x] if x < lo_x + len(seg) else bg(0, x)))) for x in xs], np.uint8)
    p0 = products_of(lib(), r0[T:-T], span_lo + T, 0)[1]
    rT = run_row(r0, T)
    ok, pr, _ = products_of(lib(), rT[T + 5:-T - 5], span_lo + T + 5, T)
    print(n, [q[0] for q in p0], "->", [q[0] for q in pr], ok, flush=True)
