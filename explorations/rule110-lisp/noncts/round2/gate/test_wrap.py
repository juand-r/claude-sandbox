"""M2 candidate: input v (prefix of v INCs), then m copies of Z6.
Expected final value (v - m) mod 7 if m >= v (Z6: DEC, 0 -> 6)."""
import sys
from stream import build, run, counter_of

m = int(sys.argv[1]) if len(sys.argv) > 1 else 3
ca = "--ca" in sys.argv
for v in range(0, 9):
    prog = ["I"] * v + ["Z"] * m
    st, log, ok = run(build(prog), ca=ca)
    vals, other = counter_of(st)
    exp = (v - m) % 7 if m >= v else v - m
    print(f"v={v} m={m} final={vals} other={other} expected={exp} CA==sim:{ok}",
          flush=True)
    zl = [(e[2], e[3], e[4], e[5]) for e in log if e[2] == "E" or e[3] == "E"]
    print("   zero-meetings:", zl)
