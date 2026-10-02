"""Check objects 00:31/00:32: E^45 with front type c = 7, hit from behind by
the (1,9) bubble wall, becomes ONE clean E-rod ((15,-4) and (300,-80)
periodic), ~27 cells shorter, left ether unchanged; control (no wall) stays
the original rod. Rows from objects/xconv_n45.json (plain cells + ether
phases, convention ETHER[(phase + y) mod 14]); my row assembly, hrun, my
defect segmentation and E-bg phase reading."""
import json
import os

import numpy as np

import hrun

vlib = hrun.vlib
HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "..", "objects", "xconv_n45.json")))
PAD = 3000


def row_of(v):
    bits = np.array([int(c) for c in v["bits"]], np.uint8)
    lo, hi = v["x_lo"] - PAD, v["x_lo"] + len(bits) + PAD
    y = np.arange(lo, hi)
    row = np.where(y < v["x_lo"], vlib.ETHER[(v["left_phase"] + y) % 14],
                   vlib.ETHER[(v["right_phase"] + y) % 14]).astype(np.uint8)
    row[PAD:PAD + len(bits)] = bits
    return row, lo


def describe(v, T):
    row, org = row_of(v)
    h = hrun.HRun(row, org)
    out = {}
    for t in (T, T + 15, T + 300):
        h.goto(t)
        out[t] = h.cells(org - t - 200, org + len(row) + t + 200)
    lo = org - T - 200
    ds = vlib.defects(out[T])
    spans = [(d["lo"] + lo, d["hi"] + lo) for d in ds]
    r0 = out[T]
    # (15,-4): row(T+15)[x] = row(T)[x+4] (windows aligned at lo - 15 vs lo)
    r15 = out[T + 15]       # covers [org - T - 215, ...)
    per15 = np.array_equal(r15[15:15 + len(r0) - 4], r0[4:])
    r300 = out[T + 300]
    per300 = np.array_equal(r300[300:300 + len(r0) - 80], r0[80:])
    # left ether phase at the far left
    lp = None
    for q in range(14):
        if np.array_equal(r0[:14], vlib.ETHER[(np.arange(lo, lo + 14) + 4 * T + q) % 14]):
            lp = q
    return spans, per15, per300, lp


if __name__ == "__main__":
    for T in (1200, 3000):
        for k in ("wall", "nowall"):
            spans, p15, p300, lp = describe(D[k], T)
            print(f"T={T} {k}: {len(spans)} defect(s) {spans}, length {[b - a for a, b in spans]}, "
                  f"(15,-4)-periodic {p15}, (300,-80)-periodic {p300}, left ether phase {lp}")
