"""Zero-test search by full simulation: which single movers behave
DIFFERENTLY on reg1 = gap(T,M) at its smallest legal gap than at larger
gaps of the same residue? Markers T=(0,0), M=-D1, P=M-D2 (reg2 large).
D1 in {R1+8PE (25.9 cells), R1+4PE (44.6), R1 (63.2), R1-4PE (81.9)}.
Each of the 1488 catalog movers (class rep relative to T) is simulated
with collider's simulate; products are recorded (JSON lines, resumable).
Usage: python zt_search.py OUT.jsonl"""
import sys, json, os
import gen
from rx import run
from tworeg_abs import R1, R2

PE = (30, -8)
OUT = sys.argv[1]
done = set()
if os.path.exists(OUT):
    for line in open(OUT):
        r = json.loads(line)
        done.add((tuple(r["mv"]), r["k"]))
gen.ABSORB = True
MV = [m for m in gen.movers("F") if gen.cross("F", (0, 0), m) is not None]   # clean on T
print("movers clean on T:", len(MV), flush=True)
D2 = (R2[0] - 12 * PE[0], R2[1] - 12 * PE[1])
fh = open(OUT, "a")
for mv in MV:
    for k in (8, 4, 0, -4):
        if (tuple(mv), k) in done:
            continue
        D1 = (R1[0] + k * PE[0], R1[1] + k * PE[1])
        T, M = (0, 0), (-D1[0], -D1[1])
        P = (M[0] - D2[0], M[1] - D2[1])
        pl = [("F",) + T, ("F",) + M, ("F",) + P, mv]
        try:
            prods = run(pl, 4000, must_settle=False)
        except Exception as e:
            prods = [("ERR:" + type(e).__name__, 0, 0)]
        fh.write(json.dumps({"mv": list(mv), "k": k, "prods": prods}) + "\n")
        fh.flush()
