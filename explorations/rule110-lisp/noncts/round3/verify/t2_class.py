"""Does the clean R1 -> R2 coupling class depend on R2's value history?
R2 = E at (0,0) operated by a prefix of a fixed left program (t1_<WORD>.json,
first m ops), R1 = E (value 0) at (t1, D), then J and I (gate packets) with
gate's J-at-zero geometry relative to R1.  Phases left of R2 are fixed
(t1lib anchoring), so R1/J/I sit at the same cells for every m.
For each m, report the outcome for t1 = 0..14 (all 3 classes x 5)."""
import sys, json
from collections import defaultdict
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()   # adaptive_ca reloads the library (libgen.load clears it)

word = sys.argv[1]
D = int(sys.argv[2]) if len(sys.argv) > 2 else 600
slots_all = [tuple(s) for s in json.load(open(f"t1_{word}.json"))["slots"]]


def run(m, t1):
    slots = slots_all[:m]
    prog = [(L.OPS[o], t, x) for o, t, x in slots][::-1]
    right = [("E", 0, 0), ("E", t1, D)] + AC.parts("J", 5 + t1, D + 447) + AC.parts("I", 5 + t1, D + 447 + 110)
    items = prog + right
    c0 = (L.C_E - sum(vlib.LIB[n].w for n, _, _ in prog)) % 14
    T = 15 * (D + 700) + 6 * D + 4000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    objs = [v3.base(n) for n, x, w, k in vlib.identify(r, org, T=T)]
    return " + ".join(objs), placed[len(prog):len(prog) + 3]


if __name__ == "__main__":
    for m in range(len(slots_all) + 1):
        v = sum(1 if o == "I" else -1 for o, _, _ in slots_all[:m])
        out = defaultdict(list)
        pl = None
        for t1 in range(15):
            o, p = run(m, t1)
            out[o].append(t1)
            if t1 == 0:
                pl = p
        print(f"m={m:2d} R2 value {v}: " + " | ".join(f"{k} {v_}" for k, v_ in out.items()) + f"   R2/R1/J seeds {pl}", flush=True)
