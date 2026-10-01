"""Independent survey (my builder + my typer + exact engine): every
right-moving or stationary library object L placed LEFT of a counter E^n,
over all seed phases t0 < P_L and 14 consecutive x offsets (snapped), so all
collision classes are covered (each class appears several times; repeated
classes must give the same outcome - a built-in consistency check).
Also E^n + Bbar from the right, and C3 + B.
Usage: python3 survey_left.py [T]"""
import sys
from collections import defaultdict
import v3

T = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
LEFT = ["A", "A^2", "A^3", "A^4", "D1", "D2", "C1", "C2", "C3"]
COUNTERS = ["E", "E^2", "E^3", "E^4", "E^5", "E^6"]
GAP = 70


def survey(L, R, side="left"):
    out = defaultdict(list)
    seen = set()
    P = v3.LIB[L].P
    for t0 in range(P):
        for dx in range(14):
            if side == "left":
                items = [(L, t0, -GAP - dx), (R, 0, 0)]
            else:
                items = [(R, 0, 0), (L, t0, GAP + dx)]
            objs, r, org, placed = v3.run(items, T)
            key = tuple((p[1], p[2]) for p in placed)
            if key in seen:
                continue
            seen.add(key)
            out[" + ".join(v3.names(objs))].append((t0, dx))
    return out


if __name__ == "__main__":
    for R in COUNTERS:
        for L in LEFT:
            res = survey(L, R)
            print(f"{L} + {R}: " + " | ".join(
                f"{k} x{len(v)}" for k, v in sorted(res.items(), key=lambda kv: -len(kv[1]))),
                flush=True)
    for R in COUNTERS:
        res = survey("Bbar", R, side="right")
        print(f"{R} + Bbar(right): " + " | ".join(
            f"{k} x{len(v)}" for k, v in sorted(res.items(), key=lambda kv: -len(kv[1]))), flush=True)
    res = survey("C3", "B")
    print("C3 + B: " + " | ".join(f"{k} x{len(v)}" for k, v in res.items()))
