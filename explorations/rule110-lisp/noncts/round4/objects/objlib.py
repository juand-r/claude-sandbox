"""Scene building for objects/ (own code; collider conventions, read-only data).

Convention (collider/r110lib.py): ether ETHER = "11111000100110"; a region is
ether of absolute phase c if cell y reads ETHER[(c + y) % 14]. A glider phase
record is (bits, lph, rph, off): with bits[0] at column s, cells left read
ETHER[(lph + y - s) % 14] (absolute phase lph - s), cells right read
ETHER[(rph + y - s) % 14] (absolute phase rph - s).

Simulation: `evolve(row, T)` is exact on a finite row whose edges shrink by
one cell per step (no wrap); `history_window` keeps all rows. Callers pad.
"""
import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LIBFILE = os.path.join(HERE, "..", "..", "collider", "gliders.json")
ETHER = "11111000100110"
EB = np.array([int(c) for c in ETHER], np.uint8)
EBG = "1101011100"         # E^n interior background tile (period 10, 5 steps)

_LIB = None


def lib():
    global _LIB
    if _LIB is None:
        _LIB = {g["name"]: g for g in json.load(open(LIBFILE))["gliders"]}
    return _LIB


def ether(c, lo, hi):
    return EB[(c + np.arange(lo, hi)) % 14]


def step(c):
    return ((c[1:-1] | c[2:]) & (1 - (c[:-2] & c[1:-1] & c[2:]))).astype(np.uint8)


def evolve(row, T):
    """row covering [x0, x0+W) -> row at time T covering [x0+T, x0+W-T)."""
    r = np.asarray(row, np.uint8)
    for _ in range(T):
        r = step(r)
    return r


def history(row, T):
    out = [np.asarray(row, np.uint8)]
    for _ in range(T):
        out.append(step(out[-1]))
    return out


class Row:
    """Left-to-right builder. Positions are absolute columns."""

    def __init__(self, c_left=0, x_start=0):
        self.c = c_left          # absolute ether phase of the current right end
        self.x = x_start         # first free column
        self.parts = []          # (s, bits)
        self.objs = []           # (label, s, len)

    def put(self, bits, lph, rph, min_gap=0, label="?", exact_s=None):
        """Place object with bits[0] at the first column s >= x + min_gap with
        (lph - s) % 14 == c. Returns s."""
        if exact_s is not None:
            s = exact_s
            assert (lph - s) % 14 == self.c % 14, "phase mismatch at exact_s"
        else:
            s = self.x + min_gap
            while (lph - s) % 14 != self.c % 14:
                s += 1
        self.parts.append((s, np.array([int(ch) for ch in bits], np.uint8)))
        self.objs.append((label, s, len(bits)))
        self.x = s + len(bits)
        self.c = (rph - s) % 14
        return s

    def glider(self, name, k=0, min_gap=0, exact_s=None):
        b, lph, rph, off = lib()[name]["phases"][k]
        return self.put(b, lph, rph, min_gap, label=f"{name}#{k}", exact_s=exact_s)

    def render(self, c_left, pad_left, pad_right):
        """cells for [x_lo, x_hi); returns (row, x_lo)."""
        if not self.parts:
            raise ValueError("empty")
        x_lo = self.parts[0][0] - pad_left
        x_hi = self.x + pad_right
        row = np.zeros(x_hi - x_lo, np.uint8)
        # fill ether piecewise: before first part with c_left, between parts
        # with the phase after each part
        c = c_left
        cur = x_lo
        for (s, bits) in self.parts:
            row[cur - x_lo:s - x_lo] = ether(c, cur, s)
            row[s - x_lo:s - x_lo + len(bits)] = bits
            cur = s + len(bits)
            c = None
            # phase after this part is recomputed below
        # recompute phases: walk again
        c = c_left
        cur = x_lo
        for (s, bits), (label, _, _) in zip(self.parts, self.objs):
            cur = s + len(bits)
        row[cur - x_lo:] = ether(self.c, cur, x_hi)
        return row, x_lo


def build(items, c_left=0, pad=600):
    """items: list of (kind, args...):
      ('g', name, k, min_gap)   library glider phase k
      ('raw', bits, lph, rph, min_gap, label)
    Returns (row, x_lo, objs, c_right)."""
    R = Row(c_left)
    phases = [c_left]
    for it in items:
        if it[0] == "g":
            _, name, k, gap = it
            R.glider(name, k, gap)
        else:
            _, bits, lph, rph, gap, label = it
            R.put(bits, lph, rph, gap, label)
        phases.append(R.c)
    x_lo = R.parts[0][0] - pad
    x_hi = R.x + pad
    row = np.zeros(x_hi - x_lo, np.uint8)
    cur = x_lo
    for (s, bits), c in zip(R.parts, phases[:-1]):
        row[cur - x_lo:s - x_lo] = ether(c, cur, s)
        row[s - x_lo:s - x_lo + len(bits)] = bits
        cur = s + len(bits)
    row[cur - x_lo:] = ether(R.c, cur, x_hi)
    return row, x_lo, R.objs, R.c


def en_bits(n, k=0):
    """E^n phase-k record for any n >= 2 by splicing interior periods into a
    library E^m (m in 2..9 with m = n mod 3 class). Returns (bits, lph, rph).
    Each 10-cell interior period adds 3 units (verified by caller)."""
    L = lib()
    if f"E^{n}" in L:
        b, lph, rph, off = L[f"E^{n}"]["phases"][k]
        return b, lph, rph
    base = None
    for m in range(9, 1, -1):
        if (n - m) % 3 == 0 and f"E^{m}" in L:
            base = m
            break
    b, lph, rph, off = L[f"E^{base}"]["phases"][k]
    j = (n - base) // 3
    # find a 10-periodic stretch of length >= 20 inside b
    for i in range(len(b) - 20 + 1):
        if b[i:i + 10] == b[i + 10:i + 20]:
            per = b[i:i + 10]
            return b[:i] + per * j + b[i:], lph, (rph - 10 * j) % 14
    raise ValueError(f"no interior period in E^{base} phase {k}")


_V3 = None


def typer():
    """round3/verify/v3 (imports round2 vlib + libgen), read-only."""
    global _V3
    if _V3 is None:
        import sys
        p = os.path.abspath(os.path.join(HERE, "..", "..", "round3", "verify"))
        if p not in sys.path:
            sys.path.insert(0, p)
        cwd = os.getcwd()
        os.chdir(p)
        try:
            import v3
        finally:
            os.chdir(cwd)
        _V3 = v3
    return _V3


def types(row, x_lo):
    """[(name, x, w)] for a row whose cell 0 is column x_lo."""
    v3 = typer()
    return [(n.split("@")[0], x, w) for n, x, w, k in v3.vlib.identify(row, x_lo)]


def types_rods(row, x_lo, nmax=200):
    """types() plus E^n recognition for long rods ('?' blocks): an E^n is
    reported if some phase-k E^n string occurs in the row with correct
    ether on both sides (8 cells checked each side)."""
    base = types(row, x_lo)
    s = "".join(map(str, row))
    out = []
    for name, x, w in base:
        if name != "?":
            out.append((name, x, w))
            continue
        found = None
        i0 = x - x_lo
        for n in range(16, nmax + 1):
            for k in range(15):
                b, lph, rph = en_bits(n, k)
                j = s.find(b, max(0, i0 - 20), i0 + len(b) + 20)
                if j < 0 or j - 8 < 0 or j + len(b) + 8 > len(s):
                    continue
                sc = x_lo + j
                okL = all(row[j - q] == EB[(lph - sc + (sc - q)) % 14] for q in range(1, 9))
                okR = all(row[j + len(b) + q] == EB[(rph - sc + sc + len(b) + q) % 14] for q in range(8))
                if okL and okR:
                    found = (f"E^{n}", x_lo + j, k)
                    break
            if found:
                break
        out.append((found[0], found[1], w) if found else ("?", x, w))
    return out


_ETH_WIN = {tuple(np.roll(EB, -c)[:14]) for c in range(14)}


def ether_mask(row):
    """True for cells covered by some 14-cell window equal to an ether phase."""
    m = np.zeros(len(row), bool)
    for i in range(len(row) - 13):
        if tuple(row[i:i + 14]) in _ETH_WIN:
            m[i:i + 14] = True
    return m


def show(row, lo=0, hi=None):
    hi = len(row) if hi is None else hi
    m = ether_mask(row)
    return "".join("." if m[i] else ("1" if row[i] else "0") for i in range(lo, hi))
