"""Local scenes cut from a full Cook machine (exact Rule 110).

A scene = the lab row of a Machine at time t_in restricted to an Ebar-frame
window [lo, hi) (global columns) plus margins M on both sides. It is evolved
with the compiled cyclic engine; cells within M - T of the margins' inner
edges cannot be influenced by the cut (light cone, speed 1), so for
T <= M the Ebar-frame window [lo, hi) at t_in + T is exact.
"""
import numpy as np
from q import *
from casim import EBAR_VELOCITY
from engine import pack, unpack, step_packed_n

def shift(origin, t):
    return origin + int(round(EBAR_VELOCITY * t))

class Scene:
    def __init__(self, machine, row, t_in, lo, hi, M):
        r = Run(row, machine.origin)
        r.step(t_in)
        self.origin, self.t_in, self.lo, self.hi, self.M = machine.origin, t_in, lo, hi, M
        sh = shift(self.origin, t_in)
        self.a = lo + sh - M                       # array coord of seg[0]
        self.seg = r.window(self.a, hi + sh + M).copy()

    def ebar_to_seg(self, x, t=None):
        """Ebar-frame global column x at time t (default t_in) -> seg index."""
        t = self.t_in if t is None else t
        return x + shift(self.origin, t) - self.a

    def run(self, seg, T, lo=None, hi=None):
        """Evolve seg T steps; return Ebar-frame window [lo, hi) at t_in+T."""
        assert T <= self.M
        lo = self.lo if lo is None else lo
        hi = self.hi if hi is None else hi
        w = pack(seg)
        w = step_packed_n(w, T)
        cells = unpack(w, len(seg))
        i = self.ebar_to_seg(lo, self.t_in + T)
        return cells[i:i + (hi - lo)]
