"""Machines shared by several test files."""

from tm import TM


def three_state_tm():
    """3-state, 2-symbol two-way TM: one step left, one step back right,
    then march right over 1's and halt on the first 2. Exercises L and R
    moves, background growth on both sides, repeated identical visits, and
    halting."""
    write = {(1, 1): 1, (2, 1): 1, (3, 1): 1}
    move = {(1, 1): "L", (2, 1): "R", (3, 1): "R", (3, 2): "H",
            (1, 2): "H", (2, 2): "H"}
    nxt = {(1, 1): 2, (2, 1): 3, (3, 1): 3}
    return TM(3, 2, write, move, nxt)


def edge_walker_tm():
    """Starts on an empty tape, writes 2's two cells into fresh blanks on
    the right, walks back left over them and off the left end, then
    halts: grows the tape at both ends from nothing."""
    write = {(1, 1): 2, (2, 1): 2, (3, 1): 2, (4, 2): 2, (4, 1): 2}
    move = {(1, 1): "R", (2, 1): "R", (3, 1): "L", (4, 2): "L",
            (4, 1): "L", (5, 1): "H", (5, 2): "H", (1, 2): "H",
            (2, 2): "H", (3, 2): "H"}
    nxt = {(1, 1): 2, (2, 1): 3, (3, 1): 4, (4, 2): 4, (4, 1): 5}
    return TM(5, 2, write, move, nxt)


def one_move_tm():
    """2 states, 1 symbol: state 1 moves right into state 2, which halts.
    The smallest machine with a state change and a head move; compiled
    through Cocke-Minsky and the filled CTS it halts at CTS read 5,760
    (NOTES.md, phase 7)."""
    return TM(2, 1, {(1, 1): 1}, {(1, 1): "R", (2, 1): "H"}, {(1, 1): 2})
