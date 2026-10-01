"""Guarded-block machine (GBM): the weakest control primitive I know that is
enough for universality with a FIXED number of registers.

Model: registers r[0..k-1] >= 0; the program is a cyclic list of BLOCKS,
each a list of ops ("INC", r) / ("DEC", r). Executing a block runs its ops in
order; a DEC on a register that is 0 ABORTS the rest of the block (the zero
answer deletes everything up to the next block boundary, like Cook's
rejector deleting table data up to the next leader). No jumps, no
programmable skip lengths, one fixed skip rule.

Compiler: any Minsky machine (states 1..N, 2 counters) -> GBM with 5
registers: x, y (data), P (state countdown), F, G (0/1 flags). One Minsky
step per program cycle. For state j (blocks in order j = 1..N):
  B1 [DEC P][INC F]              F := 1 if P >= 1 (P -= 1)
  B2 [DEC P][INC P][DEC F]       F := 0 again unless P was exactly 1
  INC r -> q':   B3 [DEC F][INC r][INC P]*(q' + N - j)
  DEC r -> (qp, qz):
                 B3 [DEC F][INC G]
                 B4 [DEC G][INC G][DEC r][DEC G][INC P]*(qp + N - j)
                 B5 [DEC G][INC P]*(qz + N - j)
  HALT:          B3 [DEC F]      (P stays 0: nothing fires any more)
Invariant: entering block 1 of a cycle, P = current state; each state's
B1/B2 pair lowers P by one while P >= 2, so state j fires when P = 1.
Run: python gbm.py  (differential test vs a direct Minsky interpreter)."""
import random, sys
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "..", "..", "scholar"))
from csm import run_minsky, random_minsky   # scholar's interpreter (read-only)

X, Y, P, F, G = range(5)

def run_gbm(blocks, regs, max_cycles):
    regs = list(regs)
    for c in range(max_cycles):
        for blk in blocks:
            for op, r in blk:
                if op == "INC":
                    regs[r] += 1
                elif regs[r] == 0:
                    break            # zero answer: abort the rest of the block
                else:
                    regs[r] -= 1
    return regs

def compile_minsky(prog):
    """prog: scholar's format, states 0..N-1: ("INC", r, j) / ("DEC", r, jp, jz)
    / ("HALT",). GBM states are 1..N (state s -> s+1)."""
    N = len(prog)
    blocks = []
    for j0, ins in enumerate(prog):
        j = j0 + 1
        blocks.append([("DEC", P), ("INC", F)])
        blocks.append([("DEC", P), ("INC", P), ("DEC", F)])
        if ins[0] == "HALT":
            blocks.append([("DEC", F)])
        elif ins[0] == "INC":
            _, r, nxt = ins
            blocks.append([("DEC", F), ("INC", r)] + [("INC", P)] * (nxt + 1 + N - j))
        else:
            _, r, jp, jz = ins
            blocks.append([("DEC", F), ("INC", G)])
            blocks.append([("DEC", G), ("INC", G), ("DEC", r), ("DEC", G)]
                          + [("INC", P)] * (jp + 1 + N - j))
            blocks.append([("DEC", G)] + [("INC", P)] * (jz + 1 + N - j))
    return blocks

def halted(prog, regs):
    return regs[P] == 0 and regs[F] == 0 and regs[G] == 0

def main():
    rng = random.Random(7)
    fails = total = 0
    tests = [([("DEC", 0, 1, 2), ("INC", 1, 0), ("HALT",)], [3, 4]),
             ([("DEC", 1, 1, 3), ("INC", 0, 2), ("INC", 0, 0), ("HALT",)], [0, 7])]
    for _ in range(400):
        tests.append((random_minsky(rng.randrange(2, 9), rng=rng),
                      [rng.randrange(5), rng.randrange(5)]))
    for prog, regs in tests:
        total += 1
        mreg, msteps, mh = run_minsky(prog, regs, 3000)
        blocks = compile_minsky(prog)
        g = run_gbm(blocks, [regs[0], regs[1], 1, 0, 0], msteps + 3 if mh else 3000)
        if mh:
            ok = g[:2] == mreg and halted(prog, g)
        else:
            ok = not halted(prog, g)       # still running after the same budget
        if not ok:
            fails += 1
            print("FAIL", prog, regs, mreg, mh, g)
    # control: the same compile but with zero DEC NOT aborting (chain-like)
    def run_noabort(blocks, regs, n):
        regs = list(regs)
        for _ in range(n):
            for blk in blocks:
                for op, r in blk:
                    if op == "INC": regs[r] += 1
                    elif regs[r] > 0: regs[r] -= 1
        return regs
    cfail = 0
    for prog, regs in tests[:100]:
        mreg, msteps, mh = run_minsky(prog, regs, 3000)
        if not mh:
            continue
        g = run_noabort(compile_minsky(prog), [regs[0], regs[1], 1, 0, 0], msteps + 3)
        cfail += g[:2] != mreg
    print(f"GBM compile: {total} differential tests, {fails} failures; "
          f"control without abort: {cfail} halting programs give wrong registers")
    return 1 if fails or cfail == 0 else 0

if __name__ == "__main__":
    sys.exit(main())
