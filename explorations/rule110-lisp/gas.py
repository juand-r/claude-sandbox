"""Event engine for Rule 110 glider systems (Phase 9; see PLAN.md).

A row is ether with finitely many non-ether patches. Two patches whose
isolated evolutions stay at least 2 ether cells apart (3 cells between
their outermost cells) evolve as the union of those isolated evolutions:
rule 110 has radius 1, so no cell's neighbourhood touches both
(superposition lemma, PLAN.md). The engine therefore moves particles
(periodic patches) in closed form and simulates exactly only patches that
come close, memoizing each such collision by its canonical key.

Patch. Cells of a patch are a Python int (bit i = cell i, left to right)
of width w. Ether at (t, x) reads ETHER[(c + x + 4t) % 14] for the
constant c of its region; a patch records the local phases instead: phL,
the ether phase index at its first cell (so cell i < 0 reads
ETHER[(phL + i) % 14]), and phR, the phase index at the cell just right of
it (cell w + j reads ETHER[(phR + j) % 14]). (bits, w, phL, phR) is
translation invariant: it is the canonical key. Patches are trimmed: the
first cell differs from the left ether, the last from the right ether
(width 0 when the two ethers agree on a cut).
"""

import numpy as np

from engine import ETHER

TILE = len(ETHER)
SHIFT = 4                     # ether: row(t+1)[x] = row(t)[x + 4]
SPLIT_GAP = TILE              # pieces split at >= one clean ether tile
MIN_GAP = 2                   # ether cells needed between patches (lemma)
P_MAX = 120                   # longest period searched for a particle

_TILE_INT = [sum(1 << k for k in range(TILE) if ETHER[(ph + k) % TILE] == "1")
             for ph in range(TILE)]
_eth_cache = {}               # phase -> (n, int) ether bits, n cells


def ether_int(ph, n):
    """n cells of ether starting at phase index ph, as an int."""
    ph %= TILE
    m, v = _eth_cache.get(ph, (0, 0))
    if m < n:
        m = max(n, 2 * m, 1024)
        m += -m % TILE
        reps = m // TILE
        v = 0
        tile = _TILE_INT[ph]
        # tile repeated reps times (doubling)
        chunk, k, pos = tile, TILE, 0
        while reps:
            if reps & 1:
                v |= chunk << pos
                pos += k
            chunk |= chunk << k
            k *= 2
            reps >>= 1
        _eth_cache[ph] = (m, v)
    return v & ((1 << n) - 1)


def trim(bits, w, phL, phR):
    """Canonical (trimmed) form -> (bits, w, phL, phR, dx): the patch now
    starts dx cells right of where it did."""
    if w == 0:
        return 0, 0, phL % TILE, phR % TILE, 0
    full = (1 << w) - 1
    dl = bits ^ ether_int(phL, w)
    i = (dl & -dl).bit_length() - 1 if dl else w          # leading ether-L cells
    dr = bits ^ ether_int(phR - w, w)
    j = w - dr.bit_length()                                # trailing ether-R cells
    if i + j >= w:                                         # empty: cut at w - j
        cut = w - j
        return 0, 0, (phL + cut) % TILE, (phR - j) % TILE, cut
    nw = w - i - j
    return (bits >> i) & ((1 << nw) - 1), nw, (phL + i) % TILE, (phR - j) % TILE, i


def step(bits, w, phL, phR):
    """One step of a patch -> trimmed (bits, w, phL, phR, dx)."""
    # extended row: two ether cells each side, then the rule on the middle
    W = w + 4
    ext = (ether_int(phL - 2, 2) | (bits << 2) |
           (ether_int(phR, 2) << (w + 2)))
    left, right = ext << 1, ext >> 1
    new = ((ext | right) & ~(left & ext & right)) >> 1
    new &= (1 << (W - 2)) - 1                             # cells -1 .. w
    # at t+1 the ether phase index at a fixed cell grows by SHIFT
    b, nw, pl, pr, dx = trim(new, W - 2, phL - 1 + SHIFT, phR + 1 + SHIFT)
    return b, nw, pl, pr, dx - 1


def key_of_cells(cells, phL, phR):
    """Trimmed key of a uint8 cell array -> (key, dx)."""
    w = len(cells)
    bits = int.from_bytes(np.packbits(cells, bitorder="little").tobytes(), "little")
    b, nw, pl, pr, dx = trim(bits, w, phL, phR)
    return (b, nw, pl, pr), dx


def cells_of(bits, w):
    out = np.zeros(w, dtype=np.uint8)
    if w:
        raw = np.frombuffer(bits.to_bytes((w + 7) // 8, "little"), dtype=np.uint8)
        out[:] = np.unpackbits(raw, bitorder="little")[:w]
    return out


def split(key):
    """Pieces of a patch separated by >= SPLIT_GAP cells of clean ether of
    one phase -> [(key, offset)], offsets relative to the patch's first
    cell. A clean cell lies in some 14-cell window equal to an ether
    rotation, and every such window covering it has the same phase."""
    bits, w, phL, phR = key
    if w < SPLIT_GAP + 2:
        return [(key, 0)]
    # two tiles of padding: windows starting in the first tile lie inside
    # the pad, so its first 14 cells are always a gap of phase phL
    pad = 2 * TILE
    row = np.concatenate([cells_of(ether_int(phL - pad, pad), pad), cells_of(bits, w),
                          cells_of(ether_int(phR, pad), pad)])
    from census import ether_phase
    ph = ether_phase(row)                       # per window start, -1 = none
    n = len(row)
    # per cell: min and max phase over the valid windows covering it
    big = TILE + 1
    lo_src = np.where(ph >= 0, ph, big)
    hi_src = np.where(ph >= 0, ph, -1)
    lo_pad = np.concatenate([np.full(TILE - 1, big), lo_src, np.full(TILE - 1, big)])
    hi_pad = np.concatenate([np.full(TILE - 1, -1), hi_src, np.full(TILE - 1, -1)])
    sw = np.lib.stride_tricks.sliding_window_view
    cmin = sw(lo_pad, TILE).min(axis=1)[:n]
    cmax = sw(hi_pad, TILE).max(axis=1)[:n]
    clean = (cmin == cmax)
    phase = np.where(clean, cmin, -1)
    # gaps: maximal runs of clean cells of one phase, >= SPLIT_GAP long
    change = np.nonzero(np.diff(phase) != 0)[0] + 1
    starts = np.concatenate([[0], change])
    ends = np.concatenate([change, [n]])
    gaps = [(a, b) for a, b in zip(starts, ends)
            if phase[a] >= 0 and b - a >= SPLIT_GAP]
    if gaps[0][0] != 0 or gaps[-1][1] != n:
        raise AssertionError("split: the padding is not a gap")
    pieces = []
    for (a0, b0), (a1, b1) in zip(gaps, gaps[1:]):
        # piece = cells [b0, a1) of the padded row; phases from the gaps
        b0, a1 = int(b0), int(a1)
        pl = (int(phase[b0 - 1]) + b0) % TILE   # gap phase c: cell y reads (c + y)
        pr = (int(phase[a1]) + a1) % TILE
        k, dx = key_of_cells(row[b0:a1], pl, pr)
        if not _empty(k):                       # a pure phase slip is kept
            pieces.append((k, int(b0 + dx - pad)))
    return pieces


class Orbit:
    """A periodic patch: p steps, displacement d. phases[s] is the key at
    phase s, off[s] its left edge relative to phase 0 (off[p] = d)."""

    def __init__(self, oid, keys, off):
        self.id = oid
        self.keys = keys
        self.p = len(keys)
        self.off = off
        self.d = off[-1]
        self.w = [k[1] for k in keys]

    def __repr__(self):
        return f"Orbit({self.id}, p={self.p}, d={self.d}, w={max(self.w)})"


class Registry:
    """Canonical key -> (orbit, phase), found by simulating the patch alone
    until its key recurs (period <= P_MAX). Non-periodic keys are cached
    as None."""

    def __init__(self, p_max=P_MAX):
        self.p_max = p_max
        self.known = {}
        self.orbits = []

    def lookup(self, key):
        if key in self.known:
            return self.known[key]
        keys, off = [key], [0]
        b, w, pl, pr = key
        x = 0
        for s in range(1, self.p_max + 1):
            b, w, pl, pr, dx = step(b, w, pl, pr)
            x += dx
            k = (b, w, pl, pr)
            if k == key:
                off.append(x)
                o = Orbit(len(self.orbits), keys, off)
                self.orbits.append(o)
                for i, ki in enumerate(keys):
                    self.known[ki] = (o, i)
                return self.known[key]
            keys.append(k)
            off.append(x)
        self.known[key] = None
        return None

    def add(self, keys, off):
        """Register an orbit seen directly (keys[i] at left edge off[i];
        off[p] is the displacement after one period)."""
        o = Orbit(len(self.orbits), list(keys), [x - off[0] for x in off])
        self.orbits.append(o)
        for i, ki in enumerate(keys):
            self.known[ki] = (o, i)
        return o


# ---------------------------------------------------------------------------
# Composites: patches that came within MIN_GAP cells of each other.

COMPOSITE_CAP = 2048          # steps per memo entry (then it continues anew)


class Entry:
    """Memoized evolution of a composite key: states[s] = (key, left
    offset) for s = 0..T, then it becomes `pieces` [(key, left offset)]
    (each a particle if the registry knows it, else a new composite)."""

    __slots__ = ("states", "lo", "w", "T", "pieces")

    def __init__(self, states, pieces):
        self.states = states
        self.T = len(states) - 1
        self.lo = np.array([x for _, x in states], dtype=np.int64)
        self.w = np.array([k[1] for k, _ in states], dtype=np.int64)
        self.pieces = pieces


def _empty(key):
    return key[1] == 0 and key[2] == key[3]


def simulate(key, reg):
    """Evolve a composite until it splits (>= 2 pieces), becomes one
    periodic piece, vanishes, or COMPOSITE_CAP steps pass."""
    states = [(key, 0)]
    seen = {key: 0}
    k, x = key, 0
    for s in range(1, COMPOSITE_CAP + 1):
        b, w, pl, pr, dx = step(*k)
        k = (b, w, pl, pr)
        x += dx
        if _empty(k):
            states.append((k, x))
            return Entry(states, [])
        if k in reg.known and reg.known[k] is not None:
            states.append((k, x))
            return Entry(states, [(k, x)])
        if k in seen:                       # periodic since step seen[k]
            s0 = seen[k]
            reg.add([kk for kk, _ in states[s0:]], [xx for _, xx in states[s0:]] + [x])
            return Entry(states[:s0 + 1], [states[s0]])
        states.append((k, x))
        seen[k] = s
        ps = split(k)
        if len(ps) != 1:
            return Entry(states, [(pk, x + off) for pk, off in ps])
    return Entry(states, [(k, x)])


# ---------------------------------------------------------------------------
# The engine.

class Item:
    """A particle (orbit, anchor t0/x0: phase 0 at time t0 has its left
    edge at x0) or a composite (entry, start time ts, left edge xs at ts).
    cL: the global ether constant on its left (ether at (t, x) reads
    ETHER[(cL + x + 4t) % 14])."""

    __slots__ = ("orbit", "t0", "x0", "entry", "ts", "xs", "cL",
                 "prev", "next", "alive", "token")

    def __init__(self):
        self.prev = self.next = None
        self.alive = True
        self.token = 0
        self.orbit = self.entry = None

    def at(self, t):
        """(key, left edge) at time t."""
        if self.orbit is not None:
            o = self.orbit
            k, s = divmod(t - self.t0, o.p)
            return o.keys[s], self.x0 + k * o.d + o.off[s]
        key, off = self.entry.states[t - self.ts]
        return key, self.xs + off

    def end(self):
        return None if self.orbit is not None else self.ts + self.entry.T

    def track(self, t, n):
        """(left edges, widths) for times t .. t+n-1, numpy arrays."""
        if self.orbit is not None:
            o = self.orbit
            j = (t - self.t0) + np.arange(n)
            k, s = np.divmod(j, o.p)
            return self.x0 + k * o.d + o.offa[s], o.wa[s]
        s = t - self.ts
        e = self.entry
        return self.xs + e.lo[s:s + n], e.w[s:s + n]


def _orbit_arrays(o):
    if not hasattr(o, "offa"):
        o.offa = np.array(o.off[:o.p], dtype=np.int64)
        o.wa = np.array(o.w, dtype=np.int64)


class Gas:
    """The row as a list of items (left to right) in ether, advanced by
    events. Public: t, advance_to(T), window(lo, hi), items()."""

    def __init__(self, reg=None):
        self.reg = reg or Registry()
        self.memo = {}
        self.t = 0
        self.head = self.tail = None
        self.heap = []
        self.seq = 0
        self.c_left = self.c_right = None      # ether constants beyond the ends
        self.n_events = 0
        self.n_sim = 0

    # -- construction ------------------------------------------------------
    def _make(self, key, lo, t):
        """Item for a piece (key at left edge lo, time t)."""
        it = Item()
        it.cL = (key[2] - lo - SHIFT * t) % TILE
        r = self.reg.lookup(key)
        if r is not None:
            o, s = r
            _orbit_arrays(o)
            it.orbit, it.t0, it.x0 = o, t - s, lo - o.off[s]
        else:
            e = self.memo.get(key)
            if e is None:
                e = self.memo[key] = simulate(key, self.reg)
                self.n_sim += 1
            it.entry, it.ts, it.xs = e, t, lo
        return it

    def _cR(self, it, t):
        key, lo = it.at(t)
        return (key[3] - lo - key[1] - SHIFT * t) % TILE

    def append_row(self, cells, x, c_left, c_right):
        """Add a t = 0 row segment [x, x + len) (ether constants c_left,
        c_right outside it) to the right end. Only at t = 0."""
        if self.t != 0:
            raise ValueError("rows are added at t = 0")
        key, dx = key_of_cells(cells, (c_left + x) % TILE, (c_right + x + len(cells)) % TILE)
        items = [self._make(pk, x + dx + off, 0) for pk, off in split(key)]
        if self.tail is None:
            self.c_left = c_left
        elif self._cR(self.tail, 0) != c_left and self.c_right != c_left:
            raise ValueError("ether constant mismatch between rows")
        for it in items:
            self._link_after(self.tail, it)
        self.c_right = c_right

    @classmethod
    def from_layout(cls, lay):
        """Engine for a whole casim.Layout at t = 0 (adjacent segments
        are joined into one row)."""
        g = cls()
        segs, ph = lay.segments, lay.phases
        i = 0
        while i < len(segs):
            j = i
            while j + 1 < len(segs) and ph[j + 1] is None:
                j += 1
            x, hi = segs[i][0], segs[j][0] + len(segs[j][1])
            g.append_row(lay.cells(x, hi), x, ph[i], ph[j + 1])
            i = j + 1
        g.start()
        return g

    def start(self):
        """Schedule the initial events (after the rows are added)."""
        it = self.head
        while it is not None:
            self._schedule(it)
            it = it.next

    # -- list ----------------------------------------------------------------
    def _link_after(self, a, it):
        """Insert it after a (a None: at the head)."""
        if a is None:
            it.next, self.head = self.head, it
            if it.next is not None:
                it.next.prev = it
            else:
                self.tail = it
        else:
            it.prev, it.next = a, a.next
            if a.next is not None:
                a.next.prev = it
            else:
                self.tail = it
            a.next = it

    def items(self):
        it = self.head
        while it is not None:
            yield it
            it = it.next

    # -- events ----------------------------------------------------------------
    def _push(self, t, kind, a, b=None):
        import heapq
        self.seq += 1
        heapq.heappush(self.heap, (t, self.seq, kind, a, b, a.token))

    def _schedule(self, it):
        """Events of a new item: its split, and the pair with its right
        neighbour (the left pair is scheduled by the caller)."""
        if it.entry is not None:
            self._push(it.ts + it.entry.T, "S", it)
        if it.next is not None:
            it.token += 1
            t = self._collision(it, it.next, self.t)
            if t is not None:
                self._push(t, "C", it, it.next)

    def _collision(self, a, b, t):
        """First time >= t at which fewer than MIN_GAP ether cells separate
        a and b (a left of b), or None (never, or not before one of them
        ends as a composite; its split reschedules)."""
        ea, eb = a.end(), b.end()
        if ea is None and eb is None:
            return self._collision_periodic(a, b, t)
        horizon = min(e for e in (ea, eb) if e is not None)
        n = horizon - t + 1
        ka, la = a.at(t)
        kb, lb = b.at(t)
        if lb - la - ka[1] >= MIN_GAP + 2 * n:       # light-cone reject
            return None
        xa, wa = a.track(t, n)
        xb, _ = b.track(t, n)
        g = xb - xa - wa
        hit = np.nonzero(g < MIN_GAP)[0]
        return t + int(hit[0]) if len(hit) else None

    def _collision_periodic(self, a, b, t):
        oa, ob = a.orbit, b.orbit
        from math import lcm
        L = lcm(oa.p, ob.p)
        xa, wa = a.track(t, L)
        xb, _ = b.track(t, L)
        g = xb - xa - wa
        delta = ob.d * (L // ob.p) - oa.d * (L // oa.p)
        if delta >= 0:
            hit = np.nonzero(g < MIN_GAP)[0]
            return t + int(hit[0]) if len(hit) else None
        n = np.where(g < MIN_GAP, 0, (g - MIN_GAP) // (-delta) + 1)
        tt = np.arange(L) + n * L
        return t + int(tt.min())

    def advance_to(self, T):
        import heapq
        heap = self.heap
        while heap and heap[0][0] <= T:
            t, _, kind, a, b, tok = heapq.heappop(heap)
            if not a.alive:
                continue
            if kind == "C":
                if not b.alive or a.next is not b or a.token != tok:
                    continue
                self.t = t
                self._merge(a, b, t)
            else:
                self.t = t
                self._split(a, t)
            self.n_events += 1
        self.t = T

    def _replace(self, olds, news, t):
        """Replace the adjacent items olds (left to right) by news."""
        left, right = olds[0].prev, olds[-1].next
        for o in olds:
            o.alive = False
        prev = left
        for it in news:
            it.prev = prev
            if prev is None:
                self.head = it
            else:
                prev.next = it
            prev = it
        if prev is None:
            self.head = right
        else:
            prev.next = right
        if right is None:
            self.tail = prev
        else:
            right.prev = prev
        for it in news:
            self._schedule(it)
        if left is not None:
            left.token += 1
            nb = left.next
            if nb is not None:
                tc = self._collision(left, nb, t)
                if tc is not None:
                    self._push(tc, "C", left, nb)

    def _merge(self, a, b, t):
        ka, la = a.at(t)
        kb, lb = b.at(t)
        g = lb - la - ka[1]
        if g < 0:
            raise AssertionError(f"t={t}: items overlap ({g})")
        if (ka[3] + g) % TILE != kb[2]:
            raise AssertionError(f"t={t}: ether phase mismatch between items")
        bits = ka[0] | (ether_int(ka[3], g) << ka[1]) | (kb[0] << (ka[1] + g))
        b2, w2, pl, pr, dx = trim(bits, ka[1] + g + kb[1], ka[2], kb[3])
        self._replace([a, b], [self._make((b2, w2, pl, pr), la + dx, t)], t)

    def _split(self, a, t):
        key, lo = a.at(t)
        if key != a.entry.states[-1][0]:
            raise AssertionError("split not at the composite's end")
        news = [self._make(pk, a.xs + off, t) for pk, off in a.entry.pieces]
        self._replace([a], news, t)

    # -- rendering --------------------------------------------------------------
    def window(self, lo, hi):
        """uint8 cells [lo, hi) at time t."""
        t = self.t
        out = np.empty(hi - lo, dtype=np.uint8)
        xs = np.arange(lo, hi)
        eth = np.array([int(c) for c in ETHER], dtype=np.uint8)
        # ether by region: walk items, filling the gap left of each
        x, c = lo, self.c_left
        for it in self.items():
            key, l = it.at(t)
            r = l + key[1]
            c_it = it.cL
            if l > x:
                e = min(l, hi)
                out[x - lo:e - lo] = eth[(c_it + xs[x - lo:e - lo] + SHIFT * t) % TILE]
                x = e
            if x >= hi:
                return out
            if r > x:
                cells = cells_of(key[0], key[1])
                a, b = max(x, l), min(r, hi)
                out[a - lo:b - lo] = cells[a - l:b - l]
                x = b
            c = (key[3] - r - SHIFT * t) % TILE
            if x >= hi:
                return out
        out[x - lo:] = eth[(c + xs[x - lo:] + SHIFT * t) % TILE]
        return out
