"""Exhaustive version of ebg_vel.py for small windows: every pattern of k
cells (k = KMAX, all 2^k) written over the background at each of the 10
spatial offsets and 5 time phases (50 background variants), evolved T0
steps on the exact 640-cell ring; surviving localized deviations
(span <= SPAN) tracked DT steps for their velocity.  Distinct velocities
(rounded) with an example are written to ebg_exh.log.
Usage: python3 ebg_exh.py KMAX"""
import sys
from collections import defaultdict
import numpy as np
import ebg_search as S
import engine
from ebg_vel import centre

KMAX = int(sys.argv[1])
SPAN, DT, T0 = 60, 200, 2000
X = 300
vel = defaultdict(list)
n = 0
for var in range(50):
    base = S.VAR[var]
    for code in range(1 << KMAX):
        bits = np.array([(code >> i) & 1 for i in range(KMAX)], np.uint8)
        if np.array_equal(bits, base[X:X + KMAX]):
            continue
        ring = base.copy()
        ring[X:X + KMAX] = bits
        n += 1
        r = engine.unpack(engine.step_packed_n(engine.pack(ring), T0), S.W)
        c0 = centre(S.deviation(r))
        if c0 is None or c0[1] > SPAN:
            continue
        r2 = engine.unpack(engine.step_packed_n(engine.pack(r), DT), S.W)
        c1 = centre(S.deviation(r2))
        if c1 is None or c1[1] > SPAN:
            continue
        d = (c1[0] - c0[0] + S.W / 2) % S.W - S.W / 2
        vel[round(d / DT, 2)].append((var, code))
with open("ebg_exh.log", "a") as log:
    log.write(f"KMAX={KMAX} trials={n}\n")
    for v, ex in sorted(vel.items()):
        log.write(f"  v={v:+.2f} count={len(ex)} example={ex[0]}\n")
print(open("ebg_exh.log").read())
