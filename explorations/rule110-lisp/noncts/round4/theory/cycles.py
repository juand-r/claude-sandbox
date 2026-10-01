"""Graph search on head-wall reaction tables (routes 12 and 14).

A table maps (head, wall) -> (kind, wall_out, dx, head_out, dir_out), where
kind in {'reflect', 'pass', 'absorbed', 'dirty', ...}; heads carry their
direction ('R' = A/D lattice, moving right; 'L' = B lattice, moving left).
Every entry is one exact single-class reaction (Lemma L1), so these
dynamics ARE the Rule 110 dynamics as long as reactions do not overlap.

Searches:
  bouncers(T)   perpetual bouncer: one head between a left wall V and a
                right wall W, alternating R- and L-reflections, until the
                state (head, V, W, side) repeats.  Reports period and net
                wall displacement per period (nonzero = a non-periodic,
                stream-free process: the interval grows or shrinks).
  ratchets(T)   natural TM on a uniform tape of one wall type: runs that
                survive many steps (escapes = translation cycles, with net
                crossing; bounded = bouncers inside the tape).
Backends: DictTable (from JSONL rows; shuttle's tables when they land) and
SyntheticTable (tests).  Run `python3 cycles.py test` for the controls.
"""
import json, sys
from collections import defaultdict


class DictTable:
    def __init__(self):
        self.t = {}
        self.dir = {}

    def add(self, h, hdir, w, kind, w_out=None, dx=0, h_out=None, dir_out=None):
        self.t[(h, w)] = (kind, w_out, dx, h_out, dir_out)
        self.dir[h] = hdir
        if h_out is not None:
            self.dir.setdefault(h_out, dir_out)

    def react(self, h, w):
        return self.t.get((h, w))          # None = unknown (not in the table)

    def heads(self, d):
        return [h for h, x in self.dir.items() if x == d]

    def walls(self):
        return sorted({w for _, w in self.t})


def bounce_run(T, h, V, W, nmax=200):
    """h moves right toward W; V is the left wall."""
    walls = {'L': V, 'R': W}
    disp = {'L': 0, 'R': 0}
    side = 'R'
    seen = {}
    for step in range(nmax):
        st = (h, walls['L'], walls['R'], side)
        if st in seen:
            s0, d0 = seen[st]
            return ('BOUNCER', step - s0, disp['L'] - d0['L'], disp['R'] - d0['R'], s0)
        seen[st] = (step, dict(disp))
        r = T.react(h, walls[side])
        if r is None:
            return ('unknown', step)
        kind, w_out, dx, h_out, dir_out = r
        if kind != 'reflect':
            return (kind, step)
        walls[side] = w_out
        disp[side] += dx
        h = h_out
        side = 'L' if side == 'R' else 'R'
    return ('alive', nmax)


def bouncers(T, nmax=200, walls=None):
    """All (h, V, W) with h + W a reflection; returns found bouncers and the
    distribution of run lengths."""
    walls = walls or T.walls()
    found, lengths = [], defaultdict(int)
    for (h, W), r in list(T.t.items()):
        if T.dir.get(h) != 'R' or r[0] != 'reflect':
            continue
        hl = r[3]
        # only left walls on which hl reflects can matter
        Vs = [V for V in walls if (T.react(hl, V) or ('',))[0] == 'reflect']
        for V in Vs:
            res = bounce_run(T, h, V, W, nmax)
            if res[0] == 'BOUNCER':
                found.append((h, V, W, res))
            else:
                lengths[res[1]] += 1
    return found, dict(lengths)


def ratchet_run(T, h, blank, nmax=400):
    """Natural TM on a uniform tape; head starts left of cell 0 if moving
    right (right of cell 0 if moving left)."""
    tape, i = {}, 0
    pos = []
    seen_fresh = {}
    lo = hi = 0
    for step in range(nmax):
        r = T.react(h, tape.get(i, blank))
        if r is None:
            return ('unknown', step)
        kind, w_out, dx, h_out, dir_out = r
        if kind not in ('reflect', 'pass'):
            return (kind, step)
        tape[i] = w_out
        h = h_out
        i += 1 if dir_out == 'R' else -1
        pos.append(i)
        if i not in tape and (i > hi or i < lo):
            side = 'R' if i > hi else 'L'
            if (h, side) in seen_fresh:
                s1, p1 = seen_fresh[(h, side)]
                btw = pos[s1:]
                if (min(btw) >= p1) if side == 'R' else (max(btw) <= p1):
                    return ('ESCAPE', step + 1, len(pos) - 1 - s1)
            seen_fresh[(h, side)] = (len(pos) - 1, i)
        lo, hi = min(lo, i), max(hi, i)
    return ('ALIVE', nmax)


def ratchets(T, blanks=None, nmax=400):
    blanks = blanks or T.walls()
    out = []
    for h in list(T.dir):
        for b in blanks:
            res = ratchet_run(T, h, b, nmax)
            if res[0] in ('ESCAPE', 'ALIVE') or res[1] >= 4:
                out.append((h, b, res))
    return out


def _test():
    # positive control: a 2-wall bouncer that moves the right wall by +1 per period
    T = DictTable()
    T.add('a', 'R', 'W', 'reflect', 'W', +1, 'b', 'L')
    T.add('b', 'L', 'V', 'reflect', 'V', 0, 'a', 'R')
    T.add('b', 'L', 'X', 'dirty')
    found, _ = bouncers(T)
    ok1 = any(f[3][0] == 'BOUNCER' and f[3][3] == 1 for f in found)
    # a bouncer that needs two round trips (wall types alternate)
    T2 = DictTable()
    T2.add('a', 'R', 'W', 'reflect', 'W2', 0, 'b', 'L')
    T2.add('a', 'R', 'W2', 'reflect', 'W', 0, 'b', 'L')
    T2.add('b', 'L', 'V', 'reflect', 'V', 0, 'a', 'R')
    f2, _ = bouncers(T2)
    ok2 = any(f[3][1] == 4 for f in f2)
    # negative control: chain that dies
    T3 = DictTable()
    T3.add('a', 'R', 'W', 'reflect', 'W', 0, 'b', 'L')
    T3.add('b', 'L', 'V', 'reflect', 'V', 0, 'c', 'R')
    T3.add('c', 'R', 'W', 'dirty')
    f3, _ = bouncers(T3)
    ok3 = not f3
    # ratchet control: head passes blanks rewriting them -> escape
    T4 = DictTable()
    T4.add('a', 'R', 'c', 'pass', 'c2', 0, 'a', 'R')
    r4 = ratchet_run(T4, 'a', 'c')
    ok4 = r4[0] == 'ESCAPE'
    # zig-zag ratchet: pass c -> c1 (head b), reflect at c (head l), reflect at c1 -> c2 (head r2),
    # r2 passes c2 -> c3 becoming a again: net +1 per period through rewrites
    T5 = DictTable()
    T5.add('a', 'R', 'c', 'pass', 'c1', 0, 'b', 'R')
    T5.add('b', 'R', 'c', 'reflect', 'c', 0, 'l', 'L')
    T5.add('l', 'L', 'c1', 'reflect', 'c2', 0, 'r2', 'R')
    T5.add('r2', 'R', 'c', 'pass', 'c3', 0, 'a', 'R')
    r5 = ratchet_run(T5, 'a', 'c')
    ok5 = r5[0] == 'ESCAPE'
    print('controls: bouncer', ok1, 'two-trip bouncer', ok2, 'dying chain rejected', ok3,
          'pass ratchet', ok4, 'zig-zag ratchet', ok5, r5)
    return all([ok1, ok2, ok3, ok4, ok5])


if __name__ == '__main__':
    if sys.argv[1:] == ['test']:
        sys.exit(0 if _test() else 1)
