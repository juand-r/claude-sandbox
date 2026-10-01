"""Inject the E-infinity defect found by ebg_search.py (single deviating
cell, period (5,2) on the ring, i.e. velocity +2/5) into the interior of a
real rod E^n in ether, and watch what happens (exact engine, my typer).
The defect moves right at +2/5 while the rod moves left at -4/15, so it
should reach the rod's BACK face after ~ (rod length) / (2/3) steps."""
import sys, re
import numpy as np
import v3, vlib, engine
import ebg_search as S

line = [l for l in open("ebg_search.log") if "span=1 " in l or l.rstrip().endswith("span=1")][0]
m = re.search(r"k=(\d+) x=(\d+) bits=(\d+)", line)
k, x, bits = int(m[1]), int(m[2]), m[3]
ring = S.VAR[0].copy()
ring[x:x + k] = [int(c) for c in bits]
r = engine.unpack(engine.step_packed_n(engine.pack(ring), S.T0), S.W)
mask = S.deviation(r)
p = int(np.nonzero(mask)[0][0])
assert mask.sum() == 1
bgwin = r.copy(); bgwin[p] ^= 1
H = 12
pat_bg = bgwin[p - H:p + H + 1]          # background around the defect
pat_def = r[p - H:p + H + 1]


def inject(n, which=0, T=4000):
    objs, row, org, placed = v3.run([(f"E^{n}", 0, 0)], 0)
    hits = [i for i in range(H, len(row) - H - 1) if np.array_equal(row[i - H:i + H + 1], pat_bg)]
    if not hits:
        return None, None
    i = hits[min(which, len(hits) - 1)]
    row2 = row.copy()
    row2[i] ^= 1
    pad = 2 * T + 200
    E = vlib.ETHER
    full = np.concatenate([E[(np.arange(org - pad, org) + phase_left(row, org)) % 14], row2,
                           E[(np.arange(org + len(row), org + len(row) + pad) + phase_right(row, org)) % 14]])
    out = engine.unpack(engine.step_packed_n(engine.pack(full), T), len(full))
    return [(v3.base(nm), xx) for nm, xx, w, kk in vlib.identify(out, org - pad, T=T)], (len(hits), i)


def phase_left(row, org):
    for c in range(14):
        if np.array_equal(row[:14], vlib.ETHER[(np.arange(org, org + 14) + c) % 14]):
            return c


def phase_right(row, org):
    n = len(row)
    for c in range(14):
        if np.array_equal(row[n - 14:], vlib.ETHER[(np.arange(org + n - 14, org + n) + c) % 14]):
            return c


if __name__ == "__main__":
    print("defect window:", "".join(map(str, pat_def)), "background:", "".join(map(str, pat_bg)))
    for n in (8, 10, 12, 15):
        for which in (0, 1, 2):
            res, info = inject(n, which)
            print(f"E^{n}, interior site {which} {info}: {res}")
