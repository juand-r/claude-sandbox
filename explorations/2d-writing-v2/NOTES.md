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
