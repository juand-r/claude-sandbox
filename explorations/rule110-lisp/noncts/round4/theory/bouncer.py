"""bouncer.py - the BOUNCER MACHINE (route 14 in ROUTES.md): a stream-free
two-counter machine made of ONE head bouncing between two movable walls.

Geometry (all walls stationary objects, head = rigid packet):

    W0 (fixed)  ~x~  W1  <-- head bounces -->  W2  ~y~  W3 (fixed)

  x = (p1 - p0 - g) / u,   y = (p3 - p2 - g) / u.
  A head moving LEFT (B lattice) hits W1 from the right and reflects into a
  right-mover (A or D lattice); a head moving RIGHT hits W2 from the left
  and reflects into a left-mover.  Every reflection may move its wall by
  -u, 0 or +u (that is the INC/DEC: the wall moves, the counter changes).
  When x = 0, W1 sits at the fixed small distance g from W0 and the pair is
  a compound Z01; a head meeting Z01 has a DIFFERENT reaction (zero test).
  Same for y with Z23.  By Lemma L1 every head-wall collision is
  single-class, so nothing depends on distances or times: the machine is
  exactly its reaction table.  No streams, no passes (Lemma L4 is about
  heads that must cross cells; here the head never crosses a wall).

Abstract model: head types are integers; the reaction table maps
  (head, wall)  with wall in {'W1', 'Z01', 'W2', 'Z23'}
  -> (dx or dy in {-1, 0, +1}, new head)
'W1'/'Z01' reactions are L-reflections, 'W2'/'Z23' R-reflections, and the
head alternates sides.  The simulator also tracks positions and times
(A speed 2/3, B speed 1/2) only to check that the geometry is consistent
(walls never cross, x, y >= 0); there is one head, so no three-body events.

Compiler: Minsky 2-counter program -> round 3's transfer machine (lm.py,
Goedel numbering, loops XY(k,1) and YX(1,j) with remainder branching)
-> bouncer reaction table.  A loop is a fixed PATTERN of round trips:
  XY(k,1): k round trips, each DECs x at W1; the k-th also INCs y at W2.
           If x hits 0 after r < k DECs of a period, the head meets Z01 at
           position r: the zero reaction for (loop, r) knows the remainder,
           and a one-shot sequence of r INC-x round trips restores x = r.
  YX(1,j): j round trips; the first DECs y at W2 (so a zero of y is seen at
           the START of a period, before any INC x), every one INCs x.
Differential test vs scholar's Minsky interpreter (via lm.py's compiler).
Controls (must fail): (a) zero reactions that ignore the position r
('norem'); (b) XY loops that INC y at the FIRST round trip of a period
instead of the last ('early').
Run: python3 bouncer.py
"""
import os, random, sys
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../round3/theory'))
sys.path.insert(0, os.path.join(HERE, '../../scholar'))
from lm import compile_minsky, decode          # read-only reuse
from csm import run_minsky, random_minsky     # read-only reuse

U, G = 10, 6            # wall step and compound spacing (abstract cells)
VA, VB = Fraction(2, 3), Fraction(1, 2)


class Table:
    """Reaction table under construction: new head ids on demand."""
    def __init__(self):
        self.r = {}       # (head, wall) -> (delta, new_head)
        self.n = 0
        self.halt = set()

    def new(self):
        self.n += 1
        return self.n - 1


def compile_bouncer(prog, variant='ok'):
    """Return (table, start_head).  Convention: every lm state's entry head
    is a LEFT-mover about to meet W1 (or Z01 if x = 0).  A round trip (RT)
    is a W1-side reflection followed by a W2-side reflection.
    Reactions that are not zero tests are defined identically on the plain
    wall and on the compound (the compound must look like a wall to them);
    zero tests are the only places where W1 vs Z01 (W2 vs Z23) differ."""
    states, q0 = compile_minsky(prog)
    T = Table()
    entry = {q: T.new() for q in states}

    def left(h, d, m, test=None):
        """h meets W1 (x side): x += d, becomes m.  test = (d0, m0) for Z01."""
        T.r[(h, 'W1')] = (d, m)
        T.r[(h, 'Z01')] = test if test is not None else (d, m)

    def right(m, d, h, test=None):
        T.r[(m, 'W2')] = (d, h)
        T.r[(m, 'Z23')] = test if test is not None else (d, h)

    def rt(h, dx, dy, nxt):
        m = T.new()
        left(h, dx, m)
        right(m, dy, nxt)

    def restore(r, target):
        if r == 0:
            return target
        hs = [T.new() for _ in range(r)]
        for i, h in enumerate(hs):
            rt(h, +1, 0, hs[i + 1] if i + 1 < r else target)
        return hs[0]

    for q, st in states.items():
        h0 = entry[q]
        if st[0] == 'HALT':
            T.halt.add(h0)
            continue
        kind, k, j, nxt = st
        if kind == 'XY':                                   # XY(k, 1)
            assert j == 1
            pos = [h0] + [T.new() for _ in range(k - 1)]
            for i, h in enumerate(pos):
                inc_y = (i == k - 1) if variant != 'early' else (i == 0)
                m = T.new()
                r = i if variant != 'norem' else 0
                mz = T.new()                                 # zero branch right-mover
                left(h, -1, m, test=(0, mz))                 # Z01: x == 0 after i DECs
                right(m, +1 if inc_y else 0, pos[(i + 1) % k])
                right(mz, 0, restore(r, entry[nxt[r]]))
        else:                                              # YX(1, j)
            assert k == 1
            a = h0
            bs = [T.new() for _ in range(j)]
            ma = T.new()
            left(a, 0, ma)
            right(ma, -1, bs[0], test=(0, entry[nxt[0]]))  # Z23: y == 0
            for i, b in enumerate(bs):
                m = T.new()
                left(b, +1, m)
                if i + 1 < j:
                    right(m, 0, bs[i + 1])
                else:
                    right(m, -1, bs[0], test=(0, entry[nxt[0]]))
    return T, entry[q0]


def run_bouncer(T, h, x, y, max_events, check_geometry=True):
    """Event simulation. Returns (x, y, halted, events, reactions_used)."""
    p0, p3 = 0, 10 ** 9
    p1, p2 = p0 + G + U * x, p3 - G - U * y
    pos, t, side = Fraction(p2 + p1, 2), Fraction(0), 'L'   # head between W1 and W2, moving left
    used = set()
    for ev in range(max_events):
        if h in T.halt:
            return x, y, True, ev, used
        if side == 'L':
            wall = 'Z01' if x == 0 else 'W1'
            t += (pos - p1) / VB
            pos = Fraction(p1)
            key = (h, wall)
            if key not in T.r:
                raise KeyError(f'missing reaction {key} (x={x}, y={y})')
            d, h = T.r[key]
            used.add(key)
            x += d
            if x < 0:
                raise AssertionError('x < 0: W1 crossed W0')
            p1 = p0 + G + U * x
            side = 'R'
        else:
            wall = 'Z23' if y == 0 else 'W2'
            t += (p2 - pos) / VA
            pos = Fraction(p2)
            key = (h, wall)
            if key not in T.r:
                raise KeyError(f'missing reaction {key} (x={x}, y={y})')
            d, h = T.r[key]
            used.add(key)
            y += d
            if y < 0:
                raise AssertionError('y < 0: W2 crossed W3')
            p2 = p3 - G - U * y
            side = 'L'
        if check_geometry and not (p0 < p1 < p2 < p3):
            raise AssertionError('walls out of order')
    return x, y, False, max_events, used


def differential(n_random=300, seed=11, budget=400, variant='ok'):
    rng = random.Random(seed)
    tests = [([('DEC', 0, 1, 2), ('INC', 1, 0), ('HALT',)], [3, 4]),
             ([('DEC', 1, 1, 3), ('INC', 0, 2), ('INC', 0, 0), ('HALT',)], [0, 7])]
    for _ in range(n_random):
        tests.append((random_minsky(rng.randrange(2, 8), rng=rng),
                      [rng.randrange(4), rng.randrange(4)]))
    fails = halting = 0
    nreact = []
    for prog, regs in tests:
        mreg, msteps, mh = run_minsky(prog, regs, budget)
        T, h0 = compile_bouncer(prog, variant)
        x0 = 2 ** regs[0] * 3 ** regs[1]
        try:
            x, y, h, ev, used = run_bouncer(T, h0, x0, 0, 400000)
        except (KeyError, AssertionError):
            fails += 1
            continue
        if mh:
            halting += 1
            regs_out, rest = decode(x)
            ok = h and y == 0 and rest == 1 and regs_out == mreg
            nreact.append((len(prog), len(T.r)))
        else:
            ok = not h
        fails += not ok
    return len(tests), halting, fails, nreact


def main():
    total, halting, fails, nreact = differential()
    _, _, f_norem, _ = differential(variant='norem')
    _, _, f_early, _ = differential(variant='early')
    print(f'bouncer compile: {total} tests ({halting} halting), {fails} failures (must be 0)')
    print(f"control 'norem' (zero reaction ignores the remainder): {f_norem} failures (must be > 0)")
    print(f"control 'early' (XY increments y at the start of a period): {f_early} failures (must be > 0)")
    if nreact:
        ratio = sum(r for _, r in nreact) / sum(n for n, _ in nreact)
        print(f'reaction-table size: {ratio:.1f} reactions per Minsky instruction (mean over halting tests)')
    return 1 if fails or f_norem == 0 or f_early == 0 else 0


if __name__ == '__main__':
    sys.exit(main())
