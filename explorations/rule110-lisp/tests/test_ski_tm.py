"""The SKI Turing machine vs the specification engine (ski.py)."""

import random
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ski import reduce_once
from ski_tm import build_machine, normalize_tm


def spec_bounded(t, max_red=400, max_len=300):
    for _ in range(max_red):
        r = reduce_once(t)
        if r is None:
            return t
        if len(r) > max_len:
            return None
        t = r
    return None


def test_basic_reductions():
    assert normalize_tm("`IK")[0] == "K"
    assert normalize_tm("``KSI")[0] == "S"
    assert normalize_tm("```SKKI")[0] == "I"
    assert normalize_tm("```SKK`IK")[0] == "K"
    assert normalize_tm("``Kxf")[0] == "x"          # inert free atoms
    assert normalize_tm("```Sfx`IK")[0] == "``fK`xK"


def test_machine_size_reported():
    b = build_machine()
    states = {s for s, _ in b.delta}
    assert len(states) < 400          # sanity: stays a small machine
    assert len(b.delta) < 12000


def test_fuzz_vs_spec():
    random.seed(3)
    def rand_term(depth):
        if depth == 0 or random.random() < 0.35:
            return random.choice("SKI")
        return "`" + rand_term(depth - 1) + rand_term(depth - 1)
    tested = 0
    for _ in range(250):
        t = rand_term(7)
        want = spec_bounded(t)
        if want is None:
            continue
        got, _ = normalize_tm(t, 50_000_000)
        assert got == want, t
        tested += 1
    assert tested > 100
