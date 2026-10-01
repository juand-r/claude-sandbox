"""Run a right-moving packet (list of seeds, any A-speed objects) against
E^n built from E at e0 by (n-1) B's, in the three classes (packet shifted by
j * (1,-4)). Reports outcome and counter displacement key (disp.py).
Used for: A (DEC), SAT trains (INC), zero-test candidates."""
import sys
from disp import disp, cls
from lsl import nval, names, run, snap, state

PE = (15, -4)


def scene(packet, e0, n, m=None, bgap=40):
    """Packet seeds shifted by m*P_E (same class, arrives later), then
    E at e0, then n-1 B's behind it."""
    m = m if m is not None else 60 + 40 * n
    pl = [(nm, t0 + m * PE[0], x0 + m * PE[1]) for nm, t0, x0 in packet]
    pl.append(("E",) + tuple(e0))
    x = e0[1] + 30
    for i in range(n - 1):
        x = snap(pl, "B", 0, x)
        pl.append(("B", 0, x))
        x += bgap
    return pl, m


def act(packet, e0, n, extra=600):
    pl, m = scene(packet, e0, n)
    ok, out = run(pl, 15 * m + 60 * n + extra)
    return ok, out


def describe(packet, e0, n):
    ok, out = act(packet, e0, n)
    Es = [p for p in out if nval(p[0])]
    rest = [p[0] for p in out if not nval(p[0])]
    if ok and len(Es) == 1:
        k = nval(Es[0][0])
        d = disp(e0, k, Es[0][1:])
        return (k, d, cls(d), tuple(rest)), out
    return (None, None, None, tuple(names(out))), out


def shifted(packet, j):
    return [(nm, t0 + j, x0 - 4 * j) for nm, t0, x0 in packet]


if __name__ == "__main__":
    # A alone, three classes
    e0 = (0, 0)
    x = snap([("A", 0, -60)], "E", 0, 0)
    e0 = (0, x)
    A = [("A", 0, -60)]
    for j in range(3):
        print("A class shift", j)
        for n in range(1, 9):
            r, out = describe(shifted(A, j), e0, n)
            print("  ", n, r)
