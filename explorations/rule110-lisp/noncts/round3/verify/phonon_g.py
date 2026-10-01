"""(P1) at R1's outer face: does a phonon arriving at the back of E^15
together with a G-family packet (GB3/GB4/GB5) change that reaction?
The packet is placed at x (gap ~ x - back), the scene is evolved to time
t_inj, a phonon is injected at an interior site (single-cell flip matching
the ring defect's background window), and the run continues; outcomes are
compared with the run without injection (exact engine, my typer)."""
import sys
from collections import Counter
import numpy as np
import v3, vlib, engine
import rod_defect as RD

PROBE = sys.argv[1] if len(sys.argv) > 1 else "GB4"
T_LO, T_HI = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (900, 1200)
T = 4000


def outcome(t0, x, t_inj, site):
    items = [("E^15", 0, 0), (PROBE, t0, x)]
    row, org, placed = vlib.build_right(items, c_right=0, T=T)
    w = engine.pack(row)
    if t_inj is not None:
        r = engine.unpack(engine.step_packed_n(w, t_inj), len(row))
        hits = [i for i in range(RD.H, len(r) - RD.H - 1)
                if np.array_equal(r[i - RD.H:i + RD.H + 1], RD.pat_bg)]
        if len(hits) <= site:
            return None
        r = r.copy()
        r[hits[site]] ^= 1
        r = engine.unpack(engine.step_packed_n(engine.pack(r), T - t_inj), len(row))
    else:
        r = engine.unpack(engine.step_packed_n(w, T), len(row))
    return " + ".join(v3.base(n) for n, xx, w_, k in vlib.identify(r, org, T=T))


if __name__ == "__main__":
    diffs = Counter()
    for t0 in range(0, 42, 3):
        x = 200
        base = outcome(t0, x, None, 0)
        for t_inj in range(T_LO, T_HI, 1):          # 1-step resolution
            for site in (0,):
                o = outcome(t0, x, t_inj, site)
                if o is not None and o != base:
                    diffs[(base, o)] += 1
                    print(f"t0={t0} t_inj={t_inj} site={site}: without {base} | with {o}", flush=True)
    print("distinct changes:", len(diffs), dict(diffs))
