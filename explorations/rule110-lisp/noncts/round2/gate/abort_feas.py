"""Catalog-level feasibility of an abort on address's fixed-stream lane:
a stationary C1 at seed s (upstream of T) meets the movers of each padded
instruction (address/fixed_stream.STD); for each C1 position class, does
every mover get EATEN (C1 + mover -> C1), or pass/convert and then cross
T, M, P cleanly (catalog prediction, gen.cross with ABSORB)?
Prints, per C1 placement (t in 0..6, x offset), the fate of every mover."""
import os
import sys
ADDR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "address")
sys.path.insert(0, ADDR)
_cwd = os.getcwd()
os.chdir(ADDR)
import fixed_stream as FS  # noqa: E402
import gen  # noqa: E402
os.chdir(_cwd)
gen.ABSORB = True

prog = sys.argv[1].split(",") if len(sys.argv) > 1 else ["DN1", "UP1", "DN2", "UP2"]
pl = FS.build(prog)
F0 = [p for p in pl if p[0] == "F"]
movers = [p for p in pl if p[0] != "F"]
T = F0[0][1:]
print("T seed", T, "movers", len(movers))
summary = {}
for dt in range(7):
    for dx in range(0, 56):
        s = (T[0] + dt, T[1] + 300 + dx)
        fates = []
        c1 = s
        ok = True
        for mv in movers:
            r = gen.cross("C1", c1, mv)
            if r is None:
                fates.append("X")
                ok = False
                break
            c1, outs = r
            fates.append("E" if not outs else "P")
        if fates and fates[0] != "X" or len(fates) > 1:
            key = "".join(fates)
            summary.setdefault(key, []).append((dt, dx))
for k, v in sorted(summary.items(), key=lambda kv: -kv[0].count("E")):
    print(len(k), "eaten", k.count("E"), "passed", k.count("P"), "fate", k[:60], "C1 offsets e.g.", v[:3])
