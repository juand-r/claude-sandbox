"""Velocities of localized defects inside the E-infinity background.
Like ebg_search.py, but instead of global periodicity (which fails when
several defects of different speeds coexist) each surviving localized
deviation (span <= SPAN) is tracked for DT steps; its velocity is the
displacement of its circular centre / DT.  Records distinct (rounded)
velocities with an example.  Usage: python3 ebg_vel.py TRIALS SEED"""
import sys
from collections import defaultdict
import numpy as np
import ebg_search as S
import engine
import ebg_search as S

SPAN, DT = int(sys.argv[4]) if len(sys.argv) > 4 else 40, 200
KMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 12


def centre(mask):
    loc = S.localized(mask)
    if loc is None:
        return None
    start, span = loc
    return (start + span / 2.0) % S.W, span


if __name__ == "__main__":
    trials, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    vel = defaultdict(list)
    for tr in range(trials):
        ring = S.VAR[0].copy()
        k = int(rng.integers(1, KMAX + 1))
        x = int(rng.integers(0, S.W - k))
        ring[x:x + k] = rng.integers(0, 2, k, dtype=np.uint8)
        r = engine.unpack(engine.step_packed_n(engine.pack(ring), S.T0), S.W)
        c0 = centre(S.deviation(r))
        if c0 is None or c0[1] > SPAN:
            continue
        r2 = engine.unpack(engine.step_packed_n(engine.pack(r), DT), S.W)
        c1 = centre(S.deviation(r2))
        if c1 is None or c1[1] > SPAN:
            continue
        d = (c1[0] - c0[0] + S.W / 2) % S.W - S.W / 2
        v = round(d / DT, 3)
        vel[v].append((tr, k, x, "".join(map(str, ring[x:x + k])), c0[1], c1[1]))
    with open("ebg_vel.log", "a") as log:
        for v, ex in sorted(vel.items()):
            log.write(f"seed={seed} v={v:+.3f} count={len(ex)} example={ex[0]}\n")
            print(f"v={v:+.3f} count={len(ex)} example={ex[0]}")
