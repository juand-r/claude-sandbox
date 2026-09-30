"""Shared imports for the F-lane work: architect's catalog-level crossing
functions (read-only import of round-1 code). winding3 chdirs to the
architect directory on import; we restore our cwd afterwards."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ARCH = os.path.join(HERE, "..", "..", "architect")
COLL = os.path.join(HERE, "..", "..", "collider")
sys.path.insert(0, ARCH)
sys.path.insert(0, COLL)
ROOT = os.path.join(HERE, "..", "..", "..")
sys.path.insert(0, ROOT)
_cwd = os.getcwd()
import winding3 as W3          # noqa: E402
os.chdir(_cwd)
from winding3 import cross, lateral, movers, same_traj, PF, PE  # noqa: E402,F401
from r110lib import class_key  # noqa: E402

KEY = lambda D: class_key(D, PF, PE)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def cross_chain(markers, mv):
    """markers: list of F seeds, front (rightmost) first. The mover mv
    crosses markers[0]; its Ebar-speed outputs cross markers[1] (leftmost
    trajectory first), and so on. Returns (new markers, final outputs) or
    None if any crossing is not clean (catalog-level prediction)."""
    r = cross(markers[0], mv)
    if r is None:
        return None
    new = [r[0]]
    outs = r[1]
    for m in markers[1:]:
        nxt = []
        for o in sorted(outs, key=lateral):
            rr = cross(m, o)
            if rr is None:
                return None
            m = rr[0]
            nxt += rr[1]
        new.append(m)
        outs = nxt
    return new, outs
