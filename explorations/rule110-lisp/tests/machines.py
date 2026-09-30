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
