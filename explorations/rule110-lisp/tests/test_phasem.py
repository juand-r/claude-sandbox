"""Phase machine = its compiled CTS, symbol for symbol and phase for phase."""
import random

import cts
from phasem import BLANK, PhaseMachine


def _random_machine(rng, B, m):
    rules = {}
    for f in range(m):
        for c in range(B):
            n = rng.choice([1, 1, 2, 2, 3])
            rules[(f, c)] = tuple(rng.choice([BLANK] + list(range(B)))
                                  for _ in range(n))
    return PhaseMachine(B, m, rules)


def test_phase_machine_equals_cts():
    rng = random.Random(7)
    for trial in range(30):
        B, m = rng.choice([6, 12]), rng.choice([1, 2, 3, 5])
        pm = _random_machine(rng, B, m)
        tape = [rng.randrange(B) for _ in range(rng.randrange(1, 8))]
        apps = pm.appendants()
        for n_sym in (0, 1, 7, 40, 200):
            q, reads = pm.run(tape, n_sym)
            last = None
            for step, t, _ in cts.run(pm.encode(tape), apps, reads * B,
                                      sample=max(1, reads * B)):
                last = (step, t)
            step, t = last
            if step != reads * B:          # CTS emptied first
                assert not q and t == ""
                continue
            assert pm.decode(t, step) == list(q), (trial, n_sym)
