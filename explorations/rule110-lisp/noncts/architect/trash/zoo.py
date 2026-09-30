"""Quick glider zoo (architect's private scratch tool, NOT the team catalog;
collider owns that). Seeds random windows into ether, evolves, extracts
isolated defects and finds each one's minimal spacetime period (dt, dx)
by testing row_t[x] == row_{t-dt}[x-dx] on the defect plus margin.

A glider is stored as (dt, dx, left_phase, bits, right_phase): `bits` is
the defect region at some time, and the ether to its left/right has
absolute phase left_phase/right_phase relative to the snippet start
(cell k of the left ether reads ETHER[(left_phase + k) % 14] where k is
measured from the snippet's first cell, i.e. k<0 on the left).
"""
import sys
import numpy as np
sys.path.insert(0, "../..")
from engine import ETHER, parse, step, ether_tape
from census import clusters, ether_phase

TILE = 14
EB = parse(ETHER)


def ether_cells(phase, start, n):
    """n ether cells for absolute positions start..start+n-1 with phase."""
    return EB[(phase + np.arange(start, start + n)) % TILE]


def evolve(row, n):
    H = np.empty((n + 1, len(row)), np.uint8)
    H[0] = row
    for t in range(n):
        H[t + 1] = step(H[t])
    return H


def period_of(H, a, b, margin=4, max_dt=120):
    """Minimal (dt, dx) with H[-1][a-m:b+m] == H[-1-dt][a-m-dx:b+m-dx],
    excluding pure-ether lattice shifts. dt ordered ascending."""
    now = H[-1]
    lo, hi = a - margin, b + margin
    for dt in range(1, min(max_dt, len(H) - 1) + 1):
        then = H[-1 - dt]
        for dx in range(-dt, dt + 1):
            if lo - dx < 0 or hi - dx > len(now) or lo < 0 or hi > len(now):
                continue
            if np.array_equal(now[lo:hi], then[lo - dx:hi - dx]):
                return dt, dx
    return None


def discover(trials=3000, width=14 * 80, T=600, seed=0, maxlen=16):
    rng = np.random.default_rng(seed)
    found = {}
    for trial in range(trials):
        row = ether_tape(width)
        L = rng.integers(1, maxlen + 1)
        c = width // 2
        row[c:c + L] = rng.integers(0, 2, L)
        H = evolve(row, T)
        cl = clusters(H[-1])
        # isolated: neighbours at least 30 cells away
        for i, (a, b) in enumerate(cl):
            if b - a > 60:
                continue
            if i > 0 and a - cl[i - 1][1] < 40:
                continue
            if i + 1 < len(cl) and cl[i + 1][0] - b < 40:
                continue
            if a < 150 or b > width - 150:
                continue
            p = period_of(H, a, b)
            if p is None:
                continue
            ph = ether_phase(H[-1])
            lphase = ph[a - TILE - 2]
            rphase = ph[b + 2]
            if lphase < 0 or rphase < 0:
                continue
            key = (p, H[-1][a:b].tobytes())
            if p not in found:
                found[p] = []
            found[p].append((trial, a, b, H[-1][a:b].copy(), int(lphase), int(rphase)))
    return found


if __name__ == "__main__":
    f = discover(trials=int(sys.argv[1]) if len(sys.argv) > 1 else 2000)
    for p in sorted(f, key=lambda p: (p[0], p[1])):
        widths = sorted(set(len(x[3]) for x in f[p]))
        print(p, "speed", p[1] / p[0], "count", len(f[p]), "widths", widths[:8])
