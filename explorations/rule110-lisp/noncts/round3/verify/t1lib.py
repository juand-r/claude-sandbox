"""T1 helpers: left-stream packets in my vlib convention.
IL = leftstream's INC train (cells 111110111110111110001110, left ether
phase 0 at x = 0), registered in my library with its (3,2) period CHECKED by
vlib.register.  Ops: 'I' -> IL, 'D' -> A.
Scenes are anchored at the counter: the phase just left of E is fixed (c_E),
so program items keep their positions when slots are added on the left, and
the input encoding (B's from the right) never moves the program."""
import numpy as np
import v3, vlib, engine

IL_BITS = "111110111110111110001110"      # leftstream 05:40, slip 6
ZL_BITS = "111110111110111000111011"      # leftstream 05:46, slip 8


def _reg(name, bits, slip):
    core = np.array([int(c) for c in bits], np.uint8)
    left = vlib.ETHER[np.arange(-56, 0) % 14]
    right = vlib.ETHER[(np.arange(24, 24 + 56) + slip) % 14]
    base = np.concatenate([left, core, right])     # base[0] at x = -56: phase 0
    vlib.register(name, base, (3, 2))              # raises unless period (3,2)


def register_IL():
    """(Re)register the left-stream packets; call again after anything that
    runs libgen.load() (it clears the library)."""
    if "IL" not in vlib.LIB:
        _reg("IL", IL_BITS, 6)
    if "ZL" not in vlib.LIB:
        _reg("ZL", ZL_BITS, 8)


register_IL()
OPS = {"I": "IL", "D": "A", "Z": "ZL"}
C_E = 0


def scene_items(slots, v, bsp=50):
    """slots: [(op, t0, x0)] in program order (first op = rightmost)."""
    prog = [(OPS[o], t, x) for o, t, x in slots][::-1]
    inp = [("E", 0, 0)] + [("B", 0, 75 + bsp * k) for k in range(v)]
    return prog + inp


def build(slots, v, T):
    items = scene_items(slots, v)
    c0 = (C_E - sum(vlib.LIB[n].w for n, _, _ in items[:len(slots)])) % 14
    row, org, placed = vlib.build(items, c0=c0, T=T)
    return row, org, placed


def outcome(slots, v, T):
    row, org, placed = build(slots, v, T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    objs = [(n, x) for n, x, w, k in vlib.identify(r, org, T=T)]
    return objs, placed


def counter_and_answers(objs):
    """(value, number of A's right of the counter) if the run ends in one
    E-family counter plus only single A's to its right; else None."""
    names = [v3.base(n) for n, x in objs]
    NEG = {"C3": -1, "C2": -2, "C1": -3}        # leftstream 05:50: R2 below zero
    cs = [i for i, b in enumerate(names) if b == "E" or b.startswith("E^") or b in NEG]
    if len(cs) != 1:
        return None
    i = cs[0]
    if names[:i] or any(b != "A" for b in names[i + 1:]):
        return None
    b = names[i]
    if b in NEG:
        return (NEG[b], len(names) - i - 1)
    return (0 if b == "E" else int(b[2:]) - 1, len(names) - i - 1)


def value(objs):
    """counter value if the run ends in exactly one E-family counter."""
    if len(objs) != 1:
        return None
    b = v3.base(objs[0][0])
    if b == "E":
        return 0
    if b.startswith("E^"):
        return int(b[2:]) - 1
    return None
