"""Is the debris the culprit? Forced-N Z at t_in, then at t2 = t_in + 3000
replace the Ebar-frame region [K0-400, K0+100) by the plain N-read
machine's cells (tape NNYY at the same time) -> later reads correct?
    python t_forced2.py NREAD k2 x2 k1 x1"""
import sys
from reads import *
nread = int(sys.argv[1]); k2, x2, k1, x1 = map(int, sys.argv[2:6])
tape, apps = "NYYN", ["YNNNNN"]
E = ebar_tiles()
v = enc._left_v(apps); T = (nread + 3) * 2 * 30 * v
# plain-N donor (tape NNYY) window at t2
t_in, t2 = 31500, 34500
md = Machine("NNYY", apps, T, v=v, left_periods=T // (30 * v) + 3, right_periods=nread + 3)
K0d = [a for n, a, b in md.blocks if n == "K"][0]
rd = Run(md.row, md.origin); rd.step(t2)
shd = rd.ebar_frame()
donor = rd.window(K0d - 400 + shd, K0d + 100 + shd).copy()
m = Machine(tape, apps, T, v=v, left_periods=T // (30 * v) + 3, right_periods=nread + 3)
K0 = [a for n, a, b in m.blocks if n == "K"][0]
regs = regions_of(m, nread)
for clean in (False, True):
    r = Run(m.row, m.origin); r.step(t_in)
    row = rewrite(r.window(0, r.width), m.origin, t_in, K0 - 345, K0 + 37,
                  [(E, k2, K0 + x2), (E, k1, K0 + x1)])
    r = Run(row, m.origin); r.t = t_in
    r.step(t2 - t_in)
    if clean:
        row = r.window(0, r.width).copy(); sh = r.ebar_frame()
        row[K0 - 400 + sh:K0 + 100 + sh] = donor
        r = Run(row, m.origin); r.t = t2
    got, times = outcomes(r, regs, T, [6] * nread)
    ref = reference(tape, apps, "KF" + "K" * nread, nread)
    print("debris removed" if clean else "debris kept", got, ref, times, flush=True)
# phase check of the transplant seams
r = Run(m.row, m.origin); r.step(t_in)
row = rewrite(r.window(0, r.width), m.origin, t_in, K0 - 345, K0 + 37, [(E, k2, K0 + x2), (E, k1, K0 + x1)])
r = Run(row, m.origin); r.t = t_in; r.step(t2 - t_in)
row = r.window(0, r.width); sh = r.ebar_frame()
a, b = K0 - 400 + sh, K0 + 100 + sh
print("target phases L,R", phase_at(row, a - 14), phase_at(row, b), "donor L,R",
      phase_at(np.concatenate([row[a-14:a], donor]), 0) , "...")
from census import clusters
print("target clusters", [(x - a, y - a) for x, y in clusters(row[a - 50:b + 50])])
print("donor clusters", clusters(donor))
