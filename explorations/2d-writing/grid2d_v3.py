"""
2D Writing System v3 - Flowing horizontal text with independent column sentences.

Horizontal: Read left-to-right, wrapping at line ends = one continuous passage.
Vertical: Each column is an independent sentence (no wrapping between columns).

Uses GPT-2 with top-p sampling, no artificial vocab restrictions.
"""

import argparse
import math
from typing import List, Tuple, Optional
from dataclasses import dataclass

import torch
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class GPT2LM:
    """GPT-2 language model with top-p sampling."""

    def __init__(self, model_name: str = "gpt2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Loading GPT-2 '{model_name}' on {self.device}...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name).to(self.device)
        self.model.eval()
        print("  Loaded.")

    def get_top_p(self, context: List[str], p: float, max_words: int = 50, alpha_only: bool = False, prefix: str = "") -> List[Tuple[str, float]]:
        """Get words in top-p nucleus given context. Returns (word, log_prob) pairs.

        Also caps at max_words to prevent flat distributions from including everything.
        If alpha_only=True, only include tokens starting with a letter.
        If prefix is set, it is prepended to the context string (e.g. an instruction).
        """
        # Build context string
        context_str = " ".join(context) if context else ""
        if prefix:
            context_str = prefix + context_str

        # Encode
        if context_str:
            input_ids = self.tokenizer.encode(context_str, return_tensors="pt").to(self.device)
        else:
            input_ids = torch.tensor([[self.tokenizer.bos_token_id or 50256]]).to(self.device)

        # Get next token probabilities
        with torch.no_grad():
            outputs = self.model(input_ids)
            logits = outputs.logits[0, -1, :]  # [vocab_size]
            probs = F.softmax(logits, dim=-1)
            log_probs = F.log_softmax(logits, dim=-1)

        # Sort by probability
        sorted_probs, sorted_indices = torch.sort(probs, descending=True)

        # Take smallest set with cumulative prob >= p, but cap at max_words
        cumulative = 0.0
        result = []
        for prob, idx in zip(sorted_probs, sorted_indices):
            token_id = idx.item()
            token = self.tokenizer.decode([token_id])

            # Skip empty/whitespace-only tokens
            if not token.strip():
                continue

            # Optional: filter to alphabetic tokens only
            if alpha_only and (not token.strip() or not token.strip()[0].isalpha()):
                continue

            log_prob = log_probs[token_id].item()
            result.append((token, log_prob))
            cumulative += prob.item()

            if cumulative >= p or len(result) >= max_words:
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
        """Get all words before this position in reading order."""
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
    lm: GPT2LM,
    n_rows: int = 4,
    n_cols: int = 4,
    p: float = 0.9,
    beam_width: int = 100,
    alpha_only: bool = False,
    prefix: str = "",
    verbose: bool = True
) -> List[Beam]:
    """
    Beam search using top-p sampling from GPT-2.

    Each word must be in the top-p nucleus for both:
    - Horizontal context (all previous words in reading order)
    - Column context (words above in same column)

    If prefix is set, it is prepended to every context before querying GPT-2.
    """
    if verbose:
        print(f"v3 Beam Search: {n_rows}x{n_cols}, p={p}, beam_width={beam_width}")
        if prefix:
            print(f"  Prefix: {prefix!r}")

    initial_grid = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    beams = [Beam(grid=initial_grid, score=0.0)]

    for row in range(n_rows):
        for col in range(n_cols):
            if verbose:
                print(f"  Cell ({row},{col}), {len(beams)} beams...")

            new_beams = []

            for beam in beams:
                h_context = beam.get_horizontal_context(row, col)
                c_context = beam.get_column_context(row, col)

                h_top_p = lm.get_top_p(h_context, p, alpha_only=alpha_only, prefix=prefix)
                c_top_p = lm.get_top_p(c_context, p, alpha_only=alpha_only, prefix=prefix)

                h_words = {w for w, _ in h_top_p}
                c_words = {w for w, _ in c_top_p}
                h_scores = {w: s for w, s in h_top_p}
                c_scores = {w: s for w, s in c_top_p}

                if row == 0:
                    # First row: no column context yet, just use horizontal
                    candidates = h_top_p
                else:
                    # Intersection of horizontal and column nuclei
                    intersection = h_words & c_words
                    if not intersection:
                        continue  # branch dies
                    # Score by min of both log-probs (bottleneck principle)
                    candidates = [(w, min(h_scores[w], c_scores[w])) for w in intersection]
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

        # Horizontal reading
        h_words = []
        for row in beam.grid:
            h_words.extend([w for w in row if w])
        print(f"\nHorizontal: {' '.join(h_words)}")

        # Columns
        print("\nColumns:")
        for c in range(n_cols):
            col_words = [beam.grid[r][c] for r in range(n_rows) if beam.grid[r][c]]
            print(f"  C{c+1}: {' '.join(col_words)}")


def main():
    parser = argparse.ArgumentParser(description="2D Writing System v3 (GPT-2)")
    parser.add_argument("--rows", type=int, default=4, help="Number of rows")
    parser.add_argument("--cols", type=int, default=4, help="Number of columns")
    parser.add_argument("--p", type=float, default=0.9, help="Top-p threshold (default: 0.9)")
    parser.add_argument("--beam", type=int, default=100, help="Beam width (default: 100)")
    parser.add_argument("--top", type=int, default=5, help="Results to show")
    parser.add_argument("--model", type=str, default="gpt2", help="GPT-2 model name")
    parser.add_argument("--alpha-only", action="store_true", help="Only allow alphabetic tokens (filter punctuation)")
    parser.add_argument("--prefix", type=str, default="", help="Instruction prefix prepended to context (e.g. 'Finish the story: ')")
    args = parser.parse_args()

    lm = GPT2LM(args.model)

    print(f"\n{'#'*60}")
    print(f"GRID: {args.rows} rows x {args.cols} columns")
    print('#'*60)

    beams = beam_search_v3(lm, n_rows=args.rows, n_cols=args.cols, p=args.p, beam_width=args.beam, alpha_only=args.alpha_only, prefix=args.prefix)
    display_results(beams, n=args.top)


if __name__ == "__main__":
    main()
