# Report: Probability is in the Mind (order 197)

Agent batch 4a. Sources and scripts in `data/sources/4a_searching-for-bayes-structure/`.

## 1. The argument in three sentences (written before annotating)

Following Jaynes, probabilities describe an agent's partial information, not properties of
objects: a coin known only to be biased, in an unknown direction, gets probability 0.5 for
one flip, and a robot that can predict the flip has a different probability, with no "real"
one between them. Two classic puzzles (two children, four cards) seem paradoxical only if a
probability is taken as a property of the children or cards, since asking different questions
yields different evidence and so different, correct, probabilities. Hence "Probabilities
express uncertainty, and it is only agents who can be uncertain."

## 2. Sources checked

- E. T. Jaynes, "Clearing up Mysteries: The Original Goal", in Maximum Entropy and Bayesian
  Methods, ed. J. Skilling (Kluwer, 1989), 1-27 (https://bayes.wustl.edu/etj/articles/cmystery.pdf;
  `data/sources/4a_searching-for-bayes-structure/jaynes_cmystery.txt`). Matched: "But that is
  claiming something that one could never know to be true; we call it the Mind Projection
  Fallacy." and "The current literature of quantum theory is saturated with the Mind
  Projection Fallacy." Also Jaynes, Probability Theory (2003), ch. 1-3
  (`data/sources/jaynes_book_ch1-3.txt`, line 1596): "We call this the 'Mind Projection
  Fallacy,'". Whether Jaynes "coined" the term is not proven by these, but he uses it as his
  own ("we call"); the note says only that.
- Stanford Encyclopedia of Philosophy, "Interpretations of Probability" (Hájek, rev. 2023),
  copy fetched in batch 1 (`data/sources/raz_batch1/sep_probability_interpret.txt`), copied
  and split into sentences in `data/sources/4a_searching-for-bayes-structure/sep_prob_sentences.txt`.
  Matched: finite frequentism "developed by Venn (1876)"; "Reichenbach thus excludes such
  sequences"; von Mises "regards single case probabilities as nonsense: 'We can say nothing
  about the probability of death of an individual ... The phrase 'probability of death', when
  it refers to a single person, has no meaning at all for us'"; "Von Mises embraces this
  consequence, insisting that the notion of probability only makes sense relative to a
  collective."; "A well-known objection to any version of frequentism is that relative
  frequencies must be relativised to a reference class" / "the so-called reference class
  problem for frequentism"; "Peirce regards the propensity as a property of the die itself,
  whereas Popper attributes the propensity to the entire chance set-up of throwing the die.";
  "Popper (1957) is motivated by the desire to make sense of single-case probability
  attributions that one finds in quantum mechanics—for example 'the probability that this
  radium atom decays in 1600 years is 1/2'."
- Diaconis, Holmes and Montgomery, "Dynamical Bias in the Coin Toss", SIAM Review 49, no. 2
  (2007): 211-235 (https://www.stat.berkeley.edu/~aldous/157/Papers/diaconis_coinbias.pdf;
  `diaconis_coin.txt`). Matched: "With careful adjustment, the coin started heads up always
  lands heads up—one hundred percent of the time." and "For natural flips, the chance of
  coming up as started is about .51." Published electronically 1 May 2007, before the post.
- Fienberg, "Randomization and Social Affairs: The 1970 Draft Lottery", Science 171 (1971):
  255-261; abstract via PubMed 17736218 (`pubmed_17736218.txt`). Matched: "several young men
  have filed suit in federal court, seeking to void the 1970 drawing and to force a new
  lottery. The basis of these suits is the lack of proper randomization (30)."
- Starr, "Nonrandom Risk: The 1970 Draft Lottery", Journal of Statistics Education 5, no. 2
  (1997) (https://jse.amstat.org/v5n2/datasets.starr.html; `starr_jse.txt`). Matched: "those
  with birthdates later in the year seemed to have had more than their share of low lottery
  numbers and hence were more likely to be drafted" and "The capsules were put in a box month
  by month, January through December, and subsequent mixing efforts were insufficient to
  overcome this sequencing." Starr's data section confirms the pattern statistically
  (correlation -.226 between birth date and draft number).
- The judge's remark "To whom is it unfair?": searched (WebSearch, two queries); not found.
  The note says so.

## 3. Arithmetic (script: `data/sources/4a_searching-for-bayes-structure/check_probability.py`)

Output:
```
P(yes to 'at least one boy') = 3/4
P(BB | at least one boy) = 1/3
P(yes to 'eldest boy') = 1/2
P(BB | eldest boy) = 1/2
P(BB | youngest boy) = 1/2
with P(boy)=0.512, P(BB | >=1 boy) = 0.344
number of hands: 6
P(yes to 'at least one ace') = 5/6
P(AA | at least one ace) = 1/5
P(yes to 'AS') = 1/2  P(AA | AS) = 1/3
P(yes to 'AH') = 1/2  P(AA | AH) = 1/3
overlap of 'has AS' and 'has AH': {('AH', 'AS')}
P(AA | names AS, random-ace protocol) = 1/5
simulated share of AA among hands with an ace: 0.2004
bias 0.6 -> P(heads) with symmetric ignorance = 0.5   (also 0.7, 0.9)
P(BB | mother volunteers 'at least one boy', random choice) = 1/2
```
Every number in the post is correct: 1/3, 1/4-1/2-1/4 priors, 1/2 (eldest, youngest), 1/5,
six combinations, 1/3 (spades, hearts), 5/6, 1/2, 3/4, 1/2. The real share of boys at birth
(about 0.512) moves 1/3 to 0.344; the post says "If you assume ... 1/2", so no note. The
random-ace protocol line shows that the case split works when the cases are disjoint (1/5
whichever ace is named); I did not put it in a note. The volunteer-protocol line supports the
note that the post's wording (you ask) is what makes 1/3 correct.

## 4. Claims about other posts

- "Mind Projection Fallacy" is the previous day's post (manifest: 2008-03-11T00:29 against
  2008-03-12T04:08). Our Response there says the probability argument is "deferred to another
  post"; this is that post; consistent.
- "Mysterious Answers to Mysterious Questions": its note already records that this post
  attributes "if I am ignorant of a phenomenon, that is a fact about my state of mind" to
  Jaynes. Not repeated.

## 5. Not verified

- The judge's remark (see above) and which lottery the author meant ("slips with names" fits
  neither the 1969 date capsules exactly; the note says "The best-known case fits").
- The post's link on "certain way" goes to overcomingbias.com/2008/01/something-to-pr.html
  ("Something to Protect"), which does not seem to be about betting theorems. Not opened; not
  noted (nitpick).
- Whether the coin example is "the classic example" in Jaynes: not checked; no note.

## 6. Judgment calls

- The clogic "As staged, the two speakers do not disagree about any fact ... a difference over
  the word 'probability'". This is the sharpest charge. Fair-defender checks: the post warns
  "I cannot do justice to this ancient war in a few words", and the note's cpara before it
  says so; the Bayesian's own "You can call that number whatever you like" is quoted. The
  Bayesian also claims that the frequency meaning is not what "probability" should mean, which
  is still a dispute about the word. The In short line says "stages a dispute over a word";
  if the editor thinks this too strong, "as staged" in the Response is the hedge to keep.
- The clogic on the apples: says the puzzles do not decide between the views. The post never
  says outright that they refute frequentism; the note ties them to the frequentist only
  through the post's own word "inherent" (frequentist: "inherent propensity"; puzzles: "inherent
  properties of objects"), and says so in the cpara, not as a reading of motive.
- "That is not the frequentist's view" (the view that each set of cards carries its own
  pair-probability). Frequentists relativize to a class, per SEP. A Peirce-style propensity
  ("property of the die itself") is closer to the target; I therefore did not say "no school",
  and the Response says only "frequentists do not hold that".
- The draft-lottery note gives information that cuts against the anecdote's point; it does not
  say the post is wrong. It keeps "I believe".
- Credit notes ("Correct", Diaconis support, the careful wording of the boy-girl puzzle) are
  frequent because the mathematics is right.
- Scope note on quantum chance: one sentence of scope, with Jaynes's own opposite view given so
  the note is not one-sided.
- Honest section is 587 words, above the 500 guide; the post is 1,744 words with two puzzles,
  and the n.b. notes carry the frequentist and propensity views the brief asked to state
  fairly. Summary is 200 words for the same reason.
- Pronoun flags: "his" for Jaynes (historical figure), "she" for the mathematician (the post's
  character). Reserved-word flags: "without contradiction" (arithmetic), "says nothing false"
  (credit).
