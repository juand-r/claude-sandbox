"""xm.py - two independent streams realising the transfer machine (lm.py)
with a CROSS-COUPLED mode: each stream keeps its own copy of the mode, and
the two copies are kept consistent only by signals emitted at zero events.
Event-driven, tick-level timing: signals take time, and optionally the two
streams' packet schedules slide against each other with the counter values
(the "skew" that E^n outer faces produce).

Model (XM):
  * Stream i delivers one packet slot per tick to its counter (x for 1,
    y for 2). Slot s has offset o = s mod B inside a BEAT of B slots.
  * Side i holds a mode copy m_i (an LM state). At beat start (o == 0) a
    pending mode is latched. A packet's op is ops[i][o][m_i]: 'D' (DEC),
    'I' (INC) or nothing.
  * Transfer state XY(k, j): side 1 DECs x at offsets 0..k-1; side 2 INCs y
    j times at offsets >= k + dmax + 1. YX(k, j) symmetric.
  * ZERO EVENT: a 'D' on a zero counter at offset o. Modelling choice: the
    beat's o earlier DECs are undone (the zero answer leaves the counter at
    value o = the remainder; physically: the zero reaction at slot o leaves
    the counter at o, like a wrap to a slot-dependent value). The side goes
    idle until the next beat start and latches nxt[o] there. It emits a
    CROSS SIGNAL carrying nxt[o]; the signal reaches the other side after a
    random delay 1..delay_max ticks and makes it idle (abort the rest of the
    beat) and latch nxt[o] at its next beat start.
  * skew beta: every change of counter i by +d at its outer face moves the
    arrival of all later stream-i packets EARLIER by beta*d ticks (E^n: the
    outer face moves toward the stream). beta = 0 is the idealised lockstep.

Design rule: the receiver's INC slots come after offset k + dmax, so a
signal from a zero at offset <= k-1 always arrives before them; and before
the next beat start. With beta = 0 and delay_max <= dmax the realisation is
exact (tested). Controls: (1) y's zero events do not reach side 1 (a
one-directional coupling); (2) skew beta > 0; (3) signals slower than the
design (delay_max > dmax). Each control must fail.

Run: python xm.py   (exit 1 on failure)
"""
import heapq
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm import compile_minsky, run_lm, decode, PRIMES        # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "scholar"))
from csm import run_minsky, random_minsky                     # noqa: E402


def build_ops(states, dmax):
    """Per side, per offset, a dict mode -> op. Returns (B, ops)."""
    B = 1
    for s in states.values():
        if s[0] != "HALT":
            B = max(B, s[1] + dmax + 1 + s[2] + 1)
    ops = {1: [dict() for _ in range(B)], 2: [dict() for _ in range(B)]}
    for q, s in states.items():
        if s[0] == "HALT":
            continue
        kind, k, j, _ = s
        src, dst = (1, 2) if kind == "XY" else (2, 1)
        for o in range(k):
            ops[src][o][q] = "D"
        for o in range(k + dmax + 1, k + dmax + 1 + j):
            ops[dst][o][q] = "I"
    return B, ops


def run_xm(states, q0, x, y, dmax, delay_max, rng, beta=0.0,
           cut_y_to_1=False, max_ticks=10 ** 7):
    """Returns (x, y, halted, ticks)."""
    B, ops = build_ops(states, dmax)
    val = {1: x, 2: y}
    mode = {1: q0, 2: q0}
    pending = {1: None, 2: None}
    idle = {1: False, 2: False}
    done = {1: 0, 2: 0}               # successful DECs in the current beat
    slot = {1: 0, 2: 0}
    shift = {1: 0.0, 2: 0.0}
    signals = []                      # heap of (time, seq, target, new_mode)
    seq = 0
    t = 0.0
    while t < max_ticks:
        # next event: earliest slot arrival or signal
        ta = {i: slot[i] + shift[i] for i in (1, 2)}
        side = 1 if ta[1] <= ta[2] else 2
        if signals and signals[0][0] < ta[side]:
            t, _, tgt, new = heapq.heappop(signals)
            idle[tgt] = True
            pending[tgt] = new
            continue
        t = ta[side]
        o = slot[side] % B
        slot[side] += 1
        if o == 0:
            if pending[side] is not None:
                mode[side] = pending[side]
                pending[side] = None
            idle[side] = False
            done[side] = 0
            if all(states[mode[i]][0] == "HALT" for i in (1, 2)):
                return val[1], val[2], True, t
        if idle[side]:
            continue
        op = ops[side][o].get(mode[side])
        if op is None:
            continue
        if op == "I":
            val[side] += 1
            shift[side] -= beta
        elif val[side] > 0:
            val[side] -= 1
            done[side] += 1
            shift[side] += beta
        else:                                     # zero event at offset o
            rem = done[side]
            val[side] += rem                      # leave the remainder
            shift[side] -= beta * rem
            new = states[mode[side]][3][rem]
            idle[side] = True
            pending[side] = new
            if not (cut_y_to_1 and side == 2):
                d = rng.randint(1, delay_max)
                heapq.heappush(signals, (t + d, seq, 3 - side, new))
                seq += 1
    return val[1], val[2], False, t


def lm_max_value(states, q0, x, budget):
    """Largest value seen at transfer boundaries (to keep tick runs small)."""
    q, y, top = q0, 0, x
    for _ in range(budget):
        q, x, y, n, h = run_lm(states, q, x, y, 1)
        top = max(top, x, y)
        if h:
            return top, True
    return top, False


def test(n_progs=150, seed=3, dmax=3, delay_max=3, beta=0.0, cut=False,
         vmax=1500, label=""):
    rng = random.Random(seed)              # programs and inputs (same for every row)
    drng = random.Random(seed + 1000)      # signal delays
    used = fails = halting = 0
    tries = 0
    while used < n_progs and tries < 50 * n_progs:
        tries += 1
        prog = random_minsky(rng.randrange(2, 8), rng=rng)
        regs = [rng.randrange(4), rng.randrange(3)]
        states, q0 = compile_minsky(prog)
        x0 = 2 ** regs[0] * 3 ** regs[1]
        top, lm_halts = lm_max_value(states, q0, x0, 400)
        if top > vmax:
            continue                       # keep tick-level runs small
        used += 1
        mreg, msteps, mh = run_minsky(prog, regs, 200)
        x, y, h, ticks = run_xm(states, q0, x0, 0, dmax, delay_max, drng, beta=beta,
                                cut_y_to_1=cut, max_ticks=2 * 10 ** 5)
        if mh:
            halting += 1
            r, rest = decode(x)
            ok = h and y == 0 and rest == 1 and r == mreg
        else:
            ok = not h
        fails += not ok
    print(f"{label:48s} {used} programs ({halting} halting): {fails} failures")
    return used, halting, fails


def main():
    rc = 0
    _, _, f = test(label="XM, lockstep, random delays 1..3 (design 3)")
    rc |= f > 0
    _, _, f = test(label="XM, delays 1..3, design dmax 5 (slack)", dmax=5)
    rc |= f > 0
    _, _, f = test(label="CONTROL one-directional (y zero not sent)", cut=True)
    rc |= f == 0
    _, _, f = test(label="CONTROL signals slower than design (1..8 vs 3)", delay_max=8)
    rc |= f == 0
    _, _, f = test(label="CONTROL skew beta = 0.3 slot/unit", beta=0.3)
    rc |= f == 0
    _, _, f = test(label="CONTROL skew beta = 0.05 slot/unit", beta=0.05)
    rc |= f == 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
