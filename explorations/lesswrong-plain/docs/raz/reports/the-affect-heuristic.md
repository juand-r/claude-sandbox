# Report: the-affect-heuristic ("The Affect Heuristic", Yudkowsky, posted 2007-11-27)

## 1. The argument in three sentences (written before annotating)

The affect heuristic is the use of a quick feeling of good or bad as a basis for judgment, and the post illustrates the biases it produces with a series of studies of increasing strangeness: people pay more to insure a sentimental clock for the same payout, judge 1,286 deaths in 10,000 as more dangerous than a 24.14% fatality rate, support a measure saving 98% of 150 lives more than one saving 150 lives, and prefer 7 red beans in 100 to 1 in 10. Finucane and colleagues found that information about benefits lowers perceived risk and vice versa, more so under time pressure, and Ganzach found that analysts judging unfamiliar stocks treated risk and return as moving together in a good-or-bad way instead of the positive relation that economic theory predicts. People merge separate good and bad aspects of a thing into one overall feeling.

## 2. Sources checked (outside quotations and figures)

Saved in `data/sources/raz_b2b/`.

- **Slovic, Finucane, Peters and MacGregor, "The affect heuristic"**, EJOR 177 (2007) 1333-1352, "Reprinted from Gilovich, T., Griffin, D., Kahneman, D. (Eds.), 2002. Heuristics and Biases". PDF: https://bear.warrington.ufl.edu/brenner/mar7588/Papers/slovic-affect-heuristic-2002.pdf -> `slovic_affect_heuristic_2002ch.pdf`, `slovic_ch.txt` (layout), `slovic_ch_raw.txt`. Matched:
  - Table 3 "Proportion dominance and airport safety": Save 150 lives / 98% / 95% / 90% / 85%; Mean support 10.4 / 13.6 / 12.9 / 11.7 / 10.9; "The response scale ranged from 0 (would not support at all) to 20 (very strong support)"; "The save 98% and save 95% conditions were both significantly different from the save 150 lives condition at p < .05". Text: "Slovic (unpublished) ... predicted (and found) that people, in a between-groups design, would more strongly support an airport-safety measure expected to save 98% of 150 lives at risk than a measure expected to save 150 lives."
  - "Hsee and Kunreuther (2000) have demonstrated ... people were willing to pay twice as much to insure a beloved antique clock (that no longer works and cannot be repaired) against loss in shipment to a new city than to insure a similar clock for which "one does not have any special feeling". In the event of loss, the insurance paid $100 in both cases."
  - "Yamagishi (1997), whose judges rated a disease that kills 1286 people out of every 10,000 as more dangerous than one that kills 24.14% of the population."
  - "Denes-Raj and Epstein (1994) showed that ... subjects often elected to draw from a bowl containing a greater absolute number, but a smaller proportion, of red beans (e.g., 7 in 100) than from a bowl with fewer red beans but a better probability of winning (e.g., 1 in 10)."
  - "In the realm of finance, Ganzach (2001) found support for a model in which analysts base their judgments of risk and return for unfamiliar stocks upon a global attitude ... However, for familiar stocks, perceived risk and return were positively correlated".
  - "Finucane et al. showed that the inverse relationship between perceived risks and benefits increased greatly under time pressure, as predicted."
- **Slovic et al. (2002), "Rational actors or rational fools"** (the post's footnote 3 and recommended article), https://cpb-us-w2.wpmucdn.com/u.osu.edu/dist/e/65099/files/2018/08/2002_Slovic_Finucane_etal._Rational_actors_or_rational_fools-2ltdwze.pdf -> `slovic2002.pdf/.txt`. Covers Finucane et al. ("increased greatly under time pressure") and the airport study (Fig. 4, "reported in Slovic et al. (2002)"). grep for Hsee and Kunreuther, Yamagishi, Denes-Raj, Ganzach, clock, beans: no matches. Basis of the last cpara.
- **Finucane et al. (2000)** -> `finucane2000.txt` (copied from `data/sources/raz_b2_politics/`, fetched by an earlier agent from https://stanford.edu/~knutson/jdm/finucane00.pdf). Matched: "Fifty-four first-year Psychology students from the University of Western Australia"; "For the time-pressure condition, the mean correlation was -0.45 ... For the no-time-pressure condition, the mean correlation was -0.33 ... The difference between the two mean correlations approached significance; t(52) = 1.64, p [symbol lost] 0.05, one-tailed." Also across items: -0.80 vs -0.75 (all 23 items), -0.69 vs -0.62 (without cigarettes and solar power). Study 2: "As predicted, the nonmanipulated attribute generally changed in the direction affectively congruent with the manipulation (the only exceptions were Food LB and Nuclear LB)."
- **Hsee and Kunreuther (2000)**, abstract only (EconPapers, https://econpapers.repec.org/article/kapjrisku/v_3a20_3ay_3a2000_3ai_3a2_3ap_3a141-59.htm -> `hsee_kunreuther_econpapers.html`). Matched: "We explain these findings by a "consolation hypothesis," according to which, people perceive insurance compensation as a token of consolation". Full text paywalled (Springer; Semantic Scholar "CLOSED").
- **Yamagishi (1997)**: paper paywalled; Crossref gives pages 495-506 (the post's footnote says 461-554; citation slip, not noted). Summary used: Bonner and Newell (2008), "How to make a risk seem riskier: The ratio bias versus construal level theory," JDM 3(5):411-416, http://journal.sjdm.org/8210/jdm8210.html -> `jdm8210.html/.txt`. Matched: "Yamagishi (1997) gave participants mortality rates of well-known causes of death, varying both the percentage incidence rate and population frame (deaths per 100 or 10,000 people) within subjects."; "participants rated cancer as riskier when it was described as killing 1,286 out of 10,000 people than as killing 24.14 out of 100 people."; "The ratio bias has been investigated in the health domain by Yamagishi (1997)". Slovic et al. (2007) above describes the second as "kills 24.14% of the population".
- **Denes-Raj and Epstein (1994)**, PubMed abstract (PMID 8014830) -> `pubmed_denesraj_ganzach.txt`. Matched: "subjects frequently elected to draw from a bowl that contained a greater absolute number, but a smaller proportion, of red beans (e.g., 7 in 100) than from a bowl with fewer red beans but better odds (e.g., 1 in 10). Subjects reported that although they knew the probabilities were against them, they felt they had a better chance when there were more red beans."
- **Ganzach (2000)**, OBHDP 83(2):353-370, PubMed abstract (PMID 11056075), same file. Matched: "for unfamiliar assets, both risk and return judgments are derived from global preference toward the asset, whereas for familiar assets, these judgments tend to be derived from the ecological values of the asset's risk and expected return-their values in the financial markets."

## 3. Arithmetic

- 98% of 150 = 147 lives.
- 1,286/10,000 = 12.86%, less than 24.14%.
- 7/100 = 7% < 1/10 = 10%.
- Finucane Study 2: 3 technologies x 4 conditions = 12; 2 exceptions, so 10 of 12 (used in the Response).

## 4. Claims about other posts

- "The Scales of Justice, the Notebook of Rationality" (Posted 2007-03-13): our notes there say the paper "did not test" waste against meltdown and that the example is the post's own. Our cpara here says this post describes the design correctly and points there. Consistent.

## 5. Not verified

- Hsee and Kunreuther's clock details (gift from grandparents on the fifth birthday, remote relative, outside insurance company, "more than twice as much"): paper not reachable. The Slovic summary says "twice as much"; the difference is small and not noted.
- Yamagishi's exact stimuli and wording: only two secondary summaries, which differ in format ("24.14 out of 100 people" vs "24.14% of the population") but agree that both figures were deaths in a population. The cpara says "In the summaries I could read" and "I could not read the paper."
- Ganzach's subjects (the post and Slovic say "analysts"; the abstract does not say).
- The "general finding" about time pressure, poor information and distraction: no source given; the cpara says so.

## 6. Judgment calls for the editor

- The Yamagishi cpara and the Response paragraph on it. The post's "a disease that was 24.14% likely to be fatal" could be read as a population probability for any one person, which is closer to the summaries than "case fatality". I therefore did not say the post misdescribes the stimulus; I said the "single person" contrast is the post's own and that its explanation "depends on the rewording". Please check that this is not stronger than the evidence, since I have only summaries.
- The consolation cpara: the post does not claim the consolation idea as its own; it presents it as something "you could get away with claiming". The note says only that it is the authors' explanation and that the post does not say so.
- The time-pressure cfact: the post's "greatly" matches the authors' own later summaries (both 2002 papers), so the note attributes the word to them and contrasts it with the 2000 paper's figures. A defender could say the post reasonably relied on the authors' summary.
- The last cpara (which article summarizes which studies) is a sourcing observation, not a charge.
- No reserved words.
