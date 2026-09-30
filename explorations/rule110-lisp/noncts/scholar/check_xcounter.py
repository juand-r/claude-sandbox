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


def main(k=3, control=False, opstr=None):
    ops = [X.INC] * k + [X.DEC] * k
    if opstr:
        ops = [X.INC if c == "I" else X.DEC for c in opstr]
    os.chdir(ARCH)
    pl, T_pred, P_pred = X.schedule((0, 0), (0, -43), ops)
    os.chdir(cwd)
    if control:
        # negative control: shift the LAST mover by the ether-lattice vector
        # (3, 2); this keeps the row valid but changes its collision class
        n, t0, x0 = pl[-1]
        pl = pl[:-1] + [(n, t0 + 3, x0 + 2)]
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
    from engine import ETHER
    for (t0, x0) in (T_pred, P_pred):
        # predicted F with 28 cells of its own ether on each side (collider's
        # convention: y < s reads ETHER[(lph + y - s) % 14], y >= s+len reads
        # ETHER[(rph + y - s) % 14])
        bits, lph, rph, s = GL["F"].state_at(t0, x0, Tn)
        ref = ("".join(ETHER[(lph + y - s) % 14] for y in range(s - 28, s)) + bits
               + "".join(ETHER[(rph + y - s) % 14] for y in range(s + len(bits), s + len(bits) + 28)))
        seg = "".join(map(str, h[-1][s - 28 - xo:s + len(bits) + 28 - xo]))
        ok_f &= seg == ref
    objs = r.objects(h, len(h) - 1, 200, len(row) - 200)
    names = [o[2] for o in objs]
    extra = [n for n in names if not (n == "F" or n.startswith(LEFT_SPEEDS)
                                      or n.startswith("?(15,-4") or n.startswith("?(30,-8"))]
    nF = names.count("F")
    print(f"{'CONTROL ' if control else ''}{opstr or f'INC^{k} DEC^{k}'}: predicted F's present cell-exact: {ok_f}; "
          f"F count {nF}; non-Ebar-speed objects: {extra}; all objects: {sorted(set(names))}")
    return ok_f and nF == 2 and not extra


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "3"
    ctrl = len(sys.argv) > 2 and sys.argv[2] == "control"
    if arg.isdigit():
        sys.exit(0 if main(int(arg), ctrl) else 1)
    sys.exit(0 if main(0, ctrl, opstr=arg) else 1)
