"""Zero test, stage 4 (fast). Build the value-0 compound once (DEC, DEC
from gap 43 in the fixed-stream layout), note its seed event relative to
the slot-2 anchor, then hit the bare compound with every pure-Ebar mover
(placed exactly as it would be in slot 2) in short simulations.
Records all products; flags compound intact + one stationary messenger."""
import json, re, sys
sys.path.insert(0, "../collider")
from collide import simulate
from winding3 import movers
from xstream import build, DELTA, SLOT_LEN, PF
from rx import LIB


def slot_anchor(j):
    return (j * DELTA[0] + j * SLOT_LEN * PF[0], j * DELTA[1] + j * SLOT_LEN * PF[1])


if __name__ == "__main__":
    res = simulate(LIB, build(["DEC", "DEC"]), 36 * (SLOT_LEN + 5) * 2 + 8000)
    comp = [p for p in res["products"] if p[0].startswith("F_19_F")]
    assert len(comp) == 1, res["products"]
    cname, ct, cx = comp[0]
    print("compound", comp[0], "anchor slot 2", slot_anchor(2), flush=True)
    a = slot_anchor(2)
    MV = [m for m in movers() if not re.search(r"E(?!bar)", m[0])]
    out = open("zc_fast.jsonl", "w")
    for i, (name, t, x) in enumerate(MV):
        mv = (name, a[0] + t + 20 * PF[0], a[1] + x + 20 * PF[1])
        # shift everything so the compound's seed is near t = 0 (same
        # relative geometry): subtract k F-periods from both
        k = mv[1] // 36 - 3
        pl = [(cname, ct - 36 * k, cx + 4 * k), (mv[0], mv[1] - 36 * k, mv[2] + 4 * k)]
        r = simulate(LIB, pl, 4000)
        names = sorted(p[0] for p in r["products"])
        out.write(json.dumps({"i": i, "mover": [name, t, x], "settled": r["settled"],
                              "products": r["products"]}) + "\n")
        out.flush()
        ncomp = sum(1 for n in names if n.startswith("F_19_F"))
        cs = [n for n in names if n in ("C1", "C2", "C3")]
        if ncomp == 1 and cs:
            print("CANDIDATE", i, (name, t, x), names, flush=True)
    print("done", len(MV), flush=True)
