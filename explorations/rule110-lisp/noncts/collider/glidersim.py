"""Event-driven glider-level simulator built on the collision catalog.

State: a set of gliders, each a library name and a seed event (t0, x0).
Between collisions every glider moves freely along its trajectory. The next
collision is always between two spatial neighbours L, R with v_L > v_R;
its class, its spacetime translation relative to the catalog entry, its
interaction region (regions.json) and its products follow from the
catalog by lattice arithmetic (see predict.py), with no cellular-automaton
simulation.

Soundness guard (fails loudly): a collision is applied only if every other
glider stays at least GUARD cells away from the collision's interaction
region during the region's time span. Otherwise ThreeBody is raised: the
catalog of pairwise collisions does not determine what happens. Pairs
missing from the catalog are computed on demand (collide.collide_pair +
regions.region) and cached in memory.

Validation: validate() compares against the real automaton on random
scenes (python glidersim.py validate N).
"""

import json
import random
import sys
from fractions import Fraction

from collide import canonical_reps, collide_pair, simulate
from library import Library
from r110lib import TILE, class_key
import regions as regmod

GUARD = 20


class ThreeBody(Exception):
    pass


class Catalog:
    def __init__(self, lib):
        self.lib = lib
        self.rows = {}
        for r in json.load(open("collisions.json")):
            self.rows[(r["X"], r["Y"], r["cls"])] = r
        self.reg = json.load(open(regmod.OUT))
        self.reps = {}
        self.added = 0

    def classes(self, X, Y):
        if (X, Y) not in self.reps:
            gx, gy = self.lib.gliders[X], self.lib.gliders[Y]
            PX, PY = (gx.p, gx.d), (gy.p, gy.d)
            reps = canonical_reps(self.lib, X, Y)
            self.reps[(X, Y)] = [(class_key(q, PX, PY), q) for q in reps]
            if (X, Y, 0) not in self.rows:
                self._compute(X, Y)
        return self.reps[(X, Y)]

    def _compute(self, X, Y):
        for r in collide_pair(self.lib, X, Y):
            if not r["settled"]:
                raise ThreeBody(f"{X}+{Y}#{r['cls']} does not settle")
            self.rows[(X, Y, r["cls"])] = r
            self.reg[regmod.key(r)] = regmod.region(self.lib, r)
            self.added += 1

    def lookup(self, X, Y, rel):
        """-> (catalog row, region, (a*pX, a*dX)) for Y at rel from X."""
        gx, gy = self.lib.gliders[X], self.lib.gliders[Y]
        PX, PY = (gx.p, gx.d), (gy.p, gy.d)
        key = class_key(rel, PX, PY)
        for k, (kk, rep) in enumerate(self.classes(X, Y)):
            if kk == key:
                break
        else:
            raise ValueError(f"{X}+{Y}: relative event {rel} not "
                             "ether-compatible")
        d = (rel[0] - rep[0], rel[1] - rep[1])
        det = PX[0] * PY[1] - PX[1] * PY[0]
        a = Fraction(d[0] * PY[1] - d[1] * PY[0], det)
        assert a.denominator == 1
        a = int(a)
        row = self.rows[(X, Y, k)]
        return row, self.reg[regmod.key(row)], (a * PX[0], a * PX[1])


class GliderSim:
    def __init__(self, lib, gliders, cat=None):
        self.lib = lib
        self.cat = cat or Catalog(lib)
        # kept in left-to-right order; the order changes only at collisions
        self.gl = sorted((tuple(g) for g in gliders),
                         key=lambda g: self.span(g, 0)[0])
        self.t = 0
        self.log = []

    def span(self, g, t):
        bits, _, _, s = self.lib.gliders[g[0]].state_at(g[1], g[2], t)
        return s, s + len(bits)

    def v(self, g):
        return self.lib.gliders[g[0]].velocity

    def next_collision(self):
        best = None
        for L, R in zip(self.gl, self.gl[1:]):
            if not self.v(L) > self.v(R):
                continue
            rel = (R[1] - L[1], R[2] - L[2])
            row, reg, sh = self.cat.lookup(L[0], R[0], rel)
            off = (L[1] + sh[0], L[2] + sh[1])
            ts, te = reg[0] + off[0], reg[1] + off[0]
            box = (reg[2] + off[1], reg[3] + off[1])
            if best is None or ts < best[0]:
                best = (ts, te, box, L, R, row, off)
        return best

    def clear_of(self, g, ts, te, box):
        """Does glider g stay >= GUARD cells from box during [ts, te]?"""
        lo, hi = box
        # quick reject by linear bounds (widths and phase offsets <= 80)
        s0, _ = self.span(g, ts)
        s1, _ = self.span(g, te)
        if min(s0, s1) - 120 > hi + GUARD or max(s0, s1) + 120 < lo - GUARD:
            return True
        for t in range(ts, te + 1):
            a, b = self.span(g, t)
            if b > lo - GUARD and a < hi + GUARD:
                return False
        return True

    def run(self, T_end, max_events=10 ** 6):
        for _ in range(max_events):
            nxt = self.next_collision()
            if nxt is None or nxt[0] > T_end:
                self.t = T_end
                return
            ts, te, box, L, R, row, off = nxt
            if ts < self.t:
                raise AssertionError("collision in the past (ordering bug)")
            if te > T_end:
                raise ThreeBody(f"collision {L[0]}+{R[0]} unfinished at "
                                f"T_end={T_end} (t {ts}..{te})")
            for g in self.gl:
                if g is L or g is R:
                    continue
                if not self.clear_of(g, ts, te, box):
                    raise ThreeBody(f"{g[0]} enters {L[0]}+{R[0]}#"
                                    f"{row['cls']} region t={ts}..{te} "
                                    f"x={box}")
            i = self.gl.index(L)
            if self.gl[i + 1] is not R:
                raise AssertionError("colliding pair not adjacent")
            new = []
            for n, t0, x0 in row["products"]:
                p = self.lib.gliders[n].p
                t, x = t0 + off[0], x0 + off[1]
                tt = t % p
                new.append((n, tt, x - (t - tt) // p * self.lib.gliders[n].d))
            new.sort(key=lambda g: self.span(g, te)[0])
            self.gl[i:i + 2] = new
            self.log.append((ts, te, L[0], R[0], row["cls"],
                             [p[0] for p in row["products"]]))
            self.t = ts
        raise RuntimeError("too many events")

    def state(self):
        def norm(g):
            gg = self.lib.gliders[g[0]]
            tt = g[1] % gg.p
            return (g[0], tt, g[2] - (g[1] - tt) // gg.p * gg.d)
        return sorted(norm(g) for g in self.gl)


# ---------------------------------------------------------------------------
# validation against the automaton

def random_scene(lib, names, n, rnd, gap=(20, 160)):
    """n gliders left to right with random types, time phases and
    ether-compatible gaps. -> list of (name, t0, x0)."""
    scene = []
    end = 0
    rph_abs = None
    for i in range(n):
        name = rnd.choice(names)
        g = lib.gliders[name]
        t0 = -rnd.randrange(g.p)
        bits, l, r, s_rel = g.state_at(t0, 0, 0)
        if rph_abs is None:
            x0 = 0
        else:
            xmin = end + rnd.randint(*gap) - s_rel
            # left ether abs phase (l - s) must equal rph_abs:
            base = (l - s_rel - rph_abs) % TILE
            x0 = xmin + (base - xmin) % TILE
        bits, l, r, s = g.state_at(t0, x0, 0)
        scene.append((name, t0, x0))
        end = s + len(bits)
        rph_abs = (r - s) % TILE
    return scene


def validate(n_scenes, seed=0, n_gliders=6, T=2500):
    lib = Library.load()
    cat = Catalog(lib)
    rnd = random.Random(seed)
    names = ["A", "B", "C1", "C2", "C3", "D1", "D2", "E", "Ebar", "F", "G",
             "A^4", "Bbar"]
    stats = {"agree": 0, "threebody": 0, "ca_unsettled": 0, "DISAGREE": 0}
    for i in range(n_scenes):
        scene = random_scene(lib, names, n_gliders, rnd)
        sim = GliderSim(lib, scene, cat)
        try:
            sim.run(T)
        except ThreeBody:
            stats["threebody"] += 1
            continue
        from collide import products_of, _pack_batch, _step_state, _unpack_batch
        from r110lib import build_row
        sts = [lib.gliders[nm].state_at(t0, x0, 0) for nm, t0, x0 in scene]
        row, x0 = build_row(sts, pad=T + 200)
        s = _pack_batch(row[None, :])
        for _ in range(T):
            s = _step_state(s)
        final = _unpack_batch(s, 1)[0]
        # cell-exact comparison: the row predicted from the simulator's
        # glider list (free gliders at time T) must equal the CA row
        from regions import free_row
        from r110lib import TILE as _T
        cL0 = (sts[0][1] - sts[0][3]) % _T
        pred = free_row(lib, sim.gl, T, x0, len(final), cL0)
        if pred is None:
            stats["ca_unsettled"] += 1      # gliders still overlapping at T
            continue
        import numpy as _np
        if _np.array_equal(pred, final):
            stats["agree"] += 1
        else:
            stats["DISAGREE"] += 1
            bad = _np.nonzero(pred != final)[0]
            print("DISAGREE scene", scene, "cells", len(bad),
                  "first col", int(bad[0]) + x0)
            print("  sim", sim.state())
            print("  log", sim.log)
    print(stats, "pairs computed on demand:", cat.added)
    return stats


if __name__ == "__main__":
    if sys.argv[1] == "validate":
        validate(int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 0)
