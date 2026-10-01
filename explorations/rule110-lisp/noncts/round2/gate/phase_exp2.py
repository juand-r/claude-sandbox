"""Phase experiments with the incremental search (fastsearch.greedy),
inputs v = 0..VMAX, BLOCKS blocks:
 (a) J^5 N Z6^6 with every N forced to class 0, 1, 2;
 (b) J^4 X Z6^6 for J variants X = K, L, M, P;
 (c) control: J^5 Z6^6 and the neutral-by-hypothesis J^3 Z6^4."""
import sys
from fastsearch import greedy

B = int(sys.argv[1]) if len(sys.argv) > 1 else 3
VM = int(sys.argv[2]) if len(sys.argv) > 2 else 4
for c in (0, 1, 2):
    prog = "JJJJJNZZZZZZ" * B
    cl, ok, s = greedy(prog, VM, {5 + 12 * b: c for b in range(B)})
    print("(a) N class", c, "OK" if ok else f"FAILED at {s}", ",".join(map(str, cl)), flush=True)
for X in "KLMP":
    cl, ok, s = greedy(("JJJJ" + X + "ZZZZZZ") * B, VM)
    print("(b) X", X, "OK" if ok else f"FAILED at {s}", ",".join(map(str, cl)), flush=True)
for prog in ("JJJJJZZZZZZ" * B, "JJJZZZZ" * B):
    cl, ok, s = greedy(prog, VM)
    print("(c)", prog[:12], "OK" if ok else f"FAILED at {s}", ",".join(map(str, cl)), flush=True)
