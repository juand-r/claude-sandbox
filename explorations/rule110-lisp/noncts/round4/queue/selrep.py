"""Replace K's first Ebar (the 'selector': crossed by the acceptor -> E0,
eaten by the rejector) by another slip-7 object at any placement in the
ether interval [K0-47, K0+22) (t_c = 6000, no gap). Stage A (answer
prepares K) and stage B (next read) for both paths (create2 pipeline,
right part from K0+25 on, transplant [RA, K0+25)).
    SPLITREL=25 python selrep.py out.jsonl"""
import sys, json
from create2 import *
from create import placements
from reads import tiles_of
gl = json.load(open(NONCTS / "collider" / "gliders.json"))["gliders"]
objs = [g["name"] for g in gl if (g["p"], g["d"]) in ((30, -8), (15, -4)) and g["slip"] % 14 == 7]
rej = Path(0, "NYYN", ("NYYN", "NNYY"), -345)
acc = Path(0, "YYNN", ("YYNN", "YNYN"), -200)
# control: the original selector re-placed (18, -25) must reproduce everything
for P_, nm in ((rej, "rej"), (acc, "acc")):
    seg = build_tight(P_.gA, P_.scA, P_.K0, [(ebar_tiles(), 18, -25)], -47, 22)
    w = P_.scA.run(seg, TA)
    print(nm, "identity rebuild equal to control:", bool((seg == P_.gA).all()), flush=True)
fh = open(sys.argv[1], "w")
for name in objs:
    try:
        tl = tiles_of(name)
    except (KeyError, RuntimeError, ValueError) as e:      # library object without a usable tile
        print("skip", name, repr(e), flush=True); continue
    p0 = phase_at(rej.gA, rej.scA.ebar_to_seg(rej.K0 - 47))
    for k, x, _ in placements(rej.scA, rej.K0, tl, -47, 22, p0):
        rec = {"obj": name, "k": k, "x": x}
        items = [(tl, k, x)]
        for P_, nm in ((rej, "rej"), (acc, "acc")):
            seg = build_tight(P_.gA, P_.scA, P_.K0, items, -47, 22)
            if seg is None:
                rec[nm + "A"] = None; break
            w = P_.scA.run(seg, TA)
            split = (P_.K0 + 25) - (P_.K0 - 1500)
            rec[nm + "A"] = int((w[split:] != P_.refA[split:]).sum())
            if rec[nm + "A"] == 0:
                full = unpack(step_packed_n(pack(seg), TA), len(seg))
                rec[nm + "B"] = P_.stageB(full)
        fh.write(json.dumps(rec) + "\n"); fh.flush()
print("done")
