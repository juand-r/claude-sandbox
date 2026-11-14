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
NGRAM_SOLVER = os.path.join(HERE, "ngram")


def make_vocab(row_keys, col_keys):
    """Word list that defines the word ids used in the solver files."""
    return sorted({w for k in row_keys for w in k} | {w for k in col_keys for w in k})


def write_inputs(directory, row_keys, col_keys, costs=None):
    """Write the solver input files into `directory`.

    Returns (vocab, [rows_path, cols_path, costs_path])."""
    row_keys, col_keys = set(row_keys), set(col_keys)
    vocab = make_vocab(row_keys, col_keys)
    ids = {w: i for i, w in enumerate(vocab)}
    costs = costs or {}
    paths = []
    for name, keys in (("rows", row_keys), ("cols", col_keys)):
        path = os.path.join(directory, name)
        with open(path, "w") as f:
            for k in sorted(keys):
                f.write(" ".join(str(ids[w]) for w in k) + "\n")
        paths.append(path)
    cost_path = os.path.join(directory, "costs")
    with open(cost_path, "w") as f:
        f.write("\n".join(str(costs.get(w, 0)) for w in vocab) + "\n")
    return vocab, paths + [cost_path]


def decode(line, vocab, n_rows, n_cols):
    """Turn one output line of a solver into a grid (tuple of row tuples)."""
    words = [vocab[int(x)] for x in line.split()]
    return tuple(tuple(words[r * n_cols:(r + 1) * n_cols]) for r in range(n_rows))


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
    with tempfile.TemporaryDirectory() as tmp:
        vocab, paths = write_inputs(tmp, row_keys, col_keys, costs)
        procs = []
        for p in range(n_procs):
            part, n_parts = (p, n_procs) if seed == 0 else (0, 1)
            args = [solver, *paths, n_rows, n_cols, max_repeats, max_cost,
                    max_solutions, max_nodes, seed + p if seed else 0]
            if algorithm == "trie":
                args += [temp, restart_nodes]
            args += [part, n_parts]
            procs.append(subprocess.Popen([str(a) for a in args], stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE, text=True))
        outputs = [p.communicate() for p in procs]
        for p, (_, stderr) in zip(procs, outputs):
            if p.returncode != 0:
                raise RuntimeError(f"solver failed: {stderr}")
    grids = {decode(line, vocab, n_rows, n_cols)
             for stdout, _ in outputs for line in stdout.splitlines()}
    exhaustive = all("(exhaustive)" in stderr for _, stderr in outputs)
    if verbose:
        for _, stderr in outputs:
            print(stderr.strip())
    return sorted(grids), exhaustive


def run_ngram(row_grams, col_grams, n_rows, n_cols, k, max_repeats=0, costs=None,
              max_cost=0, max_solutions=0, max_nodes=0, seed=0, restart_nodes=0,
              n_procs=1, verbose=False):
    """Search grids whose lines are admissible under k-gram rules (ngram.c).

    row_grams, col_grams: triples (P, M, F) of sets of k-word tuples, as
        returned by ngrams.build_kgrams. Pass the same triple twice for the
        same rules in both directions.
    Other parameters as in run_solver. Returns (grids, exhaustive).
    """
    if not os.path.exists(NGRAM_SOLVER):
        raise FileNotFoundError("compile first; see README.md")
    sets = list(row_grams) + list(col_grams)
    vocab = sorted({w for s in sets for g in s for w in g})
    ids = {w: i for i, w in enumerate(vocab)}
    costs = costs or {}
    with tempfile.TemporaryDirectory() as tmp:
        paths = []
        for i, grams in enumerate(sets):
            path = os.path.join(tmp, f"grams{i}")
            if i >= 3 and col_grams[i - 3] is row_grams[i - 3]:
                path = paths[i - 3]
            else:
                with open(path, "w") as f:
                    for g in grams:
                        f.write(" ".join(str(ids[w]) for w in g) + "\n")
            paths.append(path)
        cost_path = os.path.join(tmp, "costs")
        with open(cost_path, "w") as f:
            f.write("\n".join(str(costs.get(w, 0)) for w in vocab) + "\n")
        procs = []
        for p in range(n_procs):
            part, n_parts = (p, n_procs) if seed == 0 else (0, 1)
            args = [NGRAM_SOLVER, *paths, cost_path, n_rows, n_cols, k, max_repeats, max_cost,
                    max_solutions, max_nodes, seed + p if seed else 0, restart_nodes,
                    part, n_parts]
            procs.append(subprocess.Popen([str(a) for a in args], stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE, text=True))
        outputs = [p.communicate() for p in procs]
        for p, (_, stderr) in zip(procs, outputs):
            if p.returncode != 0:
                raise RuntimeError(f"ngram solver failed: {stderr}")
    grids = {decode(line, vocab, n_rows, n_cols)
             for stdout, _ in outputs for line in stdout.splitlines()}
    if verbose:
        for _, stderr in outputs:
            print(stderr.strip())
    return sorted(grids), all("(exhaustive)" in stderr for _, stderr in outputs)
