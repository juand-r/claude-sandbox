"""Independent check of gate's 00:27 claim: program (J^5 Z6^6)^2 with the
per-slot classes from gate/adaptive.py, inputs v = 0..3 (prefix of v GB5's,
class 0) -> final value v mod 2, garbage only Bbars leaving left.
Scene: gate's adaptive.build (read-only import; the scene is the claim's
input). Then my translation (row equality asserted), exact engine, my typer,
stability check at T and T + 3000. Control: first J in class 0."""
import os, sys
import vlib, xlate
HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.abspath(os.path.join(HERE, "..", "gate"))
COLL = os.path.abspath(os.path.join(HERE, "..", "..", "collider"))
sys.path.insert(0, GATE)
cwd = os.getcwd()
import common  # noqa: E402,F401  (chdirs into collider)
from adaptive import build  # noqa: E402
os.chdir(cwd)

def gate_scene(prog, cls, v):
    os.chdir(COLL)
    try:
        sc = build(["I"] * v + list(prog), [0] * v + cls)
    finally:
        os.chdir(cwd)
    return [(g, int(t), int(x)) for g, t, x in sc]

def run(sc, extra=0):
    ex = xlate.expand(sc)
    items, c0, same = xlate.check(ex)
    assert same, "translation mismatch"
    T = int(15 * (items[-1][2] - items[0][2] + 300)) + 3000 + extra
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = vlib.evolve(row, T)
    return [n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T)]

def value(ids):
    rest = [i for i in ids if i != "Bbar"]
    if len(rest) == 1 and (rest[0] == "E" or rest[0].startswith("E^")):
        return 0 if rest[0] == "E" else int(rest[0][2:]) - 1
    return None

def model(prog, v):
    for c in prog:
        if c == "J": v = v + 1 if v > 0 else 0
        elif c == "Z": v = v - 1 if v > 0 else 6
    return v

if __name__ == "__main__":
    prog = "JJJJJZZZZZZ" * 2
    cls = [1,0,2,1,0,1,0,0,0,0,0, 0,2,1,0,2,0,0,0,0,0,0]
    ok = True
    for v in range(4):
        sc = gate_scene(prog, cls, v)
        ids, ids2 = run(sc), run(sc, extra=3000)
        good = value(ids) == model(prog, v) and ids == ids2
        ok &= good
        print(f"v={v}: {sorted(set(ids))} value {value(ids)} model {model(prog, v)} stable {ids == ids2} {'OK' if good else 'BAD'}", flush=True)
    bad = [0] + cls[1:]
    ctrl = [value(run(gate_scene(prog, bad, v))) != model(prog, v) for v in range(2)]
    print("control (first J class 0): differs for v=0,1:", ctrl)
    print("REPRODUCED" if ok and any(ctrl) else "NOT REPRODUCED")
