"""Independent check of leftstream 05:45/05:46: zero test Z from the left,
Z = 111110111110111000111011 (slip 8): Z + E^n -> E^(n-1) (n >= 2),
Z + E -> E + A (A leaves right), one class.  And their rigid stream
ZIZZIDIIDIIZZDZZ (exported rows, v = 0..8) + control rows.
A: their exported stream rows -> engine -> MY typer, vs their 'expect'.
B: my construction for Z alone (my E^n, Z pasted at 3 phases x 4 offsets)."""
import json
import numpy as np
import verify_inc as VI
import v3, vlib, engine

VI.TR = np.array([int(c) for c in "111110111110111000111011"], np.uint8)


def train_at(r):
    pad = 60
    row = np.concatenate([VI.ether(0, -pad, 0), VI.TR, VI.ether(8, 24, 24 + pad)])
    for _ in range(r):
        row = vlib.step(row)
    cut = r + 2
    row = row[cut:len(row) - cut]
    d = vlib.defects(row)
    return row[d[0]["lo"]:d[-1]["hi"]], -pad + cut + d[0]["lo"], (4 * r) % 14


VI.train_at = train_at
_orig_scene = VI.my_scene


def my_scene(n, r, k):
    # same as verify_inc.my_scene but with slip 8
    nm = "E" if n == 1 else f"E^{n}"
    pad = 2 * VI.T + 200
    erow, eorg, placed = vlib.build_right([(nm, 0, 0)], c_right=0, pad=pad)
    c_mid = (0 - vlib.LIB[nm].w) % 14
    cells, xc, c_tr = train_at(r)
    X = (c_tr + 8 - c_mid) % 14 - 14 * (12 + k)
    a = xc + X
    row = erow.copy()
    i = a - eorg
    row[:i] = VI.ether((c_tr - X) % 14, eorg, a)
    row[i:i + len(cells)] = cells
    assert np.array_equal(row[i + len(cells):i + len(cells) + 20],
                          VI.ether(c_mid, a + len(cells), a + len(cells) + 20))
    return row, eorg, a


VI.my_scene = my_scene


def part_A(fn):
    sc = json.load(open(fn))
    bad = 0
    for s in sc:
        bits = np.array([int(c) for c in s["bits"]], np.uint8)
        pad = 2 * s["T"] + 200
        x0 = s["x0"]
        row = np.concatenate([VI.ether(s["cL"], x0 - pad, x0), bits,
                              VI.ether(s["cR"], x0 + len(bits), x0 + len(bits) + pad)])
        got = [n for n, x in VI.run_typed(row, x0 - pad, s["T"])]
        e = s["expect"]
        want = ["E" if e["value"] == 0 else f"E^{e['value'] + 1}"] + ["A"] * e["answers_right"]
        ok = got == want
        bad += not ok
        print(f"A {s['note'][:60]:60s} mine={got} want={want} ok={ok}")
    return bad


if __name__ == "__main__":
    b1 = part_A("../leftstream/stream_ZIZZIDIIDIIZZDZZ.json")
    print("stream rows mismatching their expectation:", b1)
    b2 = part_A("../leftstream/stream_ZIZZIDIIDIIZZDZZ_ctl3_1.json")
    print("control rows mismatching expectation (must be > 0):", b2)
    VI.NMAX = 9
    res = VI.part_B()
    for n in range(1, 10):
        want = ["E", "A"] if n == 1 else (["E"] if n == 2 else [f"E^{n - 1}"])
        good = sorted(rk for rk, g in res[n].items() if g == want)
        byr = {r: sorted(set(tuple(res[n][(r, k)]) for k in range(4))) for r in range(3)}
        print(f"B n={n}: want {want}: placements {good}; by r {byr}")
