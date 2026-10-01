"""Leader variants: replace K's E2 by E9 (or E5 by E12) - slip-neutral
(+7 units = +42 = 0 mod 14) - at every nearby lattice placement, remainder
re-attached with a machine symmetry shift. Record reads 0/1 outcomes for
the four tapes."""
import sys, json
from splice import *
T = 60000
which = sys.argv[1]            # "E2" or "E5"
TAPES = ("YYNN", "YNYN", "NYYN", "NNYY")
M = {t: Machine(t, ["YNNNNN"], T, left_periods=4, right_periods=3) for t in TAPES}
SH = valid_shifts(400)
if which == "E2":
    rc0, rc2, new = 41, 72, "E^9"       # cut after E5, before E^3
else:
    rc0, rc2, new = 0, 41, "E^12"
tiles = glider_tiles(new) if new != "E^12" else None
for k in range(15):
    for off in range(0, 40):
        res = {}
        for t, m in M.items():
            K = [a for n, a, b in m.blocks if n == "K"]
            o = m.origin
            row = None
            for s, D in SH:
                if D < 0:
                    continue
                row = replace_exact(m.row, o + K[0] + rc0, o + K[0] + rc2, [(tiles, k, off)], s, D)
                if row is not None:
                    break
            if row is None:
                break
            cs = m.run(row, T, 1100, K[2] + 300)
            res[t] = ([sum(1 for x, y, kk in cs if lo <= x < hi and kk == "E")
                       for lo, hi in [(1100, K[0]), (K[0], K[1])]],
                      len([1 for x, y, kk in cs if kk != "E"]), [int(s), int(D)])
        if len(res) == 4:
            print(json.dumps({"k": k, "off": off, "r": res}), flush=True)
