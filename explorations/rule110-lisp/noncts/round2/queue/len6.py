"""Experiment: what happens after a REJECTED appendant whose length is not
a multiple of 6 (Cook: the next leader then 'hits the tape incorrectly')?
Reference vs observed read outcomes via experiments.read_outcomes."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from experiments import read_outcomes
from cts import run as cts_run
from encoder import _left_v

L = int(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
tape, apps = "NYYNYY", ["N" * L, "YNNNNN"]
v = 2 * _left_v(apps)
ref = "".join(t[0] for _, t, _ in cts_run(tape, apps, n) if t)[:n]
got = read_outcomes(tape, apps, v, n, (n + 2) * 2 * 30 * v)
print(f"L={L} v={v} observed {got} reference {ref}", flush=True)
