"""hrun.py - fast exact runs of long scenes with the project's 1-D HashLife.

Wraps ../../../hashlife.py (Gosper HashLife for Rule 110 embedded in ether)
for rows built by my verify toolkit (vlib.build / build_right), so a long
multi-stream or wide-gap scene can be run for 10^5..10^7 steps exactly.

Why it is exact: hashlife computes the same Rule 110 orbit as engine.step on
an infinite ether-embedded row; HashRun raises if non-ether content would
reach its root's outer quarters. Validation against the packed engine is in
test_hrun.py (cell-for-cell, with a control that must fail).

API
  h = HRun(row, origin)          # row: time-0 cells, row[i] = global x = i + origin
  h.goto(T)                      # advance to absolute time T (forward only)
  h.cells(xlo, xhi)              # true row on global [xlo, xhi) at the current time
  h.objects(xlo, xhi)            # vlib typing of that range: [(name@phase, x, w)]
Streams must be finite (cut them long enough: a stream of k packets cut at
length L is exact until its cut end could influence the region you read).
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
R3V = os.path.abspath(os.path.join(HERE, "..", "..", "round3", "verify"))
sys.path.insert(0, ROOT)
sys.path.insert(0, R3V)
import hashlife  # noqa: E402
import v3        # noqa: E402

vlib = v3.vlib


class HRun:
    def __init__(self, row, origin):
        self.origin = origin
        self.h = hashlife.HashRun(np.asarray(row, dtype=np.uint8), 0)

    @property
    def t(self):
        return self.h.t

    def goto(self, T):
        if T < self.h.t:
            raise ValueError(f"cannot go back from t={self.h.t} to {T}")
        self.h.step(T - self.h.t)

    def cells(self, xlo, xhi):
        return self.h.window(xlo - self.origin, xhi - self.origin)

    def objects(self, xlo, xhi):
        r = self.cells(xlo, xhi)
        return [(n, x, w) for n, x, w, k in vlib.identify(r, xlo)]


def stats():
    return hashlife.stats()
