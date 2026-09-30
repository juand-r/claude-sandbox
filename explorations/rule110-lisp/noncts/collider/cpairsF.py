"""Architect's request: stationary C-pair packets (C1/C2/C3 pairs, gap
<= 30) vs F (F catches up from the right... F moves left at -1/9 and the
stationary pair is to its left), all classes."""
from library import Library
from packets import enumerate_pairs
from catalog import run_pairs, merge_save

lib = Library.load()
pk = []
unstable = []
for a in ["C1", "C2", "C3"]:
    for b in ["C1", "C2", "C3"]:
        names, uns = enumerate_pairs(lib, a, b, 30)
        pk += names
        unstable += [(a, b, u[0][1], u[1]) for u in uns]
pk = list(dict.fromkeys(pk))
print(len(pk), "stable C-pairs;", len(unstable), "unstable placements", flush=True)
rows = run_pairs(lib, [(p, "F") for p in pk])
lib.save()
merge_save(rows)
print("done", len(rows))
