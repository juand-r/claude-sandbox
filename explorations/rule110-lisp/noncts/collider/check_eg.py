"""Independent-style check of E^n + G (collider claims: -> E^(n-1) + A^3).

Builds E^n from Martinez's E string hit by n-1 B's (single class, so any
B timing), then a Martinez G from the right in each of its 3 classes, runs
../../engine.py step, and reports every remaining object with its measured
velocity (displacement of its left edge over 420 generations, 420 being a
multiple of every period involved). No library lookup is used for the
final typing."""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import engine  # noqa: E402

from collide import canonical_reps  # noqa: E402
from predict import LIB, predict  # noqa: E402
from r110lib import build_row, objects  # noqa: E402


def run(n, gclass, T=3000, dT=420):
    e, nm = (0, 0), "E"
    scene = [("E", 0, 0)]
    for k in range(n - 1):
        rep = canonical_reps(LIB, nm, "B")[0]
        rep = (rep[0] + 15 * 8 * (k + 1), rep[1] - 4 * 8 * (k + 1))  # later
        scene.append(("B", e[0] + rep[0], e[1] + rep[1]))
        _, pr = predict(nm, "B", rep, eX=e)
        nm, e = pr[0][0], pr[0][1:]
    rep = canonical_reps(LIB, nm, "G")[gclass]
    rep = (rep[0] + 15 * 40 * n, rep[1] - 4 * 40 * n)   # G far right
    scene.append(("G", e[0] + rep[0], e[1] + rep[1]))
    sts = [LIB.gliders[a].state_at(t, x, 0) for a, t, x in scene]
    row, x0 = build_row(sts, pad=T + dT + 200)
    for _ in range(T):
        row = engine.step(row)
    o1 = objects(row)
    for _ in range(dT):
        row = engine.step(row)
    o2 = objects(row)
    if len(o1) != len(o2):
        return "object count changed", len(o1), len(o2)
    return [(a + x0, b - a, str(Fraction(a2 - a, dT)))
            for (a, b, _, _), (a2, _, _, _) in zip(o1, o2)]


if __name__ == "__main__":
    for n in (2, 3, 4):
        for c in range(3):
            print(f"E^{n} + G class {c}: (start, width, velocity) =", run(n, c))
