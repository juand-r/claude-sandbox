# Two-dimensional writing from real sentences

Report for `explorations/2d-writing-v2`, 14 November 2026.

## 1. Summary

A piece of 2D writing is a grid of words that reads as English along every row
and down every column. The earlier project (`explorations/2d-writing`) built
such grids word by word with a language model. Its best 4x4 grid had lines
like "is the way to": locally probable, but not sentences.

This project does it differently. We take a large set of short sentences that
real people wrote, and search exactly for grids in which every row and every
column is one of those sentences. The grids are then ranked with a small
language model.

The main result: grids in which every line is a complete, attested sentence
exist in large numbers at 4x4, and can be found exhaustively. An example with
16 distinct words:

```
but      he       never    did
i        wouldn't forget   you
didn't   have     a        name
dare     to       face     him
```

Across: "But he never did. I wouldn't forget you. Didn't have a name. Dare to
face him." Down: "But I didn't dare. He wouldn't have to. Never forget a
face. Did you name him?" Each of these eight sentences occurs at least 10
times in the OpenSubtitles corpus.

Three further findings:

- Size has a sharp limit. With all words distinct, no 5x5 grid exists among
  the 572,554 five-word sentences seen 10 or more times. Allowing three
  repeated words, exactly one 5x5 grid exists (Section 5.2).
- The grids are built almost entirely from very common words. Attempts to
  force more content words either found nothing or gave up sentence quality
  (Section 6).
- Search cost grows a little faster than the cube of the number of sentences
  (measured exponents 3.2 to 3.4), and none of three alternative search
  strategies reduced it (Section 7).

## 2. What counts as good 2D writing

The user's goal was "the best possible system for generating good 2D
writing". The criteria below are my working definition; they were not given.

1. Every row and every column is a complete, natural English sentence.
2. The grid is not symmetric, and repeats few or no words. A symmetric grid
   (row i equals column i) says each thing twice, and repeated words make the
   problem easy in an uninteresting way.
3. Content words appear, not only function words.
4. Larger grids are better, if 1 to 3 hold.
5. Read as a short text, the rows hang together, and so do the columns.

Criterion 1 is enforced by construction. Criterion 2 is a hard constraint in
the search (all words distinct, unless stated). Criteria 3 and 5 are handled
by ranking. Criterion 4 is explored by running the search at different
shapes.

## 3. Method

### 3.1 Sentence set

Source: the OpenSubtitles 2018 English monolingual file (film and television
subtitles, 3.66 GB compressed). A line is kept if it starts with a capital
letter, contains only letters, apostrophes, spaces and commas, ends in a
period, question mark or exclamation mark, and has 2 to 7 words. Sentences
are lowercased and stripped of punctuation, and identical ones are counted.

This yields 33,960,086 distinct (sentence, final mark) pairs. The count of a
sentence is the number of subtitle lines equal to it. Throughout this report
"k" is the minimum count required of the sentences used in a run. Table 1
gives the set sizes.

Table 1. Distinct sentences by length and minimum count k.

| words | k = 3 | k = 5 | k = 10 | k = 20 | k = 50 |
|---|---|---|---|---|---|
| 4 | 2,457,411 | 1,446,729 | 596,094 | 227,462 | 63,499 |
| 5 | 2,872,208 | 1,593,694 | 572,554 | 181,461 | 37,650 |

Most runs also drop sentences containing a name. A word counts as a name if
it is capitalized in more than 80 percent of its non-initial occurrences in
the first 30 million corpus lines ("I" and its contractions excepted). Names
are excluded because a vocative fits almost anywhere ("..., Tom") and makes
grids cheap.

Two caveats about this set. First, a subtitle line is sometimes a fragment of
a longer utterance ("better than a good cop"). The filter does not detect
this, and it matters most for 3-word lines (Section 5.3). Second, the corpus
contains duplicate subtitle files, so a small count is weak evidence that
many people said the sentence. An earlier, smaller experiment with the
Tatoeba sentence collection (203,931 four-word sentences) found exactly one
4x4 grid with distinct words, so the size of the subtitle corpus is what makes
the method productive.

### 3.2 Exact search

The problem is a word square with sentences in place of words and words in
place of letters. `solver.c` stores the row sentences and the column
sentences as tries and fills the grid cell by cell, row by row. At each cell
the candidates are the words that continue both the current row prefix and
the current column prefix. The search backtracks when a cell has no
candidate.

Two budgets prune the search and shape the output: the number of cells that
may repeat a word already used (zero unless stated), and a floor on the
number of "uncommon" words in the grid, defined as words outside the N most
frequent (N = 200 or 300, stated per run).

Runs are split into independent parts by a hash of the first two words, run
on 4 cores, and can be resumed (`run_exhaustive.py`). All runs reported as
exhaustive completed every part, so their grid counts are exact for the given
sentence set and constraints.

The solver is checked in three ways. It agrees with a slow reference solver
in Python on random inputs (`test_solver.py`). A second C solver with a
different algorithm (`fill.c`) returns identical grids on the same inputs.
And `verify_grids.py` rereads the sentence files and confirms, for every grid
reported here, that each row and column is present with the required count.

### 3.3 Ranking

A search returns hundreds to thousands of grids, many of them near copies of
each other. `rank.py` computes three features per grid with SmolLM2-360M, a
small causal language model run on CPU:

- Fluency: mean log-probability per token of the row and column sentences,
  each scored alone.
- Coherence: for the rows read as one passage, the log-probability of the
  passage minus the sum of the log-probabilities of its sentences; the same
  for the columns; the two are summed and divided by the number of lines.
  This is the pointwise mutual information between the lines. It is positive
  when the sentences fit together better than unrelated sentences would.
- Uncommon words: the number of cells holding a word outside the 200 most
  frequent.

The combined score is z(fluency) + z(coherence) + 0.5 z(uncommon words),
where z standardizes a feature within the set being ranked. The weights are
my judgment from reading the top of the 4x4 list under a few settings; they
are not fitted to anything. Two observations motivated the sum. Coherence
alone prefers grids made of unlikely sentences, because an unlikely sentence
gains more from any context. Fluency alone prefers bland grids.

The gallery then walks down the ranked list and skips any grid that shares
more than half of its words with a grid already shown. Without this step the
top ten is one grid with single-word variations.

## 4. Results at 4x4

### 4.1 How many grids exist

Table 2. Exhaustive 4x4 searches, all 16 words distinct. Grid counts include
transposes, so the number of distinct pieces is half.

| sentences used | constraint | sentences | grids | search nodes | time |
|---|---|---|---|---|---|
| k = 50 | none | 63,499 | 6 | 3.5e7 | 5 s, 1 core |
| k = 20 | none | 227,462 | 16,060 | 2.0e9 | 291 s, 1 core |
| k = 10, no names | at least 4 uncommon words (top 300) | 528,874 | 730 | 3.6e10 | 28 min, 4 cores |
| k = 7, no names | at least 5 uncommon words (top 300) | 832,981 | 530 | 1.4e11 | 2 h 18 min, 4 cores |

Observation: between k = 50 and k = 20 the sentence set grows 3.6 times and
the number of grids grows about 2,700 times. A grid needs eight sentences to
fit together, so the count is very sensitive to the size of the set.

### 4.2 What the best grids look like

The four top-ranked grids of the k = 10 run, after removal of near
duplicates. Sentences are shown with the punctuation they most often have in
the corpus.

```
uh       actually i        don't          that's what   i      wish
no       it       wouldn't work           where  d'you  want   me
you      might    say      so             you    call   this   luck
can't    be       that     hard           cut    it     out    dude
```

Left, down: "Uh, no, you can't. Actually, it might be. I wouldn't say that.
Don't work so hard." Right, down: "That's where you cut. What d'you call it?
I want this out. Wish me luck, dude."

```
oh       but      i        can't          but      he       never    did
no       you      couldn't be             i        wouldn't forget   you
we       didn't   walk     far            didn't   have     a        name
don't    run      away     now            dare     to       face     him
```

Left, down: "Oh, no, we don't. But you didn't run. I couldn't walk away.
Can't be far now." Right, down: "But I didn't dare. He wouldn't have to.
Never forget a face. Did you name him?"

Two more from the top ten of the same run:

```
which  i      don't  get                  how     can     we      not
we     won't  lose   them                 could   i       have    another
can't  see    your   legs                 you     read    every   word
do     you    mind   moving               forget  it      right   now
```

Left, down: "Which we can't do. I won't see you. Don't lose your mind. Get
them legs moving!" Right, down: "How could you forget? Can I read it? We have
every right. Not another word now!"

Interpretation: the lines are dialogue, because the corpus is dialogue. Read
across, a grid sounds like one side of an argument; read down, like another.
The grids are heavy in negation, pronouns and auxiliaries ("don't", "can't",
"wouldn't"). These words begin and end many different sentences, which is
what a crossing needs.

### 4.3 Larger sentence sets give better grids

Observation: in the k = 20 run, no grid has more than 4 uncommon words (top
200), and more than half have none (0: 4265 grids, 1: 2907, 2: 766, 3: 91,
4: 1, counting each grid once). The k = 10 run with a floor of 4 uncommon
words (top 300) produced the grids in Section 4.2, which I judge more varied
than the best of the k = 20 run. The k = 20 top list is in `NOTES.md`.

Interpretation: lowering k adds rarer sentences, which carry the rarer words.
The floor on uncommon words then selects the grids that use them. The cost is
search time (Section 7).

### 4.4 The run at k = 7

The largest 4x4 search used the 832,981 sentences seen at least 7 times,
without names, and kept only grids with at least 5 uncommon words (outside
the 300 most frequent). It ran to completion in 240 parts and found 530
grids, which is 265 distinct pieces after removing transposes. All 1,215
sentences that appear in them were checked against the corpus counts.

Observation: of the 265 grids, 205 have exactly 5 uncommon words by the
ranking's count (outside the top 200), 37 have 6 and 23 have 7. Only 12 of
them use sentences that are all seen 10 or more times, so almost all of
these grids were out of reach of the k = 10 run. The median fluency is
-4.96, against -4.87 for the k = 10 set and -4.61 for the k = 20 set.

The three top-ranked grids:

```
oh       but      i        couldn't
no       it       cannot   be
you      can't    trust    anyone
don't    hurt     anybody  else
```

Down: "Oh no you don't. But it can't hurt. I cannot trust anybody. Couldn't
be anyone else."

```
here's  what     we     found
where   exactly  were   you
it      was      quite  easy
is      that     close  enough
```

Down: "Here's where it is. What exactly was that? We were quite close. Found
you easy enough."

```
but    i'm     no      fool
you    gonna   charge  me
don't  answer  at      once
forget it      all     right
```

Down: "But you don't forget. I'm gonna answer it. No charge at all. Fool me
once right?"

(The second and third are ranks 3 and 10; rank 2 contains profanity and is
in the gallery.)

Interpretation: this set has the most varied vocabulary of the 4x4 runs, and
its best grids read to me as the best 4x4 grids the system has produced. The
price is a lower floor of sentence quality. At k = 7 more lines are
fragments or transcription oddities, for example "Me working hard enough?"
and "Welcome to soon enough" in the grid ranked fourth. The fluency score
catches some of these and misses others, so the top of the list still needs
a human reader.

Caveat: the comparison of "best grids" across runs is my reading of the top
15 or so of each list, not a measurement.

## 5. Other shapes

### 5.1 Rectangles with long rows

Table 3. Exhaustive searches for rectangles, no names, all words distinct.
"3x5" means 3 rows of 5 words, so the columns are 3-word sentences.

| grid | rows k | columns k | grids | search nodes |
|---|---|---|---|---|
| 3x5 | 20 | 20 | 14,908 | 4.7e8 |
| 3x5 | 10 | 100 | 873 | 2.2e8 |
| 3x6 | 10 | 10 | 1,096 | 3.4e9 |
| 3x6 | 5 | 100 | 4 | 5.6e8 |
| 3x7 | 10 | 10 | 0 | 1.4e9 |
| 4x5 | 10 | 10 | 752 | 1.8e10 |
| 4x6 | 10 | 10 | 0 | 4.2e9 |

The 4x5 grids are, in my reading, as good as the 4x4 ones and larger: 20
distinct words and 9 sentences. Two from the top five:

```
why     don't   we      all     go        oh       but      it       couldn't help
do      you     have    the     right     no       you      can't    leave    me
i       know    another way     in        i        gotta    get      him      out
try     that    one     over    there     don't    go       in       there    now
```

Left, down: "Why do I try? Don't you know that? We have another one. All the
way over. Go right in there." Right, down: "Oh no I don't. But you gotta go.
It can't get in. Couldn't leave him there. Help me out now."

### 5.2 5x5

With all 25 words distinct, there is no 5x5 grid among the 572,554 five-word
sentences with k = 10 (exhaustive, 1.7e10 nodes). A run at k = 5 (1,593,694
sentences) was stopped after 5 percent of the search with no grid; it would
have needed about 9 hours.

Allowing 3 cells to repeat a word, at k = 10 without names (512,942
sentences), the exhaustive search (7.4e10 nodes, 12,566 CPU seconds) finds
exactly one grid and its transpose:

```
and     what    did     i       get
where   have    you     put     him
do      you     want    them    back
you     brought her     in      here
go      back    to      bed     now
```

Down: "And where do you go? What have you brought back? Did you want her to?
I put them in bed. Get him back here now." The word "you" appears three times
and "back" twice; the other 20 words appear once.

### 5.3 Short lines are the weak point of rectangles

Observation: in the 3x6 run at k = 10, many 3-word columns are not sentences:
"we have me", "that be me", "here right there". They pass the filter because
some subtitle line consisted of exactly those words.

Interpretation: a 3-word subtitle line is often a piece of a longer
utterance. Raising the threshold for the columns to k = 100 removes most of
these. The four 3x6 grids that survive are clean, for example:

```
yeah   well   i      think  you're right
we     are    just   about  here   now
can    you    do     that   again  please
```

Down: "yeah we can", "well are you", "i just do", "think about that",
"you're here again", "right now please".

## 6. Content words

The grids above use few nouns, verbs of action, or adjectives. I tried three
ways to change that.

Requiring content inside every sentence. Using only sentences with at most 2
common words (top 200) at k = 5 leaves 744,703 four-word sentences. The
search found no 4x4 grid in 2e9 nodes; it was not run to completion, so this
is not proof that none exists.

Requiring one uncommon word in every line. At k = 20 this leaves 188,583
sentences and no grid at all (exhaustive). So each of the 16,060 grids at
k = 20 contains a line made only of common words. At k = 10 it gives 368
grids, but in the sample I read the uncommon words are mostly "uh", "told",
"brought" and the like.

Generalizing beyond attested sentences. `ngram.c` accepts a 4-word line if
its first three words begin some attested sentence and its last three words
end one. This admits about 296 million lines instead of 2.5 million. Grids
with ten or more uncommon words are then easy to find, but most contain a
line that is not a sentence ("you of the day", "to not be now"). Raising the
n-gram count threshold from 5 to 20 did not fix it. The rule never checks
that the first and last word of a line fit each other.

Interpretation: a word can sit at a crossing only if it is flexible in two
directions at once. Function words are; most content words are not. Content
words enter at k = 10 one or two per sentence, where the rest of the sentence
is flexible enough to carry them. I see no way around this within attested
sentences except a larger corpus or a lower k.

## 7. Search cost

Observation: for 5x5 with distinct words, the search visited 4.0e7 nodes at
87,257 sentences and 1.7e10 nodes at 572,554 sentences. That is a growth
exponent of about 3.2. For 4x4, the step from k = 50 to k = 20 gives 3.2 and
the step from k = 20 to k = 10 gives 3.4; the last pair of runs differ
slightly in their constraints (Table 2). The step from k = 10 to k = 7 gives
3.0, again with a different floor on uncommon words. In the 4x4 run at k = 10, 90 percent
of the nodes are spent in the third row: the first two rows are easy to
stack, and most stacks cannot be continued.

Three attempts to reduce the cost, all negative:

- Most-constrained-line-first (`fill.c`), as crossword fillers do: 4 times
  fewer nodes, but roughly 25 times slower overall (timed on a busy machine), because counting the
  candidates of a line means scanning posting lists.
- Growing a top-left square block instead of filling row by row: same grids,
  2 to 4 times more nodes.
- A lower bound on the number of common words still to come: 17 percent fewer
  nodes.

Random search with restarts was also tried (random candidate order, or an
order that prefers words with many completions). At 5x5 with distinct words,
on the k = 5 and k = 3 sets, it found nothing in about 1e9 nodes. That says
little, because whether such grids exist in those sets is still unknown.

## 8. Comparison with the first project

Table 4. The v1 grids under the measures used here.

| grid | lines attested as sentences (k = 3) | fluency |
|---|---|---|
| v1, intersection search: "but it is not / it was the only / is the way to / not only to the" (symmetric) | 1 of 4 | -5.02 |
| v1, word category per column: "i know a man / we have the world / ..." | 2 of 4 rows, 0 of 4 columns | rows -4.58, columns -8.20 |
| v2, 4x4, k = 20 (8,030 grids) | all 8, by construction | median -4.61, best -3.73 |

The language model's fluency score does not separate the v1 intersection
grid from the lower half of the v2 grids. A fragment such as "it was the
only" is locally very probable. What separates them is completeness: v2 lines
are whole sentences that occur in the corpus, and v1 lines mostly are not.
This also means the fluency feature in the ranking should not be read as a
measure of sentence quality in general; within v2 it only orders sentences
that are already complete.

## 9. Limitations

- The judgment that the top grids are good is mine, from reading them. No
  one else has rated them, and the ranking weights were set by the same
  reader.
- "Attested" means "occurred as a subtitle line", which is weaker than
  "is a good sentence" (Section 3.1). At k = 10 a few lines are odd in
  isolation ("You do not need.").
- The register is film dialogue. The method would produce a different voice
  from a different corpus, and was not tried on one of comparable size.
- Coherence is measured by a 360-million-parameter model on text without
  commas. It is a rough signal.
- All counts are for these sentence sets and constraints. Statements that no
  grid exists are exact only for runs marked exhaustive.

## 10. Reproduction

See `README.md` for setup and data download. The runs in this report:

```bash
./venv/bin/python run_exhaustive.py --rows 4 --cols 4 --min-count 20
./venv/bin/python run_exhaustive.py --rows 4 --cols 4 --min-count 10 \
    --min-uncommon 4 --n-common 300 --no-names --parts 120
./venv/bin/python run_exhaustive.py --rows 4 --cols 4 --min-count 7 \
    --min-uncommon 5 --n-common 300 --no-names --parts 240
./venv/bin/python run_exhaustive.py --rows 5 --cols 5 --min-count 10 \
    --max-repeats 3 --no-names --parts 120
./venv/bin/python run_exhaustive.py --rows 4 --cols 5 --min-count 10 --no-names --parts 120
./venv/bin/python run_exhaustive.py --rows 3 --cols 6 --min-count 5 \
    --min-count-cols 100 --no-names --parts 40
./venv/bin/python score_grids.py data/runs/<run>/grids.pkl <k> data/feat_<name>.pkl
./venv/bin/python gallery.py data/feat_<name>.pkl -n 20
./venv/bin/python verify_grids.py data/feat_<name>.pkl <k>
```

The k = 20 4x4 run in Table 2 and the k = 10 5x5 run with distinct words in
Section 5.2 were made with an earlier version of the runner; the solver and
its inputs were the same. `NOTES.md` is the chronological log, including the
runs that failed.
