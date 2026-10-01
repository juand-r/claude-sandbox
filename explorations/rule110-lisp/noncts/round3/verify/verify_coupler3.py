"""Check coupler 06:20 item 2: SAT record (R1 face, Y free in (12,-6)) whose
rows give X + E^4 -> B + E^2.  A: their exact t=0 rows (sat_shuttle_results
.jsonl, kind r1, sat) rebuilt with my ether, run by the engine, typed by my
typer.  B: X cut out of the row and tested by face_test against MY E^n,
n = 1..10, all classes."""
import json, sys
import numpy as np
import v3, vlib, engine
import face_test as F

recs = [json.loads(l) for l in open("../coupler/sat_shuttle_results.jsonl")]
recs = [r for r in recs if r.get("sat") and (r.get("only") == "r1")]
print(len(recs), "SAT r1 records")
E = vlib.ETHER
T = 1500
for ri, r in enumerate(recs):
    print("record", ri, "py", r["py"], "sx", r["sx"], "K", r["K"], "classes", r["c1"], r["c2"])
    for (lo, pL, pR), bits in zip(r["frames"], r["rows0"]):
        seg = np.array([int(c) for c in bits], np.uint8)
        pad = 2 * T + 200
        row = np.concatenate([E[(np.arange(lo - pad, lo) + pL) % 14], seg,
                              E[(np.arange(lo + len(seg), lo + len(seg) + pad) + pR) % 14]])
        t0 = [v3.base(n) for n, x, w, k in vlib.identify(row, lo - pad)]
        out = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
        t1 = [v3.base(n) for n, x, w, k in vlib.identify(out, lo - pad, T=T)]
        print("   t=0:", t0, " t=%d:" % T, t1)


def cut_left_train(r, which=0):
    (lo, pL, pR), bits = r["frames"][which], r["rows0"][which]
    seg = np.array([int(c) for c in bits], np.uint8)
    pad = 200
    row = np.concatenate([E[(np.arange(lo - pad, lo) + pL) % 14], seg,
                          E[(np.arange(lo + len(seg), lo + len(seg) + pad) + pR) % 14]])
    ids = vlib.identify(row, lo - pad)
    xe = [x for n, x, w, k in ids if v3.base(n).startswith("E")][0] - (lo - pad)
    d = [dd for dd in vlib.defects(row) if dd["hi"] <= xe]
    a, b = d[0]["lo"], d[-1]["hi"]
    c = vlib.window_phase(row)[a - 20]
    x0 = a - 4
    while (x0 + c) % 14:
        x0 -= 1
    rs = vlib.runs(row[:xe])
    slip = (rs[-1][2] - rs[0][2]) % 14
    return "".join(map(str, row[x0:b + 2])), slip


if __name__ == "__main__" and len(sys.argv) > 1:
    for ri in (3, 4):
        bits, slip = cut_left_train(recs[ri])
        print("record", ri, "X =", bits, "slip", slip)
        F.test(f"X{ri}", bits, slip, (3, 2), "left", ns=range(1, 11), T=3000)
