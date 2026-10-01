"""Theory 06:29 first test: does ANY co-moving object parked at R2's back
turn an arriving wall (launched by I_L or Z_L at the front) into an
outgoing glider?  Co-moving objects tried: Ebar and E (both velocity
-4/15) at every phase and several gaps behind E^n.  For each placement:
(1) without the front op the pair must be stable (outcome = rod + object
unchanged); (2) with the front op in its clean class, report any outcome
other than the expected (rod +-1, object unchanged)."""
import sys
from collections import defaultdict
import t1lib as L
import v3, vlib, engine
L.register_IL()

T = 2500
GAPS = range(int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else range(30, 90, 4)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 8


def clean_front(P, n, want):
    for t0 in range(3):
        for dx in range(14):
            items = [(P, t0, -60 - dx), (f"E^{n}", 0, 0)]
            objs, r, org, placed = v3.run(items, T)
            if v3.names(objs) == want:
                return (P, t0, -60 - dx)
    return None


if __name__ == "__main__":
    fronts = {"IL": clean_front("IL", N, [f"E^{N + 1}"]), "ZL": clean_front("ZL", N, [f"E^{N - 1}"])}
    print("front ops:", fronts)
    res = defaultdict(list)
    for obj in ("Ebar", "E"):
        P = vlib.LIB[obj].P
        for t0 in range(P):
            for gap in GAPS:
                base_items = [(f"E^{N}", 0, 0), (obj, t0, gap)]
                try:
                    o0, *_ = v3.run(base_items, T)
                except ValueError:
                    continue
                if v3.names(o0) != [f"E^{N}", obj]:
                    continue                      # not a stable parked pair
                for fn, f in fronts.items():
                    o1, *_ = v3.run([f] + base_items, T)
                    nm = v3.names(o1)
                    exp = [f"E^{N + 1}" if fn == "IL" else f"E^{N - 1}", obj]
                    if nm != exp:
                        res[(fn, obj, " + ".join(nm))].append((t0, gap))
    for k, v in sorted(res.items(), key=lambda kv: -len(kv[1])):
        print(k, len(v), v[:6])
