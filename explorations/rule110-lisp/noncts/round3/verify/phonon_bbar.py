"""Does the +2/5 phonon change a reaction at the rod's BACK face?
Rod E^15 (my library) with a phonon injected at an interior site; a Bbar
(or B) from the right placed so that it reaches the back face around the
phonon's arrival.  For each Bbar placement, compare the outcome with and
without the phonon (exact engine, my typer).  A difference in a CLEAN
outcome would make the phonon a signal that crosses the rod."""
import sys
from collections import Counter
import numpy as np
import v3, vlib, engine
import rod_defect as RD

PROBE = sys.argv[1] if len(sys.argv) > 1 else "Bbar"
T = 3000


def scene(t0, x, site, with_phonon):
    items = [("E^15", 0, 0), (PROBE, t0, x)]
    row, org, placed = vlib.build_right(items, c_right=0, T=T)
    if with_phonon:
        hits = [i for i in range(RD.H, len(row) - RD.H - 1)
                if np.array_equal(row[i - RD.H:i + RD.H + 1], RD.pat_bg)]
        i = hits[site]
        row = row.copy()
        row[i] ^= 1
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return " + ".join(v3.base(n) for n, xx, w, k in vlib.identify(r, org, T=T))


if __name__ == "__main__":
    diff = Counter()
    P = vlib.LIB[PROBE].P
    for site in range(3):
        for t0 in range(P):
            for x in range(60, 160, 7):
                a = scene(t0, x, site, False)
                b = scene(t0, x, site, True)
                if a != b:
                    diff[(a, b)] += 1
                    print(f"site {site} t0={t0} x={x}: without {a} | with phonon {b}", flush=True)
    print("distinct changes:", len(diff))
