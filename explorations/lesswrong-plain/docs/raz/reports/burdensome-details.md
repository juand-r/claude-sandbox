# Report: burdensome-details

## 1. The argument in three sentences

In the conjunction fallacy people rate "A and B" as likelier than "A", because added detail
makes a story more representative and so more plausible, even though each detail makes it
less probable. Correcting yourself on a direct comparison is only a patch; forecasters who
each saw one statement could only have avoided the error by treating every "and" as a cost,
adding improbabilities (as log probabilities) rather than averaging them, and feeling every
added detail as a burden. So you must question each detail of a futurist's story on its
own, because support for one claim in a package is not support for the package.

## 2. Sources checked

- Tversky and Kahneman (1983), "Extensional Versus Intuitive Reasoning", Psychological Review
  90: 293-315. PDF: http://psy2.ucsd.edu/~mckenzie/TverskyKahneman1983PsychRev.pdf (read with
  pdftotext this session).
  - p. 308: "Similarly, a political analyst can improve scenarios by adding plausible causes
    and representative consequences. As Pooh-Bah in the Mikado explains, such additions
    provide 'corroborative details intended to give artistic verisimilitude to an otherwise
    bald and unconvincing narrative.'" and, just before, "although such additions can only
    lower probability."
  - pp. 307-308 (forecasters): 115 analysts; "The geometric means of estimates were .47% and
    .14%, respectively" (invasion and suspension; suspension alone), p < .01 by Mann-Whitney.
  - p. 303 (dice): "The percentages of subjects who chose the dominated option of Sequence 2
    were 65% with real payoffs and 62% in the hypothetical format." N = 125 with real payoffs.
    Also: the conjunction fallacy "is not restricted to esoteric interpretations of the
    connective and, because that connective was also absent from the problem."
  - I searched the whole text for "substitut" and "judgment of representativeness": the
    post's quoted phrase "substitute judgment of representativeness for judgment of
    probability" does not occur in this paper.
- The Mikado, Project Gutenberg #808 (The Complete Plays of Gilbert and Sullivan),
  https://www.gutenberg.org/cache/epub/808/pg808.txt: "POOH. Merely corroborative detail,
  intended to give artistic verisimilitude to an otherwise bald and unconvincing narrative."
  Context: after Ko-Ko's false report of Nanki-Poo's execution ("It is true that I stated that
  I had killed Nanki-Poo").
- "Conjunction Controversy (Or, How They Nail It Down)", LessWrong post cXzTpSiCrNGzeoRAz,
  postedAt 2007-09-20T02:41:38Z (Burdensome Details: 2007-09-20T23:46:06Z, so earlier the
  same day). Fetched via the GraphQL API. Matched:
  - "Now, a correlation near 1 does not *prove* that subjects are substituting judgment of
    representativeness for judgment of probability."
  - "The conventional interpretation has been nearly absolutely nailed down."
  - "In the conventional interpretation of the Linda experiment, subjects *substitute judgment
    of representativeness for judgment of probability:*" (so the phrase the post puts in
    quotation marks is, as far as I could check, the author's own wording from that post).
- `data/originals/twelve-virtues-of-rationality.md` (Posted: 2006-01-01), seventh virtue:
  "Each specification adds to your burden; if you can lighten your burden you must do so.
  There is no straw that lacks the power to break your back."
- LessWrong revision history (documentId Yq6aA4M3JKWaQepPJ): the 2007 text differs from the
  current one in small ways (it said "four green faces and one red face", "in 1981" for the
  Reagan study, and had a joke about box cutters). The current text is the one annotated;
  no note relies on the old one.

## 3. Arithmetic

- Absurdity in bits: 1 bit is probability 1/2, 4 bits is 1/16, 5 bits is 1/32 = (1/2)(1/16),
  which holds only if the claims are independent. In general P(A and B) = P(A) P(B | A), so
  -log2 P(A and B) = -log2 P(A) - log2 P(B | A). If B is made more likely by A, then
  P(B | A) > P(B), so -log2 P(B | A) < -log2 P(B): adding the unconditional absurdities
  overstates the total.
- Dice: the die has 4 green and 2 red faces, so P(G) = 2/3, P(R) = 1/3.
  (2/3)^6 = 64/729 = 0.0878; (1/3)^5 = 1/243 = 0.004115; ratio = (64/729) / (1/243) = 64/3
  = 21.3. "About 21 times" at a given starting position. (Over twenty rolls the ratio of the
  chances of appearing at least once is similar, since both are small; I did not compute it
  exactly and the note says "at a given position".)
- Forecasters: 0.47 / 0.14 = 3.36. The post says the forecasters "would need to penalize the
  probability substantially—a factor of four, at least, according to the experimental
  details". The smallest correction that removes the inconsistency is about 3.4, not 4. I
  judged this a nitpick with no consequence (STANDARDS 2.4(2)) and made no note; the editor
  may disagree.

## 4. Claims about other posts

- "Conjunction Controversy (Or, How They Nail It Down)": quotations above. This post is not
  in Rationality: A-Z and not in `data/originals`; I fetched it into my scratchpad only.
- "Twelve Virtues of Rationality": quotation above.
- Our note in `what-do-we-mean-by-rationality-1` (order 8) already raises Hertwig and
  Gigerenzer (1999) against the conjunction-fallacy interpretation. I did not repeat that
  criticism here. STANDARDS 2.5 says a recurring criticism should be made in full where it
  matters most; Burdensome Details, which says the experiments "confirmed" the standard
  interpretation and comes first in the book, may be the better place. The editor should
  decide; I did not touch the other post.

## 5. Items not verified

- The Reagan experiment and its 68%: the source (Tversky and Kahneman 1982, in Judgment Under
  Uncertainty) is not open. Web search results only echoed the post. The footnote cpara says
  the figure is unchecked.
- Kahneman and Frederick (2002): the UCLA copy failed TLS verification (server certificate
  chain) and then returned 503; the MIT link returned HTML. So I cannot say whether the quoted
  phrase occurs there. The report records this; no note claims the quotation is misattributed.
- The cosmology in the anecdote: universes reproducing through black holes is Lee Smolin's
  "cosmological natural selection" (Wikipedia, "Cosmological natural selection": "a
  hypothesis proposed by Lee Smolin ... Smolin first proposed the idea in 1992"). I could not
  source the added step about civilizations making black holes, so I made no note.

## 6. Judgment calls for the editor

1. Reserved words: "never" only in stating the conjunction rule and in the Mikado note. No
   verdict word is used.
2. The bits note says "Loosely stated" and "overstates the penalty". The mathematics is shown
   above. A fair defender could say the post meant independent claims; it does not say so,
   and its own target (causal futurist stories) is the dependent case.
3. The dice note: a fair defender could say "short" is shorthand for "feel every added detail
   as a burden", which is only claimed when one sequence adds to the other. The next
   paragraph ("even a single extra roll of the dice") supports that reading. The note says
   only that shortness decides this case because of containment, which is true either way.
   Consider cutting if it reads as taking a figure of speech literally.
4. "Repeats, in new words, the point made two paragraphs earlier": a structural judgment.
   Compare "only slapping a band-aid on the problem, not fixing it in general" with
   "Patching one gotcha as a special case doesn't fix the general problem."
5. The Response credits the post twice (correct point; both sides of the forecaster
   comparison). STANDARDS 2.1 allows brief credit where omitting it would mislead. I think
   both are needed for accuracy, but the older README would have cut them.
6. I considered a note that Tversky and Kahneman found "extensional cues" (thinking in
   frequencies) "markedly reduced" the fallacy (p. 309), a remedy the post does not mention.
   I dropped it: their manipulation cues the inclusion relation, which the post already
   dismisses as a band-aid, so fair-defender 5 applies.
