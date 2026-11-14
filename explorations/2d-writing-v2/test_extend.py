"""Test extend.c against a brute-force enumeration on small random problems.

Run: ./venv/bin/python test_extend.py
"""

import itertools
import random

from multi import check, cuttings, run_extend, usable_sentences
from search import columns


def brute_force(sentences, n_rows, n_cols, seed_grid, max_repeats):
    vocab = sorted({w for key in sentences for w in key})
    free = [(r, c) for r in range(n_rows) for c in range(n_cols)
            if not (seed_grid and r < len(seed_grid) and c < len(seed_grid[0]))]
    found = set()
    seed_words = {w for row in seed_grid or () for w in row}
    if max_repeats == 0:   # all words distinct: enumerate arrangements only
        fills = itertools.permutations([w for w in vocab if w not in seed_words], len(free))
    else:
        fills = itertools.product(vocab, repeat=len(free))
    for fill in fills:
        cells = [[None] * n_cols for _ in range(n_rows)]
        for r, row in enumerate(seed_grid or ()):
            for c, w in enumerate(row):
                cells[r][c] = w
        for (r, c), w in zip(free, fill):
            cells[r][c] = w
        grid = tuple(tuple(row) for row in cells)
        words = [w for row in grid for w in row]
        if len(words) - len(set(words)) > max_repeats:
            continue
        if all(cuttings(line, sentences) for line in grid + columns(grid)):
            found.add(grid)
    return sorted(found)


def random_sentences(rng, vocab, n, lengths):
    return {tuple(rng.choice(vocab) for _ in range(rng.choice(lengths))): (1, ".") for _ in range(n)}


def main():
    rng = random.Random(1)
    n_cases = n_grids = n_filtered = 0
    # (n_rows, n_cols, vocabulary, max_repeats, number of sentences, lengths)
    cases = [(2, 2, "abcde", 4, 12, [2]), (3, 3, "abcd", 9, 30, [2, 3]),
             (2, 4, "abcde", 8, 60, [2, 3, 4]), (4, 2, "abcde", 8, 60, [2, 3, 4]),
             (3, 4, "abc", 12, 25, [2, 3, 4]), (3, 3, "abcd", 5, 40, [2, 3]),
             (2, 5, "abcd", 10, 60, [2, 3, 5]), (3, 3, "abcde", 2, 60, [2, 3]),
             (2, 4, "abcdefghi", 0, 150, [2, 3, 4]), (3, 3, "abcdefghi", 0, 300, [2, 3])]
    for n_rows, n_cols, vocab, max_repeats, n_sent, lengths in cases:
        vocab = list(vocab)
        for _ in range(4):
            sentences = random_sentences(rng, vocab, n_sent, lengths)
            expected = brute_force(sentences, n_rows, n_cols, None, max_repeats)
            got, exhaustive = run_extend(sentences, n_rows, n_cols, max_repeats=max_repeats)
            assert exhaustive
            assert got == expected, (n_rows, n_cols, len(got), len(expected))
            for g in got:
                check(g, sentences, max_repeats)
            n_cases += 1
            n_grids += len(got)
            # Extension: fix the top-left 2x2 block of a solution, refill the rest.
            if expected and n_rows >= 2 and n_cols >= 2:
                seed = tuple(row[:2] for row in expected[0][:2])
                want = [g for g in expected if tuple(row[:2] for row in g[:2]) == seed]
                got, exhaustive = run_extend(sentences, n_rows, n_cols, seed_grid=seed,
                                             max_repeats=max_repeats)
                assert exhaustive and got == want
                if max_repeats == 0:
                    # Dropping unusable sentences must not change the result.
                    # The filter is for adding columns: the seed has all rows.
                    strip = tuple(row[:2] for row in expected[0])
                    want = [g for g in expected if tuple(row[:2] for row in g) == strip]
                    fewer = usable_sentences(sentences, strip)
                    got, exhaustive = run_extend(fewer, n_rows, n_cols, seed_grid=strip)
                    assert exhaustive and got == want
                    n_filtered += len(sentences) - len(fewer)
                # Random mode must return a subset of the true solutions.
                sample, _ = run_extend(sentences, n_rows, n_cols, seed_grid=seed,
                                       max_repeats=max_repeats, max_solutions=5, seed=3,
                                       restart_nodes=1000)
                assert sample and set(sample) <= set(want)
    assert n_grids > 100, "test too weak: almost no grids"
    assert n_filtered > 100, "test too weak: the sentence filter was hardly used"
    print(f"ok: {n_cases} cases, {n_grids} grids in total")


if __name__ == "__main__":
    main()
