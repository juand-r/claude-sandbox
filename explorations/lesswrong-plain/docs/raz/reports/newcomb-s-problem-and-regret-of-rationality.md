# Report: Newcomb's Problem and Regret of Rationality (order 296, batch 5c)

## 1. The argument in three sentences

The post states Newcomb's problem, grants that the dominant view in decision theory
(causal decision theory) says to take both boxes, and declines to present the author's own
alternative theory, offering instead the "motivations" behind it. Its main motivation is
that "Rational agents should WIN": since Omega rewards only the predicted choice, not any
particular way of reasoning, an agent who envies another's mere choice (as Joyce's Rachel
wishes she were Irene's type) should simply make that choice, and a definition of "reasonable"
that predictably leaves the money on the table should be revised. The author therefore uses
"rational" to mean whatever wins (currently Bayesian reasoning), and says a method that
systematically loses must be discarded, while admitting this is "not a knockdown criticism
of causal decision theory".

## 2. Sources checked

All fetched texts are in `data/sources/5c_newcomb/` (not committed).

| Claim / quotation in our text | Source | Exact words matched |
|---|---|---|
| "The most common objection to causal decision theory is that it yields the wrong choice in Newcomb's problem." | SEP "Causal Decision Theory" (Paul Weirich, rev. 24 Oct 2024), https://plato.stanford.edu/entries/decision-causal/ (`sep_cdt.txt` l. 455) | same words (curly apostrophe) |
| Nozick 1969 first published it, named after physicist William Newcomb | SEP §2.1 | "Robert Nozick (1969) presented a dilemma ... Nozick called the example Newcomb's Problem after the physicist, William Newcomb, who first formulated the problem." |
| "psychological twins", "a sign, but not a cause", Gibbard-Harper 1978 and Lewis 1979 on PD | SEP §2.1 | "Allan Gibbard and William Harper (1978: Sec. 12) and David Lewis (1979) observe that a Prisoner's Dilemma with psychological twins ... poses a Newcomb problem for each player ... Acting cooperatively is a sign, but not a cause, of the other player's acting cooperatively." |
| Lewis 1979 title | SEP bibliography ("Prisoner's Dilemma is a Newcomb Problem"); PhilPapers and the andrewmbailey.com PDF list it as "Prisoners' Dilemma Is a Newcomb Problem" (search results only) | I used the latter spelling |
| EDT recommends one box | SEP §2.1 | "using conditional probabilities to compute expected utilities, one-boxing's expected utility exceeds two-boxing's expected utility." Jeffrey 1965 from SEP §2.4 and Lewis |
| "may conclude that cultivating a disposition to one-box is rational although one-boxing itself is irrational." | SEP §2.5 | verbatim (spans line breaks) |
| "One-boxing is irrational even if one-boxers prosper." | SEP §2.5 | verbatim |
| "The reason why we are not rich is that the riches were reserved for the irrational." ; "When we made our choices, there were no millions to be had." ; "Their decision theory is that of Jeffrey" ; "that one-boxers may consistently deny" ; "So it's a standoff." | Lewis, "'Why Ain'cha Rich?'", Noûs 15 (1981) 377-380, https://andrewmbailey.com/dkl/Why_Aincha_Rich.pdf (`lewis_wacr.txt`) | all verbatim; "one more piece of two-boxist doctrine that one-boxers may consistently deny" is alternative (1), which Lewis says "appears to be correct" |
| Gibbard and Harper: "rewards predicted irrationality richly" | quoted by Lewis in the same paper: "if someone is very good at predicting behavior and rewards predicted irrationality richly, then irrationality will be richly rewarded." | Could not open Gibbard and Harper directly (Springer paywall, Kellogg PDF removed); quoted through Lewis |
| "commends an irrational policy of managing the news so as to get good news about matters which you have no control over." | Lewis, "Causal Decision Theory", AJP 59 (1981), https://andrewmbailey.com/dkl/Causal_Decision_Theory.pdf (`lewis1981_cdt.txt` l. 23-25) | verbatim ("It commends an irrational policy of managing the news so as to get good news about matters which you have no control over.") |
| PhilPapers 2009: two boxes 31.4%, one box 21.3%, other 47.4%, n=931 | https://philpapers.org/surveys/results.pl (`pp2009.txt`) | "Other 441 / 931 (47.4%) Accept or lean toward: two boxes 292 / 931 (31.4%) Accept or lean toward: one box 198 / 931 (21.3%)" |
| PhilPapers 2020: one box 31.2%, two boxes 39.0% | Bourget and Chalmers, "Philosophers on Philosophy: The 2020 PhilPapers Survey", Philosophers' Imprint 2023, https://journals.publishing.umich.edu/phimp/article/id/2109/print/ Table 1 (`pp2020_paper.txt`) | "Newcomb's problem One box 334 31.2 Two boxes 418 39.0 Other 323 30.2". Matches the figure in our notes on What Do We Mean By "Rationality"? (order 8) |
| 2020 decision theorists: one box 22.7% vs 46.1% | same paper, Table 26 | "Decision Theory Newcomb's problem: one box 22.7 46.1 −23.4 *"; header: "Column S is the percentage of non-'other' answers among specialists (inclusive of combination answers). NS is the percentage of non-'other' answers among non-specialists." Text: "Newcomb's problem (decision theorists favor two-boxing)" |
| Campbell and Sowden (1985) reprints Nozick 1969 | Search results: De Gruyter chapter "6 Newcomb's Problem and Two Principles of Choice*" under DOI 10.59962/9780774857154 (the UBC Press ISBN of the volume, as on utpdistribution.com); another search summary gave pp. 107-133 | Table of contents seen only in search results; De Gruyter and UTP pages refused direct fetch (403/405) |
| TDT 2010 | https://intelligence.org/files/TDT.pdf (`tdt.pdf`) | "Yudkowsky, Eliezer. 2010. Timeless Decision Theory. The Singularity Institute, San Francisco, CA." Abstract: "return the one-box answer for Newcomb's Problem" |
| FDT 2017 | arXiv:1710.05060 abstract (`fdt_abstract.txt`) | authors Yudkowsky, Soares; "Submitted on 13 Oct 2017"; "achieve more utility than CDT on Newcomb's problem" |
| Musashi second quotation (Water Book) | https://www.26reads.com/library/23369-the-book-of-five-rings/3 (`musashi_water.txt`) | the post's four sentences match verbatim; the next sentence is "More than anything, you must be thinking of carrying your movement through to cutting him." |
| Musashi first quotation = same as in Something to Protect | `data/originals/something-to-protect.md` l. 80-83 | same words |

## 3. Arithmetic recomputed

Script: `data/sources/5c_newcomb/newcomb_check.py` (output reproduced from a run).

- Dominance table in the dialogue: B full, two boxes 1,001,000 vs one box 1,000,000; B empty, 1,000 vs 0. Difference 1,000 in both states. The post's figures are right.
- Evidential expected value with predictor accuracy p: one box pM, two boxes A + (1-p)M. Break-even p = (M+A)/(2M) = 1001/2000 = 0.5005. With the rule of succession after 100/100, p = 101/102 = 0.990: EV one box 990,196, two boxes 10,804. Not used in a note; context only.
- Causal expected value with credence q that B is full: two boxes minus one box = 1,000 for every q.
- Serum example (assuming the two serums act independently, which the post does not say; untreated survival 10%): B full, one box 0.955, two boxes 0.964; B empty, 0.100 vs 0.280. Two boxes at least as good in each state. With accuracy 0.99: one box 0.946, two boxes 0.287. Asteroid: B full, 1.00 vs 1.00; B empty, 0.00 vs 0.10. Basis for "whatever box B holds, taking both boxes is at least as good."
- Unbounded utility. The stated preference, for every finite N: 0.8 u(forever) + 0.000001 u(googolplex) >= 0.800001 u(N) (rest of the probability the same). Counterexample with bounded u: u(N) = 1 - 1/(N+1), u(forever) = 2: left side >= 1.6 > 0.800001 > right side for every N. With continuity, u(forever) = lim u(N) = S and u(googolplex) < S, the threshold (0.8 S + 0.000001 u(G))/0.800001 is strictly below S, so some finite N violates the preference; the inference then holds. So the claim needs the continuity premise (and u(googolplex) below the limit).

## 4. Claims about other posts

- "Something to Protect" (`data/originals/something-to-protect.md`, Posted 2008-01-30): same Musashi passage, lines 80-83. The post's link "something you could not leave behind" points to it. Our notes on it (order 294) treat the daughter dilemma with Rottenstreich and Hsee; I do not repeat that point here (the serum example raises stakes, it does not turn on probability sensitivity).
- "Trust in Bayes" (fetched with src/fetch.py post BL9DuE2iTCkrnuYzx, `data/originals/trust-in-bayes.md`, Posted 2008-01-29; not in the book manifest): "a paper, 'An Air-Tight Dutch Book' by Vann McGee, which purports to show that if your utility function is not bounded, then a dutch book can be constructed against you." Matches the post's description.
- "What Do We Mean By 'Rationality'?" (order 8, Posted 2009-03-16): our notes there already give the 2020 PhilPapers figures (39.0 vs 31.2) and Nozick's "divide almost evenly" (via Holt). STANDARDS 2.5: I point back for the 2020 figure and add only the 2009 figures and the decision-theorist breakdown, which bear on this post's own claim ("dominant consensus in modern decision theory"). That essay's notes fault it for presenting one-boxing as uncontested; this post, by contrast, says openly that two-boxing is the majority view, and my note credits that. The "reasonable belief vs true belief" rule appears in both; I point back.
- The True Prisoner's Dilemma (281), Replace the Symbol with the Substance (170), High Challenge, Science Isn't Strict Enough, Many Worlds One Best Guess, Zombies! Zombies? link to this post; none of their notes makes a claim about its content that my notes contradict. The replace-the-symbol report says the Newcomb post "replaces 'reasonable' with 'winning'"; consistent.
- review_log.md: no earlier full treatment of Lewis, Gibbard-Harper, Joyce or evidential decision theory; this is the first in book order, so the points are made in full here.

## 5. Not verified

- Joyce, The Foundations of Causal Decision Theory (1999), pp. ~152-154: the post's long quotation could not be checked (no accessible text; Google Books API quota exhausted). My notes quote only words that appear in the post's quotation, and say the check was not possible.
- Gibbard and Harper (1978) directly: quoted only through Lewis 1981.
- Nozick 1969 directly: not reachable (UBC PDF gone, Springer paywall). I rely on SEP for its date and naming.
- The linked CiteSeerX "PhD thesis" (doi 10.1.1.121.724): CiteSeerX connection reset; could not identify it. No note depends on it.
- Contents of Campbell and Sowden (1985): from search result listings only.
- The 2020 figure pages on survey2020.philpeople.org are behind a JavaScript challenge; used the published paper instead.

## 6. Judgment calls for the editor

1. Note on "This is a sufficient condition to imply that my utility function is unbounded" (\clogic): says the inference needs a continuity premise, with a bounded counterexample. The math is shown in section 3. It is a side example in a parenthesis; I kept it because it bears on the parenthesis's own argument (the author need not change the utility function if a bounded one fits the stated preference). The editor may judge it a nitpick (STANDARDS 2.4 (2)); it is kept out of the "In short" line and given one clause in the Response.
2. Note on "Next, let's turn to the charge that Omega favors irrationalists": says the post's reply "does not settle" the dispute and uses Lewis's "standoff". I avoided "fails"; the claim is that the reply takes one side of a dispute Lewis judged consistent on both sides.
3. Note on the causal decision theorist's quoted objection ("you must somehow believe that your choice can affect..."): I say it is unsourced and "differs from the charge in the sources checked here" (Lewis, SEP). I cannot rule out that some causal decision theorist said it; hence "checked here".
4. Note on Rachel's envy: uses "denies" (Joyce's last sentence against the post's "envies Irene her choice, and only her choice"), not "contradicts". Then says each reading assumes its own side's answer. The post's defender would say the earlier Omega argument is the answer; the note says so.
5. Cliff analogy note: rewritten to use the post's own concession ("there are various thought experiments in which some agents start out with an advantage") rather than calling the analogy question-begging.
6. Stakes note ("Then maybe it's time to update your definition of reasonableness"): says Joyce's passage already grants the wish. Joyce's passage denies Irene's inference from the wish to "It wasn't so smart to take the money"; the post's inference is from the wish to redefining "reasonable". I treat these as the same step; the editor may judge them different enough to soften "denies the step" in the Response.
7. "I shouldn't need to show this to you" note: uses the post's own concession about verbal arguments against it. Phrased as "by the post's own account the hard part is still open", not as a contradiction.
8. Reserved-word flags: "never" appears once, paraphrasing the post's own "you never end up envying". "wrong" appears inside SEP's quoted sentence and in the post's "got the Way wrong". The honest n.b. uses "mistaken". No reserved word is used as our verdict.
9. Pronouns: "she/her" only for Joyce's characters Rachel and Irene (the text's own). No pronoun for the post's author, Lewis, Joyce or Newcomb.
10. Later work (TDT 2010, FDT 2017) appears as information in one note, one honest n.b., and not in the Response or "In short".
11. Honest section is 521 words, slightly over the 500 guideline.
