"""W3 (route 23): does an input at R1's FRONT launch a wall that reaches the
BACK and leaves one clean rod? For each input (train in all classes, or a
co-moving window object E^j at every small offset) vs E^n (n = 10, 11):
simulate T steps; require exactly one standard rod and nothing moving right
of it (only left-movers elsewhere); then find the back shift v2 = (dt, dx)
with  row_T(x) == bg(T - dt, x - dx)  near the back, and the front shift v1
likewise near the front. A wall changed the rod iff h(v2) != h(v1) where
h(t, s) = 2t - 5s mod 50 (objects' crystal phase, Z/50); h(u) = h(P_E) = 0.
Usage: python w3scan.py trains FILE out.jsonl | windows out.jsonl"""
import sys, json, os, time
sys.dont_write_bytecode = True
import numpy as np
from rod import TILE, ether_bit, simulate, build_rod
from pert import BG
from frontsim import placements, run_row, lib
from collide import products_of

T = 700
NS = (10, 11)
VEL_E = (15, -4)


def h_of(v):
    return (2 * v[0] - 5 * v[1]) % 50


def find_shift(rT, span_lo, bg, xa, xb):
    """(dt, dx) with rT[x] == bg(T - dt, x - dx) on [xa, xb); dt in [0,15),
    dx in [-60, 60]; returns list of matches."""
    seg = rT[xa - span_lo: xb - span_lo]
    out = []
    for dt in range(15):
        t = T - dt
        for dx in range(-60, 61):
            ref = np.array([bg(t, x - dx) for x in range(xa, xb)], np.uint8)
            if np.array_equal(seg, ref):
                out.append((dt, dx))
    return out


def analyse(row, span_lo, bg):
    rT = run_row(row, T)
    a0, b0 = T + 5, len(row) - T - 5
    try:
        ok, pr, objs = products_of(lib(), rT[a0:b0], span_lo + a0, T)
    except RuntimeError as e:
        return dict(kind="edge")
    names = [p[0] for p in pr]
    if not ok or "?" in names:
        return dict(kind="dirty", prods=names)
    idx = [i for i, p in enumerate(pr) if lib().gliders[p[0]].p == 15 and lib().gliders[p[0]].d == -4]
    if len(idx) != 1:
        return dict(kind="dirty", prods=names)
    i = idx[0]
    if i != len(pr) - 1:          # something right of the rod (into the stream)
        return dict(kind="emits_right", prods=names)
    a, b = objs[i][0] + span_lo + a0, objs[i][1] + span_lo + a0   # rod extent at T
    fr = find_shift(rT, span_lo, bg, a - 14, a + 10)
    br = find_shift(rT, span_lo, bg, b - 10, b + 14)
    return dict(kind="rod", prods=names, front=fr[:3], back=br[:3])


def train_rows(tr, n, bg):
    bits = [int(c) for c in tr["bits"]]
    for k, (lo_x, seg, phiL, off) in enumerate(placements(bits, tr["pR"], tr["p"], tr["d"], bg.phi_left, -40)):
        span_lo, span_hi = lo_x - 2 * T - 100, bg.W + 2 * T + 100
        xs = np.arange(span_lo, span_hi)
        row = np.array([ether_bit(phiL, 0, x) if x < lo_x else
                        (seg[x - lo_x] if x < lo_x + len(seg) else bg(0, x)) for x in xs], np.uint8)
        yield k, row, span_lo


def window_rows(j, n, bg, gmax=24):
    """E^j placed left of the rod's front at every time phase dt (0..14)
    and every ether-consistent offset whose gap g (cells between the
    window's last non-ether cell and the rod's first) is in [0, gmax]."""
    r = build_rod(j)
    W = r["W"]
    pad = 80
    fr = np.arange(-pad, W + pad)
    base = np.array([ether_bit(r["pl"], 0, x) if x < 0 else (r["seg"][x] if x < W else ether_bit(r["pr"], 0, x))
                     for x in fr], np.uint8)
    h = simulate(base, 15)
    f0 = bg.front(0)
    for dt in range(15):
        rk = h[dt]
        # translate by +4 dt so the ether is the t = 0 ether
        le = np.array([ether_bit(r["pl"], dt, x) for x in fr])
        re = np.array([ether_bit(r["pr"], dt, x) for x in fr])
        e = dt + 3
        dl = np.nonzero(rk[e:-e] != le[e:-e])[0] + e
        dr = np.nonzero(rk[e:-e] != re[e:-e])[0] + e
        a, b = dl[0], dr[-1] + 1
        seg = rk[a:b]
        fa = fr[a] + 4 * dt                     # frame column (t=0 ether) of seg[0]
        prf = (r["pr"]) % TILE                  # frame right phase (t = 0 frame)
        plf = (r["pl"]) % TILE
        for s in range(-200, 0):
            end = fa + len(seg) + s            # global column after the window
            g = f0 - end
            if not 0 <= g <= gmax:
                continue
            if (prf - s) % TILE != bg.phi_left:
                continue
            lo_x = fa + s
            span_lo, span_hi = lo_x - 2 * T - 100, bg.W + 2 * T + 100
            xs = np.arange(span_lo, span_hi)
            phiL = (plf - s) % TILE
            row = np.array([ether_bit(phiL, 0, x) if x < lo_x else
                            (seg[x - lo_x] if x < lo_x + len(seg) else bg(0, x)) for x in xs], np.uint8)
            yield (dt, g), row, span_lo


def main():
    mode, out = sys.argv[1], sys.argv[-1]
    bgs = {n: BG(n, T + 60, -2 * T - 800, 4 * n + 2 * T + 400) for n in NS}
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["key"] for l in open(out)}
    fh = open(out, "a")
    t0 = time.time()
    if mode == "trains":
        trains = [json.loads(l) for l in open(sys.argv[2])]
        for i, tr in enumerate(trains):
            key = f"{sys.argv[2]}:{i}"
            if key in done:
                continue
            res = {}
            for n in NS:
                for k, row, span_lo in train_rows(tr, n, bgs[n]):
                    r = analyse(row, span_lo, bgs[n])
                    if r["kind"] == "rod":
                        res[f"{n}:{k}"] = r
            fh.write(json.dumps(dict(key=key, bits=tr["bits"], pR=tr["pR"], p=tr["p"], d=tr["d"], res=res), default=int) + "\n")
            if i % 200 == 0:
                fh.flush()
                print(i, round(time.time() - t0), flush=True)
    if mode == "windows":
        for j in (1, 2, 4):
            for n in NS:
                for (dt, g), row, span_lo in window_rows(j, n, bgs[n]):
                    key = f"E^{j}:{n}:{dt}:{g}"
                    if key in done:
                        continue
                    r = analyse(row, span_lo, bgs[n])
                    fh.write(json.dumps(dict(key=key, j=j, n=n, dt=int(dt), g=int(g), **r), default=int) + "\n")
            fh.flush()
            print("window E^%d done" % j, round(time.time() - t0), flush=True)
    fh.close()


if __name__ == "__main__":
    main()
