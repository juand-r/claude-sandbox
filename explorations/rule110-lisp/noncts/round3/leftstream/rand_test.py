"""Random left-stream programs over {I, D, Z} (D only where the model
never decrements zero with it), each run as ONE fixed stream text for all
inputs v in VS, compared with the model in exact Rule 110.
Usage: python rand_test.py NPROG LEN VMAX SEED"""
import random
import sys
from lstream import run_program, model, outcome, T0

if __name__ == "__main__":
    N, L, VMAX, seed = map(int, sys.argv[1:5])
    rnd = random.Random(seed)
    vs = list(range(VMAX + 1))
    t0 = max(T0, 200 + 180 * VMAX)
    tot = bad = 0
    for k in range(N):
        while True:
            prog = "".join(rnd.choice("IIDZZ") for _ in range(L))
            if all(model(prog, v)[0] is not None for v in vs):
                break
        res = []
        for v in vs:
            ok, out = run_program(prog, v, t0=t0)
            got = outcome(out)
            exp = model(prog, v)
            good = ok and got[2] == [] and (got[0], got[1]) == exp
            tot += 1
            bad += not good
            res.append(f"{v}:{got[0]}/{got[1]}{'' if good else '!'}")
        print(prog, " ".join(res), flush=True)
    print(f"total {tot} runs, mismatches {bad}")
