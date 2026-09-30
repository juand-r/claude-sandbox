"""Cocke-Minsky TM -> tag system (tm.py), tested by visit sequences.

The tag system reads the TM's current state and symbol exactly when a
symbol H_{i}_{j} reaches the front and fires: j <= t is a genuine
(state i, symbol j) visit, while j = t+1 / t+2 are internal
background-extension events. The sequence of genuine firings must equal
the TM's visit sequence, which pins down the computation since writes and
moves are functions of (state, symbol).
"""

from machines import three_state_tm
from tag import run as tag_run
from tm import tm_to_ts


def fired_visits(rules, tape, s, t, max_ts_steps, stop_after):
    visits = []
    for _, tp in tag_run(rules, tape, s, max_ts_steps):
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
    tm = three_state_tm()
    cfg = dict(state=1, left_bg=[1], left=[1], cur=1,
               right=[1, 1, 1, 1, 2], right_bg=[1])
    ref = list(tm.run(**cfg, max_steps=50))
    assert ref[-1] == (3, 2)        # reaches the halting pair
    assert 5 < len(ref) < 50        # after a genuine march
    assert ref.count((3, 1)) >= 3   # with repeated identical visits

    rules, tape, s = tm_to_ts(tm, cfg["state"], cfg["left_bg"], cfg["left"],
                              cfg["cur"], cfg["right"], cfg["right_bg"])
    visits = fired_visits(rules, tape, s, tm.t, 5_000_000, len(ref) + 1)
    assert visits == ref
