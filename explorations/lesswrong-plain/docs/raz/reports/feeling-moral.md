# Report: feeling-moral ("Feeling Moral", Yudkowsky, posted 2015-03-11; book order 290)

## 1. The argument in three sentences (written before annotating)

Most people prefer saving 400 lives for certain to a 90% chance of saving 500, yet prefer the
gamble when the same options are described as deaths; since the two descriptions are the same
gamble, the preference follows the feeling produced by the wording, and the gamble, with 450
lives expected, is the better choice. The same reasoning says that if a hiccup has any
disvalue, some number of hiccups (a googolplex, say) must be worse than one person's shark
attack, and everyday choices (a console game or charity, one transplant or 200 children's
lives) are dilemmas of this kind, which people avoid by treating lives as "sacred" and
refusing trade-offs with money. Altruism is judged by the help it gives, not by how it
feels, so one should "shut up and multiply" and not regret the comfort this costs.

## 2. Sources checked

Local copies in `data/sources/5c_feeling-moral/` (curl, 29 Sept 2026).

1. Tversky and Kahneman, "The Framing of Decisions and the Psychology of Choice", Science 211
   (1981) 453-458. PDF: https://sites.stat.columbia.edu/gelman/surveys.course/TverskyKahneman1981.pdf
   (`tk1981.pdf`, `tk1981_raw.txt`). Matched: Problem 1 [N = 152] "If Program A is adopted, 200
   people will be saved. [72 percent]"; Program B "1/3 probability that 600 people will be saved,
   and 2/3 probability that no people will be saved. [28 percent]"; "a risky prospect of equal
   expected value"; Problem 2 [N = 155] "Program D ... [78 percent]"; "choices involving gains
   are often risk averse and choices involving losses are often risk taking."
2. No study with the post's own numbers (400 sure vs 500 at 90%): one web search for the exact
   option wording found only this post, "Circular Altruism" and mirrors. Hence "I found no study
   that used them".
3. Tetlock et al. 2000, JPSP 78:853-870, abstract via NCBI eutils (`tetlock2000_abstract.txt`):
   "people responded to taboo trade-offs that monetized sacred values with moral outrage and
   cleansing."
4. Tetlock 2003, Trends Cogn Sci 7:320-324, abstract via NCBI eutils (`tetlock2003_abstract.txt`):
   "They treat the mere thought of trading off sacred values against secular ones (such as money)
   as transparently outrageous"; "they often acquiesce when secular violations of sacred values are
   rhetorically reframed as routine or tragic trade-offs"; "alternately punitively rigid and
   forgivingly flexible". The post's "(Sometimes they want to punish ...)" is consistent with
   "punitively rigid"; the full papers were not read.
5. GiveWell AMF page, current (`givewell_amf_now.html/.txt`, https://www.givewell.org/charities/amf):
   "as of December 2023, we think: It costs between $3,000 and $8,000 to save a life in countries
   where GiveWell currently supports AMF to deliver ITN campaigns." The 2015 version (the post's
   link, via web.archive.org) could not be reached: the archive connection was reset each time.
6. Harsanyi's theorem: Hammond, "Harsanyi's Utilitarian Theorem: A Simpler Proof and Some
   Ethical Connotations" (https://web.stanford.edu/~hammond/HarsanyiFest.pdf, `hammond_harsanyi.txt`),
   abstract: "the social welfare function is the weighted sum of individuals' utility functions if:
   (i) society maximizes expected social welfare; (ii) individuals maximize expected utility; (iii)
   society is indifferent between two probability distributions over social states whenever all
   individuals are." Date 1955 (J. Polit. Econ. 63) from search results and Hammond's text.
7. Bounded totals as a published option: SEP "The Repugnant Conclusion" (`sep_repugnant.txt`):
   "If the value of extra lives decreases asymptotically, then there may exist an upper limit to
   the total value of a population (exactly as the sum of the infinite series 1+1/2+1/4+ … has
   the upper limit 2)". Used only as background for the clogic note; the note itself rests on the
   derivation in section 3.
8. "Circular Altruism" (4ZzefKQwAtMo5yp99, fetched to `data/originals/circular-altruism.md`,
   posted 2008-01-22): "My favorite anecdote along these lines - though my books are packed at the
   moment, so no citation for now - comes from a team of researchers..."; the chain from "one
   person being tortured for 50 years, and a googol people being tortured for 49 years, 364 days,
   23 hours, 59 minutes and 59 seconds" to "a googolplex people getting a dust speck in their eye,
   and a googolplex/googol people getting two dust specks"; "If you find your preferences are
   circular here". Its text runs from "following rationality off a cliff..." straight into that
   chain, which is why the Feeling Moral ellipsis marks the cut.
9. "Torture vs. Dust Specks" (3wYTFWY3LKQCnAptN, fetched to `data/originals/`, posted
   2007-10-30): "Would you prefer that one person be horribly tortured for fifty years without hope
   or rest, or that 3^^^3 people get dust specks in their eyes?" Not in the book (manifest).
10. The anecdote about the agency: one web search; only this post and mirrors. Not traced.

## 3. Arithmetic

Script `data/sources/5c_feeling-moral/arith.py` (output reproduced):
- Gain frame: EV of gamble = 0.9 x 500 = 450 > 400.
- Loss frame: sure option = 500 - 400 = 100 deaths; gamble 90% no deaths, 10% 500 deaths: the
  same lottery as the gain frame. EV deaths 50.
- Grandstander's 75%: EV saved 0.75 x 500 = 375 < 400 (EV deaths 125 > 100).
- T&K: sure 200 vs (1/3) x 600 = 200: equal EV.
- $700,000 / 200 = $3,500 per child's death prevented; inside $3,000 to $8,000.
- Bounded ranking for the hiccup note: u(n hiccups) = -(1 - 2^-n), u(shark) = -2. u strictly
  decreases in n (checked n = 0..59) and stays above -1 > -2, so no number of hiccups reaches the
  shark attack; expected utility with this u satisfies the von Neumann-Morgenstern axioms (any
  real-valued u does). The note's series 1/2 + 1/4 + ... < 1 is the same construction.
- Googol = 10^100, googolplex = 10^googol: the post's definitions are standard.

## 4. Claims about other posts

- Next post, "The \"Intuitions\" Behind \"Utilitarianism\"" (`data/originals/the-intuitions-behind-utilitarianism.md`):
  "Three lives are one and one and one." Used for the pointer on marginal utility.
- "Circular Altruism" and "Torture vs. Dust Specks": see sources 8 and 9. Neither is in the
  manifest (checked), so "not in the book" is correct.
- Differences between the versions (last note): Feeling Moral adds the hiccup paragraph, the
  "Moral dilemmas like these..." paragraph and "Yet there are many who avert their gaze...";
  it drops "Previously on Overcoming Bias..." through the chain and "Chimpanzees feel, but they
  don't multiply." Checked by reading both texts.
- Earlier notes (STANDARDS 2.5): no earlier post in book order has a note on Tversky and
  Kahneman 1981, Tetlock, dust specks or aggregation (grep over annotated/, honest/ and reports).
  "Something to Protect" (294, later) uses the same 400/500 dilemma; its notes (80 vs 90 per cent
  for the daughter) do not conflict with mine.

## 5. Not verified

- The 2015 GiveWell figure behind "some 200 children" (archive unreachable); the note gives the
  current range and says the 2015 page was not reached.
- The bone-marrow-transplant cost ($700,000): not checked; no note.
- Whether "Most people choose option 1" holds for the post's own numbers: no study found (one
  search). A careful search of the framing literature (for example Kühberger's meta-analysis)
  might find a version with unequal expected values.
- The agency anecdote: untraced.
- Tetlock 2000 full text (punishment measures) not read; only abstracts.

## 6. Judgment calls

1. The hiccup note ("Coherence in the decision-theoretic sense does not by itself give this")
   is a technical claim. It rests on the shown construction: a bounded utility gives a coherent
   ranking in which hiccups never outweigh the shark attack. A fair defender might say "any
   negative value" meant a fixed amount per hiccup, added up; the note covers that reading by
   saying the step needs exactly that premise. I credit Harsanyi's theorem as the standard
   argument for it (information, not a fault).
2. The fuller statement of the non-aggregative side (Scanlon, Parfit) is placed in the notes on
   the next post, which the brief assigns to it and which discusses aggregation explicitly.
   Feeling Moral points forward to it. STANDARDS 2.5 would put a recurring point at its first
   occurrence; I judged that the case against aggregation belongs where the post argues for
   aggregation. The editor may prefer to move it.
3. Neutral notes about the book leaving out "Torture vs. Dust Specks" and Circular Altruism's
   chain. The Response's "so here the claim stands on assertion" is a statement about this text,
   not a fault of the editors; it is kept out of blame language.
4. "The post's strongest point, and it is Tversky and Kahneman's": credit to prior work, not a
   charge of unoriginality (the post presents it as a known finding: "here's the interesting thing").
5. The cpara on "And I say also this to you" calls the paragraph exhortation "in the cadence of
   scripture". That describes the style; it is not a motive reading.
6. Reserved words: "never" appears only in the arithmetic statement that a geometric series
   never reaches its limit, which is exact.
