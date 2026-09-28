# Report: scope-insensitivity

## 1. The argument in three sentences

In survey experiments, what people say they would pay to save 2,000, 20,000 or 200,000
birds, to clean lakes, protect wilderness or reduce risks to human life barely changes when
the number at stake changes by factors of 10 to 600. Two explanations are offered: people
value an imagined single prototype (one oily bird), with scope adding only a little on top,
or they pay for a fixed "warm glow" of moral satisfaction; a paper on "psychophysical
numbing" adds that lives saved are judged as a proportion of the total, as in Weber's law.
The moral is that an effective altruist must reason with the numbers, not with the feeling
the image produces.

## 2. Sources checked

Local copies are in the session scratchpad (`raz_p1/`), not in the repo.

1. Desvousges et al., *Measuring Nonuse Damages Using Contingent Valuation*, RTI Press, 2nd ed.
   (2010). PDF: https://dpjh8al9zd3a4.cloudfront.net/publications/6cc56240-344c-4a68-b4d6-989132d20870/versions/Measuring_Nonuse_Damages.pdf
   - Table 5-1 ("Univariate Results for Three Migratory-Waterfowl Questionnaires: Censored Data
     Sets"): "Mean 80 78 88"; text: "using the censored data the means range from $78 to $88".
     Median $25 in all three.
   - Versions: "about 2,000 migratory waterfowl died in these holding ponds. This was much less
     than 1 percent of the 8.5 million migratory waterfowl in the Central Flyway." / "...20,000
     ... This was less than 1 percent of the 8.5 million..." / "...200,000 ... This was about 2
     percent of the 8.5 million migratory waterfowl in the Central Flyway."
   - Question: "what is the most that your household would agree to pay each year in higher
     prices for wire-net covers to prevent about 2,000 (or 20,000 or 200,000 depending on the
     version) migratory waterfowl from dying each year in waste-oil holding ponds".
   - Funding: "©1992, Exxon Corporation"; "This monograph provides the results of some
     experiments that were funded by Exxon ... Exxon decided to undertake these experiments to
     test the accuracy of contingent valuation for measuring nonuse values."
   - Conclusion: "we conclude based on our experiments that CV estimates of nonuse values fail
     to reflect large and realistic differences in levels of natural resource services.
     Although our study does not determine the cause of this failure".
   - The questionnaire proposes "(hypothetical) federal regulations".
2. Kahneman, Ritov and Schkade (1999). Primary text NOT reachable (Springer paywall; the UCSB
   copy linked from Wikipedia is 404; web.archive.org blocked). The wording used in the cfact
   note comes from two secondary sources, which agree:
   - Wikipedia "Scope neglect" (raw wikitext, fetched this session): "The story [...] probably
     evokes for many readers a mental representation of a prototypical incident, perhaps an
     image of an exhausted bird, its feathers soaked in black oil, unable to escape", cited to
     p. 212.
   - Yudkowsky, "Cognitive Biases Potentially Affecting Judgment of Global Risks" (2008),
     https://intelligence.org/files/CognitiveBiases.pdf: "The story constructed by Desvouges et.
     al. probably evokes for many readers a mental representation of a prototypical incident,
     perhaps an image of an exhausted bird, its feathers soaked in black oil, unable to escape."
   - Abstract (EconPapers, https://econpapers.repec.org/article/kapjrisku/v_3a19_3ay_3a1999_3ai_3a1-3_3ap_3a203-35.htm):
     "These answers are better understood as expressions of attitudes than as indications of
     economic preferences."
3. Fetherstonhaugh, Slovic, Johnson and Friedrich (1997), in-press version dated
   "December 20 1996", University of Oregon repository:
   https://scholarsbank.uoregon.edu/server/api/core/bitstreams/9fd990a9-47e2-43cf-9b2e-da93e10072e5/content
   (the commonsenseatheism link in the post returns a captcha page).
   - Weber's law appears only on pp. 2-3 (introduction) and in the references: "What is known
     today as 'Weber's law' states that in order for a change in a stimulus to become just
     noticeable, a fixed percentage must be added ... Fechner proposed a logarithmic law ...
     Numerous empirical studies by S. S. Stevens (1975) have demonstrated that the growth of
     sensory magnitude ... is best fit by a power function". (grep for "Weber": lines in the
     intro and reference list only.)
   - Study 1: programs "to save the lives of 4,500 refugees", camps of "250,000" and "11,000".
     Result: "they preferred the small-camp program (M = .45) over the large-camp program
     (M = -.20)" on recoded ratings from -6 to +6.
   - Study 3: "over 67% of participants responded psychophysically in Task 1 of Study 3,
     whereas only 16% responded psychophysically in Task 2"; "the way information about
     life-saving interventions was framed changed the degree of numbing"; Task 2 "emphasized
     the magnitude of each intervention's life-saving potential"; "median estimates were more
     than 11 times greater for the intervention that treated the disease killing 290,000
     annually than the one killing 15,000 annually."
   - Caveat: this is the pre-publication version, not the journal text.
4. Ziano et al. (2021), "Numbing or sensitization? Replications and extensions of
   Fetherstonhaugh et al. (1997)", JESP 97, 104222. PDF:
   https://mgto.org/wp-content/uploads/2021/09/Ziano-et-al-PPnumbing-replications-extensions-print.pdf
   Abstract: "We found mixed support, with two successful replications of Study 2 that indeed
   showed psychophysical numbing ... yet also three unsuccessful replications of Study 1
   showing instead an opposite psychophysical sensitization, a preference for saving a smaller
   proportion of lives ... all in the opposite direction"; "Materials, preregistrations, data,
   and analyses are available". Study 2 of the original also used camps of 11,000 and 250,000
   (Fetherstonhaugh preprint: "size of refugee camp (11,000 or 250,000)").
5. Background only (no note quotes it): Desvousges, Mathews and Train (2012), "Adequate
   responsiveness to scope in contingent valuation", Ecological Economics 84,
   https://eml.berkeley.edu/~train/papers/scope.pdf. Table 1 lists 109 CV studies with scope
   tests; I counted 40 Pass, 17 Fail, 47 Mixed, 5 Not reported. Text: "since there are
   rational reasons for a small response to scope, such as diminishing marginal utility and
   substitution, failing the test does not indicate that the estimated response is
   inadequate." (Funded in part by BP, as its footnote says; the same authors argue that
   responses are usually inadequate.) This informed the "no standard" point but is not cited.

## 3. Arithmetic recomputed

- Risk factor: 2.43 / 0.004 = 607.5, so "a factor of 600" is fair.
- Payment factor: 15.23 / 3.78 = 4.03, "about fourfold".
- Birds: 200,000 / 2,000 = 100 ("a hundred times more").
- Shares of 8.5 million: 2,000 = 0.024%, 20,000 = 0.24%, 200,000 = 2.35%. These match the
  survey's own "much less than 1", "less than 1", "about 2 percent".

## 4. Claims about other posts

- No note makes a claim about another post in this collection.
- Consistency: our notes on `on-caring` (not in R:A-Z; "Beyond the Sequences") already argue
  that "multiply" assumes each bird is worth the same however many there are
  (`annotated/afterwords/on-caring.tex`: "The rule rests on an assumption the essay never
  states: that each bird is worth the same however many birds there are."). My notes here make
  the related, weaker point that Scope Insensitivity gives no standard for the right response.
  The two agree. The editor may want a pointer from one to the other.

## 5. Not verified

- Kahneman (1986) on Ontario lakes, McFadden and Leonard (1993) on 57 wilderness areas and 28%:
  not checked (book chapters). No note depends on them.
- Carson and Mitchell (1995) figures (0.004, 2.43, $3.78, $15.23): not checked.
  econweb.ucsd.edu fails TLS verification through the proxy (curl error 60), and WebFetch got
  503. My note uses only the post's own numbers. I also could not check how Carson and Mitchell
  themselves read the result (I recall, unverified, that they argued for scope sensitivity; I
  did not use this).
- Baron and Greene (1996): upenn.edu returns 403. "No effect from varying lives saved by a
  factor of 10" not checked. My clogic note ("Every study in the post asks people to state
  what they would pay, or to judge proposed programs") assumes this study is a survey, which
  its title ("valuation of public goods") suggests but I did not confirm.
- Kahneman, Ritov and Schkade primary text (see 2.2).
- Whether the 2007 original said "effective altruist" (the term is later); I did not try to
  establish the original wording and made no note.

## 6. Judgment calls for the editor

1. Reserved word "the opposite" (cfact on the refugee example, and the matching n.b.). It
   follows Ziano et al.'s own words ("all in the opposite direction") and applies to Study 1
   only; the note says Study 2 replicated.
2. The KRS quotation note says "The quotation is changed", not "misquotes". The change adds
   "single" (which is the post's own point) and drops two hedges. Evidence is two agreeing
   secondary sources, one of them the author's own 2008 chapter; the primary was not reachable.
3. The population-share note (first cpara) argues only that caring about the population gives
   "less reason to pay a hundred times more". It does not claim flat answers are rational.
   A careful reader could say that 2% against 0.02% should still move answers; the note does
   not deny that.
4. "overstates what it did" on Weber's law rests on the preprint (Weber mentioned only in the
   introduction). If the published version differs, this weakens.
5. The Exxon funding note (footnote 1). It reports the monograph's own statements. I kept it
   because it tells the reader what the study was designed to test (the survey method) and
   what its authors concluded. It could read as insinuation; no motive is stated.
6. Post-dated evidence: the replication (2021) note judges the evidence, not the author. The
   afterword says "long after the post" to make that clear.
7. No \cpara on footnotes 2 to 6 (citations only). I treated them as not substantial.
8. The honest section has 7 n.b. notes, more than "a handful"; each corresponds to one
   annotated note.
