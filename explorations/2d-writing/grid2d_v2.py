"""
2D Writing System v2 - True 2D beam search with intersection.

Key insight: for interior cells, only accept tokens that are likely
in BOTH row and column contexts (intersection, not sum).
"""

import numpy as np
from collections import defaultdict
from typing import List, Tuple, Dict, Set, Optional
import random
from dataclasses import dataclass, field
import time
import math
import nltk
from nltk.corpus import brown


class NgramLM:
    """N-gram language model."""

    def __init__(self, n: int = 3):
        self.n = n
        self.ngram_counts = defaultdict(lambda: defaultdict(int))
        self.context_counts = defaultdict(int)
        self.vocab = set()
        self.smoothing = 0.01

    def train(self, sentences: List[List[str]]):
        print(f"Training {self.n}-gram model...")
        for sent in sentences:
            sent = [w.lower() for w in sent if w.isalpha()]
            if len(sent) < 2:
                continue
            padded = ['<s>'] * (self.n - 1) + sent
            for i in range(self.n - 1, len(padded)):
                context = tuple(padded[i - self.n + 1:i])
                word = padded[i]
                self.ngram_counts[context][word] += 1
                self.context_counts[context] += 1
                self.vocab.add(word)
        print(f"  Vocab size: {len(self.vocab)}, contexts: {len(self.context_counts)}")

    def get_top_k(self, context: List[str], k: int, vocab: List[str] = None) -> List[Tuple[str, float]]:
        """Get top-k most likely words given context."""
        context = tuple(w.lower() for w in context[-(self.n-1):])
        while len(context) < self.n - 1:
            context = ('<s>',) + context

        if vocab is None:
            vocab = list(self.vocab)

        scores = []
        total = self.context_counts[context]
        vocab_size = len(self.vocab)

        for word in vocab:
            count = self.ngram_counts[context][word]
            prob = (count + self.smoothing) / (total + self.smoothing * vocab_size)
            scores.append((word, math.log(prob)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]


@dataclass
class Beam:
    """A partial grid being constructed."""
    grid: List[List[Optional[str]]]  # None for unfilled cells
    score: float = 0.0

    def copy(self) -> 'Beam':
        return Beam(
            grid=[row.copy() for row in self.grid],
            score=self.score
        )

    def get_row_context(self, row: int, col: int) -> List[str]:
        """Get filled words to the left in this row."""
        return [w for w in self.grid[row][:col] if w is not None]

    def get_col_context(self, row: int, col: int) -> List[str]:
        """Get filled words above in this column."""
        return [self.grid[r][col] for r in range(row) if self.grid[r][col] is not None]

    def set_cell(self, row: int, col: int, word: str, score_delta: float):
        """Set a cell and update score."""
        self.grid[row][col] = word
        self.score += score_delta

    def __str__(self):
        lines = []
        for row in self.grid:
            line = " ".join(w if w else "___" for w in row)
            lines.append(line)
        return "\n".join(lines)


def diagonal_order(n_rows: int, n_cols: int) -> List[Tuple[int, int]]:
    """Generate cells in diagonal order: (0,0), (0,1), (1,0), (0,2), (1,1), (2,0), ..."""
    cells = []
    for diag in range(n_rows + n_cols - 1):
        for row in range(max(0, diag - n_cols + 1), min(diag + 1, n_rows)):
            col = diag - row
            if col < n_cols:
                cells.append((row, col))
    return cells


def beam_search_2d(
    lm: NgramLM,
    vocab: List[str],
    n_rows: int = 3,
    n_cols: int = 3,
    k: int = 50,  # beam width / top-k
    verbose: bool = True
) -> List[Beam]:
    """
    True 2D beam search.

    For interior cells (row > 0 and col > 0), we take the INTERSECTION
    of top-k from row context and top-k from column context.
    """
    if verbose:
        print(f"2D Beam Search: {n_rows}x{n_cols}, k={k}")

    # Initialize with empty grid
    initial_grid = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    beams = [Beam(grid=initial_grid, score=0.0)]

    cells = diagonal_order(n_rows, n_cols)

    for cell_idx, (row, col) in enumerate(cells):
        if verbose:
            print(f"  Cell ({row},{col}), {len(beams)} beams...")

        new_beams = []

        for beam in beams:
            row_context = beam.get_row_context(row, col)
            col_context = beam.get_col_context(row, col)

            # Get top-k from each context
            row_top_k = lm.get_top_k(row_context, k, vocab)
            col_top_k = lm.get_top_k(col_context, k, vocab)

            row_words = {w for w, _ in row_top_k}
            col_words = {w for w, _ in col_top_k}
            row_scores = {w: s for w, s in row_top_k}
            col_scores = {w: s for w, s in col_top_k}

            if row == 0 and col == 0:
                # First cell: just use top-k
                candidates = row_top_k
            elif row == 0:
                # First row: only row context matters
                candidates = row_top_k
            elif col == 0:
                # First column: only column context matters
                candidates = col_top_k
            else:
                # Interior cell: INTERSECTION
                intersection = row_words & col_words
                if not intersection:
                    # This branch dies
                    continue
                # Score by sum of both log probs
                candidates = [(w, row_scores[w] + col_scores[w]) for w in intersection]
                candidates.sort(key=lambda x: x[1], reverse=True)

            # Expand beam with each candidate
            for word, word_score in candidates[:k]:
                new_beam = beam.copy()
                new_beam.set_cell(row, col, word, word_score)
                new_beams.append(new_beam)

        if not new_beams:
            if verbose:
                print(f"  All beams died at ({row},{col})!")
            break

        # Keep top-k beams by total score
        new_beams.sort(key=lambda b: b.score, reverse=True)
        beams = new_beams[:k]

    if verbose:
        print(f"  Final: {len(beams)} beams")

    return beams


def display_results(beams: List[Beam], lm: NgramLM, n: int = 5):
    """Display top n results."""
    print(f"\n{'='*60}")
    print(f"TOP {min(n, len(beams))} RESULTS")
    print('='*60)

    for i, beam in enumerate(beams[:n]):
        print(f"\n--- Result {i+1} (score: {beam.score:.2f}) ---")
        print(beam)

        # Show rows and columns as sentences
        n_rows = len(beam.grid)
        n_cols = len(beam.grid[0]) if beam.grid else 0

        print("\nRows:")
        for r in range(n_rows):
            row_words = [w for w in beam.grid[r] if w]
            print(f"  R{r+1}: {' '.join(row_words)}")

        print("Columns:")
        for c in range(n_cols):
            col_words = [beam.grid[r][c] for r in range(n_rows) if beam.grid[r][c]]
            print(f"  C{c+1}: {' '.join(col_words)}")


def main():
    # Load corpus
    print("Loading Brown corpus...")
    nltk.download('brown', quiet=True)
    sentences = brown.sents()
    print(f"  {len(sentences)} sentences")

    # Train LM
    lm = NgramLM(n=3)
    lm.train(sentences)

    # Common words vocabulary
    vocab = [
        "the", "a", "an", "this", "that", "my", "your", "his", "her",
        "i", "you", "he", "she", "it", "we", "they",
        "man", "woman", "child", "time", "day", "night", "life", "world",
        "way", "place", "house", "hand", "eye", "head", "heart", "mind",
        "is", "are", "was", "were", "be", "have", "has", "had",
        "do", "does", "did", "will", "would", "could", "can",
        "see", "know", "think", "make", "take", "come", "go", "want",
        "say", "said", "get", "give", "find", "tell", "feel", "become",
        "good", "new", "old", "great", "little", "own", "other", "long",
        "to", "of", "in", "for", "on", "with", "at", "by", "from",
        "and", "but", "or", "if", "when", "so", "as", "than",
        "not", "all", "some", "no", "more", "just", "now", "then",
        "very", "also", "well", "only", "even", "still", "back", "there",
    ]

    # Try different grid sizes
    for size in [3, 4, 5]:
        print(f"\n{'#'*60}")
        print(f"GRID SIZE: {size}x{size}")
        print('#'*60)

        beams = beam_search_2d(lm, vocab, n_rows=size, n_cols=size, k=300, verbose=True)
        display_results(beams, lm, n=3)


if __name__ == "__main__":
    main()
