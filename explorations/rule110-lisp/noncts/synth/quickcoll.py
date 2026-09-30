"""Quick look: single glider X hitting a stationary Ci (one collision class
each for A/B vs C). Prints census of the result. Diagnostic only."""
import sys
import numpy as np
from lib import load_gliders, place_after, compose, right_phase_of, left_phase_of
from r110sat import simulate
from census import census

G = load_gliders()


def collide(xn, yn, T=400, gap=30, k=0):
    X, Y = G[xn], G[yn]
    # Y at x ~ 400, time 0, phase 0 left ether
    sy = Y.state(0, 2000, 0)
    if X.d > 0:   # X comes from the left
        pl = (left_phase_of(sy, 0) - X.slip) % 14
        t0, x0 = place_after(X, 0, pl, 2000 - gap - 40, k)
        sx = X.state(t0, x0, 0)
        if sx[3] + len(sx[0]) > sy[3] - 5:
            raise ValueError
        states = [sx, sy]
        # need right phase of X == left phase of Y
        assert right_phase_of(sx, 0) == left_phase_of(sy, 0)
    else:
        pl = right_phase_of(sy, 0)
        t0, x0 = place_after(X, 0, pl, sy[3] + len(sy[0]) + gap, k)
        states = [sy, X.state(t0, x0, 0)]
    cells, _, _ = compose(states, 0, 0, 4004)
    h = simulate(cells, T + 40)
    return census(h[-31:, 1400:2600])


if __name__ == "__main__":
    for xn in sys.argv[1].split(","):
        for yn in sys.argv[2].split(","):
            for k in range(G[xn].p):
                try:
                    c = collide(xn, yn, k=k)
                except (ValueError, AssertionError):
                    continue
                print(xn, yn, k, [(a + 1400 - 2000, kind) for a, b, kind in c])
