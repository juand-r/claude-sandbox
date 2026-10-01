"""lm.py - the TRANSFER (loop) machine: the universal target for two-stream
machines with a shared mode, and its compiler from 2-counter Minsky machines.

Why this model (THEORY.md s.5). The no-go theorems say a two-counter
machine needs a persistent mode, changed by zero events of BOTH counters,
that sets the drift while both counters are large. The simplest such
machine is one in which every state is a transfer loop that runs until its
source counter (nearly) empties:

  state q = ("XY", k, j, nxt)  repeat { x -= k; y += j } while x >= k;
                               then rem = x (0..k-1) stays in x and the
                               machine goes to nxt[rem]
  state q = ("YX", k, j, nxt)  the same with the roles of x and y swapped
  state q = ("HALT",)

Physically a transfer state is a pair of drifts (one per stream) plus the
zero event that ends it; the remainder is what the zero event's phase
reveals. There are no single INC/DEC instructions: everything is a loop,
which is exactly what a periodic stream with a mode can do.

Compiler (Goedel numbering): Minsky registers (a, b) -> x = 2^a 3^b, y = 0.
  INC r -> j        : XY(1,1) -> YX(1,p_r) -> state(j)        (p_0=2, p_1=3)
  DEC r -> (jp, jz) : XY(p_r,1) -> rem = x mod p_r
                        rem == 0 : YX(1,1)   -> state(jp)     (x = n / p)
                        rem != 0 : YX(1,p_r) -> state(jz)     (x = rem + p*(n div p) = n)
  HALT              : HALT
Two transfers per Minsky step, three loop types per counter.

Transfers used by the compiled code have the restricted forms
XY(k,1) and YX(1,j) (only division x -> y and multiplication y -> x).
`uses_restricted_forms` checks this; THEORY.md s.6 uses it.

Run: python lm.py   (differential tests vs scholar's Minsky interpreter;
                     controls must fail; exit 1 on failure)
"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "scholar"))
from csm import run_minsky, random_minsky   # noqa: E402  (read-only reuse)

PRIMES = (2, 3)


def run_lm(states, q, x, y, max_transfers):
    """Exact closed-form execution (each loop in O(1) with big ints).
    Returns (q, x, y, transfers, halted)."""
    n = 0
    while n < max_transfers:
        s = states[q]
        if s[0] == "HALT":
            return q, x, y, n, True
        kind, k, j, nxt = s
        if kind == "XY":
            d, rem = divmod(x, k)
            x, y = rem, y + j * d
        else:
            d, rem = divmod(y, k)
            y, x = rem, x + j * d
        q = nxt[rem]
        n += 1
    return q, x, y, n, False


def compile_minsky(prog):
    """prog in scholar's format. Returns (states, start_state).
    State ids: 3 per Minsky instruction (entry + two continuations)."""
    N = len(prog)
    entry = lambda i: 4 * i               # noqa: E731
    states = {}
    for i, ins in enumerate(prog):
        e = entry(i)
        if ins[0] == "HALT":
            states[e] = ("HALT",)
        elif ins[0] == "INC":
            _, r, j = ins
            p = PRIMES[r]
            states[e] = ("XY", 1, 1, {0: e + 1})
            states[e + 1] = ("YX", 1, p, {0: entry(j)})
        else:
            _, r, jp, jz = ins
            p = PRIMES[r]
            nxt = {0: e + 1}
            for rem in range(1, p):
                nxt[rem] = e + 2
            states[e] = ("XY", p, 1, nxt)
            states[e + 1] = ("YX", 1, 1, {0: entry(jp)})       # divisible: DEC done
            states[e + 2] = ("YX", 1, p, {0: entry(jz)})       # not divisible: restore
    return states, entry(0)


def uses_restricted_forms(states):
    for s in states.values():
        if s[0] == "XY" and s[2] != 1:
            return False
        if s[0] == "YX" and s[1] != 1:
            return False
    return True


def decode(x):
    a = b = 0
    while x % 2 == 0 and x > 0:
        x //= 2
        a += 1
    while x % 3 == 0 and x > 0:
        x //= 3
        b += 1
    return [a, b], x


def differential(n_random=500, seed=7, budget=1500, variant="ok"):
    """variant 'ok': the compiler as above. 'norem': control in which the
    zero event does not reveal the remainder (every remainder goes to the
    'divisible' branch), i.e. a zero test without branching information."""
    rng = random.Random(seed)
    tests = [([("DEC", 0, 1, 2), ("INC", 1, 0), ("HALT",)], [3, 4]),
             ([("DEC", 1, 1, 3), ("INC", 0, 2), ("INC", 0, 0), ("HALT",)], [0, 7])]
    for _ in range(n_random):
        tests.append((random_minsky(rng.randrange(2, 9), rng=rng),
                      [rng.randrange(5), rng.randrange(5)]))
    fails = halting = 0
    for prog, regs in tests:
        mreg, msteps, mh = run_minsky(prog, regs, budget)
        states, q0 = compile_minsky(prog)
        if variant == "norem":
            states = {k: (v if v[0] == "HALT" else
                          (v[0], v[1], v[2], {r: v[3][0] for r in range(v[1])}))
                      for k, v in states.items()}
        x0 = 2 ** regs[0] * 3 ** regs[1]
        q, x, y, nt, h = run_lm(states, q0, x0, 0, 2 * budget + 4)
        if mh:
            halting += 1
            regs_out, rest = decode(x)
            ok = h and y == 0 and rest == 1 and regs_out == mreg and nt == 2 * msteps
        else:
            ok = not h
        fails += not ok
    return len(tests), halting, fails


def main():
    total, halting, fails = differential()
    _, _, cfails = differential(variant="norem")
    states, _ = compile_minsky(random_minsky(8, rng=random.Random(1)))
    print(f"LM compile: {total} differential tests ({halting} halting), "
          f"{fails} failures (must be 0)")
    print(f"control 'no remainder information at zero': {cfails} failures (must be > 0)")
    print(f"compiled code uses only XY(k,1) and YX(1,j): {uses_restricted_forms(states)}")
    return 1 if fails or cfails == 0 else 0


if __name__ == "__main__":
    sys.exit(main())
