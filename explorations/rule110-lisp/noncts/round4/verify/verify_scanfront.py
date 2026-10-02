"""Check objects 00:53 (scan_front): library right-movers that hit the
FRONT of E^24 and leave ONE clean rod while a front->back wall reaches the
back: v2/3s6w13 -> E^25, v2/3s8w5 -> E^23, v2/3s2w20 -> E^17, D1_9_D1 /
D1_8_D1 / D2_7_D2#2 -> E^18 (in some time phases); A in 1 of 3 phases is
the plain DEC with no back hit.
My construction: object cells from my library / collider definition
(clib, period re-found) taken in each time phase as raw list-form cells;
E^24 = round-3 longrod splice (my library); rawscene + hrun; rodval for
the value; "back hit" = the rod's right end differs from the rod-alone run
before T."""
import sys

import numpy as np

import clib
import hrun
import rawscene
import rodval
import spot_bounce as SB

sys.path.insert(0, hrun.R3V)
import longrod  # noqa: E402

vlib = hrun.vlib
T = 900


def list_forms(name):
    """(bits, pR) of the object in each time phase s = 0..P-1 (my builder)."""
    g = vlib.LIB[name]
    out = []
    for s in range(g.P):
        row, org, _ = vlib.build([(name, s, 0)], pad=200)
        ds = vlib.defects(row)
        a, b = min(d["lo"] for d in ds), max(d["hi"] for d in ds)
        bits, pR, _ = SB.list_form(row, org, 0, a, b)
        out.append((bits, pR))
    return sorted(set(out))


def rod_form():
    row, org = longrod.rod(24)
    ds = vlib.defects(row)
    a, b = min(d["lo"] for d in ds), max(d["hi"] for d in ds)
    bits, pR, _ = SB.list_form(row, org, 0, a, b)
    return bits, pR


def run(objs):
    row, org, st = rawscene.assemble(objs)
    return row, org, st


if __name__ == "__main__":
    rb, rp = rod_form()
    # rod alone reference (same placement as in the scenes: 100 + gap)
    for name in ["A", "v2/3s6w13", "v2/3s8w5", "v2/3s2w20", "D1_9_D1", "D1_8_D1", "D2_7_D2#2"]:
        if name not in vlib.LIB:
            clib.ensure(name)
        res = []
        for bits, pR in list_forms(name):
            row, org, st = run([(bits, pR, 100), (rb, rp, 60)])
            v = rodval.value(row, org, T)
            # back hit: compare the rod's right end region with a rod-alone run
            row0, org0, st0 = run([(rb, rp, 100 + len(bits) + 60)])
            h, h0 = hrun.HRun(row, org), hrun.HRun(row0, org0)
            hit = None
            for t in range(0, T, 10):
                h.goto(t); h0.goto(t)
                xr = st[1] + len(rb) - (4 * t) // 15
                a = h.cells(xr - 30, xr + 30); b = h0.cells(xr - 30, xr + 30)
                if not np.array_equal(a, b):
                    hit = t
                    break
            res.append((v, hit))
        print(name, "per phase (value, first back-hit time):", res, flush=True)
