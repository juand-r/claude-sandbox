# Report: anchoring-and-adjustment

## 1. The argument in three sentences

Arbitrary numbers bias estimates: subjects who saw a wheel of fortune stop at 65 guessed a
higher share of African countries in the UN than those who saw 10, and students who saw
8 × 7 × ... × 1 guessed a larger product than those who saw 1 × 2 × ... × 8. The post explains
this by adjustment from the anchor that stops at the first plausible value, and adds that
payoffs did not reduce the effect and that even absurd anchors work. Since debiasing has
mostly failed, the author suggests discarding implausible anchors and deliberately
considering an anchor on the opposite side.

## 2. Sources checked

All saved in `data/sources/raz_b2b_fresh/`.

- Tversky and Kahneman (1974), Science 185: 1124-1131. PDF from
  https://sites.socsci.uci.edu/~bskyrms/bio/readings/tversky_k_heuristics_biases.pdf
  (`tk1974.pdf`, `tk1974.txt`). Matched: "the median estimates of the percentage of African
  countries in the United Nations were 25 and 45 for groups that received 10 and 65,
  respectively, as starting points. Payoffs for accuracy did not reduce the anchoring effect."
  Also "The subjects were instructed to indicate first whether that number was higher or lower
  than the value of the quantity, and then to estimate the value of the quantity by moving
  upward or downward from the given number." Multiplication: "Two groups of high school
  students estimated, within 5 seconds"; "The median estimate for the ascending sequence was
  512, while the median estimate for the descending sequence was 2,250. The correct answer is
  40,320." Also "adjustments are typically insufficient". The anchoring section says nothing
  about plausibility or confidence intervals.
- Strack and Mussweiler (1997), JPSP 73: 437-446. PDF from
  https://bear.warrington.ufl.edu/brenner/mar7588/Papers/strack-mussweiler-jpsp97.pdf
  (`sm1997.pdf/.txt`). Abstract: "Results of 3 studies support the notion that anchoring is a
  special case of semantic priming". Study 3: 69 recruited, 2 excluded (n = 67 in Table 6);
  Table 5 lists Einstein, actual 1921, plausible anchors 1939 / 1905, implausible 1992 / 1215,
  one of eight questions; Table 6 gives pooled z values (plausible .04 / -.13, implausible
  .25 / -.17). Text: "A mere inspection of the means reveals that implausible anchors were at
  least as effective as plausible ones." Discussion questions "a simple adjustment to the
  boundary of the plausibility range".
- Epley and Gilovich (2001), Psychological Science 12: 391-396. PDF from
  https://bear.warrington.ufl.edu/brenner/mar7588/Papers/epley-gilovich-psysci2001.pdf
  (`eg2001.pdf/.txt`). Matched: "anchoring effects observed in the standard paradigm appear to
  be produced by the increased accessibility of anchor-consistent information"; abstract
  "a consensus that none takes place seems to be emerging. We argue that this conclusion is
  premature"; Study 2 description of adjusting by "jumps" until a value "seems plausible,
  adjustment stops".
- Klein et al. (2014), "Investigating Variation in Replicability: A 'Many Labs' Replication
  Project", Social Psychology 45: 142-152. PDF from https://stanford.edu/~knutson/jdm/klein14.pdf
  (`manylabs1.pdf/.txt`). Abstract: "13 classic and contemporary effects across 36 independent
  samples totaling 6,344 participants"; Discussion: "The original studies produced
  underestimates of some effects (e.g., anchoring-and-adjustment and allowed versus forbidden
  message framing)". The anchoring items came from Jacowitz and Kahneman (1995), not the 1974
  wheel; the note says "a later version of the task".
- Mussweiler, Strack and Pfeiffer (2000), PSPB 26: 1142-1150. Abstract via Crossref API
  (`crossref_msp2000.json`): "anchoring can be reduced by applying a consider-the-opposite
  strategy"; "Considering the opposite (i.e., generating reasons why an anchor is
  inappropriate) fulfills this objective"; "Study 1 demonstrated that listing arguments that
  speak against a provided anchor value reduces the effect."
- "Priming and Contamination" (`data/originals/priming-and-contamination.md`, Posted
  2007-10-10): "But modern research seems to show that most anchoring is actually due to
  contamination, not sliding adjustment."

## 3. Arithmetic

- 8! = 40,320 (checked). 512 and 2,250 as in the paper.
- 7 September 2007 to 10 October 2007 = 33 days: "a month later".
- Strack and Mussweiler Table 6: plausible difference .04 - (-.13) = .17; implausible
  .25 - (-.17) = .42. So the implausible effect was, if anything, larger; the post's "just as
  large" is conservative. Not noted.

## 4. Claims about other posts

- "Priming and Contamination": quoted above, matched in the original.

## 5. Not verified

- Quattrone et al. (1981), unpublished manuscript, cited for "subjects instructed to avoid
  anchoring still seem to do so". I could not find it. No note relies on it.
- The claim that debiasing "generally proved not very effective" is hedged and uncited; I
  made no note beyond the one on Mussweiler, Strack and Pfeiffer.

## 6. Judgment calls

- The main note (paragraph "The current theory ...") says "Overstated for the post's own main
  example." The fair-defender reply would be "adjustment was still a live theory in 2007". It
  was, for self-generated anchors, and the note says so. For experimenter-supplied anchors
  the post's own cited source (Strack and Mussweiler) and Epley and Gilovich say otherwise,
  and the author said so a month later. I did not use "wrong".
- The \cfact on the 1974 instructions ("did not choose the anchor as a starting point on their
  own"): this is a design fact, not a criticism of the post's numbers. Later studies without
  such instructions also find anchoring (Many Labs). The Response uses it only to say the
  wheel study does not show spontaneous starting from the anchor.
- The Many Labs credit sentence: added because the neighbouring priming post gets a
  replication note, and a reader should not carry that doubt over to anchoring.
- The last cpara says the post "reports no test of either" remedy. True of the post (the
  Quattrone citation supports the claim that instructions fail, not the remedies). The
  Mussweiler, Strack and Pfeiffer method is different from the post's second remedy (reasons
  against the anchor vs. a counter-anchor); the note says "a different one".
