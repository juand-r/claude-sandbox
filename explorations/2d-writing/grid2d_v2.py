"""
2D Writing System v2 - True 2D beam search with intersection.

Key insight: for interior cells, only accept tokens that are likely
in BOTH row and column contexts (intersection, not sum).

Usage:
    python grid2d_v2.py              # Use n-gram (default)
    python grid2d_v2.py --gpt2       # Use GPT-2
"""

import argparse
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


class GPT2LM:
    """GPT-2 language model wrapper."""

    def __init__(self, model_path: str = "gpt2"):
        """
        Load GPT-2 model.

        Args:
            model_path: HuggingFace model name or local path to model directory
        """
        import torch

        try:
            from transformers import GPT2LMHeadModel, GPT2Tokenizer
        except ImportError:
            raise ImportError("transformers not installed. Run: pip install transformers")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading GPT-2 from '{model_path}' on {self.device}...")

        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
            self.model = GPT2LMHeadModel.from_pretrained(model_path).to(self.device)
        except Exception as e:
            if "403" in str(e) or "Proxy" in str(e):
                raise RuntimeError(
                    f"Cannot download model (proxy blocked).\n"
                    f"To use GPT-2, download the model manually and specify path:\n"
                    f"  1. Download from https://huggingface.co/gpt2\n"
                    f"  2. Run: python grid2d_v2.py --gpt2 --model-path /path/to/gpt2\n"
                    f"Original error: {e}"
                )
            raise

        self.model.eval()

        # Cache: word -> token_id (for single-token words)
        self._word_to_token = {}
        self._multi_token_words = set()

        print("  GPT-2 loaded")

    def _prepare_vocab(self, vocab: List[str]):
        """Pre-compute token mappings for vocabulary."""
        for word in vocab:
            if word in self._word_to_token or word in self._multi_token_words:
                continue
            # GPT-2 expects space before word (except at start)
            tokens = self.tokenizer.encode(" " + word, add_special_tokens=False)
            if len(tokens) == 1:
                self._word_to_token[word] = tokens[0]
            else:
                self._multi_token_words.add(word)

    def get_top_k(self, context: List[str], k: int, vocab: List[str] = None) -> List[Tuple[str, float]]:
        """Get top-k most likely words given context."""
        import torch
        import torch.nn.functional as F

        if vocab is None:
            raise ValueError("GPT2LM requires explicit vocab")

        self._prepare_vocab(vocab)

        # Build context string
        if context:
            context_str = " ".join(context)
        else:
            context_str = ""

        # Encode context
        if context_str:
            input_ids = self.tokenizer.encode(context_str, return_tensors="pt").to(self.device)
        else:
            # Use BOS or just predict from nothing
            input_ids = torch.tensor([[self.tokenizer.bos_token_id or 50256]]).to(self.device)

        # Get logits for next token
        with torch.no_grad():
            outputs = self.model(input_ids)
            next_token_logits = outputs.logits[0, -1, :]  # [vocab_size]
            log_probs = F.log_softmax(next_token_logits, dim=-1)

        # Score each vocab word
        scores = []
        for word in vocab:
            if word in self._word_to_token:
                token_id = self._word_to_token[word]
                score = log_probs[token_id].item()
            else:
                # Multi-token word: compute joint probability
                tokens = self.tokenizer.encode(" " + word, add_special_tokens=False)
                # For simplicity, use first token's probability (approximation)
                score = log_probs[tokens[0]].item()
                # Penalize multi-token slightly
                score -= 0.5 * (len(tokens) - 1)
            scores.append((word, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]

    def train(self, sentences):
        """No-op for GPT-2 (pretrained)."""
        pass


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

    # Use curated set of valid phrase starters (not LM predictions, which are unreliable)
    start_words = VALID_STARTERS & set(vocab)

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
                # First cell: must be a valid starter (will start both row 0 and col 0)
                candidates = [(w, s) for w, s in row_top_k if w in start_words]
                if not candidates:
                    candidates = row_top_k  # fallback
            elif row == 0:
                # First row: must be good for row AND be valid column starter
                # (these words will start columns)
                intersection = row_words & start_words
                if not intersection:
                    # Fallback to row-only if no intersection
                    candidates = row_top_k
                else:
                    # Filter row_top_k to only include valid starters
                    candidates = [(w, s) for w, s in row_top_k if w in start_words]
            elif col == 0:
                # First column: must be good for column AND be valid row starter
                # (these words will start rows)
                intersection = col_words & start_words
                if not intersection:
                    # Fallback to col-only if no intersection
                    candidates = col_top_k
                else:
                    # Filter col_top_k to only include valid starters
                    candidates = [(w, s) for w, s in col_top_k if w in start_words]
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


def is_symmetric(beam: Beam) -> bool:
    """Check if grid is symmetric (rows == columns)."""
    n_rows = len(beam.grid)
    n_cols = len(beam.grid[0]) if beam.grid else 0
    if n_rows != n_cols:
        return False
    for r in range(n_rows):
        for c in range(n_cols):
            if beam.grid[r][c] != beam.grid[c][r]:
                return False
    return True


def display_results(beams: List[Beam], lm: NgramLM, n: int = 5, show_symmetric: bool = True):
    """Display top n results."""
    print(f"\n{'='*60}")
    print(f"TOP {min(n, len(beams))} RESULTS")
    print('='*60)

    # Separate symmetric and non-symmetric
    symmetric = [b for b in beams if is_symmetric(b)]
    non_symmetric = [b for b in beams if not is_symmetric(b)]

    print(f"\n[{len(symmetric)} symmetric, {len(non_symmetric)} non-symmetric out of {len(beams)} total]")

    # Show non-symmetric first (more interesting)
    shown = 0

    if non_symmetric:
        print(f"\n*** NON-SYMMETRIC RESULTS ***")
        for i, beam in enumerate(non_symmetric[:n]):
            if shown >= n:
                break
            print(f"\n--- Non-sym {i+1} (score: {beam.score:.2f}) ---")
            print(beam)
            _print_rows_cols(beam)
            shown += 1

    if show_symmetric and shown < n and symmetric:
        print(f"\n*** SYMMETRIC RESULTS ***")
        for i, beam in enumerate(symmetric[:n - shown]):
            print(f"\n--- Sym {i+1} (score: {beam.score:.2f}) ---")
            print(beam)
            _print_rows_cols(beam)


def _print_rows_cols(beam: Beam):
    """Helper to print rows and columns."""
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

# Words that can validly start a sentence/phrase
# (pronouns, articles, demonstratives, some verbs, some adverbs)
VALID_STARTERS = {
    # Pronouns
    "i", "you", "he", "she", "it", "we", "they",
    # Articles/determiners
    "the", "a", "an", "this", "that", "my", "your", "his", "her",
    # Some verbs that can start sentences
    "do", "does", "did", "will", "would", "could", "can", "have", "has", "had",
    # Nouns that can start (as subjects)
    "man", "woman", "child", "time", "day", "night", "life", "world",
    # Common sentence-starting adverbs
    "now", "then", "there", "here", "just", "only", "even", "still", "also",
    # Conjunctions that can start (in certain contexts)
    "but", "so", "if", "when",
    # Other
    "all", "some", "no", "not",
}


def main():
    parser = argparse.ArgumentParser(description="2D Writing System")
    parser.add_argument("--gpt2", action="store_true", help="Use GPT-2 instead of n-gram")
    parser.add_argument("--model-path", type=str, default="gpt2",
                        help="Path to GPT-2 model (local dir or HuggingFace name)")
    parser.add_argument("--size", type=int, nargs="+", default=[4, 5, 6],
                        help="Grid sizes to try (default: 4 5 6)")
    parser.add_argument("--k", type=int, default=500, help="Beam width (default: 500)")
    parser.add_argument("--top", type=int, default=10, help="Number of results to show (default: 10)")
    args = parser.parse_args()

    # Create language model
    if args.gpt2:
        lm = GPT2LM(model_path=args.model_path)
    else:
        print("Loading Brown corpus...")
        nltk.download('brown', quiet=True)
        sentences = brown.sents()
        print(f"  {len(sentences)} sentences")
        lm = NgramLM(n=3)
        lm.train(sentences)

    # Run for each grid size
    for size in args.size:
        print(f"\n{'#'*60}")
        print(f"GRID SIZE: {size}x{size}")
        print('#'*60)

        beams = beam_search_2d(lm, VOCAB, n_rows=size, n_cols=size, k=args.k, verbose=True)
        display_results(beams, lm, n=args.top)


if __name__ == "__main__":
    main()
