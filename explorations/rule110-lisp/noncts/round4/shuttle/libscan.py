"""Front scan of LIBRARY right-movers (v > -4/15) against E^n, all classes,
n in NS. Writes one json line per (X, class) with the product list per n.
Usage: python libscan.py out.jsonl [n1,n2,...]"""
import sys, json, os, time
sys.dont_write_bytecode = True
import numpy as np
from fractions import Fraction
from frontsim import placements, BG, run_row, lib, ether_bit
from collide import products_of
from rod import GL, TILE

T = 900
out = sys.argv[1]
NS = [int(v) for v in sys.argv[2].split(",")] if len(sys.argv) > 2 else [8, 9, 10, 11]
Gj = {g['name']: g for g in json.load(open('../../collider/gliders.json'))['gliders']}
names = [n for n, g in Gj.items() if Fraction(g['velocity']) > Fraction(-4, 15)]
bgs = {n: BG(n, T + 60, -2 * T - 600, 4 * n + 2 * T + 300) for n in NS}
done = set()
if os.path.exists(out):
    done = {json.loads(l)["X"] for l in open(out)}
t0 = time.time()
for X in names:
    if X in done:
        continue
    g = Gj[X]
    gl = GL[X]
    bits, lph, rph, off = gl.phases[0]
    lp = lph % TILE
    row = [ether_bit(0, 0, x) for x in range(lp)] + [int(c) for c in bits]
    pR = (rph - lph) % TILE
    res = {}
    for n in NS:
        bg = bgs[n]
        pls = placements(row, pR, g['p'], g['d'], bg.phi_left, -40)
        for k, pl in enumerate(pls):
            lo_x, seg, phiL, offc = pl
            span_lo = lo_x - 2 * T - 100
            span_hi = bg.W + 2 * T + 100
            xs = np.arange(span_lo, span_hi)
            r0 = np.array([ether_bit(phiL, 0, x) if x < lo_x else (seg[x - lo_x] if x < lo_x + len(seg) else bg(0, x)) for x in xs], np.uint8)
            rT = run_row(r0, T)
            try:
                ok, pr, _ = products_of(lib(), rT[T + 5:-T - 5], span_lo + T + 5, T)
                res.setdefault(k, {})[n] = [p[0] for p in pr] + ([] if ok else ["UNSETTLED"])
            except RuntimeError as e:
                res.setdefault(k, {})[n] = ["EDGE"]
    with open(out, "a") as fh:
        for k, d in res.items():
            fh.write(json.dumps(dict(X=X, cls=k, prods=d)) + "\n")
print("done", round(time.time() - t0))
