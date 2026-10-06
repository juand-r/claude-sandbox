"""The gas engine with its event loop in C (gasc.c); same interface and
results as gas.Gas, which stays the reference.

C holds the items, the event heap and the geometry of orbits and
memoized composites; Python holds every key (the cells) and does the
cell-level work C asks for: an unknown merge (simulate the new
composite), a composite piece not yet simulated, a side to materialize.
"""

import ctypes
import os
import subprocess

import numpy as np

import gas
from gas import SHIFT, TILE, Registry, cells_of, ether_int, key_of_cells, simulate, split, trim

_DIR = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_DIR, "gasc.c")
_LIB = os.path.join(_DIR, "__pycache__", "gasc.so")

DEAD, PART, COMP, SENL, SENR = range(5)
OK, NEED_MERGE, NEED_SIDE, NEED_PIECE, NEED_UNIT, ERR = 0, 1, 2, 3, 4, -1
FAR = 1 << 62
_ETHER_BITS = np.array([int(c) for c in gas.ETHER], dtype=np.uint8)


def _load():
    if not os.path.exists(_LIB) or os.path.getmtime(_LIB) < os.path.getmtime(_SRC):
        os.makedirs(os.path.dirname(_LIB), exist_ok=True)
        # build beside and rename: running processes keep the old file
        tmp = f"{_LIB}.{os.getpid()}"
        subprocess.run(["cc", "-O2", "-shared", "-fPIC", "-o", tmp, _SRC], check=True)
        os.replace(tmp, _LIB)
    lib = ctypes.CDLL(_LIB)
    i32, i64, p = ctypes.c_int32, ctypes.c_int64, ctypes.c_void_p
    for name, res, args in (
            ("gc_reset", i32, []), ("gc_failed", i32, []), ("gc_now", i64, []),
            ("gc_events", i64, []), ("gc_heap", i64, []), ("gc_count", i64, []),
            ("gc_request", None, [p, p, p, p]),
            ("gc_item", None, [i32, i64, p, p]),
            ("gc_item_entry", i32, [i32]),
            ("gc_set_piece", None, [i32, i32, i32, i32, i32]),
            ("gc_add_orbit", i32, [i32, i32, p, p, p, p]),
            ("gc_add_entry", i32, [i32, p, p, p, p, i32, p, p, p, p, p]),
            ("gc_set_merge", i32, [i32, i32, i32, i32]),
            ("gc_append", i32, [i32, i32, i64, i64, i32, i64]),
            ("gc_set_side", None, [i32, i64, i64, i64]),
            ("gc_side_request", i64, [i32]),
            ("gc_dump", i64, [i64, p, p]), ("gc_set_now", None, [i64]),
            ("gc_family_counts", None, [p]),
            ("gc_start", i32, []),
            ("gc_materialize", i32, [i32, p, p, p, p, p]),
            ("gc_advance", i32, [i64]),
            ("gc_list", i64, [i64, i64, i64, p, p, p, p, p, p, p]),
            ("gc_debug", i64, [p]), ("gc_rope_on", i32, []), ("gc_rope_info", None, [p]),
            ("gc_rope_absorb", i32, [i64, i64]),
            ("gc_rope_push_ossifier", i32, [i32, p, p, p, p, i64]),
            ("gc_unit_request", i32, [p, p, p]),
            ("gc_set_unit", i32, [i64, p, i32])):
        f = getattr(lib, name)
        f.restype, f.argtypes = res, args
    return lib


_lib = _load()
_live = [None]                 # the one CGas the C state belongs to


def _arr(xs, dtype):
    return np.ascontiguousarray(np.array(xs, dtype=dtype))


class CGas:
    """Gas engine (gas.Gas interface: t, advance_to, window, n_events,
    count) with the event loop in C. One instance at a time (the C state
    is global)."""

    def __init__(self, reg=None):
        if not _lib.gc_reset():
            raise MemoryError("gasc: initial allocation failed")
        _live[0] = self
        self.reg = reg or Registry()
        self.n_orbits_c = 0            # orbits pushed to C (ids = reg ids)
        self.entries = []              # C entry id -> gas.Entry
        self.memo = {}                 # composite key -> C entry id
        self.sides = [None, None]      # L, R side sources
        self.n_sim = 0
        self.c_left = None
        self._rows = []                # setup: items before start()
        self.n_events_before = 0       # events before a resume
        self._row_cache = {}           # side row key -> its pieces, resolved
        self._oflat = None
        # rendering: flat key slots and their cells (window)
        self._obase, self._ebase, self._nkeys = [], [], 0
        self._koff = np.zeros(0, np.int64)
        self._cellbuf = np.zeros(1 << 16, np.uint8)
        self._ncells = 0

    # -- tables ----------------------------------------------------------------
    def _check(self, r=None):
        if _live[0] is not self:
            raise RuntimeError("another CGas owns the C state")
        f = _lib.gc_failed()
        if f or r == ERR:
            detail = ""
            if f == 3:                     # bad merge: the two items
                a, b, _, t = self._request()
                detail = f" at t={t}: {self._item(a, t)} / {self._item(b, t)}"
            raise RuntimeError(f"gasc: C failure code {f}{detail}")

    def _push_orbits(self):
        while self.n_orbits_c < len(self.reg.orbits):
            o = self.reg.orbits[self.n_orbits_c]
            arrs = [_arr(o.off[:o.p], np.int32), _arr(o.w, np.int32),
                    _arr([k[2] for k in o.keys], np.int8), _arr([k[3] for k in o.keys], np.int8)]
            i = _lib.gc_add_orbit(o.p, o.d, *[a.ctypes.data for a in arrs])
            if i != o.id:
                raise RuntimeError("gasc: orbit ids out of step")
            self.n_orbits_c += 1

    def _resolve(self, key):
        """(kind, id, phase) of a piece key, simulating it if new."""
        r = self.reg.lookup(key)
        if r is not None:
            self._push_orbits()
            return PART, r[0].id, r[1]
        eid = self.memo.get(key)
        if eid is None:
            e = simulate(key, self.reg)
            self.n_sim += 1
            self._push_orbits()
            eid = self._add_entry(e)
            self.entries.append(e)
            self.memo[key] = eid
        return COMP, eid, 0

    def _add_entry(self, e):
        """Push a gas.Entry to C (its composite pieces resolved if known)."""
        kinds, ids, phases = [], [], []
        for pk, _ in e.pieces:
            r = self.reg.lookup(pk)
            if r is not None:
                self._push_orbits()
                kinds.append(PART); ids.append(r[0].id); phases.append(r[1])
            else:                  # composite piece: simulated when reached
                kinds.append(COMP); ids.append(self.memo.get(pk, -1)); phases.append(0)
        st = e.states
        arrs = [_arr([x for _, x in st], np.int32), _arr([k[1] for k, _ in st], np.int32),
                _arr([k[2] for k, _ in st], np.int8), _arr([k[3] for k, _ in st], np.int8)]
        parrs = [_arr(kinds, np.int32), _arr(ids, np.int32), _arr(phases, np.int32),
                 _arr([x for _, x in e.pieces], np.int64),
                 _arr([k[2] for k, _ in e.pieces], np.int32)]
        eid = _lib.gc_add_entry(e.T, *[a.ctypes.data for a in arrs], len(e.pieces),
                                *[a.ctypes.data for a in parrs])
        self._check(eid if eid >= 0 else ERR)
        return eid

    def _key(self, kind, i, phase):
        if kind == PART:
            return self.reg.orbits[i].keys[phase]
        return self.entries[i].states[phase][0]

    def _item_tuple(self, key, lo, t):
        """(kind, id, t0, x0, cL) of a new item for a piece."""
        kind, i, ph = self._resolve(key)
        cL = (key[2] - lo - SHIFT * t) % TILE
        if kind == PART:
            o = self.reg.orbits[i]
            return kind, i, t - ph, lo - o.off[ph], cL
        return kind, i, t, lo, cL

    # -- setup (gas.Gas interface) ------------------------------------------------
    def append_row(self, cells, x, c_left, c_right):
        key, dx = key_of_cells(cells, (c_left + x) % TILE, (c_right + x + len(cells)) % TILE)
        if self.c_left is None:
            self.c_left = c_left
        for pk, off in split(key):
            self._rows.append(self._item_tuple(pk, x + dx + off, 0))

    def add_sides(self, left, right):
        self.sides = [left, right]

    def _side_params(self, s):
        side = self.sides[s]
        b0, num, den = side.linear()
        _lib.gc_set_side(s, b0, num, den)

    def start(self):
        rows = self._rows
        if self.sides[0] is not None:
            rows = [(SENL, -1, 0, 0, 0)] + rows
            self._side_params(0)
        if self.sides[1] is not None:
            rows = rows + [(SENR, -1, 0, 0, 0)]
            self._side_params(1)
        for r in rows:
            if _lib.gc_append(*r, 0) < 0:          # rows of the layout: tc = 0
                self._check(ERR)
        self._rows = None
        self._check(_lib.gc_start())

    # -- events ---------------------------------------------------------------------
    def _own(self):
        if _live[0] is not self:
            raise RuntimeError("another CGas owns the C state")

    @property
    def t(self):
        self._own()
        return _lib.gc_now()

    @property
    def n_events(self):
        self._own()
        return _lib.gc_events() + self.n_events_before

    def count(self):
        self._own()
        return _lib.gc_count()

    def family_counts(self):
        """Merges so far by the two items' glider family (A, C, E, other)."""
        out = np.zeros(16, np.int64)
        _lib.gc_family_counts(out.ctypes.data)
        return {f"{a}x{b}": int(out[4 * i + j]) for i, a in enumerate("ACEX")
                for j, b in enumerate("ACEX") if out[4 * i + j]}

    def _request(self):
        a, b, k = ctypes.c_int32(), ctypes.c_int32(), ctypes.c_int32()
        t = ctypes.c_int64()
        _lib.gc_request(ctypes.byref(a), ctypes.byref(b), ctypes.byref(k), ctypes.byref(t))
        return a.value, b.value, k.value, t.value

    def _item(self, i, t):
        out = np.zeros(5, dtype=np.int32)
        left = ctypes.c_int64()
        _lib.gc_item(i, t, out.ctypes.data, ctypes.byref(left))
        kind, eid, ph, w, cL = out.tolist()
        return kind, eid, ph, left.value, w, cL

    def advance_to(self, T):
        self._own()
        while True:
            r = _lib.gc_advance(T)
            if r == OK:
                return
            if r == NEED_MERGE:
                self._merge()
            elif r == NEED_PIECE:
                a, _, k, t = self._request()
                e = _lib.gc_item_entry(a)
                kind, i, ph = self._resolve(self.entries[e].pieces[k][0])
                _lib.gc_set_piece(e, k, kind, i, ph)
            elif r == NEED_UNIT:
                self._rope_unit()
            elif r == NEED_SIDE:
                if _lib.gc_rope_on() and self._request()[0] >= 0 and \
                        self._item(self._request()[0], self._request()[3])[0] == SENL:
                    self._rope_draw()
                else:
                    self._materialize()
            else:
                self._check(ERR)

    def _merge(self):
        a, b, _, t = self._request()
        kda, ia, pa, la, wa, _ = self._item(a, t)
        kdb, ib, pb, lb, wb, _ = self._item(b, t)
        ka, kb = self._key(kda, ia, pa), self._key(kdb, ib, pb)
        g = lb - la - ka[1]
        if g < 0 or (ka[3] + g) % TILE != kb[2]:
            raise AssertionError(f"t={t}: bad merge (gap {g})")
        bits = ka[0] | (ether_int(ka[3], g) << ka[1]) | (kb[0] << (ka[1] + g))
        b2, w2, pl, pr, dx = trim(bits, ka[1] + g + kb[1], ka[2], kb[3])
        self._check(_lib.gc_set_merge(*self._resolve((b2, w2, pl, pr)), dx))

    def ensure(self, lo, hi):
        """Materialize the sides until neither reaches into [lo, hi)."""
        while _lib.gc_side_request(0) >= lo - gas.SENTINEL_MARGIN:
            if _lib.gc_rope_on():
                raise ValueError(f"window [{lo}, {hi}) reaches into the rope")
            self._materialize()
        while _lib.gc_side_request(1) < hi + gas.SENTINEL_MARGIN:
            self._materialize()

    def _materialize(self):
        a, b, _, t = self._request()
        s = 0 if a >= 0 and self._item(a, t)[0] == SENL else 1
        side = self.sides[s]
        bound = side.bound(t)
        row = side.src()
        if row is None:
            raise RuntimeError(f"t={t}: side {'LR'[s]} exhausted")
        cells, x, cl, cr = row
        key, dx = key_of_cells(cells, (cl + x) % TILE, (cr + x + len(cells)) % TILE)
        # a side's rows repeat (ossifiers; the table's super-period chunks):
        # split and resolve each distinct row once
        info = self._row_cache.get(key)
        if info is None:
            rows = []
            for pk, off in split(key):
                kind, i, ph = self._resolve(pk)
                if kind != PART:
                    raise RuntimeError(f"side {'LR'[s]}: non-periodic piece at {x + dx + off}")
                rows.append((i, ph, off, pk[2]))
            info = self._row_cache[key] = np.array(rows, dtype=np.int64).reshape(-1, 4)
        oid, ph, off, phl = info.T
        ob, ooff, ow, op, od = self._orbit_flat()
        lo = x + dx + off
        cL = (phl - lo) % TILE                       # t = 0
        t0 = -ph
        x0 = lo - ooff[ob[oid] + ph]
        # every new item must lie beyond the side's bound at time t
        k_, s_ = np.divmod(t - t0, op[oid])
        l_now = x0 + k_ * od[oid] + ooff[ob[oid] + s_]
        w_now = ow[ob[oid] + s_]
        if np.any(l_now + w_now - 1 > bound) if s == 0 else np.any(l_now < bound):
            raise AssertionError(f"t={t}: side {'LR'[s]} content beyond its bound")
        self._side_params(s)
        n = len(oid) + 1
        kind = np.full(n, PART, np.int32)
        ids, t0s, x0s, cls = (np.zeros(n, np.int32), np.zeros(n, np.int64),
                              np.zeros(n, np.int64), np.zeros(n, np.int32))
        sl = slice(1, n) if s == 0 else slice(0, n - 1)
        kind[0 if s == 0 else n - 1] = SENL if s == 0 else SENR
        ids[0 if s == 0 else n - 1] = -1
        ids[sl], t0s[sl], x0s[sl], cls[sl] = oid, t0, x0, cL
        self._check(_lib.gc_materialize(n, *[q.ctypes.data for q in (kind, ids, t0s, x0s, cls)]))

    def _row_items(self, s, row):
        """Side row (cells, x, cL, cR at t = 0) -> its particles as arrays
        (orbit id, t0, x0, cL), left to right."""
        cells, x, cl, cr = row
        key, dx = key_of_cells(cells, (cl + x) % TILE, (cr + x + len(cells)) % TILE)
        info = self._row_cache.get(key)
        if info is None:
            rows = []
            for pk, off in split(key):
                kind, i, ph = self._resolve(pk)
                if kind != PART:
                    raise RuntimeError(f"side {'LR'[s]}: non-periodic piece at {x + dx + off}")
                rows.append((i, ph, off, pk[2]))
            info = self._row_cache[key] = np.array(rows, dtype=np.int64).reshape(-1, 4)
        oid, ph, off, phl = info.T
        ob, ooff, ow, op, od = self._orbit_flat()
        lo = x + dx + off
        return oid, -ph, lo - ooff[ob[oid] + ph], (phl - lo) % TILE

    # -- the rope (gasc.c; PLAN.md phase 10b) -----------------------------------------
    ROPE_SEP = 1600           # debris closer than this forms one unit (> ossifier span)
    ROPE_MARGIN = 1 << 13     # cells kept between the cut and the rightmost ossifier

    def _rope_draw(self):
        """No ossifier in transit: put the train's next one behind the rope."""
        row = self.sides[0].src()
        if row is None:
            raise RuntimeError("left side exhausted")
        oid, t0, x0, cl = self._row_items(0, row)
        for i in oid:
            o = self.reg.orbits[int(i)]
            if 3 * o.d != 2 * o.p:
                raise RuntimeError(f"train row has a non-A particle (orbit {o.id})")
        arrs = [_arr(oid, np.int32), _arr(t0, np.int64), _arr(x0, np.int64), _arr(cl, np.int32)]
        self._check(_lib.gc_rope_push_ossifier(len(oid), *[a.ctypes.data for a in arrs], 0))

    def _rope_unit(self):
        """An unknown crossing: simulate the ossifier's gliders and the
        unit's items, alone, with the reference engine (gas.Gas) from tau
        until no event is left, and store the result in C."""
        key = np.zeros(2 + 3 * (64 + 8), np.int32)
        tau, ref = ctypes.c_int64(), ctypes.c_int64()
        n = _lib.gc_unit_request(key.ctypes.data, ctypes.byref(tau), ctypes.byref(ref))
        key = key[:n].tolist()
        tau, ref = tau.value, ref.value
        ng, nu = key[0], key[1]
        g = gas.Gas(self.reg)
        if not hasattr(self, "_sub_memo"):
            self._sub_memo = {}
        g.memo = self._sub_memo
        prev = None
        for q in range(ng + nu):
            oid, ph, off = key[2 + 3 * q: 5 + 3 * q]
            it = g._make(self.reg.orbits[oid].keys[ph], ref + off, tau)
            g._link_after(prev, it)
            prev = it
        g.t = tau
        g.start()
        last = tau
        import heapq
        while g.heap:
            t = g.heap[0][0]
            before = g.n_events
            g.advance_to(t)
            if g.n_events > before:
                last = t
            if g.t - tau > (1 << 22):
                raise RuntimeError(f"rope crossing at t={tau} does not settle")
        items = list(g.items())
        if any(it.orbit is None for it in items):
            raise RuntimeError(f"rope crossing at t={tau}: a composite remains")
        fam = ["A" if 3 * it.orbit.d == 2 * it.orbit.p else
               "E" if 15 * it.orbit.d == -4 * it.orbit.p else "X" for it in items]
        if fam.count("A") != ng or "X" in fam or fam[-ng:] != ["A"] * ng:
            raise RuntimeError(f"rope crossing at t={tau}: outcome {''.join(fam)} "
                               f"(expected E..E then {ng} A)")
        out = [ng, len(items) - ng]
        order = items[-ng:] + items[:-ng]                 # gliders first, as in the key
        for it in order:
            k, lo = it.at(last)
            o = it.orbit
            out += [o.id, (last - it.t0) % o.p, lo - ref]
        self._push_orbits()
        res = _arr(out, np.int32)
        self._check(_lib.gc_set_unit(last - tau, res.ctypes.data, len(out)))

    def rope_info(self):
        out = np.zeros(6, np.int64)
        _lib.gc_rope_info(out.ctypes.data)
        return dict(zip(("units", "ossifiers", "wake", "crossings", "memo", "misses"),
                        out.tolist()))

    def rope_absorb(self, min_items=64):
        """Move settled debris and the ossifiers among it from the left end
        of the gas into the rope. Everything an ossifier has passed is
        debris (moving data would have stopped it), so the cut lies left of
        the rightmost A glider in the gas by ROPE_MARGIN; it falls after an
        E particle followed by a gap of at least ROPE_SEP, with only E and
        A particles before it and no ossifier cut in half or straddling a
        unit. Returns the number of items moved."""
        self._own()
        t = self.t
        kind, ids, ph, left, width, _, tc = self.list_items(-FAR, FAR)
        if not len(kind) or kind[0] != SENL:
            raise RuntimeError("rope: no left sentinel")
        orbs = self.reg.orbits
        fam = []
        for k, i in zip(kind, ids):
            if k != PART:
                fam.append("X")
                continue
            o = orbs[int(i)]
            fam.append("A" if 3 * o.d == 2 * o.p else "C" if o.d == 0
                       else "E" if 15 * o.d == -4 * o.p else "X")
        a_pos = [int(left[j]) for j, f in enumerate(fam) if f == "A"]
        if not a_pos:
            return 0
        limit = max(a_pos) - self.ROPE_MARGIN
        cut, open_oss = 0, None          # open_oss: left edge of the last A seen
        for j in range(1, len(kind)):
            f = fam[j]
            if f not in "EA":
                break
            r = int(left[j]) + int(width[j])
            if r > limit:
                break
            if f == "A":
                open_oss = int(left[j])
                continue
            # an E: inside an ossifier's span means a crossing in progress
            nxt = int(left[j + 1]) if j + 1 < len(kind) else None
            if open_oss is not None and int(left[j]) - open_oss < self.ROPE_SEP:
                if j + 1 < len(kind) and fam[j + 1] == "A" and nxt - open_oss < self.ROPE_SEP:
                    break
            if nxt is not None and kind[j + 1] != SENR and nxt - r >= self.ROPE_SEP:
                # the gliders after this cut must not belong to an ossifier before it
                cut = j
        if cut < min_items:
            return 0
        i_last = int(ids[cut])
        o = orbs[i_last]
        hi_max = max(o.off[s] + o.w[s] - o.d * s / o.p for s in range(o.p))
        s = int(ph[cut])
        x_lin = int(left[cut]) - o.off[s] + o.d * s / o.p
        b0 = int(np.ceil(x_lin + 4 * t / 15 + hi_max)) + 2
        _lib.gc_set_side(0, b0, -4, 15)
        self._check(_lib.gc_rope_absorb(cut, self.ROPE_SEP))
        return cut

    def _orbit_flat(self):
        """Flat per-phase arrays of all orbits: base index per orbit,
        offsets, widths; and per orbit p and d."""
        n = len(self.reg.orbits)
        if self._oflat is None or len(self._oflat[0]) < n:
            ob, off, w = [], [], []
            for o in self.reg.orbits:
                ob.append(len(off))
                off.extend(o.off[:o.p])
                w.extend(o.w)
            self._oflat = (np.array(ob, np.int64), np.array(off, np.int64),
                           np.array(w, np.int64),
                           np.array([o.p for o in self.reg.orbits], np.int64),
                           np.array([o.d for o in self.reg.orbits], np.int64))
        return self._oflat

    # -- rendering ------------------------------------------------------------------
    def _key_index(self, kind, ids, ph):
        """Flat index of each (kind, id, phase) key: orbits and entries
        get consecutive slots (one per phase or step), allocated here."""
        while len(self._obase) < len(self.reg.orbits):
            o = self.reg.orbits[len(self._obase)]
            self._obase.append(self._nkeys)
            self._nkeys += o.p
        while len(self._ebase) < len(self.entries):
            e = self.entries[len(self._ebase)]
            self._ebase.append(self._nkeys)
            self._nkeys += e.T + 1
        if len(self._koff) < self._nkeys:
            grow = max(self._nkeys, 2 * len(self._koff)) - len(self._koff)
            self._koff = np.concatenate([self._koff, np.full(grow, -1, np.int64)])
        ob, eb = np.array(self._obase, np.int64), np.array(self._ebase, np.int64)
        part = kind == PART
        kid = np.empty(len(kind), np.int64)
        kid[part] = ob[ids[part]] + ph[part]
        kid[~part] = eb[ids[~part]] + ph[~part]
        # cells of keys not seen before
        new = np.nonzero(self._koff[kid] < 0)[0]
        for j in new:
            k = kid[j]
            if self._koff[k] >= 0:
                continue
            key = self._key(int(kind[j]), int(ids[j]), int(ph[j]))
            cells = cells_of(key[0], key[1])
            if self._ncells + len(cells) > len(self._cellbuf):
                self._cellbuf = np.concatenate(
                    [self._cellbuf, np.zeros(max(len(self._cellbuf), len(cells)), np.uint8)])
            self._cellbuf[self._ncells:self._ncells + len(cells)] = cells
            self._koff[k] = self._ncells
            self._ncells += len(cells)
        return kid

    def list_items(self, lo, hi):
        """Items overlapping [lo, hi) at time t (and the sentinels met), as
        arrays: kind, id, phase or step, left edge, width, cL, creation
        time (0 for untouched layout rows)."""
        cap = 1 << 12
        while True:
            bufs = [np.zeros(cap, np.int32), np.zeros(cap, np.int32), np.zeros(cap, np.int32),
                    np.zeros(cap, np.int64), np.zeros(cap, np.int32), np.zeros(cap, np.int32),
                    np.zeros(cap, np.int64)]
            n = _lib.gc_list(lo, hi, cap, *[q.ctypes.data for q in bufs])
            if n >= 0:
                return [q[:n] for q in bufs]
            cap *= 4

    def window(self, lo, hi):
        """uint8 cells [lo, hi) at time t (vectorized rendering)."""
        self._own()
        self.ensure(lo, hi)
        t = self.t
        kind, ids, ph, left, width, cls, _ = self.list_items(lo, hi)
        sen = kind >= SENL
        if np.any(sen & (kind == SENL) & (left >= lo)) or np.any(sen & (kind == SENR) & (left < hi)):
            raise ValueError(f"window [{lo}, {hi}) reaches an unmaterialized side")
        keep = ~sen
        kind, ids, ph, left, width, cls = (kind[keep], ids[keep], ph[keep], left[keep],
                                           width[keep].astype(np.int64), cls[keep])
        if not len(kind):
            raise ValueError("window: no item found")
        kid = self._key_index(kind, ids, ph)
        # ether: each gap reads the constant of the item right of it; after
        # the last item, that item's right constant
        last = self._key(int(kind[-1]), int(ids[-1]), int(ph[-1]))
        c_end = (last[3] - int(left[-1]) - last[1] - SHIFT * t) % TILE
        # constant per cell, run by run: cells before item k's left edge
        # (and after item k-1's) read item k's constant
        edges = np.clip(left, lo, hi)
        runs = np.diff(np.concatenate([[lo], edges, [hi]]))
        c = np.repeat(np.append(cls.astype(np.int64), c_end), runs)
        out = _ETHER_BITS[(c + np.arange(lo, hi) + SHIFT * t) % TILE]
        # patches
        total = int(width.sum())
        if total:
            starts = np.cumsum(width) - width
            within = np.arange(total) - np.repeat(starts, width)
            pos = np.repeat(left, width) + within - lo
            vals = self._cellbuf[np.repeat(self._koff[kid], width) + within]
            m = (pos >= 0) & (pos < hi - lo)
            out[pos[m]] = vals[m]
        return out

    # -- checkpoints ----------------------------------------------------------------
    def state(self):
        """Everything needed to resume (with the same side sources), as
        plain Python data. Only between advance_to calls."""
        self._own()
        n = self.count()
        small, big = np.zeros(3 * n, np.int32), np.zeros(3 * n, np.int64)
        if _lib.gc_dump(n, small.ctypes.data, big.ctypes.data) != n:
            raise RuntimeError("gasc: dump failed")
        return {"t": self.t, "n_events": self.n_events, "items": (small, big),
                "orbits": [(o.keys, o.off) for o in self.reg.orbits],
                "entries": self.entries, "memo": self.memo, "n_sim": self.n_sim}

    @classmethod
    def from_state(cls, st, sides):
        """Resume from state(): the C tables are rebuilt in the same id
        order and every pending event is recomputed from time t (the first
        collision at or after t is the one originally scheduled, since
        none was skipped)."""
        g = cls()
        for keys, off in st["orbits"]:
            g.reg.add(keys, off)
        g._push_orbits()
        g.memo = st["memo"]
        g.n_sim = st["n_sim"]
        for e in st["entries"]:
            g.entries.append(e)
            g._add_entry(e)
        g.sides = sides
        _lib.gc_set_now(st["t"])
        small, big = st["items"]
        for k in range(len(small) // 3):
            kind = int(small[3 * k])
            if kind in (SENL, SENR):
                g._side_params(0 if kind == SENL else 1)
            if _lib.gc_append(kind, int(small[3 * k + 1]), int(big[3 * k]),
                              int(big[3 * k + 1]), int(small[3 * k + 2]), int(big[3 * k + 2])) < 0:
                g._check(ERR)
        g._rows = None
        g._check(_lib.gc_start())
        g.n_events_before = st["n_events"]
        return g

    @classmethod
    def from_layout(cls, lay):
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
