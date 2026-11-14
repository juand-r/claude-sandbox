"""Check ngram.c against brute force on small random k-gram sets."""

import itertools
import random

from grids import run_ngram
from ngrams import admissible
from search import columns, solve


def random_grams(rng, n, k, vocab):
    return {tuple(rng.choice(vocab) for _ in range(k)) for _ in range(n)}


def all_admissible(length, k, grams, vocab):
    return {s for s in itertools.product(vocab, repeat=length) if admissible(s, k, *grams)}


def test_matches_brute_force():
    rng = random.Random(1)
    vocab = [f"w{i}" for i in range(6)]
    # (n_rows, n_cols, k, number of k-grams per set)
    for n_rows, n_cols, k, n_grams in ((3, 3, 2, 14), (4, 3, 2, 16), (3, 4, 2, 16), (4, 4, 3, 70), (4, 5, 3, 60), (5, 5, 3, 75)):
        row_grams = tuple(random_grams(rng, n_grams, k, vocab) for _ in range(3))
        col_grams = tuple(random_grams(rng, n_grams, k, vocab) for _ in range(3))
        row_set = all_admissible(n_cols, k, row_grams, vocab)
        col_set = all_admissible(n_rows, k, col_grams, vocab)
        ref = set(solve(row_set, col_set, n_rows, n_cols))
        assert ref, "test would be vacuous"
        got, exhaustive = run_ngram(row_grams, col_grams, n_rows, n_cols, k, max_repeats=99)
        assert exhaustive and set(got) == ref
        split, _ = run_ngram(row_grams, col_grams, n_rows, n_cols, k, max_repeats=99, n_procs=3)
        assert set(split) == ref
        budget = n_rows * n_cols - 4
        few_repeats, _ = run_ngram(row_grams, col_grams, n_rows, n_cols, k, max_repeats=budget)
        ref_few = {g for g in ref if n_rows * n_cols - len({w for r in g for w in r}) <= budget}
        assert set(few_repeats) == ref_few
        rand, _ = run_ngram(row_grams, col_grams, n_rows, n_cols, k, max_repeats=99, seed=3,
                            restart_nodes=500, max_nodes=100000)
        assert rand and set(rand) <= ref
        for g in got:
            assert all(admissible(r, k, *row_grams) for r in g)
            assert all(admissible(c, k, *col_grams) for c in columns(g))


if __name__ == "__main__":
    test_matches_brute_force()
    print("ok")
