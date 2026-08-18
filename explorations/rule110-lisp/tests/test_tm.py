"""Differential test: TM visit sequence vs its tag-system compilation.

The tag system reads the current TM state and symbol precisely when a
symbol H_{i}_{j} fires (lands at the front and its rule is applied): j <= t
is a genuine (state psi_i, symbol sigma_j) visit, while j = t+1 / t+2 are
internal background-extension events. The sequence of genuine firings must
equal the TM's visit sequence, which pins down the whole computation since
writes and moves are functions of (state, symbol).
"""


import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tm import TM, tm_to_ts, ts_run_list


def fired_visits(rules, tape, s, t, max_ts_steps, stop_after):
    """Genuine (state, symbol) H-firings during a tag-system run."""
    visits = []
    for n, tp in ts_run_list(rules, tape, s, max_ts_steps):
        if len(tp) < s:
            break
        head = tp[0]
        if head.startswith("H_") and head.count("_") == 2:
            i, j = map(int, head.split("_")[1:])
            if j <= t:
                visits.append((i, j))
                if len(visits) >= stop_after:
                    break
    return visits


def test_tm_vs_ts_visits():
    # 3-state 2-symbol machine: one step left, back right, then march right
    # over 1's until a 2 is found, then halt. Exercises L, R and halting.
    write = {(1, 1): 1, (2, 1): 1, (3, 1): 1}
    move = {(1, 1): "L", (2, 1): "R", (3, 1): "R", (3, 2): "H",
            (1, 2): "H", (2, 2): "H"}
    nxt = {(1, 1): 2, (2, 1): 3, (3, 1): 3}
    tm = TM(3, 2, write, move, nxt)

    cfg = dict(state=1, left_bg=[1], left=[1], cur=1,
               right=[1, 1, 1, 1, 2], right_bg=[1])
    ref = list(tm.run(**cfg, max_steps=50))
    assert ref[-1] == (3, 2)      # reaches the halting pair
    assert 5 < len(ref) < 50      # halts after a genuine march
    assert ref.count((3, 1)) >= 3  # contains repeated identical visits

    rules, tape, s = tm_to_ts(tm, cfg["state"], cfg["left_bg"], cfg["left"],
                              cfg["cur"], cfg["right"], cfg["right_bg"])
    visits = fired_visits(rules, tape, s, tm.t, 5_000_000, len(ref) + 1)
    assert visits == ref, (visits[:10], ref[:10])
