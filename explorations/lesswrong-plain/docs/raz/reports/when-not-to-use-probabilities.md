# Report: When (Not) To Use Probabilities (order 295, batch 5c)

## 1. The argument in three sentences

The laws of probability govern all reasoning under uncertainty, but people usually cannot
compute them, and a number produced by a non-numerical procedure (a gut feeling put into
words as "one in a thousand") carries an air of authority and a calibration it does not have,
so one should generally not make up numerical probabilities without some numerical basis.
The example is an argument at the 2008 Global Catastrophic Risks conference that put at least
1 in 1000 on the LHC safety papers being wrong and at least 1 in 1000 on the world being
destroyed if they were; the author proposes instead to debate the general rule of banning
experiments that cannot be proved safe, which brings in frequencies and historical cases.
The author admits the stance leaves inconsistencies (more alarm at a 1-in-a-million lottery
than at the LHC, yet no ability to make a million statements that reliable) and prefers to
keep them rather than make up numbers, since accuracy and winning matter more than
consistency.

(Written before annotating.)

## 2. Sources checked

All saved in `data/sources/batch5c_when-not-to-use-probabilities/` (S below).

- Ord, Hillerbrand, Sandberg, "Probing the Improbable", arXiv 0810.5515v1, submitted
  30 Oct 2008 (S: `ord2008.pdf`, `ord2008.txt`, `abs_0810.5515.txt`). Published J. Risk
  Research 13(2), 2010 (not read; the arXiv version was used). Matched:
  - "let us suppose that the argument made in the report looks very solid, and that our best
    estimate of the probability that it is flawed is one in a thousand" ... "we also treat this
    probability as one in a thousand. Equation (1) tells us that the probability of catastrophe
    would then be just over one in a million".
  - "P(X|¬A), is generally even more difficult to evaluate"; "few would dispute that we really
    have very little idea of what value to put on P(X|¬A)".
  - retraction rates: Cokol et al. 2007 on MEDLINE, "between 0.001 and 0.01"; "In particular,
    the hard sciences may be less prone to error than the more applied sciences."
  - "It is true that the grey area can never be completely removed, however if a new argument
    (A2) is independent of the previous argument (A1) then the grey area will shrink"; "A small
    remaining grey area can be acceptable if P(X|¬A)P(¬A) is estimated to be sufficiently small
    in comparison to the stakes."
  - Giddings and Mangano as "three sequential arguments, each partly filling in the grey area".
  - "the RHIC had been running for five years on the strength of a flawed safety report, before
    Tegmark and Bostrom noticed and fixed this gap"; Castle Bravo; Kelvin (age of the Earth).
  - "the current safety report should not be the final word"; "so further analysis is critical";
    "we are open to the possibility that additional supporting arguments and independent
    verification of the models and calculations could significantly reduce the current chance of a
    flaw".
  - They cite "Yudkowsky 2008" for the lottery point ("if we could not correctly predict
    probabilities lower than 10-6, we could not run lotteries").
- GCR 2008 programme and abstracts, https://global-catastrophic-risks.com/docs/Programme.pdf and
  https://global-catastrophic-risks.com/docs/Lectures%20by%20Subject.pdf (S: `gcr_programme.txt`,
  `gcr_lectures.txt`). Sunday 20 July, 12.20: "Rafaela Hillerbrand, Anders Sandberg and Toby Ord,
  'Probing the Improbable: ...'". Abstract ends "using the risk estimates from the Large Hadron
  Collider as a test case." Friday 18 July, 12.20: Michelangelo Mangano, "Expected and Unexpected
  in the Exploration of the Fundamental Laws of Nature" (abstract: "discussions over the possible
  outcomes of new high-energy experiments"). The author spoke on 18 and 20 July.
- Ronald Bailey, "A 1-in-1,000 Chance* of Gotterdammerung", Reason, 2 Sept 2008,
  https://reason.com/2008/09/02/a-1-in-1000-chance-of-gotterda/ (S: `reason_bailey.txt`). Matched:
  "Ord argued that it's not unreasonable to think that there is a 1-in-1,000 chance that the
  theories underlying the LHC are flawed"; "Ord cited survey evidence which found that 1-in-1,000
  to 1-in-100 articles are retracted from high-impact scientific journals"; "Thus Ord concluded
  that the LHC should not be switched on"; Kelvin "calculated the age of the sun"; Castle Bravo;
  "miscalculations in medication dosages"; "Ord responded that his analysis should only apply to
  experiments that pose an existential risk to humanity". The article's correction says the
  headline is inaccurate, the Mangano quotation "gives a misleading impression of his actual
  estimates", and "Ord informs me that his overall estimate of disaster from switching on the LHC
  is between 1 in 10,000 and 1 in 1,000,000." Because of the correction I dropped the Mangano
  quotation and kept only that Ord answered an objection from Mangano.
- LSAG, "Review of the Safety of LHC Collisions", arXiv 0806.3414, 20 June 2008 (S:
  `abs_0806.3414.txt`, `arxiv_0806.3414.txt`). Abstract: "so that they present no conceivable
  danger" (black holes). Text: the 2003 LHC Safety Study Group report (Blaizot et al.,
  CERN-2003-001) "concluded that there is no basis for any conceivable threat from the LHC."
  The 2003 report itself (CDS) was blocked by a bot check; described only via LSAG 2008 and
  Wikipedia. Note: the brief calls both reports "LSAG"; the 2003 group was the LHC Safety Study
  Group, LSAG is the 2008 group.
- Giddings and Mangano, arXiv 0806.3381, 20 June 2008 (S: `abs_0806.3381.txt`). Abstract:
  "conclude, from multiple perspectives, that there is no risk of any significance whatsoever
  from such black holes."
- Wikipedia, "Safety of high-energy particle collision experiments" (raw; S: `wiki_safety.txt`),
  secondary, for the suit: "On 21 March 2008, a complaint requesting an injunction to halt the
  LHC's startup was filed by Walter L. Wagner and Luis Sancho ... before the United States District
  Court for the District of Hawaii." (Later events, not used in notes: dismissed 26 Sept 2008;
  appeal dismissed 24 Aug 2010; ECHR application 26 Aug 2008 rejected; German Constitutional Court
  Feb 2010.)
- Yudkowsky, "Cognitive biases potentially affecting judgment of global risks", draft of 31 August
  2006, https://www.stat.berkeley.edu/~aldous/157/Papers/yudkowsky.pdf (S: `yud_aldous.txt`, line
  745): "Of all the times an expert has ever stated, even from strict calculation, that an event has
  a probability of 10-6, they have undoubtedly been wrong more often than one time in a million."
  Line 655: "Accuracy "jumped" to 81% at 1000:1". Same passages in the MIRI reprint
  (`data/sources/CognitiveBiases.txt`, lines 565, 644-646); "Only 73% of the answers assigned odds
  of 100:1 were correct".
- Cooper, Artificial Intelligence 42 (1990) 393-405, https://stat.duke.edu/~sayan/npcomplete.pdf
  (S: `cooper1990.txt`): "We show that probabilistic inference using belief networks is NP-hard."
- Körding and Wolpert, Nature 427 (2004) 244-7, PubMed abstract (S: `kording2004.txt`): "subjects
  internally represent both the statistical distribution of the task and their sensory
  uncertainty, combining them in a manner consistent with a performance-optimizing bayesian
  process."
- Kent, "Words of Estimative Probability" (1964),
  https://www.cia.gov/resources/csi/static/Words-of-Estimative-Probability.pdf (S: `kent1964.txt`):
  "the low man was thinking of about 20 to 80, the high of 80 to 20"; "The poets would probably
  argue that in a sentence of this sort the introduction of any of the terms for particular odds
  would make the writer look silly."
- Friedman, Baker, Mellers, Tetlock, Zeckhauser, "The Value of Precision in Probability
  Assessment", preprint of ISQ 62(2) 2018 (S: `friedman2018.txt`): "coarsening numeric probability
  assessments in a manner consistent with common qualitative expressions – including expressions
  currently recommended for use by intelligence analysts – consistently sacrifices predictive
  accuracy"; "888,328 forecasts in response to 380 questions administered between 2011 and ...";
  "Project began in 2011".

## 3. Arithmetic

- Speaker's figures: 10^-3 × 10^-3 = 10^-6; with P(X|A) ~ 10^-9 (the paper's example report),
  P(X) = 10^-9 × 0.999 + 10^-6 ≈ 1.001 × 10^-6, "just over one in a million". The post says
  "at least" for each figure, so the product is "at least one in a million".
- The post's test: not able to make 10^6 statements of equal authority with about one error
  means an error rate above about 10^-6 per statement, i.e. P(LHC destroys world) judged above
  about 10^-6 in calibration terms. Hence "close to" the speaker's product. I wrote "close to"
  rather than "equal to" because the post's test gives only a lower bound and the speaker's
  figures are lower bounds too.
- 1000:1 odds correspond to 99.9%; 81% observed.

## 4. Claims about other posts

- Beautiful Probability (order 188), `data/originals/beautiful-probability.md`: "Needing to
  calculate approximations to a law doesn't change the law." (the post links it for "laws, not
  suggestions").
- Infinite Certainty (order 61): "If you say 99.9999% confidence, you're implying that you could
  make one million equally fraught statements, one after the other, and be wrong, on average,
  about once." Our notes there discuss the Fischhoff study (afterword: odds of 100 to 1 right 73%).
- Should We Ban Physics? (21 July 2008, not in the book), fetched with `src/fetch.py post
  rnk9gmWSrcqNfg7p8` to `data/originals/should-we-ban-physics.md`: "So the one who proposed the
  policy, disagreed that their policy cashed out to a blanket ban on physics experiments."
- Planning Fallacy (order 9): outside view = ask how long "broadly similar projects" took.
- Something to Protect (order 294, the previous post in book order), Lost Purposes (154), A
  Technical Explanation (261): pointers only.

## 5. Not verified

- What was said in the talk itself. I rely on the programme, the abstract, Bailey's report
  (with its correction) and the paper posted three months later. The post's "at least 1 in 1000"
  for P(X|¬A) matches the paper's illustration; I found no record of the talk's slides.
  The Oxford podcast series of the conference may have audio (not checked).
- Whether the speaker in the post is Ord or another of the three authors. The post says "the
  speaker" and "the authors"; Bailey attributes the talk to Ord.
- The 2003 LHC Safety Study Group report directly (CDS blocked).
- The published 2010 version of Ord et al. (paywalled); the arXiv v1 was used.
- Wayback copy of the 2008 chapter could not be fetched (connection resets); the 2006 draft
  was used instead, so the claim is dated to 2006.

## 6. Judgment calls for the editor

- Reserved word "wrong": used only in the ordinary sense ("chance of being wrong about the LHC",
  "papers might be wrong", summary of the post). No verdict uses a reserved word.
- Note on "the most disingenuous part" (cpara) and its Response and honest counterparts: we
  criticize the post's charge of bad faith. The support is the speakers' later paper, which may
  differ from the talk; the note says so. The note's other point, that the post's reason would at
  most show a mistake, rests on the post's own text.
- Note on "numbers pulled out of thin air": "Overstated for the first figure". The evidence that
  the talk grounded the first figure in retraction rates is Bailey's report (a journalist present)
  plus the later paper. I kept the caveat that the rates are biomedical and that the paper itself
  grants the hard sciences may err less.
- Note on the million-statements paragraph: "close to the speaker's". This is my derivation from
  the post's own two sentences; the post itself calls the result an inconsistency and does not
  resolve it, which the notes credit.
- Note on (3) "illusion": "asserted, not argued". The post gives no argument for (3) beyond the
  next paragraph's "no possible physics paper can ever get rid of it", which concerns removal,
  not reduction. A fair defender could say the next paragraph is the argument; I think it answers
  a different question (removal), and the "disingenuous" note says the speakers granted it.
- Note on the general rule: "broader than the one the speakers defended". Support: the author's
  own report two days earlier and Bailey's report of Ord's reply. The post frames its proposal as
  "the alternative I would propose", not as the speakers' view, so the note says only that the
  rule is broader.
- Friedman et al. (2018) is hindsight. It is in one sentence note only (information, with the
  post's "I think" noted), not in the Response or the In short line. The honest n.b. omits it.
- Kent (1964) is used as prior debate, not as a fault: the note says the post takes the poets'
  side with their argument, and that Kent's concern (the reader) is outside the post's reason.
  An editor may judge the last clause as scope and cut it.
- The talk identification ("almost certainly") rests on the programme and Bailey. Mangano also
  spoke on high-energy experiments, two days earlier, so the note mentions him.
- Response length 441 words; honest 525 words (slightly above 500). Summary 223 words.
- Pronouns: Kent (historical figure) is not given pronouns in notes; the afterword avoids them too.
