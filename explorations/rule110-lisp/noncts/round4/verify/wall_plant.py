"""Partial independent check of objects 23:11 plant.py claim (every -3/5 wall
kind destroys the rod when it reaches the front).

My rods: round-3 longrod.rod(45) (E^15 from my library + spliced E-bg periods,
typed E^45 by my typer). A wall is launched by zeroing a w-cell window
95..104 cells behind the front (all 10 alignments, w = 4..12): this makes
the -3/5 wall measured in wall_check.py plus right-moving debris toward the
back. Run 1000 steps exactly (hrun), type with my typer. Control: the
unperturbed rod is still exactly E^45."""
import sys
import numpy as np
import hrun

sys.path.insert(0, hrun.R3V)
import longrod  # noqa: E402

vlib = hrun.vlib
T = 1000


def typed(row, org):
    h = hrun.HRun(row, org)
    h.goto(T)
    lo, hi = org - 2 * T, org + len(row) + T
    return [n.split("@")[0] for n, x, w in h.objects(lo, hi)]


if __name__ == "__main__" and len(sys.argv) == 1:
    row, org = longrod.rod(45)
    pad = vlib.ETHER  # rod row already has ether margins
    print("control:", typed(row, org))
    front = vlib.defects(row)[0]["lo"]
    outs = {}
    for w in (4, 6, 8, 10, 12):
        for off in range(10):
            r = row.copy()
            a = front + 95 + off
            r[a:a + w] = 0
            o = tuple(typed(r, org))
            outs.setdefault(o, []).append((w, off))
    for o, ks in sorted(outs.items(), key=lambda kv: -len(kv[1])):
        print(len(ks), o[:12], "..." if len(o) > 12 else "", ks[:4])


def rod_info(row, org):
    """After T steps: list of defects (lo, span, is (15,-4)-periodic over 30 steps)."""
    h = hrun.HRun(row, org)
    h.goto(T)
    lo, hi = org - 2 * T, org + len(row) + T
    r0 = h.cells(lo, hi)
    h.goto(T + 30)
    r1 = h.cells(lo - 8, hi - 8)
    out = []
    for d in vlib.defects(r0):
        a, b = d["lo"], d["hi"]
        out.append((a + lo, b - a, bool(np.array_equal(r0[a - 5:b + 5], r1[a - 5:b + 5]))))
    return out


def launched(row, r, org, t=200):
    """Leftmost difference between perturbed and control rows at time t,
    relative to the perturbation site; a -3/5 wall gives about -0.6 t."""
    h0, h1 = hrun.HRun(row, org), hrun.HRun(r, org)
    h0.goto(t); h1.goto(t)
    lo, hi = org, org + len(row)
    d = np.nonzero(h0.cells(lo, hi) != h1.cells(lo, hi))[0]
    return int(d[0]) if len(d) else None


def main2():
    row, org = longrod.rod(45)
    ctrl = rod_info(row, org)
    front = vlib.defects(row)[0]["lo"]
    n_wall = n_clean = 0
    for w in (4, 6, 8, 10, 12):
        for off in range(10):
            r = row.copy()
            a = front + 95 + off
            r[a:a + w] = 0
            e = launched(row, r, org)
            wall = e is not None and a - e >= 100        # moved >= 100 cells left in 200 steps
            info = rod_info(r, org)
            clean = len(info) == 1 and info[0][2]
            n_wall += wall
            n_clean += wall and clean
            if wall:
                print(f"w={w} off={off}: wall (edge moved {a - e} in 200 steps); "
                      f"after {T}: {len(info)} defect(s), first {info[0]}, control {ctrl[0]}")
    print(f"{n_wall} perturbations launched a -3/5 wall; {n_clean} of them leave one clean rod")


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "walls":
    main2()
