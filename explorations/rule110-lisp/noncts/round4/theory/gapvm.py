"""gapvm.py - route 20: a full Minsky compiler on top of gap2.py's exact
transfer kinematics (two windows, two gaps, rate-matched transfers with
start/stop signals across the gaps; no per-unit handshake).

Pipeline: Minsky 2-counter program -> round 3's transfer machine (lm.py,
Goedel x = 2^a 3^b) -> sequence of PHYSICAL transfers:
  XY(p,1): source x (left gap) drained by W_L walking in, W_R walking out
           with mask (kL, kR) chosen so the slope is 1/p; the remainder r is
           READ from W_R's mask phase when the stop arrives (calibrated
           table phase -> r, plus a constant offset per r);
  YX(1,j): the mirror image (source y, destination x), slope j.
  Fix-ups: constant offsets and the remainder r are applied as single
  unit walks (a bounded number per transfer, chosen from the observed
  phase) - finite control only.
Calibration (compile time, once per geometry): run each transfer type on
g = 40..90 and tabulate (phase -> residue, offset).  Execution uses ONLY
the calibrated tables and the observed phases, never the true values.
Differential test vs scholar's Minsky interpreter on random programs.
Control: an incommensurate geometry (u = 5, P = 7) calibrated the same
way must fail.
Run: python3 gapvm.py
"""
import random, sys, os
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../round3/theory'))
sys.path.insert(0, os.path.join(HERE, '../../scholar'))
from gap2 import transfer
from lm import compile_minsky, decode
from csm import run_minsky, random_minsky

MASK = {('div', 2): (1, 5), ('div', 3): (1, 7), ('div', 1): (1, 3),
        ('mul', 1): (1, 3), ('mul', 2): (1, 2), ('mul', 3): (2, 2)}


def calibrate(geo):
    """(kind, p) -> {phase: (residue, offset)} with out = slope*g + offset,
    residue = g mod denominator(slope)."""
    cal = {}
    for (kind, p), (kL, kR) in MASK.items():
        slope = Fr(kL + 1, kR - 1)
        tab = {}
        for g in range(40, 91):
            try:
                out, _ = transfer(g, **geo, kL=kL, kR=kR)
            except RuntimeError:
                tab = None
                break
            ph = transfer.last_phase
            ent = (g % slope.denominator, out - slope * g)
            tab.setdefault(ph, set()).add(ent)
        cal[(kind, p)] = (slope, tab)
    return cal


def phys(cal, geo, kind, p, g):
    """Run one physical transfer of g units; decode the result with the
    calibrated table only.  Returns (exact quotient/product, residue) or
    raises if the observed phase is ambiguous / unknown."""
    kL, kR = MASK[(kind, p)]
    slope, tab = cal[(kind, p)]
    if g == 0:
        return 0, 0                       # nothing to move: the contact is immediate
    out, _ = transfer(g, **geo, kL=kL, kR=kR)
    ph = transfer.last_phase
    if tab is None or ph not in tab or len(tab[ph]) != 1:
        raise ValueError('phase does not determine the residue')
    r, off = next(iter(tab[ph]))
    # undo the constant offset (finite control: a fixed number of unit walks)
    val = out - off                       # = slope*g exactly when calibration is right
    if kind == 'div':
        # val = (g - r)/p + r/p ... slope*g = g/p; quotient = (g - r)/p
        q = val - Fr(r, p)
        return q, r
    return val, 0


def run_gap(states, q0, x, cal, geo, max_transfers):
    y = 0
    q = q0
    n = 0
    while n < max_transfers:
        s = states[q]
        if s[0] == 'HALT':
            return x, y, True, n
        kind, k, j, nxt = s
        if kind == 'XY':                  # x -> y, k = p, j = 1  (y is 0 here)
            assert j == 1 and y == 0
            qd, r = phys(cal, geo, 'div', k, x)
            x, y = Fr(r), qd              # remainder restored into x by r unit walks
            q = nxt[int(r)]
        else:                             # YX(1, j): y -> x (multiply), x keeps its r
            assert k == 1
            prod, _ = phys(cal, geo, 'mul', j, y)
            x, y = x + prod, 0
            q = nxt[0]
        n += 1
    return x, y, False, n


def differential(geo, n_random=150, seed=5, budget=40, regmax=3):
    cal = calibrate(geo)
    rng = random.Random(seed)
    tests = [([('DEC', 0, 1, 2), ('INC', 1, 0), ('HALT',)], [3, 2]),
             ([('DEC', 1, 1, 3), ('INC', 0, 2), ('INC', 0, 0), ('HALT',)], [0, 3])]
    for _ in range(n_random):
        tests.append((random_minsky(rng.randrange(2, 7), rng=rng), [rng.randrange(3), rng.randrange(3)]))
    compared = fails = 0
    for prog, regs in tests:
        mreg, ms, mh = run_minsky(prog, regs, budget)
        if not mh:
            continue
        # keep values small (each transfer is an exact event simulation)
        r2 = list(regs); pc = 0; big = False
        for _ in range(ms):
            ins = prog[pc]
            if ins[0] == 'INC':
                r2[ins[1]] += 1; pc = ins[2]
            elif ins[0] == 'DEC':
                if r2[ins[1]] == 0: pc = ins[3]
                else: r2[ins[1]] -= 1; pc = ins[2]
            if max(r2) > regmax: big = True
        if big:
            continue
        compared += 1
        states, q0 = compile_minsky(prog)
        try:
            x, y, h, n = run_gap(states, q0, 2 ** regs[0] * 3 ** regs[1], cal, geo, 2 * budget + 4)
            ok = h and y == 0 and x.denominator == 1 and decode(int(x)) == (mreg, 1)
        except (ValueError, KeyError, AssertionError, RuntimeError):
            ok = False
        fails += not ok
    return compared, fails


if __name__ == '__main__':
    com = dict(u=Fr(4), vp=Fr(1, 3), vs=Fr(2, 3), P=Fr(6))
    inc = dict(u=Fr(5), vp=Fr(1, 3), vs=Fr(2, 3), P=Fr(7))
    c1, f1 = differential(com)
    print(f'commensurate geometry: {c1} halting Minsky runs compared, {f1} failures (must be 0)')
    c2, f2 = differential(inc)
    print(f'CONTROL incommensurate geometry: {c2} compared, {f2} failures (must be > 0)')
    sys.exit(0 if f1 == 0 and f2 > 0 and c1 > 0 else 1)
