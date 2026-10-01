"""Decoder-free multi-read check of a Cook machine with SURGERY: the run is
stopped at t_in, an Ebar-frame region is rewritten (ether + objects), and
the run continues. Read outcomes per appendant region as in
splice.read_outcomes_row (settled region: 0 Ebar clusters = N, 4 per
symbol (+-2) = Y, else '!').
Reference: queue machine with per-read leader kinds ('K' normal, 'F'
forced N: consumes, appends nothing)."""
from collections import deque
import numpy as np
from q import *
import encoder as enc
from census import census, MAX_DT
from engine import ETHER
ETH = np.array([int(c) for c in ETHER], dtype=np.uint8)

def reference(tape, apps, kinds, n):
    q = deque(tape); out = ""
    for i in range(n):
        if not q:
            break
        s = q.popleft()
        if kinds[i] == "F":
            out += "N"
        else:
            out += s
            if s == "Y":
                q.extend(apps[i % len(apps)])
    return out

def regions_of(m, nread):
    lead = [(a, b) for n, a, b in m.blocks if n in "GKX"]
    return [(b1, a2) for (a1, b1), (a2, b2) in zip(lead, lead[1:])][:nread]

def ebar_shift(origin, t):
    from casim import EBAR_VELOCITY
    return origin + int(round(EBAR_VELOCITY * t))

def rewrite(row, origin, t, lo, hi, items):
    """Rewrite Ebar-frame global [lo, hi) of a lab row at time t as ether +
    items [(tiles, k, xglob)] left to right; None if phases do not fit."""
    sh = ebar_shift(origin, t)
    a, b = lo + sh, hi + sh
    p, pb = phase_at(row, a), phase_at(row, b - TILE)
    new = row.copy(); pos = a
    for tiles, k, xg in items:
        arr, cl, cr = tiles[k]
        x = xg + sh
        if x < pos or x + len(arr) > b or (cl - x) % TILE != p:
            return None
        new[pos:x] = ETH[(p + np.arange(pos, x)) % TILE]
        new[x:x + len(arr)] = arr
        pos = x + len(arr); p = (cr - x) % TILE
    if p != pb:
        return None
    new[pos:b] = ETH[(p + np.arange(pos, b)) % TILE]
    return new

def outcomes(r, regions, T, per_symbol, every=600, lookahead=4, margin=3000, tol=2):
    """splice.read_outcomes_row continued from an existing Run r."""
    before = [None] * len(regions); last = [None] * len(regions)
    state = ["." for _ in regions]; read_at = [None] * len(regions)
    while r.t + every <= T and any(s in ".r" for s in state):
        pending = [j for j, s in enumerate(state) if s in ".r"][:lookahead]
        lo_g = min(regions[j][0] for j in pending) - margin
        hi_g = max(regions[j][1] for j in pending) + margin
        r.step(every - MAX_DT)
        sh = r.ebar_frame(r.t + MAX_DT)
        cs = census(r.history(lo_g + sh, hi_g + sh, MAX_DT))
        rel = [(a + lo_g, k) for a, b, k in cs]
        for j in pending:
            a, b = regions[j]
            inside = tuple(c for c in rel if a <= c[0] < b)
            if before[j] is None:
                before[j] = inside
            elif state[j] == "." and inside != before[j]:
                state[j], read_at[j] = "r", r.t
            elif (state[j] == "r" and inside == last[j]
                  and not any(k in "CA?" for _, k in inside)):
                n_e = sum(1 for _, k in inside if k == "E")
                expect = 4 * per_symbol[j]
                if n_e == 0:
                    state[j] = "N"
                elif abs(n_e - expect) <= tol:
                    state[j] = "Y"
                else:
                    state[j] = "!"
            last[j] = inside
    return "".join(s if s in "YN!" else "." for s in state), read_at

def check(tape, apps, nread, surgery=None, v=None, T=None):
    """surgery(m, row_at_tin) -> new row, applied at surgery.t_in.
    Returns (observed, read times)."""
    v = v or enc._left_v(apps)
    T = T or (nread + 3) * 2 * 30 * v
    m = Machine(tape, apps, T, v=v, left_periods=T // (30 * v) + 3,
                right_periods=nread // len(apps) + 3)
    regs = regions_of(m, nread)
    r = Run(m.row, m.origin)
    if surgery is not None:
        # outcomes() steps in units of `every`; do the surgery at t_in exactly
        r.step(surgery.t_in)
        row = r.window(0, r.width)
        new = surgery(m, row)
        if new is None:
            raise ValueError("surgery does not fit")
        r2 = Run(new, m.origin); r2.t = r.t; r = r2
    got, times = outcomes(r, regs, T, [len(apps[j % len(apps)]) for j in range(nread)])
    return got, times, m


def rewrite2(row, origin, t, lo, hi, items, mingap=3):
    """rewrite() allowing tiles to overlap in their 16-cell ether margins
    (cores >= mingap apart), as zscreen.build2."""
    sh = ebar_shift(origin, t)
    a, b = lo + sh, hi + sh
    p, pb = phase_at(row, a), phase_at(row, b - TILE)
    new = row.copy()
    new[a:b] = ETH[(p + np.arange(a, b)) % TILE]
    core_end = a - mingap
    for tiles, k, xg in items:
        arr, cl, cr = tiles[k]
        x = xg + sh
        if x + 16 < core_end + mingap or x < a or x + len(arr) > b or (cl - x) % TILE != p:
            return None
        s0 = max(0, core_end - x)
        new[x + s0:x + len(arr)] = arr[s0:]
        core_end = x + len(arr) - 16
        p = (cr - x) % TILE
        new[x + len(arr):b] = ETH[(p + np.arange(x + len(arr), b)) % TILE]
    if p != pb:
        return None
    return new

def tiles_of(name):
    return ebar_tiles() if name == "Ebar" else glider_tiles(name)
