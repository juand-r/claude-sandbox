"""Incremental version of adaptive.py's greedy/DFS: for every input v the
glider-level simulation of the program prefix is cached and extended by one
packet at a time (the new packet is the rightmost object and moves freely
until it reaches the counter, so earlier events are unaffected).

Same placement rule as adaptive.build (class key relative to E(0,0) where
the predecessors' slip is 0 mod 14, else seed phase t0 = class).
Usage: python fastsearch.py PROGRAM VMAX [--force slot:class,...]
"""
import copy
import sys
from common import LIB, CHAIN
from glidersim import GliderSim, ThreeBody
from onesided import place
from r110lib import class_key
from collide import canonical_reps
from stream import ALIAS
from adaptive import place_phase, good, SPACING, CAT
from test_prog import OPS


class Run:
    """Cached simulation of one input v."""

    def __init__(self, v):
        E = LIB.gliders["E"]
        self.scene = [("E", 0, 0)]
        self.prev = E.state_at(0, 0, 0)
        self.slip = 0
        self.sim = GliderSim(LIB, list(self.scene), cat=CAT)
        self.val = 0           # the prefix below writes v
        self.broken = False
        for _ in range(v):
            self.add("I", 0)

    def placement(self, op, c):
        g = ALIAS[op]
        G = LIB.gliders[g]
        E = LIB.gliders["E"]
        target = self.prev[3] + len(self.prev[0]) + SPACING
        if self.slip % 14 == 0 and c is not None:
            reps = canonical_reps(LIB, "E", g)
            key = class_key(reps[c], (E.p, E.d), (G.p, G.d))
            ev = place(self.prev, g, target, want_key=key)
        else:
            ev = place_phase(self.prev, g, target, c or 0)
        return g, ev

    def add(self, op, c):
        """Extend by one packet (in place). Returns False if the outcome is
        not the model's clean value."""
        g, ev = self.placement(op, c)
        G = LIB.gliders[g]
        self.scene.append((g,) + ev)
        self.prev = G.state_at(ev[0], ev[1], 0)
        self.slip += G.slip
        self.val = OPS[op](self.val)
        self.sim.gl.append((g,) + ev)
        # run until this packet has met the counter: estimate the meeting
        # time from the CURRENT positions (zero-J's push E right, so a
        # horizon computed from t = 0 positions can overshoot the next
        # packet's arrival), plus slack for the reaction itself
        t = self.sim.t
        ecs = [q for q in self.sim.gl if q[0] in CHAIN]
        bP = G.state_at(ev[0], ev[1], t)
        if ecs:
            bE = LIB.gliders[ecs[0][0]].state_at(ecs[0][1], ecs[0][2], t)
            gap = bP[3] - (bE[3] + len(bE[0]))
        else:
            gap = bP[3]
        T = t + int(15 * max(gap, 0)) + 2500
        try:
            self.sim.run(T)
        except ThreeBody:
            self.broken = True
            return False
        except AssertionError as e:
            # glidersim: the new packet would collide before the previous
            # horizon, i.e. a leftover object moved into the stream: the
            # trial is broken (logged loudly, counted as failure)
            print("   [trial broken:", e, "| state", self.sim.state(), "]", flush=True)
            self.broken = True
            return False
        return good(self.sim.state(), self.val)

    def trial(self, op, c):
        r = copy.copy(self)
        r.scene = list(self.scene)
        r.sim = copy.copy(self.sim)
        r.sim.gl = list(self.sim.gl)
        r.sim.log = list(self.sim.log)
        ok = r.add(op, c)
        return r, ok


def greedy(prog, vmax, forced=None):
    forced = forced or {}
    runs = [Run(v) for v in range(vmax + 1)]
    classes = []
    for s, op in enumerate(prog):
        sens = any(r.val == 0 or (r.val == 1 and op in "ZWX") for r in runs)
        choices = (forced[s],) if s in forced else ((0, 1, 2) if sens else (0,))
        for c in choices:
            new = []
            for r in runs:
                r2, ok = r.trial(op, c)
                if not ok:
                    break
                new.append(r2)
            else:
                runs = new
                classes.append(c)
                break
        else:
            return classes, False, s
    return classes, True, len(prog)


if __name__ == "__main__":
    prog = sys.argv[1]
    vmax = int(sys.argv[2])
    forced = {}
    if "--force" in sys.argv:
        for kv in sys.argv[sys.argv.index("--force") + 1].split(","):
            a, b = kv.split(":")
            forced[int(a)] = int(b)
    cl, ok, s = greedy(prog, vmax, forced)
    print("classes", ",".join(map(str, cl)), "OK" if ok else f"FAILED at slot {s}")
