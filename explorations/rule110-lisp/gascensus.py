"""The read check's census, taken from the event engine's particles.

experiments.sample renders the whole watched span (~2e5 cells on the
three-state machine) and runs census() on it: most of a long run's time.
Here the span is cut into clumps of items (gaps under G_JOIN cells):

- A rigid clump - every item an old particle (TOO_YOUNG steps or more
  since it was made, or an untouched layout row), all one velocity, and
  nothing else within M_ISO cells - has, over the census's 30-step
  history, exactly the cells of the clump evolving alone in ether, and
  the census of a cluster only looks at the cluster, two cells around it
  and their positions up to 30 steps back. So its clusters are those of
  the clump alone, which depend only on its items' orbits, phases and
  relative offsets: computed once (census() on the clump rendered alone)
  and memoized. The untouched table repeats, so this is the common case.
- Every other clump (a collision under way, young particles, different
  velocities nearby) gets census() on a local window, exactly as
  experiments.sample does on the whole span.

The result is the same list of (Ebar-frame position, kind) that sample
gives, for every cluster ReadWatch looks at (inside the watched
regions); mode "both" in gasrun.GasReads computes the two and raises on
any difference.
"""

from fractions import Fraction

import numpy as np

from census import census
from gas import SHIFT, TILE, cells_of

G_JOIN = 32        # items closer than this form one clump
M_ISO = 96         # a rigid clump has only same-velocity old particles this near
TOO_YOUNG = 64     # steps a particle must have existed to have its own past
PAD = 64           # ether around a clump in its rendering / local window
OWN = 14           # a clump owns the clusters starting within this of it
FLAG_REACH = 216   # at the sample time: M_ISO + 2 x the census depth (<= 59)

_ETHER = np.array([int(c) for c in "11111000100110"], dtype=np.uint8)
KINDS = ("E", "C", "A", "?")


class _Rows:
    """Some rows of a 31-row history, indexed like the whole array."""

    def __init__(self, rows, width):
        self.rows, self.n, self.shape = rows, 31, (31, width)

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        k = i + self.n if i < 0 else i
        if k not in self.rows:
            raise KeyError(f"history row {i} was not kept")
        return self.rows[k]


class ParticleCensus:
    def __init__(self, g):
        self.g = g
        self.memo = {}                  # clump composition -> clusters
        self._k_start = np.zeros(0, np.int64)   # single particles, by key index
        self._k_count = np.zeros(0, np.int64)
        self._f_off, self._f_kind = [], []
        self._f_off_a = np.zeros(0, np.int64)
        self._f_kind_a = np.zeros(0, np.int8)
        self.stats = {"memo": 0, "rendered": 0, "local_cells": 0, "span_cells": 0}

    # -- the particles' geometry -----------------------------------------------------
    def _at(self, oid, ph, left, k):
        """(key, left) of a particle k steps before the state (ph, left)."""
        o = self.g.reg.orbits[oid]
        base = left - o.off[ph]
        j = ph - k
        q, s = divmod(j, o.p)
        return o.keys[s], base + q * o.d + o.off[s]

    def _render_clump(self, parts, T):
        """census() of a clump alone in ether. parts: [(oid, phase, left,
        cL)] at time T, left to right. -> [(x, kind)] in lab columns."""
        lo = parts[0][2] - PAD
        last_key, last_left = self._at(parts[-1][0], parts[-1][1], parts[-1][2], 0)
        hi = last_left + last_key[1] + PAD
        cR = (last_key[3] - last_left - last_key[1] - SHIFT * T) % TILE
        xs = np.arange(lo, hi)
        rows = {}
        for back, k in ((0, 30), (3, 27), (7, 23), (30, 0)):
            t = T - back
            placed = [(self._at(oid, ph, left, back), cL) for oid, ph, left, cL in parts]
            # ether: each gap reads the constant of the item right of it
            edges = [l for (_, l), _ in placed]
            runs = np.diff(np.concatenate([[lo], np.clip(edges, lo, hi), [hi]]))
            c = np.repeat(np.array([cl for _, cl in placed] + [cR], dtype=np.int64), runs)
            row = _ETHER[(c + xs + SHIFT * t) % TILE]
            for (key, l), _ in placed:
                row[l - lo:l - lo + key[1]] = cells_of(key[0], key[1])
            rows[k] = row
        return [(int(x0) + lo, kind) for x0, _, kind in census(_Rows(rows, hi - lo))]

    # -- memo of single particles, flat for vectorized lookup -----------------------
    def _missing(self, kid):
        """Mask of key indices not rendered yet (beyond the table, or -1)."""
        out = kid >= len(self._k_start)
        inside = ~out
        out[inside] = self._k_start[kid[inside]] < 0
        return out

    def _single(self, kid, oid, ph, T):
        """Clusters of one particle alone (orbit oid at phase ph), stored
        flat: kid -> rows of the flat offset / kind arrays."""
        if kid >= len(self._k_start):
            grow = max(kid + 1, 2 * len(self._k_start)) - len(self._k_start)
            self._k_start = np.concatenate([self._k_start, np.full(grow, -1, np.int64)])
            self._k_count = np.concatenate([self._k_count, np.zeros(grow, np.int64)])
        if self._k_start[kid] < 0:
            key, l = self._at(oid, ph, 0, 0)
            cl = (key[2] - l - SHIFT * T) % TILE
            res = self._render_clump([(oid, ph, 0, cl)], T)
            self._k_start[kid] = len(self._f_off)
            self._k_count[kid] = len(res)
            self._f_off.extend(x - l for x, _ in res)
            self._f_kind.extend(KINDS.index(k) for _, k in res)
            self._f_off_a = np.array(self._f_off, np.int64)
            self._f_kind_a = np.array(self._f_kind, np.int8)
            self.stats["rendered"] += 1

    # -- one sample -----------------------------------------------------------------
    def rel(self, watch, pending, depth):
        """(T, [(Ebar-frame x, kind)]) as experiments.sample would observe,
        the gas at time t and the census at T = t + depth."""
        g = self.g
        t, T = g.t, g.t + depth
        if T % 30:
            raise ValueError(f"census at t={T}: not 0 mod 30")
        lo_g, hi_g = watch.span(pending)
        lo, hi = lo_g + g.ebar_frame(t), hi_g + g.ebar_frame(t)
        reach = FLAG_REACH + PAD + depth
        list_lo, list_hi = lo - reach, hi + reach
        g.ensure(list_lo, list_hi)
        kind, ids, ph, left, width, cls, tc = g.list_items(list_lo, list_hi)
        keep = kind < 3                                    # no sentinels
        kind, ids, ph, left, width, cls, tc = (a[keep] for a in (kind, ids, ph, left, width, cls, tc))
        ids, ph, width = ids.astype(np.int64), ph.astype(np.int64), width.astype(np.int64)
        n = len(kind)
        if n == 0:
            raise RuntimeError("particle census: no items")
        ob, ooff, ow, op, od = g._orbit_flat()
        part = kind == 1
        oid = np.where(part, ids, 0)
        # velocity class: one integer per (d, p) in lowest terms; composites -1
        p_, d_ = op[oid], od[oid]
        gcd = np.gcd(p_, np.abs(d_))
        vkey = np.where(part, (d_ // gcd) * 1_000_003 + p_ // gcd, -1)
        _, vel = np.unique(vkey, return_inverse=True)
        old = part & ((tc == 0) | (T - tc >= TOO_YOUNG))
        # flagged: not an old particle, or a different velocity within reach,
        # or so close to the listing's ends that a neighbour may be unseen
        right = left + width
        a = np.searchsorted(right, left - FLAG_REACH, side="left")
        b = np.searchsorted(left, right + FLAG_REACH, side="right") - 1
        run_id = np.concatenate([[0], np.cumsum(vel[1:] != vel[:-1])])
        flagged = (~old | (run_id[a] != run_id[b])
                   | (left - FLAG_REACH < list_lo) | (right + FLAG_REACH > list_hi))
        # states at T: by the orbit for unflagged particles (nothing can
        # reach them before T), widened by depth for flagged items
        base = left - ooff[ob[oid] + ph]
        q, sT = np.divmod(ph + depth, p_)
        lT = np.where(flagged, left - depth, base + q * d_ + ooff[ob[oid] + sT])
        rT = np.where(flagged, right + depth, lT + ow[ob[oid] + sT])
        phT = np.where(flagged, ph, sT)
        # (widened flagged items may overlap their neighbours: sort by left)
        order = np.argsort(lT, kind="stable")
        oid, phT, lT, rT, cls, flagged = (x[order] for x in (oid, phT, lT, rT, cls, flagged))
        # clumps at T
        gap = lT[1:] - np.maximum.accumulate(rT)[:-1]
        starts = np.r_[0, np.nonzero(gap >= G_JOIN)[0] + 1]
        ends = np.r_[starts[1:], n]
        c_lo = lT[starts]
        c_hi = np.maximum.reduceat(rT, starts)
        c_flag = np.logical_or.reduceat(flagged, starts)
        # rigid: no flagged item within M_ISO of the clump
        fl_lo, fl_hi = lT[flagged], rT[flagged]
        if len(fl_lo):
            near = (np.searchsorted(fl_lo, c_hi + M_ISO, side="right") >
                    np.searchsorted(np.maximum.accumulate(fl_hi), c_lo - M_ISO, side="left"))
        else:
            near = np.zeros(len(starts), bool)
        in_span = (c_hi >= lo) & (c_lo < hi)
        rigid = ~c_flag & ~near
        xs, ks = [], []
        # rigid single particles: flat memo, vectorized
        single = rigid & in_span & (ends - starts == 1)
        si = starts[single]
        kid = ob[oid[si]] + phT[si]
        for k in np.unique(kid[self._missing(kid)]):
            j = si[np.nonzero(kid == k)[0][0]]
            self._single(int(k), int(oid[j]), int(phT[j]), T)
        if len(si):
            st, ct = self._k_start[kid], self._k_count[kid]
            tot = int(ct.sum())
            first = np.repeat(np.cumsum(ct) - ct, ct)
            idx = np.repeat(st, ct) + np.arange(tot) - first
            xs.append(np.repeat(lT[si], ct) + self._f_off_a[idx])
            ks.append(self._f_kind_a[idx])
            self.stats["memo"] += len(si)
        # rigid clumps of several particles: memo by composition
        for c in np.nonzero(rigid & in_span & (ends - starts > 1))[0]:
            sl = slice(starts[c], ends[c])
            bse = lT[starts[c]]
            key = (oid[sl].tobytes(), phT[sl].tobytes(), (lT[sl] - bse).tobytes())
            res = self.memo.get(key)
            if res is None:
                parts = [(int(o_), int(p__), int(l_), int(c_))
                         for o_, p__, l_, c_ in zip(oid[sl], phT[sl], lT[sl], cls[sl])]
                cl = self._render_clump(parts, T)
                res = (np.array([x - bse for x, _ in cl], np.int64),
                       np.array([KINDS.index(k) for _, k in cl], np.int8))
                self.memo[key] = res
                self.stats["rendered"] += 1
            else:
                self.stats["memo"] += 1
            xs.append(res[0] + bse)
            ks.append(res[1])
        # every other clump: census() on a local window, as sample() does
        loose = np.nonzero(~rigid & (c_hi >= lo - PAD) & (c_lo < hi + PAD))[0]
        windows = []
        for c in loose:
            w_lo, w_hi = c_lo[c] - PAD, c_hi[c] + PAD
            if windows and w_lo <= windows[-1][1]:
                windows[-1][1] = max(windows[-1][1], w_hi)
                windows[-1][2].append(c)
            else:
                windows.append([w_lo, w_hi, [c]])
        for w_lo, w_hi, cs in windows:
            # history() takes lab columns at time t and returns rows over the
            # same columns up to T; the clumps' extents at T lie inside
            hist = g.history(int(w_lo), int(w_hi), depth)
            self.stats["local_cells"] += int(w_hi - w_lo)
            for x0, _, k in census(hist):
                x = int(x0) + int(w_lo)
                if any(c_lo[c] - OWN <= x <= c_hi[c] + OWN for c in cs):
                    xs.append(np.array([x], np.int64))
                    ks.append(np.array([KINDS.index(k)], np.int8))
        self.stats["span_cells"] += int(hi - lo)
        if not xs:
            return T, []
        x = np.concatenate(xs)
        k = np.concatenate(ks)
        m = (x >= lo) & (x < hi)
        x, k = x[m], k[m]
        o = np.lexsort((k, x))
        sh = g.ebar_frame(T)
        return T, list(zip((x[o] - sh).tolist(), [KINDS[i] for i in k[o].tolist()]))


class LightCensus:
    """A lighter read check: the watched regions' contents from the
    engine's particles, without rendering cells.

    The table's components and the moving data made from them are
    E-family particles (Ebar speed), static in the Ebar frame until a read
    touches them. Each is listed as (its Ebar-frame left edge at T, "E"),
    with T = t + depth = 0 mod 30 as for the census, so an untouched
    particle gives the same entry at every sample. Every other item
    (another velocity, or a composite: a sweep or crossing under way) is
    listed as (its Ebar-frame left edge at t, "?"), which ReadWatch reads
    as "not settled". ReadWatch then works unchanged: a read starts when a
    region's entries change, settles when they stop changing with no "?"
    inside, and is Y or N by the number of "E" entries (one per census
    Ebar cluster: measured equal on every Y read of car, 95-288 each).

    It is not the census: it trusts the engine's particle bookkeeping
    instead of looking at cells. gasrun.GasReads(census="light") checks
    it against the census on every spot_every-th read."""

    REACH = 64         # cells listed beyond the span (items straddling it)

    def __init__(self, g):
        self.g = g
        self._efam = np.zeros(0, bool)

    def _e_family(self):
        ob, ooff, ow, op, od = self.g._orbit_flat()
        if len(self._efam) != len(op):
            self._efam = 15 * od == -4 * op
        return self._efam

    def rel(self, watch, pending, depth):
        """(T, sorted [(Ebar-frame x, "E" or "?")]) for the pending span."""
        g = self.g
        t, T = g.t, g.t + depth
        if T % 30:
            raise ValueError(f"light census at t={T}: not 0 mod 30")
        lo_g, hi_g = watch.span(pending)
        sh_t, sh_T = g.ebar_frame(t), g.ebar_frame(T)
        lo, hi = lo_g + sh_t - self.REACH - depth, hi_g + sh_t + self.REACH + depth
        g.ensure(lo, hi)
        kind, ids, ph, left, _, _, _ = g.list_items(lo, hi)
        keep = kind < 3                                    # no sentinels
        kind, ids, ph, left = kind[keep], ids[keep].astype(np.int64), ph[keep].astype(np.int64), left[keep]
        efam = self._e_family()
        ob, ooff, ow, op, od = g._orbit_flat()
        part = kind == 1
        oid = np.where(part, ids, 0)
        e = part & efam[oid]
        oe, pe = oid[e], ph[e]
        q, sT = np.divmod(pe + depth, op[oe])
        xe = left[e] - ooff[ob[oe] + pe] + q * od[oe] + ooff[ob[oe] + sT] - sh_T
        xo = left[~e] - sh_t
        out = list(zip(xe.tolist(), ["E"] * len(xe))) + list(zip(xo.tolist(), ["?"] * len(xo)))
        out.sort()
        return T, out
