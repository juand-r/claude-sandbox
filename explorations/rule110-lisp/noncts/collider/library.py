"""Glider library: named, verified gliders and a phase-key index.

Base gliders come from the literature strings (martinez_strings.py), each
re-derived and verified here by standalone simulation (r110lib.isolate_glider).
Canonical phase 0 of a glider is the state of ether* + string + ether*
at time 0. Compound objects met during the collision search (several
gliders travelling together, e.g. A^n) are registered on the fly with
automatic names and the same verification.

Library file: gliders.json = {"gliders": [Glider.to_json(), ...]}.
"""

import json
import os

import numpy as np

from r110lib import ETHER, Glider, isolate_glider, obj_key, objects
from martinez_strings import STRINGS, EXPECTED

HERE = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.join(HERE, "gliders.json")

BASE_ORDER = ["A", "B", "Bbar", "Bhat", "C1", "C2", "C3", "D1", "D2",
              "E", "Ebar", "F", "G", "H"]


def key_of_string(s, pad_tiles=40):
    """(bits, lph, rph) of the single object in ether* + s + ether*."""
    row = np.array([int(c) for c in ETHER * pad_tiles + s + ETHER * pad_tiles],
                   np.uint8)
    objs = objects(row)
    if len(objs) != 1:
        raise ValueError(f"string gives {len(objs)} objects")
    return obj_key(row, *objs[0])


class Library:
    def __init__(self):
        self.gliders = {}      # name -> Glider
        self.index = {}        # (bits, lph, rph) -> (name, phase k)
        self.failed = set()    # keys known not to be gliders

    def add(self, g):
        if g.name in self.gliders:
            raise ValueError(f"duplicate glider name {g.name}")
        for k, (bits, l, r, _) in enumerate(g.phases):
            key = (bits, l, r)
            if key in self.index:
                raise ValueError(f"{g.name} phase {k} already known as "
                                 f"{self.index[key]}")
            self.index[key] = (g.name, k)
        self.gliders[g.name] = g

    def lookup(self, key):
        return self.index.get(key)

    def identify(self, key, auto=True):
        """-> (name, k) for an object key; registers a new compound glider
        if the key is an unknown glider and auto is set; None if the
        object is not (yet) a glider."""
        hit = self.index.get(key)
        if hit or not auto or key in self.failed:
            return hit
        try:
            g = isolate_glider(*key)
        except ValueError:
            self.failed.add(key)
            return None
        # the key may be a transient that settles into a known glider;
        # isolate_glider starts phase 0 at the first repeated state, so
        # check whether that orbit is already known
        k0 = (g.phases[0][0], g.phases[0][1], g.phases[0][2])
        if k0 in self.index:
            self.failed.add(key)       # transient: not itself periodic
            return None
        if (key[0], key[1], key[2]) not in {(p[0], p[1], p[2]) for p in g.phases}:
            self.failed.add(key)
            return None
        g.name = self._auto_name(g)
        g.note = "auto-registered compound/unnamed"
        self.add(g)
        return self.index[key]

    def parse_parts(self, g):
        """Parse compound g into base gliders whose own trajectories explain
        it at EVERY phase (chain_ok for t = 0..p-1). Sets g.parts to the
        base-glider seed events relative to g's seed event and returns a
        name such as 'B_8_B' (B, 8 ether cells, B); None if no parse
        found at phase 0 survives all phases."""
        ph0 = g.phases[0]
        for parts in parses(self, ph0[:3], g.velocity):
            evs = []
            for nm, _, k, s in parts:
                pg = self.gliders[nm]
                t0 = (-k) % pg.p
                m = (-t0 - k) // pg.p
                evs.append((nm, t0, ph0[3] + s - pg.phases[k][3] - m * pg.d))
            good = True
            for t, ph in enumerate(g.phases):
                sts = []
                for nm, t0, x0 in evs:
                    b, l, r, s = self.gliders[nm].state_at(t0, x0, t)
                    sts.append((b, l, r, s - ph[3]))
                sts.sort(key=lambda z: z[3])
                if not chain_ok(ph[:3], sts):
                    good = False
                    break
            if good:
                g.parts = evs
                return parts[0][0] + "".join(f"_{gap}_{nm}" for nm, gap, _, _
                                             in parts[1:])
        return None

    def _auto_name(self, g):
        base = self.parse_parts(g) or f"v{g.d}/{g.p}s{g.slip}w{g.width}"
        name, i = base, 1
        while name in self.gliders:
            i += 1
            name = f"{base}#{i}"
        return name

    def save(self, path=LIB_PATH):
        json.dump({"gliders": [g.to_json() for g in self.gliders.values()]},
                  open(path, "w"), indent=0)

    @classmethod
    def load(cls, path=LIB_PATH):
        lib = cls()
        for j in json.load(open(path))["gliders"]:
            lib.add(Glider.from_json(j))
        return lib


def _object_row(key, margin):
    """Row of an object with `margin` ether cells each side; column 0 of
    the object is index `margin`."""
    from r110lib import ether_cells
    bits, lph, rph = key
    n = len(bits)
    return np.concatenate([ether_cells(lph, -margin, 0),
                           np.array([int(c) for c in bits], np.uint8),
                           ether_cells(rph, n, n + margin)])


def _agreement(R, lo, hi, b, l, r, s):
    """Agreement interval [p, q) (global columns) of the glider row
    (bits b, phases l, r, start s) with R around the glider's bits, or None
    if the bits themselves disagree."""
    from r110lib import ether_cells
    bl = len(b)
    row = np.concatenate([ether_cells(l - s, lo, s),
                          np.array([int(c) for c in b], np.uint8),
                          ether_cells(r - s, s + bl, hi)])
    if len(row) != len(R):
        return None
    eq = row == R
    i0, i1 = s - lo, s + bl - lo
    if i0 < 0 or i1 > len(eq) or not eq[i0:i1].all():
        return None
    p = i0
    while p > 0 and eq[p - 1]:
        p -= 1
    q = i1
    while q < len(eq) and eq[q]:
        q += 1
    return p + lo, q + lo


def chain_ok(key, states, margin=30):
    """Do the glider states [(bits, l, r, s)] (s relative to the object's
    start, sorted by s) explain the object: object row = state_1's row left
    of cut m_1, state_2's row on [m_1, m_2), ... with strictly increasing
    cuts and every glider's bits inside its own piece?"""
    n = len(key[0])
    lo, hi = -margin, n + margin
    R = _object_row(key, margin)
    ivs = []
    for b, l, r, s in states:
        iv = _agreement(R, lo, hi, b, l, r, s)
        if iv is None:
            return False
        ivs.append(iv)
    if ivs[0][0] != lo or ivs[-1][1] != hi:
        return False
    lb = states[0][3]
    for i in range(len(states) - 1):
        s, bl = states[i][3], len(states[i][0])
        s2 = states[i + 1][3]
        if s2 < s + bl:
            return False
        m = max(ivs[i + 1][0], s + bl, lb + 1)
        if m > min(ivs[i][1], s2):
            return False
        lb = m
    return True


def parses(lib, key, velocity, margin=30, max_pops=20000):
    """Generate parses of an object into base gliders of the given
    velocity (see chain_ok), fewest parts first: lists of
    (name, gap, k, s), s relative to the object's start."""
    from r110lib import TILE
    from collections import deque
    bits, lph, rph = key
    n = len(bits)
    lo, hi = -margin, n + margin
    R = _object_row(key, margin)
    cands = []    # (s, name, blen, p, q, k)
    for name in BASE_ORDER:
        g = lib.gliders[name]
        if g.velocity != velocity:
            continue
        for kk, (b, l, r, _) in enumerate(g.phases):
            for s in range(-6, n - len(b) + 7):
                iv = _agreement(R, lo, hi, b, l, r, s)
                if iv:
                    cands.append((s, name, len(b), iv[0], iv[1], kk))
    cands.sort()
    queue = deque((c, c[0], ((c[1], 0, c[5], c[0]),))
                  for c in cands if c[3] == lo)
    pops = 0
    while queue and pops < max_pops:
        pops += 1
        c, lb, path = queue.popleft()
        s, name, bl, p, q, _ = c
        if len(path) > 1 + n // 4:
            continue
        if q == hi:
            slip = sum(lib.gliders[it[0]].slip for it in path) % TILE
            if slip == (rph - lph) % TILE:
                yield list(path)
        for c2 in cands:
            s2, n2, bl2, p2, q2, k2 = c2
            if s2 < s + bl:
                continue
            m = max(p2, s + bl, lb + 1)
            if m <= min(q, s2):
                queue.append((c2, m, path + ((n2, s2 - (s + bl), k2, s2),)))


def decompose(lib, key, velocity, margin=30):
    """First (fewest-parts) parse, or None."""
    return next(parses(lib, key, velocity, margin), None)


COOK_PACKETS = {
    "A^2": ("111", 0, 2), "A^3": ("", 6, 2), "A^4": ("1", 6, 10),
    "A^5": ("0", 3, 1), "B^2": ("0", 0, 12), "B^3": ("1011100", 6, 10),
    # extendible E: E^n = E hit by n-1 B's (single class; see rename.py)
    "E^2": ('110011100', 9, 10),
    "E^3": ('0000011011', 11, 4),
    "E^4": ('01000111001100', 0, 13),
    "E^5": ('00000110111111101011', 11, 2),
    "E^6": ('001111111010111111101011', 1, 12),
    "E^7": ('111101111111010111111101011', 6, 9),
    "E^8": ('0000010011010111001101011100', 8, 3),
    "E^9": ('11000110101110011010111001101011100', 9, 10),
}


def build_base():
    lib = Library()
    for name in BASE_ORDER:
        g = isolate_glider(*key_of_string(STRINGS[name]), name=name)
        if (g.p, g.d) != EXPECTED[name]:
            raise AssertionError(f"{name}: got {(g.p, g.d)}")
        # make phase 0 the literature state itself
        k0 = key_of_string(STRINGS[name])
        ks = [(p[0], p[1], p[2]) for p in g.phases]
        k = ks.index(k0)
        if k:
            ph = g.phases[k:] + g.phases[:k]
            off0 = ph[0][3]
            # offsets re-based; phases wrapping past the end gain -d shift
            n = len(g.phases)
            new = []
            for i, (b, l, r, o) in enumerate(ph):
                shift = g.d if i >= n - k else 0
                new.append((b, l, r, o - off0 + shift))
            g.phases = new
        g.note = "Martinez et al. arXiv:0706.3348 f1_1 string"
        lib.add(g)
    # Martinez's nA = (111110)^n: wide A-packets, named Aw<n>
    for n in range(2, 7):
        g = isolate_glider(*key_of_string("111110" * n), name=f"Aw{n}")
        g.note = f"wide A-packet: Martinez nA string (111110)^{n}"
        lib.add(g)
    # tight packets as in Cook's construction (see rename.py for the
    # evidence): object keys (bits, lph, rph) of one phase
    for name, key in COOK_PACKETS.items():
        g = isolate_glider(*key, name=name)
        g.note = "tight packet; Cook's A^4 is the ossifier packet of block B"
        lib.add(g)
    return lib


if __name__ == "__main__":
    from r110lib import verify_glider
    lib = build_base()
    for g in lib.gliders.values():
        verify_glider(g, periods=6)
        print(f"{g.name:5s} p={g.p:3d} d={g.d:4d} v={str(g.velocity):6s} "
              f"slip={g.slip:2d} width={g.width}")
    lib.save()
    print("saved", LIB_PATH)
