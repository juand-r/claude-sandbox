"""
2D Writing System v3 - Flowing horizontal text with independent column sentences.

Horizontal: Read left-to-right, wrapping at line ends = one continuous passage.
Vertical: Each column is an independent sentence (no wrapping between columns).

Usage:
    python grid2d_v3.py              # Use n-gram (default)
    python grid2d_v3.py --gpt2       # Use GPT-2
"""

import argparse
import math
from collections import defaultdict
from typing import List, Tuple, Optional
from dataclasses import dataclass
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

    def get_top_p(self, context: List[str], p: float, vocab: List[str] = None) -> List[Tuple[str, float]]:
        """Get words using nucleus (top-p) sampling - smallest set with cumulative prob >= p."""
        # Use last n-1 words of context
        context = tuple(w.lower() for w in context[-(self.n-1):])
        while len(context) < self.n - 1:
            context = ('<s>',) + context

        if vocab is None:
            vocab = list(self.vocab)

        # Compute probabilities
        total = self.context_counts[context]
        vocab_size = len(self.vocab)

        scores = []
        for word in vocab:
            count = self.ngram_counts[context][word]
            prob = (count + self.smoothing) / (total + self.smoothing * vocab_size)
            scores.append((word, prob, math.log(prob)))

        # Sort by probability descending
        scores.sort(key=lambda x: x[1], reverse=True)

        # Take smallest set with cumulative prob >= p
        result = []
        cumulative = 0.0
        for word, prob, log_prob in scores:
            result.append((word, log_prob))
            cumulative += prob
            if cumulative >= p:
                break

        return result


@dataclass
class Beam:
    """A partial grid being constructed."""
    grid: List[List[Optional[str]]]
    score: float = 0.0

    def copy(self) -> 'Beam':
        return Beam(
            grid=[row.copy() for row in self.grid],
            score=self.score
        )

    def get_horizontal_context(self, row: int, col: int) -> List[str]:
        """Get all words before this position in reading order (left-to-right, top-to-bottom)."""
        words = []
        n_cols = len(self.grid[0]) if self.grid else 0
        for r in range(row + 1):
            for c in range(n_cols):
                if r == row and c >= col:
                    break
                if self.grid[r][c] is not None:
                    words.append(self.grid[r][c])
        return words

    def get_column_context(self, row: int, col: int) -> List[str]:
        """Get words above in this column."""
        return [self.grid[r][col] for r in range(row) if self.grid[r][col] is not None]

    def set_cell(self, row: int, col: int, word: str, score_delta: float):
        self.grid[row][col] = word
        self.score += score_delta

    def __str__(self):
        lines = []
        for row in self.grid:
            line = " ".join(w if w else "___" for w in row)
            lines.append(line)
        return "\n".join(lines)


def beam_search_v3(
    lm: NgramLM,
    vocab: List[str],
    n_rows: int = 4,
    n_cols: int = 4,
    p: float = 0.9,
    beam_width: int = 100,
    verbose: bool = True
) -> List[Beam]:
    """
    Beam search for v3 grid using top-p (nucleus) sampling.

    Fill in row-major order. Each word must be:
    - In top-p nucleus given horizontal context (all previous words in reading order)
    - In top-p nucleus given column context (words above in same column)
    """
    if verbose:
        print(f"v3 Beam Search: {n_rows}x{n_cols}, p={p}, beam_width={beam_width}")

    initial_grid = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    beams = [Beam(grid=initial_grid, score=0.0)]

    start_words = VALID_STARTERS & set(vocab)

    for row in range(n_rows):
        for col in range(n_cols):
            if verbose:
                print(f"  Cell ({row},{col}), {len(beams)} beams...")

            new_beams = []

            for beam in beams:
                h_context = beam.get_horizontal_context(row, col)
                c_context = beam.get_column_context(row, col)

                h_top_p = lm.get_top_p(h_context, p, vocab)
                c_top_p = lm.get_top_p(c_context, p, vocab)

                h_words = {w for w, _ in h_top_p}
                c_words = {w for w, _ in c_top_p}
                h_scores = {w: s for w, s in h_top_p}
                c_scores = {w: s for w, s in c_top_p}

                if row == 0:
                    # First row: column context is empty, word starts a column
                    # Must be valid starter AND in horizontal nucleus
                    candidates = [(w, s) for w, s in h_top_p if w in start_words]
                    if not candidates:
                        candidates = h_top_p
                else:
                    # Interior cell: intersection of horizontal and column nuclei
                    intersection = h_words & c_words
                    if not intersection:
                        continue  # branch dies
                    candidates = [(w, h_scores[w] + c_scores[w]) for w in intersection]
                    candidates.sort(key=lambda x: x[1], reverse=True)

                for word, word_score in candidates:
                    new_beam = beam.copy()
                    new_beam.set_cell(row, col, word, word_score)
                    new_beams.append(new_beam)

            if not new_beams:
                if verbose:
                    print(f"  All beams died at ({row},{col})!")
                break

            new_beams.sort(key=lambda b: b.score, reverse=True)
            beams = new_beams[:beam_width]

    if verbose:
        print(f"  Final: {len(beams)} beams")

    return beams


def display_results(beams: List[Beam], n: int = 5):
    """Display top n results."""
    print(f"\n{'='*60}")
    print(f"TOP {min(n, len(beams))} RESULTS")
    print('='*60)

    for i, beam in enumerate(beams[:n]):
        print(f"\n--- Result {i+1} (score: {beam.score:.2f}) ---")
        print("\nGrid:")
        print(beam)

        n_rows = len(beam.grid)
        n_cols = len(beam.grid[0]) if beam.grid else 0

        # Show horizontal reading
        h_words = []
        for row in beam.grid:
            h_words.extend([w for w in row if w])
        print(f"\nHorizontal: {' '.join(h_words)}")

        # Show each column
        print("\nColumns:")
        for c in range(n_cols):
            col_words = [beam.grid[r][c] for r in range(n_rows) if beam.grid[r][c]]
            print(f"  C{c+1}: {' '.join(col_words)}")


VOCAB = [
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

VALID_STARTERS = {
    "i", "you", "he", "she", "it", "we", "they",
    "the", "a", "an", "this", "that", "my", "your", "his", "her",
    "do", "does", "did", "will", "would", "could", "can", "have", "has", "had",
    "man", "woman", "child", "time", "day", "night", "life", "world",
    "now", "then", "there", "just", "only", "even", "still", "also",
    "but", "so", "if", "when",
    "all", "some", "no", "not",
}


def main():
    parser = argparse.ArgumentParser(description="2D Writing System v3")
    parser.add_argument("--rows", type=int, default=4, help="Number of rows")
    parser.add_argument("--cols", type=int, default=4, help="Number of columns")
    parser.add_argument("--p", type=float, default=0.9, help="Top-p nucleus threshold (default: 0.9)")
    parser.add_argument("--beam", type=int, default=100, help="Beam width (default: 100)")
    parser.add_argument("--top", type=int, default=5, help="Results to show")
    args = parser.parse_args()

    print("Loading Brown corpus...")
    nltk.download('brown', quiet=True)
    sentences = brown.sents()
    print(f"  {len(sentences)} sentences")

    lm = NgramLM(n=3)
    lm.train(sentences)

    print(f"\n{'#'*60}")
    print(f"GRID: {args.rows} rows x {args.cols} columns")
    print('#'*60)

    beams = beam_search_v3(lm, VOCAB, n_rows=args.rows, n_cols=args.cols, p=args.p, beam_width=args.beam)
    display_results(beams, n=args.top)


if __name__ == "__main__":
    main()
