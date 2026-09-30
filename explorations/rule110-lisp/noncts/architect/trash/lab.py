"""Architect's collision lab (scratch; the team catalog is collider's).

Glider: a standalone ether row containing one isolated periodic defect.
We keep the row itself (width W, multiple of 14), the defect's period
(dt, dx), and can evolve it. Collisions are made by splicing two such
rows at a cut in clean ether where the phases agree.
"""
import sys
import numpy as np
sys.path.insert(0, "../..")
from engine import ETHER, parse, step, ether_tape, pack, unpack, step_packed
from census import clusters, ether_phase
from zoo import period_of, evolve, discover

TILE = 14
EB = parse(ETHER)


def run_packed(row, n):
    w = pack(row)
    for _ in range(n):
        w = step_packed(w)
    return unpack(w, len(row))


class Glider:
    def __init__(self, row, period, name="?"):
        self.row = row            # standalone row at its canonical phase 0
        self.dt, self.dx = period
        self.name = name

    def at(self, k):
        """Standalone row after k steps."""
        r = self.row
        for _ in range(k):
            r = step(r)
        return r

    def span(self, row=None):
        row = self.row if row is None else row
        cl = clusters(row)
        assert len(cl) == 1, cl
        return cl[0]


def shape_key(row):
    (a, b), = clusters(row)
    return row[a - 1:b + 1].tobytes(), b - a


def canonical_zoo(trials=2000, seed=1, width=14 * 30):
    """-> list of Glider, one per distinct orbit shape."""
    found = discover(trials=trials, seed=seed)
    out = []
    seen = set()
    for p, items in found.items():
        for (_, a, b, bits, lph, rph) in items:
            # rebuild a standalone row: left ether phase lph, bits, right rph
            n = len(bits)
            c = width // 2
            row = np.empty(width, np.uint8)
            # absolute positions: in original row, bits started at a; the
            # left phase lph is absolute w.r.t. original indices, so shift
            sh = c - a
            y = np.arange(width)
            row[:c] = EB[(lph + (y[:c] - sh)) % TILE]
            row[c:c + n] = bits
            row[c + n:] = EB[(rph + (y[c + n:] - sh)) % TILE]
            # check periodicity standalone
            H = evolve(row, 2 * p[0] + 2)
            cl = clusters(H[-1])
            if len(cl) != 1:
                continue
            q = period_of(H, *cl[0])
            if q != p:
                continue
            # orbit key: min over phases of shape bytes
            keys = []
            r = row
            for _ in range(p[0]):
                if len(clusters(r)) != 1:
                    keys = None
                    break
                keys.append(shape_key(r))
                r = step(r)
            if keys is None:
                continue
            k = (p, min(keys))
            if k in seen:
                continue
            seen.add(k)
            out.append(Glider(row, p))
    return out


def splice(left_row, right_row, cut_left, shift):
    """Row = left_row[:cut_left] + right_row shifted: right_row cell j
    lands at j + shift. Checks phase agreement at the cut."""
    W = len(left_row)
    out = left_row.copy()
    idx = np.arange(cut_left, W)
    src = idx - shift
    if src.min() < 0 or src.max() >= len(right_row):
        raise ValueError("shift out of range")
    out[cut_left:] = right_row[src]
    # verify ether continuity around cut
    ph = ether_phase(out[cut_left - 14:cut_left + 14])
    if (ph < 0).any() or len(set(ph.tolist())) != 1:
        raise ValueError("phase mismatch at cut")
    return out


NAMES = {(3, 2): "A", (4, -2): "B", (7, 0): "C", (10, 2): "D",
         (12, -6): "Bbar", (15, -4): "E", (30, -8): "Ebar",
         (36, -4): "F", (42, -14): "G", (92, -18): "H", (77, -20): "gun"}


def census_typed(H, margin=4):
    """-> list of (a, b, name) for last row of H using minimal periods."""
    out = []
    for a, b in clusters(H[-1]):
        p = period_of(H, a, b, margin=margin, max_dt=min(100, len(H) - 1))
        out.append((a, b, NAMES.get(p, str(p)) if p else "?"))
    return out
