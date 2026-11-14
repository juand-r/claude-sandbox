"""Python front end for the C solvers.

Two programs solve the same problem with the same output:
  fill.c    fills the most constrained row or column first (default, faster)
  solver.c  fills cells in row-major order with tries; it also has a guided
            random search with restarts (temp, restart_nodes)
"""

import os
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOLVERS = {"fill": os.path.join(HERE, "fill"), "trie": os.path.join(HERE, "solver")}


def run_solver(row_keys, col_keys, n_rows, n_cols, max_repeats=0, costs=None,
               max_cost=0, max_solutions=0, max_nodes=0, seed=0, temp=-1.0,
               restart_nodes=0, n_procs=1, verbose=False, algorithm="fill"):
    """Return (grids, exhaustive). Each grid is a tuple of row tuples of words.

    row_keys: iterable of word tuples of length n_cols; col_keys: length n_rows.
    costs: {word: int}; words not listed cost 0. The sum of costs over the
        grid's cells must not exceed max_cost.
    n_procs: number of solver processes. With seed == 0 they split the search
        by the top-left word; with seed != 0 each gets its own seed.
        max_solutions and max_nodes apply to each process.
    temp, restart_nodes: only for algorithm="trie"; see solver.c.
    Duplicate grids are removed.
    """
    solver = SOLVERS[algorithm]
    if not os.path.exists(solver):
        raise FileNotFoundError("compile first; see README.md")
    row_keys, col_keys = set(row_keys), set(col_keys)
    vocab = sorted({w for k in row_keys for w in k} | {w for k in col_keys for w in k})
    ids = {w: i for i, w in enumerate(vocab)}
    costs = costs or {}
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for name, keys in (("rows", row_keys), ("cols", col_keys)):
            path = os.path.join(tmp, name)
            with open(path, "w") as f:
                for k in keys:
                    f.write(" ".join(str(ids[w]) for w in k) + "\n")
            paths.append(path)
        cost_path = os.path.join(tmp, "costs")
        with open(cost_path, "w") as f:
            f.write("\n".join(str(costs.get(w, 0)) for w in vocab) + "\n")
        procs = []
        for p in range(n_procs):
            part, n_parts = (p, n_procs) if seed == 0 else (0, 1)
            args = [solver, *paths, cost_path, n_rows, n_cols, max_repeats, max_cost,
                    max_solutions, max_nodes, seed + p if seed else 0]
            if algorithm == "trie":
                args += [temp, restart_nodes]
            args += [part, n_parts]
            procs.append(subprocess.Popen([str(a) for a in args], stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE, text=True))
        outputs = [p.communicate() for p in procs]
        for p in procs:
            if p.returncode != 0:
                raise RuntimeError(f"solver failed: {p.stderr}")
    grids = set()
    for stdout, _ in outputs:
        for line in stdout.splitlines():
            words = [vocab[int(x)] for x in line.split()]
            grids.add(tuple(tuple(words[r * n_cols:(r + 1) * n_cols]) for r in range(n_rows)))
    exhaustive = all("(exhaustive)" in stderr for _, stderr in outputs)
    if verbose:
        for _, stderr in outputs:
            print(stderr.strip())
    return sorted(grids), exhaustive
