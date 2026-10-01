"""Batch: random fixed-stream programs + unbalanced controls."""
import sys, random
import fixed_stream as F
seed, n, L = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rnd = random.Random(seed)
ok = 0
for i in range(n):
    prog = [rnd.choice(list(F.BASE)) for _ in range(L)]
    good, got, want, junk = F.check(prog)
    ok += good
    print(" ".join(prog), "->", "OK" if good else "FAIL", got, want, junk, flush=True)
print(f"balanced: {ok}/{n}", flush=True)
for prog in (["UP2", "DN2", "UP2"], ["UP1", "DN2", "DN1"]):
    good, got, want, junk = F.control_unbalanced(prog)
    print("CONTROL unbalanced", " ".join(prog), "->", "passes (BAD control)" if good else "fails (good)", got, want, junk, flush=True)
