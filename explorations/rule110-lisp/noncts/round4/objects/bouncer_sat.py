"""Perpetual-bouncer SAT (theory 23:38 / lead 23:46: objects owns the SAT form).

Two scenes in ONE CNF sharing the head variables:
  R:  h1 (right-mover, lattice (p1, d1)) + W  ->  W (same pattern, any shift)
      + h2 (left-mover, lattice (p2, d2)); nothing to the right.
  L:  h2 + V  ->  V (same, any shift) + h1; nothing to the left.
W, V free stationary walls (period (7,0), widths WW, WV, right phases sW,
sV); h1, h2 free trains (widths W1, W2, right phase s; slip balance forces
s(h1) = s(h2) = s when the walls are restored).
Separation (objects 00:19): the band between a wall and the outgoing head is
ether of the phase on the head's near side (prevents an absorbed head from
matching as a phase jump at the wall's edge).
Every solution: synth's verify_reaction on both scenes, then an exact
multi-bounce run (bouncer_run) is the real test.
Usage: python3 bouncer_sat.py W1 W2 WW WV T2 out.jsonl [--s list] [--sW list]
       [--sV list] [--lat1 3,2] [--lat2 4,-2]
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


def separate(r, T2, side, slip):
    """band next to the middle on `side` = ether of the near-side phase."""
    st = r.st
    if side == "R":
        ph = (r.pfr - slip) % TILE
        xs = range(r.b, r.b + 14)
    else:
        ph = (r.pfl + slip) % TILE
        xs = range(r.a - 14, r.a)
    for x in xs:
        st.fix(T2, x, ether_bit(ph, T2, x))


def build(W1, W2, WW, WV, T2, s, sW, sV, lat1, lat2, mM=12, onlyR=False, onlyL=False):
    cnf = CNF()
    h1 = TrainVar(cnf, W1, lat1[0], lat1[1], s, name="h1")
    h2 = TrainVar(cnf, W2, lat2[0], lat2[1], s, name="h2")
    Wo = ObjectVar(cnf, WW, sW, name="W")
    Vo = ObjectVar(cnf, WV, sV, name="V")
    rR = None
    if not onlyL:
        rR = Reaction(cnf, Wo, h1, T2, left=("is", h2), middle=("is", Wo), right=None,
                      mL=mM, mR=mM, name="R")
        separate(rR, T2, "L", s)
    if onlyR:
        return cnf, h1, h2, Wo, Vo, rR, None
    rL = Reaction(cnf, Vo, h2, T2, left=None, middle=("is", Vo), right=("is", h1),
                  mL=mM, mR=mM, name="L")
    separate(rL, T2, "R", s)
    return cnf, h1, h2, Wo, Vo, rR, rL


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for a in ("W1", "W2", "WW", "WV", "T2"):
        ap.add_argument(a, type=int)
    ap.add_argument("out")
    ap.add_argument("--s", default=",".join(map(str, range(TILE))))
    ap.add_argument("--sW", default=",".join(map(str, range(TILE))))
    ap.add_argument("--sV", default=",".join(map(str, range(TILE))))
    ap.add_argument("--lat1", default="3,2")
    ap.add_argument("--lat2", default="4,-2")
    ap.add_argument("--onlyR", action="store_true", help="scene R alone (prune/control)")
    ap.add_argument("--onlyL", action="store_true", help="scene L alone (prune)")
    A = ap.parse_args()
    lat1 = tuple(map(int, A.lat1.split(",")))
    lat2 = tuple(map(int, A.lat2.split(",")))
    done = set()
    if os.path.exists(A.out):
        for l in open(A.out):
            r = json.loads(l)
            done.add((r["s"], r["sW"], r["sV"]))
    for s in map(int, A.s.split(",")):
        for sW in map(int, A.sW.split(",")):
            for sV in map(int, A.sV.split(",")):
                if (s, sW, sV) in done:
                    continue
                t0 = time.time()
                try:
                    cnf, h1, h2, Wo, Vo, rR, rL = build(A.W1, A.W2, A.WW, A.WV, A.T2,
                                                        s, sW, sV, lat1, lat2, onlyR=A.onlyR, onlyL=A.onlyL)
                except ValueError as e:
                    rec = {"s": s, "sW": sW, "sV": sV, "error": str(e)}
                    print(json.dumps(rec), flush=True)
                    with open(A.out, "a") as fh:
                        fh.write(json.dumps(rec) + "\n")
                    continue
                sol = cnf.solve()
                rec = {"W1": A.W1, "W2": A.W2, "WW": A.WW, "WV": A.WV, "T2": A.T2,
                       "lat1": lat1, "lat2": lat2, "s": s, "sW": sW, "sV": sV,
                       "onlyR": A.onlyR, "onlyL": A.onlyL, "sat": sol is not None, "secs": round(time.time() - t0, 1)}
                if sol is not None:
                    vR = verify_reaction(rR, sol) if rR is not None else {}
                    vL = verify_reaction(rL, sol) if rL is not None else {}
                    rec["vR"] = {k: (v if isinstance(v, str) else bool(v)) for k, v in vR.items()}
                    rec["vL"] = {k: (v if isinstance(v, str) else bool(v)) for k, v in vL.items()}
                    for nm, it in (("h1", h1), ("h2", h2), ("W", Wo), ("V", Vo)):
                        rec[nm] = "".join(map(str, it.decode(sol)))
                    if rR is not None:
                        rec["rowR"] = "".join(map(str, rR.initial_row(sol)))
                        rec["frR"] = (rR.lo, rR.pfl, rR.pfr)
                    if rL is not None:
                        rec["rowL"] = "".join(map(str, rL.initial_row(sol)))
                        rec["frL"] = (rL.lo, rL.pfl, rL.pfr)
                print(json.dumps({k: v for k, v in rec.items() if not k.startswith("row")}), flush=True)
                with open(A.out, "a") as fh:
                    fh.write(json.dumps(rec) + "\n")
