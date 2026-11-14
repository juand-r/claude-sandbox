"""Check the C solvers against the Python reference solver on small inputs."""

import random

import grids
from search import columns, solve


def random_sentences(rng, n_sent, length, vocab):
    return {tuple(rng.choice(vocab) for _ in range(length)) for _ in range(n_sent)}


MAX_REPEATS = 3


def n_repeats(grid):
    """Number of cells holding a word that already occurs earlier in the grid."""
    words = [w for row in grid for w in row]
    return len(words) - len(set(words))


def test_matches_reference():
    for algorithm in ("fill", "trie"):
        check_matches_reference(algorithm)


def check_matches_reference(algorithm):
    def run_solver(*args, **kwargs):
        return grids.run_solver(*args, algorithm=algorithm, **kwargs)

    rng = random.Random(0)
    vocab = [f"w{i}" for i in range(12)]
    for n_rows, n_cols in ((3, 3), (2, 4), (4, 3)):
        row_set = random_sentences(rng, 300, n_cols, vocab)
        col_set = random_sentences(rng, 300, n_rows, vocab)
        ref_all = set(solve(row_set, col_set, n_rows, n_cols))
        ref_distinct = {g for g in ref_all if n_repeats(g) <= MAX_REPEATS}
        got_all, exhaustive = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=99)
        assert len(got_all) == len(set(got_all))
        got_distinct, _ = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=MAX_REPEATS)
        assert exhaustive
        assert set(got_all) == ref_all
        assert set(got_distinct) == ref_distinct
        assert ref_distinct and ref_distinct != ref_all, "test would be vacuous"
        # splitting over processes must not change the result
        split, exhaustive = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=99, n_procs=3)
        assert exhaustive and set(split) == ref_all
        # cost budget: count cells holding "expensive" words
        costs = {w: 1 for w in vocab[:6]}
        budget = n_rows * n_cols // 3
        got_cheap, _ = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=99,
                                  costs=costs, max_cost=budget)
        ref_cheap = {g for g in ref_all if sum(costs.get(w, 0) for row in g for w in row) <= budget}
        assert set(got_cheap) == ref_cheap and ref_cheap and ref_cheap != ref_all
        # randomized orders with restarts only ever return valid grids, and
        # with enough nodes they find some
        variants = [{}] if algorithm == "fill" else [
            {"temp": temp, "restart_nodes": 2000} for temp in (-1.0, 1.0)]
        for extra in variants:
            rand, _ = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=99, seed=5,
                                 max_nodes=200000, **extra)
            assert rand and set(rand) <= ref_all
        if algorithm == "trie":
            # no cell equal to its mirror cell (excludes symmetric grids)
            def mirror_free(g):
                return all(g[r][c] != g[c][r] for r in range(n_rows) for c in range(n_cols)
                           if r != c and c < n_rows and r < n_cols)
            ref_free = {g for g in ref_all if mirror_free(g)}
            got_free, exhaustive = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=99,
                                              no_mirror=True)
            assert exhaustive and set(got_free) == ref_free
            assert ref_free and ref_free != ref_all, "test would be vacuous"
            # a word at most `limit` times in a row or a column
            for limit in (1, 2):
                def lines_ok(g):
                    return all(line.count(w) <= limit for line in g + columns(g) for w in line)
                ref_ld = {g for g in ref_all if lines_ok(g)}
                got_ld, exhaustive = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=99,
                                                max_per_line=limit)
                assert exhaustive and set(got_ld) == ref_ld
                assert ref_ld and ref_ld != ref_all, "test would be vacuous"
                got_both, exhaustive = run_solver(row_set, col_set, n_rows, n_cols, max_repeats=99,
                                                  max_per_line=limit, no_mirror=True)
                assert exhaustive and set(got_both) == ref_ld & ref_free
        assert ref_all, "test is vacuous if no grids exist"
        for grid in got_all:
            assert set(grid) <= row_set and set(columns(grid)) <= col_set


if __name__ == "__main__":
    test_matches_reference()
    print("ok")
