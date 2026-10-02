"""Theory's S1 (board 23:18): a head that PASSES a stationary cell and
re-emerges identical, rewriting the cell: h + c -> c' + h.

synth's Reaction (imported read-only): obj = free stationary cell c
(ObjectVar, period (7,0), width WC, right ether phase sc), train = free head
h (TrainVar, period (p, d), width WH, right phase sh); A lattice (3,2) or
D lattice (10,2) heads come from the left, B lattice (4,-2) from the right.
All of these have ONE collision class against a period-7 cell, so the
placement is without loss of generality.
At T2: the side the head came from is pure ether (nothing reflected); the
middle is a NONEMPTY period-7 pattern (c', any, may equal c); the far side
is exactly h again (shared variables) -- or, with --anytrain (positive
control), any nonempty train of the head's lattice.
Solutions are re-simulated by synth's verify_reaction (SAT rows = sim, the
middle persists, the far side moves as a train).
Usage: python3 s1_pass.py p d WH WC T2 out.jsonl [--sc list] [--sh list] [--anytrain]
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "synth")))
from r110sat import CNF, TILE, ether_bit, neg      # noqa: E402
from react import TrainVar, ObjectVar, Reaction, verify_reaction  # noqa: E402

ap = argparse.ArgumentParser()
for a in ("p", "d", "WH", "WC", "T2"):
    ap.add_argument(a, type=int)
ap.add_argument("out")
ap.add_argument("--sc", default=",".join(map(str, range(TILE))))
ap.add_argument("--sh", default=",".join(map(str, range(TILE))))
ap.add_argument("--anytrain", action="store_true")
ap.add_argument("--mM", type=int, default=12)
ap.add_argument("--outA", action="store_true", help="control: far side = one library A (slip 8), separation band enforced")
A = ap.parse_args()

for sc in map(int, A.sc.split(",")):
    for sh in map(int, A.sh.split(",")):
        t0 = time.time()
        cnf = CNF()
        c = ObjectVar(cnf, A.WC, sc, name="c")
        h = TrainVar(cnf, A.WH, A.p, A.d, sh, name="h")
        far = ("train", A.p, A.d) if A.anytrain else ("is", h)
        out_slip = sh
        if A.outA:
            from lib import load_gliders
            from react import fixed_from_glider
            Aitem = fixed_from_glider(cnf, load_gliders()["A"], 8)
            far = ("is", Aitem)
            out_slip = Aitem.pR
        if A.d > 0:
            left, right = None, far
        else:
            left, right = far, None
        try:
            r = Reaction(cnf, c, h, A.T2, left=left, middle=("stationary",),
                         right=right, mL=A.mM, mR=A.mM)
        except ValueError as e:
            print(json.dumps({"sc": sc, "sh": sh, "error": str(e)}), flush=True)
            continue
        # c' nonempty: the middle differs from the ether of the near band
        st, T2 = r.st, A.T2
        band = r.bandL
        for ph in range(TILE):
            cl = [-band[ph]]
            for x in range(r.a, r.b):
                l = st.lit(T2, x)
                cl.append(neg(l) if ether_bit(ph, T2, x) else l)
            cnf.add(cl)
        # the head must be SEPARATED from c': the band between the middle and
        # the far region is ether of the phase on the head's near side
        # (otherwise a head absorbed into c' can masquerade as a phase jump
        # at the middle's edge: found 2026-10-02 00:05, sc=2 sh=8 witness)
        if not A.anytrain:
            if A.d > 0:
                ph_near = (r.pfr - out_slip) % TILE
                for x in range(r.b, r.b + 14):
                    st.fix(T2, x, ether_bit(ph_near, T2, x))
            else:
                ph_near = (r.pfl + out_slip) % TILE
                for x in range(r.a - 14, r.a):
                    st.fix(T2, x, ether_bit(ph_near, T2, x))
        sol = cnf.solve()
        rec = {"p": A.p, "d": A.d, "WH": A.WH, "WC": A.WC, "T2": A.T2,
               "sc": sc, "sh": sh, "anytrain": A.anytrain, "outA": A.outA,
               "sat": sol is not None, "secs": round(time.time() - t0, 1)}
        if sol is not None:
            v = verify_reaction(r, sol)
            rec["verify"] = {k: (bool(x) if not isinstance(x, str) else x) for k, x in v.items()}
            rec["h"] = "".join(map(str, h.decode(sol)))
            rec["c"] = "".join(map(str, c.decode(sol)))
            rec["row0"] = "".join(map(str, r.initial_row(sol)))
            rec["lo"], rec["pfl"], rec["pfr"] = r.lo, r.pfl, r.pfr
            if not v["ok"]:
                rec["WARNING"] = "verify_reaction not ok"
        print(json.dumps({k: v for k, v in rec.items() if k != "row0"}), flush=True)
        with open(A.out, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
