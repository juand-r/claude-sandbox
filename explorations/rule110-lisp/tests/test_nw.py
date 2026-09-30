"""Neary-Woods polynomial simulation (nw.py): the 2-deletion tag system
against the clockwise binary TM it compiles, decoded at stage-2 fronts."""

from cw import CWTM
from nw import build_rules, decode_stage2, initial_tape
from tag import run as tag_run


def decoded_configs(rules, tape, tag_steps):
    seen = []
    for _, t in tag_run(rules, tape, 2, tag_steps):
        dec = decode_stage2(t)
        if dec is not None and (not seen or seen[-1] != dec):
            seen.append(dec)
    return seen


def reference_configs(tm, state0, tape0, n):
    ref = []
    for q, tp in tm.run(state0, tape0, n):
        if not ref or ref[-1] != (q, tp):
            ref.append((q, tp))
    return ref


def assert_emulates(tm, states, state0, tape0, counter, tag_steps, n_cfgs):
    """Every reference configuration (consecutive repeats collapsed) must
    appear, in order, among the tag system's decoded configurations."""
    seen = decoded_configs(build_rules(tm, states),
                           initial_tape(state0, tape0, counter), tag_steps)
    ref = reference_configs(tm, state0, tape0, n_cfgs)
    it = iter(seen)
    matched = sum(1 for cfg in ref if any(s == cfg for s in it))
    assert matched == len(ref), (matched, len(ref), seen[:6], ref[:6])


def test_flipflop():
    tm = CWTM({(1, "A"): (("B",), 1), (1, "B"): (("A",), 1)})
    assert_emulates(tm, [1], 1, ["A", "B", "A"], 4, 40_000, 12)


def test_growth_counter_doubling():
    # every step writes two symbols: the tape grows and the counter doubles
    tm = CWTM({(1, "A"): (("B", "A"), 1), (1, "B"): (("A", "B"), 1)})
    assert_emulates(tm, [1], 1, ["A", "B"], 2, 300_000, 8)


def test_two_state_machine():
    tm = CWTM({(1, "A"): (("B",), 2), (1, "B"): (("A",), 2),
               (2, "A"): (("A", "B"), 1), (2, "B"): (("A",), 1)})
    assert_emulates(tm, [1, 2], 1, ["A", "B", "B"], 4, 600_000, 8)


def test_halting_drains():
    tm = CWTM({(1, "A"): (("B",), 1)})   # halts on reading B
    last = None
    for _, t in tag_run(build_rules(tm, [1]), initial_tape(1, ["A", "B"], 2),
                        2, 100_000):
        last = list(t)
    assert len(last) < 2
