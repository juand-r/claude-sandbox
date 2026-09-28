# Report: optimization-and-the-intelligence-explosion

## 1. The argument in three sentences

Intelligence and natural selection are both optimization processes, and the history of Earth
can be divided into epochs in which a protected meta level (natural selection, the human
brain) does the optimizing while object-level products accumulate, with rare meta-level
innovations (sex, cells and DNA, science) starting new epochs. A fully recursive
self-improving AI would have no protected optimizing level, so it would break with the
whole past; the objection that self-improvement may need exponentially more effort for each
linear gain is answered by the hominid line, where roughly constant selection pressure did
not seem to need exponentially more time per increment. The author admits this is analogy,
good at best for qualitative predictions, but gives it as the reason for not extrapolating
growth over time: the right graph is optimization power in against optimized product out.

## 2. Sources checked

- First version of the post: LessWrong GraphQL, post `HFTn3bAT6uXSNwv4m`, "Optimization and
  the Singularity", postedAt 2008-06-23T05:55:35Z (old URL lesswrong.com/lw/rk/... redirects
  there). Saved: `data/sources/b3a_optim/lw_2008_optsing.md` (and `.json`, and comments in
  `lw_2008_optsing_comments.json`; Hanson did not comment). Matched: "lest I annoy my esteemed
  co-blogger"; "a clash of intuitions between myself and Robin. Robin's looking at populations
  and resource utilization."; "would *not* be bound to one-month economic doubling times". Used
  only to identify the forecast the last paragraph answers (note on the last paragraph,
  Response, honest n.b.), not as grounds for criticism (STANDARDS 2.5).
- Robin Hanson, "Economics of the Singularity", IEEE Spectrum, page dated "01 Jun 2008".
  https://spectrum.ieee.org/economics-of-the-singularity, curl, text in
  `data/sources/b3a_optim/hanson_spectrum.txt`. Matched: "acceleration also ensues as the
  economy, by getting larger, enables its members to explore an ever-increasing number of
  innovations"; "If a new transition were to show the same pattern as the past two, then growth
  would quickly speed up by between 60- and 250-fold. The world economy, which now doubles in 15
  years or so, would soon double in somewhere from a week to a month."
- I. J. Good, "Speculations Concerning the First Ultraintelligent Machine", Advances in
  Computers 6 (1965), p. 33. http://incompleteideas.net/papers/Good65ultraintelligent.pdf
  (scanned, no text layer; no OCR tool here). I read the page image (PDF page 2, rendered with
  pdftoppm) and transcribed it in `data/sources/b3a_optim/good1965_p33_transcribed.txt`.
  Matched: "an ultraintelligent machine could design even better machines; there would then
  unquestionably be an "intelligence explosion," and the intelligence of man would be left far
  behind". (The note drops the comma inside the inner quotation marks.)
- Book's own introduction to this part: `data/originals/minds-an-introduction.md`, "Since then,
  Yudkowsky has come to favor I.J. Good's older term, "intelligence explosion,"".
- Maynard Smith and Szathmáry, The Major Transitions in Evolution (1995): secondary only,
  Wikipedia raw text, `data/sources/b3a_optim/mt_wiki.txt`. Table rows used: "Independent
  replicators (probably RNA) | Chromosomes"; "RNA as both genes and enzymes | DNA as genes;
  proteins as enzymes"; "Asexual clones | Sexual populations"; "Primate societies | Human
  societies with language". I did not see the book.

## 3. Arithmetic

None in the notes. (Hanson's "60- and 250-fold" and the 15-year doubling are quoted as
context, not recomputed: 15 years / 250 is about 22 days, 15 / 60 is 3 months, so "a week to a
month" is Hanson's own rounding; not used in any note.)

## 4. Claims about other posts

- "Optimization and the Singularity" (first version): see section 2.
- "Minds: An Introduction" credits Good's term: see section 2.
- The post's own words used in other notes (Artificial Addition cites this post):
  "natural selection is an *accidental* optimization process"; "humans are *optimized*
  optimizers handcrafted by natural selection".

## 5. Items not verified

- Whether the 2015 LessWrong text is identical to the book text. I annotated the LessWrong text.
- Hominid brain evolution rates: I did not bring in data. The note only says the post measures
  neither quantity and that the case stops at human level.
- The Maynard Smith and Szathmáry list is from Wikipedia, not the book.

## 6. Judgment calls for the editor

1. The Hanson note on "constant optimization pressure". A fair defender could say "constant
   rate" meant per optimizer, the brain being the same. The note grants that ("The brain has not
   changed") and only says the total input was not constant. It is sourced to Hanson, who is
   the opponent; an independent economic source (Kremer 1993, population and technological
   change) would also fit, but I did not fetch it.
2. The hominid note says the evidence "covers only the climb from ape to human" and that the
   objection concerns an AI going far beyond that. This is a scope point, not a counter-argument.
   I avoided saying the returns do diminish.
3. The Good note: prior work that the post does not credit. Following the brief, it is phrased
   as information and credit ("Its own addition is the account in terms of a protected meta
   level"), not as a fault. The Response says "Its central idea has a known source"; the editor
   may want it softer, since the book's own introduction already credits Good's term.
4. Earlier revision used for context only: the last-paragraph note and the Response identify
   Hanson's forecast from the 2008 text. I removed my first draft's "so a reader cannot tell
   which forecast is being answered" from the note, as it leaned on the revision; the Response
   still says the forecast is not named "in this version", which is a plain fact.
5. The Einstein note ("The inference needs a premise it does not state") is flagged "motive?"
   by raz_check only because of the word "inference". It is about logic, not motive.
6. "invents" flagged as reserved: it paraphrases the post's hammer example, not a charge.
7. No "My reading" inferences. No reserved words used as charges.
8. The honest section is 525 words by the checker's count (slightly over 500).
9. Tooling: another batch-3a agent uses `data/sources/b3a_tools/`; it overwrote my first helper
   script there. My files are now in `data/sources/b3a_147-149_tools/` (skeleton copies, note
   lists, inserter). Nothing of theirs was changed.
