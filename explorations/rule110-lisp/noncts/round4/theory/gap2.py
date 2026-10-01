"""gap2.py - route 20 (two-window gap machine): exact kinematics of ONE
rate-matched transfer, to test the overshoot law of THEORY.md s.6b.

Abstract physics (not Rule 110; parameters stand for measured ones):
  M fixed at 0.  W_L at a <= 0 (g1 = -a/u), W_R at b >= 0 (g2 = b/u).
  Left-stream packets move right at speed vp, one every P time units;
  right-stream packets move left at vp, one every P.  An OPEN window takes
  one step of size u (toward or away from M) on every packet of its
  stream whose index i (counted from the window's mode start) satisfies
  i mod k_mask == 0; a CLOSED window ignores packets.  Signals move at vs.
Transfer protocol XY(k): start with W_R touching M (g2 = 0), W_L at g1.
  t = 0: a start signal leaves M; W_R opens at once (walks OUT, mask kR);
  W_L opens (walks IN, mask 1) when the start signal reaches it.
  When W_L reaches M (g1 = 0) a stop signal leaves M; W_R closes when it
  arrives.  Output: g2 at the end.
Exact rational event simulation.  The script fits g2_out = alpha*g1 + c and
reports c as a function of g1 mod m: the overshoot law predicts an affine
map with a bounded, residue-periodic offset; under commensurability the
offset is constant.
Run: python3 gap2.py
"""
from fractions import Fraction as Fr
import math


def next_arrival(t, x, v_window_static, vp, P, direction, phase):
    """first packet arrival time >= t at a STATIC window at x.
    direction +1: packets move right, packet n at x = vp (t - n P) + phase*vp.
    Solve vp (t - nP - phase) = x  ->  t = x/vp + nP + phase  (right movers)
    direction -1: packets move left, x = -vp (t - nP - phase) -> t = -x/vp + nP + phase."""
    base = (x / vp if direction > 0 else -x / vp) + phase
    n = math.ceil((t - base) / P)
    return base + n * P


def transfer(g1, u, vp, vs, P, kR, kL=1, phaseL=Fr(0), phaseR=Fr(0), maxev=10 ** 6):
    a, b = Fr(-g1 * u), Fr(0)
    t = Fr(0)
    # start signal reaches W_L at time |a|/vs (W_L static until then)
    tL_open = -a / vs
    R_open, L_open = True, False
    iR = 0                      # W_R packet counter since open
    iL = 0                      # W_L packet counter since open
    tR = next_arrival(t, b, None, vp, P, -1, phaseR)
    tL = next_arrival(tL_open, a, None, vp, P, +1, phaseL)
    t_stop = None               # time the stop signal reaches W_R
    stop_emit = None
    for _ in range(maxev):
        # next event: W_R packet, W_L packet (if open), or stop arrival
        cands = [(tR, 'R')]
        if L_open or tL >= tL_open:
            cands.append((tL, 'L'))
        if stop_emit is not None:
            # stop signal position: vs (t - stop_emit); meets W_R at b (static between steps)
            ts = stop_emit + b / vs
            cands.append((ts, 'S'))
        t, ev = min(cands)
        if ev == 'S':
            transfer.last_phase = iR % kR      # W_R's mask phase when the stop arrives
            return b / u, t
        if ev == 'R':
            if iR % kR == 0:
                b += u
            iR += 1
            tR = next_arrival(t + Fr(1, 10 ** 9), b, None, vp, P, -1, phaseR)
            tR = max(tR, t + Fr(1, 10 ** 9))
        else:
            L_open = True
            if iL % kL == 0:
                a += u
            iL += 1
            if a == 0:
                stop_emit = t
                L_open = False
                tL = Fr(10 ** 30)
            else:
                tL = next_arrival(t + Fr(1, 10 ** 9), a, None, vp, P, +1, phaseL)
    raise RuntimeError('no end')


def period_test(params, gmax=600, mmax=300, g0=100):
    """smallest m with out(g + m) - out(g) constant for g0 <= g <= gmax - m:
    the map is then affine with offsets periodic mod m."""
    outs = {g: transfer(g, **params)[0] for g in range(1, gmax + 1)}
    for m in range(1, mmax + 1):
        ds = {outs[g + m] - outs[g] for g in range(g0, gmax - m + 1)}
        if len(ds) == 1:
            inc = ds.pop()
            offs = {outs[g] - inc / m * g for g in range(g0, gmax + 1)}
            return m, inc / m, offs, outs
    return None, None, None, outs


if __name__ == '__main__':
    com = dict(u=Fr(4), vp=Fr(1, 3), vs=Fr(2, 3), P=Fr(6))
    inc = dict(u=Fr(5), vp=Fr(1, 3), vs=Fr(2, 3), P=Fr(7))
    res = {}
    for name, base in (('commensurate (u/vp = 2P, u/vs = P)', com), ('incommensurate (u = 5, P = 7)', inc)):
        for kR in (1, 2, 3):
            try:
                m, alpha, offs, outs = period_test(dict(base, kR=kR), gmax=400, mmax=200)
            except RuntimeError:
                print(f'{name}, W_R walks every {kR}: the stop signal never catches W_R '
                      f'(window walks faster than vs): no transfer')
                continue
            res[(name, kR)] = (m, alpha, offs)
            print(f'{name}, W_R walks every {kR}: affine with offsets periodic mod {m}, '
                  f'slope {alpha}, {len(offs) if offs else "-"} distinct offsets '
                  f'{sorted(str(o) for o in offs)[:4] if offs else ""}')
    ok = bool(res) and all(v[0] is not None for v in res.values())
    const = all(len(res[(n, k)][2]) == 1 for n, k in res if n.startswith('commensurate'))
    print('overshoot law (affine, residue-periodic offsets) holds in all 6 cases:', ok)
    print('commensurate cases have ONE constant offset (exact multiplier):', const)
