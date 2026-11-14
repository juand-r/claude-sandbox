"""Build a word grid with a language model and beam search.

The grid is filled cell by cell, row by row. For the next cell the language
model gives two next-word distributions: one after the words to its left
(the row so far) and one after the words above it (the column so far). A
candidate word is scored by the sum of its two log-probabilities, so it has
to continue both lines well. The beam keeps the best partial grids.

Nothing is looked up in a sentence list: a line is judged only by its
probability under the model. Lines need not end a sentence.

Wrap-around (--wrap): the rows are read as one running text (row 2 continues
row 1) and so are the columns (column 2 continues column 1).
  rows: the row context of a cell is all earlier cells in reading order.
  columns: the column context of a cell is the earlier columns down to the
    row above, then the cells above it. While the grid is being filled the
    lower part of the earlier columns does not exist yet, so the context
    jumps from row r-1 of one column to row 0 of the next. In the last row
    the jump disappears: a word there must also make the top of the next
    column a good continuation. That is scored by a look-ahead term for the
    best candidates (see `junction_scores`).

Rules on repeated words (always on):
  - no cell holds the same word as its mirror cell (row and column swapped),
    which excludes symmetric grids;
  - a word occurs at most MAX_PER_LINE times in a row and in a column;
  - each earlier use of a word anywhere in the grid costs --repeat-penalty.

Cells hold single tokens of the model that are whole lowercase words
(contractions such as "don't" are several tokens and are not available yet).

Usage:
  lmgrid.py N_ROWS N_COLS [--beam 32] [--top 40] [--wrap] [--out FILE.json]
"""

import argparse
import json
import pickle
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "HuggingFaceTB/SmolLM2-360M"
BATCH_SIZE = 64
MAX_PER_LINE = 2
MIN_WORD_COUNT = 200    # a token is a word if the corpus word list has it this often
SINGLE_LETTER_WORDS = {"a", "i"}
# Text put before every context. Without it a lowercase word right after the
# start token makes the model expect program code ("void main function").
PREFIX = "The text below is ordinary English prose, in lowercase and without punctuation.\n\n..."


class Model:
    def __init__(self):
        self.tok = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, dtype=torch.float32).eval()
        self.prefix = torch.tensor([self.tok.bos_token_id]
                                   + self.tok(PREFIX, add_special_tokens=False).input_ids)
        self.word_ids, self.words = self._word_tokens()
        self.word_index = {w: i for i, w in enumerate(self.words)}

    def _word_tokens(self, path="data/word_counts.pkl"):
        """Token ids that are whole lowercase words when preceded by a space."""
        with open(path, "rb") as f:
            counts = pickle.load(f)
        ids, words = [], []
        for token, token_id in self.tok.get_vocab().items():
            if not token.startswith("Ġ"):
                continue
            word = token[1:]
            if not (word.isascii() and word.isalpha() and word.islower()):
                continue
            if len(word) == 1 and word not in SINGLE_LETTER_WORDS:
                continue
            if counts.get(word, 0) >= MIN_WORD_COUNT:
                ids.append(token_id)
                words.append(word)
        return torch.tensor(ids), words

    @torch.no_grad()
    def next_word_logprobs(self, contexts):
        """For each context (list of word indices) the log-probability of every
        word as the next token. Returns a tensor [len(contexts), n_words].

        The probabilities are renormalized over the words, so the two
        distributions of a cell are comparable."""
        out = []
        for i in range(0, len(contexts), BATCH_SIZE):
            batch = contexts[i:i + BATCH_SIZE]
            n_pre = len(self.prefix)
            width = max(len(c) for c in batch) + n_pre
            ids = torch.zeros((len(batch), width), dtype=torch.long)
            mask = torch.zeros((len(batch), width), dtype=torch.long)
            for j, c in enumerate(batch):
                ids[j, :n_pre] = self.prefix
                ids[j, n_pre:n_pre + len(c)] = self.word_ids[torch.tensor(c, dtype=torch.long)]
                mask[j, :n_pre + len(c)] = 1
            logits = self.model(input_ids=ids, attention_mask=mask).logits
            last = logits[torch.arange(len(batch)), mask.sum(1) - 1]
            out.append(torch.log_softmax(last[:, self.word_ids], dim=-1))
        return torch.cat(out)

    @torch.no_grad()
    def continuation_logprobs(self, prefixes, continuation):
        """Sum of log-probabilities of the word sequences `continuation[i]`
        after `prefixes[i]` (both lists of word indices)."""
        out = []
        for i in range(0, len(prefixes), BATCH_SIZE):
            pre, con = prefixes[i:i + BATCH_SIZE], continuation[i:i + BATCH_SIZE]
            n_pre = len(self.prefix)
            width = max(len(p) + len(c) for p, c in zip(pre, con)) + n_pre
            ids = torch.zeros((len(pre), width), dtype=torch.long)
            mask = torch.zeros((len(pre), width), dtype=torch.long)
            for j, (p, c) in enumerate(zip(pre, con)):
                seq = torch.tensor(p + c, dtype=torch.long)
                ids[j, :n_pre] = self.prefix
                ids[j, n_pre:n_pre + len(seq)] = self.word_ids[seq]
                mask[j, :n_pre + len(seq)] = 1
            logp = torch.log_softmax(self.model(input_ids=ids, attention_mask=mask).logits, dim=-1)
            for j, (p, c) in enumerate(zip(pre, con)):
                total = 0.0
                for k in range(len(c)):
                    position = n_pre + len(p) + k - 1   # logits here predict the next token
                    total += logp[j, position, ids[j, position + 1]].item()
                out.append(total)
        return out


def row_context(cells, n_cols, wrap):
    """Words before the next cell in row reading order."""
    if wrap:
        return list(cells)
    return list(cells[len(cells) - len(cells) % n_cols:])


def col_context(cells, n_cols, wrap):
    """Words before the next cell in column reading order (see module text)."""
    r, c = divmod(len(cells), n_cols)
    above = [cells[i * n_cols + c] for i in range(r)]
    if not wrap:
        return above
    earlier = [cells[i * n_cols + j] for j in range(c) for i in range(r)]
    return earlier + above


def allowed(cells, n_cols, word):
    """The rules on repeated words for putting `word` into the next cell."""
    r, c = divmod(len(cells), n_cols)
    if c < r and r < n_cols and cells[c * n_cols + r] == word:      # mirror cell
        return False
    in_row = sum(cells[r * n_cols + j] == word for j in range(c))
    in_col = sum(cells[i * n_cols + c] == word for i in range(r))
    return in_row < MAX_PER_LINE and in_col < MAX_PER_LINE


def junction_scores(model, candidates, n_rows, n_cols):
    """Look-ahead for the last row with wrap-around: how well does the top of
    column c+1 follow once column c is complete?

    candidates: list of cell lists that end with a new word in the last row,
    column c < n_cols - 1. Returns, for each, the log-probability of column
    c+1 (rows above the last) after columns 0..c in full, minus the same
    quantity under the context used while filling (which lacked the last
    row). The difference is what the new last-row words change."""
    prefixes, old_prefixes, continuations = [], [], []
    for cells in candidates:
        r, c = divmod(len(cells) - 1, n_cols)
        full = [cells[i * n_cols + j] for j in range(c + 1) for i in range(n_rows)]
        partial = [cells[i * n_cols + j] for j in range(c + 1) for i in range(n_rows - 1)]
        nxt = [cells[i * n_cols + c + 1] for i in range(n_rows - 1)]
        prefixes.append(full)
        old_prefixes.append(partial)
        continuations.append(nxt)
    new = model.continuation_logprobs(prefixes, continuations)
    old = model.continuation_logprobs(old_prefixes, continuations)
    return [a - b for a, b in zip(new, old)]


def beam_search(model, n_rows, n_cols, beam, top, wrap, repeat_penalty, start=None, verbose=True):
    """Return the final beam: list of (score, cells) with cells in row order.

    start: optional list of beams (score, cells) to continue from, e.g. the
    result for fewer rows (without wrap, or to keep adding rows)."""
    beams = start or [(0.0, [])]
    first = len(beams[0][1])
    for cell in range(first, n_rows * n_cols):
        r, c = divmod(cell, n_cols)
        row_lp = model.next_word_logprobs([row_context(cells, n_cols, wrap) for _, cells in beams])
        col_lp = model.next_word_logprobs([col_context(cells, n_cols, wrap) for _, cells in beams])
        combined = row_lp + col_lp
        expansions = []
        for b, (score, cells) in enumerate(beams):
            kept = 0
            for word in torch.argsort(combined[b], descending=True).tolist():
                if kept == top:
                    break
                if allowed(cells, n_cols, word):
                    # Soft limit on repeats: each earlier use of the word costs.
                    penalty = repeat_penalty * cells.count(word)
                    expansions.append((score + combined[b, word].item() - penalty, cells + [word]))
                    kept += 1
        expansions.sort(key=lambda e: -e[0])
        if wrap and r == n_rows - 1 and c < n_cols - 1 and n_rows > 1:
            # Rescore a wider shortlist with the look-ahead term.
            shortlist = expansions[:beam * 4]
            extra = junction_scores(model, [cells for _, cells in shortlist], n_rows, n_cols)
            expansions = sorted(((s + e, cells) for (s, cells), e in zip(shortlist, extra)),
                                key=lambda e: -e[0])
        beams = expansions[:beam]
        if verbose and c == n_cols - 1:
            words = [model.words[w] for w in beams[0][1]]
            print(f"row {r}: best {beams[0][0]:.1f}  " + " ".join(words[-n_cols:]), flush=True)
    return beams


def as_grid(model, cells, n_cols):
    words = [model.words[w] for w in cells]
    return [words[i:i + n_cols] for i in range(0, len(words), n_cols)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("n_rows", type=int)
    p.add_argument("n_cols", type=int)
    p.add_argument("--beam", type=int, default=32)
    p.add_argument("--top", type=int, default=40, help="candidate words per beam and cell")
    p.add_argument("--wrap", action="store_true")
    p.add_argument("--repeat-penalty", type=float, default=2.0,
                   help="cost in nats for each earlier use of a word in the grid")
    p.add_argument("--show", type=int, default=3)
    p.add_argument("--out")
    args = p.parse_args()
    model = Model()
    print(f"{len(model.words)} words", flush=True)
    start = time.time()
    beams = beam_search(model, args.n_rows, args.n_cols, args.beam, args.top, args.wrap,
                        args.repeat_penalty)
    seconds = round(time.time() - start)
    results = []
    for score, cells in beams:
        grid = as_grid(model, cells, args.n_cols)
        results.append({"score": score, "grid": grid})
    for result in results[:args.show]:
        grid = result["grid"]
        width = max(len(w) for row in grid for w in row) + 1
        print(f"\nscore {result['score']:.1f} ({result['score'] / (2 * args.n_rows * args.n_cols):.2f} per word and direction)")
        for row in grid:
            print("  " + "".join(w.ljust(width) for w in row))
        print("  down: " + " / ".join(" ".join(col) for col in zip(*grid)))
    print(f"\n{seconds} s")
    if args.out:
        with open(args.out, "w") as f:
            json.dump({"args": vars(args), "seconds": seconds, "results": results}, f, indent=1)


if __name__ == "__main__":
    main()
