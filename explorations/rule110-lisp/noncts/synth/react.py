"""General reaction synthesizer: free stationary objects and free moving
trains, joined in reactions, all in one CNF.

Items (shared unknowns, each with its own stability spacetime):
  ObjectVar(W, pR)          stationary, period (7, 0), cells [0, W) at t=0,
                            ether my-phase 0 on the left, pR on the right.
  TrainVar(W, p, d, pR)     moving, period (p, d) (A-trains (3,2), B-trains
                            (4,-2), D-trains (10,2) ...), same layout.
  Fixed(bits, pR)           a known pattern (e.g. a library glider), no
                            stability constraint added.

A Reaction places one object (at its canonical position) and one incoming
train (left of it if d > 0, right if d < 0) at t = 0 and constrains the
row at time T2 as three regions separated by 14-cell ether bands:

    left region [.., a)  |band|  middle [a, b)  |band|  right region [b, ..)

Each region gets a spec:
  None                  pure ether
  ("train", p, d)       nonempty (p, d)-invariant pattern (any train)
  ("is", item)          exactly `item` (ObjectVar/TrainVar/Fixed) at some
                        time phase and position (indicator disjunction)
  ("stationary",)       middle only: any period-(7,0) pattern (may be empty)

Invariance checks use rows T2 and T2 + p (or + 7); the bands guarantee that
each region, embedded alone in ether, evolves exactly as checked. Every
solution is re-simulated with ../../engine.py (`verify_reaction`).
"""

import numpy as np

from r110sat import CNF, Spacetime, TILE, ether_bit, neg, simulate

BAND = 14
# free moving items with period p > 7 are constrained to be ether outside
# [min(0, d tau/p) - M, W + max(0, d tau/p) + M) at row tau (a mild
# restriction of the search space; it makes placements compact)
TIGHT_MARGIN = 6


class Item:
    """Base: an unknown or fixed pattern with canonical frame: cells [0, W)
    at t = 0, ether my-phase 0 left of 0, my-phase pR right of W."""
    period = None   # (p, d)

    def row_lits(self, tau, lo, hi):
        """Literals/constants of the item's canonical spacetime at time
        tau (0 <= tau < p) for x in [lo, hi) (ether outside the cone)."""
        return [self.st.lit(tau, x) for x in range(lo, hi)]

    def extent(self, tau):
        """Cells [lo, hi) at time tau that may differ from ether. The light
        cone [-tau, W + tau) unless the item has tighter extents (moving
        items with p > 7: see TIGHT_MARGIN). Using the cone for long-period
        items made is_item miss real matches (the cone of row 29 of a
        (30,-8) train is W + 58 wide) -> false UNSAT; fixed 03:55."""
        t = getattr(self, "_tight", None)
        return t[tau] if t else (-tau, self.W + tau)

    def default_tight(self, tau):
        import math
        p, d = self.period
        s = d * tau / p
        lo = max(-tau, min(0, math.floor(s)) - TIGHT_MARGIN)
        hi = min(self.W + tau, self.W + max(0, math.ceil(s)) + TIGHT_MARGIN)
        return lo, hi

    def decode(self, sol):
        return np.array([sol.val(self.st.lit(0, x)) for x in range(self.W)],
                        np.uint8)


class ObjectVar(Item):
    def __init__(self, cnf, W, pR, name="O", nonempty=True):
        self.cnf, self.W, self.pR, self.name = cnf, W, pR, name
        self.period = (7, 0)
        self.st = Spacetime(cnf, 7, 0, W, 0, pR)
        self.st.periodic(0, 7, -7, W + 7)
        if nonempty and pR == 0:
            self.st.differs(0, 0, W, [ether_bit(0, 0, x) for x in range(W)])


class TrainVar(Item):
    def __init__(self, cnf, W, p, d, pR, name="H", nonempty=True):
        if (4 * p + d) % TILE:
            raise ValueError("(p, d) not in the ether lattice")
        self.cnf, self.W, self.pR, self.name = cnf, W, pR, name
        self.period = (p, d)
        self.st = Spacetime(cnf, p, 0, W, 0, pR)
        # row p [x + d] == row 0 [x] on the whole modelled line
        for x in range(-p - d - 1, W + p - d + 1):
            if -p <= x + d < W + p:
                cnf.equal(self.st.lit(p, x + d), self.st.lit(0, x))
        if nonempty and pR == 0:
            self.st.differs(0, 0, W, [ether_bit(0, 0, x) for x in range(W)])
        if p > 7:
            self._tight = [self.default_tight(tau) for tau in range(p)]
            for tau in range(1, p):
                lo, hi = self._tight[tau]
                for x in range(-tau, lo):
                    self.st.fix(tau, x, ether_bit(0, tau, x))
                for x in range(hi, W + tau):
                    self.st.fix(tau, x, ether_bit(pR, tau, x))


class Fixed(Item):
    """Known pattern (bits at t=0 on [0, W), phases 0 / pR), with period
    (p, d) given for bookkeeping. Its spacetime is computed by SAT
    propagation (a tiny Spacetime with all t=0 cells constant)."""

    def __init__(self, cnf, bits, pR, period, name="F"):
        self.cnf, self.W, self.pR, self.name = cnf, len(bits), pR, name
        self.period = period
        self.bits = np.array([int(b) for b in bits], np.uint8)
        init = {x: bool(self.bits[x]) for x in range(self.W)}
        self.st = Spacetime(cnf, period[0], 0, self.W, 0, pR, init=init)
        if period[0] > 7:
            self._tight = self._exact_extents()

    def _exact_extents(self):
        """Exact non-ether extent of each row tau, by simulation."""
        p = self.period[0]
        pad = 2 * p + 20
        row = np.concatenate([
            np.array([ether_bit(0, 0, x) for x in range(-pad, 0)], np.uint8),
            self.bits,
            np.array([ether_bit(self.pR, 0, x) for x in range(self.W, self.W + pad)],
                     np.uint8)])
        h = simulate(row, p)
        out = []
        for tau in range(p):
            xs = range(-tau, self.W + tau)
            left = [x for x in xs if h[tau, x + pad] != ether_bit(0, tau, x)]
            right = [x for x in xs if h[tau, x + pad] != ether_bit(self.pR, tau, x)]
            lo = min(left) if left else self.W
            hi = max(right) + 1 if right else 0
            lo, hi = min(lo, hi), max(lo, hi)
            out.append((max(-tau, lo - 1), min(self.W + tau, hi + 1)))
        return out


def _band_indicators(st, t, lo):
    """Row t on [lo, lo + BAND) is ether of some phase: returns the 14
    indicator vars (at least one true)."""
    inds = []
    for ph in range(TILE):
        m = st.cnf.new_var()
        for x in range(lo, lo + BAND):
            l = st.lit(t, x)
            st.cnf.add([-m, l if ether_bit(ph, t, x) else neg(l)])
        inds.append(m)
    st.cnf.add(inds)
    return inds


class Reaction:
    def __init__(self, cnf, obj, train, T2, left=None, middle=("stationary",),
                 right=None, gap=4, mL=10, mR=10, name="R",
                 train_shift=(0, 0), windows=None):
        self.cnf, self.obj, self.train, self.T2 = cnf, obj, train, T2
        self.windows = windows or {}   # tag -> (dmin, dmax) for "is" deltas
        self.name = name
        self.specs = {"L": left, "M": middle, "R": right}
        p_t, d_t = train.period
        W = obj.W
        init = {}
        # train_shift (dt, dx) must be an ether-lattice vector; it moves the
        # train in spacetime (selects the collision class for trains with
        # several classes against the object)
        dt, dx = train_shift
        if (4 * dt + dx) % TILE:
            raise ValueError("train_shift not in the ether lattice")
        q, tau = divmod(-dt, p_t)
        self.tau = tau
        if d_t > 0:
            # base: train left of the object, right phase pR_t - s == 0
            s = -gap - train.W
            s -= (s - train.pR) % TILE
            s2 = s + dx + q * d_t
            if s2 + train.W + tau > -1:
                raise ValueError("shifted train overlaps the object")
            lo, hi = s2 - tau, W
            pfl, pfr = (-s) % TILE, obj.pR
            for x in range(s2 - tau, s2 + train.W + tau):
                init[x] = train.st.lit(tau, x - s2)
            for x in range(s2 + train.W + tau, 0):
                init[x] = bool(ether_bit(0, 0, x))
        else:
            s = W + gap
            s += (-obj.pR - s) % TILE
            s2 = s + dx + q * d_t
            if s2 - tau < W + 1:
                raise ValueError("shifted train overlaps the object")
            lo, hi = 0, s2 + train.W + tau
            pfl, pfr = 0, (train.pR - s) % TILE
            for x in range(W, s2 - tau):
                init[x] = bool(ether_bit(obj.pR, 0, x))
            for x in range(s2 - tau, s2 + train.W + tau):
                init[x] = train.st.lit(tau, x - s2)
        for x in range(W):
            init[x] = obj.st.lit(0, x)
        self.shift = s2
        self.lo, self.hi, self.pfl, self.pfr = lo, hi, pfl, pfr
        P = 7
        for spec in (left, right):
            if spec and spec[0] == "train":
                P = max(P, spec[1])
            if spec and spec[0] == "is":
                P = max(P, spec[1].period[0])
        self.T = T2 + P
        st = Spacetime(cnf, self.T, lo, hi, pfl, pfr, init=init)
        self.st = st
        a, b = -mL, W + mR
        self.a, self.b = a, b
        L, R = lo - T2, hi + T2
        self.L, self.R = L, R
        # bands
        self.bandL = _band_indicators(st, T2, a - BAND)
        self.bandR = _band_indicators(st, T2, b)
        # middle
        if middle is None:
            # pure ether across the middle: phase given by band L
            for ph in range(TILE):
                for x in range(a, b):
                    l = st.lit(T2, x)
                    cnf.add([-self.bandL[ph], l if ether_bit(ph, T2, x) else neg(l)])
        elif middle[0] == "stationary":
            st.periodic(T2, T2 + 7, a - 7, b + 7)
        elif middle[0] == "is":
            self._is(middle[1], a - BAND, b + BAND, "M")
        else:
            raise ValueError(middle)
        # sides
        self._side(left, L, a - BAND, "L")
        self._side(right, b + BAND, R, "R")

    def _side(self, spec, lo, hi, side):
        st, T2 = self.st, self.T2
        far = self.pfl if side == "L" else self.pfr
        band = self.bandL if side == "L" else self.bandR
        if spec is None:
            for x in range(lo, hi):
                st.fix(T2, x, ether_bit(far, T2, x))
            return
        if spec[0] == "train":
            p, d = spec[1], spec[2]
            if side == "L":
                xs = range(lo - p, hi + BAND - 7)
            else:
                xs = range(lo - BAND + 7, hi + p)
            for x in xs:
                self.cnf.equal(st.lit(T2 + p, x + d), st.lit(T2, x))
            # nonempty: the near band's phase differs from the far phase,
            # or some cell of the region differs from far ether
            diff = [neg(st.lit(T2, x)) if ether_bit(far, T2, x) else st.lit(T2, x)
                    for x in range(lo, hi)]
            self.cnf.add([neg(band[far])] + diff)
            return
        if spec[0] == "is":
            self._is(spec[1], lo - (BAND if side == "R" else 0),
                     hi + (BAND if side == "L" else 0), side)
            return
        raise ValueError(spec)

    def _is(self, item, lo, hi, tag):
        """Row T2 on [lo, hi) equals `item` (in some time phase tau and
        shift delta) embedded in ether. Indicator disjunction. For the
        side regions the far ether phase is known, which fixes delta mod
        14 for each tau (options violating it are skipped)."""
        st, T2, cnf = self.st, self.T2, self.cnf
        p = item.period[0]
        opts = []
        win = self.windows.get(tag)
        for tau in range(p):
            ilo, ihi = item.extent(tau)
            for delta in range(lo - ilo, hi - ihi + 1):
                if win and not win[0] <= delta <= win[1]:
                    continue
                # item left ether at time tau: ETHER[x' + 4 tau];
                # placed at x = x' + delta it must be ETHER[x + 4 T2 + ph]
                if tag == "L" and (4 * tau - delta - 4 * T2 - self.pfl) % TILE:
                    continue
                if tag == "R" and (4 * tau + item.pR - delta - 4 * T2
                                   - self.pfr) % TILE:
                    continue
                m = cnf.new_var()
                for x in range(lo, hi):
                    a = st.lit(T2, x)
                    bl = item.st.lit(tau, x - delta)
                    if isinstance(bl, bool):
                        cnf.add([-m, a if bl else neg(a)])
                    else:
                        cnf.add([-m, neg(a), bl])
                        cnf.add([-m, a, neg(bl)])
                opts.append(((tau, delta), m))
        if not opts:
            raise ValueError(f"no placement options for 'is' on {tag}")
        cnf.add([m for _, m in opts])
        setattr(self, "is_" + tag, opts)

    # -- decoding --------------------------------------------------------
    def initial_row(self, sol):
        return np.array([sol.val(self.st.lit(0, x))
                         for x in range(self.lo, self.hi)], np.uint8)

    def row(self, sol, t):
        return np.array([sol.val(self.st.lit(t, x))
                         for x in range(self.lo - t, self.hi + t)], np.uint8)


def default_extra(r, at_least=400):
    import math
    L = 7
    for side in ("L", "R"):
        spec = r.specs[side]
        if spec is None:
            continue
        p = spec[1] if spec[0] == "train" else spec[1].period[0]
        L = L * p // math.gcd(L, p)
    return L * (-(-at_least // L))


def verify_reaction(r, sol, extra=None):
    """Independent forward simulation of the decoded initial row.
    Checks: (1) SAT rows 0..T equal simulation; (2) at T2 + extra, the
    middle region equals the T2 middle (extra multiple of 7) and each
    side region equals its T2 content shifted by its train period."""
    if extra is None:
        extra = default_extra(r)
    lo, hi = r.lo, r.hi
    row0 = r.initial_row(sol)
    Tf = r.T2 + extra
    # wrap-seam debris spreads Tf cells in from each array end; keep all
    # compared cells (up to Tf + |shift| beyond the T2 cone) well inside
    pad = 3 * Tf + 100
    left = np.array([ether_bit(r.pfl, 0, x) for x in range(lo - pad, lo)], np.uint8)
    right = np.array([ether_bit(r.pfr, 0, x) for x in range(hi, hi + pad)], np.uint8)
    h = simulate(np.concatenate([left, row0, right]), Tf)
    off = pad - lo
    out = {}
    out["sat_equals_sim"] = all(
        np.array_equal(h[t, lo - t + off:hi + t + off], r.row(sol, t))
        for t in range(0, r.T + 1, max(1, r.T // 10)))
    a, b, T2 = r.a, r.b, r.T2
    if extra % 7:
        raise ValueError("extra must be a multiple of 7")
    out["middle_persists"] = np.array_equal(
        h[Tf, a - BAND + off:b + BAND + off], h[T2, a - BAND + off:b + BAND + off])
    for side in ("L", "R"):
        spec = r.specs[side]
        if spec is None:
            continue
        p, d = (spec[1], spec[2]) if spec[0] == "train" else spec[1].period
        if extra % p:
            out["side_" + side] = "skipped (extra not multiple of p)"
            continue
        sh = extra // p * d
        if side == "L":
            xs = (r.L - 2, a - BAND)
        else:
            xs = (b + BAND, r.R + 2)
        # content at T2 on the side region (widened), shifted by sh
        x0, x1 = xs
        if side == "L":
            now = h[Tf, x0 + off + sh - 0:x1 + off + sh]
            then = h[T2, x0 + off:x1 + off]
        else:
            now = h[Tf, x0 + off + sh:x1 + off + sh]
            then = h[T2, x0 + off:x1 + off]
        out["side_" + side] = bool(np.array_equal(now, then))
    out["ok"] = all(v is True or (isinstance(v, (bool, np.bool_)) and v)
                    for v in out.values() if not isinstance(v, str))
    return out


def fixed_from_glider(cnf, g, width, k=0):
    """Fixed item for library glider g (lib.Glider) in time-phase k,
    placed in [0, width) with my-phase 0 on its left."""
    from lib import place_after, compose, right_phase_of
    t0, x0 = place_after(g, 0, 0, 0, k)
    st = g.state(t0, x0, 0)
    if st[3] + len(st[0]) > width:
        raise ValueError("width too small")
    cells, pl, pr = compose([st], 0, 0, width, left_p=0)
    # right phase of the composed window at x = width
    return Fixed(cnf, "".join(map(str, cells)), pr, (g.p, g.d), name=g.name)
