"""Control for the chain-machine conjecture: add ONE non-monotone op
TZ(x, y): if x > 0: x -= 1 else: y += 1  (a zero answer that causes an
increment). Random search for non-eventually-periodic zero patterns."""
import sys, time
import numpy as np
from numba import njit
from chain_search import eventual_period

@njit(cache=True)
def run(ops, regs0, cycles, pat):
    regs = regs0.copy()
    L = ops.shape[0]
    for c in range(cycles):
        code = 0
        for j in range(L):
            k = ops[j, 0]
            if k == 0:
                regs[ops[j, 1]] += 1
            elif k == 1:
                m = ops[j, 4]; fired = m
                for i in range(m):
                    r = ops[j, 1 + i]
                    if regs[r] > 0:
                        regs[r] -= 1; fired = i; break
                code = code * 4 + fired
            else:  # TZ
                if regs[ops[j, 1]] > 0:
                    regs[ops[j, 1]] -= 1; code = code * 4
                else:
                    regs[ops[j, 2]] += 1; code = code * 4 + 1
        pat[c] = code
    return regs

def main(N, k, Lmax, cycles, seed, ptz):
    rng = np.random.default_rng(seed)
    pat = np.zeros(cycles, dtype=np.int64)
    found = 0
    for it in range(N):
        L = rng.integers(3, Lmax + 1)
        ops = np.zeros((L, 5), dtype=np.int64)
        for j in range(L):
            u = rng.random()
            if u < 0.35:
                ops[j, 0] = 0; ops[j, 1] = rng.integers(k)
            elif u < 0.35 + ptz:
                ops[j, 0] = 2; a, b = rng.permutation(k)[:2]; ops[j, 1] = a; ops[j, 2] = b
            else:
                m = rng.integers(1, min(3, k) + 1); ch = rng.permutation(k)[:m]
                ops[j, 0] = 1; ops[j, 4] = m; ops[j, 1:1 + m] = ch
        regs = rng.integers(0, 6, k).astype(np.int64)
        run(ops, regs, cycles, pat)
        if eventual_period(pat, 3) < 0:
            found += 1
            if found <= 3:
                print("NONPERIODIC", ops.tolist(), regs.tolist(), flush=True)
    print(f"TZ control N={N} k={k}: {found} not eventually periodic", flush=True)

if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]))
