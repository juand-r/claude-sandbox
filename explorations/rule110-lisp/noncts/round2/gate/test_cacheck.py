"""ca_check (fast exact window) must agree with the full-row engine check,
and must FAIL against a wrong prediction (negative control)."""
import time
from common import LIB
from glidersim import GliderSim
from stream import build, run, horizon, ca_check

for v in (0, 2):
    sc = build(["I"] * v + ["Z"] * 2)
    t = time.time()
    st, log, ok_full = run(sc, ca=True)
    t1 = time.time() - t
    t = time.time()
    st2, log2, ok_fast = run(sc, ca="fast")
    t2 = time.time() - t
    print(f"v={v} full engine: {ok_full} ({t1:.0f}s)  fast window: {ok_fast} ({t2:.0f}s)  final {st}")
# negative control: CA of scene v=0 against glidersim of a DIFFERENT scene
sc0 = build(["Z"] * 2)
sc1 = build(["I"] + ["Z"] * 2)
T = max(horizon(sc0), horizon(sc1))
sim1 = GliderSim(LIB, sc1)
sim1.run(T)
print("control (wrong prediction) accepted?", ca_check(sc0, sim1, T))
