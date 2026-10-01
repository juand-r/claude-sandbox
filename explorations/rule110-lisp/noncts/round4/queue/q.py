"""Shared helpers for round4/queue: import round2/queue/splice (read-only)."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
NONCTS = HERE.parents[1]
sys.path.insert(0, str(NONCTS / "round2" / "queue"))
from splice import *  # noqa
