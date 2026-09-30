"""Direct check of the F read-and-reset gadget (relay.py finding 1).
Scenario idle: C2 at (0,0), F at (0,47).  Scenario set: the same plus an
A placed so that A + C2 happens first (A at C2 - (0,53), the A+C2#0
geometry). Both are simulated with ../../engine.py's scalar step and the
final rows are compared against the predicted products."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import numpy as np
import engine
from library import Library
from r110lib import build_row, ether_cells, TILE, objects, obj_key

lib = Library.load()
T = 900


def run(placements):
    sts = [lib.gliders[n].state_at(t, x, 0) for n, t, x in placements]
    row, x0 = build_row(sts, pad=T + 60)
    for _ in range(T):
        row = engine.step(row)
    found = []
    for a, b, cl, cr in objects(row):
        name, k = lib.identify(obj_key(row, a, b, cl, cr))
        g = lib.gliders[name]
        s = x0 + a
        t0 = (T - k) % g.p
        m = (T - t0 - k) // g.p
        found.append((name, t0, s - g.phases[k][3] - m * g.d))
    return found


idle = run([("C2", 0, 0), ("F", 0, 47)])
set_ = run([("A", 0, -53), ("C2", 0, 0), ("F", 0, 47)])
print("idle:", idle)
print("set: ", set_)
assert ("C2", 4, 13) in idle and ("C2", 4, 13) in set_
assert [p[0] for p in idle] == ["F", "C2"] or sorted(p[0] for p in idle) == ["C2", "F"]
assert sorted(p[0] for p in set_) == ["C2", "Ebar"]
print("F read-and-reset confirmed")
