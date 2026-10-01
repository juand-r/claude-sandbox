"""Run given words with assembler v2 (stream.build2 + TABLE) and exact CA."""
import sys
import common  # noqa: F401
from stream import build2, run, counter_of
from test_prog import OPS
from diff_test import TABLE  # noqa: E402  (module guarded below)

for w in sys.argv[1:]:
    exp = 0
    for c in w:
        exp = OPS[c](exp)
    st, log, ok = run(build2(list(w), TABLE), ca="fast")
    vals, other = counter_of(st)
    print(f"{w}: model {exp} got {vals} other {other} CA==sim {ok}", flush=True)
