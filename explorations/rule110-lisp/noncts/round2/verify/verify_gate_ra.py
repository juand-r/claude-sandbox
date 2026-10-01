"""Independent check of gate's 00:53 claim: fixed program (Z6 N)^10 with
classes 0,1,0,1,0,0,1,0,2,0,0,0,1,0,2,0,0,0,1,0 (rafast conventions), inputs
v = 0..9 -> (v - 10) mod 7, one E^k, nothing else.
Scenes from gate's rafast (read-only import: Program, input_prefix,
shift_for). I check (1) that the program items are the SAME for all inputs up
to an x-shift, (2) translation into my convention (row equality asserted),
(3) exact engine + my typer, stability T vs T+3000, (4) gate's control."""
import os, sys
import vlib, xlate
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.abspath(os.path.join(HERE, "..", "gate"))
COLL = os.path.abspath(os.path.join(HERE, "..", "..", "collider"))
sys.path.insert(0, GATE)
cwd = os.getcwd()
import common  # noqa: E402,F401
from rafast import Program, input_prefix, shift_for  # noqa: E402
os.chdir(cwd)

def scenes(prog, cls, vs):
    os.chdir(COLL)
    try:
        P = Program()
        for op, c in zip(prog, cls):
            P.add(op, c)
        out = {}
        for v in vs:
            pre = input_prefix(v)
            D = shift_for(pre, P.items[0])
            out[v] = (pre + [(n, t, x + D) for n, t, x in P.items], D, list(P.items))
    finally:
        os.chdir(cwd)
    return out

def run(sc, extra=0):
    ex = xlate.expand([(g, int(t), int(x)) for g, t, x in sc])
    items, c0, same = xlate.check(ex)
    assert same
    T = int(15 * (items[-1][2] - items[0][2] + 300)) + 3000 + extra
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = vlib.evolve(row, T)
    return [n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T)]

def value(ids):
    if len(ids) == 1 and (ids[0] == "E" or ids[0].startswith("E^")):
        return 0 if ids[0] == "E" else int(ids[0][2:]) - 1
    return None

if __name__ == "__main__":
    prog = "ZN" * 10
    cls = [0,1,0,1,0,0,1,0,2,0,0,0,1,0,2,0,0,0,1,0]
    sc = scenes(prog, cls, range(10))
    items0 = sc[0][2]
    print("program items identical for all inputs:", all(s[2] == items0 for s in sc.values()),
          "| x-shifts per input:", [s[1] for s in sc.values()])
    ok = True
    for v in range(10):
        ids, ids2 = run(sc[v][0]), run(sc[v][0], extra=3000)
        exp = (v - 10) % 7
        good = value(ids) == exp and ids == ids2
        ok &= good
        print(f"v={v}: {ids} value {value(ids)} model {exp} stable {ids == ids2} {'OK' if good else 'BAD'}", flush=True)
    bad = list(cls); bad[1] = 0
    scb = scenes(prog, bad, [0, 1, 2])
    ctrl = {v: run(scb[v][0]) for v in (0, 1, 2)}
    print("control (slot 1 class 1->0):", ctrl)
    print("REPRODUCED" if ok and value(ctrl[1]) != (1 - 10) % 7 else "NOT REPRODUCED")
