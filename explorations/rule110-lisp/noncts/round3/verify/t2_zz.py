"""R2 -> R1 channel with a data-dependent number of signals.
Fixed left program Z Z (Z_L slots from t1z_ZZ.json, moved 600 lattice
periods left so they arrive after R1's input packets).  R2 = E + y B's
(y = 0: two zero events -> two A's to R1; y = 1: one; y = 2: none).
R1 = E + 5 GB5's at (t1, D).  Model: R2 = max(y-2,0), R1 = 5 - max(2-y,0).
For each R1 phase t1 (15) report outcomes per y; a t1 that works for all y
means the channel composes with a data-dependent signal count."""
import sys, json
from collections import defaultdict
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()
D = 900
SH = -14 * 700
slots = [tuple(s) for s in json.load(open("t1z_ZZ.json"))["slots"]][:2]


def run(y, t1, m=5):
    prog = [(L.OPS[o], t, x + SH) for o, t, x in slots][::-1]
    right = [("E", 0, 0)] + [("B", 0, 75 + 50 * k) for k in range(y)] + [("E", t1, D)]
    for j in range(m):
        right += AC.parts("I", t1, D + 150 + 110 * j)
    items = prog + right
    c0 = (L.C_E - sum(vlib.LIB[n].w for n, _, _ in prog)) % 14
    T = 15 * (D + 150 + 110 * m) + 16000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return " + ".join(v3.base(n) for n, x, w, k_ in vlib.identify(r, org, T=T))


if __name__ == "__main__":
    want = {0: "E + E^4", 1: "E + E^5", 2: "E + E^6"}
    for t1 in range(15):
        res = {y: run(y, t1) for y in range(3)}
        ok = all(res[y] == want[y] for y in range(3))
        print(f"t1={t1:2d} {'ALL OK' if ok else '      '} " + " | ".join(f"y={y}: {res[y]}" for y in range(3)), flush=True)
