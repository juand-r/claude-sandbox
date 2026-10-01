"""Check theory 23:05 (route LN) example head steps with MY builder/typer.

Each reaction: collider scene [(X,0,0),(Y,t,x)] (X left), rebuilt by my
builder (rows asserted equal to collider's build_row), run T steps exactly
(engine), typed by my typer (expected product objects registered in my
library by clib.ensure, periods found by my own search).

Single-class test (can fail): Y moved to other valid ether-lattice events
(t + dt, x + dx) with dx + 4 dt = 0 mod 14 must give the SAME products
(the lemma: |det(P_H, (7,0))| / 14 = 1).
Negative control: the cell replaced by another cell must change the products."""
import clib
import xlate

T = 700
CASES = [  # (X, Y, Y_event, expected products) from theory/lnscan2.jsonl
    ("A@(0,0)+A@(-1,24)", "C1", (0, 73), ["B_2_B_4_B_2_B", "C2"], "C2"),
    ("D2_7_D2#2", "C3", (0, 63), ["A_0_A_7_A", "C2"], "C1"),
    ("C1", "v-2/4s6w29", (0, 43), ["B", "C1"], "C2"),
    ("v0/7s2w48", "v-2/4s12w33", (0, 93), ["C2", "D1"], "C1"),
]
SHIFTS = [(0, 0), (0, 14), (1, 10), (2, 20), (5, 36), (0, 28)]


def scene_of(X, Y, ev):
    return xlate.expand([(X, 0, 0)]) + xlate.expand([(Y, ev[0], ev[1])])


def valid(scene):
    """Move the last object right by 0..13 cells until the ether phases of
    the scene agree (collider's build_row is the validity oracle: it raises
    ValueError on a phase mismatch). Used only for the control scene."""
    *rest, (g, t, x) = scene
    for dx in range(14):
        sc = rest + [(g, t, x + dx)]
        try:
            xlate.their_row(sc)
            return sc
        except ValueError:
            continue
    raise ValueError("no valid placement")


def products(objs):
    return sorted(n.split("@")[0] for n, x, w in objs)


def main():
    n_ok = 0
    for X, Y, ev, want, other in CASES:
        for p in want:
            clib.ensure(p)
        res = []
        for dt, dx in SHIFTS:
            assert (dx + 4 * dt) % 14 == 0
            objs, r, org = clib.rebuild(scene_of(X, Y, (ev[0] + dt, ev[1] + dx)), T)
            res.append(products(objs))
        ok = all(p == sorted(want) for p in res)
        n_ok += ok
        # negative control: swap the cell
        if X.startswith("C") or X.startswith("v0/7"):
            ctrl = scene_of(other, Y, ev)
        else:
            ctrl = scene_of(X, other, ev)
        cp = products(clib.rebuild(valid(ctrl), T)[0])
        print(f"{X} + {Y}: {'OK' if ok else 'DIFF'} {res[0]} over {len(SHIFTS)} lattice shifts"
              f" | control (cell -> {other}): {cp} {'differs' if cp != sorted(want) else 'SAME?!'}")
    print(f"{n_ok}/{len(CASES)} confirmed")


if __name__ == "__main__":
    main()
