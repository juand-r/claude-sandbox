"""The E0 idea: Cook's acceptor leaves one extra Ebar E0 in front of the
reader; the rejector does not. Take a modifier Q that is EXACT-NORMAL in the
rejector path (rej-path read unchanged, debris V-standard) and test the
acceptor path with Q added in the pure-ether interval [K0+LO, K0+HI)
between the last moving-data Ebar (cluster K0-118) and E0 (cluster K0+0)
at t_in = 31500. Want: acc path FORCED-N with exact debris -> then the
same table material behaves differently by state (E0 present or not).
Input: vfilter output lines (only (0,0),(0,0) entries are used), Q must
persist (rej-path scene differs from plain at t_in+200 in [K0-345,K0+37)).
    python accZ.py vfilter_yn.txt out.jsonl"""
import sys, json
import numpy as np
from lscene import *
from create2 import build_tight
from reads import tiles_of
TIN, T = 31500, 3000
JS = range(-8, 9)
WLO, WHI, SPLIT = -400, 800, 100
LO, HI = -104, -2
S = {}
for t in ("YYNN", "YNYN", "NYYN"):
    m = Machine(t, ["YNNNNN"], TIN + T + 500, left_periods=3, right_periods=2)
    K0 = [a for n, a, b in m.blocks if n == "K"][0]
    sc = Scene(m, m.row, TIN, K0 + WLO, K0 + WHI, T + 30 * 8 + 50)
    S[t] = (K0, sc, {j: sc.run(sc.seg, T - 30 * j) for j in JS})
def score(w, tapes=("YYNN", "YNYN")):
    s = SPLIT - WLO
    out = []
    for rt in tapes:
        R = S[rt][2]
        d = {j: int((w[s:] != R[j][s:]).sum()) for j in JS}
        j = min(d, key=lambda q: (d[q], abs(q)))
        out += [d[j], j]
    return out + [int((w[:s] != S[rt][2][0][:s]).sum()) for rt in tapes]
for t in ("YYNN", "YNYN"):
    print("control", t, score(S[t][1].run(S[t][1].seg, T)), flush=True)
fh = open(sys.argv[2], "w")
seen = set()
for line in open(sys.argv[1]):
    if "(0, 0), (0, 0)" not in line: continue
    r = json.loads(line[line.index("{"):])
    if "A" in r:
        spec = [(r["B"], r["kb"], r["xb"]), (r["A"], r["ka"], r["xa"])]
    elif "obj" in r:
        spec = [(r["obj"], r["k"], r["x"])]
    else:
        spec = [("Ebar", r["k2"], r["x2"]), ("Ebar", r["k1"], r["x1"])]
    key = json.dumps(spec)
    if key in seen: continue
    seen.add(key)
    # persistence check in the rej path
    K0r, scr, _ = S["NYYN"]
    import zscreen
    items = [(tiles_of(n), k, x) for n, k, x in spec]
    segr = zscreen.build2(scr, K0r, items)
    if segr is None: continue
    a = scr.ebar_to_seg(K0r - 345, TIN + 200); b = scr.ebar_to_seg(K0r + 37, TIN + 200)
    w1 = unpack(step_packed_n(pack(segr), 200), len(segr))[a:b]
    w0 = unpack(step_packed_n(pack(scr.seg), 200), len(segr))[a:b]
    if np.array_equal(w1, w0): continue          # Q vanished by itself
    # shift Q so that it lies in [LO, HI): try translations by multiples of 56 (V-trivial)
    xs = [x for _, _, x in spec]
    rec = None
    for sh in range(-560, 561, 56):
        if min(xs) + sh < LO or max(x for x in xs) + sh + 44 > HI + 16: continue
        its = [(tiles_of(n), k, x + sh) for n, k, x in spec]
        out = {}
        for t in ("YYNN", "YNYN"):
            K0, sc, _ = S[t]
            seg = build_tight(sc.seg, sc, K0, its, LO, HI)
            if seg is None: out = None; break
            out[t] = score(sc.run(seg, T))
        if out:
            rec = {"Q": spec, "shift": sh, **out}
            fh.write(json.dumps(rec) + "\n"); fh.flush()
print("done", len(seen))
