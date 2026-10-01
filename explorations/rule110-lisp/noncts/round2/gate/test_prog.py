"""Run a program (string of op letters, see stream.ALIAS) on inputs v and
compare with the semantic model (semantic_search.OPS).
Usage: python test_prog.py PROGRAM VMAX [--ca]"""
import sys
from stream import build, run, counter_of

OPS = {
    "I": lambda v: v + 1, "N": lambda v: v,
    "Z": lambda v: v - 1 if v else 6,
    "W": lambda v: v if v else 7,
    "X": lambda v: v + 1 if v else 8,
    "J": lambda v: v + 1 if v else 0,
    "K": lambda v: v + 1 if v else 0, "L": lambda v: v + 1 if v else 0,
    "M": lambda v: v + 1 if v else 0, "P": lambda v: v + 1 if v else 0,
}


def main():
  prog = sys.argv[1]
  vmax = int(sys.argv[2])
  ca = "--ca" in sys.argv
  allok = True
  for v in range(vmax + 1):
      exp = v
      for c in prog:
          exp = OPS[c](exp)
      try:
          st, log, ok = run(build(["I"] * v + list(prog)), ca=ca)
      except Exception as e:  # report loudly, keep going over other inputs
          print(f"v={v}: FAILED {type(e).__name__}: {e}", flush=True)
          allok = False
          continue
      vals, other = counter_of(st)
      good = vals == [exp] and ca is False or (vals == [exp] and ok)
      allok &= bool(good)
      zl = [(e[3][:12], e[4], e[5]) for e in log if e[2] == "E"]
      print(f"v={v} final={vals} garbage={other} expected={exp} CA==sim:{ok} {'OK' if good else 'BAD'}",
            flush=True)
      print("   zero meetings:", zl, flush=True)
  print("ALL OK" if allok else "SOME FAILED")


if __name__ == "__main__":
    main()
