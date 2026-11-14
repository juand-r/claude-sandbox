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
