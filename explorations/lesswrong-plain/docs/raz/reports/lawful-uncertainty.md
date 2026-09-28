# Report: lawful-uncertainty

## 1. The argument in three sentences

In a probability-learning experiment described by Dawes, subjects asked to predict cards
that are 70% blue predict blue only about 70 to 76% of the time, which yields fewer correct
guesses than always predicting blue; they could have tested their pattern hypotheses
privately while still betting blue. The author suspects the all-blue strategy simply did not
occur to them, because people expect the best strategy to resemble the random sequence, and
it is a counterintuitive idea that one should act lawfully under uncertainty. Randomizing
one's actions only takes one further from the target, so "fighting chaos with chaos" is why
there are few rationalists, and every departure from lawful thinking, like every bet on red,
is an expected loss.

## 2. Sources checked

Saved texts are in `data/sources/` (listed per item).

- Tversky and Edwards (1966), "Information versus reward in binary choices", J. Exp. Psychol.
  71(5): 680-683, doi 10.1037/h0023123. NOT READ. PubMed (efetch, PMID 5939707) has no
  abstract; Semantic Scholar says the abstract is elided by the publisher; OpenAlex has none;
  PsycNET and ResearchGate blocked the request. So the 76%, the nickel, the thousand trials and
  the 70/30 split are unchecked against the primary source.
- Dawes, Rational Choice in an Uncertain World (1988). NOT READ. archive.org item
  `rationalchoicein00dawe` exists but its text is lending-restricted (401 on the djvu text;
  "Item not available" from the inside-book search). A web search for the exact phrase
  "cannot bring themselves to believe that the situation is one in which they cannot predict"
  found only unrelated pages. The quotation is unchecked.
- Juni, Gureckis and Maloney, "Information sampling behavior with explicit sampling costs",
  Decision (in press version, advance online publication; year not printed on the PDF).
  https://people.psych.ucsb.edu/juni/mordechai/papers/JuniGureckisMaloney-Decision-InPress.pdf
  (`data/sources/juni_gureckis_maloney.pdf`, `.txt`, lines 62-74). Matched: "Tversky &
  Edwards (1966), for example, had participants perform a probability-learning task. On each
  of 1000 trials, participants had to guess which of two mutually exclusive alternatives would
  occur. Although participants were rewarded at the end of the experiment for all of their
  correct guesses, they received no feedback following each guess. To gain information about
  the relative frequencies of the mutually exclusive alternatives, participants could forgo
  guessing on any particular trial and observe the outcome instead. They forfeited any possible
  reward on trials that they chose to observe which event would occur instead of guessing."
  Also: "observing around 300 trials spread out throughout the experiment".
- Shanks, Tunney and McCarthy (2002), J. Behav. Dec. Making 15: 233-250.
  http://www.cs.ucl.ac.uk/fileadmin/sec/publications/Shanks_Tunney_McCarthy_A_re-examination_of_probability_matching_and_rational_choice_Journal_of_behavioral_decision_making2002.pdf
  (`data/sources/shanks2002.pdf`, `.txt`). Matched: "In Edwards' (1961) study, for instance,
  participants' asymptotic choice probability for a response that had a payoff probability of
  0.7 was 0.83." and (General Discussion) "large proportions of participants (71% ± 18% across
  Experiment 2 and the Payoff + Feedback group of Experiment 3) can maximize their payoffs when
  maximizing is defined as a run of at least 50 consecutive choices of the optimal response."
  (pdftotext renders ± as a blank and + as "þ"; the note writes $\pm$ and elides the middle
  with \ldots.) Also abstract: "(i) large financial incentives, (ii) meaningful and regular
  feedback, and (iii) extensive training".
- Vulkan (2000), "An economist's perspective on probability matching", J. Econ. Surveys
  (`data/sources/vulkan2000.pdf`, `.txt`), https://worthylab.org/wp-content/uploads/2020/12/vulcan_2000_probabilitymatching.pdf.
  Table 1 row "Edwards (61) 10 1000 ... 0.70 0.83" confirms the Shanks figure; not quoted in
  the notes.
- Koehler and James (2010), "Probability matching and strategy availability", Memory &
  Cognition 38(6): 667-676, abstract via PubMed efetch PMID 20852231
  (`data/sources/koehler_james_abstracts.txt`). Matched: "the majority of participants endorse
  maximizing as superior to matching in a direct comparison when both strategies are
  described" and "when the maximizing strategy is brought to their attention, more
  participants subsequently engage in maximizing".
- "The Weighted Majority Algorithm", Yudkowsky, postedAt 2008-11-12T23:19:58Z, id
  AAqTP6Q5aeWnoAYr4, fetched through the LessWrong GraphQL API
  (`data/sources/the-weighted-majority-algorithm.md`). Matched: "For example, you are playing
  rock-paper-scissors against an opponent who is *smarter than you are*, and who knows exactly
  how you will be making your choices.  In this condition it is wise to choose randomly,
  because any method your opponent can predict will do worse-than-average."
- "Worse Than Random", postedAt 2008-11-11T19:01:31Z, id GYuKqAL95eaWTDje5
  (`data/sources/worse-than-random.md`): "(There are exceptions to this rule, but they have to
  do with defeating cryptographic adversaries ...)". Not quoted in the notes; it supports "the
  author gave the exception" but I cited only the clearer later post.
- Neither follow-up is in `data/manifests/rationality_az.json` (grep count 0).

## 3. Arithmetic

- Matching: 0.70 x 0.70 + 0.30 x 0.30 = 0.49 + 0.09 = 0.58. Correct.
- At the reported 76% blue: 0.76 x 0.70 + 0.24 x 0.30 = 0.532 + 0.072 = 0.604, "about 60%".
- "30% stupid": if f is the share of red bets, accuracy = 0.70(1 - f) + 0.30 f = 0.70 - 0.40 f.
  f = 0: 70%; f = 1: 30%; f = 0.3: 58%. (0.70 - 0.58) / (0.70 - 0.30) = 0.12 / 0.40 = 0.30,
  so betting red 30% of the time is 30% of the way from best to worst. The post's figure holds.
- Dates: Lawful Uncertainty 2008-11-10, Weighted Majority 2008-11-12: two days.
- "three paragraphs later": randomizing paragraph, then "It is a counterintuitive idea ...
  think lawfully", "And so there are not many rationalists", "You have heard the unenlightened
  ones" (the third). Counted.
- "three sentences that each begin 'It is a counterintuitive idea'": counted, three.

## 4. Claims about other posts

- The Weighted Majority Algorithm (see section 2). Not in this book.
- No neighbour note in the collection discusses this post.

## 5. Items not verified

- Tversky and Edwards (1966): design, 76%, nickel, thousand trials, 70/30. Needs the paper
  (APA PsycARTICLES).
- Dawes's text, including "Despite feedback through a thousand trials, subjects cannot bring
  themselves to believe ...". Needs the book (1988 or the 2001/2010 Hastie and Dawes edition).
- Whether Dawes's "cards" example is the Tversky-Edwards apparatus: Juni et al. say only "two
  mutually exclusive alternatives"; Vulkan says lights were the usual apparatus. I made no note.
- Schul and Mayo (2003): not read; no note relies on it.

## 6. Judgment calls for the editor

1. The Juni et al. note (\cfact after Dawes's feedback sentence) rests on one secondary summary
   of a paper I could not read. It is hedged ("One later summary ... If that summary is right")
   and repeated, hedged, in the Response and one n.b. If the editor thinks one secondary
   source is too thin, cut it from all three places; the rest does not depend on it. It matters
   because the post's paragraph on private testing, and "hundreds of earlier guesses had been
   disconfirmed", assume per-trial feedback.
2. The randomizing note cites a post outside the book (Weighted Majority Algorithm). Fair
   defender 5 ("I answer that later") does not apply inside this post; the exception is stated
   only in later posts. Reserved words: none.
3. "And so there are not many rationalists" note: says the behaviour "gives way to practice and
   pay", using Edwards 1961 and Shanks 2002. Fair defender: the post's claim is about "most who
   perceive a chaotic world", not only the lab task. The note attacks only the evidence offered.
4. Credit given twice (the private-testing reasoning is "sound"; the suspicion is supported by
   Koehler and James). I think both are needed for accuracy (STANDARDS 2.1).
5. "is asserted, not argued" for "the most important idea in all of rationality": I searched
   the post; nothing argues the ranking. The last paragraph's "every departure from the Way"
   generalizes but does not compare with other ideas.
6. The flagged "wrong" ("their guesses were not shown to be wrong") and "never" ("never red")
   are descriptive, not verdicts.
7. Afterword Response words 379 (audit) / 369 (raz_check); both within range.
