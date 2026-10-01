"""Screen for a state-dependent reader: a TIGHT Ebar pair (collider
compound 'Ebar@(0,0)+Ebar@(dt,dx)' etc., slip 0) inserted right before the
first raw leader K, remainder attached with a machine symmetry shift.
Stage A (this script): acceptor tape YNYN must stay NORMAL (read0 Y,
read1 N, no garbage at T). Survivors are listed for stage B (check4-like,
all four tapes). Resumable: skips logged entries.
    python screen_tight.py   (appends to screen_tight.jsonl)"""
import json, os
from splice import *
T = 40000
LOG = "screen_tight.jsonl"
done = set()
if os.path.exists(LOG):
    for line in open(LOG):
        d = json.loads(line)
        done.add((d["name"], d["k"], d["o"]))
g = json.load(open(ROOT / "noncts" / "collider" / "gliders.json"))["gliders"]
names = [x["name"] for x in g if x["name"].startswith("Ebar") and x["name"].count("Ebar") == 2
         and "E_" not in x["name"] and x["p"] == 30]
m = Machine("YNYN", ["YNNNNN"], T, left_periods=4, right_periods=3)
K = [a for n, a, b in m.blocks if n == "K"]
c = ether_cut(m.row, m.origin + K[0], search=10, tight=True)
SH = valid_shifts(600)
out = open(LOG, "a")
for name in names:
    tiles = glider_tiles(name)
    for k in range(len(tiles)):
        arr, cl, cr = tiles[k]
        base = (cl - c - phase_at(m.row, c)) % TILE
        for o in (base, base + 14):
            if (name, k, int(o)) in done:
                continue
            row = None
            for s, D in SH:
                row = replace_exact(m.row, c, c, [(tiles, k, int(o))], s, D)
                if row is not None:
                    break
            if row is None:
                res = None
            else:
                cs = m.run(row, T, 1100, K[2] + 300)
                res = ([sum(1 for x, y, kk in cs if lo <= x < hi and kk == "E")
                        for lo, hi in [(1100, K[0]), (K[0], K[1])]],
                       len([1 for x, y, kk in cs if kk != "E"]), [int(s), int(D)])
            out.write(json.dumps({"name": name, "k": k, "o": int(o), "r": res}) + "\n")
            out.flush()
