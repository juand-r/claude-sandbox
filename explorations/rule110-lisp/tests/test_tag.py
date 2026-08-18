"""Differential tests: TS reference vs its CTS compilation."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cts import run as cts_run
from tag import ts_run, ts_to_cts

# Chapman's 3x+1 tag system (Cook 2009): deletion number 2,
# tape C [D]^(x-1); tracks the Collatz map on string lengths.
CHAPMAN = {"A": "C", "B": "D", "C": "AE", "D": "BF", "E": "CCD", "F": "DDD"}


def decode_cts_tape(cts_tape, order):
    """Inverse of the unary encoding; None if not currently decodable."""
    n = len(order)
    if len(cts_tape) % n:
        return None
    out = []
    for i in range(0, len(cts_tape), n):
        blk = cts_tape[i:i + n]
        if blk.count("Y") != 1:
            return None
        out.append(order[blk.index("Y")])
    return "".join(out)


def test_chapman_reference():
    # x=7: Collatz trajectory of 7 passes through 22, 11, 34, ...
    tape = "C" + "D" * 6
    states = [t for _, t in ts_run(CHAPMAN, tape, 2, 200)]
    # after enough steps the tape should consist of C/D only periodically;
    # check the known first few tapes by direct simulation of the rules
    assert states[0] == "CDDDDDD"
    assert states[1] == "DDDDDAE"   # removed CD, appended rule C -> AE
    assert states[2] == "DDDAEBF"


def test_ts_to_cts_emulation():
    tape = "C" + "D" * 4   # x = 5
    s = 2
    cts_tape, apps, order = ts_to_cts(CHAPMAN, tape, s)
    n = len(order)
    assert n % 6 == 0 and len(apps) == s * n

    ref = [t for _, t in ts_run(CHAPMAN, tape, s, 40)]
    # run the CTS; sample its tape at each cycle boundary (s*n CTS steps)
    cycle = s * n
    got = []
    for step_no, t, _ in cts_run(cts_tape, apps, 40 * cycle):
        if step_no % cycle == 0:
            dec = decode_cts_tape(t, order)
            assert dec is not None, f"undecodable at cycle {step_no // cycle}"
            got.append(dec)
    # drop trailing dummy-symbol content: dummies never appear on tapes
    assert got[:len(ref)] == ref[:len(got)]
    assert len(got) >= 20


def test_tm_to_ts_to_cts_composed():
    """Full lower tower: TM -> TS -> CTS, decoded at cycle boundaries."""
    from tm import TM, tm_to_ts
    write = {(1, 1): 1, (2, 1): 1, (3, 1): 1}
    move = {(1, 1): "L", (2, 1): "R", (3, 1): "R", (3, 2): "H",
            (1, 2): "H", (2, 2): "H"}
    nxt = {(1, 1): 2, (2, 1): 3, (3, 1): 3}
    tm = TM(3, 2, write, move, nxt)
    rules, ts_tape, s = tm_to_ts(tm, 1, [1], [1], 1, [1, 2], [1])

    from tm import ts_run_list
    ref = ["".join(tp) for _, tp in ts_run_list(rules, ts_tape, s, 400)]
    cts_tape, apps, order = ts_to_cts(rules, ts_tape, s)
    n = len(order)
    cycle = s * n
    got = []
    for step_no, t, _ in cts_run(cts_tape, apps, 300 * cycle, sample=cycle):
        dec = decode_cts_tape(t, order)
        assert dec is not None, f"undecodable at cycle {step_no // cycle}"
        got.append(dec)
    assert len(got) >= 250
    assert got[:len(ref)] == ref[:len(got)]


def test_demol_3x1_cts():
    """De Mol's 3x+1 tag system emulated exactly by its CTS compilation,
    tracing Collatz 3 -> 5 -> 8 -> 4 -> 2 -> 1, then the CTS continues
    into the 1 -> 2 -> 1 Collatz cycle (no CTS-level halt)."""
    DEMOL = {"A": "CY", "C": "A", "Y": "AAA"}
    from tm import ts_run_list
    ref = ["".join(tp) for _, tp in ts_run_list(DEMOL, "AAA", 2, 60)]
    assert len(ref) == 25 and ref[-1] == "A"
    pure = [len(s) for s in ref if set(s) == {"A"}]
    assert pure == [3, 5, 8, 4, 2, 1]

    cts_tape, apps, order = ts_to_cts(DEMOL, "AAA", 2)
    n = len(order)
    cycle = 2 * n
    got = []
    for _, t2, _ in cts_run(cts_tape, apps, (len(ref) + 3) * cycle, sample=cycle):
        got.append(decode_cts_tape(t2, order))
    assert got[:25] == ref
    assert got[25:28] == ["Y", "AA", "CY"]   # Collatz 1 -> 2 -> 1 cycle
