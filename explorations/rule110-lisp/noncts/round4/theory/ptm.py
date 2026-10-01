"""Particle Turing machines in Rule 110's phase-free sub-chemistry (route 12).

PHYSICS LAYER (exact Rule 110, collider's verified pipeline, read-only):
  react(head, cell) collides ONE rigid head packet with ONE stationary cell
  and returns the products. A head is a rigid packet of gliders that all
  share one period: (3,2) or (10,2) (moving right) or (4,-2) (moving left).
  By Lemma R4-L1 (THEORY.md) every such collision has exactly one class, so
  react() needs no placement parameter: any far-enough placement gives the
  same outcome up to translation.  react() checks this assumption on every
  call by recomputing the class count with collider's n_classes().

ABSTRACT LAYER (the natural TM):
  A tape of cells (index -> cell name), a head (packet, direction) sitting
  next to cell i.  One step = react(head, tape[i]).  A step is CLEAN if the
  products are exactly one stationary object (the new cell) plus a rigid
  packet of one head lattice (the new head), or one stationary object and
  nothing else (head absorbed: the run stops).  Anything else = DIRTY (the
  run stops).  The new head moves right (A/D lattice) or left (B lattice)
  and meets cell i+1 or i-1 next.  Cell displacements are recorded; with a
  large pitch they do not change outcomes (R4-L1), but unbounded drift would
  eventually make cells touch (R4-L2), so runs report the max drift.

Caveat (scope): the abstraction assumes the pitch is large enough that the
outgoing head is clear of the old cell before it meets the next one, and
that no product of a reaction lingers.  Every CLAIM built on a run must be
re-checked by one full Rule 110 simulation of the whole configuration
(see fullcheck() below).
"""
import os, sys
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
COLL = os.path.join(HERE, '../../collider')
sys.path.insert(0, COLL)
_cwd = os.getcwd(); os.chdir(COLL)
from library import Library
from collide import simulate, canonical_reps
from r110lib import n_classes, build_row
LIB = Library.load()          # in-memory only; never saved
os.chdir(_cwd)

RIGHT = {(3, 2), (10, 2)}
LEFT = {(4, -2)}
STAT = (7, 0)
T_MAX = 3000


def period(name):
    g = LIB.gliders[name]
    return (g.p, g.d)


def expand(pl):
    """Identity (kept for clarity).  Library compounds are NOT replaced by
    their parsed parts: collider's part events do not reassemble into a
    valid row with build_row (checked on B_2_B_4_B_2_B, 23:2x), so the
    representation used everywhere is the library's own identification of
    the products.  Within one process that identification is unique."""
    return list(pl)
    out = []
    for name, t0, x0 in pl:
        g = LIB.gliders[name]
        if g.parts:
            for nm, pt, px in g.parts:
                out.append((nm, t0 + pt, x0 + px))
        else:
            out.append((name, t0, x0))
    return out


def norm_event(name, t, x, tmin=0):
    """Move a seed event along the glider's own trajectory so t in [tmin, tmin+p)."""
    g = LIB.gliders[name]
    m = (t - tmin) // g.p
    return (name, t - m * g.p, x - m * g.d)


def canon(pl):
    """Translation-invariant key of a rigid packet [(name, t0, x0)]."""
    pl = [norm_event(*e) for e in expand(pl)]
    def lat(e):
        g = LIB.gliders[e[0]]
        return Fraction(e[2]) - Fraction(g.d, g.p) * e[1]
    a = min(pl, key=lambda e: (lat(e), e[1], e[0]))
    key = []
    for name, t, x in pl:
        key.append(norm_event(name, t - a[1], x - a[2]))
    return tuple(sorted(key))


def direction(key):
    ps = {period(n) for n, _, _ in key}
    assert len(ps) == 1, ('not rigid', key)
    p = ps.pop()
    return 'R' if p in RIGHT else 'L' if p in LEFT else None


def _start(e):
    name, t0, x0 = e
    return LIB.gliders[name].state_at(t0, x0, 0)[3]


_cache = {}


def rephase(pl):
    """Translate the packet by an ether-lattice vector (dt, dx), dx = -4 dt
    mod 14, so that its gliders' time-0 states assemble into a valid row
    (tight packets can have touching per-glider representations at some
    phases). Physics is unchanged; only the representation moves."""
    for dt in range(0, 42):
        dx = (-4 * dt) % 14
        q = [(n, t + dt, x + dx) for n, t, x in pl]
        try:
            build_row([LIB.gliders[n].state_at(t, x, 0) for n, t, x in q])
            return q
        except ValueError:
            continue
    return None


def react(hkey, cell):
    """Collide head packet hkey (canonical key) with stationary cell `cell`.
    -> dict(kind='clean'|'absorbed'|'dirty', cell=..., head=..., dx=..., raw=...)."""
    ck = (hkey, cell)
    if ck in _cache:
        return _cache[ck]
    d = direction(hkey)
    pl = rephase(list(hkey))
    if pl is None:
        out = {'kind': 'dirty', 'why': 'no clean time-0 representation of the head'}
        _cache[ck] = out
        return out
    hp, cp = period(pl[0][0]), period(cell)
    assert cp == STAT and n_classes(hp, cp) == 1, (hp, cp)   # Lemma R4-L1
    if d == 'R':
        G = max(pl, key=_start)
        tY, xY = canonical_reps(LIB, G[0], cell)[0]
        cpl = (cell, G[1] + tY, G[2] + xY)
    else:
        G = min(pl, key=_start)
        tX, xX = canonical_reps(LIB, cell, G[0])[0]   # G relative to cell at (0,0)
        cpl = (cell, G[1] - tX, G[2] - xX)
    try:
        res = simulate(LIB, pl + [cpl], T_MAX)
    except (ValueError, RuntimeError) as e:
        out = {'kind': 'dirty', 'why': repr(e)}
        _cache[ck] = out
        return out
    prods = res['products']
    out = {'raw': prods, 'settled': res['settled']}
    if not res['settled'] or any(p[0] == '?' for p in prods):
        out['kind'] = 'dirty'
    else:
        st = [p for p in prods if period(p[0]) == STAT]
        mv = [p for p in prods if period(p[0]) != STAT]
        pers = {period(p[0]) for p in mv}
        if len(st) != 1 or len(pers) > 1 or (pers and not (pers <= RIGHT | LEFT)):
            out['kind'] = 'dirty'
        else:
            out['cell'] = st[0][0]
            out['dx'] = st[0][2] - cpl[2]        # seed-x displacement of the cell
            if mv:
                out['kind'] = 'clean'
                out['head'] = canon(mv)
            else:
                out['kind'] = 'absorbed'
    _cache[ck] = out
    return out


def run(hkey, blank, init=None, start=0, nmax=400):
    """Natural TM on a tape that is `blank` everywhere except init {i: cell}.
    The head starts next to cell `start` (moving its own direction).
    -> dict(outcome, steps, heads, cells, lo, hi, drift, trace)."""
    tape = dict(init or {})
    drift = {}
    i, h = start, hkey
    heads, cells, trace = {h}, set(tape.values()) | {blank}, []
    seen_fresh = {}
    pos = []
    lo = hi = i
    for step in range(nmax):
        c = tape.get(i, blank)
        r = react(h, c)
        trace.append((i, c, r['kind']))
        if r['kind'] != 'clean':
            return dict(outcome=r['kind'], steps=step, heads=len(heads), cells=len(cells),
                        lo=lo, hi=hi, drift=max(map(abs, drift.values()), default=0), trace=trace)
        tape[i] = r['cell']
        drift[i] = drift.get(i, 0) + r['dx']
        h = r['head']
        heads.add(h); cells.add(r['cell'])
        i += 1 if direction(h) == 'R' else -1
        pos.append(i)
        # escape detector: the head enters virgin blank territory on the same
        # side in the same head state twice, and in between never went back
        # behind the first entry point: then the run repeats by translation.
        if i not in tape and (i > hi or i < lo):
            side = 'R' if i > hi else 'L'
            k = (h, side)
            if k in seen_fresh:
                s1, p1 = seen_fresh[k]
                between = pos[s1:]
                ok = min(between) >= p1 if side == 'R' else max(between) <= p1
            else:
                ok = False
            if ok:
                return dict(outcome='escape', steps=step + 1, heads=len(heads), cells=len(cells),
                            lo=lo, hi=hi, drift=max(map(abs, drift.values()), default=0), trace=trace)
            seen_fresh[k] = (len(pos) - 1, i)
        lo, hi = min(lo, i), max(hi, i)
    return dict(outcome='alive', steps=nmax, heads=len(heads), cells=len(cells), lo=lo, hi=hi,
                drift=max(map(abs, drift.values()), default=0), trace=trace)
