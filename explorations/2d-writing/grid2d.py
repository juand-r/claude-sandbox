"""
2D Writing System - Generate word grids readable in both dimensions.

Each row and each column should form coherent English text.
Uses n-gram model built from Brown corpus (no network needed).
"""

import numpy as np
from collections import defaultdict
from typing import List, Tuple, Dict
import random
from dataclasses import dataclass
import time
import math
import nltk
from nltk.corpus import brown


# --- N-gram Language Model ---

class NgramLM:
    """Simple n-gram language model with Laplace smoothing."""

    def __init__(self, n: int = 3, vocab: List[str] = None):
        self.n = n
        self.vocab = set(vocab) if vocab else None
        self.ngram_counts = defaultdict(lambda: defaultdict(int))
        self.context_counts = defaultdict(int)
        self.unigram_counts = defaultdict(int)
        self.total_words = 0
        self.smoothing = 0.1  # Laplace smoothing parameter

    def train(self, sentences: List[List[str]]):
        """Train on list of tokenized sentences."""
        print(f"Training {self.n}-gram model...")

        for sent in sentences:
            # Filter to vocab if specified
            if self.vocab:
                sent = [w.lower() for w in sent if w.lower() in self.vocab]
            else:
                sent = [w.lower() for w in sent]

            if len(sent) < 2:
                continue

            # Add start tokens
            padded = ['<s>'] * (self.n - 1) + sent + ['</s>']

            for i in range(len(padded) - self.n + 1):
                context = tuple(padded[i:i + self.n - 1])
                word = padded[i + self.n - 1]

                self.ngram_counts[context][word] += 1
                self.context_counts[context] += 1

            for word in sent:
                self.unigram_counts[word] += 1
                self.total_words += 1

        print(f"  Trained on {self.total_words} words, {len(self.context_counts)} contexts")

    def log_prob(self, word: str, context: List[str]) -> float:
        """Log probability of word given context."""
        word = word.lower()
        context = tuple(w.lower() for w in context[-(self.n-1):])

        # Pad context if needed
        while len(context) < self.n - 1:
            context = ('<s>',) + context

        count = self.ngram_counts[context][word]
        total = self.context_counts[context]
        vocab_size = len(self.unigram_counts) + 1  # +1 for unknown

        # Laplace smoothing
        prob = (count + self.smoothing) / (total + self.smoothing * vocab_size)
        return math.log(prob + 1e-10)

    def score_sequence(self, words: List[str]) -> float:
        """Score a sequence of words (sum of log probs)."""
        if not words:
            return 0.0

        words = [w.lower() for w in words]
        padded = ['<s>'] * (self.n - 1) + words

        total = 0.0
        for i in range(self.n - 1, len(padded)):
            context = padded[i - self.n + 1:i]
            word = padded[i]
            total += self.log_prob(word, context)

        return total

    def get_next_word_probs(self, context: List[str], vocab: List[str]) -> Dict[str, float]:
        """Get log probabilities for each word in vocab given context."""
        return {word: self.log_prob(word, context) for word in vocab}


# --- Grid ---

@dataclass
class Grid:
    """A 2D grid of words."""
    words: List[List[str]]  # words[row][col]

    @property
    def rows(self) -> int:
        return len(self.words)

    @property
    def cols(self) -> int:
        return len(self.words[0]) if self.words else 0

    def get_row(self, i: int) -> List[str]:
        return self.words[i]

    def get_col(self, j: int) -> List[str]:
        return [self.words[i][j] for i in range(self.rows)]

    def copy(self) -> "Grid":
        return Grid([row.copy() for row in self.words])

    def __str__(self) -> str:
        widths = []
        for j in range(self.cols):
            col_width = max(len(self.words[i][j]) for i in range(self.rows))
            widths.append(col_width)

        lines = []
        for row in self.words:
            line = " ".join(word.ljust(widths[j]) for j, word in enumerate(row))
            lines.append(line)
        return "\n".join(lines)


def score_grid(grid: Grid, lm: NgramLM, repetition_penalty: float = 0.0) -> Tuple[float, List[float], List[float]]:
    """Score a grid. Returns (total_score, row_scores, col_scores).

    repetition_penalty: penalty per repeated word occurrence (beyond first).
    """
    row_scores = [lm.score_sequence(grid.get_row(i)) for i in range(grid.rows)]
    col_scores = [lm.score_sequence(grid.get_col(j)) for j in range(grid.cols)]
    total = sum(row_scores) + sum(col_scores)

    # Apply repetition penalty
    if repetition_penalty > 0:
        all_words = [w for row in grid.words for w in row]
        word_counts = defaultdict(int)
        for w in all_words:
            word_counts[w] += 1
        # Penalize each repetition beyond the first occurrence
        for word, count in word_counts.items():
            if count > 1:
                total -= repetition_penalty * (count - 1)

    return total, row_scores, col_scores


# --- Vocabulary ---

# Common English words for the grid
COMMON_WORDS = [
    # Determiners
    "the", "a", "an", "this", "that", "my", "your", "his", "her", "our",
    # Pronouns
    "i", "you", "he", "she", "it", "we", "they", "me", "him", "us",
    # Nouns - people
    "man", "woman", "child", "people", "friend", "mother", "father", "boy", "girl",
    # Nouns - things
    "time", "day", "night", "year", "life", "world", "way", "place", "thing",
    "house", "home", "room", "door", "water", "food", "book", "word", "name",
    "hand", "eye", "face", "head", "heart", "mind", "light",
    # Nouns - nature
    "sun", "moon", "sky", "sea", "tree", "bird", "dog", "cat",
    # Verbs - be/have/do
    "is", "are", "was", "were", "be", "been",
    "have", "has", "had", "do", "does", "did",
    # Verbs - modal
    "will", "would", "could", "should", "can", "may", "might", "must",
    # Verbs - common
    "go", "come", "see", "look", "know", "think", "make", "take",
    "get", "give", "find", "tell", "say", "ask", "want", "need",
    "feel", "seem", "leave", "keep", "let", "begin", "run",
    "stand", "sit", "hear", "read", "write", "love", "live",
    "walk", "move", "open", "close", "hold", "bring", "wait",
    # Past tense
    "went", "came", "saw", "knew", "thought", "made", "took", "found", "said",
    # Adjectives
    "good", "bad", "new", "old", "great", "small", "big", "long", "little",
    "young", "dark", "bright", "white", "black", "true", "real", "right",
    "first", "last", "own", "same", "other", "only",
    "cold", "warm", "soft", "hard", "deep", "strong", "happy", "sad",
    # Adverbs
    "now", "then", "here", "there", "always", "never", "often", "again",
    "very", "just", "also", "still", "well", "away", "back", "down", "up",
    # Prepositions
    "of", "to", "for", "with", "at", "by", "from", "into", "through",
    "about", "after", "before", "under", "over", "near",
    # Conjunctions
    "and", "but", "or", "so", "if", "when", "while", "because",
    # Other
    "not", "no", "yes", "all", "some", "many", "more", "most",
    "each", "every", "than", "as", "like", "what", "who", "how",
]


# --- Generation Approaches ---

def beam_search_grid(
    lm: NgramLM,
    vocab: List[str],
    n_rows: int = 5,
    n_cols: int = 5,
    beam_width: int = 100,
    verbose: bool = True
) -> Grid:
    """
    Beam search: fill grid cell by cell, keeping top-k candidates.
    Fill order: row by row, left to right.
    """
    if verbose:
        print(f"Beam search: {n_rows}x{n_cols}, beam_width={beam_width}")

    # (grid state, score)
    initial = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    beams = [(initial, 0.0)]

    total_cells = n_rows * n_cols

    for cell_idx in range(total_cells):
        row = cell_idx // n_cols
        col = cell_idx % n_cols

        if verbose and cell_idx % 5 == 0:
            print(f"  Cell ({row},{col}), {len(beams)} beams...")

        new_beams = []

        for grid_state, prev_score in beams:
            # Row context (words to left)
            row_context = [w for w in grid_state[row][:col] if w is not None]
            # Column context (words above)
            col_context = [grid_state[i][col] for i in range(row) if grid_state[i][col] is not None]

            row_probs = lm.get_next_word_probs(row_context, vocab)
            col_probs = lm.get_next_word_probs(col_context, vocab)

            for word in vocab:
                word_score = row_probs[word] + col_probs[word]
                new_score = prev_score + word_score

                new_grid = [r.copy() for r in grid_state]
                new_grid[row][col] = word
                new_beams.append((new_grid, new_score))

        # Keep top beam_width
        new_beams.sort(key=lambda x: x[1], reverse=True)
        beams = new_beams[:beam_width]

    best_grid_state, best_score = beams[0]
    result = Grid(best_grid_state)

    if verbose:
        print(f"  Best beam score: {best_score:.2f}")

    return result


def gibbs_sampling_grid(
    lm: NgramLM,
    vocab: List[str],
    n_rows: int = 5,
    n_cols: int = 5,
    n_iterations: int = 200,
    temperature: float = 1.0,
    verbose: bool = True
) -> Grid:
    """
    Gibbs sampling: start with random grid, iteratively resample each cell.
    """
    if verbose:
        print(f"Gibbs sampling: {n_rows}x{n_cols}, {n_iterations} iterations, temp={temperature}")

    # Initialize randomly
    grid = Grid([[random.choice(vocab) for _ in range(n_cols)] for _ in range(n_rows)])

    best_grid = grid.copy()
    best_score, _, _ = score_grid(grid, lm)

    if verbose:
        print(f"  Initial score: {best_score:.2f}")

    for iteration in range(n_iterations):
        # Sweep through all cells
        for row in range(n_rows):
            for col in range(n_cols):
                # Score each candidate
                scores = []
                for word in vocab:
                    old_word = grid.words[row][col]
                    grid.words[row][col] = word

                    row_score = lm.score_sequence(grid.get_row(row))
                    col_score = lm.score_sequence(grid.get_col(col))
                    scores.append((word, row_score + col_score))

                    grid.words[row][col] = old_word

                # Sample with temperature
                score_values = np.array([s for _, s in scores])
                score_values = score_values / temperature
                score_values = score_values - np.max(score_values)
                probs = np.exp(score_values)
                probs = probs / probs.sum()

                chosen_idx = np.random.choice(len(vocab), p=probs)
                grid.words[row][col] = scores[chosen_idx][0]

        current_score, _, _ = score_grid(grid, lm)
        if current_score > best_score:
            best_score = current_score
            best_grid = grid.copy()

        if verbose and (iteration + 1) % 20 == 0:
            print(f"  Iter {iteration + 1}: score={current_score:.2f}, best={best_score:.2f}")

    return best_grid


def constrained_beam_search(
    lm: NgramLM,
    n_rows: int = 5,
    n_cols: int = 5,
    beam_width: int = 50,
    unique_per_column: bool = False,
    structure: str = "dns",  # det-noun-verb-adj-noun vs pronoun-verb-adj-noun-adv
    verbose: bool = True
) -> Grid:
    """
    Beam search with grammatical constraints per column.

    Structures:
    - "dns": [Det] [Noun] [Verb] [Adj] [Noun]
    - "pvn": [Pronoun] [Verb] [Det] [Adj] [Noun]
    - "simple": [Subject] [Verb] [Object] [Prep] [Noun]

    If unique_per_column=True, each word in a column must be different.
    """
    DETS = ["the", "a", "my", "your", "his", "her", "this", "that", "our", "each", "every"]
    PRONOUNS = ["i", "you", "he", "she", "it", "we", "they"]
    NOUNS = ["man", "woman", "child", "dog", "cat", "bird", "sun", "moon",
             "day", "night", "life", "world", "time", "place", "house", "tree",
             "water", "light", "hand", "eye", "heart", "mind", "friend", "way",
             "book", "word", "name", "door", "room", "boy", "girl", "head", "face"]
    VERBS = ["is", "was", "has", "sees", "knows", "finds", "takes", "makes",
             "gives", "loves", "needs", "wants", "feels", "holds", "keeps",
             "brings", "leaves", "tells", "walks", "runs", "comes", "goes"]
    VERBS_TRANS = ["see", "know", "find", "take", "make", "give", "love", "need",
                   "want", "feel", "hold", "keep", "bring", "leave", "tell", "have"]
    ADJS = ["good", "bad", "old", "new", "great", "small", "big", "dark", "bright",
            "long", "deep", "strong", "soft", "warm", "cold", "true", "real",
            "first", "last", "young", "happy", "sad", "white", "black", "little"]
    PREPS = ["in", "at", "by", "for", "with", "to", "from", "on", "of", "about"]
    ADVS = ["now", "then", "here", "there", "always", "never", "well", "still", "just", "often"]

    if structure == "dns":
        col_vocab = [DETS, NOUNS, VERBS, ADJS, NOUNS]
        struct_name = "Det - Noun - Verb - Adj - Noun"
    elif structure == "pvn":
        # Use third-person singular verbs for better grammar variety
        VERBS_3RD = ["sees", "knows", "finds", "takes", "makes", "gives", "loves", "needs",
                     "wants", "feels", "holds", "keeps", "brings", "leaves", "tells", "has"]
        col_vocab = [PRONOUNS, VERBS_3RD, DETS, ADJS, NOUNS]
        struct_name = "Pronoun - Verb(3rd) - Det - Adj - Noun"
    elif structure == "pvn_base":
        col_vocab = [PRONOUNS, VERBS_TRANS, DETS, ADJS, NOUNS]
        struct_name = "Pronoun - Verb(base) - Det - Adj - Noun"
    elif structure == "pvn_agree":
        # Only use pronouns that agree with base verbs (I, you, we, they)
        PRONOUNS_PLURAL = ["i", "you", "we", "they"]
        col_vocab = [PRONOUNS_PLURAL, VERBS_TRANS, DETS, ADJS, NOUNS]
        struct_name = "Pronoun(plural) - Verb(base) - Det - Adj - Noun"
    elif structure == "pvn4":
        # 4-column structure: Pronoun - Verb - Det/Adj - Noun
        # For 4x4 grids with correct subject-verb agreement
        PRONOUNS_PLURAL = ["i", "you", "we", "they"]
        ADJ_DET = DETS + ADJS  # Mix determiners and adjectives
        col_vocab = [PRONOUNS_PLURAL, VERBS_TRANS, ADJ_DET, NOUNS]
        struct_name = "Pronoun - Verb - Det/Adj - Noun"
    elif structure == "nvpn":
        # Noun - Verb - Prep - Noun (e.g., "man walks to door")
        col_vocab = [NOUNS, VERBS, PREPS, NOUNS]
        struct_name = "Noun - Verb - Prep - Noun"
    elif structure == "poetry":
        # For more poetic/evocative output: Adj - Noun - Verb - Adv
        col_vocab = [ADJS, NOUNS, VERBS, ADVS]
        struct_name = "Adj - Noun - Verb - Adv"
    elif structure == "pvn3":
        # 3-column structure: Pronoun - Verb - Noun
        PRONOUNS_PLURAL = ["i", "you", "we", "they"]
        col_vocab = [PRONOUNS_PLURAL, VERBS_TRANS, NOUNS]
        struct_name = "Pronoun - Verb - Noun"
    elif structure == "pvn5":
        # 5-column structure with 5 agreeing subjects
        # Use "people", "children", "men", "women" + "friends" as plural nouns acting as subjects
        SUBJECTS_PLURAL = ["people", "children", "men", "women", "friends"]
        col_vocab = [SUBJECTS_PLURAL, VERBS_TRANS, DETS, ADJS, NOUNS]
        struct_name = "PluralSubject - Verb - Det - Adj - Noun"
    elif structure == "simple":
        col_vocab = [NOUNS, VERBS, NOUNS, PREPS, NOUNS]
        struct_name = "Noun - Verb - Noun - Prep - Noun"
    else:
        raise ValueError(f"Unknown structure: {structure}")

    # Backwards compatible: old code didn't have structure param
    # col_vocab = [DETS, NOUNS, VERBS, ADJS, NOUNS]

    if verbose:
        print(f"Constrained beam: {n_rows}x{n_cols}, unique_per_col={unique_per_column}")
        print(f"  Structure: {struct_name}")

    # Track used words per column: list of sets
    initial = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    initial_used = [set() for _ in range(n_cols)]
    beams = [(initial, initial_used, 0.0)]

    total_cells = n_rows * n_cols

    for cell_idx in range(total_cells):
        row = cell_idx // n_cols
        col = cell_idx % n_cols
        vocab = col_vocab[col]

        new_beams = []

        for grid_state, col_used, prev_score in beams:
            row_context = [w for w in grid_state[row][:col] if w is not None]
            col_context = [grid_state[i][col] for i in range(row) if grid_state[i][col] is not None]

            row_probs = lm.get_next_word_probs(row_context, vocab)
            col_probs = lm.get_next_word_probs(col_context, vocab)

            # Filter to available words if uniqueness required
            if unique_per_column:
                available = [w for w in vocab if w not in col_used[col]]
            else:
                available = vocab

            for word in available:
                word_score = row_probs[word] + col_probs[word]
                new_score = prev_score + word_score

                new_grid = [r.copy() for r in grid_state]
                new_grid[row][col] = word

                new_col_used = [s.copy() for s in col_used]
                new_col_used[col].add(word)

                new_beams.append((new_grid, new_col_used, new_score))

        new_beams.sort(key=lambda x: x[2], reverse=True)
        beams = new_beams[:beam_width]

    best_grid_state, _, best_score = beams[0]
    result = Grid(best_grid_state)

    if verbose:
        print(f"  Best beam score: {best_score:.2f}")

    return result


def unique_beam_search(
    lm: NgramLM,
    vocab: List[str],
    n_rows: int = 5,
    n_cols: int = 5,
    beam_width: int = 200,
    verbose: bool = True
) -> Grid:
    """
    Beam search where each word in the grid must be unique.
    This forces diversity and avoids degenerate solutions.
    """
    if verbose:
        print(f"Unique beam search: {n_rows}x{n_cols}, beam_width={beam_width}")

    # (grid state, used_words set, score)
    initial = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    beams = [(initial, set(), 0.0)]

    total_cells = n_rows * n_cols

    for cell_idx in range(total_cells):
        row = cell_idx // n_cols
        col = cell_idx % n_cols

        if verbose and cell_idx % 5 == 0:
            print(f"  Cell ({row},{col}), {len(beams)} beams...")

        new_beams = []

        for grid_state, used_words, prev_score in beams:
            row_context = [w for w in grid_state[row][:col] if w is not None]
            col_context = [grid_state[i][col] for i in range(row) if grid_state[i][col] is not None]

            row_probs = lm.get_next_word_probs(row_context, vocab)
            col_probs = lm.get_next_word_probs(col_context, vocab)

            # Only consider unused words
            available_words = [w for w in vocab if w not in used_words]

            for word in available_words:
                word_score = row_probs[word] + col_probs[word]
                new_score = prev_score + word_score

                new_grid = [r.copy() for r in grid_state]
                new_grid[row][col] = word
                new_used = used_words | {word}
                new_beams.append((new_grid, new_used, new_score))

        # Keep top beam_width
        new_beams.sort(key=lambda x: x[2], reverse=True)
        beams = new_beams[:beam_width]

        if not beams:
            print("  WARNING: No valid beams found!")
            break

    if beams:
        best_grid_state, _, best_score = beams[0]
        result = Grid(best_grid_state)
        if verbose:
            print(f"  Best beam score: {best_score:.2f}")
        return result
    else:
        # Fallback to random
        return Grid([[random.choice(vocab) for _ in range(n_cols)] for _ in range(n_rows)])


def iterative_refinement(
    lm: NgramLM,
    vocab: List[str],
    n_rows: int = 5,
    n_cols: int = 5,
    n_iterations: int = 100,
    verbose: bool = True
) -> Grid:
    """
    Start with greedy row-wise generation, then hill-climb to improve columns.
    """
    if verbose:
        print(f"Iterative refinement: {n_rows}x{n_cols}")

    # Phase 1: Generate rows greedily
    if verbose:
        print("  Phase 1: Greedy row generation...")

    rows = []
    for r in range(n_rows):
        row = []
        for c in range(n_cols):
            probs = lm.get_next_word_probs(row, vocab)
            best_word = max(probs.keys(), key=lambda w: probs[w])
            row.append(best_word)
        rows.append(row)

    grid = Grid(rows)

    if verbose:
        print("  Initial (row-optimized):")
        print(grid)
        score, rs, cs = score_grid(grid, lm)
        print(f"  Score: {score:.2f} (rows: {sum(rs):.2f}, cols: {sum(cs):.2f})")

    # Phase 2: Hill climbing
    if verbose:
        print("  Phase 2: Hill climbing...")

    best_grid = grid.copy()
    best_score, _, _ = score_grid(grid, lm)

    for iteration in range(n_iterations):
        improved = False

        for row in range(n_rows):
            for col in range(n_cols):
                current_word = grid.words[row][col]
                current_score, _, _ = score_grid(grid, lm)

                best_replacement = current_word
                best_replacement_score = current_score

                for word in vocab:
                    if word == current_word:
                        continue
                    grid.words[row][col] = word
                    new_score, _, _ = score_grid(grid, lm)
                    if new_score > best_replacement_score:
                        best_replacement = word
                        best_replacement_score = new_score

                grid.words[row][col] = best_replacement
                if best_replacement != current_word:
                    improved = True

        current_score, _, _ = score_grid(grid, lm)
        if current_score > best_score:
            best_score = current_score
            best_grid = grid.copy()

        if verbose and (iteration + 1) % 20 == 0:
            print(f"  Iter {iteration + 1}: score={current_score:.2f}")

        if not improved:
            if verbose:
                print(f"  Converged at iteration {iteration + 1}")
            break

    return best_grid


# --- Main ---

def run_experiment(approach: str, lm: NgramLM, **kwargs) -> Tuple[Grid, float]:
    """Run an experiment with the given approach."""
    print(f"\n{'='*60}")
    print(f"APPROACH: {approach}")
    print('='*60)

    start_time = time.time()

    if approach == "beam":
        grid = beam_search_grid(lm, COMMON_WORDS, **kwargs)
    elif approach == "gibbs":
        grid = gibbs_sampling_grid(lm, COMMON_WORDS, **kwargs)
    elif approach == "constrained":
        grid = constrained_beam_search(lm, **kwargs)
    elif approach == "iterative":
        grid = iterative_refinement(lm, COMMON_WORDS, **kwargs)
    elif approach == "unique":
        grid = unique_beam_search(lm, COMMON_WORDS, **kwargs)
    else:
        raise ValueError(f"Unknown approach: {approach}")

    elapsed = time.time() - start_time

    print(f"\nResult ({elapsed:.1f}s):")
    print(grid)
    print()

    total, row_scores, col_scores = score_grid(grid, lm)
    print(f"Total score: {total:.2f}")
    print(f"Row scores: {[f'{s:.1f}' for s in row_scores]}")
    print(f"Col scores: {[f'{s:.1f}' for s in col_scores]}")

    print("\nRows as sentences:")
    for i in range(grid.rows):
        print(f"  R{i+1}: {' '.join(grid.get_row(i))}")

    print("\nColumns as sentences:")
    for j in range(grid.cols):
        print(f"  C{j+1}: {' '.join(grid.get_col(j))}")

    return grid, total


def main():
    # Load Brown corpus and train n-gram model
    print("Loading Brown corpus...")
    nltk.download('brown', quiet=True)
    sentences = brown.sents()
    print(f"  {len(sentences)} sentences")

    # Train trigram model
    lm = NgramLM(n=3, vocab=COMMON_WORDS)
    lm.train(sentences)

    results = {}

    # Best 4x4 approach (proven to work)
    results["4x4_pvn4"] = run_experiment("constrained", lm, beam_width=200,
                                         n_rows=4, n_cols=4,
                                         unique_per_column=True, structure="pvn4")

    # Try 3x3 for comparison
    results["3x3_pvn3"] = run_experiment("constrained", lm, beam_width=200,
                                         n_rows=3, n_cols=3,
                                         unique_per_column=True, structure="pvn3")

    # Try 5x5 with plural subjects
    results["5x5_pvn5"] = run_experiment("constrained", lm, beam_width=200,
                                         n_rows=5, n_cols=5,
                                         unique_per_column=True, structure="pvn5")

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    for name, (grid, score) in results.items():
        print(f"\n{name}:")
        print(grid)
        print(f"Score: {score:.2f}")


if __name__ == "__main__":
    main()
