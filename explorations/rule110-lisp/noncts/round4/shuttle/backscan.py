"""BACK scan: library LEFT-movers (v < -4/15) hitting E^n's back (right
end) from the right, every class, n in NS. Records product lists.
Usage: python backscan.py out.jsonl [n1,n2,..] [namefilter]"""
import sys, json, os, time
sys.dont_write_bytecode = True
import numpy as np
from fractions import Fraction
from frontsim import BG, run_row, lib, ether_bit, simulate, SYNTH
from collide import products_of
from rod import GL, TILE
sys.path.insert(0, SYNTH)
from classes import same_class, n_classes

T = 900


def placements_right(bits, pR, p, d, phir, x_start, PE=(15, -4)):
    """one placement per class of a left-moving train placed RIGHT of the
    rod (its left ether must have global phase phir), starting >= x_start."""
    ncls = n_classes((p, d), PE)
    W = len(bits)
    out = []
    for dt in range(p):
        pad = 3 * dt + 20
        xs = range(-pad, W + pad)
        r0 = np.array([ether_bit(0, 0, x) if x < 0 else (bits[x] if x < W else ether_bit(pR, 0, x)) for x in xs], np.uint8)
        rk = simulate(r0, dt)[dt] if dt else r0
        fr = np.arange(-pad, W + pad)
        le = np.array([ether_bit(0, dt, x) for x in fr])
        re = np.array([ether_bit(pR, dt, x) for x in fr])
        edge = dt + 3
        dl = np.nonzero(rk[edge:-edge] != le[edge:-edge])[0] + edge
        dr = np.nonzero(rk[edge:-edge] != re[edge:-edge])[0] + edge
        a, b = dl[0], dr[-1] + 1
        seg = rk[a:b]
        fa = fr[a]
        # left global phase: frame phase at time dt is 0 + 4dt ... global = 4dt - s
        s0 = (4 * dt - phir) % TILE
        s = x_start - fa
        s += (s0 - s) % TILE
        for j in range(ncls + 1):
            sj = s + TILE * j
            off = (-dt, sj)
            if any(same_class(off, o[3], (p, d), PE) for o in out):
                continue
            out.append((fa + sj, seg, (pR + 4 * dt - sj) % TILE, off))
        if len(out) == ncls:
            break
    assert len(out) == ncls, (len(out), ncls)
    return out


if __name__ == "__main__":
    out = sys.argv[1]
    NS = [int(v) for v in sys.argv[2].split(",")] if len(sys.argv) > 2 else [8, 9, 10, 11]
    Gj = {g['name']: g for g in json.load(open('../../collider/gliders.json'))['gliders']}
    names = [n for n, g in Gj.items() if Fraction(g['velocity']) < Fraction(-4, 15)]
    if len(sys.argv) > 3:
        if sys.argv[3].startswith("="):
            names = sys.argv[3][1:].split(",")
        else:
            names = [n for n in names if sys.argv[3] in n]
    bgs = {n: BG(n, T + 60, -2 * T - 600, 4 * n + 2 * T + 900) for n in NS}
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
            for k, pl in enumerate(placements_right(row, pR, g['p'], g['d'], bg.phi_right, bg.W + 40)):
                lo_x, seg, phiR, offc = pl
                span_lo = -2 * T - 100
                span_hi = lo_x + len(seg) + 2 * T + 200
                xs = np.arange(span_lo, span_hi)
                r0 = np.array([bg(0, x) if x < lo_x else (seg[x - lo_x] if x < lo_x + len(seg) else ether_bit(phiR, 0, x)) for x in xs], np.uint8)
                rT = run_row(r0, T)
                try:
                    ok, pr, _ = products_of(lib(), rT[T + 5:-T - 5], span_lo + T + 5, T)
                    res.setdefault(k, {})[n] = [p[0] for p in pr] + ([] if ok else ["UNSETTLED"])
                except RuntimeError:
                    res.setdefault(k, {})[n] = ["EDGE"]
        with open(out, "a") as fh:
            for k, d in res.items():
                fh.write(json.dumps(dict(X=X, cls=k, prods=d)) + "\n")
    print("done", round(time.time() - t0))
