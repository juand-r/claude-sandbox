"""Exact-CA verification of a fixed program found by adaptive.py:
python verify_classes.py PROGRAM CLASSES(comma list) VMAX
For each input v (prefix of v GB5's), build with adaptive.build (same class
list for every v), run glidersim + exact moving-window CA, compare."""
import sys
import common  # noqa: F401
from adaptive import build
from stream import run, counter_of, ca_only
from glidersim import ThreeBody
from test_prog import OPS

prog = sys.argv[1]
cls = [int(c) for c in sys.argv[2].split(",")]
vmax = int(sys.argv[3])
allok = True
for v in range(vmax + 1):
    exp = v
    for c in prog:
        exp = OPS[c](exp)
    sc = build(["I"] * v + list(prog), [0] * v + cls)
    try:
        st, log, ok = run(sc, ca="fast")
    except ThreeBody as e:
        names, settled = ca_only(sc)
        print(f"v={v}: model {exp}; glidersim 3-body ({str(e)[:50]}); exact CA final objects: {names} (settled {settled}) BAD", flush=True)
        allok = False
        continue
    vals, other = counter_of(st)
    good = vals == [exp] and ok
    allok &= bool(good)
    print(f"v={v}: model {exp} got {vals} garbage {other} CA==sim {ok} {'OK' if good else 'BAD'}", flush=True)
print("ALL OK" if allok else "FAILED")
