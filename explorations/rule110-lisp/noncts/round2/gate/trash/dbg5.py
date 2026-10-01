from fastsearch import Run
for v in range(2):
    r = Run(v)
    print(v, r.val, r.sim.state(), r.broken)
    for c in range(3):
        r2, ok = r.trial("J", c)
        print("  c", c, ok, r2.val, r2.sim.state(), r2.broken, r2.sim.log[-1:])
