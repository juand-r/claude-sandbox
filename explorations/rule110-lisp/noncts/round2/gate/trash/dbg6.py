import sys
from fastsearch import Run
prog = sys.argv[1]; cls = [int(c) for c in sys.argv[2].split(",")]; vmax = int(sys.argv[3])
for v in range(vmax + 1):
    r = Run(v)
    for op, c in zip(prog, cls):
        r.add(op, c)
    out = []
    for c in range(3):
        r2, ok = r.trial(prog[len(cls)], c)
        out.append((c, ok, r2.val, [g[0] for g in r2.sim.state() if not g[0].startswith("Bbar")], r2.sim.log[-1][2:] if r2.sim.log else None))
    print(v, "val before", r.val, out)
