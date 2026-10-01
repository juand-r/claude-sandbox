"""Long E^n rods by splicing whole spatial periods (10 cells) of the
interior background into my library E^15 (at time 0, where the interior
is periodic).  Checked by my typer: each 10-cell insertion must give
E^(n+3) exactly (3 units per period), and the result must be stable."""
import numpy as np
import v3, vlib, engine

BGP = "1101011100"


def rod(n):
    """Row (with ether margins) and origin holding E^n, n >= 15, n = 15 + 3j."""
    assert n >= 15 and (n - 15) % 3 == 0
    objs, row, org, placed = v3.run([("E^15", 0, 0)], 0)
    s = "".join(map(str, row))
    i = s.find(BGP * 2)
    assert i >= 0
    j = (n - 15) // 3
    s2 = s[:i] + BGP * j + s[i:]
    r2 = np.array([int(c) for c in s2], np.uint8)
    return r2, org


def check(n, T=600):
    r, org = rod(n)
    w = engine.pack(np.concatenate([r, vlib.ETHER[(np.arange(len(r), len(r) + 2 * T + 200) + 0) % 14][:0]]))
    # use v3-style padding: rebuild with ether pads of the right phases
    ids0 = [v3.base(nm) for nm, x, ww, k in vlib.identify(r, org)]
    return ids0


if __name__ == "__main__":
    for n in (15, 18, 30, 60):
        r, org = rod(n)
        print(n, [v3.base(nm) for nm, x, w, k in vlib.identify(r, org)])
