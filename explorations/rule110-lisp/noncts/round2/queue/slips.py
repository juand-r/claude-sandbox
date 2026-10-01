"""Measure slips (ether phase jump, right - left, mod 14) of the objects
the slip law uses, directly in running machines [sim]:
tape symbols (clean groups of C gliders), and blocks at t = 0."""
import sys
from splice import *

def groups(row, gap=60):
    cl = clusters(row)
    out = []
    for a, b in cl:
        if out and a - out[-1][1] < gap:
            out[-1][1] = b
        else:
            out.append([a, b])
    return out

def tape_symbols(tape, T0, T1, dt):
    """Clean C-only groups in the lab frame [-3000, 2000], typed by census."""
    m = Machine(tape, ["YNNNNN"], T1, left_periods=6, right_periods=3)
    r = Run(m.row, m.origin)
    seen = set()
    for t in range(T0, T1 + 1, dt):
        r.step(t - MAX_DT - r.t)
        lo, hi = m.origin - 6000, m.origin + 3000
        h = r.history(lo, hi, MAX_DT)
        cs = census(h)
        row = h[-1]
        for a, b in groups(row):
            inside = [k for x, y, k in cs if a <= x < b]
            if inside and all(k == "C" for k in inside):
                w = rc.width(row, a, b)
                key = (len(inside), int(w))
                if key not in seen:
                    seen.add(key)
                    print(f"{tape} t={t} x={a + lo - m.origin}: {len(inside)} C's, slip {w}")

if __name__ == "__main__":
    for tape in ("YYYY", "NNNN"):
        tape_symbols(tape, 3000, 60000, 1500)
