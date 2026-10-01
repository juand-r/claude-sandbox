"""Validate a fixed left-stream program (t1_<WORD>.json) on inputs
VLO..VHI: exact CA, my typer; also checks the program's cells are identical
for every input, and runs a control (one slot moved to another class) that
must fail for some input.  Usage: python3 t1_validate.py WORD VLO VHI"""
import sys, json
import numpy as np
import t1lib as L
from t1_nonzero import model, Tfor  # noqa  (module-level code guarded below)

if __name__ == "__main__":
    word, vlo, vhi = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    d = json.load(open(f"t1_{word}.json"))
    slots = [tuple(s) for s in d["slots"]]
    T = Tfor(len(slots))
    progs = set()
    bad = 0
    for v in range(vlo, vhi + 1):
        objs, placed = L.outcome(slots, v, T)
        row, org, _ = L.build(slots, v, T)
        # program cells: from the row start to 40 cells left of the counter
        ex = [p for p in placed if p[0] == "E"][0][2]
        progs.add((org, row[:ex - 60 - org].tobytes()))
        got, want = L.value(objs), model(word, v)
        bad += got != want
        print(f"v={v:2d}: model {want:2d}  CA {got}  objects {[L.v3.base(n) for n, x in objs]}")
    print("program cells identical across inputs:", len(progs) == 1)
    print("mismatches:", bad)
    # control: move slot k to another class (t0+1, same x)
    k = len(slots) // 2
    ctl = list(slots)
    op, t0, x = ctl[k]
    ctl[k] = (op, (t0 + 1) % 3, x)
    cbad = sum(L.value(L.outcome(ctl, v, T)[0]) != model(word, v) for v in range(vlo, vhi + 1))
    print(f"control (slot {k} moved to t0+1): {cbad} mismatches (must be > 0)")
    assert bad == 0 and len(progs) == 1 and cbad > 0
    print("OK")
