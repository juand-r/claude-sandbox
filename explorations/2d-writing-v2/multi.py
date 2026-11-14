"""Grids whose lines are sequences of sentences (front end for extend.c).

A line is valid if it can be cut into consecutive attested sentences. This
module loads the sentence set, runs the solver, checks grids independently,
and chooses a cutting of each line for display.
"""

import math
import os
import subprocess
import tempfile

from ngrams import load_names
from search import columns
from sentences import load_opensub

HERE = os.path.dirname(os.path.abspath(__file__))
EXTEND = os.path.join(HERE, "extend")
MIN_LEN, MAX_LEN = 2, 7


def load_sentences(min_counts, no_names=True):
    """Sentence set {key: (count, punct)} for lengths MIN_LEN..MAX_LEN.

    min_counts: {length: minimum corpus count}; lengths not listed are left out.
    """
    names = load_names() if no_names else set()
    sentences = {}
    for n, k in min_counts.items():
        if not MIN_LEN <= n <= MAX_LEN:
            raise ValueError(f"length {n} not supported")
        for key, info in load_opensub(n, k).items():
            if names.isdisjoint(key):
                sentences[key] = info
    return sentences


def cuttings(line, sentences):
    """Best cutting of `line` (tuple of words) into sentences, or None.

    Among all valid cuttings, prefer the fewest sentences, then the largest
    sum of log counts. Returns a list of sentence keys."""
    best = [None] * (len(line) + 1)   # best[i] = (n_pieces, -sum_log_count, pieces) for line[:i]
    best[0] = (0, 0.0, [])
    for i in range(1, len(line) + 1):
        for length in range(MIN_LEN, min(MAX_LEN, i) + 1):
            prev = best[i - length]
            key = line[i - length:i]
            if prev is None or key not in sentences:
                continue
            cand = (prev[0] + 1, prev[1] - math.log(sentences[key][0]), prev[2] + [key])
            if best[i] is None or cand[:2] < best[i][:2]:
                best[i] = cand
    return best[-1][2] if best[-1] else None


def check(grid, sentences, max_repeats=0):
    """Raise ValueError unless every row and column of `grid` can be cut into
    sentences and at most max_repeats cells repeat a word."""
    for kind, lines in (("row", grid), ("column", columns(grid))):
        for line in lines:
            if cuttings(tuple(line), sentences) is None:
                raise ValueError(f"{kind} {' '.join(line)!r} is not a sequence of sentences")
    words = [w for row in grid for w in row]
    if len(words) - len(set(words)) > max_repeats:
        raise ValueError("too many repeated words")


def usable_sentences(sentences, seed_grid):
    """Sentences that can still occur when columns are added to the right of
    `seed_grid` and no word may repeat. Removing the others does not change
    the solutions but makes the search much faster.

    A sentence with an already used word can only lie inside a seed line, or
    start inside a seed row, run to its end and continue with new words."""
    used = {w for row in seed_grid for w in row}
    inside, tails = set(), set()
    for line in tuple(seed_grid) + columns(seed_grid):
        for i in range(len(line)):
            for j in range(i + MIN_LEN, min(i + MAX_LEN, len(line)) + 1):
                inside.add(tuple(line[i:j]))
    for row in seed_grid:
        for i in range(max(0, len(row) - MAX_LEN + 1), len(row)):
            tails.add(tuple(row[i:]))
    result = {}
    for key, info in sentences.items():
        n_old = 0   # length of the longest prefix made of used words
        while n_old < len(key) and key[n_old] in used:
            n_old += 1
        if any(w in used for w in key[n_old:]):
            ok = key in inside
        else:
            ok = n_old == 0 or key in inside or key[:n_old] in tails
        if ok:
            result[key] = info
    return result


def run_extend(sentences, n_rows, n_cols, seed_grid=None, max_repeats=0, max_solutions=0,
               max_nodes=0, seed=0, restart_nodes=0, n_procs=1):
    """Return (grids, exhaustive). Grids are tuples of row tuples.

    seed_grid: grid to keep in the top-left corner (or None).
    With seed != 0, n_procs processes run with seeds seed, seed+1, ...;
    max_solutions and max_nodes apply to each process."""
    if not os.path.exists(EXTEND):
        raise FileNotFoundError("compile first: gcc -O2 -o extend extend.c")
    if n_procs > 1 and seed == 0:
        raise ValueError("several processes need a random seed")
    vocab = sorted({w for key in sentences for w in key})
    ids = {w: i for i, w in enumerate(vocab)}
    cells = [[-1] * n_cols for _ in range(n_rows)]
    for r, row in enumerate(seed_grid or ()):
        for c, w in enumerate(row):
            cells[r][c] = ids[w]
    with tempfile.TemporaryDirectory() as tmp:
        sent_path, seed_path = os.path.join(tmp, "sents"), os.path.join(tmp, "seed")
        with open(sent_path, "w") as f:
            for key in sorted(sentences):
                f.write(" ".join(str(ids[w]) for w in key) + "\n")
        with open(seed_path, "w") as f:
            f.write(" ".join(str(x) for row in cells for x in row) + "\n")
        procs = [subprocess.Popen(
            [str(a) for a in (EXTEND, sent_path, seed_path, n_rows, n_cols, max_repeats,
                              max_solutions, max_nodes, seed + p if seed else 0, restart_nodes)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for p in range(n_procs)]
        outputs = [p.communicate() for p in procs]
    grids, exhaustive = set(), True
    for p, (out, err) in zip(procs, outputs):
        if p.returncode != 0:
            raise RuntimeError(f"extend failed: {err}")
        exhaustive = exhaustive and "(exhaustive)" in err
        for line in out.splitlines():
            words = [vocab[int(x)] for x in line.split()]
            grids.add(tuple(tuple(words[r * n_cols:(r + 1) * n_cols]) for r in range(n_rows)))
    return sorted(grids), exhaustive
