"""Differential test (after verify's INZZ counterexample): random words over
an op alphabet, assembled with stream.build2 (classes designated relative to
the reference E^(val+1) of each slot, val forced by slip), run at glider
level (optionally exact CA), compared with the semantic model.
Usage: python diff_test.py SEED N LEN [ALPHABET] [--ca]"""
import random
import sys
import common  # noqa: F401  (sets up collider imports)
from glidersim import ThreeBody
from stream import build2, run, counter_of
from test_prog import OPS

TABLE = {("Z", 1): 2}          # Z at value-1 slots: trailing GB4 meets zero E in its no-displacement class



def main():
  seed, N, L = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
  alph = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else "INZ"
  ca = "fast" if "--ca" in sys.argv else False
  rnd = random.Random(seed)
  bad = 0
  for i in range(N):
      w = "".join(rnd.choice(alph) for _ in range(L))
      exp = 0
      for c in w:
          exp = OPS[c](exp)
      try:
          st, log, ok = run(build2(list(w), TABLE), ca=ca)
          vals, other = counter_of(st)
      except ThreeBody as e:
          vals, other, ok = None, [str(e)[:60]], None
      good = vals == [exp] and not other and ok is not False
      bad += not good
      print(f"{w:14s} model={exp:2d} got={vals} other={other} CA:{ok} {'OK' if good else 'BAD'}", flush=True)
  print(f"{N - bad}/{N} OK")



if __name__ == "__main__":
    main()