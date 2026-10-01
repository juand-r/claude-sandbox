"""Back-face scan: every library left-mover fast enough to catch an E^N rod
(velocity -1/2 or -1/3) hits the BACK of a long rod, in every phase k (all
collision classes). Question: does anything reach the rod's FRONT (right to
left influence through the rod)? Exact Rule 110, batched.

For each (glider, k): scene = E^N + glider (gap >= GAP); reference = E^N
alone (same left part). First time t at which some cell left of the front
line (x < front(t) + MARGIN) differs from the reference, else None.
Usage: python3 scan_back.py N T out.jsonl [names_file|all] [start] [stop]
Resumable: skips (name, k) already in out.jsonl."""
import json
import os
import sys
import numpy as np
import objlib as O

N, T, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
which = sys.argv[4] if len(sys.argv) > 4 else "all"
start = int(sys.argv[5]) if len(sys.argv) > 5 else 0
stop = int(sys.argv[6]) if len(sys.argv) > 6 else 10 ** 9
GAP, MARGIN, BATCH = 4, 3, 64

L = O.lib()
if which == "all":
    names = [n for n, g in L.items() if g["velocity"] in ("-1/2", "-1/3")]
else:
    names = [s.strip() for s in open(which) if s.strip()]
names = names[start:stop]
done = set()
if os.path.exists(OUT):
    for line in open(OUT):
        r = json.loads(line)
        done.add((r["name"], r["k"]))

eb, el, er = O.en_bits(N)
PADL = T + 40
WIDTH = len(eb) + 2 * T + 400


def scene(name, k):
    items = [("raw", eb, el, er, 0, "E")]
    if name is not None:
        items.append(("g", name, k, GAP))
    row, x_lo, objs, c = O.build(items, pad=PADL)
    s_front = objs[0][1]
    # normalize to fixed width: cut or extend on the right with ether(c)
    if len(row) >= WIDTH:
        row = row[:WIDTH]
        # recompute tail ether to be safe only if tail is ether: it is (pad)
    else:
        ext = O.ether(c, x_lo + len(row), x_lo + WIDTH)
        row = np.concatenate([row, ext])
    return row, x_lo, s_front, objs


ref, xr, s_front, _ = scene(None, 0)
jobs = [(n, k) for n in names for k in range(L[n]["p"]) if (n, k) not in done]
print(f"{len(jobs)} jobs", flush=True)
for b0 in range(0, len(jobs), BATCH):
    batch = jobs[b0:b0 + BATCH]
    rows = []
    for n, k in batch:
        r, x_lo, sf, objs = scene(n, k)
        assert x_lo == xr and sf == s_front
        rows.append(r)
    A = np.stack(rows + [ref])
    first = [None] * len(batch)
    for t in range(1, T + 1):
        A = ((A[:, 1:-1] | A[:, 2:]) & (1 - (A[:, :-2] & A[:, 1:-1] & A[:, 2:]))).astype(np.uint8)
        xs0 = xr + t
        fx = s_front + (-4 * t) // 15 + MARGIN
        hi = fx - xs0
        if hi <= 0:
            continue
        diff = (A[:-1, :hi] != A[-1, :hi]).any(axis=1)
        for i in np.nonzero(diff)[0]:
            if first[i] is None:
                first[i] = t
    with open(OUT, "a") as fh:
        for (n, k), f, row in zip(batch, first, A[:-1]):
            rec = {"N": N, "T": T, "name": n, "k": k, "front_hit": f}
            fh.write(json.dumps(rec) + "\n")
    hits = sum(f is not None for f in first)
    print(f"batch {b0}: {len(batch)} done, {hits} front hits", flush=True)
