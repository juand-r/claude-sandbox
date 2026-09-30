"""Tag systems and their CTS compilation, differentially tested."""

from cts import run as cts_run
from machines import three_state_tm
from tag import decode_cts_tape, run as tag_run, ts_to_cts
from tm import tm_to_ts

# Chapman's 3x+1 tag system (quoted in Cook 2009): deletion number 2,
# tape C D^(x-1).
CHAPMAN = {"A": "C", "B": "D", "C": "AE", "D": "BF", "E": "CCD", "F": "DDD"}
# De Mol's 3x+1 tag system: deletion number 2, tape A^x; the pure-A tapes
# it passes through have lengths following the Collatz trajectory of x.
DEMOL = {"A": "CY", "C": "A", "Y": "AAA"}


def tapes(rules, tape, s, steps):
    return ["".join(map(str, t)) for _, t in tag_run(rules, tape, s, steps)]


def cts_tapes_at_cycles(rules, tape, s, cycles):
    """Run the CTS compilation and decode it at each TS-step boundary."""
    cts_tape, apps, order = ts_to_cts(rules, tape, s)
    cycle = s * len(order)
    assert len(order) % 6 == 0 and len(apps) == cycle
    out = []
    for _, t, _ in cts_run(cts_tape, apps, cycles * cycle, sample=cycle):
        dec = decode_cts_tape(t, order)
        assert dec is not None, "CTS tape not word-aligned at a cycle boundary"
        out.append("".join(map(str, dec)))
    return out


def test_tag_run_rules():
    got = tapes(CHAPMAN, "CDDDDDD", 2, 3)
    assert got[:3] == ["CDDDDDD", "DDDDDAE", "DDDAEBF"]


def test_tag_run_rejects_never_read_symbol():
    import pytest
    with pytest.raises(RuntimeError):
        list(tag_run({"a": None}, "aa", 2, 5))


def test_chapman_cts_emulation():
    ref = tapes(CHAPMAN, "CDDDD", 2, 40)
    got = cts_tapes_at_cycles(CHAPMAN, "CDDDD", 2, 40)
    assert len(got) >= 20 and got[:len(ref)] == ref[:len(got)]


def test_demol_collatz_and_cts():
    ref = tapes(DEMOL, "AAA", 2, 60)
    assert len(ref) == 25 and ref[-1] == "A"          # halts (len < 2)
    assert [len(t) for t in ref if set(t) == {"A"}] == [3, 5, 8, 4, 2, 1]
    got = cts_tapes_at_cycles(DEMOL, "AAA", 2, 28)
    assert got[:25] == ref
    # the CTS has no length-<2 halt: it continues into Collatz 1 -> 2 -> 1
    assert got[25:28] == ["Y", "AA", "CY"]


def test_tm_to_ts_to_cts_composed():
    rules, ts_tape, s = tm_to_ts(three_state_tm(), 1, [1], [1], 1, [1, 2], [1])
    ref = tapes(rules, ts_tape, s, 400)
    cts_tape, apps, order = ts_to_cts(rules, ts_tape, s)
    cycle = s * len(order)
    got = []
    for _, t, _ in cts_run(cts_tape, apps, 300 * cycle, sample=cycle):
        dec = decode_cts_tape(t, order)
        assert dec is not None
        got.append("".join(dec))
    assert len(got) >= 250 and got[:len(ref)] == ref[:len(got)]



def _read_trace(tape, apps, steps, junk_len=0):
    """(appendant index, symbol) of every read, skipping reads of symbols
    that were appended as junk (appendants of length junk_len made only of
    N). A CTS runner written out here so reads can be told apart by origin."""
    from collections import deque
    q = deque((c, False) for c in tape)
    out = []
    for n in range(steps):
        if not q:
            break
        c, junk = q.popleft()
        if not junk:
            out.append((n % len(apps), c))
        if c == "Y":
            a = apps[n % len(apps)]
            is_junk = junk_len > 0 and len(a) == junk_len and "Y" not in a
            q.extend((x, is_junk) for x in a)
    return out


def test_fill_empty_appendants_exact():
    from cts import fill_empty_appendants
    for rules, tape in ((DEMOL, "AAA"), (CHAPMAN, "CDDDD")):
        cts_tape, apps, _ = ts_to_cts(rules, tape, 2)
        filled = fill_empty_appendants(apps)
        assert "" in apps and "" not in filled
        assert all(len(a) % 6 == 0 for a in filled)
        m = len(filled[apps.index("")])
        ref = _read_trace(cts_tape, apps, 5_000)
        got = _read_trace(cts_tape, filled, 20_000, junk_len=m)
        assert len(got) >= len(ref) >= 250
        assert got[:len(ref)] == ref
