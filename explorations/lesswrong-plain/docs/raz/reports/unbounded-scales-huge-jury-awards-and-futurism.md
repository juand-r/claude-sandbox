# Report: unbounded-scales-huge-jury-awards-and-futurism ("Unbounded Scales, Huge Jury Awards, & Futurism", Yudkowsky, posted 2007-11-29)

## 1. The argument in three sentences (written before annotating)

In psychophysics, people rating a stimulus on an unbounded scale with no reference value
(no modulus) agree on ratios but pick arbitrary scales, so the raw numbers vary wildly.
Kahneman, Schkade and Sunstein found the same in punitive damages: jury-eligible
respondents agreed on outrage and punishment on bounded scales and on the ranking of dollar
awards, but the dollar amounts themselves were almost unpredictable, so an award is an
attitude expression on an unbounded scale. The author proposes that forecasts of when
human-level AI will arrive are the same kind of thing: a feeling of difficulty (or of
optimism) expressed on an unbounded scale and labeled "years".

## 2. Sources checked

Local copies in `data/sources/raz_b2b_jury/`.

1. Kahneman, Schkade and Sunstein (1998), "Shared Outrage and Erratic Awards", J. Risk and
   Uncertainty 16 (the post's footnote): text from
   https://slideheaven.com/shared-outrage-and-erratic-awards-the-psychology-of-punitive-damages.html
   (`kss_jru_slideheaven.txt`; an HTML rendering of the journal PDF, with page headers).
   - "The sample consisted of 899 jury-eligible respondents who were recruited from the Travis
     County, Texas voter registration list ... Thirty-two respondents were dropped" (899 - 32 = 867).
   - "The respondents were told to assume in all cases that compensatory damages had been
     awarded in the amount of $200,000".
   - Table 6 ("Proportion of Variance in Individual Responses Accounted for by Scenarios"):
     Outrage raw .29, ranks .42; Punishment raw .49, ranks .58; $ Awards raw .06, ranks .51,
     Ln($) .42.
   - Demographic groups: punishment median correlation .99; outrage "a median correlation of
     .94"; dollars "the median correlation was .65".
   - Synthetic juries: "randomly selecting a group of 12 individuals, using the median response";
     "agreement between independent synthetic juries judging dollar awards on a magnitude scale
     is quite weak (r = .42)"; outrage and punishment ".87 and .89"; "when the size of the juries
     is increased to 30, the correlation ... rises to .80".
   - "Eisenberg et al concluded that the unpredictability of punitive awards has been overstated.
     ... we agree with their conclusion that log awards are reasonably predictable. Defendants
     and plaintiffs, however, live in a world of dollars, not log dollars."
   - "There is no reason to believe that our main findings would be altered by the process of
     group deliberation."
   - Abstract: "These results are familiar characteristics of judgments made on unbounded
     magnitude scales."
   - Case with the burned child: "Jack Newton, a five-year-old child, was playing with matches
     when his cotton flannel pajamas caught fire" (quoted from the Yale version's appendix).
2. Sunstein, Kahneman and Schkade (1998), "Assessing Punitive Damages", Yale Law Journal 107:
   https://scispace.com/pdf/assessing-punitive-damages-with-notes-on-cognition-and-2q3uemd9md.pdf
   (`sks_scispace.pdf/.txt`).
   - "Here is the central point: Magnitude scaling without a modulus produces extremely large
     variability in judgments of any particular stimulus, because of arbitrary individual
     differences in moduli."
   - "these findings do not replicate the real world of punitive damage awards. Ours was an
     experimental study ... Moreover, our 'juries' did not deliberate."
   - "Our study ... did not contain two usual 'anchors': the plaintiff's demand and the jury's own
     prior determination of compensatory damages."
   - Footnote 118: "Only 49% of the variance in individual punishment ratings, 29% of outrage
     ratings, and 6% of dollar awards are explained by differences between cases."
3. Stevens's power law, Wikipedia raw wikitext (`wiki_stevens.txt`): table row "Loudness || 0.67
   || Sound pressure of 3000 Hz tone"; description of magnitude estimation with and without a
   modulus. Sone, Wikipedia raw (`wiki_sone.txt`): "each 10 phon increase (or 10 dB at 1 kHz)
   produces almost exactly a doubling of the loudness in sones"; exponent 0.3 against intensity.
4. Grace, Salvatier, Dafoe, Zhang and Evans, "When Will AI Exceed Human Performance?",
   arXiv:1705.08807v3 (`grace2017.pdf/.txt`): "a 50% chance of HLMI occurring within 45 years";
   "a subset were asked a logically similar question"; full automation "a 50% probability in 122
   years"; "Yet our survey respondents do not treat them as logically equivalent. We observed
   effects of question framing in all our prediction questions". Survey of 2015 NIPS/ICML
   authors, "Years from 2016".
5. Not used in a note: Schkade, Sunstein and Kahneman, "Deliberating about Dollars: The Severity
   Shift" (Columbia Law Review 100, 2000). Could not get the text (chicagounbound and SSRN
   blocked); a web-search summary says deliberation raised awards above the median of jurors'
   pre-deliberation judgments. Not relied on.

## 3. Arithmetic

- 899 - 32 = 867.
- Loudness: energy (intensity) is proportional to pressure squared, so an exponent of 0.67 on
  pressure is 0.335 on intensity. Doubling loudness needs intensity x 2^(1/0.335) = 2^2.99 =
  about 7.9. With the sone exponent 0.3: 2^(1/0.3) = 2^3.33 = about 10.1. So "more like eight
  times" is within the range; no fault.
- Grace et al.: HLMI 45 years, full automation 122 years (as stated in the paper; aggregate of
  individual CDFs, not a median; the notes say "a 50 per cent chance").

## 4. Claims about other posts

- None.

## 5. Not verified

- The anecdote ("a mainstream AI guy said to me, 'Five hundred years.'"): not checkable.
- Footnote gives pages 48-86 for the 1998 JRU paper; the paper is pp. 49-86. Not noted.
- The second footnote reference (Kahneman, Ritov and Schkade 1999) is not used by the notes;
  the scope-insensitivity report has the abstract.

## 6. Judgment calls

1. cfact "Overstated" on "completely unpredictable": 6% is not zero, and logs give .42. The
   post's word "completely" may be informal emphasis; I kept the note because the log figure is
   in the same table the post quotes and changes the picture, and the authors themselves
   concede it. The note also gives the authors' reply ("a world of dollars").
2. The note on "the agreement is between averages" (29% of individual outrage variance) is a
   description, not a charge; the paper itself says "substantial consensus".
3. The two clogic notes on the futurism paragraph: (a) no pattern like the jury pattern is
   shown; (b) spread alone does not separate attitude expression from real uncertainty, which
   the post itself grants ("not very predictable"). Both are logical points, not empirical
   claims; no outside source needed. A fair defender could say the post's claim is hedged
   ("As far as I can guess"; "I have been unable to determine it"). The notes attack the
   evidence, not a certainty the post does not claim.
4. Credit note: the Grace et al. survey (post-dates the post) fits the thesis; the Response says
   so and says the post did not have it.
5. No reserved words used.
