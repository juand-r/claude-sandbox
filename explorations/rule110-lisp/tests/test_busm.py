"""Bus programs compiled to phase machines compute what the reference does."""
import random

import cts
from busm import Bcast, Compiled, Local, run_reference


def _random_program(rng, n, V, n_ops):
    ops = []
    for _ in range(n_ops):
        if rng.random() < 0.3:
            ks = rng.sample(range(n), rng.randint(1, n))
            ops.append(Local({k: _lut1(rng, V) for k in ks}))
        else:
            j = rng.randrange(n)
            others = [k for k in range(n) if k != j]
            ks = rng.sample(others, rng.randint(0, len(others)))
            emit_t = [rng.randrange(2) for _ in range(V)]
            ops.append(Bcast(j, emit_t.__getitem__,
                             {k: _lut2(rng, V) for k in ks}))
    return ops


def _lut1(rng, V):
    t = [rng.randrange(V) for _ in range(V)]
    return t.__getitem__


def _lut2(rng, V):
    t = [[rng.randrange(V) for _ in range(2)] for _ in range(V)]
    return lambda v, b: t[v][b]


def test_compiled_equals_reference():
    rng = random.Random(3)
    for trial in range(60):
        n, V = rng.randint(1, 6), rng.randint(1, 5)
        ops = _random_program(rng, n, V, rng.randint(0, 12))
        comp = Compiled(n, V, ops)
        for _ in range(4):
            vals = [rng.randrange(V) for _ in range(n)]
            assert comp.run(vals) == run_reference(ops, vals, V), trial


def test_compiled_equals_cts():
    """The phase machine is exact against the bit-level CTS (phasem tests
    this in general; here once more on a compiled bus program)."""
    rng = random.Random(5)
    n, V = 4, 3
    ops = _random_program(rng, n, V, 8)
    comp = Compiled(n, V, ops)
    vals = [2, 0, 1, 1]
    tape = comp.pm.encode(comp.initial_tape(vals))
    apps = comp.pm.appendants()
    B = comp.pm.B
    *_, (step, t, _) = cts.run(tape, apps, comp.p * B, sample=comp.p * B)
    got = [c // 2 for c, _ in comp.pm.decode(t, step) if c >= 0]
    assert got == run_reference(ops, vals, V)
