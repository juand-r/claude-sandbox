"""Python front end for the C solver (solver.c)."""

import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOLVER = os.path.join(HERE, "solver")


def run_solver(row_keys, col_keys, n_rows, n_cols, max_repeats=0,
               max_solutions=0, max_nodes=0, seed=0):
    """Return (grids, exhaustive). Each grid is a tuple of row tuples of words.

    row_keys: iterable of word tuples of length n_cols; col_keys: length n_rows.
    See solver.c for the meaning of the limits and the seed.
    """
    if not os.path.exists(SOLVER):
        raise FileNotFoundError("compile first: gcc -O2 -o solver solver.c")
    row_keys, col_keys = set(row_keys), set(col_keys)
    vocab = sorted({w for k in row_keys for w in k} | {w for k in col_keys for w in k})
    ids = {w: i for i, w in enumerate(vocab)}
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name, keys in (("rows", row_keys), ("cols", col_keys)):
            path = os.path.join(tmp, name)
            with open(path, "w") as f:
                for k in keys:
                    f.write(" ".join(str(ids[w]) for w in k) + "\n")
            paths.append(path)
        out = subprocess.run(
            [SOLVER, *paths, str(n_rows), str(n_cols), str(max_repeats),
             str(max_solutions), str(max_nodes), str(seed)],
            capture_output=True, text=True, check=True)
    grids = []
    for line in out.stdout.splitlines():
        words = [vocab[int(x)] for x in line.split()]
        grids.append(tuple(tuple(words[r * n_cols:(r + 1) * n_cols]) for r in range(n_rows)))
    return grids, "(exhaustive)" in out.stderr
