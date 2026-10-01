"""Several R2 -> R1 signals in a row.  Fixed left program Z^4 (built on
R2 = 0 alone, t1z_ZZZZ.json).  Inputs: R2 = y via B's?  No: R2 = E always,
and the left program prefix decides how many Z's fire at zero; instead we
vary R1 = m (GB5's) and use only the first k Z's (k = 1..4), all at zero.
For each R1 phase t1 (15), report outcomes.  Clean = R2 = E, R1 = m - k."""
import sys, json
from collections import defaultdict
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()
D = 600
slots = [tuple(s) for s in json.load(open("t1z_ZZZZ.json"))["slots"]]


def run(k, m, t1):
    prog = [(L.OPS[o], t, x) for o, t, x in slots[:k]][::-1]
    right = [("E", 0, 0), ("E", t1, D)]
    for j in range(m):
        right += AC.parts("I", t1, D + 150 + 110 * j)
    items = prog + right
    c0 = (L.C_E - sum(vlib.LIB[n].w for n, _, _ in prog)) % 14
    T = 15 * (D + 150 + 110 * m) + 9000
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return " + ".join(v3.base(n) for n, x, w, k_ in vlib.identify(r, org, T=T))


if __name__ == "__main__":
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    for k in range(1, 5):
        out = defaultdict(list)
        for t1 in range(15):
            out[run(k, m, t1)].append(t1)
        print(f"k={k} R1={m}: " + " | ".join(f"{o} {v}" for o, v in out.items()), flush=True)
