"""M1 scan: counter E^(v+1), then a DEC-test packet GB3 (designated class),
then a G packet behind it. Zero answer A meets G; in some classes
A + G -> B^2 (catalog). Sweep G's relative placement; for each, simulate
v = 0..4 exactly and type the result with my own typer."""
import sys, json
import vlib, libgen
from collections import Counter
libgen.load()

def E(v):
    return "E" if v == 0 else f"E^{v+1}"

def run(items, T):
    row, org, placed = vlib.build(items, T=T)
    r = vlib.evolve(row, T)
    ids = vlib.identify(r, org, T=T)
    return [(n.split("@")[0], x, w) for n, x, w, k in ids], placed

# 1. designated class for GB3 at zero: t0 values giving E + A
good = []
for t0 in range(42):
    out, _ = run([("E", 0, 0), ("GB3", t0, 30)], 800)
    if [o[0] for o in out] == ["E", "A"]:
        good.append(t0)
print("GB3 t0 with E+A at zero:", good)
t_gb3 = good[0]
T = 1600
res = {}
for dt in range(42):
    for dx in range(40, 200, 14):
        scene = lambda v: [(E(v), 0, 0), ("GB3", t_gb3, 30), ("G", t_gb3 + dt, 30 + dx)]
        try:
            outs = []
            for v in range(0, 5):
                out, placed = run(scene(v), T)
                outs.append(" ".join(o[0] for o in out))
        except ValueError as e:
            continue
        res[(dt, dx)] = outs
        if outs[0].split() in (["E^3"], ["E^2"], ["E^4"]) or "B" in outs[0]:
            print(dt, dx, placed[2], outs, flush=True)
json.dump({f"{k[0]},{k[1]}": v for k, v in res.items()}, open("m1_scan.json", "w"))
c = Counter(v[0] for v in res.values())
print(c.most_common(15))
