"""Glider library and row composition for synthesis.

Glider data: ../collider/gliders.json (collider's verified library; format
in ../collider/r110lib.py). A phase record (bits, lph, rph, off): the
glider seeded at (t0, x0) is, at time t with k = (t - t0) mod p and
q = (t - t0) div p, the string `bits` starting at column
s = x0 + off_k + q d; cells y < s read ETHER[(lph + y - s) % 14], cells
y >= s + len(bits) read ETHER[(rph + y - s) % 14].

My phase convention (r110sat): cell(t, x) = ETHER[(x + 4t + p) % 14]. So an
ether region whose collider absolute phase at time t is c has p = c - 4t.
"""

import json
import os

import numpy as np

from r110sat import TILE, ether_bit

HERE = os.path.dirname(os.path.abspath(__file__))
GLIDER_FILE = os.path.join(HERE, "..", "collider", "gliders.json")


class Glider:
    def __init__(self, j):
        self.name, self.p, self.d = j["name"], j["p"], j["d"]
        self.phases = [tuple(ph) for ph in j["phases"]]
        b, l, r, _ = self.phases[0]
        self.slip = (r - l) % TILE

    def state(self, t0, x0, t):
        """(bits, lph, rph, s) at time t for seed event (t0, x0)."""
        q, k = divmod(t - t0, self.p)
        bits, lph, rph, off = self.phases[k]
        return bits, lph, rph, x0 + off + q * self.d

    def __repr__(self):
        return f"Glider({self.name}, p={self.p}, d={self.d})"


def load_gliders(path=GLIDER_FILE):
    with open(path) as fh:
        data = json.load(fh)
    return {j["name"]: Glider(j) for j in data["gliders"]}


def place_after(g, t, left_p, x_min, k=0):
    """Seed event (t0, x0) placing glider g (in time-phase k at time t) so
    that its left ether has my-phase `left_p` and its bits start at the
    smallest column s >= x_min compatible with that phase."""
    bits, lph, rph, off = g.phases[k]
    # need (lph - s) - 4t == left_p (mod 14)  ->  s == lph - 4t - left_p
    s = x_min + ((lph - 4 * t - left_p - x_min) % TILE)
    t0 = t - k
    x0 = s - off
    return (t0, x0)


def right_phase_of(state, t):
    """My-phase of the ether right of an object state at time t."""
    bits, lph, rph, s = state
    return (rph - s - 4 * t) % TILE


def left_phase_of(state, t):
    bits, lph, rph, s = state
    return (lph - s - 4 * t) % TILE


def compose(states, t, lo, hi, left_p=None):
    """Cells [lo, hi) at time t for a list of object states (bits, lph,
    rph, s), with ether in between (phases must be consistent; checked).
    `bits` may be None for a free placeholder of length rph... no: free
    spans are handled by the caller. Returns (cells, p_left, p_right)."""
    st = sorted(states, key=lambda q: q[3])
    if not st:
        if left_p is None:
            raise ValueError("empty composition needs left_p")
        return np.array([ether_bit(left_p, t, x) for x in range(lo, hi)],
                        np.uint8), left_p, left_p
    for a, b in zip(st, st[1:]):
        if a[3] + len(a[0]) > b[3]:
            raise ValueError(f"objects overlap at {b[3]}")
        if right_phase_of(a, t) != left_phase_of(b, t):
            raise ValueError("inconsistent ether phases between objects")
    pl = left_phase_of(st[0], t)
    pr = right_phase_of(st[-1], t)
    if left_p is not None and left_p != pl:
        raise ValueError("left phase mismatch")
    cells = np.zeros(hi - lo, np.uint8)
    cur = pl
    idx = 0
    x = lo
    for bits, lph, rph, s in st:
        if s < lo or s + len(bits) > hi:
            raise ValueError("object outside [lo, hi)")
        while x < s:
            cells[x - lo] = ether_bit(cur, t, x)
            x += 1
        for c in bits:
            cells[x - lo] = int(c)
            x += 1
        cur = (rph - s - 4 * t) % TILE
    while x < hi:
        cells[x - lo] = ether_bit(cur, t, x)
        x += 1
    return cells, pl, pr
