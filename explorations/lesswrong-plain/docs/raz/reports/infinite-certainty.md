# Report: infinite-certainty

## 1. The argument in three sentences

A statement can be exactly and always true (the lightspeed limit, 2 + 2 = 4) while our
confidence in it stays short of certainty, because a degree of confidence is not a degree
of truth. The right standard for confidence is calibration, and human beings who say they
are 99% sure are not right 99% of the time; claiming 99.9999% or more amounts to claiming
you could make a million or a trillion statements with about one error, which no one can.
So no one should claim probability 1, even for 2 + 2 = 4; and, as the closing quotation
says, a probability of 1 could never be revised by any evidence.

## 2. Sources checked

- Yudkowsky, "Cognitive Biases Potentially Affecting Judgment of Global Risks", MIRI reprint,
  https://intelligence.org/files/CognitiveBiases.pdf (`data/sources/CognitiveBiases.txt`,
  already in the collection). Section 10, "Calibration and Overconfidence", quoting Slovic,
  Fischhoff and Lichtenstein (1982, 472) on Fischhoff, Slovic and Lichtenstein (1977):
  "people were asked to indicate the odds that they were correct in choosing the more frequent
  of two lethal events"; "Only 73% of the answers assigned odds of 100:1 were correct (instead
  of 99.1%)"; "For answers assigned odds of 1,000,000:1 or greater, accuracy was 90%". The same
  section has the chapter's own version of the rule: "I avoid discussing the research on
  calibration unless I have previously spoken of the confirmation bias".
- Stanford Encyclopedia of Philosophy, "Bayesian Epistemology" (first published 13 June 2022),
  https://plato.stanford.edu/entries/epistemology-bayesian/ (`data/sources/sep_epistemology_bayesian.txt`).
  Matched: "Probabilism is often thought to demand that one be logically omniscient, having
  credence 1 in every logical truth and credence 0 in every logical falsehood." and
  "Garber (1983) tries to do that for certain logical truths; Hacking (1967) and Talbott (2016),
  for all logical truths" (context: replacing probabilism by a norm "that permits credences less
  than 1 in logical truths").
- Wikipedia, "Knuth's up-arrow notation" (raw, `data/sources/wiki_Knuth_up-arrow.txt`):
  "3\uparrow\uparrow 3=3^{3^3}=3^{27}=7,625,597,484,987". 3↑↑↑3 = 3↑↑(3↑↑3), a tower of 3s of
  height 7,625,597,484,987 (standard definition; my derivation).
- Peter de Blanc's anecdote (footnote 2), https://web.archive.org/web/20090203013258/http://www.spaceandgames.com/?p=27:
  NOT reached. curl got "Connection reset by peer" twice (proxy log: web.archive.org
  ws_closed_mid_exchange); WebFetch refuses web.archive.org. The note says it could not be checked.

## 3. Arithmetic

- 16 h × 3600 s / 20 s = 2,880 statements a day; 1,000,000 / 2,880 = 347.2 days. "Around a
  solid year" holds.
- 99.9999999999% = 1 − 10^-12, so a trillion statements. 10^12 / 2,880 = 3.47 × 10^8 days =
  951,294 years; / 80 years = 11,891 lifetimes (9,513 at 100 years). The post says "a hundred
  human lifetimes": off by a factor of about 100. At a hundred lifetimes of 80 years
  (2.5 × 10^11 s), a trillion statements would need about 4 statements per second, nonstop.
  Given a note because the figure is off by far more than a fifth (STANDARDS 2.4); the error
  runs against the post's own point, and the note says so.
- Bayes's rule with P(A) = 1: P(E) = P(E|A)P(A) + P(E|¬A)P(¬A) = P(E|A), so
  P(A|E) = P(E|A)·1/P(E|A) = 1 for every E with P(E) > 0.
- Log odds of 90%: 10 log10 9 = 9.54 dB; of 1 − 1/N: about 10 log10 N dB, finite for any finite N.

## 4. Claims about other posts

- "Absolute Authority" (`data/originals/absolute-authority.md`, Posted: 2008-01-08).
  - The post's block quotation reorders that post: there, "You can have uncertain knowledge of
    relatively better and relatively worse options, and still choose. It should be routine, in
    fact, not something to get all dramatic about." comes BEFORE "I mean, yes, if you have to
    choose between two alternatives A and B ... It is not a *necessary* condition." The quote
    also drops "I mean, yes," and "not something to get all dramatic about". Meaning unchanged,
    so no note (STANDARDS 2.3 on "misquotes").
  - Matched for the note on the million statements: "if you say that something is 99.9999%
    probable, it means you think you could make *one million* equally strong independent
    statements, *one after the other*, over the course of a solid year or so".
  - Matched for the closing note: "For technical reasons of probability theory, if it's
    theoretically possible for you to change your mind about something, it can't have a
    probability exactly equal to one."
- "Knowing About Biases Can Hurt People" (`data/originals/knowing-about-biases-can-hurt-people.md`,
  Posted: 2007-04-04): "I now try to never mention calibration and overconfidence unless I have
  first talked about disconfirmation bias, motivated skepticism, sophisticated arguers, and
  dysrationalia in the mentally agile." Our notes on that post already criticize the rule
  (it changes only the order of warnings) and the "70%" figure; I made only a pointer here.
- "How to Convince Me That 2 + 2 = 3" (`data/originals/how-to-convince-me-that-2-2-3.md`,
  2007-09-27): the post's reference to it ("could be done using much the same sort of evidence")
  matches "What would convince me that 2 + 2 = 3, in other words, is exactly the same kind of
  evidence that currently convinces me that 2 + 2 = 4". No note needed.
- "0 And 1 Are Not Probabilities" (next day): the log-odds scale; the note on 3↑↑↑3 points there.

## 5. Not verified

- The de Blanc anecdote (archive unreachable).
- Rafal Smigrodski's quotation: source not given in the post; not searched.
- Hacking (1967) and Garber (1983) themselves: cited only as the SEP entry reports them.

## 6. Judgment calls for the editor

- The logical-omniscience note (cfact on "I could be misremembering it") is the main technical
  charge, and it is in the "In short" line. The fair-defender reply would be "I was describing a
  fallible human, not an ideal reasoner." The note does not say the post is wrong to take that
  side, only that it does not tell the reader that the standard theory requires probability 1
  for logical truths. I phrased the example as "that SS0 + SS0 = SSSS0 follows from the Peano
  axioms", which is a logical truth, rather than claiming "2 + 2 = 4" itself is one.
- Reserved-word flags: "about one of them wrong" (describes the calibration count, not a
  verdict); "could never be revised" (paraphrase of Smigrodski in the Summary). Both kept.
- The Response calls much of the post a restatement of "Absolute Authority". This rests on two
  matched passages (the million statements; the point about revising probability 1). The other
  agent annotating "Absolute Authority" in this batch may make the calibration point there; the
  editor may want one full treatment and a pointer.
- Structural note on paragraph 3 (2 + 2 = 4 announced, lightspeed discussed) is descriptive; the
  editor may cut it as a nitpick.
- Preview builds: `annotated/preview.sh posts infinite-certainty` OK.
