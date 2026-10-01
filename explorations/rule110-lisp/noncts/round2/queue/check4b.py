"""Stage B of screen_tight: survivors on all four tapes, 2 reads (T=60000).
Outcome letters per tape: read0 read1 / number of non-Ebar objects."""
import sys, json
from splice import *
T = 60000
TAPES = ("YYNN", "YNYN", "NYYN", "NNYY")
M = {t: Machine(t, ["YNNNNN"], T, left_periods=4, right_periods=3) for t in TAPES}
SH = valid_shifts(600)
def l0(c): return "Y" if 22 <= c <= 30 else "N" if c <= 5 else "?"
def l1(c): return "Y" if 20 <= c <= 30 else "N" if c <= 3 else "R" if c >= 50 else "?"
def run(name, k, o):
    out = {}
    tiles = glider_tiles(name)
    for t, m in M.items():
        K = [a for n, a, b in m.blocks if n == "K"]
        c = ether_cut(m.row, m.origin + K[0], search=10, tight=True)
        for s, D in SH:
            row = replace_exact(m.row, c, c, [(tiles, k, o)], s, D)
            if row is not None:
                break
        cs = m.run(row, T, 1100, K[2] + 300)
        c0, c1 = [sum(1 for x, y, kk in cs if lo <= x < hi and kk == "E") for lo, hi in [(1100, K[0]), (K[0], K[1])]]
        out[t] = l0(c0) + l1(c1) + f"/{len([1 for x, y, kk in cs if kk != 'E'])}"
    return out
if __name__ == "__main__":
    rows = [json.loads(l) for l in open("screen_tight.jsonl")]
    ok = [r for r in rows if r["r"] and 24 <= r["r"][0][0] <= 30 and r["r"][0][1] <= 3 and r["r"][1] <= 5]
    import os
    LOG = "check4b.jsonl"
    done = set()
    if os.path.exists(LOG):
        for line in open(LOG):
            d = json.loads(line)
            done.add((d["name"], d["k"], d["o"]))
    out = open(LOG, "a")
    for r in ok:
        if (r["name"], r["k"], r["o"]) in done:
            continue
        res = run(r["name"], r["k"], r["o"])
        out.write(json.dumps({"name": r["name"], "k": r["k"], "o": r["o"], "res": res}) + "\n")
        out.flush()
        print(r["name"], r["k"], r["o"], res, flush=True)
