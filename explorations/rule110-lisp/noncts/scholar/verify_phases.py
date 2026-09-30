"""Verify Martinez's published glider-phase strings (data/listPhasesR110.txt)
by simulation.

Each line "[bits] = NAME(phase), ..." is embedded as  ether^L + bits + ether^L
on a ring (the wrap seam is far away and ignored). We then measure the
smallest spacetime period (p, d) under which the defect region is invariant,
at an early time (exactness of the phase) and a late time (stability), and
compare with Cook 2004, Fig. 5.

Run:  python verify_phases.py        (prints a table; exits 1 on any failure)
"""

import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engine import ETHER, parse, step  # noqa: E402

DATA = Path(__file__).parent / "data" / "listPhasesR110.txt"

# Cook 2004 Fig. 5: (period t, displacement x) per glider family.
COOK_PERIOD = {
    "A": (3, 2), "B": (4, -2), "B-": (12, -6), "B^": (12, -6),
    "C1": (7, 0), "C2": (7, 0), "C3": (7, 0), "D1": (10, 2), "D2": (10, 2),
    "E": (15, -4), "E-": (30, -8), "F": (36, -4), "G": (42, -14),
    "H": (92, -18), "Gun": (77, -20),
}

L = 60            # ether tiles on each side
T_LATE = 300      # late check time
MAX_P = 200


def defect_mask(h, t):
    """Cells at time t violating either ether symmetry (7,0) or (3,2)."""
    now = h[t]
    a = now != h[t - 7]
    b = now != np.roll(h[t - 3], 2)
    return a | b


def find_period(h, t0, lo, hi):
    """Smallest (p, d) with h[t0+p][lo+d:hi+d] == h[t0][lo:hi]."""
    ref = h[t0, lo:hi]
    for p in range(1, MAX_P + 1):
        if t0 + p >= len(h):
            break
        for d in range(-p, p + 1):
            if np.array_equal(h[t0 + p, lo + d:hi + d], ref):
                return p, d
    return None


def spans(mask):
    """Maximal runs of True, merged when closer than 14 cells."""
    xs = np.nonzero(mask)[0]
    if len(xs) == 0:
        return []
    out, start, prev = [], xs[0], xs[0]
    for x in xs[1:]:
        if x - prev > 14:
            out.append((start, prev + 1))
            start = x
        prev = x
    out.append((start, prev + 1))
    return out


def check(bits):
    row = parse(ETHER * L + bits + ETHER * L)
    n = len(row)
    h = np.empty((T_LATE + MAX_P + 1, n), dtype=np.uint8)
    h[0] = row
    for t in range(len(h) - 1):
        h[t + 1] = step(h[t])
    res = {}
    for label, t0 in (("early", 10), ("late", T_LATE)):
        m = defect_mask(h, t0)
        # ignore the wrap seam: keep spans away from both ends
        sp = [s for s in spans(m) if s[0] > 250 and s[1] < n - 250]
        if not sp:
            res[label] = ("no defect", None)
            continue
        lo, hi = sp[0][0] - 20, sp[-1][1] + 20
        res[label] = (len(sp), find_period(h, t0, lo, hi))
    return res


def main():
    pat = re.compile(r"^\[([01]+)\]\s*=\s*([A-Za-z]+-?\^?\d*)\(([^)]*)\)")
    rows, bad = [], 0
    for line in DATA.read_text().splitlines():
        m = pat.match(line)
        if not m:
            continue
        bits, name, phase = m.groups()
        fam = name
        if fam == "e":
            continue
        r = check(bits)
        want = COOK_PERIOD.get(fam)
        e_n, e_pd = r["early"]
        l_n, l_pd = r["late"]
        ok = (e_n == 1 and l_n == 1 and e_pd is not None and e_pd == l_pd
              and want is not None and e_pd[1] * want[0] == want[1] * e_pd[0])
        bad += not ok
        rows.append((name, phase, len(bits), e_n, e_pd, l_n, l_pd, want, ok))
    for r in rows:
        print("%-4s %-10s len=%3d early:%s %s late:%s %s cook=%s %s" % (
            r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7],
            "ok" if r[8] else "MISMATCH"))
    print(f"{len(rows)} strings, {bad} mismatches")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
