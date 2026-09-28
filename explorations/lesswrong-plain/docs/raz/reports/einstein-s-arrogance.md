# Report: einstein-s-arrogance

## 1. The argument in three sentences

Einstein's reply that he would "feel sorry for the good Lord" if Eddington's eclipse
observations failed looks like arrogance, since no one can know a theory is right before the
test. But singling out the correct hypothesis from a large space already takes about as many
bits of evidence as the hypothesis is complex (27 bits for one in 100 million), and this is
true of hunches too, so Einstein must already have held enough evidence to find General
Relativity. It is unlikely that he had just enough to find it and not much more, so he
probably had enough to be very sure, and his confidence was not foolhardy.

## 2. Sources checked

All saved in `data/sources/`.

- Lemos, "Shadow of the Moon and general relativity: Einstein, Dyson, Eddington and the 1919
  light deflection", arXiv:1912.05587 (`lemos_shadow_1912.05587.txt`, pdftotext).
  - Fig. 37 caption: "Lorentz telegram to Einstein in September 22, 1919, stating “Eddington
    found stellar shift at solar limb, tentative value between nine-tenths of a second and
    twice that.”"
  - "Sometime later he then states his famous phrase when the student of philosophy Ilse
    Schneider asks what he would say if the eclipse results were otherwise, not confirming his
    predictions: “I would have to be sorry for the dear Lord. The theory is correct”".
  - "However, wonderful as it was, this precession was an a posteriori confirmation, not an
    apriori prediction" (quoted in the Mercury note).
  - Abstract: Sobral team "Crommelin and Davidson ... led at a distance by the Astronomer Royal
    Frank Dyson, and with Eddington of Cambridge University that went to Principe".
- Wikiquote, "Albert Einstein" (`?action=raw`, `wikiquote_einstein.txt`, line ~1144):
  "Then I would have felt sorry for the dear Lord. The theory is correct." / "When asked by a
  student what he would have done if Sir Arthur Eddington's famous 1919 gravitational lensing
  experiment, which confirmed relativity, had instead disproved it." / "As quoted in Reality
  and Scientific Truth : Discussions with Einstein, von Laue, and Planck (1980) by Ilse
  Rosenthal-Schneider, p. 74". I did not read the memoir; the note says so.
- Janssen and Renn, "Einstein and the Perihelion Motion of Mercury", arXiv:2111.11238
  (`arxiv_2111.11238.txt`): "the Einstein-Grossmann or Entwurf (= outline or draft) theory ...
  could only account for 18 of the 43 seconds-of-arc-per-century discrepancy"; "In November
  1915, however, ... Einstein showed that his new general theory of relativity could account
  for all missing 43′′"; "He kept quiet about the 18′′ and continued to work on the Entwurf
  theory."
- Weinstein, "Genesis of general relativity", arXiv:1204.3386 (`arxiv_1204.3386.txt`, lines
  693-695, footnote 62 = "Einstein to Besso, March 10, 1914, CPAE, Vol. 5, Doc. 514"): "Now I
  am perfectly satisfied and no longer doubt the correctness of the whole system, regardless
  of whether the observation of the solar eclipse will be successful or not. The logic of the
  thing is too evident". This is Weinstein's translation; the note says "translation in
  Weinstein".
- Wikipedia, "History of general relativity" (`wp_history_gr.txt`): 1911 deflection
  prediction "too small (0.83 seconds of arc) by a factor of two"; "In 1914 and much of 1915,
  Einstein was trying to create field equations based on another approach." Background only.
- Peirce, Collected Papers vols. 5-6, archive.org djvu text (`peirce_cp5_6_djvu.txt`, lines
  5787-5870). 5.172: "Think of what trillions of trillions of hypotheses might be made of which
  one only is true; and yet after two or three or at the very most a dozen guesses, the
  physicist hits pretty nearly on the correct hypothesis. By chance he would not have been
  likely to do so in the whole time that has elapsed since the earth was solidified." 5.173:
  "man has a certain Insight, not strong enough to be oftener right than wrong, but strong
  enough not to be overwhelmingly more often wrong than right". Date: CP 5 Book I is
  "Lectures on Pragmatism ... Delivered at Cambridge, Massachusetts, March 26 to May 17, 1903".
- Stanford Encyclopedia of Philosophy, "Abduction", supplement "Peirce on Abduction"
  (`sep-abduction-peirce.txt`): "what the logical empiricists called the “context of
  justification”" and "for Peirce abduction had its proper place in the context of discovery".

## 3. Arithmetic

- log2(10^8) = 26.58. With 27 bits the odds are 2^27 / (10^8 - 1) = 1.34, probability 0.57:
  "at least 27 bits (or thereabouts)" is right.
- log2(10^6) = 19.93 ("~ 20 bits" right); 10^8 / 10^6 = 100 candidates, right.
- "at more than 99% probability, requires 34 bits": for 10^8 hypotheses log2(99 x 10^8) = 33.2;
  for the lottery of the previous post log2(99 x 131,115,984) = 33.6. 34 is right as a
  round-up. No note.
- 2^19 = 524,288 < 10^6, so 19 bits leave about (10^6 - 1) / 2^19 = 1.9 false positives per
  true target: "can't find one out of a million targets using only 19 bits" is right.
- 29.5 - 29.3 = 0.2 bits: odds 2^0.2 = 1.149, probability 0.535. The post pairs these numbers
  with "55%"; 53.5% is within the rounding the post's own framing allows. No note (STANDARDS
  2.4 numbers rule).
- log2(99) = 6.63, so 99% for a 29.3-bit hypothesis needs 35.9 bits: the range 29.3 to about 36
  used in the note.

## 4. Claims about other posts

- "How Much Evidence Does It Take?" (`data/originals/how-much-evidence-does-it-take.md`,
  Posted 2007-09-24): the 27-bit and 34-bit arithmetic. "the previous day's" checked against
  Posted 2007-09-25 for this post.
- I did not repeat the neighbour's criticism of "cannot form accurate beliefs based on
  inadequate evidence" (a lucky guess can be right), although this post's "cannot single out a
  correct 10-bit hypothesis" and "Or he couldn't have gotten them right" have the same
  looseness. The post's own conclusion is hedged ("probably"), so the looseness changes
  little here; I judged a pointer note would be a nitpick.
- `annotated/posts/faster-than-science.tex` (book order much later, posted 2008-05-20)
  already credits Peirce 1903. Since this post comes first in book order, the full Peirce
  point now sits here (STANDARDS 2.5); the editor may want to reduce the faster-than-science
  note to a pointer in the whole-book pass. Also: that note says Peirce "made the same
  argument". Peirce made the same counting argument but drew a different conclusion (an
  insight "not strong enough to be oftener right than wrong", CP 5.173), so "the same
  argument" is loose for the conclusion. I did not edit that file.

## 5. Items not verified

- Rosenthal-Schneider's memoir itself (1980), and whether the question was put by a
  journalist in any other account. The note relies on Lemos (2019) and Wikiquote and says
  the memoir was not read.
- Minor facts left without a note (STANDARDS 2.4(2)): the post says Eddington "led
  expeditions to Brazil and to the island of Principe"; per Lemos, Eddington went to Principe,
  and the Sobral (Brazil) team of Crommelin and Davidson was "led at a distance" by Dyson. The
  post also says "solar eclipses" (one eclipse, 29 May 1919, two sites).
- The Entwurf theory's light-deflection prediction (the "half value") is from Lemos ("the
  Newtonian value also predicted by the equivalence principle [2] and the entwurf theory");
  not used in any note.

## 6. Judgment calls for the editor

1. Reserved word "wrong" for the Entwurf theory ("That theory was wrong"; also in Response and
   an n.b.). Evidence: it accounted for 18 of 43 arcseconds and was abandoned by Einstein in
   November 1915 (Janssen and Renn: "Einstein listed the value of 18′′ as one of his reasons
   for abandoning the Entwurf theory"). I think the word is met.
2. The key logic note ("Or he couldn't have gotten them right"): a fair defender may say the
   post argues from the fact of correctness only to explain Einstein's 1919 remark, not to
   give a test usable beforehand. The note says what the argument can and cannot show; it
   does not say the conclusion is false. The Response's "In short" repeats this.
3. The point-versus-range note: a defender may say "exactly" was rhetorical and the post
   meant "just above the threshold". The note targets the step from a point to "Not likely!";
   the post gives no distribution. Consider softening if it reads as taking a figure of
   speech literally.
4. The "perfect Bayesian" note (paragraph on inefficiency): a logical gap, not an outside
   objection, but the editor should check it does not read as contrived (STANDARDS 2.4(5)).
5. The Peirce note: "old idea" criticism. Peirce drew a different conclusion, which the note
   says; the post's point about hunches needing evidence is not in Peirce. Credit is also
   given in the Response ("real content").
6. The "context of discovery / justification" remark in a cpara is descriptive, not a
   criticism; cut if it looks like padding.
7. Pronouns: Einstein and Peirce keep "he" (historical figures). Rosenthal-Schneider is named,
   never given a pronoun. The post's author gets none.
