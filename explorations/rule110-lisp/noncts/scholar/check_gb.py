"""Independent evaluation of collider's G-speed instruction set for the E^n
counter (BOARD ~13:00): GB3 = DEC, GB4 = NOP, GB5 = INC in a rigid stream.
Placements from collider's ecounter.gb_stream (library read-only); evolution
with ../../engine.step; my census typer must find exactly ONE E-type object
whose slip equals the predicted counter value's (E^n slip = 9 + 6(n-1) mod
14) and nothing else. Control: shift all packets (the first meets the zero state) by (3,2).
Usage: python check_gb.py PROGRAM [control]   (PROGRAM over I, N, D)"""
import os
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
COL = HERE.parent / "collider"
sys.path.insert(0, str(COL))
cwd = os.getcwd()
os.chdir(COL)
import ecounter as EC                 # noqa: E402
from r110lib import build_row         # noqa: E402
os.chdir(cwd)
sys.path.insert(0, str(HERE))
import r110check as r                 # noqa: E402
from engine import step               # noqa: E402


def expected_n(program):
    n = 1
    for op in program:
        if op == "I":
            n += 1
        elif op == "D" and n > 1:
            n -= 1
        elif op == "D":
            raise ValueError("program DECs at zero; this check covers answer-free runs")
    return n


def main(program, control=False, shift=7):
    os.chdir(COL)
    scene = EC.gb_stream(program)
    os.chdir(cwd)
    if control:
        # shift the FIRST packet (it meets the counter at zero, where only
        # the designated class works) by the ether-lattice vector (7, 0), which is
        # NOT in <P_E, P_G> ((3, 2) is, so it would not change any class);
        # later packets are shifted too so the row stays ether-consistent
        scene = [scene[0]] + [(g, t0 + shift, x0) for g, t0, x0 in scene[1:]]
    L = EC.LIB.gliders
    sts = [L[a].state_at(t, x, 0) for a, t, x in scene]
    last = sts[-1]
    T = int(15 * (last[3] + 60)) + 600
    row, x0 = build_row(sts, pad=T + 200)
    hist = []
    cur = row
    for t in range(T):
        cur = step(cur)
        if t >= T - 160:
            hist.append(cur)
    h = np.array(hist)
    objs = [o[2] for o in r.objects(h, len(h) - 1, 150, len(row) - 150)]
    n = expected_n(program)
    slip = (9 + 6 * (n - 1)) % 14
    # my typer names E-type objects by width: 'E' (9), '?(15,-4,w..)' or 'E^k'
    def is_E_with_slip(name):
        if name == "E":
            return slip == 9
        if name.startswith("?(15,-4,w"):
            return int(name.split("w")[1].rstrip(")")) == slip
        if name.startswith("E^"):
            return (9 * int(name[2:])) % 14 == slip
        return False
    ok = len(objs) == 1 and is_E_with_slip(objs[0])
    print(f"{'CONTROL ' if control else ''}{program}: expected E^{n} (slip {slip}); "
          f"census {objs} -> {'OK' if ok else 'MISMATCH'}")
    return ok


if __name__ == "__main__":
    ctrl = len(sys.argv) > 2 and sys.argv[2].startswith("control")
    shift = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    sys.exit(0 if main(sys.argv[1], ctrl, shift) else 1)
