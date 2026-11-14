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
    """A grid and its transpose are the same piece of writing; pick one."""
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
