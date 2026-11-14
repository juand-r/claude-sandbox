"""Features for ranking grids.

For a grid of words we compute:
  min_count   smallest corpus count among its row and column sentences
  n_content   number of cells whose word is outside the N_COMMON most frequent
  fluency     mean log-probability per token of the row and column sentences,
              each scored on its own by the language model
  coherence   how much the lines help predict each other. For the rows read as
              one passage, PMI = logP(passage) - sum of logP(each sentence);
              the same for the columns. coherence = (PMI_rows + PMI_cols) / number
              of lines. Positive means the sentences fit together better than
              unrelated sentences would.
"""

import pickle

from search import columns

N_COMMON = 200


def load_caps(path="data/caps.tsv"):
    with open(path) as f:
        return dict(line.rstrip("\n").split("\t") for line in f)


def load_common_words(path="data/word_counts.pkl", n=N_COMMON):
    with open(path, "rb") as f:
        counts = pickle.load(f)
    return {w for w, _ in counts.most_common(n)}


def surface(key, punct, caps):
    """Sentence as it would be written: capitals and final punctuation."""
    words = [caps.get(w, w) for w in key]
    words[0] = words[0][0].upper() + words[0][1:]
    return " ".join(words) + punct


def canonical(grid):
    """A square grid and its transpose are the same piece of writing; pick
    one. Rectangular grids are returned unchanged, to keep one orientation."""
    if len(grid) != len(grid[0]):
        return grid
    return min(grid, columns(grid))


def features(grids, sentence_sets, scorer, caps, common):
    """Return one feature dict per grid.

    sentence_sets: {length: {key: (count, punct)}} covering all rows and columns.
    """
    def info(key):
        return sentence_sets[len(key)][key]

    def text(key):
        return surface(key, info(key)[1], caps)

    lines = [list(g) + list(columns(g)) for g in grids]
    unique = sorted({key for ls in lines for key in ls})
    sent_lp = dict(zip(unique, scorer.logprobs([text(k) for k in unique])))
    passages = []
    for g in grids:
        passages.append(" ".join(text(k) for k in g))
        passages.append(" ".join(text(k) for k in columns(g)))
    passage_lp = scorer.logprobs(passages)

    result = []
    for i, (g, ls) in enumerate(zip(grids, lines)):
        n_rows = len(g)
        row_pmi = passage_lp[2 * i][0] - sum(sent_lp[k][0] for k in ls[:n_rows])
        col_pmi = passage_lp[2 * i + 1][0] - sum(sent_lp[k][0] for k in ls[n_rows:])
        result.append({
            "grid": g,
            "min_count": min(info(k)[0] for k in ls),
            "n_content": sum(w not in common for row in g for w in row),
            "fluency": sum(sent_lp[k][0] for k in ls) / sum(sent_lp[k][1] for k in ls),
            "row_pmi": row_pmi,
            "col_pmi": col_pmi,
            "coherence": (row_pmi + col_pmi) / len(ls),
            "rows_text": passages[2 * i],
            "cols_text": passages[2 * i + 1],
        })
    return result


# Weights of the standardized features in the combined score. Chosen by
# reading the top of the 4x4 list under a few settings (see NOTES.md); they
# are a judgment call, not fitted to data.
WEIGHTS = {"fluency": 1.0, "coherence": 1.0, "n_content": 0.5}


def combined_scores(feats, weights=WEIGHTS):
    """Weighted sum of z-scores of the features, one score per grid."""
    scores = [0.0] * len(feats)
    for key, weight in weights.items():
        values = [f[key] for f in feats]
        mean = sum(values) / len(values)
        sd = (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5
        if sd > 0:
            scores = [s + weight * (v - mean) / sd for s, v in zip(scores, values)]
    return scores


def diverse_top(feats, scores, n, max_shared):
    """Best-scoring grids, skipping any that shares more than max_shared
    words with a grid already chosen. Without this the top of the list is one
    grid repeated with single-word changes."""
    chosen, chosen_words = [], []
    for i in sorted(range(len(feats)), key=lambda i: -scores[i]):
        words = {w for row in feats[i]["grid"] for w in row}
        if all(len(words & other) <= max_shared for other in chosen_words):
            chosen.append(i)
            chosen_words.append(words)
            if len(chosen) == n:
                break
    return chosen
