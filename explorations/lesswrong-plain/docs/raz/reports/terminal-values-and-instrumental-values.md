# Report: terminal-values-and-instrumental-values

## 1. The argument in three sentences

People handle means and ends well in daily planning but confuse them when they talk about
goals abstractly, and English does not keep the two apart. A simple expected-utility model
(outcomes, actions, a utility over outcomes, a probability of each outcome given each
action) separates them as two types: utility belongs to outcomes and stands for terminal
values, expected utility belongs to actions, and instrumental values reappear only as
shortcuts through the causal structure that the probability function hides, so they
depend entirely on beliefs of fact. With this in hand, the selfish philosopher's "she
valued that choice" is a type error, instrumental values should be dropped where their
regularity fails, and moral disputes should be sorted into factual disputes about means
and genuine disputes about terminal values, a sorting the human brain does badly.

## 2. Sources checked

All saved in `data/sources/b3a_values/` (HTML plus a tag-stripped `.txt`).

- Robin Hanson, "Expert At Versus Expert On", Overcoming Bias, 23 April 2007 (the post's
  link), curl of http://www.overcomingbias.com/2007/04/expert_at_versu.html
  (`ob_expert_at.txt`). Matched: "A prosperous and successful plumber is an expert at
  plumbing.  Someone who is a good source for accurate information on plumbing is an expert
  on plumbing."
- SEP, "Intrinsic vs. Extrinsic Value" (substantive revision 2 June 2025),
  https://plato.stanford.edu/entries/value-intrinsic-extrinsic/ (`sep_value-intrinsic-extrinsic.txt`).
  Matched: "(cf. Aristotle, Nicomachean Ethics, 1094a). That which is intrinsically good is
  nonderivatively good; it is good for its own sake." and, for "final value", "She contends
  that 'instrumental value' is to be contrasted with 'final value,' that is, the value that
  something has as an end or for its own sake" (Korsgaard 1983).
- Wikipedia, "Strategy (game theory)", `?action=raw` (`wiki_strategy.txt`). Matched: "A
  '''pure strategy''' provides a complete and deterministic plan for how a player will act
  in every possible situation in a game. It specifies exactly what action the player will
  take at each decision point, given any information they may have." Also SEP "Decision
  Theory" section 6 (`sep_decision-theory.txt`): in the tree form, "Some of these branches
  lead to further choice points, often after the resolution of some uncertainty due to new
  evidence."
- SEP, "Egoism" (substantive revision 9 January 2023), already in `data/sources/sep_egoism.txt`
  (fetched by an earlier agent; I re-read the section). Matched: "Say a soldier throws himself
  on a grenade to prevent others from being killed."; "Perhaps he threw himself on the grenade
  because he believed that he could not bear to live with himself afterwards if he did not do
  so."; "If self-interest is identified with the satisfaction of all of one's preferences,
  then all intentional action is self-interested ... Psychological egoism turns out to be
  trivially true."; Batson: "He found that the altruistic hypothesis always made superior
  predictions."
- SEP, "Decision Theory" (substantive revision 20 August 2025),
  https://plato.stanford.edu/entries/decision-theory/ (`sep_decision-theory.txt`). Matched:
  "For starters, the character of an act may feature as a property of all its possible
  outcomes."
- Joel Spolsky, "The Law of Leaky Abstractions", 11 November 2002,
  https://www.joelonsoftware.com/2002/11/11/the-law-of-leaky-abstractions/ (`spolsky_leaky.txt`).
  Matched: "This is what I call a leaky abstraction." and "All non-trivial abstractions, to
  some degree, are leaky."
- SEP, "Charles Leslie Stevenson" (substantive revision 2 July 2021),
  https://plato.stanford.edu/entries/stevenson/ (`sep_stevenson.txt`). Matched: "Interpersonal
  disagreement is of two broad kinds: disagreement in belief and disagreement in attitude."
  (organizing Ethics and Language, 1944) and the quoted Stevenson passage "Like any typical
  ethical argument, then, this argument involves both disagreement in attitude and
  disagreement in belief. (1948b, 4)". Note: the "involves both" words are from Stevenson
  1948b as quoted by SEP; the note gives 1944 for the book in which the distinction is drawn,
  and does not date the quotation. The editor may prefer to add "(1948)".
- WHO fact sheet "Female genital mutilation",
  https://www.who.int/news-room/fact-sheets/detail/female-genital-mutilation, fetched
  28 September 2026 (`who_fgm.txt`). Matched: "FGM is often considered a necessary part of
  raising a girl, and a way to prepare her for adulthood and marriage. This can include
  controlling her sexuality to promote premarital virginity and marital fidelity." and "Some
  people believe that the practice has religious support, although no religious scripts
  prescribe the practice."

## 3. Arithmetic

- EU(administer) = 1 x 0.9 + 0 x 0.1 = 0.9; EU(don't) = 1 x 0.3 + 0 x 0.7 = 0.3. Both
  distributions sum to 1 (0.9 + 0.1; 0.3 + 0.7). Correct as printed.
- Sequences versus strategies. With n possible acts at each of k steps, there are n^k fixed
  sequences. If before each step after the first the agent observes one of m possible
  signals, a strategy assigns an act to every possible observation history: 1 + m + m^2 + ...
  + m^(k-1) = (m^k - 1)/(m - 1) decision points, so n^((m^k - 1)/(m - 1)) strategies, which is
  larger than n^k whenever m >= 2 and k >= 2. Example from the post: k = 2 (drive, then buy
  or order pizza), m = 2 (radio says the chocolate is gone or not). A fixed sequence
  "drive, then buy" cannot turn back when the news comes; the strategy "if the radio reports
  the earthquake, order pizza; otherwise drive" can, and has higher expected utility whenever
  the news has positive probability and changes the best act. The note says only "more
  strategies than sequences, so the space is larger still".
- "a term in the utility function": if U(outcome) = sum_i u_i(feature_i) (additive
  separability), then the contribution of C is u_C(C), fixed. For a general U, the
  difference U(C, rest) - U(not C, rest) can vary with "rest". Example: U = 1 if the sister
  lives and the Earth survives, 0 otherwise; then the sister's survival adds 1 if the Earth
  survives and 0 if not. No fixed "term" for her life exists.

## 4. Claims about other posts

- "Thou Art Godshatter" (`data/originals/thou-art-godshatter.md`, Posted 2007-11-13; this post
  2007-11-15, so "two days earlier"). Matched: "So long as the organism knows *this very
  fact*, and has a utility function that values reproduction, it will automatically eat."
  and the closing "Being a thousand shards of desire isn't always fun, but at least it's not
  *boring*." Our Godshatter notes (another agent, in progress) describe the food point as an
  answer to one objection; no conflict.
- "Are Your Enemies Innately Evil?" named only as the target of the post's link.
- "Leaky Generalizations" (next in book order) relies on the "a term" assumption; its notes
  point back to this post.

## 5. Items not verified

- Batson's experiments: from SEP's summary only.
- Aristotle, Korsgaard, Stevenson: from SEP only (secondary; cited as such in the notes).
- The Wikipedia source for "strategy" is secondary; the derivation above is the real support.

## 6. Judgment calls for the editor

1. The sequence note (clogic on "letting each Action stand for a whole sequence") is the
   formal correction I was asked to look for. A fair defender could say the post meant
   open-loop plans only; but the post's own opening plan changes on news received mid-way,
   and the fix (strategies) is standard. Worded as "works only when", not "wrong".
2. The egoism clogic ("The type error fits one reading of these words"). It rests on SEP
   (the egoist's guilt reply; outcomes can include facts about the act). The post's own
   argument against the simple egoist ("rather unlikely to sacrifice") is left intact.
   Check that this does not read as my own speculative objection; I think SEP makes it a
   standard one.
3. The separability clogic ("A term assumes more than the model states"). Mathematically
   certain (see section 3). Its importance is mainly for Leaky Generalizations; in this post
   alone it may look like a nitpick. Consider moving it there if the editor prefers.
4. Credit notes: Aristotle/final value (cpara on "In particularly"), Stevenson (cpara on
   "In moral arguments"), SEP triviality objection (cpara on "The choices of our simple
   decision system"). All given as information or support, not as faults; the post claims
   no novelty for the distinction.
5. The circumcision clogic: WHO's reasons partly support the post (values like premarital
   virginity) and partly show factual beliefs. I kept it balanced; the editor may judge it
   unnecessary.
6. Considered and dropped: (a) the formula uses P(O|A), which is Jeffrey's (evidential)
   form; causal decision theorists would write the probability of O under the intervention
   A. It matters only in Newcomb-type problems, and the post calls the model a sketch, so
   I made no note. (b) In Jeffrey's decision theory, acts and outcomes are both propositions
   with values on one scale, so the "type" separation is a feature of this formalization,
   not of decision theory generally; I judged this a nitpick, since the post says "our
   simple formalism". (c) The typo "In particularly" and the missing period after "happy".
7. Reserved words: none used as verdicts. "invented" was changed to "hypothetical" for the
   philosopher.
8. Honest section: 902 words by raz_check, at the ~900 allowed for this long post. Overfull boxes: annotated 0.38pt; honest none after a rewording.
