"""Rod (E^n) backgrounds in exact Rule 110, for perturbation searches.

Conventions (synth/r110sat): ether phase p means cell(t,x) = ETHER[(x+4t+p)%14].
build_rod(n) simulates E + (n-1) B's (synth/en.py recipe) until settled and
returns a settled row with the rod, plus left/right ether phases.
"""
import os
import sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
SYNTH = os.path.abspath(os.path.join(HERE, "..", "..", "synth"))
sys.path.insert(0, SYNTH)
import numpy as np  # noqa: E402
from r110sat import TILE, ether_bit, simulate  # noqa: E402
from lib import load_gliders, compose  # noqa: E402

GL = load_gliders()
PE = (15, -4)


def ether_phase_at(row, t, x0, lo, hi):
    """phase p with row[lo..hi) == ether(p) at time t (x0 = column of row[0])."""
    for p in range(TILE):
        if all(row[x - x0] == ether_bit(p, t, x) for x in range(lo, hi)):
            return p
    return None


def nonether_extent(row, t, x0, pl, pr):
    """[a, b): leftmost cell differing from left ether pl, rightmost+1
    differing from right ether pr."""
    n = len(row)
    a = next(i for i in range(n) if row[i] != ether_bit(pl, t, x0 + i))
    b = next(i for i in range(n - 1, -1, -1) if row[i] != ether_bit(pr, t, x0 + i)) + 1
    return x0 + a, x0 + b


def build_rod(n, settle=None):
    """Row (time 0 after settling) with E^n near x = 0.
    Returns dict(row, x0, pl, pr, a, b) where [a, b) is the rod extent."""
    E, B = GL["E"], GL["B"]
    sts = [E.state(0, 0, 0)]
    x = 40
    for i in range(n - 1):
        rp = (sts[-1][2] - sts[-1][3]) % TILE
        s = x
        while True:
            st = B.state(0, s, 0)
            if (st[1] - st[3]) % TILE == rp:
                break
            s += 1
        sts.append(B.state(0, s, 0))
        x = s + 30
    T = settle or (200 + 150 * n)
    T -= T % 15                      # whole rod periods
    lo, hi = -2 * T - 200, x + 2 * T + 200
    cells, pl, pr = compose(sts, 0, lo, hi)
    h = simulate(cells, T)
    row = h[T]
    # ether phases far left / right at time T
    pL = ether_phase_at(row, T, lo, lo + T + 50, lo + T + 78)
    pR = ether_phase_at(row, T, lo, hi - T - 78, hi - T - 50)
    a, b = nonether_extent(row[T + 60: len(row) - T - 60], T, lo + T + 60, pL, pR)
    # re-express as a time-0 row: shift x so the rod starts at 0. A row at
    # time T with phase p equals a row at time 0 with phase p + 4T.
    pl0, pr0 = (pL + 4 * T) % TILE, (pR + 4 * T) % TILE
    seg = row[a - lo: b - lo]
    # translate by -a: phase p at x  ->  phase p + a at x - a
    pl0, pr0 = (pl0 + a) % TILE, (pr0 + a) % TILE
    return dict(seg=seg, pl=pl0, pr=pr0, W=len(seg))


def embed(parts, lo, hi):
    """parts: list of (x, seg, pl, pr) sorted by x; returns row on [lo,hi)
    at time 0, checking phase consistency between parts."""
    row = np.zeros(hi - lo, np.uint8)
    cur = parts[0][2]
    x = lo
    for (xs, seg, pl, pr) in parts:
        if pl != cur:
            raise ValueError(f"phase mismatch at {xs}: {pl} vs {cur}")
        while x < xs:
            row[x - lo] = ether_bit(cur, 0, x)
            x += 1
        row[xs - lo: xs - lo + len(seg)] = seg
        x = xs + len(seg)
        cur = pr
    while x < hi:
        row[x - lo] = ether_bit(cur, 0, x)
        x += 1
    return row


def rod_piece(r, x):
    """rod r placed with its first cell at column x: (x, seg, pl, pr) with
    phases expressed in global columns."""
    return (x, r["seg"], (r["pl"] - x) % TILE, (r["pr"] - x) % TILE)


if __name__ == "__main__":
    for n in range(1, 13):
        r = build_rod(n)
        print(n, r["W"], r["pl"], r["pr"], (r["pr"] - r["pl"]) % 14, "".join(map(str, r["seg"])))
