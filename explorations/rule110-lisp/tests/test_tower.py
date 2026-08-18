"""Capstone: the full tower composed on one machine, verified at every
junction.

  two-way TM -> clockwise TM -> binary clockwise TM -> NW 2-tag -> CTS

The 3-state test TM (one L move, R moves, halt) runs identically at each
level; the CTS level is verified exactly for a prefix of tag steps.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tm import TM
from cw import two_way_to_cw, binarize, run_cw, decode_cw
from nw import CWTM, build_rules, decode_stage2, initial_tape, tag_run
from tag import ts_to_cts
from cts import run as cts_run


def make_tm():
    write = {(1, 1): 1, (2, 1): 1, (3, 1): 1}
    move = {(1, 1): "L", (2, 1): "R", (3, 1): "R", (3, 2): "H",
            (1, 2): "H", (2, 2): "H"}
    nxt = {(1, 1): 2, (2, 1): 3, (3, 1): 3}
    return TM(3, 2, write, move, nxt)


def test_two_way_to_clockwise():
    tm2 = make_tm()
    ref = list(tm2.run(1, [1], [1], 1, [1, 1, 2], [1], 50))
    delta, word, st0 = two_way_to_cw(tm2, 1, [1], 1, [1, 1, 2])
    visits = []
    for n, w, s in run_cw(delta, word, st0, 5000):
        d = decode_cw(list(w), s)
        if d is not None:
            visits.append((d[0], d[1]))
    assert visits == ref


def test_full_tower():
    tm2 = make_tm()
    delta, word, st0 = two_way_to_cw(tm2, 1, [1], 1, [1, 1, 2])
    bdelta, bword, bst0, wid = binarize(delta, word, st0, 2)
    bstates = sorted({s for s, _ in bdelta}, key=repr)
    btm = CWTM(bdelta)
    ref_cw = []
    for q, tp in btm.run(bst0, list(bword), 3000):
        if not ref_cw or ref_cw[-1] != (q, tp):
            ref_cw.append((q, tp))
    assert 90 < len(ref_cw) < 120         # binary machine runs and halts

    rules = build_rules(btm, bstates)
    tape0 = initial_tape(bst0, list(bword), 16)
    got = []
    for n, t in tag_run(rules, tape0, 3_000_000):
        dec = decode_stage2(t)
        if dec is not None and (not got or got[-1] != dec):
            got.append(dec)
    it = iter(got)
    matched = 0
    for cfg in ref_cw[:40]:
        for s in it:
            if s == cfg:
                matched += 1
                break
    assert matched == 40                  # tag emulates the binary machine

    tag_rules = {k: v for k, v in rules.items() if v is not None}
    tag_rules["-"] = []
    order = sorted(tag_rules, key=repr)
    cts_tape, apps, order = ts_to_cts(tag_rules, tape0, 2, order=order)
    n_ = len(order)
    cycle = 2 * n_
    ref_tag = [list(t) for _, t in tag_run(rules, list(tape0), 40)]
    i = 0
    for step_no, t, _ in cts_run(cts_tape, apps, 40 * cycle, sample=cycle):
        blocks = [t[j:j + n_] for j in range(0, len(t), n_)]
        assert not (len(t) % n_) and all(b.count("Y") == 1 for b in blocks)
        dec = [order[b.index("Y")] for b in blocks]
        assert dec == ref_tag[i]
        i += 1
    assert i >= 40                        # CTS emulates the tag system
