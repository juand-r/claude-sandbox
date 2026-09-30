"""Independent evaluation of architect's crossing-only F-pair counter
(architect/xcounter.py). Placements and predicted final F seeds come from
architect's schedule() (collider library, read-only). Evolution uses
../../engine.step; the check is cell-exact: the final row must contain each
predicted F (bits at the predicted columns, from Glider.state_at), and my
census typer must find nothing but the two F's and Ebar-speed gliders.
Usage: python check_xcounter.py [k]   (INC^k then DEC^k, default 3)"""
import os
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ARCH = HERE.parent / "architect"
sys.path.insert(0, str(ARCH))
sys.path.insert(0, str(HERE.parent / "collider"))
cwd = os.getcwd()
os.chdir(ARCH)
import xcounter as X                  # noqa: E402
from rx import G as GL                # noqa: E402
from r110lib import build_row         # noqa: E402
os.chdir(cwd)
sys.path.insert(0, str(HERE))
import r110check as r                 # noqa: E402
from engine import step               # noqa: E402

LEFT_SPEEDS = ("E", "E-")             # family prefixes allowed besides F


def main(k=3):
    ops = [X.INC] * k + [X.DEC] * k
    os.chdir(ARCH)
    pl, T_pred, P_pred = X.schedule((0, 0), (0, -43), ops)
    os.chdir(cwd)
    Tn = 36 * 20 * len(pl) + 6000
    states = [GL[n].state_at(t0, x0, 0) for n, t0, x0 in pl]
    row, xo = build_row(states, pad=Tn + 300)
    cur = row
    hist = []
    for t in range(Tn):
        cur = step(cur)
        if t >= Tn - 160:
            hist.append(cur)
    h = np.array(hist)
    ok_f = True
    for (t0, x0) in (T_pred, P_pred):
        bits, lph, rph, s = GL["F"].state_at(t0, x0, Tn)
        seg = "".join(map(str, h[-1][s - xo:s - xo + len(bits)]))
        ok_f &= seg == bits
    objs = r.objects(h, len(h) - 1, 200, len(row) - 200)
    names = [o[2] for o in objs]
    extra = [n for n in names if not (n == "F" or n.startswith(LEFT_SPEEDS)
                                      or n.startswith("?(15,-4") or n.startswith("?(30,-8"))]
    nF = names.count("F")
    print(f"INC^{k} DEC^{k}: predicted F's present cell-exact: {ok_f}; "
          f"F count {nF}; non-Ebar-speed objects: {extra}; all objects: {sorted(set(names))}")
    return ok_f and nF == 2 and not extra


if __name__ == "__main__":
    sys.exit(0 if main(int(sys.argv[1]) if len(sys.argv) > 1 else 3) else 1)
