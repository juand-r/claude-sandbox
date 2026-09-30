"""M1 search: [GB3 test][G conv at (dt=35, dx=54) from m1_scan][X collector].
Want: every v in 0..4 ends with ONLY a counter E^m (no garbage), and
m(v) is not of the form v + const (a genuine branch)."""
import vlib, libgen, sys
libgen.load()
def E(v): return "E" if v == 0 else f"E^{v+1}"
def val(nm):
    if nm == "E": return 0
    if nm.startswith("E^"): return int(nm[2:]) - 1
    return None
T = 4200
TG = 1  # t_gb3 from m1_scan
base = lambda v: [(E(v), 0, 0), ("GB3", TG, 30), ("G", TG + 35, 30 + 54)]
hits = []
for X in sys.argv[1].split(","):
    for dt in range(42):
        for dx in range(28, 170, 14):
            outs = []
            ok = True
            for v in range(0, 5):
                try:
                    row, org, placed = vlib.build(base(v) + [(X, TG + 35 + dt, 30 + 54 + dx)], T=T)
                except ValueError:
                    ok = False; break
                r = vlib.evolve(row, T)
                ids = [n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T)]
                outs.append(ids)
                if len(ids) != 1 or val(ids[0]) is None:
                    ok = False
                    if v <= 2: break
            if ok:
                ms = [val(o[0]) for o in outs]
                print(X, dt, dx, placed[-1], ms, flush=True)
                hits.append((X, dt, dx, ms))
print("hits", len(hits))
