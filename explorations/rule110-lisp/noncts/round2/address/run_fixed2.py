"""Batch 2: random fixed-stream programs restricted to the working range
(both registers >= -2 units from the start at every instruction boundary;
dips.py: deeper values push intermediate gaps below the ~25-cell
multi-body threshold), plus the unbalanced controls."""
import sys, random
import fixed_stream as F
seed, n, L = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rnd = random.Random(seed)
STEP = {"DN1": (-1, 0), "UP1": (1, 0), "DN2": (0, -1), "UP2": (0, 1)}
ok = 0
for i in range(n):
    while True:
        prog, v = [], [0, 0]
        for _ in range(L):
            op = rnd.choice(list(F.BASE)); prog.append(op)
            v = [v[0] + STEP[op][0], v[1] + STEP[op][1]]
            if min(v) < -2:
                break
        else:
            break
    good, got, want, junk = F.check(prog)
    ok += good
    print(" ".join(prog), "->", "OK" if good else "FAIL", got, want, junk, flush=True)
print(f"balanced: {ok}/{n}", flush=True)
for prog in (["UP2", "DN2", "UP2"], ["UP1", "DN2", "DN1"]):
    try:
        good, got, want, junk = F.control_unbalanced(prog)
        print("CONTROL unbalanced", " ".join(prog), "->", "passes (BAD control)" if good else "fails (good)", got, want, junk, flush=True)
    except Exception as e:
        print("CONTROL unbalanced", " ".join(prog), "-> fails (good):", type(e).__name__, str(e)[:120], flush=True)
