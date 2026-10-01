"""Right-anchored fixed program + incremental per-slot class search.

The PROGRAM packets have the same absolute placements for every input v
(literally the same stream text). The input is written to their LEFT:
  E, then v INC packets (GB5), each placed backwards from the program with
  ether compatibility and fixed spacing (so E's position depends on v).
For program slot s the class choice c in {0,1,2} is the seed time phase
t0 = -c of that packet (x nearest the target spacing, ether-compatible);
because the program does not move with v, c is one physical placement for
all inputs. Greedy over slots, branching only where some input meets the
packet in a class-sensitive state (value 0; value 1 for Z/W/X).
Usage: python rafast.py PROGRAM VMAX [--force s:c,...] [--spacing N]
"""
import copy
import sys
from common import LIB, CHAIN
from glidersim import GliderSim, ThreeBody
from r110lib import TILE
from stream import ALIAS
from adaptive import good, CAT
from test_prog import OPS

SPACING = 450
X0 = 0                        # left end of the program region


def place_right(prev_state, name, target_x, t0):
    """Seed (-t0, x) right of prev_state, ether-compatible, start nearest
    target_x."""
    g = LIB.gliders[name]
    pb, pl, pr, ps = prev_state
    c = (pr - ps) % TILE
    b, l, r, s_rel = g.state_at(-t0, 0, 0)
    base = (l - s_rel - c) % TILE
    lo = ps + len(pb) + 40 - s_rel
    x = lo + (base - lo) % TILE
    k = max(0, round((target_x - (x + s_rel)) / TILE))
    return (-t0, x + TILE * k)


def place_left(next_state, name, target_end):
    """Seed (0, x) LEFT of next_state with ether compatibility, end of the
    glider nearest target_end (<= next start - 40)."""
    g = LIB.gliders[name]
    nb, nl, nr, ns = next_state
    c = (nl - ns) % TILE                 # absolute ether phase left of next
    b, l, r, s_rel = g.state_at(0, 0, 0)
    # need (r - (x + s_rel)) % 14 == c  ->  x = r - s_rel - c (mod 14)
    hi = ns - 40 - len(b) - s_rel        # max x
    x = hi - ((hi - (r - s_rel - c)) % TILE)
    k = max(0, round((x + s_rel + len(b) - target_end) / TILE))
    return (0, x - TILE * k)


class Program:
    """Fixed program placements (independent of inputs)."""

    def __init__(self, anchor=("GB4", 0, 0)):
        # an invisible anchor fixes the program's ether: we start placing
        # right of a virtual GB4 state at X0 (not part of the scene)
        g = LIB.gliders[anchor[0]]
        self.prev = g.state_at(anchor[1], X0 + anchor[2], 0)
        self.first_state = None
        self.items = []

    def add(self, op, c):
        g = ALIAS[op]
        G = LIB.gliders[g]
        target = self.prev[3] + len(self.prev[0]) + SPACING
        ev = place_right(self.prev, g, target, c)
        self.items.append((g,) + ev)
        self.prev = G.state_at(ev[0], ev[1], 0)
        return (g,) + ev


def input_prefix(v):
    """Canonical input: E at (0,0) followed by v GB5's (the first in its
    designated zero class relative to E, as in stream.build)."""
    from stream import build
    return build(["I"] * v)


def shift_for(prefix, first_prog_item):
    """Pure x-shift D (same t = 0 text) that puts the program's first packet
    ether-compatibly at least SPACING right of the input prefix."""
    last = max((LIB.gliders[n].state_at(t, x, 0) for n, t, x in prefix), key=lambda q: q[3])
    c = (last[2] - last[3]) % TILE              # absolute ether right of prefix
    g = LIB.gliders[first_prog_item[0]]
    b, l, r, s = g.state_at(first_prog_item[1], first_prog_item[2], 0)
    cp = (l - s) % TILE                         # program's absolute left ether
    lo = last[3] + len(last[0]) + SPACING - s   # minimal shift by distance
    # shifting by D changes the program's ether phase to (cp - D): need == c
    D = lo + ((cp - c) - lo) % TILE
    return D


def input_part(v, first_prog_item):
    """E and v GB5's to the left of the program's first packet."""
    g0 = LIB.gliders[first_prog_item[0]]
    nxt = g0.state_at(first_prog_item[1], first_prog_item[2], 0)
    items = []
    for _ in range(v):
        ev = place_left(nxt, "GB5", nxt[3] - SPACING)
        items.append(("GB5",) + ev)
        nxt = LIB.gliders["GB5"].state_at(ev[0], ev[1], 0)
    ev = place_left(nxt, "E", nxt[3] - SPACING)
    items.append(("E",) + ev)
    return items[::-1]


COSET = True          # enforce coset_ok in greedy
MODE = "shift"        # "shift": canonical prefix + program x-shifted; "left": input built leftward


class Run:
    def __init__(self, v, first_item):
        self.v = v
        self.val = v
        if MODE == "shift":
            pre = input_prefix(v)
            self.D = shift_for(pre, first_item)
            self.sim = GliderSim(LIB, pre, cat=CAT)
        else:
            self.D = 0
            self.sim = GliderSim(LIB, input_part(v, first_item), cat=CAT)
        self.sim.run(self.horizon_for(None))
        assert good(self.sim.state(), v), self.sim.state()
        self.started = False

    def horizon_for(self, item):
        t = self.sim.t
        ecs = [q for q in self.sim.gl if q[0] in CHAIN]
        bE = LIB.gliders[ecs[0][0]].state_at(ecs[0][1], ecs[0][2], t)
        if item is None:      # finish the input part
            far = max(LIB.gliders[q[0]].state_at(q[1], q[2], t)[3] for q in self.sim.gl)
            return t + int(15 * max(far - bE[3], 0)) + 2500
        bP = LIB.gliders[item[0]].state_at(item[1], item[2], t)
        return t + int(15 * max(bP[3] - bE[3] - len(bE[0]), 0)) + 2500

    def add(self, op, item):
        self.val = OPS[op](self.val)
        if not self.started:
            # the first program packet: it was already right of the input
            # part from t = 0; it has been moving freely, so just add it
            self.started = True
        item = (item[0], item[1], item[2] + self.D)
        self.sim.gl.append(item)
        try:
            self.sim.run(self.horizon_for(item))
        except (ThreeBody, AssertionError):
            return False
        return good(self.sim.state(), self.val)

    def trial(self, op, item):
        r = copy.copy(self)
        r.sim = copy.copy(self.sim)
        r.sim.gl = list(self.sim.gl)
        r.sim.log = list(self.sim.log)
        return r, r.add(op, item)


def coset_ok(runs):
    """Inputs v and v + 7 have the same prefix ether, so their counters are
    directly comparable: if they hold the same value they must sit on the same
    trajectory class (mod <P_E, P_G>), otherwise they can never again be
    served by the same fixed stream at a zero meeting."""
    from r110lib import class_key as ck
    by = {}
    for r in runs:
        es = [g for g in r.sim.state() if g[0] in CHAIN]
        if len(es) != 1:
            return False
        key = (r.v % 7, r.val)
        k = ck((es[0][1], es[0][2]), (15, -4), (42, -14))
        if by.setdefault(key, k) != k:
            return False
    return True


def greedy(prog, vmax, forced=None):
    forced = forced or {}
    P = Program()
    first = P.add(prog[0], forced.get(0, 0))
    # input parts are built against the first packet's placement; the first
    # packet's class is then searched by rebuilding (it is cheap)
    classes = []
    best = None
    for c0 in ((forced[0],) if 0 in forced else (0, 1, 2)):
        P = Program()
        first = P.add(prog[0], c0)
        try:
            runs = [Run(v, first) for v in range(vmax + 1)]
        except AssertionError:
            continue
        new = []
        for r in runs:
            r2, ok = r.trial(prog[0], first)
            if not ok:
                break
            new.append(r2)
        else:
            best = (P, new, c0)
            break
    if best is None:
        return [], False, 0, None
    P, runs, c0 = best
    classes = [c0]
    for s in range(1, len(prog)):
        op = prog[s]
        sens = any(r.val == 0 or (r.val == 1 and op in "ZWX") for r in runs)
        choices = (forced[s],) if s in forced else ((0, 1, 2) if sens else (0,))
        for c in choices:
            P2 = copy.copy(P)
            P2.items = list(P.items)
            item = P2.add(op, c)
            new = []
            for r in runs:
                r2, ok = r.trial(op, item)
                if not ok:
                    break
                new.append(r2)
            else:
                if COSET and not coset_ok(new):
                    continue
                runs, P = new, P2
                classes.append(c)
                break
        else:
            return classes, False, s, P
    return classes, True, len(prog), P


def dfs(prog, vmax, limit=20000):
    """Backtracking version of greedy (same placement rules). Returns
    (classes, ok, Program)."""
    import itertools  # noqa: F401
    stats = {"nodes": 0}

    def rec(s, P, runs, classes):
        if s == len(prog):
            return classes, P
        if stats["nodes"] > limit:
            return None
        op = prog[s]
        sens = s == 0 or any(r.val == 0 or (r.val == 1 and op in "ZWX") for r in runs)
        for c in ((0, 1, 2) if sens else (0,)):
            stats["nodes"] += 1
            P2 = copy.copy(P)
            P2.items = list(P.items)
            item = P2.add(op, c)
            if s == 0:
                try:
                    runs0 = [Run(v, item) for v in range(vmax + 1)]
                except AssertionError:
                    continue
            else:
                runs0 = runs
            new = []
            for r in runs0:
                r2, ok = r.trial(op, item)
                if not ok:
                    break
                new.append(r2)
            else:
                if COSET and not coset_ok(new):
                    continue
                res = rec(s + 1, P2, new, classes + [c])
                if res is not None:
                    return res
        return None

    res = rec(0, Program(), None, [])
    print("nodes", stats["nodes"])
    if res is None:
        return None, False, None
    return res[0], True, res[1]




if __name__ == "__main__":
    prog = sys.argv[1]
    vmax = int(sys.argv[2])
    forced = {}
    if "--force" in sys.argv:
        for kv in sys.argv[sys.argv.index("--force") + 1].split(","):
            a, b = kv.split(":")
            forced[int(a)] = int(b)
    if "--dfs" in sys.argv:
        cl, ok, P = dfs(prog, vmax)
        cl = cl or []
        s = len(cl)
    else:
        cl, ok, s, P = greedy(prog, vmax, forced)
    print("classes", ",".join(map(str, cl)), "OK" if ok else f"FAILED at slot {s}")
    if P is not None:
        print("program", P.items)
