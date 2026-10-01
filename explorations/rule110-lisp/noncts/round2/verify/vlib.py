"""verify/vlib.py - an independent Rule 110 glider toolkit for verification.

Written from scratch (round 2, agent verify) so that teammates' claims can be
re-checked through a code path that shares nothing with collider/, synth/ or
scholar/ except the Rule 110 update itself (which I also re-implement and
cross-check against ../../../engine.py).

Conventions
-----------
Global ether. At time t the unperturbed background reads
    E(t, x) = ETHER[(x + 4 t + c) mod 14]
for a region "phase" c. (The ether is invariant under (dt, dx) = (1, -4):
7*1 + 3*(-2) = 1 gives (7,0) - 2*(3,2) = (1,-4).) Every glider changes the
region phase by its width w (charge): c_right = c_left + w (mod 14).

Glider records. A glider is given by a base row B: ether (phase 0 at x = 0)
+ core + ether, plus its period (P, D): B evolved P steps equals B shifted
by D cells. Base rows come from the Martinez phase-f1_1 strings (published,
arXiv:0706.3348 App. A), or are harvested from my own simulations
(compounds such as E^n, G B^k).

Placement. `build(items)` takes (name, t0, x0) triples ordered left to right:
"glider `name` whose base row sits at spacetime event (t0, x0)", i.e. at time
t0 its base row's cell 0 is at global x0. Rows are returned at global time 0.
Constraint: x0 + 4 t0 + c_left = 0 (mod 14), c_left the phase of the region
the glider starts in; `place` returns the nearest valid x0.

Typing. `objects(row)` segments a row into ether runs and defects and keys
each defect canonically: (cells not explained by either neighbouring ether,
alignment mod 14, width). Keys of every phase of every library glider are
precomputed, so identification is an exact lookup.
"""

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, ROOT)
import engine  # noqa: E402  (exact Rule 110, used for cross-checks and speed)

ETHER = np.array([int(c) for c in "11111000100110"], dtype=np.uint8)
T14 = 14

# Martinez et al. 2008, phase f1_1 strings (ether* + s + ether*), and the
# periods (P, D) they report. I re-verify every period below.
MARTINEZ = {
    "A": ("111110", (3, 2)),
    "B": ("11111010", (4, -2)),
    "Bbar": ("1111100010110111100110", (12, -6)),
    "Bhat": ("111110001011011110011001111111000100110", (12, -6)),
    "C1": ("111110000", (7, 0)),
    "C2": ("11111000000100110", (7, 0)),
    "C3": ("11111011010", (7, 0)),
    "D1": ("11111000010", (10, 2)),
    "D2": ("1111101011000100110", (10, 2)),
    "E": ("1111100000000100110", (15, -4)),
    "Ebar": ("111110000100011111010", (30, -8)),
    "F": ("111110001011010", (36, -4)),
    "G": ("111110100111110011100110", (42, -14)),
    "H": ("11111000101100000000111110001001101001111111000100110", (92, -18)),
}

# Family periods used for velocity typing of unknown clusters.
FAMILY = {"A": (3, 2), "B": (4, -2), "C": (7, 0), "D": (10, 2),
          "E": (15, -4), "F": (36, -4), "G": (42, -14), "H": (92, -18),
          "Bbar": (12, -6), "gun": (77, -20)}


# ---------------------------------------------------------------- dynamics

def step(row):
    """One Rule 110 step on a finite row; the two edge cells are computed
    as if the row continued with its own ether (callers keep margins wide
    enough that edge effects never reach the region of interest)."""
    l = np.empty_like(row)
    r = np.empty_like(row)
    l[1:] = row[:-1]
    l[0] = row[0]
    r[:-1] = row[1:]
    r[-1] = row[-1]
    return (row | r) & (1 - (l & row & r))


def evolve(row, T):
    """Row after T steps. Uses the compiled cyclic engine; the wrap seam is
    harmless as long as the margins exceed T (checked by `check_margins`)."""
    n = len(row)
    w = engine.pack(row.astype(np.uint8))
    w = engine.step_packed_n(w, T)
    return engine.unpack(w, n)


def history(row, T):
    """(T+1, n) array of rows; my own stepper (finite, ether-padded)."""
    out = np.empty((T + 1, len(row)), dtype=np.uint8)
    out[0] = row
    for t in range(T):
        out[t + 1] = step(out[t])
    return out


# ---------------------------------------------------------------- ether phase

def ether_row(c, lo, hi, t=0):
    x = np.arange(lo, hi)
    return ETHER[(x + 4 * t + c) % T14]


def window_phase(row):
    """Per window start x: phase c with row[x+k] = ETHER[(x+k+c) % 14] for
    k < 14, or -1. (Row at time 0; for time t subtract 4t yourself.)"""
    n = len(row)
    out = np.full(n, -1, dtype=np.int64)
    if n < T14:
        return out
    win = np.lib.stride_tricks.sliding_window_view(row, T14)
    for c in range(T14):
        pat = ETHER[(np.arange(T14) + c) % T14]
        # window at x matches phase c' where (x + c') = c (mod 14)
        m = np.all(win == pat, axis=1)
        xs = np.nonzero(m)[0]
        out[xs] = (c - xs) % T14
    return out


def runs(row):
    """Maximal ether runs as (first_window, last_window, phase)."""
    ph = window_phase(row)
    xs = np.nonzero(ph >= 0)[0]
    res = []
    if len(xs) == 0:
        return res
    start = xs[0]
    for i in range(1, len(xs) + 1):
        if i == len(xs) or xs[i] != xs[i - 1] + 1 or ph[xs[i]] != ph[xs[i - 1]]:
            res.append((int(start), int(xs[i - 1]), int(ph[xs[i - 1]])))
            if i < len(xs):
                start = xs[i]
    return res


def defects(row, min_run=1):
    """Defects between consecutive ether runs: list of dicts with the cells
    not explained by the left ether (extended right) and the right ether
    (extended left). Keys are translation invariant."""
    rs = [r for r in runs(row) if r[1] - r[0] + 1 >= min_run]
    out = []
    n = len(row)
    for (a0, a1, cl), (b0, b1, cr) in zip(rs, rs[1:]):
        # left ether explains cells up to the first mismatch after a1
        x = a1 + T14
        while x < n and row[x] == ETHER[(x + cl) % T14]:
            x += 1
        lo = x
        y = b0 - 1
        while y >= 0 and row[y] == ETHER[(y + cr) % T14]:
            y -= 1
        hi = y + 1
        if hi <= lo:        # pure phase slip with no unexplained cell
            lo, hi = hi, lo
        cells = tuple(int(v) for v in row[lo:hi])
        key = (cells, (lo + cl) % T14, (cr - cl) % T14)
        out.append({"lo": lo, "hi": hi, "cl": cl, "cr": cr, "key": key,
                    "w": (cr - cl) % T14})
    return out


# ---------------------------------------------------------------- library

class Glider:
    def __init__(self, name, base, period, lo, hi):
        self.name = name
        self.base = base            # uint8 row, left ether phase 0 at x=0
        self.P, self.D = period
        self.lo, self.hi = lo, hi   # core bounds in base coordinates
        rs = runs(base)
        assert rs[0][2] == 0, (name, rs[0])
        self.w = (rs[-1][2] - rs[0][2]) % T14

    def snapshot(self, s):
        """Base evolved s steps (0 <= s < P): (row, x offset of row[0]) in
        base coordinates. Rows carry wide margins."""
        m = self.P + 40 + abs(self.D)
        row = np.concatenate([ether_row(0, -m * 1, 0), self.base,
                              ether_row(self.w, len(self.base),
                                        len(self.base) + m)])
        # ether_row(c, lo, hi) uses global x; left part phase 0, right w
        h = row
        for _ in range(s):
            h = step(h)
        # my finite stepper corrupts one cell per step at each edge: trim
        return h[s:len(h) - s].copy(), -m + s


def _martinez_base(s, margin_tiles=4):
    left = np.tile(ETHER, margin_tiles)
    right = np.tile(ETHER, margin_tiles)
    core = np.array([int(c) for c in s], dtype=np.uint8)
    return np.concatenate([left, core, right]), len(left), len(left) + len(core)


LIB = {}          # name -> Glider
KEYS = {}         # defect key -> (name, phase s)
MULTI = {}        # first defect key -> [(name, s, ((key, rel_lo), ...))]


def verify_period(base, P, D, margin=None):
    """True iff base evolved P steps equals base shifted by D (checked on
    the region away from the margins)."""
    m = margin or (P + abs(D) + 30)
    w = runs(base)
    wr = (w[-1][2] - w[0][2]) % T14
    row = np.concatenate([ether_row(0, -m, 0), base,
                          ether_row(wr, len(base), len(base) + m)])
    h = row
    for _ in range(P):
        h = step(h)
    # compare h[x] with row[x - D] on the interior
    a, b = m, m + len(base)
    return np.array_equal(h[a:b], row[a - D:b - D]) and \
        np.array_equal(h[a - 20:a], row[a - 20 - D:a - D])


def register(name, base, period, check=True):
    P, D = period
    if check and not verify_period(base, P, D):
        raise ValueError(f"{name}: period {period} does not hold")
    ds = defects(base)
    lo = min(d["lo"] for d in ds) if ds else 0
    hi = max(d["hi"] for d in ds) if ds else 0
    g = Glider(name, base, period, lo, hi)
    LIB[name] = g
    for s in range(P):
        row, off = g.snapshot(s)
        dd = defects(row)
        if len(dd) != 1:
            # compounds may split into several defects (separated by ether)
            # in some phases: remember the sequence of keys and offsets
            seq = tuple((d["key"], d["lo"] - dd[0]["lo"]) for d in dd)
            MULTI.setdefault(seq[0][0], []).append((name, s, seq))
            continue
        key = dd[0]["key"]
        if key in KEYS and KEYS[key][0] != name:
            raise ValueError(f"key clash {name} vs {KEYS[key]}")
        KEYS.setdefault(key, (name, s))
    return g


def init_martinez():
    for name, (s, per) in MARTINEZ.items():
        base, lo, hi = _martinez_base(s)
        register(name, base, per)


# ---------------------------------------------------------------- building

def glider_state(name, t0, x0):
    """(row, start_x, left_phase_needed) of glider `name` at global time 0,
    base row at event (t0, x0). Row is the snapshot with margins."""
    g = LIB[name]
    s = (-t0) % g.P
    k = (s + t0) // g.P
    row, off = g.snapshot(s)
    start = x0 + off - k * g.D
    return row, start


def place(name, t0, x_approx, c_left):
    """Nearest x0 >= x_approx with x0 + 4 t0 + c_left = 0 mod 14."""
    x0 = x_approx
    while (x0 + 4 * t0 + c_left) % T14:
        x0 += 1
    return x0


def build(items, width=None, pad=None, c0=0, T=0):
    """items: [(name, t0, x0)] left to right (x0 need not be aligned: the
    nearest valid x0 >= given is used; returned as `placed`).
    Returns (row, origin, placed): row[i] is global cell i + origin at time 0.
    pad: ether margin on each side (default T + 100)."""
    pad = pad if pad is not None else 2 * T + 100
    c = c0
    pieces = []           # (start_global, cells)
    placed = []
    for name, t0, x0 in items:
        g = LIB[name]
        x0 = place(name, t0, x0, c)
        row, start = glider_state(name, t0, x0)
        # the snapshot's left ether is phase 0 in base coords at time s;
        # check it matches the global phase c at time 0
        placed.append((name, t0, x0))
        pieces.append((start, row, c, (c + g.w) % T14))
        c = (c + g.w) % T14
    # assemble: cut between consecutive pieces in the middle of the ether gap
    lo = pieces[0][0] - pad
    hi = pieces[-1][0] + len(pieces[-1][1]) + pad
    out = np.empty(hi - lo, dtype=np.uint8)
    # default: ether at the phase of each region
    cuts = [lo]
    for i in range(len(pieces) - 1):
        s0, r0, _, _ = pieces[i]
        s1, r1, _, _ = pieces[i + 1]
        # core of piece i ends around s0 + len(r0) - margin; take midpoint of
        # the two snapshots' interior ether: use defect bounds
        d0 = defects(r0)
        d1 = defects(r1)
        e0 = s0 + max(d["hi"] for d in d0)
        b1 = s1 + min(d["lo"] for d in d1)
        if b1 - e0 < 0:
            raise ValueError(f"gliders {i} and {i+1} overlap ({e0} > {b1})")
        cuts.append((e0 + b1) // 2)
    cuts.append(hi)
    for i, (s0, r0, cl, cr) in enumerate(pieces):
        a, b = cuts[i], cuts[i + 1]
        x = np.arange(a, b)
        seg = np.where(True, 0, 0) * x  # placeholder
        # fill with the snapshot where it covers, else with region ether
        seg = np.empty(b - a, dtype=np.uint8)
        d = defects(r0)
        core_lo = s0 + min(dd["lo"] for dd in d)
        core_hi = s0 + max(dd["hi"] for dd in d)
        left = x < core_lo
        right = x >= core_hi
        mid = ~left & ~right
        seg[left] = ETHER[(x[left] + cl) % T14]
        seg[right] = ETHER[(x[right] + cr) % T14]
        seg[mid] = r0[x[mid] - s0]
        # consistency: the snapshot's own ether must agree on its covered part
        cov = (x >= s0) & (x < s0 + len(r0))
        if not np.array_equal(seg[cov], r0[x[cov] - s0]):
            bad = np.nonzero(seg[cov] != r0[x[cov] - s0])[0]
            raise ValueError(f"phase mismatch placing {placed[i]} "
                             f"(first bad at {x[cov][bad[0]]})")
        out[a - lo:b - lo] = seg
    return out, lo, placed


# ---------------------------------------------------------------- typing

def identify(row, origin=0, T=0):
    """List of (name_or_?, x_lo_global, width_charge, key) for each defect.
    Glider phase s is included when known: name@s. Unknown defects are
    reported as '?'. T: steps the row has been evolved with `evolve`; the
    T + 16 cells at each end (possibly touched by the wrap seam) are
    ignored."""
    res = []
    cut = T + 16 if T else 0
    sub = row[cut:len(row) - cut] if cut else row
    ds = [dict(d, lo=d["lo"] + cut) for d in defects(sub)]
    i = 0
    while i < len(ds):
        d = ds[i]
        best = None
        for name, s, seq in MULTI.get(d["key"], []):
            m = len(seq)
            if i + m > len(ds):
                continue
            if all(ds[i + j]["key"] == seq[j][0] and
                   ds[i + j]["lo"] - d["lo"] == seq[j][1] for j in range(m)):
                if best is None or m > best[2]:
                    best = (name, s, m)
        if best:
            name, s, m = best
            w = sum(ds[i + j]["w"] for j in range(m)) % T14
            key = tuple(ds[i + j]["key"] for j in range(m))
            res.append((f"{name}@{s}", d["lo"] + origin, w, key))
            i += m
            continue
        nm = KEYS.get(d["key"])
        res.append((f"{nm[0]}@{nm[1]}" if nm else "?", d["lo"] + origin,
                    d["w"], d["key"]))
        i += 1
    return res


def names(row):
    return [r[0].split("@")[0] for r in identify(row)]


def velocity_type(row, T_extra=400, fam=FAMILY):
    """For each defect in `row`, the families whose period leaves it
    invariant (evolve and compare). Coarse; used for unknown clusters."""
    h = history(row, max(p for p, _ in fam.values()) + 1)
    out = []
    for d in defects(row):
        a, b = d["lo"] - 3, d["hi"] + 3
        kinds = []
        for f, (P, D) in fam.items():
            if a + D < 0 or b + D > len(row):
                continue
            if np.array_equal(h[P][a + D:b + D], h[0][a:b]):
                kinds.append(f)
        out.append((d["lo"], d["w"], kinds))
    return out


# ---------------------------------------------------------------- self test

def selftest():
    # 1. my stepper vs engine.step on a random cyclic tape
    rng = np.random.default_rng(1)
    tape = rng.integers(0, 2, 280, dtype=np.uint8)
    a = tape.copy()
    for _ in range(50):
        a2 = engine.step(a)
        l = np.roll(a, 1)
        r = np.roll(a, -1)
        mine = (a | r) & (1 - (l & a & r))
        assert np.array_equal(a2, mine)
        a = a2
    # 2. ether phase law: E(t+1, x) = E(t, x + 4)
    e = ether_row(0, 0, 280)
    assert np.array_equal(step(e)[5:-5], ether_row(0, 0, 280, t=1)[5:-5])
    # 3. every Martinez period holds, and a wrong period fails
    init_martinez()
    base, _, _ = _martinez_base(MARTINEZ["A"][0])
    assert not verify_period(base, 3, 4)
    assert not verify_period(base, 4, 2)
    print("selftest ok:", {n: (g.P, g.D, g.w) for n, g in LIB.items()})


if __name__ == "__main__":
    selftest()


# ---------------------------------------------------------------- harvesting

def extract_base(row, lo, hi, margin_tiles=4):
    """Cut a base row (left ether phase 0 at x = 0) around cells [lo, hi)
    of a row taken as time 0 (a row at time T is fine: phases are read
    from the row itself)."""
    ph = window_phase(row)
    # left phase: the window ending just before lo
    xl = lo - T14 - 2
    cl = ph[xl]
    assert cl >= 0, "no ether left of the object"
    xs = lo - margin_tiles * T14
    while (xs + cl) % T14:
        xs -= 1
    xr = hi + margin_tiles * T14
    return row[xs:xr].copy()


def find_period(base, maxP=200):
    """Smallest (P, D) with D + 4P = 0 mod 14, |D| <= P, that holds."""
    for P in range(1, maxP + 1):
        for D in range(-P, P + 1):
            if (D + 4 * P) % T14:
                continue
            if verify_period(base, P, D):
                return P, D
    return None


def harvest(name, row, T, which=0):
    """Register the `which`-th unknown defect of an evolved row as a new
    glider `name` (period found by search). Returns the Glider."""
    if which == "all":
        cut = T + 16
        ds = defects(row[cut:len(row) - cut])
        lo = min(d["lo"] for d in ds) + cut
        hi = max(d["hi"] for d in ds) + cut
    else:
        unk = [r for r in identify(row, T=T) if r[0] == "?"]
        k = unk[which]
        d = [d for d in defects(row) if d["key"] == k[3]][0]
        lo, hi = d["lo"], d["hi"]
    base = extract_base(row, lo, hi)
    per = find_period(base)
    if per is None:
        raise ValueError(f"{name}: no period <= 200")
    return register(name, base, per)


def build_right(items, c_right=0, **kw):
    """Like build, but the ether phase to the RIGHT of the last item is
    fixed (c_right), so the snapped positions of the right-hand items do not
    depend on the widths of the items to their left. Use this for a rigid
    program stream whose left part (e.g. the counter) varies."""
    c0 = (c_right - sum(LIB[n].w for n, _, _ in items)) % T14
    return build(items, c0=c0, **kw)
