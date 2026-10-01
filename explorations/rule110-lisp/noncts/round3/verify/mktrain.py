"""Cut a rigid train (several same-period items) out of my builder's row as
raw cells with phase-0 ether on its left (the convention of face_test /
t1lib), plus its slip."""
import vlib


def cut(items):
    row, org, placed = vlib.build(items, c0=0, pad=60)
    d = vlib.defects(row)
    lo, hi = d[0]["lo"], d[-1]["hi"]
    c = vlib.window_phase(row)[lo - 20]          # row-index phase
    x0 = lo - 4
    while (x0 + c) % 14:
        x0 -= 1
    rs = vlib.runs(row)
    slip = (rs[-1][2] - rs[0][2]) % 14
    return "".join(map(str, row[x0:hi + 2])), slip, placed
