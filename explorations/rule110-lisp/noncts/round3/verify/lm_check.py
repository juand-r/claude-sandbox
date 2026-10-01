"""Independent re-implementation (from THEORY.md s.5.1's text only, not
theory/lm.py) of the transfer machine and its Minsky compiler, with a
differential test against my own 2-counter Minsky interpreter.

Transfer machine: state XY(k, j, nxt): while x >= k: x -= k, y += j;
then r = x (0..k-1) and go to nxt[r].  YX(k, j, nxt) symmetric. HALT.
Compiler (Goedel x = 2^a 3^b, y = 0):
  INC r -> J : XY(1,1,[A]); A = YX(1, p_r, [J])
  DEC r -> (Jp, Jz): XY(p_r, 1, [Z0, Zr, ...]); Z0 = YX(1,1,[Jp]);
                     Zr (r != 0) = YX(1, p_r, [Jz])
Control: zero events without remainder information (nxt[r] = nxt[0])."""
import random

P = (2, 3)


def minsky(prog, a, b, budget):
    """prog: list of ('INC', r, j) / ('DEC', r, jp, jz) / ('HALT',).
    Returns (halted, a, b, steps)."""
    reg = [a, b]
    pc, steps = 0, 0
    while steps < budget:
        ins = prog[pc]
        if ins[0] == "HALT":
            return True, reg[0], reg[1], steps
        if ins[0] == "INC":
            reg[ins[1]] += 1
            pc = ins[2]
        else:
            if reg[ins[1]] > 0:
                reg[ins[1]] -= 1
                pc = ins[2]
            else:
                pc = ins[3]
        steps += 1
    return False, reg[0], reg[1], steps


def compile_tm(prog, no_remainder=False):
    """-> dict state -> ('XY'|'YX', k, j, [next states]) or ('HALT',);
    entry state for Minsky instruction i is ('I', i)."""
    tm = {}
    for i, ins in enumerate(prog):
        if ins[0] == "HALT":
            tm[("I", i)] = ("HALT",)
        elif ins[0] == "INC":
            r, j = ins[1], ins[2]
            tm[("I", i)] = ("XY", 1, 1, [("A", i)])
            tm[("A", i)] = ("YX", 1, P[r], [("I", j)])
        else:
            r, jp, jz = ins[1], ins[2], ins[3]
            p = P[r]
            nxt = [("Z", i, rr) for rr in range(p)]
            if no_remainder:
                nxt = [nxt[0]] * p
            tm[("I", i)] = ("XY", p, 1, nxt)
            tm[("Z", i, 0)] = ("YX", 1, 1, [("I", jp)])
            for rr in range(1, p):
                tm[("Z", i, rr)] = ("YX", 1, p, [("I", jz)])
    return tm


def run_tm(tm, x, budget):
    """Returns (halted, x, y, transfers, minsky_steps_equiv)."""
    y, s, transfers = 0, ("I", 0), 0
    while transfers < budget:
        op = tm[s]
        if op[0] == "HALT":
            return True, x, y, transfers
        kind, k, j, nxt = op
        if kind == "XY":
            q, r = divmod(x, k)
            x, y = r, y + j * q
            s = nxt[r]
        else:
            q, r = divmod(y, k)
            y, x = r, x + j * q
            s = nxt[r]
        transfers += 1
    return False, x, y, transfers


def godel_decode(x):
    a = b = 0
    while x and x % 2 == 0:
        x //= 2; a += 1
    while x and x % 3 == 0:
        x //= 3; b += 1
    return a, b, x


def rand_prog(rng, n):
    prog = []
    for i in range(n):
        u = rng.random()
        if u < 0.4:
            prog.append(("INC", rng.randrange(2), rng.randrange(n + 1)))
        elif u < 0.9:
            prog.append(("DEC", rng.randrange(2), rng.randrange(n + 1), rng.randrange(n + 1)))
        else:
            prog.append(("HALT",))
    prog.append(("HALT",))
    return prog


if __name__ == "__main__":
    rng = random.Random(2026)
    tests = halting = bad = ctl_bad = 0
    for _ in range(600):
        prog = rand_prog(rng, rng.randrange(2, 9))
        for a in range(4):
            for b in range(4):
                h, ma, mb, steps = minsky(prog, a, b, 300)
                tests += 1
                tm = compile_tm(prog)
                th, x, y, tr = run_tm(tm, 2 ** a * 3 ** b, 2 * 300 + 1)
                if h:
                    halting += 1
                    ga, gb, rest = godel_decode(x)
                    ok = th and (ga, gb, rest, y, tr) == (ma, mb, 1, 0, 2 * steps)
                    bad += not ok
                    ctl = compile_tm(prog, no_remainder=True)
                    ch, cx, cy, ctr = run_tm(ctl, 2 ** a * 3 ** b, 2 * 300 + 1)
                    ctl_bad += not (ch and godel_decode(cx)[:2] == (ma, mb))
                else:
                    bad += th          # must not halt within the budget
    print(f"{tests} runs, {halting} halting: mismatches {bad}; "
          f"control (no remainder info) wrong on {ctl_bad} halting runs")
    assert bad == 0 and ctl_bad > 0
    print("OK")
