"""Check the C solver against the Python reference solver on small inputs."""

import random

from grids import run_solver
from search import columns, solve


def random_sentences(rng, n_sent, length, vocab):
    return {tuple(rng.choice(vocab) for _ in range(length)) for _ in range(n_sent)}


def distinct_words(rows, r, c, w):
    return all(w not in row for row in rows)


def test_matches_reference():
    rng = random.Random(0)
    vocab = [f"w{i}" for i in range(12)]
    for n_rows, n_cols in ((3, 3), (2, 4), (4, 3)):
        row_set = random_sentences(rng, 300, n_cols, vocab)
        col_set = random_sentences(rng, 300, n_rows, vocab)
        ref_all = set(solve(row_set, col_set, n_rows, n_cols))
        ref_distinct = set(solve(row_set, col_set, n_rows, n_cols, accept_cell=distinct_words))
        got_all, exhaustive = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=99)
        got_distinct, _ = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=0)
        assert exhaustive
        assert len(got_all) == len(set(got_all)) and set(got_all) == ref_all
        assert set(got_distinct) == ref_distinct
        assert ref_all, "test is vacuous if no grids exist"
        for grid in got_all:
            assert set(grid) <= row_set and set(columns(grid)) <= col_set


if __name__ == "__main__":
    test_matches_reference()
    print("ok")
