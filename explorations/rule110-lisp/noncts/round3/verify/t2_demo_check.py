"""Checks on the T2 demo (t2_demo.json): (1) model on inputs 0..VMAX;
(2) left-program cells identical (same positions) for all inputs; right
program J I cells identical up to the phase snap forced by the input's
charge (report the translation per input); (3) controls that must fail:
(a) one left Z slot moved to another class, (b) the R1 phase class t1+1
(cuts the R1 -> R2 channel), (c) no J I block."""
import sys, json
import numpy as np
import t2_demo as D
import vlib

d = json.load(open("t2_demo.json"))
t1, slots = d["t1"], [tuple(s) for s in d["slots"]]
VMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
bad, lefts, jpos = 0, set(), {}
for v in range(VMAX + 1):
    got, objs, row, placed = D.outcome(slots, v, t1)
    bad += got != D.model(D.LEFT, v)
    items, c0 = D.scene(slots, v, t1)
    r0, org, pl = vlib.build(items, c0=c0, pad=200)
    ie = [i for i, p in enumerate(pl) if p[0] == "E"][0]
    lefts.add(tuple(pl[:ie]))
    jpos[v] = [p for p in pl if p[0] == "GB1"][0][1:]
    print(f"v1={v}: model {D.model(D.LEFT, v)} CA {got} objects {objs}")
print(f"mismatches {bad}; left-program placements identical across inputs: {len(lefts) == 1}")
print("J seed (t0, x) per input (translation = phase snap):", jpos)
# controls
c = list(slots); op, t0, x = c[3]; c[3] = (op, (t0 + 1) % 3, x)
ca = sum(D.outcome(c, v, t1)[0] != D.model(D.LEFT, v) for v in range(4))
cb = sum(D.outcome(slots, v, (t1 + 1) % 3)[0] != D.model(D.LEFT, v) for v in range(4))
cc = sum(D.outcome(slots, v, t1, block=False)[0] != D.model(D.LEFT, v) for v in range(4))
print(f"controls (mismatches over v1 = 0..3, each must be > 0): moved Z slot {ca}, "
      f"R1 class t1+1 {cb}, no J I block {cc}")
assert bad == 0 and len(lefts) == 1 and ca and cb and cc
print("OK")
