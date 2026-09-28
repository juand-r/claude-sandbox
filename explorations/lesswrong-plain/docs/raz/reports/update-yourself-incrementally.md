# Report: update-yourself-incrementally

## 1. The argument in three sentences

A theory that makes probabilistic predictions will sometimes meet contrary evidence even when
it is true, so the right response to one contrary observation is a small downward shift in
belief, not a defence that argues the observation away and not a rejection of the theory.
People resist this because they treat evidence qualitatively, as if a true theory could have
no failures, and because they want to win debates, but rationality is for deciding which side
to join, not for winning. By conservation of expected evidence you must expect as much
downward as upward revision, so a downward shift is normal, and when the downward shifts keep
coming you should let the belief go and celebrate.

## 2. Sources checked

- No outside sources. Comments fetched for context (GraphQL) in
  `data/sources/b2_againstrat/comments_uyi.json`; none used in the notes.
- The phrase "you must expect to be exactly as confident as when you started out"
  (note on the conservation paragraph; afterword "exactly as confident") is from
  `data/originals/conservation-of-expected-evidence.md`: "On *average*, you must expect to be
  *exactly* as confident as when you started out." Our note there calls it false if
  "confident" means "sure"; my note calls it a "slip", consistent with that note.

## 3. Arithmetic

- Coin, 95% hypothesis against a fair coin: a head has likelihood ratio 0.95/0.5 = 1.9; a
  tail 0.05/0.5 = 0.1, i.e. it divides the odds by 10. (Note on "shift downward a little".)
- Against a 90% coin, for the report only: head 0.95/0.90 = 1.056, tail 0.05/0.10 = 0.5.
- "At nineteen heads per tail the 95% hypothesis beats any rival": with 19 H and 1 T the
  likelihood q^19 (1-q) is maximized at q = 19/20 = 0.95 (derivative of 19 ln q + ln(1-q)
  is zero at q = 0.95), so every other q has lower likelihood on those data.
- "On average a correct theory will generate a greater weight of support": the expected log
  likelihood ratio under the true hypothesis is the Kullback-Leibler divergence, which is
  non-negative (zero only if the rival predicts identically). Standard result; no source cited
  in the note.

## 4. Claims about other posts

- "Conservation of Expected Evidence" posted 2007-08-13 (`Posted:` line), this post 2007-08-14:
  "the day before".
- The note refers to our notes on that post (the "exactly as confident" slip, and what the
  rule does and does not forbid). Checked in `annotated/posts/conservation-of-expected-evidence.tex`.

## 5. Not verified

- The original has a footnote marker "2" after "take a hit or two" (`[2](#fn2x25)`) with no
  footnote text in the LessWrong text. Probably an import artifact from the book. The
  skeleton drops it; I made no note (editor's slip, no consequence).
- Considered and dropped: "If you think you already know what evidence will come in, then
  you must already be fairly sure of your theory" is not true in general (P(H)=0.5,
  P(E|H)=1, P(E|~H)=0.9 gives P(E)=0.95 with H at 0.5). The conclusion drawn (little room
  to rise) still holds, because such E carries little information. No consequence for the
  argument, so no note (STANDARDS 2.4).

## 6. Judgment calls

- Reserved words: "never names" (a rival hypothesis): I searched the post; no rival
  hypothesis for the coin or anything else is named. "refute", "false" appear only in
  describing the post's own claims.
- The main criticism (no way to size a downward shift; a single tail against a fair-coin
  rival is a tenfold shift) is a clogic and the Response's main point. The post's "iota"
  hedge is acknowledged in the note: the criticism is that the post does not say which
  observations are iotas.
- "Asserted without an example" for "widely believed": a claim about what people believe,
  given without an instance. Mild; the editor may judge it an "any essay" point.
- Response credits the post (correct lesson; exact statement of the conservation rule).
