"""Rod 'dumps': a right-mover X hits E^n's front and the whole rod turns
into a left-moving B-family train. For each X (library glider name) and
each class, list the products for n = 2..NMAX (exact simulation)."""
import sys, json
sys.dont_write_bytecode = True
import numpy as np
from frontsim import placements, BG, run_row, lib, ether_bit
from collide import products_of

T = 900
X = sys.argv[1]
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 16
G = {g['name']: g for g in json.load(open('../../collider/gliders.json'))['gliders']}
g = G[X]
# frame row of X: library phase 0 with left my-phase 0: find bits by building
from rod import GL, TILE
gl = GL[X]
bits, lph, rph, off = gl.phases[0]
# library: cells left of s read ETHER[(lph + y - s)], i.e. my-phase lph - s at t=0;
# put s = lph so the left phase is 0
# frame with left phase 0: library frame phase is lph, so prepend lph cells
lp = lph % TILE
row = [ether_bit(0, 0, x) for x in range(lp)] + [int(c) for c in bits]
pR = (rph - lph) % TILE
for n in range(2, NMAX + 1):
    bg = BG(n, T + 60, -2 * T - 600, 4 * n + 2 * T + 300)
    out = []
    for pl in placements(row, pR, g['p'], g['d'], bg.phi_left, -40):
        lo_x, seg, phiL, offc = pl
        span_lo, span_hi = lo_x - 2 * T - 100, bg.W + 2 * T + 100
        xs = np.arange(span_lo, span_hi)
        r0 = np.array([ether_bit(phiL, 0, x) if x < lo_x else (seg[x - lo_x] if x < lo_x + len(seg) else bg(0, x)) for x in xs], np.uint8)
        rT = run_row(r0, T)
        try:
            pr = products_of(lib(), rT[T + 5:-T - 5], span_lo + T + 5, T)[1]
            out.append([p[0] for p in pr])
        except RuntimeError as e:
            out.append(str(e))
    print(n, out, flush=True)
