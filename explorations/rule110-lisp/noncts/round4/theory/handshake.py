"""handshake.py - exact two-gap transfers by a per-unit HANDSHAKE, under
realistic window kinematics (lead's task 1, 00:4x).

Layout (route 20/23 geometry, M fixed at 0):

    [left stream ->]  W_L ~~g1~~ M ~~g2~~ W_R  [<- right stream]

- Streams: left packets move right at vL, right packets move left at vR,
  one packet every P time units at a fixed point (Doppler is exact: a
  window at position a meets left packet m at t = m P + (a - cL)/vL).
- Windows never move on their own (closed).  A TOKEN (a signal crossing the
  gaps, crossing M) ARMS a window with a displacement d in {-1, 0, +1}
  counter units; at the window's NEXT stream packet the window takes that
  step (step size s, which may be much smaller than the packet spacing:
  no jumping over packets) and emits the next token toward the other
  window.  The token's type is the finite control.
- So every counter unit is moved by exactly one token arrival: transfers
  are exact BY CONSTRUCTION, whatever the skew.  What the kinematics can
  still break is the PHASE at which a token meets a window or crosses M:
  physical arming/crossing reactions are multi-class and have failure
  bands (delayline 00:19: 1 arrival phase in 6 gives debris).  The model
  records every arrival phase and counts arrivals inside a failure band.

Finite control and compiler: exactly bouncer.py's reflection table
(Minsky -> round-3 transfer machine -> table (token, wall) -> (d, token')),
with 'W1'/'Z01' = W_L (g1 > 0 / g1 = 0, contact with M) and 'W2'/'Z23'
= W_R.  Zero test = the window is in contact with M when the token arrives.

Phase-locking condition [thm, below; checked here]: if each token moves at
the SAME speed as the packets of the stream of the window that emits it
(L->R tokens at vL, R->L tokens at vR), then (i) every token crosses M at
the same stream phase, and (ii) if moreover s (1/vL + 1/vR) is a multiple
of P, every token meets each window at one fixed phase of that window's
stream, for all counter values.  Then a failure band can be avoided by
the choice of the stream offsets.
Run: python3 handshake.py   (exit 0 = all checks as predicted)
"""
import os, sys, math, random
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '../../round3/theory'))
sys.path.insert(0, os.path.join(HERE, '../../scholar'))
from bouncer import compile_bouncer, max_reg
from lm import decode
from csm import run_minsky, random_minsky


class Geo:
    def __init__(self, s, vL, vR, P, vTL, vTR, cL=Fr(0), cR=Fr(0), beta=Fr(1, 6)):
        self.s, self.vL, self.vR, self.P = Fr(s), Fr(vL), Fr(vR), Fr(P)
        self.vTL, self.vTR = Fr(vTL), Fr(vTR)       # token speeds L->R and R->L
        self.cL, self.cR, self.beta = Fr(cL), Fr(cR), Fr(beta)

    def next_left(self, a, t):
        """first left-stream packet arrival at window position a strictly after t."""
        base = (a - self.cL) / self.vL
        m = math.floor((t - base) / self.P) + 1
        return m * self.P + base

    def next_right(self, b, t):
        base = (self.cR - b) / self.vR
        n = math.floor((t - base) / self.P) + 1
        return n * self.P + base


def run_handshake(T, h, g1, g2, geo, max_events=10 ** 7):
    """Simulate; returns dict with final counters, halted flag and phase stats."""
    s = geo.s
    pos_L = lambda g: -(g + 1) * s
    pos_R = lambda g: (g + 1) * s
    # first token: emitted by W_R at time 0, heading left
    t_e, x_e, side = Fr(0), pos_R(g2), 'L'
    ph = {'L': set(), 'R': set(), 'M': set()}
    band = 0
    for ev in range(max_events):
        if side == 'L' and h in T.halt:
            return dict(g1=g1, g2=g2, halted=True, events=ev, ph=ph, band=band)
        if side == 'L':
            xa = pos_L(g1)
            t_c = t_e + (x_e - 0) / geo.vTR              # crossing M
            t_a = t_e + (x_e - xa) / geo.vTR
            ph['M'].add(t_c % geo.P)
            last = geo.next_left(xa, t_a) - geo.P        # last packet at or before t_a
            phase = (t_a - last) % geo.P
            ph['L'].add(phase)
            band += phase < geo.beta * geo.P
            d, h = T.r[(h, 'Z01' if g1 == 0 else 'W1')]
            t_s = geo.next_left(xa, t_a)                  # the armed window steps here
            g1 += d
            if g1 < 0:
                raise AssertionError('W_L crossed M')
            t_e, x_e, side = t_s, pos_L(g1), 'R'
        else:
            xb = pos_R(g2)
            t_c = t_e + (0 - x_e) / geo.vTL
            t_a = t_e + (xb - x_e) / geo.vTL
            ph['M'].add(t_c % geo.P)
            last = geo.next_right(xb, t_a) - geo.P
            phase = (t_a - last) % geo.P
            ph['R'].add(phase)
            band += phase < geo.beta * geo.P
            d, h = T.r[(h, 'Z23' if g2 == 0 else 'W2')]
            t_s = geo.next_right(xb, t_a)
            g2 += d
            if g2 < 0:
                raise AssertionError('W_R crossed M')
            t_e, x_e, side = t_s, pos_R(g2), 'L'
    return dict(g1=g1, g2=g2, halted=False, events=max_events, ph=ph, band=band)


def differential(geo, n_random=120, seed=3, budget=60, regmax=3, variant='ok'):
    rng = random.Random(seed)
    tests = [([('DEC', 0, 1, 2), ('INC', 1, 0), ('HALT',)], [3, 2]),
             ([('DEC', 1, 1, 3), ('INC', 0, 2), ('INC', 0, 0), ('HALT',)], [0, 3])]
    for _ in range(n_random):
        tests.append((random_minsky(rng.randrange(2, 7), rng=rng), [rng.randrange(3), rng.randrange(3)]))
    compared = fails = 0
    phases = {'L': set(), 'R': set(), 'M': set()}
    band = 0
    events = 0
    for prog, regs in tests:
        mreg, ms, mh = run_minsky(prog, regs, budget)
        if not mh or max_reg(prog, regs, budget) > regmax:
            continue
        compared += 1
        Tb, h0 = compile_bouncer(prog, variant)
        try:
            r = run_handshake(Tb, h0, 2 ** regs[0] * 3 ** regs[1], 0, geo, max_events=300000)
            ok = r['halted'] and r['g2'] == 0 and decode(r['g1']) == (mreg, 1)
            for k in phases:
                phases[k] |= r['ph'][k]
            band += r['band']
            events += r['events']
        except (KeyError, AssertionError):
            ok = False
        fails += not ok
    return dict(compared=compared, fails=fails, nphase={k: len(v) for k, v in phases.items()},
                band=band, events=events)


def best_offsets(make_geo, grid=12):
    """Search stream offsets (cL, cR) on a grid of P/grid steps for the fewest
    band hits, using a small sample of programs (phase sets do not depend on
    the program, only on the step types used)."""
    best = None
    for i in range(grid):
        for j in range(grid):
            g = make_geo(i, j)
            r = differential(g, n_random=12, seed=9)
            key = (r['band'], i, j)
            if best is None or key < best[0]:
                best = (key, r)
            if r['band'] == 0:
                return (i, j), r
    return best[0][1:], best[1]


def main():
    vL, vR = Fr(2, 3), Fr(1, 3)        # left stream: A-lattice trains; right stream: G-speed packets
    s = Fr(78)                          # window step per armed packet (cells)
    P = s * (1 / vL + 1 / vR)           # phase-locking period: 351 (spacing 234 / 117 cells)
    mk_locked = lambda i, j: Geo(s, vL, vR, P, vTL=vL, vTR=vR, cL=P * vL * i / 12, cR=P * vR * j / 12)
    mk_offP = lambda i, j: Geo(s, vL, vR, P + 7, vTL=vL, vTR=vR, cL=(P + 7) * vL * i / 12, cR=(P + 7) * vR * j / 12)
    (i, j), _ = best_offsets(mk_locked)
    r1 = differential(mk_locked(i, j))
    print(f'LOCKED (tokens at their stream speed, P = s(1/vL+1/vR) = {P}), offsets {i},{j}/12:', r1)
    (i2, j2), rA = best_offsets(mk_offP)
    r2 = differential(mk_offP(i2, j2))
    print(f'control A (period P+7), best offsets {i2},{j2}/12:', r2)
    r4 = differential(mk_locked(i, j), variant='norem')
    print("control C (remainder ignored):", r4)
    # value-independence of the phase sets: big counters, one long transfer each way
    big = {}
    for name, g in (('locked', mk_locked(i, j)), ('P+7', mk_offP(i2, j2))):
        prog = [('DEC', 0, 1, 2), ('INC', 1, 0), ('HALT',)]       # moves register a into b
        Tb, h0 = compile_bouncer(prog)
        ph = {'L': set(), 'R': set(), 'M': set()}
        for a in (3, 5, 7):
            r = run_handshake(Tb, h0, 2 ** a, 0, g)
            for k in ph:
                ph[k] |= r['ph'][k]
        big[name] = {k: len(v) for k, v in ph.items()}
    print('phase-set sizes with registers up to 7 (x up to 128):', big)
    bounded = all(big['locked'][k] <= max(r1['nphase'][k], 1) for k in ('L', 'R'))
    grows = sum(big['P+7'][k] for k in ('L', 'R')) > sum(big['locked'][k] for k in ('L', 'R'))
    ok = (r1['fails'] == 0 and r1['compared'] > 0 and r1['band'] == 0
          and r2['fails'] == 0 and r2['band'] > 0 and r4['fails'] > 0 and bounded and grows)
    print('as predicted:', ok)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
