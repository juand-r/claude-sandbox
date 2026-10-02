"""Check objects 00:19: stationary extendable rods ("C-stacks").
Rod S9_k = ether(phase 0) | (100000110)^k | ether(rp_k), rp_k = 6 - 9 (k - 4)
mod 14 (objects/srods.json entry 000000111 #5, cells only).
(a) stationary and stable: row(t + 7) == row(t) on the rod for k = 1..30
    (my stepper via hrun), and nothing else appears, up to t = 2000.
(b) from the LEFT, A / A^2 / A^4 remove ONE tile and send F / Ebar / E back
    left; D1, D2 remove two tiles. From the RIGHT, B / B^2 / B^3 destroy the
    whole stack. Checked at k = 6 with the glider at 3 different gaps
    (single class: the outcome must not depend on the gap).
Remaining rod read as: the final row (t = 0 mod 7) contains exactly the
cells of S9_(k-j) somewhere (my list-form match), nothing else stationary."""
import numpy as np

import hrun
import rawscene

vlib = hrun.vlib
TILE9 = "100000110"


def rod(k):
    return TILE9 * k, (6 - 9 * (k - 4)) % 14


def bits_of(name):
    g = vlib.LIB[name]
    ds = vlib.defects(g.base)
    lo = min(d["lo"] for d in ds)
    hi = max(d["hi"] for d in ds)
    lo -= lo % 14
    return "".join(map(str, g.base[lo:hi])), (lo + g.w) % 14


def run(objs, T):
    row, org, st = rawscene.assemble(objs)
    h = hrun.HRun(row, org)
    h.goto(T)
    lo = org - T - 300
    return h.cells(lo, org + len(row) + T + 300), lo, h


def tiles_left(r):
    """largest j such that the row contains the cells of S9_j with its two
    ether faces (14 cells of each face's ether), else 0"""
    s = "".join(map(str, r))
    for j in range(40, 0, -1):
        bits, rp = rod(j)
        # canonical faces: left ether phase 0, right ether rp, in local coords
        left = "".join(str(vlib.ETHER[i % 14]) for i in range(-14, 0))
        right = "".join(str(vlib.ETHER[(i + rp) % 14]) for i in range(len(bits), len(bits) + 14))
        if left + bits + right in s:
            return j
    return 0


if __name__ == "__main__":
    # (a) stability
    for k in range(1, 31):
        bits, rp = rod(k)
        r0, lo, h = run([(bits, rp, 100)], 2002)
        r1 = h.cells(lo, lo + len(r0)) if False else None
        h.goto(2009)
        r7 = h.cells(lo, lo + len(r0))
        ds = vlib.defects(r0)
        assert np.array_equal(r0, r7) and tiles_left(r0) == k, k
    print("(a) S9_k stationary (period 7) and intact at t = 2002, k = 1..30")
    # control: a wrong right phase is NOT a clean rod
    bits, rp = rod(6)
    r0, lo, h = run([(bits, (rp + 1) % 14, 100)], 700)
    print("    control (right phase off by 1): tiles found", tiles_left(r0), "(must not be 6)")
    # (b) reactions at k = 6
    k = 6
    bits, rp = rod(k)
    for g, side in (("A", "L"), ("A^2", "L"), ("A^4", "L"), ("D1", "L"), ("D2", "L"),
                    ("B", "R"), ("B^2", "R"), ("B^3", "R")):
        if g not in vlib.LIB:
            import clib
            clib.ensure(g)
        gb, gp = bits_of(g)
        outs = set()
        for gap in (30, 47, 61):
            objs = [(gb, gp, 100), (bits, rp, gap)] if side == "L" else [(bits, rp, 100), (gb, gp, gap)]
            r, lo, h = run(objs, 1400)
            movers = [n.split("@")[0] for n, x, w, _ in vlib.identify(r, lo)
                      if not n.startswith("?")]
            outs.add((tiles_left(r), tuple(movers), len(vlib.identify(r, lo))))
        print(f"(b) {g} from the {side}: {sorted(outs)}  (tiles left, named objects, #objects; 3 gaps)")
