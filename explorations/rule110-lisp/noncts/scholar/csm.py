"""Cyclic skip machine (CSM): the abstract target for a stream-programmed
counter machine in Rule 110, with a compiler from Minsky machines and a
differential test.

Model (what the glider machine would implement):
  - k counters r[0..k-1], values >= 0.
  - A program is a cyclic list of packets P[0..L-1], supplied periodically.
  - Executing packet i and then "skipping s" means the next s packets are
    deleted (not executed); execution continues at packet (i + 1 + s) mod L.
  - Packet types:
      ("INC", r)                 r += 1, skip 0
      ("DEC", r, s_zero, s_pos)  if r == 0: skip s_zero
                                 else: r -= 1, skip s_pos
      ("NOP",)                   skip 0 (an idle packet; see `latency`)
      ("HALT",)                  stop
  The only data-dependent behaviour is the DEC answer: how many following
  packets to delete. In a glider realisation the answer is produced by the
  register and must reach the stream before the first packet it may delete
  arrives; `latency` NOP packets after every DEC model that delay.

Minsky machines (the source): instructions
  ("INC", r, j), ("DEC", r, j_pos, j_zero), ("HALT",), with explicit targets.

Compiler: one block per Minsky instruction.
  INC r, j   ->  INC r ; [NOP]*0 ; then an unconditional jump to j
  DEC r, jp, jz -> DEC r (s_zero -> jz, s_pos -> jp) ; NOP*latency
  unconditional jump to t = INC r0 ; DEC r0 (s_pos -> t)   (r0 was just
  incremented, so the positive branch is certain and r0 is restored)
Skips are forward distances mod L, so backward jumps wrap around the cycle.
Fall-through (skip 0) is used whenever the target is the next block.

Run:  python csm.py     (differential tests; exits 1 on failure)
"""

import random
import sys


# ---------------------------------------------------------------- Minsky

def run_minsky(prog, regs, max_steps):
    regs = list(regs)
    pc, steps = 0, 0
    while steps < max_steps:
        ins = prog[pc]
        if ins[0] == "HALT":
            return regs, steps, True
        if ins[0] == "INC":
            regs[ins[1]] += 1
            pc = ins[2]
        else:
            _, r, jp, jz = ins
            if regs[r] == 0:
                pc = jz
            else:
                regs[r] -= 1
                pc = jp
        steps += 1
    return regs, steps, False


# ---------------------------------------------------------------- CSM

def run_csm(packets, regs, max_executed):
    """Returns (regs, executed, halted, delivered): delivered = total packets
    that arrived (executed or deleted), i.e. the stream length consumed."""
    regs = list(regs)
    L = len(packets)
    i, executed, delivered = 0, 0, 0
    while executed < max_executed:
        p = packets[i]
        delivered += 1
        executed += 1
        if p[0] == "HALT":
            return regs, executed, True, delivered
        skip = 0
        if p[0] == "INC":
            regs[p[1]] += 1
        elif p[0] == "DEC":
            _, r, s0, s1 = p
            if regs[r] == 0:
                skip = s0
            else:
                regs[r] -= 1
                skip = s1
        elif p[0] != "NOP":
            raise ValueError(f"bad packet {p!r}")
        delivered += skip
        i = (i + 1 + skip) % L
    return regs, executed, False, delivered


def compile_minsky(prog, latency=0, scratch=0):
    """Minsky program -> CSM packet list.

    latency: NOP packets placed after every DEC (answer delay).
    scratch: the register used for unconditional jumps (INC then DEC).
    """
    # 1. lay out blocks with symbolic targets
    blocks = []
    for ins in prog:
        if ins[0] == "HALT":
            blocks.append([("HALT",)])
        elif ins[0] == "INC":
            _, r, j = ins
            blocks.append([("INC", r), ("JUMP", j)])
        else:
            _, r, jp, jz = ins
            blocks.append([("DEC*", r, jp, jz)] + [("NOP",)] * latency)
    # 2. expand JUMP into INC scratch; DEC scratch (+latency) unless it
    #    falls through to the next block
    starts, out = [], []
    # first pass: sizes (JUMP expansion size is known: 2 + latency, or 0)
    for b_idx, b in enumerate(blocks):
        starts.append(sum(len(x) for x in out))
        blk = []
        for p in b:
            if p[0] == "JUMP":
                if p[1] == (b_idx + 1) % len(blocks):
                    continue                       # fall through
                blk += [("INC", scratch), ("DEC*", scratch, p[1], p[1])]
                blk += [("NOP",)] * latency
            else:
                blk.append(p)
        out.append(blk)
    flat, owner = [], []
    for b_idx, blk in enumerate(out):
        for p in blk:
            flat.append(p)
    starts = []
    pos = 0
    for blk in out:
        starts.append(pos)
        pos += len(blk)
    L = len(flat)
    # 3. resolve DEC* targets to forward skip counts. The answer is
    #    "delete the next s packets"; the NOP latency packets right after a
    #    DEC are part of what gets deleted or passed.
    packets = []
    for idx, p in enumerate(flat):
        if p[0] == "DEC*":
            _, r, jp, jz = p
            s_pos = (starts[jp] - idx - 1) % L
            s_zero = (starts[jz] - idx - 1) % L
            # the latency NOPs after a DEC must not be needed as skip room
            # when the target is the fall-through block: skip counts are
            # measured over all packets, so they already include them.
            packets.append(("DEC", r, s_zero, s_pos))
        else:
            packets.append(p)
    return packets


# ---------------------------------------------------------------- tests

def check_latency(packets, latency):
    """Every DEC must have at least `latency` packets that it cannot skip
    before its effect matters: the answer may only delete packets that
    arrive after it is effective. With latency NOPs following each DEC the
    answer is effective from packet idx+1+latency on; so a skip s must be
    either 0 ... impossible to express partially. We therefore require
    that the first `latency` packets after a DEC are NOPs (they are then
    harmless whether deleted or executed)."""
    L = len(packets)
    for idx, p in enumerate(packets):
        if p[0] == "DEC":
            for d in range(1, latency + 1):
                if packets[(idx + d) % L][0] != "NOP":
                    return False
    return True


def random_minsky(n, k=2, rng=random):
    prog = []
    for i in range(n - 1):
        if rng.random() < 0.5:
            prog.append(("INC", rng.randrange(k), rng.randrange(n)))
        else:
            prog.append(("DEC", rng.randrange(k), rng.randrange(n), rng.randrange(n)))
    prog.append(("HALT",))
    return prog


def main():
    fails = 0
    # hand-written: r1 += r0 (move), then r0 = 2*r1 (double back)
    add = [("DEC", 0, 1, 2), ("INC", 1, 0), ("HALT",)]
    double = [("DEC", 1, 1, 3), ("INC", 0, 2), ("INC", 0, 0), ("HALT",)]
    tests = [(add, [3, 4]), (add, [0, 5]), (double, [0, 7]), (double, [0, 0])]
    rng = random.Random(1)
    for _ in range(400):
        tests.append((random_minsky(rng.randrange(2, 9), rng=rng),
                      [rng.randrange(4), rng.randrange(4)]))
    budget = 2000
    for prog, regs in tests:
        for latency in (0, 1, 3):
            # scratch = register 0 of the program itself: INC r0; DEC r0 is
            # a certain positive branch and leaves r0 unchanged, so only
            # the program's two registers are needed.
            mreg, msteps, mh = run_minsky(prog, regs, 10 * budget)
            pk = compile_minsky(prog, latency=latency, scratch=0)
            if mh:
                creg, cex, ch, cdel = run_csm(pk, regs, 10 ** 7)
                ok = ch and creg == mreg
            else:
                # CSM executes >= 1 packet per Minsky step, so `budget`
                # executed packets simulate at most `budget` Minsky steps
                creg, cex, ch, cdel = run_csm(pk, regs, budget)
                ok = not ch
            ok = ok and check_latency(pk, latency)
            if not ok:
                fails += 1
                print("FAIL", prog, regs, latency, mreg, mh, creg, ch)
    print(f"{len(tests) * 3} differential tests, {fails} failures")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
