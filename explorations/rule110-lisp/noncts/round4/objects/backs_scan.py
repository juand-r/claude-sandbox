"""Non-standard BACK types of an E-rod: does any library left-mover hitting
them launch something that reaches the front?

Backs: (15,-4) interfaces E-bg(phase 0) | ether(phase c) (wallsat), minimal
width <= WMAX, for every right ether phase c. Rod = standard E^N (front +
interior aligned to bg phase 0 by a whole-period shift) with its back
replaced by the back of type c. Each rod alone must be stable (checked);
then each left-mover in NAMES (all time phases) hits the back; front hit =
any cell left of the front line differing from the rod alone, up to T.
Usage: python3 backs_scan.py N T WMAX out.jsonl NAMES_FILE|Bfamily"""
import json
import sys
import numpy as np
import cone
import objlib as O
import wallsat as WS

N, T, WMAX, OUT, NAMES = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
BG = cone.Background(O.EBG)
ETH = O.ETHER
L = O.lib()
if NAMES == "Bfamily":
    names = [n for n, g in L.items() if g["velocity"] == "-1/2"]
elif NAMES == "Gbase":
    names = [n for n, g in L.items() if g["velocity"] == "-1/3" and "@" not in n]
else:
    names = [s.strip() for s in open(NAMES) if s.strip()]
MARGIN, BATCH, GAP = 3, 64, 4


def backs():
    out = {}
    for c in range(14):
        tileR = ETH[c:] + ETH[:c]
        bR = cone.Background(tileR)
        for W in range(2, WMAX + 1, 2):
            m = WS.InterfaceModel(BG, bR, (0, 0), 15, -4, W)
            r = m.solve()
            if r is not None:
                out[c] = (W, r, m.a[0])
                break
    return out


def rod_with_back(c, bk, extra_right=0):
    """row (cells), x0, s_front, back_end column, right ether phase (abs)."""
    b, l, r = O.en_bits(N)
    pad = 2 * T + 400
    row, x0, objs, cR = O.build([("raw", b, l, r, 0, "E")], pad=pad)
    s_front = objs[0][1]
    lb = len(b)
    mid = s_front + lb // 2
    r0 = [q for q in range(10) if all(row[y - x0] == BG.bit(0, y - q) for y in range(mid - 15, mid + 15))]
    assert len(r0) == 1
    W, br, a0 = bk
    target = s_front + lb - 25
    k = (target - a0 - r0[0]) // 10
    shift = r0[0] + 10 * k
    bs = a0 + shift
    scene = row.copy()
    for y in range(mid, bs):
        scene[y - x0] = BG.bit(0, y - shift)
    scene[bs - x0:bs + W - x0] = br
    # right ether: bg coords ether tile rotated by c: cell x reads ETHER[(x + c)]
    for y in range(bs + W, x0 + len(row)):
        scene[y - x0] = O.EB[(y - shift + c) % 14]
    c_abs = (c - shift) % 14            # absolute phase of the right ether
    return scene, x0, s_front, bs + W, c_abs


def add_glider(scene, x0, back_end, c_abs, name, kg):
    """place library glider phase kg right of back_end (gap >= GAP)."""
    bits, lph, rph, off = L[name]["phases"][kg]
    s = back_end + GAP
    while (lph - s) % 14 != c_abs % 14:
        s += 1
    out = scene.copy()
    bb = np.array([int(ch) for ch in bits], np.uint8)
    out[s - x0:s - x0 + len(bb)] = bb
    c2 = (rph - s) % 14
    for y in range(s + len(bb), x0 + len(scene)):
        out[y - x0] = O.EB[(c2 + y) % 14]
    return out


if __name__ == "__main__":
    B = backs()
    print(f"back types (right ether phase c): {sorted(B)}", flush=True)
    for c, bk in sorted(B.items()):
        scene, x0, s_front, be, c_abs = rod_with_back(c, bk)
        # stability of the rod alone: (300,-80) periodic after 300 steps
        a = O.evolve(scene, 300); b2 = O.evolve(a, 300)
        xs = np.arange(x0 + 300 + 320, x0 + 300 + len(a) - 320)
        stable = bool(np.array_equal(a[xs - (x0 + 300)], b2[xs - 80 - (x0 + 600)]))
        jobs = [(n, k) for n in names for k in range(L[n]["p"])]
        hits = []
        for b0 in range(0, len(jobs), BATCH):
            batch = jobs[b0:b0 + BATCH]
            A = np.stack([add_glider(scene, x0, be, c_abs, n, k) for n, k in batch] + [scene])
            first = [None] * len(batch)
            for t in range(1, T + 1):
                A = ((A[:, 1:-1] | A[:, 2:]) & (1 - (A[:, :-2] & A[:, 1:-1] & A[:, 2:]))).astype(np.uint8)
                hi = s_front + (-4 * t) // 15 + MARGIN - (x0 + t)
                if hi <= 0:
                    continue
                d = (A[:-1, :hi] != A[-1, :hi]).any(axis=1)
                for i in np.nonzero(d)[0]:
                    if first[i] is None:
                        first[i] = t
            hits += [(n, k, f) for (n, k), f in zip(batch, first) if f is not None]
        rec = {"N": N, "T": T, "back_c": c, "back_W": bk[0], "rod_stable": stable,
               "scenes": len(jobs), "front_hits": len(hits), "examples": hits[:10]}
        print(json.dumps(rec), flush=True)
        with open(OUT, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
