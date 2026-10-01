"""CLAIM [sim]: INC of the E^n counter from the LEFT by one right-moving
(3,2) train (slip 6), n = 1..NMAX, in exact Rule 110; plus controls.
Train = SAT record 6 of sat_inc_results.jsonl (cells below, left ether
phase 0 at x = 0, time 0). E at collider seed (7, 44); E^n = E + (n-1) B's
from the right (B x E^n is single-class; B's are absorbed before the train
arrives). Train moved left by m * (15,-4) (same class, later arrival).
Writes inc_scenes.json (exact rows) for independent re-checks.
Controls: the train shifted by (1,-4) and (2,-8) (other two classes)."""
import json
import sys
from lsl import embed, parse_row, nval, names, export, run_exported
from ops import scene, shifted
from disp import disp, cls

TRAIN_BITS = "111110111110111110001110"


def train_seeds():
    row, x0 = embed(TRAIN_BITS + "1110001001101111100011110000110111", 0, 0, 1)
    ok, prods = parse_row(row, x0)
    tr = [p for p in prods if not nval(p[0])]
    E = [p for p in prods if nval(p[0])]
    assert len(tr) == 1 and E == [("E", 7, 44)], prods
    return tr, (7, 44)


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    tr, e0 = train_seeds()
    scenes = []
    fails = 0
    for j in range(3):
        for n in range(1, nmax + 1):
            pk = shifted(tr, j)
            pl, m = scene(pk, e0, n)
            T = 15 * m + 60 * n + 600
            # store the train as raw cells: export uses library states
            sc = export(pl, T, expect=f"E^{n+1}" if j == 0 else "control",
                        note=f"class shift {j}, n = {n}")
            ok, out = run_exported(sc)
            good = ok and len(out) == 1 and nval(out[0][0]) == n + 1
            if j == 0:
                d = disp(e0, n + 1, out[0][1:]) if good else None
                print(f"INC n={n}: {names(out)} ok={good} disp={d} key={cls(d) if d else None}")
                fails += not good
            else:
                print(f"control shift {j} n={n}: {names(out)} (INC: {good})")
            sc["result"] = names(out)
            scenes.append(sc)
    json.dump(scenes, open("inc_scenes.json", "w"))
    print("INC failures:", fails)
