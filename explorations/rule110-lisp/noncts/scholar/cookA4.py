"""Cook's A4 (from the ossifier in an assembled Cook row) versus Ebar, all
6 collision classes. Checks the claim 'A4 + Ebar -> C2 in all 6 classes'
against Cook 2009 fig. 6(e,f): 3 classes give C2, 'up 0' is a crossing."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from collections import defaultdict
import numpy as np
import encoder as E, census, r110check as r
from engine import ETHER, parse, step, show


def cook_a4():
    row, _ = E.assemble("YN", ["YYYYNN"], left_periods=1, right_periods=1)
    h = [np.asarray(row, dtype=np.uint8)]
    for _ in range(40):
        h.append(step(h[-1]))
    h = np.array(h)
    cs = [c for c in census.census(h[-31:]) if c[2] == "A" and c[0] > 1000]
    a, b, _ = cs[2]
    snip = h[-1][a - 70:b + 70]
    ph = census.ether_phase(snip)
    return snip, int(ph[0]), int(ph[len(snip) - 14])   # left/right abs phase at 0


def compose(snip, rph, n, yname, pad=300):
    """snip + ether up to a tile boundary + n tiles + Y string + ether."""
    s = "".join(map(str, snip))
    L = len(s)
    k = (-(rph + L)) % 14            # cells until (rph + y) % 14 == 0
    right = "".join(ETHER[(rph + L + i) % 14] for i in range(k))
    lph = None
    body = s + right + ETHER * n + r.PHASES[yname]
    # left ether: must continue snip's left ether leftwards
    return body


def main():
    snip, lph, rph = cook_a4()
    print("A4 snippet:", show(snip))
    # prepend/append ether consistent with snip's phases
    res = defaultdict(set)
    for y in [k for k in r.PHASES if k.startswith("E-(")]:
        for n in (6, 7):
            body = compose(snip, rph, n, y)
            # left pad: ether with phase lph at snip start
            left = "".join(ETHER[(lph - 14 * 300 + i) % 14] for i in range(14 * 300))
            full = parse(left + body + ETHER * 300)
            h = r.evolve(full, 1400)
            lo, hi = 1500, len(full) - 1500
            obj = [o[2] for o in r.objects(h, 1400, lo, hi)]
            obj2 = [o[2] for o in r.objects(h, 1250, lo, hi)]
            key = (y, n)
            res[tuple(sorted(obj)) + (() if obj == obj2 else ("UNSETTLED",))].add(key)
    for k, v in res.items():
        print(len(v), k, sorted(v)[:3])


if __name__ == "__main__":
    main()
