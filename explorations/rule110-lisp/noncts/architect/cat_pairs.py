"""Run collider's pairwise collision enumerator (read-only import) on pairs
the architecture needs; print one line per collision class. Errors from
the enumerator are printed loudly per pair (not hidden).
Usage: python cat_pairs.py X Y [X Y ...]"""
import sys
sys.path.insert(0, "../collider")
from library import Library
from collide import collide_pair, describe

lib = Library.load()
args = sys.argv[1:]
for X, Y in zip(args[::2], args[1::2]):
    try:
        rs = collide_pair(lib, X, Y)
    except Exception as e:
        print(f"{X}+{Y}: ENUMERATOR ERROR {type(e).__name__}: {str(e)[:120]}")
        continue
    for r in rs:
        print(describe(r), r["products"], flush=True)
