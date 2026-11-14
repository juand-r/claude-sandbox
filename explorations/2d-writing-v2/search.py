"""Exact search for word grids whose rows and columns are all in given sets.

A grid has `n_rows` rows and `n_cols` columns. Every row must be a member of
`row_set` (tuples of length n_cols) and every column a member of `col_set`
(tuples of length n_rows). The search fills cells in row-major order. At each
cell the candidates are the words that extend both the current row prefix and
the current column prefix to a prefix of some member.
"""

import random


def prefix_table(keys):
    """Map every proper prefix of every key to the set of words that follow it."""
    table = {}
    for key in keys:
        for i in range(len(key)):
            table.setdefault(key[:i], set()).add(key[i])
    return table


def solve(row_set, col_set, n_rows, n_cols, rng=None, accept_cell=None,
          max_nodes=None):
    """Yield grids (tuple of row tuples) by depth-first search.

    rng: if given, candidates at each cell are tried in random order, so the
        first grids found are a varied sample instead of one corner of the space.
    accept_cell(grid_so_far, r, c, word) -> bool: optional pruning hook, called
        with the rows filled so far (the last row may be partial).
    max_nodes: stop after this many search nodes (None = exhaustive).
    """
    row_next = prefix_table(row_set)
    col_next = prefix_table(col_set)
    rows = [[] for _ in range(n_rows)]
    cols = [[] for _ in range(n_cols)]
    nodes = 0

    def fill(r, c):
        nonlocal nodes
        if r == n_rows:
            yield tuple(tuple(row) for row in rows)
            return
        nodes += 1
        if max_nodes is not None and nodes > max_nodes:
            return
        row_cands = row_next.get(tuple(rows[r]))
        col_cands = col_next.get(tuple(cols[c]))
        if not row_cands or not col_cands:
            return
        cands = row_cands & col_cands
        if rng is not None:
            cands = list(cands)
            rng.shuffle(cands)
        nr, nc = (r, c + 1) if c + 1 < n_cols else (r + 1, 0)
        for w in cands:
            if accept_cell is not None and not accept_cell(rows, r, c, w):
                continue
            rows[r].append(w)
            cols[c].append(w)
            yield from fill(nr, nc)
            rows[r].pop()
            cols[c].pop()

    yield from fill(0, 0)


def columns(grid):
    return tuple(zip(*grid))


def show(grid):
    width = max(len(w) for row in grid for w in row)
    return "\n".join(" ".join(w.ljust(width) for w in row).rstrip() for row in grid)
