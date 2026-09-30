"""Independent check of collider's F read-and-reset gadget (BOARD 06:40):
idle cell C2 + F -> C2 + F (crossing); set cell (C1 made by an A from the
left) + same F -> C2 + Ebar, with the restored C2 at the SAME place and
phase in both cases."""
import numpy as np
import r110check as r, locate as L

T = 1600
hits = 0
for fph in [k for k in r.PHASES if k.startswith("F(")]:
    for n in (8, 9):
        idle = f"C2(A,f1_1)-{n}e-{fph}"
        sett = f"A(f1_1)-12e-C2(A,f1_1)-{n}e-{fph}"
        ri, si = r.build(idle, pad=260); rs, ss = r.build(sett, pad=260)
        hi = r.evolve(ri, T); hs = r.evolve(rs, T)
        # C2 position in both, relative to the C2's original start column
        c2_start_i = si
        c2_start_s = ss + len(r.PHASES["A(f1_1)"]) + 14 * 12
        oi = [o[2] for o in r.objects(hi, T, 1700, len(ri) - 1700)]
        os_ = [o[2] for o in r.objects(hs, T, 1700, len(rs) - 1700)]
        if sorted(oi) != ["C2", "F"]:
            continue
        ci = L.find(hi, T - 7, "C2", si - 100, si + 200)
        cs = L.find(hs, T - 7, "C2", c2_start_s - 100, c2_start_s + 200)
        ci = [(t, x - c2_start_i) for t, x in ci]
        cs = [(t, x - c2_start_s) for t, x in cs]
        same = ci == cs
        hits += 1
        print(f"{fph:12s} n={n} idle:{oi} set:{os_} C2 idle {ci} set {cs} "
              f"{'SAME CELL' if same else 'different'}")
print("idle-crossing configurations:", hits)
