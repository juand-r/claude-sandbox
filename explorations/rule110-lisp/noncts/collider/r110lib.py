"""Core library for the Rule 110 collision catalog.

Conventions (used everywhere in collider/):

Ether. ETHER = "11111000100110", spatial period 14. A row region is ether
with *absolute phase* c if cell y reads ETHER[(c + y) % 14]. The ether is
invariant under the spacetime shifts (dt, dx) = (7, 0) and (3, 2), so the
ether lattice is L = {(7a + 3b, 2b)}; (dt, dx) is in L iff dx is even and
dt - 3*dx/2 = 0 (mod 7). One generation maps absolute phase c to c + 4
(the ether moves by (1, 10) in L).

Objects. A localized object at time t is (bits, lph, rph): its cells as a
'0'/'1' string; if bits[0] sits at column s, cells y < s read
ETHER[(lph + y - s) % 14] and cells y >= s + len(bits) read
ETHER[(rph + y - s) % 14]. (lph, rph) are the *relative* ether phases;
rph - lph (mod 14) is the object's phase slip, a time invariant.

Gliders. A glider has period vector (p, d): after p generations it is the
same object shifted by d. Its library record stores the p phases
k = 0..p-1 as (bits, lph, rph, off), `off` being the column of bits[0]
relative to the phase-0 start. A *seed event* (t0, x0) places phase 0 with
bits[0] at column x0 at time t0; at time t the glider is phase
k = (t - t0) mod p, starting at x0 + off_k + ((t - t0) div p) * d.

Segmentation. A row is cut into ether runs (consecutive matching 14-cell
windows of one phase) and the defects between them (as in ../../census.py).
Defects closer than MERGE cells are merged into one object, so an object is
a maximal group of defects separated by >= MERGE ether cells.
"""

from fractions import Fraction
import math

import numpy as np

ETHER = "11111000100110"
TILE = 14
ETHER_BITS = np.array([int(c) for c in ETHER], dtype=np.uint8)
MERGE = 20          # defects closer than this (in cells) form one object
ETHER_STEP = 4      # absolute ether phase advance per generation


def in_ether_lattice(dt, dx):
    return dx % 2 == 0 and (dt - 3 * (dx // 2)) % 7 == 0


def ether_cells(c, lo, hi):
    """Cells [lo, hi) of ether with absolute phase c."""
    idx = (c + np.arange(lo, hi)) % TILE
    return ETHER_BITS[idx]


# ---------------------------------------------------------------------------
# Evolution

def step_rows(rows):
    """One Rule 110 step on a (B, W) or (W,) uint8 array, cyclic per row."""
    l = np.roll(rows, 1, axis=-1)
    r = np.roll(rows, -1, axis=-1)
    return (rows | r) & (1 - (l & rows & r))


def _pack_batch(rows):
    """(B, W) uint8 -> (W, NB) uint64; bit j of word b = experiment 64b+j."""
    B, W = rows.shape
    pad = (-B) % 64
    if pad:
        rows = np.concatenate([rows, np.zeros((pad, W), np.uint8)])
    bits = np.packbits(rows.T, axis=1, bitorder="little")   # (W, Bpad/8)
    return np.ascontiguousarray(bits).view(np.uint64)


def _unpack_batch(state, B):
    """(W, NB) uint64 -> (B, W) uint8."""
    bits = np.unpackbits(state.view(np.uint8), axis=1, bitorder="little")
    return np.ascontiguousarray(bits[:, :B].T)


def _step_state(s):
    l = np.roll(s, 1, axis=0)
    r = np.roll(s, -1, axis=0)
    return (s | r) & ~(l & s & r)


def evolve_batch(rows, T, keep=0):
    """Evolve B independent cyclic rows (B, W) for T steps (bit-sliced).

    Returns (final (B, W), hist) where hist is None if keep == 0, else a
    (keep + 1, B, W) array of the last keep+1 rows (hist[-1] = final).
    """
    rows = np.asarray(rows, dtype=np.uint8)
    B = rows.shape[0]
    s = _pack_batch(rows)
    kept = []
    for t in range(T):
        if keep and t >= T - keep:
            kept.append(s.copy())
        s = _step_state(s)
    final = _unpack_batch(s, B)
    if not keep:
        return final, None
    kept.append(s)
    hist = np.stack([_unpack_batch(k, B) for k in kept])
    return final, hist


def evolve_hist(row, T):
    """Single row: (T+1, W) spacetime history, cyclic."""
    out = np.empty((T + 1, len(row)), np.uint8)
    out[0] = row
    for t in range(T):
        out[t + 1] = step_rows(out[t])
    return out


# ---------------------------------------------------------------------------
# Segmentation

_WEIGHTS = (1 << np.arange(TILE, dtype=np.int64))
_ROT = {int(sum(int(c) << k for k, c in enumerate(ETHER[r:] + ETHER[:r]))): r
        for r in range(TILE)}
_CODES = np.array(sorted(_ROT), dtype=np.int64)
_ROT_OF = np.array([_ROT[c] for c in _CODES], dtype=np.int64)


def window_phase(row):
    """Per window start x (0..W-14): absolute ether phase or -1."""
    win = np.lib.stride_tricks.sliding_window_view(row.astype(np.int64), TILE)
    codes = win @ _WEIGHTS
    pos = np.searchsorted(_CODES, codes).clip(0, len(_CODES) - 1)
    ok = _CODES[pos] == codes
    x = np.arange(len(codes))
    return np.where(ok, (_ROT_OF[pos] - x) % TILE, -1)


def defects(row):
    """Defects of a (non-cyclic view of a) row: list of (a, b, cL, cR),
    cells [a, b) with absolute ether phase cL to the left, cR to the right.
    Regions touching the row ends are omitted."""
    ph = window_phase(row)
    xs = np.nonzero(ph >= 0)[0]
    if len(xs) == 0:
        return []
    p = ph[xs]
    brk = np.nonzero((np.diff(xs) != 1) | (np.diff(p) != 0))[0]
    out = []
    for i in brk:
        ll, rf = int(xs[i]), int(xs[i + 1])
        a, b = ll + TILE, rf
        if b <= a:
            a, b = rf, ll + TILE
        out.append((a, b, int(p[i]), int(p[i + 1])))
    return out


def objects(row, merge=MERGE):
    """Group defects into objects: list of (a, b, cL, cR)."""
    out = []
    for a, b, cl, cr in defects(row):
        if out and a - out[-1][1] < merge:
            pa, pb, pcl, _ = out[-1]
            out[-1] = (pa, max(pb, b), pcl, cr)
        else:
            out.append((a, b, cl, cr))
    return out


MAX_OBJECT = 120    # a periodic object wider than this is not accepted


def union_object(row):
    """All defects of the row as one object (first start .. last end), or
    None for pure ether. Used for standalone glider tests, where the row
    contains one (possibly compound) object only."""
    objs = objects(row)
    if not objs:
        return None
    return objs[0][0], objs[-1][1], objs[0][2], objs[-1][3]


def obj_key(row, a, b, cl, cr):
    """(bits, lph, rph) of object [a, b) in the placement convention."""
    bits = "".join(map(str, row[a:b]))
    return bits, (cl + a) % TILE, (cr + a) % TILE


def cyclic_view(row, center):
    """Rotate a cyclic row so that column `center` is in the middle; returns
    (rotated row, shift) with rotated[i] = row[(i + shift) % W]."""
    W = len(row)
    shift = (center - W // 2) % W
    return np.roll(row, -shift), shift


# ---------------------------------------------------------------------------
# Period detection

def lattice_dxs(dt, vmax=1.0):
    """dx values with (dt, dx) in the ether lattice and |dx| <= vmax*dt."""
    b0 = (5 * dt) % 7            # 3b = dt (mod 7) <=> b = 5 dt (mod 7)
    lim = int(vmax * dt) // 2
    bs = range(-lim - 7, lim + 8)
    return [2 * b for b in bs if b % 7 == b0 and abs(2 * b) <= vmax * dt]


def find_period(hist, a, b, maxdt=None, margin=3):
    """Smallest (dt, dx) in the ether lattice with hist[-1][a-m:b+m] ==
    hist[-1-dt][a-m-dx:b+m-dx]. None if none up to maxdt. The (dt, dx)
    pairs (7,0),(3,2) are ether symmetries; objects invariant under them
    alone are ether and never reach here."""
    now = hist[-1]
    W = now.shape[0]
    maxdt = maxdt or (len(hist) - 1)
    lo, hi = a - margin, b + margin
    if lo < 0 or hi > W:
        return None
    seg = now[lo:hi]
    for dt in range(1, maxdt + 1):
        then = hist[-1 - dt]
        for dx in lattice_dxs(dt):
            if lo - dx < 0 or hi - dx > W:
                continue
            if np.array_equal(seg, then[lo - dx:hi - dx]):
                return dt, dx
    return None


# ---------------------------------------------------------------------------
# Gliders

class Glider:
    """A verified periodic object (see module docstring)."""

    def __init__(self, name, p, d, phases, note="", parts=None):
        self.name, self.p, self.d, self.note = name, p, d, note
        self.phases = phases        # list of (bits, lph, rph, off)
        # compound gliders: base-glider seed events relative to own seed
        self.parts = parts

    @property
    def slip(self):
        b, l, r, _ = self.phases[0]
        return (r - l) % TILE

    @property
    def velocity(self):
        return Fraction(self.d, self.p)

    @property
    def width(self):
        return min(len(ph[0]) for ph in self.phases)

    def state_at(self, t0, x0, t):
        """(bits, lph, rph, start column) of the glider seeded at (t0, x0),
        observed at time t."""
        k = t - t0
        q, r = divmod(k, self.p)
        bits, lph, rph, off = self.phases[r]
        return bits, lph, rph, x0 + off + q * self.d

    def to_json(self):
        return {"name": self.name, "p": self.p, "d": self.d,
                "velocity": str(self.velocity), "slip": self.slip,
                "width": self.width, "note": self.note,
                "parts": self.parts,
                "phases": [list(ph) for ph in self.phases]}

    @classmethod
    def from_json(cls, j):
        return cls(j["name"], j["p"], j["d"],
                   [tuple(ph) for ph in j["phases"]], j.get("note", ""),
                   [tuple(x) for x in j["parts"]] if j.get("parts") else None)


def build_row(states, pad=60, width=None):
    """Assemble one row from object states [(bits, lph, rph, start), ...]
    (all at the same time). Objects are sorted by start; neighbouring
    ether phases must agree (else ValueError). The row is cyclic with a
    clean wrap: its width W is chosen >= span + 2*pad with W = total slip
    (mod 14), or `width` (checked). Returns (row, x_of_col0): column i of
    the row is global column x_of_col0 + i."""
    st = sorted(states, key=lambda s: s[3])
    for (b1, l1, r1, s1), (b2, l2, r2, s2) in zip(st, st[1:]):
        if s1 + len(b1) > s2:
            raise ValueError(f"objects overlap: {s1}+{len(b1)} > {s2}")
        if (r1 - s1 - (l2 - s2)) % TILE:
            raise ValueError("ether phases of neighbouring objects disagree")
    x0 = st[0][3] - pad
    xend = st[-1][3] + len(st[-1][0]) + pad
    cL = (st[0][1] - st[0][3]) % TILE           # absolute phase, far left
    cR = (st[-1][2] - st[-1][3]) % TILE         # absolute phase, far right
    need = (cL - cR) % TILE                     # W = cL - cR (mod 14)
    W = xend - x0
    W += (need - W) % TILE
    if width is not None:
        if width < W or (width - need) % TILE:
            raise ValueError(f"width {width} incompatible (need >= {W}, "
                             f"= {need} mod 14)")
        W = width
    row = ether_cells(cL, x0, x0 + W).copy()
    for bits, lph, rph, s in st:
        row[s - x0:s - x0 + len(bits)] = [int(c) for c in bits]
        c = (rph - s) % TILE        # ether after this object
        nxt = [q for q in st if q[3] > s]
        end = nxt[0][3] if nxt else x0 + W
        row[s + len(bits) - x0:end - x0] = ether_cells(c, s + len(bits), end)
    # verify the wrap is clean: phase continuity across column W-1 -> 0
    return row, x0


def isolate_glider(bits, lph, rph, p_hint=None, maxp=200, periods=4,
                   name="?"):
    """Place one object in fresh ether and determine whether it is a
    glider: find its period vector, record all phases, and verify exact
    periodicity over `periods` periods. Returns Glider or raises."""
    T = maxp * (periods + 1) + 2
    # pad on both sides beyond light speed: nothing can wrap unseen
    row, x0 = build_row([(bits, lph, rph, 0)], pad=T + 50)
    hist = evolve_hist(row, T)
    W = len(row)
    # track the single object; find (p, d) from state keys
    seen = {}
    track = []
    for t in range(T + 1):
        r = hist[t]
        u = union_object(r)
        if u is None:
            raise ValueError(f"object vanishes at t={t}")
        a, b, cl, cr = u
        if a < 30 or b > W - 30:
            raise AssertionError("object reached the row edge (cannot happen)")
        if b - a > MAX_OBJECT:
            raise ValueError(f"object grows beyond {MAX_OBJECT} cells at t={t}")
        key = obj_key(r, a, b, cl, cr)
        track.append((key, a + x0))
        if key in seen:
            t1 = seen[key]
            p = t - t1
            d = (a + x0) - track[t1][1]
            break
        seen[key] = t
    else:
        raise ValueError("no period found")
    if not in_ether_lattice(p, d):
        raise ValueError(f"period ({p},{d}) not in ether lattice")
    t1 = seen[track[-1][0]]
    base = track[t1][1]
    phases = [(track[t1 + k][0][0], track[t1 + k][0][1], track[t1 + k][0][2],
               track[t1 + k][1] - base) for k in range(p)]
    g = Glider(name, p, d, phases)
    # additional verification with a fresh row for `periods` periods
    verify_glider(g, periods)
    return g


def verify_glider(g, periods=4):
    """Re-simulate phase 0 in fresh ether; check every phase for
    `periods` periods. Raises on mismatch."""
    row, x0 = build_row([g.state_at(0, 0, 0)], pad=150 + 2 * g.p * periods)
    hist = evolve_hist(row, g.p * periods)
    for t in range(len(hist)):
        u = union_object(hist[t])
        if u is None:
            raise AssertionError(f"{g.name}: vanished at t={t}")
        a, b, cl, cr = u
        got = obj_key(hist[t], a, b, cl, cr) + (a + x0,)
        exp = g.state_at(0, 0, t)
        if got != exp:
            raise AssertionError(f"{g.name}: mismatch at t={t}: {got} vs {exp}")


# ---------------------------------------------------------------------------
# Collision classes

def class_key(r, P1, P2):
    """Class of relative vector r modulo the lattice spanned by P1, P2:
    fractional parts of the coordinates of r in the basis (P1, P2)."""
    (a, b), (c, d) = P1, P2
    det = a * d - b * c
    if det == 0:
        raise ValueError("parallel period vectors")
    rt, rx = r
    al = Fraction(rt * d - rx * c, det)
    be = Fraction(a * rx - b * rt, det)
    return (al - math.floor(al), be - math.floor(be))


def n_classes(P1, P2):
    (a, b), (c, d) = P1, P2
    return abs(a * d - b * c) // TILE
