# Plan: 2D Writing v2

## Where v1 (`../2d-writing`) ended

Summary taken from v1's `NOTES.md`, `PLAN.md` and source headers. I have not
re-run the v1 code in this session.

- `grid2d.py`: beam search with summed row + column n-gram scores, and a
  variant with a fixed word category per column. Rows were sentences; columns
  were only word lists ("i we they you").
- `grid2d_v2.py`: beam search in diagonal order. An interior cell accepts only
  words in the intersection of the top-k continuations of its row and of its
  column. Trigram model on the Brown corpus. Best 4x4:

  ```
  but it is not
  it was the only
  is the way to
  not only to the
  ```

  The grid is symmetric (row i equals column i), and it is built from function
  words. 5x5 degenerates in the fifth row and column.
- GPT-2 as the scorer did worse than the n-gram model: poor sentence starters
  and locally plausible but ungrammatical phrases ("had be a good").
- `grid2d_v3.py`: GPT-2 with top-p sampling; rows wrap into one continuous
  passage, each column is an independent sentence. Its results are not
  recorded in v1's notes.

## Goal of v2 (set by the user, 2026-11-14)

Build the best system we can for generating good 2D writing.

My working definition of "good" (my choice, open to revision):

1. Every row and every column is a complete, natural English sentence.
   v1's lines were fragments ("is the way to").
2. The grid is not symmetric and repeats few or no words.
3. Content words appear, not only function words.
4. Larger grids are better, as long as 1-3 hold.
5. Read as a short text, the rows (and the columns) hang together.

## Approach

v1 generated word by word with a language model and hoped that lines came out
well formed. v2 turns this around.

1. Collect a large set of attested short sentences, with frequencies
   (Tatoeba, OpenSubtitles).
2. Search exactly for grids whose rows and columns all belong to the set.
   This is a word square problem with sentences in place of words and words in
   place of letters. Every line of every grid found is then a real sentence.
3. Rank the grids found: sentence frequency, word variety, and fluency and
   coherence under a neural language model.

## Tasks

- [x] Create project directory, README, PLAN
- [x] Decide goals
- [x] Sentence loader and normalizer (`sentences.py`)
- [x] Reference solver in Python (`search.py`)
- [x] Fast solver in C (`solver.c`, wrapper `grids.py`), tested against the
      reference (`test_solver.py`)
- [x] First results on Tatoeba (see `NOTES.md`)
- [x] Larger sentence set from OpenSubtitles (`extract_opensub.sh`,
      `build_sentence_sets.py`)
- [x] Exhaustive 4x4 with distinct words at count >= 20: 16,060 grids
- [x] Exhaustive 5x5 with distinct words at count >= 10: none exist
- [ ] Ranking of grids (`rank.py`, `lm.py`): fluency and coherence under a
      language model, number of uncommon words
- [ ] 5x5 on a larger sentence set (long run), or with a few repeated words
- [ ] Grids with more content words (cost budget in the solver)
- [ ] Rectangles
- [ ] Evaluation and report
