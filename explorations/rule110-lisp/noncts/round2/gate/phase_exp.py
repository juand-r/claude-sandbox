"""Phase experiments (greedy adaptive, v = 0..4, three blocks):
 (a) J^5 N Z^6 with the N (slot 5 of each block) forced to class 0, 1, 2;
 (b) J^4 X Z^6 for J-variants X in K, L, M, P (does X undo J's displacement?)
A run that survives three blocks for all inputs means the block is
phase-neutral in its zero branch."""
from adaptive import search

blocks = 3
for c in (0, 1, 2):
    prog = "JJJJJNZZZZZZ" * blocks
    forced = {5 + 12 * b: c for b in range(blocks)}
    cl, ok = search(prog, 4, forced=forced)
    print("(a) N class", c, "OK" if ok else "FAILED", cl, flush=True)
for X in "KLMP":
    prog = ("JJJJ" + X + "ZZZZZZ") * blocks
    cl, ok = search(prog, 4)
    print("(b) X =", X, "OK" if ok else "FAILED", cl, flush=True)
