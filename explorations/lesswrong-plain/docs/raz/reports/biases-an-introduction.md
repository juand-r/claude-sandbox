# Report: biases-an-introduction

## 1. The argument in three sentences

Random sampling error shrinks as you gather more data, but a statistical bias pushes a
sample in one direction and more data may not fix it; cognitive biases are the same kind of
systematic error in how we think, and are harder to correct because the faulty instrument is
ourselves. Knowing about biases (base rate neglect, sunk costs) does not make people immune
to them or even able to see them in themselves, but biases can be reduced, and the book's
approach is to build "expertise": an understanding of why good reasoning works, compared to
Serfas's finding that accounting courses, not work experience, reduced sunk-cost bias. The
last section introduces the book: essays by Yudkowsky from 2006 to 2009, organized around
Korzybski's "the map is not the territory" in four sequences and a closing dialogue.

## 2. Sources checked

- Tversky and Kahneman (1974), "Judgment under Uncertainty: Heuristics and Biases", Science.
  PDF: https://www2.psych.ubc.ca/~schaller/Psyc590Readings/TverskyKahneman1974.pdf.
  Matched: "Steve is very shy and withdrawn, invariably helpful, but with little interest in
  people, or in the world of reality. A meek and tidy soul, he has a need for order and
  structure, and a passion for detail." and "a list of possibilities (for example, farmer,
  salesman, airline pilot, librarian, or physician)".
- Hansen, Gerbasi, Todorov, Kruse and Pronin (2014), PSPB 40(6).
  PDF: https://bpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/f/3051/files/2021/02/Hansen_PSPB2014.pdf.
  Matched: abstract "Across the three experiments, participants who used a biased strategy
  rated it as relatively biased, provided biased judgments, and then claimed to be relatively
  objective."; Experiment 3: "Participants in the explicitly biased condition claimed
  objectivity after using their biased assessment strategy—indeed, they claimed more
  objectivity than they had prior to using the strategy." Bias shown: famous-attributed
  paintings M = 6.24 vs 6.00, p < .0001. Pre-task self-objectivity 4.98, post-task 6.89 (biased
  condition). Participants were "led to use" the strategy (assigned, not chosen, in Exps 2-3).
- Korzybski quotation: Wikipedia "Map–territory relation" (raw wikitext): "A map is not the
  territory it represents, but, if correct, it has a similar structure to the territory, which
  accounts for its usefulness", cited to Science and Sanity (1933), p. 58. Secondary.
- Manifest `data/manifests/rationality_az.json`: Map and Territory has sequences Predictably
  Wrong, Fake Beliefs, Noticing Confusion, Mysterious Answers; last post the-simple-truth;
  Yudkowsky posts in the book dated 2006-11-22 to 2009-03-16; six books in all. Matches the
  introduction.

## 3. Arithmetic recomputed

- None of the notes relies on arithmetic. For my own check of "more data can even
  consistently worsen a biased prediction": for a sample proportion with fixed bias b, the
  expected absolute error falls toward |b| as n grows, so more data does not worsen it on
  average; but the probability of landing within a tolerance smaller than |b| of the truth
  falls toward zero, so "can ... worsen" is defensible in that sense, and with a good prior
  plus biased data it clearly can. That is why the note says only that the claim is hedged and
  given no example, not that it is wrong.

## 4. Claims about other posts

- Preface (`data/originals/preface.md`), third paragraph: "the first-largest mistake in my
  writing, which was that I didn't realize that the big problem in learning this valuable way
  of thinking was figuring out how to practice it, not knowing the theory." Quoted in the
  clogic note, the Response and the honest n.b. The preface is by Yudkowsky; this
  introduction is by Bensinger. The notes say "sits uneasily with", not "contradicts".

## 5. Not verified

- The 75:1 salesperson-to-librarian ratio (Weiten textbook): not checked. Google Books API
  returned a quota error (429). The note says I could not check it. (Rough BLS-style reasoning
  suggests the ratio depends heavily on which occupations count as "sales"; I did not use this.)
- Heuer on base rate neglect; Pronin, Lin and Ross (2002); Ehrlinger, Gilovich and Ross (2005),
  including the phrase "biased-feeling thoughts": not checked. The cpara says so.
- Serfas (2010): the book is paywalled (Springer chapter PDF returned HTML). The quotation and
  the "accounting courses" finding are unchecked; the cpara says the quotation was not checked.
- "It's known that subjects can reduce base rate neglect ... by thinking of probabilities as
  frequencies": I did not check the literature (Gigerenzer and Hoffrage 1995 is the obvious
  source; Crossref confirms the title "How to improve Bayesian reasoning without instruction:
  Frequency formats"). My note says only that the sentence has no source.
- Yudkowsky's parents' professions; Ariely: not checked, no note.

## 6. Judgment calls for the editor

1. The clogic "sits uneasily with the Preface". Criticizes Bensinger's text using Yudkowsky's
   preface. Fair-defender reply for Bensinger: "understanding why good reasoning works" is more
   than "knowing the theory", and the Serfas quote itself includes spotting and tools. I think
   "sits uneasily" survives that reply; "contradicts" would not.
2. "Accounting courses are formal instruction in a subject; the book is a collection of blog
   essays." Could read as belittling. The introduction itself calls them essays from a blog.
3. The Steve-problem cpara credits Tversky and Kahneman. It is not a charge: the introduction
   does not claim the example as new, and it may have come via the Weiten textbook.
4. "Reports Hansen et al. (2014) accurately" is credit. I kept it because I checked it and a
   reader should know the summary holds.
5. Paragraphs without \cpara: the "Question:" line and the seven citation footnotes.
6. BUILD FAILURE (not fixable within my files): `annotated/preview.sh posts
   biases-an-introduction` fails with "Unicode character ⁴ (U+2074) not set up for use with
   LaTeX". md2tex left the footnote markers as Unicode superscripts ¹ to ⁷; ¹²³ are in
   Latin-1 and work, ⁴ to ⁷ do not. `\DeclareUnicodeCharacter` is preamble-only, so it cannot go
   in the post file, and replacing the characters with `\fnnum{}` makes check_verbatim fail.
   Tested fix: adding to `annotated/preamble.tex`
   `\DeclareUnicodeCharacter{2074}{\textsuperscript{4}}` and the same for 2075, 2076, 2077.
   With that (in a scratch copy of the preamble) the post and afterword build with 0 overfull
   boxes. Other agents' posts with ⁴ or higher will hit the same error.
