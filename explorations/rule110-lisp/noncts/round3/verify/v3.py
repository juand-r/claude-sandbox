"""round3/verify/v3.py - shared helpers on top of my round-2 toolkit.

Imports (read-only) round2/verify/vlib.py (own row builder from Martinez
strings, own canonical-key typer, exact engine) and libgen.py (own compound
library E^2..E^15, GB1..GB8, A^2..A^4).  Nothing here uses collider/,
synth/ or a teammate's builder; xlate.py (round 2) is used only to translate
collider-convention seeds and to assert row equality with the teammate's
builder."""
import os
import sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R2V = os.path.abspath(os.path.join(HERE, "..", "..", "round2", "verify"))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, R2V)
sys.path.insert(0, ROOT)
import vlib      # noqa: E402
import libgen    # noqa: E402
import engine    # noqa: E402

libgen.load()
LIB = vlib.LIB


def base(n):
    """'E^3@7' -> 'E^3'."""
    return n.split("@")[0]


def run(items, T, right=True, c=0, pad=None):
    """Build `items` [(name, t0, x0)] left to right with my builder (anchored
    on the right ether phase if right=True so right-hand items do not move
    with the widths of left-hand ones), evolve T steps exactly, type.
    Returns (objects, row_T, origin, placed); objects = [(name@phase, x, w)]."""
    if right:
        row, org, placed = vlib.build_right(items, c_right=c, T=T, pad=pad)
    else:
        row, org, placed = vlib.build(items, c0=c, T=T, pad=pad)
    r = vlib.evolve(row, T) if T else row
    objs = [(n, x, w) for n, x, w, k in vlib.identify(r, org, T=T)]
    return objs, r, org, placed


def names(objs):
    return [base(n) for n, x, w in objs]


def selftest():
    # E^3 alone moves (15,-4): after 150 steps it is 40 cells left, same phase
    o0, *_ = run([("E^3", 0, 0)], 0)
    o1, *_ = run([("E^3", 0, 0)], 150)
    assert names(o0) == names(o1) == ["E^3"], (o0, o1)
    assert o1[0][1] == o0[0][1] - 40 and o1[0][0] == o0[0][0], (o0, o1)
    # control that can fail: after 149 steps the phase differs
    o2, *_ = run([("E^3", 0, 0)], 149)
    assert o2[0][0] != o0[0][0]
    print("v3 selftest ok")


if __name__ == "__main__":
    selftest()
