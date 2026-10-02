"""All 12 face-free C-stack variants x small gliders from both faces (srod.run),
k = 6 and 7, every time phase. Prints per (variant, glider) the distinct
outcomes (dk, stationary, movers)."""
import json, sys
import srod
SR = srod.SR
left = ["A", "A^2", "A^3", "A^4", "A^5", "D1", "D2"]
right = ["B", "B^2", "B^3", "Bbar", "Bhat", "G", "E", "Ebar", "F"]
L = srod.O.lib()
for tile, sols in SR.items():
    for idx in range(len(sols)):
        for side, names in (("L", left), ("R", right)):
            for name in names:
                outs = {}
                for k in (6, 7):
                    for kg in range(L[name]["p"]):
                        r = srod.run(tile, idx, side, k, 500, name, kg)
                        key = (r["dk"], r["stationary"], tuple(r["movers"]))
                        outs.setdefault(key, set()).add(k)
                clean = [list(k) for k in outs if k[1] and len(k[2]) <= 1]
                print(json.dumps({"tile": tile, "idx": idx, "side": side, "g": name,
                                  "n_outcomes": len(outs), "outcomes": [list(k) + [sorted(v)] for k, v in outs.items()][:6]}), flush=True)
