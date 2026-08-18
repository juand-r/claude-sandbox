"""Neary-Woods polynomial simulation: 2-deletion tag system vs clockwise
binary TM, differentially. Decodes the tag tape at stage-2 head fronts and
compares the (state, tape) sequence with the reference machine."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nw import CWTM, build_rules, decode_stage2, initial_tape, tag_run


def run_and_decode(tm, states, state0, tape0, counter, tag_steps, want_cfgs):
    rules = build_rules(tm, states)
    tape = initial_tape(state0, tape0, counter)
    seen = []
    for n, t in tag_run(rules, tape, tag_steps):
        dec = decode_stage2(t)
        if dec is not None and (not seen or seen[-1] != dec):
            seen.append(dec)
    ref = []
    for q, tp in tm.run(state0, tape0, want_cfgs):
        if not ref or ref[-1] != (q, tp):
            ref.append((q, tp))
    it = iter(seen)
    matched = 0
    for cfg in ref:
        for s in it:
            if s == cfg:
                matched += 1
                break
    assert matched == len(ref), (matched, len(ref), seen[:6], ref[:6])
    return seen


def test_flipflop():
    tm = CWTM({(1, "A"): (("B",), 1), (1, "B"): (("A",), 1)})
    run_and_decode(tm, [1], 1, ["A", "B", "A"], 4, 40_000, 12)


def test_growth_counter_doubling():
    tm = CWTM({(1, "A"): (("B", "A"), 1), (1, "B"): (("A", "B"), 1)})
    run_and_decode(tm, [1], 1, ["A", "B"], 2, 300_000, 8)


def test_two_state_machine():
    # richer trajectory: alternates states and rewrites without fixpoints
    tm = CWTM({(1, "A"): (("B",), 2), (1, "B"): (("A",), 2),
               (2, "A"): (("A", "B"), 1), (2, "B"): (("A",), 1)})
    run_and_decode(tm, [1, 2], 1, ["A", "B", "B"], 4, 600_000, 8)


def test_halting_drains():
    tm = CWTM({(1, "A"): (("B",), 1)})   # halts on B
    rules = build_rules(tm, [1])
    tape = initial_tape(1, ["A", "B"], 2)
    last = None
    for n, t in tag_run(rules, tape, 100_000):
        last = list(t)
    assert len(last) < 4
