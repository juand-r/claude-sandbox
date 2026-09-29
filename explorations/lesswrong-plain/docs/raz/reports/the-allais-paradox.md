# Report: The Allais Paradox (batch 5c, order 288)

## 1. The argument in three sentences

The post presents a modified Allais problem (1A: $24,000 for certain; 1B: 33/34 of $27,000;
2A: 34% of $24,000; 2B: 33% of $27,000), reports that most people prefer 1A and 2B, and shows
algebraically that no utility function over outcomes, whatever its shape, can give both
preferences under expected utility, since the 2s are the 1s played with probability 0.34.
It reports that Allais took his result as a flaw in the independence axiom rather than in human
judgment, and replies that intuitions expose facts about cognition, not directly about which
strategies are wise. Its argument that the pattern is costly is a money pump: in a two-stage
game an agent with both preferences pays a penny to switch from A to B before a die roll and a
penny to switch back after it, so "there is always a price for leaving the Bayesian Way."

## 2. Sources checked

Saved in `data/sources/5c_the-allais-paradox/` unless stated.

- Kahneman and Tversky (1979), "Prospect Theory", Econometrica 47 (`kt1979.txt`, copied from
  `data/sources/b2_lottery/kt1979.txt`, which is pdftotext of the paper). Matched:
  - p. 266: "the analysis of individual patterns of choice indicates that a majority of
    respondents (61 per cent) made the modal choice in both problems."
  - p. 266: "A simpler demonstration of the same phenomenon, involving only two-outcome gambles is
    given below. This example is also based on Allais [2]." Problem 3: A (4,000,.80) [20],
    B (3,000) [80]; Problem 4: C (4,000,.20) [65], D (3,000,.25) [35].
  - p. 271-272, Problem 10: "Of 141 subjects who answered Problem 10, 78 per cent chose the latter
    prospect, contrary to the modal preference in Problem 4. Evidently, people ignored the first
    stage of the game, whose outcomes are shared by both prospects".
  - Abstract: "Overweighting of low probabilities may contribute to the attractiveness of both
    insurance and gambling."
- Stanford Encyclopedia, "Normative Theories of Rational Choice: Expected Utility",
  https://plato.stanford.edu/entries/rationality-normative-utility/
  (`../5c_one-life-against-the-world/sep_rationality-normative-utility.txt`, lines 1150-1380).
  Matched: Allais lotteries A-D (89% common consequence, tickets 12-100); "This incompatibility
  does not require any assumptions about the relative utilities of the $0, the $100 million, and
  the $500 million."; "one might follow Savage (101 ff) and Raiffa (1968, 80–86), and defend
  expected utility theory on the grounds that the Allais and Ellsberg preferences are
  irrational."; "one might follow Buchak (2013) and claim that that the Allais and Ellsberg
  preferences are rationally permissible"; "but other, “risk-averse” settings rationalise the
  Allais preferences."
- Stanford Encyclopedia, "Decision Theory", https://plato.stanford.edu/entries/decision-theory/
  (`../5c_one-life-against-the-world/sep_decision-theory.txt`, lines 2470-2600). Matched:
  "Defenders of resolute choice typically defend decision theories and associated preferences
  that violate the Independence axiom/Sure-Thing Principle (notably McClennen 1990 and Machina
  1989"; "Hammond shows that only a fully Bayesian agent can plan to pursue any path in a
  sequential decision tree that is deemed optimal at the initial choice node."; "(notably,
  Machina 1989 and McClennen 1990) ... They reject the assumption of sophisticated choice
  underpinning the dynamic consistency arguments."; "those who defend theories that violate the
  Independence axiom but retain the Completeness and Transitivity (i.e., Ordering) axioms of EU
  theory". The note quotes only "resolute choice".
- Cailloux and Destercke, "Reasons and Means to Model Preferences as Incomplete", arXiv
  1801.01657 (2018), `../5c_zut-allais/arxiv_1801.01657.txt` line 314 f.: "When thinking more
  about the comparison and presented with different views of the same problem, individuals may
  in some cases change their preference. ... Savage [1972, pp. 101–103] famously reported that it
  happened to him." With the SEP line above, this supports "argued that the Allais preferences are
  irrational, and reported that he had first held them himself and changed his mind." Savage's
  book itself could not be read (archive.org lending copy, 401).
- Allais and Hagen (eds.), Expected Utility Hypotheses and the Allais Paradox (1979), Springer
  pages (`allais_hagen_book.txt`, `allais_hagen_book_p2.txt`, `allais1979_chapter.txt`):
  chapter "The So-Called Allais Paradox and Rational Decisions under Uncertainty", Maurice Allais,
  "Pages 437-681" (245 pages); summary: "The present memoir constitutes an extension of my 1952
  study, The Foundations of a Positive Theory of Choice Involving Risk and a Criticism of the
  Postulates and Axioms of the American School (see Part II of this Volume), completing it and
  adding further comments in the light of the criticisms addressed to it".
- Wikipedia, "Allais paradox" (raw, `wp_Allais_paradox.txt`): alternatives "[[prospect theory]]
  ... [[weighted utility]] (Chew), [[rank-dependent expected utility]] by [[John Quiggin]], and
  [[Regret (decision theory)|regret theory]]"; first presented in 1952 at a Paris conference.
  Used for Quiggin's name only.

## 3. Arithmetic

Script: `data/sources/5c_the-allais-paradox/check_allais.py`, output in
`check_allais_output.txt` (run with `.venv/bin/python`).

- 0.34 x 1 = 0.34 (2A); 0.34 x 33/34 = 0.33 (2B); 0.34 x 1/34 + 0.66 = 0.67. Exact (fractions).
- Inconsistency: from U24 > (33/34) U27 + (1/34) U0, multiply by 0.34 and add 0.66 U0:
  0.34 U24 + 0.66 U0 > 0.33 U27 + 0.67 U0, the reverse of the second inequality. Also checked by
  200,000 random utility triples: none satisfies both.
- Expected values: 1B = 33/34 x 27,000 = 26,205.88; 2A = 0.34 x 24,000 = 8,160;
  2B = 0.33 x 27,000 = 8,910.
- Money pump: P(die <= 34) = 0.34; "The die comes up 12" continues the game.
- "one-third": 0.34 against 0.333; the post's next sentence gives 34%, so no note beyond a clause.
- Sophisticated/resolute agent: my derivation from the SEP descriptions. Sophisticated: knows it
  will switch to A at 12:05 (prefers 1A), so a first penny buys nothing; keeps A; pays 0; ends
  with 2A. Resolute: pays once to switch to B, keeps B; pays 1. Hence "at most one penny".

## 4. Claims about other posts

- "But There's Still A Chance, Right?": our afterword there says "Something close to it, that
  people treat a tiny chance and no chance as different in kind, was part of Kahneman and
  Tversky's prospect theory in 1979, where decision weights change abruptly near zero and help
  explain gambling." My note says those notes "make the same point".
- "Ends: An Introduction": our note there already says "The book gives it later: ``The Allais
  Paradox'' argues that the subjects of those experiments ``can't have a consistent utility
  function over outcomes.''" Consistent with my notes (I say this is true of expected utility).
- "Beautiful Probability": our notes there discuss Dutch books for degrees of belief. My notes
  do not repeat them; the money pump here concerns preferences over gambles.
- Zut Allais! (posted 2008-01-20, the day after this post, 2008-01-19) is not cited here. Its
  notes point back to these notes for the dynamic-choice debate and Problem 10 (STANDARDS 2.5).

## 5. Not verified

- Allais (1953) itself (French, JSTOR). Allais's position is taken from the SEP, K&T and his 1979
  chapter summary.
- Savage (1954), pp. 101-103: via the SEP and Cailloux and Destercke only.
- Hammond, Machina, McClennen, Buchak, Quiggin: via the SEP and Wikipedia only.
- The post's exact numbers (24,000/27,000, 33/34) were not tested in any study I found; the note
  gives K&T's analogous figures.

## 6. Judgment calls for the editor

- No reserved words remain in my text (one "backwards" was reworded).
- The "consistent" clogic: says the claim is true of expected utility and that independence-
  violating theories keep a consistent ranking. The post itself puts "consistent" in quotation
  marks; I mention that, so the note should pass test 6 (term read in the post's sense).
- The Problem 10 note ("most subjects did not show the preference for B before the roll that the
  pump assumes"): information, not a refutation; the pump is stated for an agent who has both
  preferences. It appears in the Response as "a complication". Check it is not read as a fault.
- The resolute/sophisticated note includes my own one-line application ("Either way the agent
  pays at most one penny"). It follows directly from the SEP's descriptions, but it is my
  derivation.
- The "Initially" note: the 1979 chapter summary supports that Allais still held the view then; I
  do not claim he never changed it.
- "In short" says the verdict "is Savage's side of a dispute with Allais that the money pump, as
  described, does not settle." "Does not settle" rests on the SEP account that Hammond's argument
  is disputed by Machina and McClennen.
- Pronouns: he/his for Allais and Savage (well-documented historical figures).
