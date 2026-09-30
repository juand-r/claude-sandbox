"""Crossing counter with value 0 = the SEPARATED pair at gap 24.33
(D = (12,23), standard residue), fixed stream.

DEC' = DEC + S1, where S1 = [lane Ebar, pair(-1,25)@(-14,55)] is exactly
the identity on separated pairs (catalog prediction) and splits the close
compound F_19_F (what DEC leaves at gap 33.67 -> below) into the
separated gap-24.33 pair (ztest3/ztest4). So DEC' decrements for every
value >= 1 and lands on the separated zero state. At value 0, DEC destroys
the pair and emits one A to the right (the zero event), all other debris
moving left. INC works from the separated zero state (checked).
Instructions are padded with lane Ebars so that all drift T identically
modulo L_FE (lane Ebar drift f3 generates the needed shifts)."""
import sys
from fractions import Fraction
import xstream as xs
from xstream import INC, DEC, LANE, C_ID
from r110lib import class_key

S1 = [LANE, ("Ebar@(0,0)+Ebar@(-1,25)", -14, 55)]
BASE = {"INC": INC, "DEC": list(DEC) + S1, "NOP": [C_ID]}


def balanced():
    """Pad each instruction with lane Ebars so all drifts agree mod L."""
    PF, PE = (36, -4), (30, -8)
    prog = {}
    drift = {}
    for nm, seq in BASE.items():
        for k in range(12):
            xs.PROG = {nm: seq + [LANE] * k}
            plan = xs.slot_plan(nm, (0, 0), (0, -43))
            drift[(nm, k)] = class_key(plan[1], PF, PE)
    target = None
    for kd in range(12):
        t = drift[("DEC", kd)]
        ks = {nm: next((k for k in range(12) if drift[(nm, k)] == t), None) for nm in BASE}
        if all(v is not None for v in ks.values()):
            target = ks
            break
    assert target, "no balanced padding"
    return {nm: BASE[nm] + [LANE] * target[nm] for nm in BASE}


if __name__ == "__main__":
    xs.PROG = balanced()
    print({k: len(v) for k, v in xs.PROG.items()}, flush=True)
    xs.STD = {nm: xs.slot_plan(nm, (0, 0), (0, -43)) for nm in xs.PROG}
    xs.DELTA = xs.STD["DEC"][1]
    xs.SLOT_LEN = max(xs.STD[nm][2] for nm in xs.PROG) + xs.GAP
    tests = [["DEC"], ["DEC", "DEC"], ["DEC", "DEC", "INC"], ["DEC", "DEC", "INC", "INC"],
             ["INC", "DEC", "DEC", "DEC", "INC", "INC"], ["DEC", "DEC", "NOP", "INC", "DEC"]]
    for prog in tests:
        good, msg = xs.check(prog)
        print(prog, "OK" if good else "FAIL", msg, flush=True)
