import sys
from splice import *
T = 16000
A0 = "HIIJIJIJIJIJ"
REST = "HIIJIJIJIJIJK" * 2
variants = {"std": A0 + "K" + REST, "G": A0 + "G" + REST, "L": A0 + "L" + REST,
            "KK": A0 + "KK" + REST, "LK": A0 + "LK" + REST, "KL": A0 + "KL" + REST,
            "GK": A0 + "GK" + REST, "EDK": A0 + "EDK" + REST, "FDK": A0 + "FDK" + REST,
            "DK": A0 + "DK" + REST, "HK": A0 + "HK" + REST, "IK": A0 + "IK" + REST}
for name, seq in variants.items():
    for tape in ("YN", "NY"):
        try:
            m = Machine(tape, None, T, right_names=seq)
        except Exception as e:
            print(name, tape, "assembly fails:", e); break
        kpos = [a for n, a, b in m.blocks if n in "KGLEDFHI" and a > 3500][0]
        cs = m.run(m.row, T, 1100, 8000)
        print(name, tape, kpos, sum(1 for x, y, k in cs if x < kpos and k == "E"),
              sum(1 for x, y, k in cs if x >= kpos and k == "E"),
              [f"{k}{x}" for x, y, k in cs if k != "E"], flush=True)
