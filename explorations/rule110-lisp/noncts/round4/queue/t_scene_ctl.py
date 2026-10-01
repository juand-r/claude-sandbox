"""Control: local scene reproduces the full machine window."""
import time
from lscene import *
tape = "NYYN"; t_in = 30000; T = 3000
m = Machine(tape, ["YNNNNN"], t_in + T + 500, left_periods=3, right_periods=2)
K0 = [a for n, a, b in m.blocks if n == "K"][0]
t0 = time.time()
sc = Scene(m, m.row, t_in, K0 - 1000, K0 + 1000, 3200)
print("cut", time.time() - t0)
t0 = time.time()
w = sc.run(sc.seg, T)
print("run", time.time() - t0)
r = Run(m.row, m.origin); r.step(t_in + T)
sh = r.ebar_frame()
full = r.window(K0 - 1000 + sh, K0 + 1000 + sh)
print("diff vs full machine:", int((w != full).sum()))
# negative control: one flipped cell near P
seg2 = sc.seg.copy(); seg2[sc.ebar_to_seg(K0 + 45)] ^= 1
w2 = sc.run(seg2, T)
print("flipped-cell control diff:", int((w2 != full).sum()))
