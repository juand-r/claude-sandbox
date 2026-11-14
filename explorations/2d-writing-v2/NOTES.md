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

Cost projection: from k = 20 (2.0e9 nodes, 227k sentences) to this run
(3.6e10 nodes, 529k sentences) the growth exponent is about 3.4 (the two runs
differ slightly in constraints). At that rate the same run at k = 5 (1.45
million sentences) would need about 1e12 nodes, around a day on 4 cores.
Extrapolation, not measured. (An earlier version of this note used an
exponent of 2.8, which was too low.)

## 2026-11-14: block cell order (negative result)

`solver.c` can fill cells by growing a top-left square block (2x2, 3x3, ...)
instead of row by row (optional last argument). I expected it to fail
earlier, since rows and columns get constrained evenly. It returns the same
grids but visits more nodes:

| grid, k | row by row | block |
|---|---|---|
| 4x4, k = 30 | 2.9e8 nodes | 5.4e8 |
| 5x5, k = 30 | 4.0e7 | 1.2e8 |
| 5x5, k = 20 | 3.3e8 | 1.3e9 |

Row by row stays the default.

## 2026-11-14: a 5x5 grid

Run: `run_exhaustive.py --rows 5 --cols 5 --min-count 10 --max-repeats 3
--no-names` (512,942 sentences, at most 3 cells may repeat a word). 7.4e10
nodes, 12,566 CPU seconds (about 52 minutes on 4 cores, shared with another
job), exhaustive. Result: one grid and its transpose.

```
and     what    did     i       get
where   have    you     put     him
do      you     want    them    back
you     brought her     in      here
go      back    to      bed     now
```

Down: "and where do you go", "what have you brought back", "did you want her
to", "i put them in bed", "get him back here now". All ten lines occur at
least 10 times in the corpus. "you" appears three times and "back" twice, so
22 of the 25 words are distinct.

## 2026-11-14: rectangles

All runs: no names, all words distinct, exhaustive, `run_exhaustive.py`.
"rows x cols": a 3x5 grid has 3 rows of 5 words and 5 columns of 3 words.

| grid | k | row sentences | column sentences | grids | nodes | CPU s |
|---|---|---|---|---|---|---|
| 3x5 | 20 | 168,181 | 166,688 | 14,908 | 4.7e8 | 104 |
| 3x6 | 10 | 413,854 | 361,547 | 1,096 | 3.4e9 | 928 |
| 4x5 | 10 | 512,942 | 528,874 | 752 | 1.8e10 | 4,199 |
| 3x7 | 10 | 310,584 | 361,547 | 0 | 1.4e9 | 486 |
| 4x6 | 10 | 413,854 | 528,874 | 0 | 4.2e9 | 1,260 |
| 3x5 | rows 10, columns 100 | 512,942 | 30,399 | 873 | 2.2e8 | 72 |
| 3x6 | rows 5, columns 100 | 1,267,371 | 30,399 | 4 | 5.6e8 | 178 |
 Earlier quick tests with names allowed: at k = 20 there are 5
grids for 3x6, 4 for 4x5, none for 3x7 and 4x6.

3x5 at k = 20: scored the 2,278 grids with at least 2 uncommon words
(`data/feat_3x5_k20.pkl`). Top grid:

```
because he      didn't  do      it
i       can     have    you     killed
don't   try     to      follow  me
```

Down: "Because I don't. He can try. Didn't have to. Do you follow? It killed
me."

3x6 at k = 10 (`data/feat_3x6_k10.pkl`): rows are good, but many 3-word
columns are fragments rather than sentences ("we have me", "that be me",
"here right there"). Three-word subtitle lines with count 10 are often pieces
of longer utterances. The sentence filter (capital first letter, final
mark) does not catch this. A higher count threshold for short lines would
help; not done yet.

## 2026-11-14: v1 grids under the same measures

Fluency (mean log-probability per token of each line written as a sentence,
SmolLM2-360M):

- v1 intersection grid ("but it is not / it was the only / is the way to /
  not only to the"): -5.02. One of its 4 distinct lines occurs as a sentence
  in the corpus with count >= 3 ("but it is not", 76).
- v1 category grid ("i know a man / we have the world / ..."): rows -4.58,
  columns -8.20. Two of 4 rows are attested, no column is.
- v2 4x4 grids: median -4.61 (k = 20 set), best -3.73; every line attested
  by construction.

Fluency alone does not separate the v1 intersection grid from the lower half
of the v2 grids: a fragment such as "it was the only" is locally very
probable. The difference that matters is that v2 lines are complete
sentences, which the language model score does not measure well.

## 2026-11-14: stricter threshold for short columns

`run_exhaustive.py --min-count-cols` sets a separate count threshold for the
column sentences. With columns at k = 100 the 3-word fragments mostly
disappear. The four 3x6 grids (rows k = 5) are clean, for example
"yeah well i think you're right / we are just about here now / can you do
that again please" with columns "yeah we can", "well are you", "i just do",
"think about that", "you're here again", "right now please".

4x5 at k = 10 (`data/feat_4x5_k10.pkl`, 752 grids): top grids are as good as
the 4x4 ones, e.g. "why don't we all go / do you have the right / i know
another way in / try that one over there", down: "Why do I try? Don't you
know that? We have another one. All the way over. Go right in there."

## 2026-11-14: long 4x4 run at k = 7

Started `run_exhaustive.py --rows 4 --cols 4 --min-count 7 --min-uncommon 5
--n-common 300 --no-names --parts 240` (832,981 sentences). After 5 parts:
3.5e9 nodes, 4 grids. At that rate the whole run needs about 1.7e11 nodes,
4 to 5 hours on 4 cores.

Finished 09:23 UTC, 2 h 18 min wall, 32,523 CPU s, 1.40e11 nodes, all 240
parts exhaustive. 530 grids (265 after removing transposes). Verified with
`verify_grids.py` (1,215 distinct sentences, all count >= 7). Scored to
`data/feat_4x4_k7_u5.pkl`. Uncommon words (top 200): 5: 205 grids, 6: 37,
7: 23. Only 12 grids have all lines with count >= 10. Median fluency -4.96.
Cost exponent from the k = 10 run: ln(1.40e11/3.6e10)/ln(832981/528874) = 3.0
(the floors on uncommon words differ: 4 vs 5).

Top grids are the most varied so far: "oh but i couldn't / no it cannot be /
you can't trust anyone / don't hurt anybody else"; "here's what we found /
where exactly were you / it was quite easy / is that close enough". Some
k = 7 lines are poor ("me working hard enough", "welcome to soon enough").

## 2026-11-14: lines as sequences of sentences (user request)

User request: allow punctuation, so that a line can hold several sentences,
and grow a grid step by step to be as large as possible.

Definition used: a line (row or column) is valid if it can be cut into
consecutive attested sentences. Cuts of different lines are independent. All
words of the grid are still distinct.

Code: `extend.c` (solver; keeps for every line the set of trie nodes reachable
under any cutting), `multi.py` (front end, independent check, display
cutting), `grow.py` (growth loop), `test_extend.py` (solver against brute
force on 40 small cases, including seeded extension and the sentence filter).

Findings so far:

- With 2-word sentences at count >= 200 the 4x4 seed extends to 6x6 in
  seconds, but the new cells are fragments ("because what", "man up down
  there"). Dropped 2-word sentences for the first level.
- Adding 3 full rows by filling cells row by row did not finish in 12 CPU
  minutes per process. Fix: transpose, add columns, transpose back, so the
  new block is always filled along its short side. 4x7 -> 7x7 then takes
  about 80 s.
- Run 1 (3-word count >= 50, longer >= 10) stopped at 7x10 with a budget of
  2e7 nodes per process. Cause: all words must be new, and the grid has used
  up the common words. Most sentences contain a used word and are dead.
- Fix: before each step remove the sentences that cannot occur any more
  (`multi.usable_sentences`; exactness tested). At 10x10 only 58,213 of
  1,794,185 sentences remain usable. Steps now take seconds to minutes and
  an exhaustive search of a step is feasible.
- Run 2 (`data/grow/run2.json`, seed "oh but i couldn't / ...", profanity
  list `banned_words.txt` removed from the sentence set): 4x4 -> 4x7 -> 7x7
  -> 7x10 -> 10x10 in about 3 minutes. At 10x10 the exhaustive search proved
  that no 3, 4 or 5 columns and no 3, 4 or 5 rows can be added (steps of 6
  and 7 were not tried). So this grid is maximal for this sentence set and
  these steps. Fluency -4.48.
- The new block of a step hardly interacts with the old grid: old lines are
  complete sentences, so a new sentence usually starts at the old edge. The
  only coupling is that words must be new. Growth is therefore limited by
  the supply of words, not by the fit of sentences.
- Added levels to `grow.py`: when no step works, rarer sentences (and
  frequent 2-word ones) are admitted. Run 3 uses the default four levels.

## 2026-11-14: change of direction (user): language model with beam search

User feedback: the sentence lookup is not what was wanted. Wanted: build the
grid incrementally with a language model and beam search. Further decisions
by the user: repeats allowed but limited; no word equal to its mirror cell;
a word at most twice per row or column; punctuation is to be a token in a
cell (off for now); lines must be fluent but need not end a sentence; next
step is wrap-around (row 2 continues row 1, same for columns).

Lookup experiments under the new repeat rules, before the change: 5x5 at
count >= 20 with unlimited repeats and no mirrored words gives 180 grids, all
degenerate (identical rows, columns like "come come come come come"). With
"at most 2 per line" added: 0 grids at count >= 20. The count >= 10 run was
stopped. The grown 10x10 and 13x13 grids (lines cut into several sentences)
used a reading of "punctuation" that the user did not intend.

`lmgrid.py`: cells filled row by row; candidate score = log P(word | row so
far) + log P(word | column so far) under SmolLM2-360M, renormalized over
13,487 single-token lowercase words; beam search.

- Without a prefix the model reads a lowercase start as code ("void main
  function void function"). A one-line prefix saying the text is lowercase
  prose fixes that.
- Without a cost on repeats one word floods the grid ("function" 6 times in
  5x5). Added 2 nats per earlier use of a word.
- 5x5, beam 16: 28 s. "and then there is the / so he was a man / it took a
  lot of / was the time of the / that two in one house"; down "and so it was
  that / then he took the two / there was a time in / is a lot of one / the
  man of the house".
- 8x8, beam 32, no wrap: 167 s, -3.71 nats per word and direction
  (`data/lm/8x8.json`). Rows such as "the idea had been floating around in
  my", columns such as "then the world was made to my will".
- 8x8 with wrap, first try: degenerate. Each row was the previous row
  shifted by one word ("on to the end of it all" repeated), which makes
  copying cheap in both directions. Fix: no three-word sequence may occur
  twice, along rows or down columns.
- 6x6 with wrap and that rule: 235 s (`data/lm/6x6_wrap.json`). Rows read as
  one text: "and so on for the rest of it until the next of course is the
  last one in there at end time and that is all of it then you just put that
  in there to". Columns: "and of course there is just so it is at all put on
  until the end of that for the last time it in the next one and then there
  rest of in that you to". The column text weakens toward the end.
- Observation: the grids consist almost only of function words. A word must
  be likely in two contexts at once, which favors generic words.

Row-only wrap (`--wrap rows`; user request after seeing that wrap in both
directions was not fluent). Rows form one text, each column stands alone.
Cells are filled row by row, so the row context always consists of complete
earlier rows. Beam 32, top 30.

- 6x6: 122 s, -3.39 (`data/lm/6x6_wraprows.json`). Rows: "and so on to the
  end of it all the time of course is the place for this in a world where
  everything is a question and there is a lot that we are not very". Columns:
  "and of course in a lot", "so it is a question that", "on all the world and
  we", "to the place where there are", "the time for everything is not",
  "end of this is a very".
- 8x8: 275 s, -3.58 (`data/lm/8x8_wraprows.json`). Rows: "and so on for a
  while and then there is this one line in it that is the very last of its
  kind in the whole day time long history of the text world as we know it
  goes back to when we have not had something of which you are to be made
  like me you can now say but no this was". Weak spots: "day time long
  history", column "a line of long know not be but".
