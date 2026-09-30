"""Capstone: the polynomial tower composed on one machine, verified at
every junction.

  two-way TM -> clockwise TM -> binary clockwise TM -> NW 2-tag -> CTS

The 3-state test TM runs identically at each level; the CTS level is
verified exactly for a prefix of tag steps.
"""

from cts import run as cts_run
from cw import CWTM, binarize, decode_cw, run_cw, two_way_to_cw
from machines import three_state_tm
from nw import build_rules, decode_stage2, initial_tape
from tag import decode_cts_tape, run as tag_run, ts_to_cts

CFG = (1, [1], 1, [1, 1, 2])       # state, left, cur, right (blank bg = 1)


def test_two_way_to_clockwise():
    tm2 = three_state_tm()
    q, left, cur, right = CFG
    ref = list(tm2.run(q, [1], left, cur, right, [1], 50))
    delta, word, st0 = two_way_to_cw(tm2, q, left, cur, right)
    visits = []
    for _, w, s in run_cw(delta, word, st0, 5000):
        d = decode_cw(list(w), s)
        if d is not None:
            visits.append((d[0], d[1]))
    assert visits == ref


def test_full_tower():
    delta, word, st0 = two_way_to_cw(three_state_tm(), *CFG)
    bdelta, bword, bst0, _ = binarize(delta, word, st0)
    btm = CWTM(bdelta)
    bstates = sorted({s for s, _ in bdelta}, key=repr)
    ref_cw = []
    for q, tp in btm.run(bst0, bword, 3000):
        if not ref_cw or ref_cw[-1] != (q, tp):
            ref_cw.append((q, tp))
    assert 90 < len(ref_cw) < 120            # the binary machine halts

    rules = build_rules(btm, bstates)
    tape0 = initial_tape(bst0, list(bword), 16)
    got = []
    for _, t in tag_run(rules, tape0, 2, 3_000_000):
        dec = decode_stage2(t)
        if dec is not None and (not got or got[-1] != dec):
            got.append(dec)
    it = iter(got)
    assert all(any(s == cfg for s in it) for cfg in ref_cw[:40])

    order = sorted(rules, key=repr)
    cts_tape, apps, order = ts_to_cts(rules, tape0, 2, order=order)
    cycle = 2 * len(order)
    ref_tag = [list(t) for _, t in tag_run(rules, tape0, 2, 40)]
    i = 0
    for _, t, _ in cts_run(cts_tape, apps, 40 * cycle, sample=cycle):
        assert decode_cts_tape(t, order) == ref_tag[i]
        i += 1
    assert i >= 40


def test_ski_machine_through_clockwise():
    """The Lisp-running SKI machine itself (not just the 3-state test
    machine) survives the two-way -> clockwise conversion: the clockwise
    machine normalizes SKI terms to the same results."""
    from ski_tm import as_two_way_tm, normalize_tm
    for term in ["``KSI", "```Sfx`IK"]:
        tm2, q0, tape, syms = as_two_way_tm(term)
        delta, word, st0 = two_way_to_cw(tm2, q0, [], tape[0], tape[1:])
        last = None
        for _, w, s in run_cw(delta, word, st0, 10**6):
            d = decode_cw(list(w), s)
            if d is not None:
                last = d
        q, cur, right, left = last
        cells = "".join(syms[c - 1] for c in left[::-1] + [cur] + right)
        got = "".join(c for c in cells[cells.rindex("$") + 1:] if c in "`SKIfx")
        assert got == normalize_tm(term)[0]
