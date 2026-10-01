"""Generic version of verify_gate_ra.py for any gate rafast program:
python verify_gate_ra2.py PROGRAM CLASSES VMIN VMAX
Model from gate's test_prog.OPS (read-only); scenes from rafast; my
translation + exact engine + typer; stability T vs T+3000 on the first and
last input only (long runs)."""
import os, sys
import verify_gate_ra as G
sys.path.insert(0, G.GATE)
from test_prog import OPS     # noqa: E402

prog, cls = sys.argv[1], [int(c) for c in sys.argv[2].split(",")]
vmin, vmax = int(sys.argv[3]), int(sys.argv[4])
sc = G.scenes(prog, cls, range(vmin, vmax + 1))
items0 = sc[vmin][2]
print("program items identical for all inputs:", all(s[2] == items0 for s in sc.values()), flush=True)
ok = True
for v in range(vmin, vmax + 1):
    exp = v
    for c in prog:
        exp = OPS[c](exp)
    ids = G.run(sc[v][0])
    stable = True
    if v in (vmin, vmax):
        stable = ids == G.run(sc[v][0], extra=3000)
    rest = [i for i in ids if i != "Bbar"]
    got = G.value(rest)
    good = got == exp and stable
    ok &= good
    print(f"v={v}: {sorted(set(ids))} value {got} model {exp} stable {stable} {'OK' if good else 'BAD'}", flush=True)
print("REPRODUCED" if ok else "NOT REPRODUCED")
