"""streamwin.py - exact Rule 110 runs of two-stream scenes on a moving window.

Setting.  A scene = LEFT stream (gliders that all share one period vector
(PL, DL), e.g. A-family (3,2)) + CORE (counters, anything) + RIGHT stream (all
sharing (PR, DR), e.g. G-family (42,-14)), on ether.  Long runs spend almost
all cells on the two streams in free flight.

Free references.  F_L = exact evolution of (left-stream cells + ether to the
right), F_R = exact evolution of (ether + right-stream cells).  Each is a
Rule 110 orbit invariant under its period vector, F(t+P, x+D) = F(t, x); this
is CHECKED at construction (raises if false).  So F(t, x) is a lookup into P
stored rows.

Invariant (rigorous, the fastca argument with ether replaced by F):
    true(t, x) = F_L(t, x) for all x < lo(t),  true(t, x) = F_R(t, x) for x >= hi(t).
The window [lo, hi) is stepped exactly with boundary neighbours F_L(t, lo-1)
and F_R(t, hi).  If the window's first M cells equal F_L(t, .) and its last
M cells equal F_R(t, .) after every step, the invariant is preserved: a
cell outside the window at t+1 depends only on cells that equal F at t, and
F is itself a Rule 110 orbit.  A deviation within M cells of an edge makes
the driver extend the window (filling with F, valid by the invariant).  The
driver also shrinks the window back to the active region (cells equal to F
at an edge may be dropped).  Nothing is assumed about gliders; the checks
are exact cell equalities.  Any failure of the precondition raises.

The only assumption is the input split: left-stream cells must all lie left
of the core, right-stream cells right of it, and the boundary cells between
them must be ether (checked).

Read-out: cells(lo, hi) returns the TRUE row on any range at the current time
(window inside, F_L / F_R outside).
"""
import numpy as np
from numba import njit

import v3
import engine

ETHER = np.array([int(c) for c in "11111000100110"], dtype=np.uint8)
M = 48            # margin that must equal the free reference


def ether(c, lo, hi, t=0):
    return ETHER[(np.arange(lo, hi) + 4 * t + c) % 14]


def phase_at(row, i, x_glob):
    """Time-0 ether phase c of the 14-window starting at row index i (global
    x_glob), or raise."""
    for c in range(14):
        if np.array_equal(row[i:i + 14], ether(c, x_glob, x_glob + 14)):
            return c
    raise ValueError(f"no ether at x={x_glob}")


class FreeStream:
    """A stream's free evolution, F(t, x), from its cells at time 0."""

    def __init__(self, cells, x0, c_left, c_right, P, D):
        self.P, self.D = P, D
        self.cl, self.cr = c_left, c_right
        pad = 4 * (P + abs(D)) + 4 * M + 64
        lo, hi = x0 - pad, x0 + len(cells) + pad
        row = np.concatenate([ether(c_left, lo, x0), cells,
                              ether(c_right, x0 + len(cells), hi)])
        n = len(row)
        # P+1 rows by the exact engine (cyclic tape, seam > P cells from the
        # stored region: pad >= 4P)
        rows = [row]
        w = engine.pack(row)
        for _ in range(P):
            w = engine.step_packed(w)
            rows.append(engine.unpack(w, n))
        cut = 2 * (P + abs(D)) + 8           # seam-free part of every row
        self.xs = lo + cut
        self.rows = np.stack([r[cut:n - cut] for r in rows[:P]]).astype(np.uint8)
        self.W = self.rows.shape[1]
        # periodicity check: row P at x equals row 0 at x - D, where both are
        # seam-free, plus ether consistency outside the stored range
        a, b = cut + max(D, 0) + 1, n - cut + min(D, 0) - 1
        if not np.array_equal(rows[P][a:b], rows[0][a - D:b - D]):
            raise ValueError("stream is not invariant under its period vector")
        if (D + 4 * P) % 14:
            raise ValueError("period vector incompatible with the ether")
        # outside the stored range the reference is ether: check edges
        for r in range(P):
            if not (np.array_equal(self.rows[r][:14], ether(c_left, self.xs, self.xs + 14, r)) and
                    np.array_equal(self.rows[r][-14:],
                                   ether(c_right, self.xs + self.W - 14, self.xs + self.W, r))):
                raise ValueError("stored rows do not end in ether")

    def at(self, t, lo, hi):
        """F(t, x) for x in [lo, hi) (vectorised)."""
        return _ref_range(self.rows, self.xs, self.W, self.cl, self.cr,
                          self.P, self.D, t, lo, hi, ETHER)


@njit(cache=True)
def _ref(rows, xs, W, cl, cr, P, D, t, x, eth):
    r = t % P
    k = t // P
    xp = x - k * D
    i = xp - xs
    if i < 0:
        return eth[(xp + 4 * r + cl) % 14]
    if i >= W:
        return eth[(xp + 4 * r + cr) % 14]
    return rows[r, i]


@njit(cache=True)
def _ref_range(rows, xs, W, cl, cr, P, D, t, lo, hi, eth):
    out = np.empty(hi - lo, np.uint8)
    for x in range(lo, hi):
        out[x - lo] = _ref(rows, xs, W, cl, cr, P, D, t, x, eth)
    return out


@njit(cache=True)
def _run(row, lo, t, nsteps, Lr, Lxs, LW, Lcl, Lcr, LP, LD,
         Rr, Rxs, RW, Rcl, Rcr, RP, RD, eth, margin):
    n = row.shape[0]
    hi = lo + n
    new = np.empty_like(row)
    for _ in range(nsteps):
        lft = _ref(Lr, Lxs, LW, Lcl, Lcr, LP, LD, t, lo - 1, eth)
        rgt = _ref(Rr, Rxs, RW, Rcl, Rcr, RP, RD, t, hi, eth)
        for i in range(n):
            l = row[i - 1] if i > 0 else lft
            c = row[i]
            r = row[i + 1] if i < n - 1 else rgt
            v = (l << 2) | (c << 1) | r
            new[i] = (110 >> v) & 1
        row, new = new, row
        t += 1
        for i in range(margin):
            if row[i] != _ref(Lr, Lxs, LW, Lcl, Lcr, LP, LD, t, lo + i, eth):
                return row, t, 1
            if row[n - 1 - i] != _ref(Rr, Rxs, RW, Rcl, Rcr, RP, RD, t, hi - 1 - i, eth):
                return row, t, 2
    return row, t, 0


class StreamWindow:
    def __init__(self, row, origin, xa, xb, Lper, Rper):
        """row at time 0, row[i] = cell origin + i.  Left stream = cells
        < xa, right stream = cells >= xb (global x); both cuts must sit in
        ether.  Lper/Rper = (P, D) of the left/right stream."""
        ia, ib = xa - origin, xb - origin
        ca = phase_at(row, ia, xa)          # ether phase at the left cut
        cb = phase_at(row, ib - 14, xb - 14)
        c0 = phase_at(row, 0, origin)
        cn = phase_at(row, len(row) - 14, origin + len(row) - 14)
        self.L = FreeStream(row[:ia], origin, c0, ca, *Lper)
        self.R = FreeStream(row[ib:], xb, cb, cn, *Rper)
        self.lo = xa - M
        self.row = row[ia - M:ib + M].copy()
        self.t = 0
        assert np.array_equal(self.row[:M], self.L.at(0, self.lo, self.lo + M))
        assert np.array_equal(self.row[-M:], self.R.at(0, xb, xb + M))
        self.max_width = len(self.row)

    @property
    def hi(self):
        return self.lo + len(self.row)

    def _extend(self, side, k=4 * M):
        if side == 1:
            self.row = np.concatenate([self.L.at(self.t, self.lo - k, self.lo), self.row])
            self.lo -= k
        else:
            self.row = np.concatenate([self.row, self.R.at(self.t, self.hi, self.hi + k)])
        self.max_width = max(self.max_width, len(self.row))

    def _shrink(self):
        fl = self.L.at(self.t, self.lo, self.hi)
        d = np.nonzero(self.row != fl)[0]
        k = (d[0] if len(d) else len(self.row)) - 2 * M
        if k > 2 * M:
            self.row = self.row[k:]
            self.lo += k
        fr = self.R.at(self.t, self.lo, self.hi)
        d = np.nonzero(self.row != fr)[0]
        k = (len(self.row) - 1 - d[-1] if len(d) else len(self.row)) - 2 * M
        if k > 2 * M and len(self.row) - k > 4 * M:
            self.row = self.row[:len(self.row) - k]

    def run(self, T, chunk=500):
        L, R = self.L, self.R
        while self.t < T:
            k = min(chunk, T - self.t)
            row, t, st = _run(self.row, self.lo, self.t, k,
                              L.rows, L.xs, L.W, L.cl, L.cr, L.P, L.D,
                              R.rows, R.xs, R.W, R.cl, R.cr, R.P, R.D, ETHER, M)
            self.row, self.t = row.copy(), t
            if st:
                self._extend(st)
            else:
                self._shrink()
        return self

    def cells(self, lo, hi):
        """True row at the current time on [lo, hi)."""
        out = np.empty(hi - lo, np.uint8)
        x = np.arange(lo, hi)
        a, b = self.lo, self.hi
        m = x < a
        out[m] = self.L.at(self.t, lo, min(hi, a))[:m.sum()] if m.any() else out[m]
        m2 = (x >= a) & (x < b)
        out[m2] = self.row[x[m2] - a]
        m3 = x >= b
        if m3.any():
            s = max(lo, b)
            out[m3] = self.R.at(self.t, s, hi)
        return out


def auto_cuts(row, origin, nleft, nright):
    """Cuts in the middle of the longest ether run between object nleft-1
    and object nleft (and between objects -nright-1 and -nright) of the
    time-0 row, by my typer's object list (global x)."""
    import vlib
    ids = [x - origin for n, x, w, k in vlib.identify(row, origin)]
    rs = vlib.runs(row)

    def cut(a, b):
        best = None
        for f, l, c in rs:
            lo, hi = max(f, a), min(l + 14, b)      # ether cells [lo, hi)
            if hi - lo >= 40 and (best is None or hi - lo > best[1] - best[0]):
                best = (lo, hi)
        if best is None or best[1] - best[0] < 40:
            raise ValueError("no ether gap to cut in")
        return (best[0] + best[1]) // 2

    xa = cut(ids[nleft - 1] + 1, ids[nleft]) if nleft else ids[0] - 2 * M
    xb = cut(ids[-nright - 1] + 1, ids[-nright]) if nright else None
    if xb is None:
        xb = rs[-1][0] + 2 * M + 14          # inside the last ether run
        assert xb + 14 <= len(row), "row too short on the right"
    if not nleft:
        xa = rs[0][1] - 2 * M - 14 if rs[0][1] - 2 * M - 14 > 0 else xa
    return xa + origin, xb + origin


def from_items(left, core, right, Lper=(3, 2), Rper=(42, -14), c_right=0):
    """Build a scene with my builder (right-anchored) and wrap it in a
    StreamWindow.  left/core/right: [(name, t0, x0)] left to right.
    Returns (sw, placed)."""
    import vlib
    items = left + core + right
    pad = 400
    row, org, placed = vlib.build_right(items, c_right=c_right, pad=pad)
    # one typed object per item at time 0 is required for automatic cuts
    ids = vlib.identify(row, org)
    if len(ids) != len(items):
        raise ValueError(f"cannot cut automatically: {len(items)} items, "
                         f"{len(ids)} objects")
    xa, xb = auto_cuts(row, org, len(left), len(right))
    return StreamWindow(row, org, xa, xb, Lper, Rper), placed


def snapshot(sw, extra=300):
    """Typed objects [(name@phase, x)] in the window plus `extra` cells of
    free stream on each side, at the current time."""
    import vlib
    lo, hi = sw.lo - extra, sw.hi + extra
    row = sw.cells(lo, hi)
    return [(n, x) for n, x, w, k in vlib.identify(row, lo)]


def run_packed(sw, T, K=1024):
    """Same contract as StreamWindow.run, but steps the window bit-packed in
    chunks of K steps (much faster for wide windows).  Rigour: if
    true(t) = F_L(t) on x < lo then true(t+s) = F_L(t+s) on x < lo - s
    (F_L is a Rule 110 orbit; information moves <= 1 cell/step), and the
    same on the right.  The chunk is computed on [lo-2K, hi+2K) filled with
    the free streams outside the window, so cells of [lo-K, hi+K) at t+K are
    exact (light cone; the cyclic seam / zero padding stay >= K away).  The
    new window is cut at the first deviation from F_L and the last deviation
    from F_R inside that exact range, minus/plus a margin M."""
    L, R = sw.L, sw.R
    while sw.t < T:
        k = min(K, T - sw.t)
        lo, hi, t = sw.lo, sw.hi, sw.t
        cells = np.concatenate([L.at(t, lo - 2 * k, lo), sw.row, R.at(t, hi, hi + 2 * k)])
        n = len(cells)
        c = engine.unpack(engine.step_packed_n(engine.pack(cells), k), n)
        ex_lo, ex_hi = lo - k, hi + k
        seg = c[k:n - k]
        assert len(seg) == ex_hi - ex_lo
        t2 = t + k
        dl = np.nonzero(seg != L.at(t2, ex_lo, ex_hi))[0]
        dr = np.nonzero(seg != R.at(t2, ex_lo, ex_hi))[0]
        a = ex_lo + (dl[0] if len(dl) else len(seg))
        b = ex_lo + (dr[-1] + 1 if len(dr) else 0)
        nlo, nhi = min(a, b) - M, max(a, b) + M
        new = np.empty(nhi - nlo, np.uint8)
        x = np.arange(nlo, nhi)
        m1, m3 = x < ex_lo, x >= ex_hi
        m2 = ~m1 & ~m3
        if m1.any():
            new[m1] = L.at(t2, nlo, ex_lo)
        new[m2] = seg[x[m2] - ex_lo]
        if m3.any():
            new[m3] = R.at(t2, ex_hi, nhi)
        sw.row, sw.lo, sw.t = new, nlo, t2
        sw.max_width = max(sw.max_width, len(new))
    return sw


def counters(objs):
    """E-family counters [(value, x, name@phase)] left to right (E^k has
    value k-1; Ebar is not a counter)."""
    out = []
    for n, x in objs:
        b = n.split("@")[0]
        if b == "E":
            out.append((0, x, n))
        elif b.startswith("E^"):
            out.append((int(b[2:]) - 1, x, n))
    return out


def timeline(sw, T, every, K=1024):
    """Run to T (packed), snapshot every `every` steps.  Returns
    [(t, objects, counters)]; consecutive identical counter-value lists
    are kept (cheap to post-process)."""
    out = []
    while sw.t < T:
        run_packed(sw, min(T, sw.t + every), K=K)
        objs = snapshot(sw)
        out.append((sw.t, objs, counters(objs)))
    return out
