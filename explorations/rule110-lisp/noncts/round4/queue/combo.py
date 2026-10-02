"""Compose a forced-N modifier Z (slip 0, from the screens) with an
exact-normal modifier M (slip 0, consumed without trace in a normal read,
debris V-standard; from vfilter_yn.txt, persisting ones only). Rejector
path scenes (t_in = 31500). Want: forced-N for Y and N with V-standard
debris (vequiv.vclass) for both.
    python combo.py out.jsonl"""
import sys, json
import numpy as np
import zscreen
zscreen.JS = range(-8, 9)
from zscreen import *
from vequiv import vclass
from reads import tiles_of
S = zscreen.setup()
def cls(v):
    if v is None: return "-"
    return "Y" if v[0] == 0 else ("N" if v[2] == 0 else "x")
def items_of(r):
    if "A" in r:
        return [(r["B"], r["kb"], r["xb"]), (r["A"], r["ka"], r["xa"])]
    if "obj" in r:
        return [(r["obj"], r["k"], r["x"])]
    return [("Ebar", r["k2"], r["x2"]), ("Ebar", r["k1"], r["x1"])]
# forced-N Z's (rej path NN)
Zs = {}
for f in ("zpairs_rej.jsonl", "zlib0.jsonl", "zmix.jsonl", "zmix_tight.jsonl"):
    for l in open(f):
        r = json.loads(l)
        if cls(r.get("NYYN")) + cls(r.get("NNYY")) == "NN":
            it = items_of(r); Zs[json.dumps(it)] = it
# exact-normal M's, persisting
K0r, scr = S["NYYN"][:2]
Ms = {}
for line in open("vfilter_yn.txt"):
    if "(0, 0), (0, 0)" not in line: continue
    it = items_of(json.loads(line[line.index("{"):]))
    seg = zscreen.build2(scr, K0r, [(tiles_of(n), k, x) for n, k, x in it])
    if seg is None: continue
    a = scr.ebar_to_seg(K0r - 345, zscreen.TIN + 200); b = scr.ebar_to_seg(K0r + 37, zscreen.TIN + 200)
    w1 = unpack(step_packed_n(pack(seg), 200), len(seg))[a:b]
    w0 = unpack(step_packed_n(pack(scr.seg), 200), len(seg))[a:b]
    if not np.array_equal(w1, w0):
        Ms[json.dumps(it)] = it
print("Z", len(Zs), "M", len(Ms), flush=True)
fh = open(sys.argv[1], "w"); n = 0
for zk, Z in Zs.items():
    for mk, M in Ms.items():
        allit = sorted(Z + M, key=lambda t: t[2])
        rec = {"Z": Z, "M": M}
        for tape in ("NYYN", "NNYY"):
            K0, sc = S[tape][:2]
            seg = zscreen.build2(sc, K0, [(tiles_of(nm), k, x) for nm, k, x in allit])
            if seg is None:
                rec = None; break
            s_ = zscreen.score(S, tape, sc.run(seg, zscreen.T))
            rec[tape] = s_
            if s_[2] != 0:
                break
            rec[tape + "_v"] = vclass(S, tape, seg, K0)
        if rec is None: continue
        n += 1
        if rec.get("NNYY") is not None and rec["NNYY"][2] == 0:
            fh.write(json.dumps(rec) + "\n"); fh.flush()
print("done", n)
