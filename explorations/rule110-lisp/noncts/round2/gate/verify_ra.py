"""Exact-CA verification of a FIXED program (rafast conventions):
the program text is placed once (Program().add per slot, classes given);
input v = E at (0,0) + v GB5's (stream.build rule); the program is shifted in
x only (rafast.shift_for: same t = 0 text) to sit after the input.
python verify_ra.py PROGRAM CLASSES VMIN VMAX [--control SLOT:CLASS]"""
import sys
import common  # noqa: F401
from rafast import Program, input_prefix, shift_for
from stream import run, counter_of, ca_only
from glidersim import ThreeBody
from test_prog import OPS

prog = sys.argv[1]
cls = [int(c) for c in sys.argv[2].split(",")]
vmin, vmax = int(sys.argv[3]), int(sys.argv[4])
if "--control" in sys.argv:
    a, b = sys.argv[sys.argv.index("--control") + 1].split(":")
    cls[int(a)] = int(b)
    print("CONTROL: slot", a, "class changed to", b)
P = Program()
for op, c in zip(prog, cls):
    P.add(op, c)
print("program items:", P.items)
allok = True
for v in range(vmin, vmax + 1):
    exp = v
    for c in prog:
        exp = OPS[c](exp)
    pre = input_prefix(v)
    D = shift_for(pre, P.items[0])
    scene = pre + [(n, t, x + D) for n, t, x in P.items]
    try:
        st, log, ok = run(scene, ca="fast")
        vals, other = counter_of(st)
        good = vals == [exp] and ok and all(o.startswith("Bbar") for o in other)
        print(f"v={v}: model {exp} got {vals} garbage {other} CA==sim {ok} {'OK' if good else 'BAD'}", flush=True)
    except ThreeBody as e:
        names, settled = ca_only(scene)
        good = False
        print(f"v={v}: model {exp}; glidersim 3-body; exact CA final objects {names} BAD", flush=True)
    allok &= bool(good)
print("ALL OK" if allok else "FAILED")
