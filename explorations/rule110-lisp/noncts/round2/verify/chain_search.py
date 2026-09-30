"""Random search for chain machines (backward chains allowed) whose zero
pattern is NOT eventually periodic. Fast numba version of models.run_chain.
Encoding: op = (kind, r1, r2, r3, len): kind 0 = INC r1, kind 1 = CH(r1..).
A pattern is declared eventually periodic if the full state (register
values, capped relative info not used) ... we use the pattern sequence."""
import sys, time
import numpy as np
from numba import njit

@njit(cache=True)
def run(ops, regs0, cycles, pat):
    regs = regs0.copy()
    L = ops.shape[0]
    for c in range(cycles):
        code = 0
        for j in range(L):
            if ops[j, 0] == 0:
                regs[ops[j, 1]] += 1
            else:
                m = ops[j, 4]
                fired = m
                for i in range(m):
                    r = ops[j, 1 + i]
                    if regs[r] > 0:
                        regs[r] -= 1
                        fired = i
                        break
                code = code * 4 + fired
        pat[c] = code
    return regs

@njit(cache=True)
def eventual_period(seq, min_reps):
    n = seq.shape[0]
    for p in range(1, n // min_reps + 1):
        i = n - p - 1
        while i >= 0 and seq[i] == seq[i + p]:
            i -= 1
        pre = i + 1
        if n - pre >= min_reps * p:
            return p
    return -1

def main(N, k, Lmax, cycles, seed):
    rng = np.random.default_rng(seed)
    pat = np.zeros(cycles, dtype=np.int64)
    nonper = 0
    t = time.time()
    for it in range(N):
        L = rng.integers(3, Lmax + 1)
        ops = np.zeros((L, 5), dtype=np.int64)
        for j in range(L):
            if rng.random() < 0.45:
                ops[j, 0] = 0; ops[j, 1] = rng.integers(k)
            else:
                m = rng.integers(1, min(3, k) + 1)
                ch = rng.permutation(k)[:m]
                ops[j, 0] = 1; ops[j, 4] = m; ops[j, 1:1 + m] = ch
        # only CH ops within 4-ary code budget: at most 15 CH ops fine for int64
        regs = rng.integers(0, 6, k).astype(np.int64)
        run(ops, regs, cycles, pat)
        if eventual_period(pat, 3) < 0:
            nonper += 1
            print("NONPERIODIC", ops.tolist(), regs.tolist(), flush=True)
    print(f"N={N} k={k} Lmax={Lmax} cycles={cycles}: {nonper} not eventually periodic "
          f"({time.time()-t:.0f}s)", flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
