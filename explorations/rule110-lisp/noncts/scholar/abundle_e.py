"""Right-moving A bundles (A^2..A^5, collider's tight packets) against E^n
(collider's E, E^2, E^3), all 3 classes each: does any bundle INCREMENT an
E counter from the left? Placement by collider's canonical_reps (library
read-only); evolution by engine.step; typing by my r110check.objects."""
import os, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "collider"))
cwd = os.getcwd(); os.chdir(HERE.parent / "collider")
from library import Library
from collide import canonical_reps
from r110lib import build_row
LIB = Library.load(); os.chdir(cwd)
sys.path.insert(0, str(HERE))
import r110check as r
from engine import step

T = 1500


def evaluate(pl):
    G = LIB.gliders
    states = [G[n].state_at(t0, x0, 0) for n, t0, x0 in pl]
    row, xo = build_row(states, pad=T + 200)
    cur = row
    keep = []
    for t in range(T):
        cur = step(cur)
        if t >= T - 160:
            keep.append(cur)
    h = np.array(keep)
    return sorted(o[2] for o in r.objects(h, len(h) - 1, 150, len(row) - 150))


for X in ["A", "A^2", "A^3", "A^4", "A^5"]:
    for Y in ["E", "E^2", "E^3"]:
        reps = canonical_reps(LIB, X, Y)
        outs = []
        for k, rep in enumerate(reps):
            outs.append(evaluate([(X, 0, 0), (Y, rep[0], rep[1])]))
        print(f"{X} + {Y}:", outs, flush=True)
