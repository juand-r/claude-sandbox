"""Leader variants: replace one E-glider of the raw leader K by a
slip-equivalent longer one (E5->E12, E2->E9, E^3->E^10), at every nearby
lattice placement; the rest re-attached with a machine symmetry shift.
Output: reads 0/1 region counts for the four tapes (acc-in: YYNN, YNYN;
rej-in: NYYN, NNYY). Base: [26,25] [26,1] [3,24] [3,1]."""
import sys, json
from splice import *
T = 60000
which = sys.argv[1]
SPEC = {"E5": (-2, 41, 12), "E2": (41, 72, 9), "E3": (72, 150, 10)}
rc0, rc2, n = SPEC[which]
tiles = en_tiles(n)
TAPES = ("YYNN", "YNYN", "NYYN", "NNYY")
M = {t: Machine(t, ["YNNNNN"], T, left_periods=4, right_periods=3) for t in TAPES}
SH = [sd for sd in valid_shifts(400) if sd[1] >= 0]
for k in range(15):
    for off in range(0, 60):
        res = {}
        for t, m in M.items():
            K = [a for nn, a, b in m.blocks if nn == "K"]
            o = m.origin
            c = ether_cut(m.row, o + K[0] + rc0, search=3, tight=True) if which == "E5" else o + K[0] + rc0
            row = None
            for s, D in SH:
                row = replace_exact(m.row, c, o + K[0] + rc2, [(tiles, k, off)], s, D)
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
