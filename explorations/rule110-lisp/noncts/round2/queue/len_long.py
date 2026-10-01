"""Main-project question: must REJECTED appendants have length = 0 mod 6
(Cook; cts.LENGTH_UNIT) or only even length? Program {N^L, YNNNNN}
(appendant 0 = N^L), tape NYYNYY, v = 2 x Cook's, N reads observed with
experiments.read_outcomes (decoder-free, StreamRun) and compared with the
reference CTS. N^L is accepted whenever a Y meets appendant 0, so its
symbols are later READ too (that is where a x6 rule could bite).
    python len_long.py L N"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from experiments import read_outcomes
from cts import run as cts_run
from encoder import _left_v
L, n = int(sys.argv[1]), int(sys.argv[2])
tape, apps = "NYYNYY", ["N" * L, "YNNNNN"]
v = 2 * _left_v(apps)
ref = "".join(t[0] for _, t, _ in cts_run(tape, apps, n) if t)[:n]
got = read_outcomes(tape, apps, v, n, (n + 2) * 2 * 30 * v)
same = sum(a == b for a, b in zip(got, ref))
print(f"L={L} v={v} n={n} observed {got} reference {ref} {'MATCH' if got == ref else 'DIFFER'} ({same}/{n})", flush=True)
