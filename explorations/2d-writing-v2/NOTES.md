# Notes

Chronological log of findings. Newest at the bottom.

## 2026-11-14: Tatoeba, exact search

Data: Tatoeba English sentences export (2,040,567 lines), downloaded from
https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences.tsv.bz2.
After normalization (lowercase, punctuation removed, sentences with digits or
other symbols dropped) there are 203,931 distinct 4-word sentences and 297,941
distinct 5-word sentences.

Exhaustive search with the C solver, requiring all words in the grid to be
distinct:

- 3x3: thousands of grids, found in seconds.
- 4x4: exactly 2 grids, which are transposes of each other (18 s):

  ```
  what  would you   take
  did   tom   see   this
  i     like  that  stuff
  do    it    right away
  ```

  Columns: "what did i do", "would tom like it", "you see that right",
  "take this stuff away".
- 5x5: none (27 s).

If repeated words are allowed, 4x4 grids are plentiful, but most of the ones
sampled were symmetric (2336 of 3437 in a random sample).

Conclusion: the method works, and the sentence set is the limiting factor.

## 2026-11-14: OpenSubtitles sentence set

Data: OpenSubtitles 2018 English monolingual file (3.66 GB gzip),
https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2018/mono/en.txt.gz.
`extract_opensub.sh` keeps lines that start with a capital, contain only
letters, apostrophes, spaces and commas, end in `.`, `?` or `!`, and have 2 to
7 words. This gives 33,960,086 distinct (sentence, final mark) pairs.
`build_sentence_sets.py` sums counts over the final mark and keeps sentences
with total count >= 3. Number of distinct sentences by length:

| words | count >= 3 | >= 5 | >= 10 | >= 20 | >= 50 |
|---|---|---|---|---|---|
| 4 | 2,457,411 | 1,446,729 | 596,094 | 227,462 | 63,499 |
| 5 | 2,872,208 | 1,593,694 | 572,554 | 181,461 | 37,650 |

Caveat: subtitle lines are sometimes fragments of a longer sentence ("better
than a good cop"), and the corpus contains duplicate subtitle files, so a low
count is weak evidence that a line is a natural sentence.

## 2026-11-14: exhaustive search, all words distinct

"k" below is the minimum corpus count of the sentences used. All runs used
`solver.c` (row-major fill with tries) and ran to completion, so the counts
are exact for the given sentence set.

| grid | k | sentences | grids found | search nodes | time |
|---|---|---|---|---|---|
| 4x4 | 50 | 63,499 | 6 | 3.5e7 | 5 s, 1 core |
| 4x4 | 20 | 227,462 | 16,060 | 2.0e9 | 291 s, 1 core |
| 5x5 | 30 | 87,257 | 0 | 4.0e7 | 2 s, 4 cores |
| 5x5 | 10 | 572,554 | 0 | 1.7e10 | 1194 s, 3 cores |

Grid counts include transposes (a grid and its transpose both count).

Example 4x4 (k = 20):

```
no     he     can't  come
you    may    go     home
should be     back   soon
stay   right  there  please
```

Columns: "no you should stay", "he may be right", "can't go back there",
"come home soon please".

5x5 with 25 distinct words: none exists among sentences with count >= 10. In
that run the search reached the last row only 1277 times. Search cost grows
roughly as (number of sentences)^3.2 (from the k = 30 and k = 10 rows), which
puts k = 5 at about 4.5e11 nodes, around 9 hours on 3 cores. This is an
extrapolation from two points.

## 2026-11-14: search variants that did not help

- Random candidate order without restarts: the search never leaves the
  subtree of its first row. Found no 5x5 in 2e9 nodes.
- Guided random order (prefer words with many completions) with restarts
  (`solver.c`, `temp`, `restart_nodes`): no 5x5 with distinct words in about
  1e9 nodes over several settings at k = 5 and k = 3. With repeats allowed it
  finds 5x5 grids quickly, but they reuse "i", "don't", "you" heavily.
- Positional consistency filter (drop a sentence from line i if one of its
  words cannot occur in the crossing line at that position, iterate to a fixed
  point): removes only 15 to 30 percent of sentences per line position.
- `fill.c`, a crossword-style solver that always fills the row or column with
  the fewest candidates: 4 times fewer nodes than `solver.c` on 4x4 (k = 50)
  and 5x5 (k = 30), but each node is far more expensive (it scans posting
  lists to count candidates), about 25 times slower overall. Kept for
  reference and as an independent check; both solvers return identical grids
  on the test inputs. (Timing was taken while another job used a core, so the
  factor is rough.)

## 2026-11-14: ranking 4x4 grids with a language model

`score_grids.py` computes the features in `rank.py` for each grid, using
SmolLM2-360M on CPU (`lm.py`). On one core, with other jobs running, it scores
about 250 4x4 grids per minute. The model must be loaded in float32; the
default bfloat16 load gave scores that changed by 0.15 nats with batch
padding.

Observations on the 8,030 distinct 4x4 grids at k = 20 (16,060 counting
transposes):

- "Uncommon" words (outside the 200 most frequent) are scarce. Number of
  grids by count of uncommon words: 0: 4265, 1: 2907, 2: 766, 3: 91, 4: 1.
- Coherence (PMI between lines) alone favours grids with unlikely sentences,
  because an unlikely sentence gains more from any context. Fluency alone
  favours bland grids. The sum of their z-scores, plus half the z-score of
  the number of uncommon words, gives a top list that I judge good by
  reading. The weights are a judgment call (`rank.WEIGHTS`).
- The top of the list is dominated by families of grids that differ in one
  or two words, so `gallery.py` skips a grid that shares more than half its
  words with one already shown.

Top of the list (`gallery.py data/feat_4x4_k20.pkl`):

```
oh       and      you      don't          yeah   but    you    can't
no       it       couldn't be             well   it     might  be
she      didn't   do       this           i      didn't say    that
doesn't  work     that     way            don't  work   so     hard
```

Down, left grid: "Oh no she doesn't. And it didn't work. You couldn't do
that. Don't be this way." Down, right grid: "Yeah well I don't. But it didn't
work. You might say so. Can't be that hard."

## 2026-11-14: attempts to get more content words

- Sentences with at most 2 common words (top 200), k = 5: 744,703 sentences.
  No 4x4 grid found in 2e9 nodes (search not completed).
- Every line must have at least one uncommon word (top 200):
  k = 20: 188,583 sentences, 0 grids (exhaustive). So every one of the 16,060
  grids at k = 20 has a line made only of common words.
  k = 10: 528,702 sentences, 368 grids (exhaustive, 8.5 min on 4 cores). The
  "uncommon" words are mostly words like "uh", "told", "brought"; the grids
  are not more interesting.
- N-gram generalization (`ngram.c`, `ngrams.py`): accept a 4-word line if its
  first 3 words begin an attested sentence and its last 3 words end one. This
  admits about 296 million 4-word lines (2.5 million are attested). Grids with
  10 or more uncommon words are then easy to find, but most contain lines
  that are not sentences ("you of the day", "to not be now"). Raising the
  n-gram count threshold from 5 to 20 did not fix this. The rule is too
  loose: the first and last word of a line never have to fit each other.
  The solver is tested against brute force (`test_ngram.py`) and kept, but
  its output is not used in the results.

## 2026-11-14: 5x5 status

The exhaustive run at k = 5 (1,593,694 sentences, all words distinct) was
stopped after 30 of 600 parts (3.1e10 nodes, about 2 CPU hours): no grid
found, 25,483 search nodes in the last row. Finished parts are kept in
`data/runs/5x5_k5_rep0/` (old runner format).

## 2026-11-14: 4x4 on the larger set with a floor on uncommon words

Run: `run_exhaustive.py --rows 4 --cols 4 --min-count 10 --min-uncommon 4
--n-common 300 --no-names` (sentences seen 10 or more times, no names, 16
distinct words, at least 4 words outside the 300 most frequent). 528,874
sentences, 3.6e10 nodes, 28 minutes on 4 cores, exhaustive: 730 grids (365 up
to transpose).

After scoring (`data/feat_4x4_k10_u4.pkl`), these read better than the k = 20
list. Examples from the top 10:

```
but      he       never    did            which  i      don't  get
i        wouldn't forget   you            we     won't  lose   them
didn't   have     a        name           can't  see    your   legs
dare     to       face     him            do     you    mind   moving
```

Down, left: "But I didn't dare. He wouldn't have to. Never forget a face. Did
you name him?" Down, right: "Which we can't do. I won't see you. Don't lose
your mind. Get them legs moving!"

Lower bound on remaining cost in `solver.c` (sum over columns of the cheapest
completion): identical results, 17 percent fewer nodes on a test run (4x4,
k = 30, at least 3 uncommon words). Small gain, because almost every column
prefix has some completion made of uncommon words.

Cost projection: nodes grow about as (number of sentences)^2.8, so the same
run at k = 5 (1.45 million sentences) would need about 6e11 nodes, around 8
hours on 4 cores. Extrapolation, not measured.
