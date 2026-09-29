# Report: Zut Allais! (batch 5c, order 289)

## 1. The argument in three sentences

Answering commenters who defended the Allais preferences, the post argues from the
heuristics-and-biases literature that subjects defend incoherent preferences even when they are
silly (a recalled choice/pricing preference reversal, a money pump, and a transcript of a
Las Vegas subject who would not give up the pattern), and that people put an extra value on
certainty, which is exploitable because "one time's certainty is another time's probability."
It restates the Allais money pump, gives a framing example with the same distribution over
outcomes, and tells the reader to multiply utilities by probabilities, with a worked rule for
the Allais problem under a logarithmic utility of total assets. Against "the utility of
certainty" it says utilities are over outcomes, not probabilities; paying for a feeling of
certainty is human, but when lives or other things that matter are at stake, circular
preferences mean one is not steering the future, and one should follow the mathematics.

## 2. Sources checked

Files in `data/sources/5c_zut-allais/` unless stated.

- Kahneman and Tversky (1979), `../5c_the-allais-paradox/kt1979.txt`. Matched:
  - pp. 266-267: "Apparently, reducing the probability of winning from 1.0 to .25 has a greater effect
    than the reduction from .8 to .2."
  - p. 283, Zeckhauser: "Most people feel that they would be willing to pay much more for a
    reduction of the probability of death from 1/6 to zero than for a reduction from 4/6 to 3/6."
  - p. 273, Problems 11 and 12: given 1,000, A (1,000,.50) [16], B (500) [84]; given 2,000,
    C (-1,000,.50) [69], D (-500) [31]; "when viewed in terms of final states, the two choice
    problems are identical."
  - p. 284: "Lichtenstein and Slovic [27] have constructed pairs of prospects A and B, such that
    people generally prefer A over B, but bid more for B than for A. This phenomenon has been
    confirmed in several studies, with both hypothetical and real gambles, e.g., Grether and
    Plott [20]." and "We have not treated in detail the more complicated production task (e.g.,
    bidding)"; "Because prospect theory has been proposed as a model of choice". My note's "their
    theory treats choice, not bidding" paraphrases these.
  - p. 277: "These departures from expected utility theory must lead to normatively unacceptable
    consequences, such as inconsistencies, intransitivities, and violations of dominance."
- Humphrey and Kruse, "Who accepts Savage's axiom now?", Theory and Decision (2023),
  https://link.springer.com/article/10.1007/s11238-023-09938-8 (`../5c_the-allais-paradox/savage_now.txt`).
  Matched: "Violations of the axiom persisted as the modal pattern of behaviour."; "Nielsen and
  Rehbeck ( 2022 ) observe a systematic tendency for decision-makers who violated the sure-thing
  principle in lottery choices to correct those violations when given the opportunity.";
  abstract: "incentive-compatible choices of 147 subjects" and "violations of the sure-thing
  principle are robust to its normative justification"; "Although Slovic and Tversky’s result
  provides putative support for Allais’ view that violating the axiom is reasonable, the debate
  remains unresolved." Slovic and Tversky's procedure: "They were then presented with normative
  arguments favouring the counterfactual behaviour" (my "arguments favouring the choice they had
  not made").
- Berg, Dickhaut and Rietz, "Preference reversals: The impact of truth-revealing monetary
  incentives", Games and Economic Behavior (2010), accepted manuscript at
  https://www.biz.uiowa.edu/faculty/trietz/papers/prefrev.pdf (`seidl_prefrev.txt`; file name is
  a leftover, the paper is Berg et al.). Matched, abstract: "Lichtenstein and Slovic (1973) and
  Grether and Plott (1979) introduce incentives, but aggregate reversal rates change little." and
  "we find that incentives can generate more economically consistent behavior". Las Vegas study:
  "Lichtenstein and Slovic (1973) report two studies conducted at the Four Queens Hotel and Casino
  in Las Vegas. Subjects in the experiments purchased chips with their own money."
- Stanford Encyclopedia, "Normative Theories of Rational Choice: Expected Utility"
  (`../5c_one-life-against-the-world/sep_rationality-normative-utility.txt`): "Loomes and Sugden
  suggest that in addition to monetary amounts, the outcomes of the gambles include feelings of
  disappointment (or elation)"; "Weirich suggests that ... (for instance) $100 million as the
  result of a sure bet is more than $100 million from a gamble that might have paid nothing.";
  Broome: "Any preferences can be justified by re-describing the space of outcomes" and his
  constraint "A and B must differ in some way that justifies preferring one to the other."
- Tversky and Kahneman (1981), "The Framing of Decisions", Science 211 (`tk1981.txt`, copied from
  the Feeling Moral agent's folder `data/sources/5c_feeling-moral/tk1981.txt`, not edited there).
  Matched: Program A "200 people will be saved. [72 percent]"; Program D "213 [2/3] probability
  that 600 people will die. [78 percent]" (OCR renders 1/3 and 2/3 as 113 and 213).
- Not reachable: the Google Books page linked for the transcript (API quota, 429). The Lichtenstein
  and Slovic 1971 paper (Oregon repository returned an HTML page, not the PDF). Semantic Scholar
  and OpenAlex (429).

## 3. Arithmetic

Script `data/sources/5c_the-allais-paradox/check_allais.py` (output `check_allais_output.txt`).

- Recalled bets: EV(1) = 18/3 - 1.5 x 2/3 = 6 - 1 = 5.00; EV(2) = 0.95 x 4 - 0.05 x 0.25 = 3.8 -
  0.0125 = 3.7875.
- Transcript: 550 - 401 = 149, as the experimenter says.
- Framing: sure 400 against {500: 0.8, 300: 0.2}, EV 460; from 500, a sure loss of 100 gives 400,
  a 20% chance of losing 200 gives {500: 0.8, 300: 0.2}. Same distribution.
- Allais rule: 1A > 1B iff 34 U24 > 33 U27 + U0 iff (U24 - U0) > 33 (U27 - U24). Correct.
- Log utility of total assets W: EU(1A) = ln(W + 24,000); EU(1B) = (33/34) ln(W + 27,000) +
  (1/34) ln W.

  | W | EU(1A) | EU(1B) | choice |
  |---|---|---|---|
  | 100 | 10.0900 | 10.0425 | A |
  | 500 | 10.1064 | 10.1041 | A |
  | 600 | 10.1105 | 10.1130 | B |
  | 1,000 | 10.1266 | 10.1420 | B |
  | 24,000 | 10.7790 | 10.8174 | B |
  | 100,000 | 11.7280 | 11.7449 | B |

  Indifference (bisection) at W = 546. At W = 24,000: ln 2 = 0.693 against 33 ln(51/48) = 2.001,
  so the 33 units win. Case 2 at W = 24,000 gives B as well (10.3215 against 10.3346), as the
  post says the cases agree. So "If $24,000 would double your existing assets, pick A" does not
  follow from the post's own method; A needs assets under about $550 (a prize about 44 times
  one's assets).

## 4. Claims about other posts

- "Terminal Values and Instrumental Values" (`data/originals/terminal-values-and-instrumental-values.md`):
  "terminal values and instrumental values are separate and incompatible types" and
  "TYPE ERROR: No constructor found for Expected\_Utility -> Utility." My note says the post's
  answer "follows" that post; consistent.
- "The Allais Paradox" (previous day): my notes point to our notes there for the pump's
  arithmetic, Problem 10 and the resolute/sophisticated replies, and do not repeat them.
- "The Lens That Sees Its Flaws": linked by the post twice; my notes only name it.

## 5. Not verified

- The transcript (the post's Google Books link could not be opened). The post attributes it to a
  Las Vegas study with real money; the bracket in the transcript mentions points converted to
  dollars. Both Lichtenstein and Slovic 1971 (Experiment 3, points and a conversion curve) and the
  1973 Las Vegas study (chips) used such units, per Berg et al., so I could not tell which study it
  comes from. The note says it is unchecked and names the Las Vegas study only as the study the
  post describes.
- The two recalled preference-reversal bets: not found in Berg et al.'s data sets or elsewhere.
- The "100% to 99% versus 80% to 20%" experiment: not found. "I could not find a study that
  reports it" is the claim, not "no such study exists".
- Tversky and Kahneman (1992) weighting-function parameters were not reachable, so no
  weighting-function calculation is given.
- Omohundro's taxi example: not looked up (the post says "paraphrase").

## 6. Judgment calls for the editor

- No reserved words in my text.
- The log-utility note is a technical correction by derivation (table above). It stays out of
  the "In short" line, since the post's point (use expected utility; B for most people) survives,
  and the Response says so.
- Attribution note ("The cases come from Lichtenstein and Slovic rather than from prospect
  theory"): the post says "Anyone who knows a little prospect theory will have no trouble
  constructing cases". A fair defender could say "prospect theory" stood for the field. I kept it
  as credit, quoting Kahneman and Tversky's own statement.
- The certainty-experiment note and "In short" say the recalled result is "much stronger than any
  finding I could trace". The post hedges with "I believe"; the note keeps the hedge.
- The redescription note says the post does not discuss the non-feeling version (Weirich). This
  is scope in one sentence; the post does answer the feeling version, and the note says so.
- Persistence: I give the mixed evidence and the opposite reading as information; the post's own
  qualification ("Some subjects abandon them") is kept.
- Consistency with neighbours: Feeling Moral (next in book order, another agent) uses Tversky and
  Kahneman 1981; my note only reports its two percentages.
