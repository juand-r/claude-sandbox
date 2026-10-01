"""Edit the table data of a Cook assembly at t = 0 and run it exactly.

Everything right of the central region is Ebar-speed material evolving
freely until the answer (acceptor/rejector) or the tape reaches it, so a
t = 0 row in which some component region is replaced by other Ebar-speed
material is a legitimate initial condition. This module:

- builds the Cook row (casim.padded_row) and the global spans of blocks;
- replaces a region [a, b) of the table (which must start and end in
  clean ether) by ether plus Ebars at chosen lattice placements, keeping
  the ether phase consistent at b (else the placement is rejected);
- runs it (casim.Run, plain cyclic packed engine, pads sized for T) and
  censuses the table in the Ebar frame.

An Ebar placement is (k, o): the Ebar evolved k steps (0..29) in
isolation, whose cropped cells (with ether margins) start at offset o
from a. For a given k only o = const (mod 14) matches the ether; others
are rejected.
"""

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "noncts" / "scholar"))
from casim import Run, padded_row  # noqa: E402
from census import MAX_DT, census, clusters, ether_phase  # noqa: E402
from encoder import assemble  # noqa: E402
from engine import ETHER, parse, step  # noqa: E402
import r110check as rc  # noqa: E402

TILE = 14
EBAR_V = (-8, 30)


def phase_at(row, x):
    """Ether phase c (cell y = ETHER[(c + y) % 14]) of the window at x."""
    c = ether_phase(row[x:x + TILE])[0]
    if c < 0:
        raise ValueError(f"no ether at {x}")
    return (c - x) % TILE


@lru_cache(None)
def ebar_tiles(spec="E-(A,f1_1)", margin=16, period=30):
    """`period` arrays: an isolated glider (default Ebar) after k steps,
    cropped with ether margins, plus (left phase, right phase) in the
    array's own coordinates."""
    row = parse(ETHER * 40 + rc.PHASES[spec] + ETHER * 40)
    out = []
    for k in range(period):
        cl = clusters(row)
        a, b = cl[0][0] - margin, cl[-1][1] + margin
        arr = row[a:b].copy()
        out.append((arr, phase_at(arr, 0), phase_at(arr, len(arr) - TILE)))
        row = step(row)
    return out


def fill_ether(n, c, x0):
    """n ether cells starting at global x0 with phase c."""
    return np.array([int(ETHER[(c + x0 + j) % TILE]) for j in range(n)],
                    dtype=np.uint8)


def replace_region(row, a, b, placements):
    """New row with [a, b) replaced by ether + Ebars; None if the ether
    phase at b does not match or Ebars overlap. placements: (k, o)."""
    c = phase_at(row, a)
    cb = phase_at(row, b)
    seg = []
    pos = a
    for k, o in sorted(placements, key=lambda p: p[1]):
        arr, cl, cr = ebar_tiles()[k]
        x = a + o
        if x < pos or x + len(arr) > b:
            return None
        if (cl - x) % TILE != c:
            return None
        seg.append(fill_ether(x - pos, c, pos))
        seg.append(arr)
        pos = x + len(arr)
        c = (cr - x) % TILE
    if c != cb:
        return None
    seg.append(fill_ether(b - pos, c, pos))
    new = row.copy()
    new[a:b] = np.concatenate(seg)
    return new


class Machine:
    """A Cook assembly as a t = 0 row plus block spans (global columns)."""

    def __init__(self, tape, apps, T, v=None, right_periods=2, right_names=None,
                 left_names=None, left_periods=1, central=None):
        self.T = T
        if right_names is not None:
            self.row, self.origin, self.blocks = custom_row(
                tape, right_names, T + 2000, left_names, central)
            return
        self.row, self.origin = padded_row(tape, apps, left_periods=left_periods,
                                           right_periods=right_periods,
                                           left_pad=T + 2000, right_pad=T + 2000,
                                           v_override=v)
        _, placed = assemble(tape, apps, left_periods, right_periods, v_override=v)
        self.blocks = [(p.block.name, p.gspan(0)[0], p.gspan(0)[1]) for p in placed]

    def span(self, name, index):
        """Global span of the index-th block with this name (right side)."""
        hits = [(a, b) for n, a, b in self.blocks if n == name]
        return hits[index]

    def run(self, row, T, lo, hi):
        """Run row for T steps; census over Ebar-frame global [lo, hi)."""
        r = Run(row, self.origin)
        r.step(T - MAX_DT)
        sh = r.ebar_frame(T)
        h = r.history(lo + sh, hi + sh, MAX_DT)
        return [(a + lo, b + lo, k) for a, b, k in census(h)]


def ether_cut(row, x, search=60, tight=False):
    """Nearest position to x (array coords) with clean ether on
    [x - 14, x + 14), so a region may start or end there. tight: only
    [x, x + 14) must be ether (enough for insert_items / shifts)."""
    for d in sorted(range(-search, search + 1), key=abs):
        y = x + d
        if tight:
            if ether_phase(row[y:y + TILE])[0] >= 0 and ether_phase(row[y - 1:y - 1 + TILE])[0] < 0:
                return y
            continue
        ph = ether_phase(row[y - TILE:y + TILE])
        if ph[0] >= 0 and ph[TILE] >= 0 and (ph[0] - (y - TILE)) % TILE == (ph[TILE] - y) % TILE:
            return y
    raise ValueError(f"no ether cut near {x}")


def defects_in(row, a, b):
    """Defect clusters of row inside [a, b) (array coords)."""
    return [(x, y) for x, y in clusters(row[a - 30:b + 30]) if a <= x + a - 30 < b]


def trace(machine, row, times, lo, hi, all_types=False):
    """Census at each time (ascending) in Ebar-frame global [lo, hi)."""
    r = Run(row, machine.origin)
    out = []
    for t in times:
        r.step(t - MAX_DT - r.t)
        sh = r.ebar_frame(t)
        h = r.history(lo + sh, hi + sh, MAX_DT)
        cs = [(a + lo, b + lo, k) for a, b, k in census(h)]
        out.append((t, cs))
    return out


def evolve_free(seg, s, pad=64):
    """Evolve an ether-bounded segment s steps in isolation, with ether
    continuing on both sides; returns the evolved array INCLUDING `pad`
    cells of ether on each side (index j <-> original index j - pad)."""
    cl = phase_at(seg, 0)
    cr = phase_at(seg, len(seg) - TILE)
    row = np.concatenate([fill_ether(pad, cl, -pad), seg,
                          fill_ether(pad, cr, len(seg))])
    for _ in range(s):
        row = step(row)
    return row


def shift_remainder(row, c, s, m):
    """Row with everything from array index c on (the remainder: free
    Ebar-speed material) translated in spacetime: evolved s steps in
    isolation, then re-attached so that its first glider starts at least
    14 cells right of c, at the first ether-consistent offset, plus 14*m.
    Returns (new row, displacement of the remainder's cells)."""
    pad = 64
    c0 = phase_at(row, c)
    ext = evolve_free(row[c:].copy(), s, pad)
    ext[:32] = fill_ether(32, phase_at(ext, 32), 0)   # wrap-seam garbage
    ext[-32:] = fill_ether(32, phase_at(ext, len(ext) - 32 - TILE), len(ext) - 32)
    lp = phase_at(ext, 0)
    f = next(x for x in range(len(ext)) if ether_phase(ext[x:x + TILE])[0] < 0)
    # ext[j] goes to index c + j - pad + d; ether phase continuity:
    # (lp - (c - pad + d)) % 14 == c0
    d = (lp - c + pad - c0) % TILE
    while f - pad + d < 0:
        d += TILE
    d += TILE * m
    start = c - pad + d               # index of ext[0]
    k = c - start                     # ext cells before c are dropped
    if k < 0:
        body = np.concatenate([fill_ether(-k, c0, c), ext])
    else:
        body = ext[k:]
    new = np.concatenate([row[:c], body])
    if len(new) >= len(row):
        new = new[:len(row)]
    else:
        new = np.concatenate([new, fill_ether(len(row) - len(new),
                                              phase_at(new, len(new) - TILE), len(new))])
    return new, d


def custom_row(tape, right_names, pad, left_names=None, central=None):
    """Assemble Cook blocks with an arbitrary right-side block sequence
    (after the central region). Returns (row, origin, blocks) with ether
    pads of `pad` cells, like casim.padded_row."""
    import encoder as enc
    from casim import ether_pad, ether_rotation, trim_right_to_ether
    blocks, t0 = enc.load_blocks()
    if central is None:
        central = "".join("FD" if c == "Y" else "ED" for c in tape)
        central = "C" + central[:-1] + "G"
    c = enc.Placed(blocks["C"], -t0, 0)
    placed = [c]
    for name in central[1:] + right_names:
        placed.append(enc._attach(placed[-1], blocks[name], "R"))
    left = [c]
    for name in (left_names if left_names is not None else enc.OSSIFIER + "A" * 600):
        left.append(enc._attach(left[-1], blocks[name], "L"))
    placed = left[:0:-1] + placed
    bits = np.array([int(ch) for ch in "".join(p.gbits(0) for p in placed)], np.uint8)
    origin = -placed[0].gspan(0)[0]
    bits = trim_right_to_ether(bits)
    rl, rr = ether_rotation(bits[:TILE]), ether_rotation(bits[-TILE:])
    lp = ether_pad(rl, pad)
    row = np.concatenate([lp, bits, ether_pad(rr, pad)])
    return row, origin + len(lp), [
        (p.block.name, p.gspan(0)[0], p.gspan(0)[1]) for p in placed]


def insert_items(row, c, placements, s=0, m=0):
    """Insert Ebars (k, o) after array index c (o = offset from c of the
    tile start; per k only one residue mod 14 fits and o is rounded up to
    it), then re-attach the remainder row[c:] translated by (s, m) as in
    shift_remainder. Returns the new row."""
    c0 = phase_at(row, c)
    seg = []
    pos, cph = c, c0
    for pl in sorted(placements, key=lambda p: p[1]):
        k, o = pl[:2]
        tiles = ebar_tiles() if len(pl) == 2 else ebar_tiles(pl[2], 16, pl[3])
        arr, cl, cr = tiles[k]
        x = c + o
        x += (cl - x - cph) % TILE          # smallest x' >= x with ether match
        if x < pos:
            return None
        seg.append(fill_ether(x - pos, cph, pos))
        seg.append(arr)
        pos = x + len(arr)
        cph = (cr - x) % TILE
    seg.append(fill_ether(TILE, cph, pos))
    pos += TILE
    head = np.concatenate([row[:c]] + seg)
    # attach remainder at pos with phase cph: reuse shift_remainder on a
    # row whose prefix is `head` and whose remainder is row[c:]
    tmp = np.concatenate([head, row[c:]])
    # fix the seam: shift_remainder aligns the remainder to the phase at pos
    rem_row, d = _attach_remainder(head, row[c:], s, m)
    return rem_row[:len(row)] if len(rem_row) >= len(row) else None


def _attach_remainder(head, rem, s, m):
    pad = 64
    c = len(head)
    c0 = phase_at(head, c - TILE)
    ext = evolve_free(rem.copy(), s, pad)
    ext[:32] = fill_ether(32, phase_at(ext, 32), 0)
    ext[-32:] = fill_ether(32, phase_at(ext, len(ext) - 32 - TILE), len(ext) - 32)
    lp = phase_at(ext, 0)
    f = next(x for x in range(len(ext)) if ether_phase(ext[x:x + TILE])[0] < 0)
    d = (lp - c + pad - c0) % TILE
    while f - pad + d < 0:
        d += TILE
    d += TILE * m
    start = c - pad + d
    k = c - start
    body = np.concatenate([fill_ether(-k, c0, c), ext]) if k < 0 else ext[k:]
    return np.concatenate([head, body]), d


# Spacetime displacements (-s, D) of "leader K and everything after it"
# that keep reads 0 and 1 correct for all four tapes (scan_shift2.log:
# (0,0), (6,24), (18,16) valid; 57 other shifts fail). They are the
# lattice V = <(12, 8), (30, -8)>; listed as (s, D) with s = evolve steps.
def valid_shifts(max_d=400):
    out = []
    for k in range(-20, 21):
        for j in range(-20, 21):
            t, x = 12 * k + 30 * j, 8 * k - 8 * j
            if -29 <= t <= 0 and -60 <= x <= max_d:
                out.append((-t, x))
    return sorted(set(out), key=lambda p: p[1])


def insert_exact(row, c, placements, s, D):
    """Insert Ebars (k, o) after array index c (exact offsets o from c, must
    match the ether; see insert_items) and re-attach row[c:] displaced by
    (-s, D) in spacetime (evolved s steps, shifted D cells). Returns None if
    the ether does not match at the seam or material would overlap."""
    c0 = phase_at(row, c)
    seg, pos, cph = [], c, c0
    for pl in sorted(placements, key=lambda p: p[1]):
        k, o = pl[:2]
        tiles = ebar_tiles() if len(pl) == 2 else ebar_tiles(pl[2], 16, pl[3])
        arr, cl, cr = tiles[k]
        x = c + o
        if x < pos or (cl - x) % TILE != cph:
            return None
        seg.append(fill_ether(x - pos, cph, pos))
        seg.append(arr)
        pos, cph = x + len(arr), (cr - x) % TILE
    pad = 64
    ext = evolve_free(row[c:].copy(), s, pad)
    ext[:32] = fill_ether(32, phase_at(ext, 32), 0)
    start = c - pad + D                   # array index of ext[0]
    f = next(x for x in range(len(ext)) if ether_phase(ext[x:x + TILE])[0] < 0)
    if start + f < pos:                   # remainder's first glider window
        return None
    if (phase_at(ext, 0) - start) % TILE != cph:
        return None                       # slip of the inserted material != 0
    k = pos - start
    head = np.concatenate([row[:c]] + seg)
    new = np.concatenate([head, ext[k:]])
    if len(new) < len(row):
        return None
    return new[:len(row)]


def lab_trace(machine, row, times, lo, hi):
    """Census in the LAB frame over global columns [lo, hi) at each time."""
    r = Run(row, machine.origin)
    out = []
    for t in times:
        r.step(t - MAX_DT - r.t)
        h = r.history(lo + machine.origin, hi + machine.origin, MAX_DT)
        out.append((t, [(a + lo, b + lo, k) for a, b, k in census(h)]))
    return out


@lru_cache(None)
def glider_tiles(name, margin=16):
    """Tiles (arr, left phase, right phase) for each phase of a glider from
    collider/gliders.json, isolated in ether with `margin` cells each side."""
    import json
    sys.path.insert(0, str(ROOT / "noncts" / "collider"))
    from r110lib import Glider, build_row
    g = {j["name"]: j for j in json.load(open(ROOT / "noncts" / "collider" / "gliders.json"))["gliders"]}
    G = Glider.from_json(g[name])
    out = []
    for k in range(G.p):
        bits, lph, rph, off = G.phases[k]
        row, x0 = build_row([(bits, lph, rph, 0)], pad=margin)
        arr = np.array(row[:margin + len(bits) + margin], dtype=np.uint8)
        out.append((arr, phase_at(arr, 0), phase_at(arr, len(arr) - TILE)))
    return out


def replace_exact(row, c, c2, placements, s, D):
    """Like insert_exact, but the material in [c, c2) is dropped: the head is
    row[:c] + placements, and row[c2:] is re-attached displaced by (-s, D)
    relative to its original position. placements: (tiles, k, o) with
    tiles a list as returned by ebar_tiles / glider_tiles."""
    c0 = phase_at(row, c)
    seg, pos, cph = [], c, c0
    for tiles, k, o in sorted(placements, key=lambda p: p[2]):
        arr, cl, cr = tiles[k]
        x = c + o
        if x < pos or (cl - x) % TILE != cph:
            return None
        seg.append(fill_ether(x - pos, cph, pos))
        seg.append(arr)
        pos, cph = x + len(arr), (cr - x) % TILE
    pad = 64
    ext = evolve_free(row[c2:].copy(), s, pad)
    ext[:32] = fill_ether(32, phase_at(ext, 32), 0)
    start = c2 - pad + D
    f = next(x for x in range(len(ext)) if ether_phase(ext[x:x + TILE])[0] < 0)
    if start + f < pos:
        return None
    if (phase_at(ext, 0) - start) % TILE != cph:
        return None
    k = pos - start
    if k < 0:
        seg.append(fill_ether(-k, cph, pos))
        k = 0
    new = np.concatenate([row[:c]] + seg + [ext[k:]])
    if len(new) < len(row):
        return None
    return new[:len(row)]
