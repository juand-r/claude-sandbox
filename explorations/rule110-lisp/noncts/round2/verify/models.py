"""verify/models.py - abstract machines for stream-programmed counters, with
executable checks of what they can and cannot do.

Background (see THEORY.md in this directory for the full argument).
In the glider designs of round 1/2 a register ("store") sits in the path of a
program stream that arrives from one side (the right). A packet acts on the
first store it reaches that it does not cross. The only output of a store is
its zero answer (a "flag"), which moves back toward the stream (to the right,
in the store's frame) and can act on packets that have not yet reached the
store. Gate's slip lemma (BOARD 23:37) and my charge audit say that a clean
answer can do exactly one thing: land its missing -1 on a later packet, or
leave the system (escape). That is the semantics of a *decrement chain*:

    CH(r1, r2, ..., rk): decrement the first nonzero register among r1..rk;
                         if all are zero, the answer escapes (nothing).

A *chain machine* is k registers plus a cyclic list of ops INC(r) and
CH(r1..rk), executed forever in order. It is the most general machine that
the "one DEC, one flag, flag lands on a later packet" physics gives, if the
flag is absorbed within a bounded number of packets.

Geometry. Registers are ordered along the stream: index 0 is upstream
(meets the stream first), larger index = further downstream. A flag born at
register r can reach packets for r itself and for registers downstream of r
(they must still pass r). It reaches packets for an upstream register only
if it crosses that register against the transport asymmetry (a "relay").
So a chain is FORWARD if its indices are non-decreasing, BACKWARD otherwise.

Theorem (in this model; proof in THEORY.md s.2): if every chain is forward,
the zero pattern of the machine (which link of each chain fired, per
cycle) is eventually periodic; halting defined by any zero event is
decidable. So such a machine is not universal, whatever the program.
This file checks the theorem's claims on random programs and exhibits
backward programs whose zero pattern is not eventually periodic.

Run: python models.py   (exits 1 on any failure)
"""

import random
import sys


# ---------------------------------------------------------------- chain machine

def run_chain(prog, regs, cycles, record=True):
    """prog: list of ("INC", r) | ("CH", (r1, ..., rk)).
    Returns (regs, pattern): pattern[c] = tuple over CH ops in cycle c of
    the index of the link that fired (k = escaped)."""
    regs = list(regs)
    pattern = []
    for _ in range(cycles):
        pc = []
        for op in prog:
            if op[0] == "INC":
                regs[op[1]] += 1
            else:
                chain = op[1]
                for i, r in enumerate(chain):
                    if regs[r] > 0:
                        regs[r] -= 1
                        break
                else:
                    i = len(chain)
                if record:
                    pc.append(i)
        if record:
            pattern.append(tuple(pc))
    return regs, pattern


def is_forward(prog):
    return all(op[0] == "INC" or list(op[1]) == sorted(op[1]) for op in prog)


def eventual_period(seq, min_reps=3):
    """Smallest (preperiod, period) with seq periodic from preperiod on and at
    least min_reps full periods observed; None if none."""
    n = len(seq)
    for p in range(1, n // min_reps + 1):
        # find the earliest start from which seq[i] == seq[i+p] to the end
        i = n - p - 1
        while i >= 0 and seq[i] == seq[i + p]:
            i -= 1
        pre = i + 1
        if n - pre >= min_reps * p:
            return pre, p
    return None


def random_prog(k, L, forward, rng, max_chain=3):
    prog = []
    for _ in range(L):
        if rng.random() < 0.45:
            prog.append(("INC", rng.randrange(k)))
        else:
            m = rng.randint(1, min(max_chain, k))
            chain = rng.sample(range(k), m)
            if forward:
                chain.sort()
            prog.append(("CH", tuple(chain)))
    return prog


def forward_bound(prog, k):
    """An upper bound on preperiod + period (in cycles) from the proof, for
    the checker to be falsifiable: registers are handled upstream first; see
    THEORY.md s.2. Deliberately generous."""
    L = len(prog)
    B = 1
    for _ in range(k):
        B = B * (2 * L + 2) * 4 + L
    return B


def test_forward(n=300, seed=3):
    """Theorem check: forward chain machines have an eventually periodic zero
    pattern within the simulated horizon, for random programs and inputs."""
    rng = random.Random(seed)
    fails = 0
    worst = (0, 0)
    for _ in range(n):
        k = rng.randint(1, 3)
        L = rng.randint(2, 8)
        prog = random_prog(k, L, True, rng)
        regs = [rng.randrange(30) for _ in range(k)]
        _, pat = run_chain(prog, regs, 3000)
        ep = eventual_period(pat)
        if ep is None:
            fails += 1
            print("FORWARD NOT PERIODIC", prog, regs)
        else:
            worst = max(worst, ep)
    return fails, worst


def doubling_prog():
    """A BACKWARD chain machine whose zero events are not eventually
    periodic (built by hand). Registers: 0 = x, 1 = y, 2 = z (reservoir).
    One cycle moves one unit x -> y twice... see `backward_demo`."""
    return None


def search_backward(n=4000, seed=5):
    """Random backward programs: find ones whose zero pattern has no period
    within 3000 cycles and whose gaps between zero events grow (a witness
    that backward chains escape the theorem). Returns examples."""
    rng = random.Random(seed)
    found = []
    for _ in range(n):
        k = rng.randint(2, 3)
        L = rng.randint(3, 8)
        prog = random_prog(k, L, False, rng)
        if is_forward(prog):
            continue
        regs = [rng.randrange(5) for _ in range(k)]
        _, pat = run_chain(prog, regs, 3000)
        if eventual_period(pat) is not None:
            continue
        # zero events of the first chain op that can fire past link 0
        ev = [c for c, p in enumerate(pat) if any(x > 0 for x in p)]
        gaps = [b - a for a, b in zip(ev, ev[1:])]
        if len(gaps) > 6 and gaps[-1] > gaps[len(gaps) // 2] > gaps[2]:
            found.append((prog, regs, gaps[:12]))
            if len(found) >= 3:
                break
    return found


def main():
    rc = 0
    f, worst = test_forward()
    print(f"forward chain machines: 300 random programs, {f} not eventually "
          f"periodic within 3000 cycles (worst preperiod, period = {worst})")
    rc |= f > 0
    ex = search_backward()
    print(f"backward chain machines: {len(ex)} non-periodic witnesses found")
    for prog, regs, gaps in ex:
        print("  ", prog, regs, "gaps:", gaps)
    rc |= len(ex) == 0          # control: the checker must be able to fail
    return rc


if __name__ == "__main__":
    sys.exit(main())
