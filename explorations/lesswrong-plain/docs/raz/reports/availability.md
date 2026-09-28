# Report: availability

## 1. The argument in three sentences

People judge how frequent or likely an event is by how easily examples come to mind, and a
1978 study found errors in judged causes of death (accidents against disease, homicide
against suicide) that a 1979 follow-up linked to what newspapers report. Selective
reporting, stronger now than in the ancestral environment, makes the easily recalled
unrepresentative, and events never experienced are treated as impossible, as with flood
insurance and the false security that dams create. Past experience of small hazards sets a
perceived upper bound on risk, so memory is not always a good guide to probability.

## 2. Sources checked

- Lichtenstein, Slovic, Fischhoff, Layman and Combs (1978), "Judged Frequency of Lethal
  Events", PDF from https://scholarsbank.uoregon.edu/server/api/core/bitstreams/f85876d9-06ae-44dd-8c09-9135806411b5/content
  (read with pdftotext this session).
  - Table 1 ("frequency of death per 10^8 United States residents per year"): Homicide
    9,200; Suicide 12,000; All accidents 55,000; All disease 849,000.
  - Table 2, pair 13 (Homicide vs Suicide): true ratio 1.30; % correct: students 32, LWV 30.
    So about 68 to 70 percent chose homicide.
  - Text p. 555: "Accidental deaths were reported by the students to be about as likely as
    death from disease despite a true ratio of 15.4 for diseases over accidents (pair 69)."
  - Footnote 5 (p. 569): official records probably "underestimate the frequency of
    suicide". I did not mention this in the note; it slightly weakens the "1.3 not 2" point
    (the true ratio may be above 1.3), which is why the note says "loose", not "wrong".
- Yudkowsky, "Cognitive Biases Potentially Affecting Judgment of Global Risks":
  - Published version (MIRI reprint of the 2008 chapter): https://intelligence.org/files/CognitiveBiases.pdf.
    Matched: "Kates (1962) suggests underreaction to threats of flooding may arise from 'the
    inability of individuals to conceptualize floods that have never occurred. . . . Men on
    flood plains appear to be very much prisoners of their experience. . . . Recently
    experienced floods appear to set an upper bound to the size of loss with which managers
    believe they ought to be concerned.'" Also "(Diseases cause about 16 times as many deaths
    as accidents.)" and "correlated strongly (.85 and .89) with selective reporting in
    newspapers." Reference list: "Tversky, Amos, and Daniel Kahneman. 1973. 'Availability: A
    Heuristic for Judging Frequency and Probability.' Cognitive Psychology 5 (2): 207-232."
  - Draft of August 31, 2006: https://www.stat.berkeley.edu/~aldous/157/Papers/yudkowsky.pdf.
    Matched: "Kunreuther et. al. (1993) suggests underreaction to threats of flooding may arise
    from ... Recently experienced floods appear to set an upward bound to the size of loss".
  - The post's paragraphs 1-3 and 6-8 closely follow section 2 of the paper ("Availability").
- Combs and Slovic (1979), ERIC abstract https://eric.ed.gov/?id=EJ219546: "These biases in
  coverage corresponded closely to people's judgments of causes of death". The .85/.89
  figures were not checked (see section 5).
- LessWrong revision history of this post (GraphQL `revisions`, documentId R8cpqD3NA4rZxRdQ4):
  the 2007 text matches the current text in substance (including "Kunreuther et. al. (1993)"
  and "upward bound").

## 3. Arithmetic

- Suicide/homicide in the study: 12,000 / 9,200 = 1.304 (Table 2 gives 1.30).
- Disease/accidents in the study: 849,000 / 55,000 = 15.44 (paper: 15.4). "About sixteen"
  is close; no note on it.
- Bill Gates: 0.00000000015 = 1.5e-10; 1 / 1.5e-10 = 6.7e9, about the world population in
  2007 (I did not source the population figure; no note relies on it).
- 19% on less than $1/day: not recomputed. A World Bank page
  (https://www.worldbank.org/en/news/feature/2008/08/26/world-bank-updates-poverty-estimates-for-the-developing-world,
  seen only as a search snippet) gives 985 million in 2004, which would be about 15 percent of
  a world population of about 6.4 billion. Unverified; no note relies on it.

## 4. Claims about other posts

- None beyond the author's paper above. The post links "absurdity bias" (lw/j4); I did not
  make any claim about that post.

## 5. Items not verified

- Combs and Slovic's correlations 0.85 and 0.89: the paper (Journalism Quarterly 56) is not
  open; only the ERIC abstract was read. Note: Lichtenstein et al. 1978 (Table 7) report only
  moderate correlations (.54 to .59) between their own newspaper measures and judgments; that
  is a different measure, so I did not use it.
- Kates (1962): HathiTrust has it in full view (uc1.31210023540931) but returned a Cloudflare
  challenge; rwkates.org returned a bot-check page. Kunreuther, Hogarth and Meszaros (1993) is
  paywalled. So which source contains the flood quotation is not settled; the note says so.
- Burton, Kates and White (1978), the claim that average yearly damage increases: not reached.
  The footnote cpara says so.
- The flood-insurance claim ("heavily subsidized and priced far below an actuarially fair
  value") has no citation in the post; not checked, no note.

## 6. Judgment calls for the editor

1. Reserved words: none used as verdicts. "never" appears only in paraphrase of the post.
   "his" refers to Bill Gates (a real person the post itself calls "him"), not to the author.
2. The "Twice is loose" note. The true ratio in the study is 1.3, but the study's authors
   say suicide is probably under-recorded, and the ratio was near 2 in the US by the mid
   2000s (not sourced by me). The post says "Actually ... suicide is twice as frequent", in
   the present tense, which a fair defender could read as current figures. If the editor
   finds this a nitpick under 2.4(2), cut the note and the matching Response and n.b.
   sentences together.
3. The "either way" note offers an alternative explanation (editors covering what readers
   fear). It is a standard correlation point, not taken from a source. It could be judged
   "speculative objection" (2.4(5)).
4. The Kunreuther/Kates note does not say the post is wrong; it reports that the author's
   own later version changed the attribution. I could not see either primary source.
5. I considered and dropped a note that the post never says the heuristic usually works
   (Tversky and Kahneman's point). The last line's "not always" answers it (fair-defender 5).
6. The first cpara names Tversky and Kahneman (1973) as the source of the term. This is
   information, not a charge; the post does not claim the idea as its own.

## 7. Pilot feedback on the brief and standards (covers all three of my posts)

1. The brief lists four model posts; STANDARDS section 1 lists five (adds
   positive-bias-look-into-the-dark). I read the four in the brief.
2. The models and STANDARDS 2.2 pull in different directions. Several model notes would
   arguably fail the fair-defender test or 2.4 as written: "The diagnosis is mind-reading"
   and "The rest is decoration" (Lens), "It is only decoration" (Bottom Line), "The joke is
   funny" (an honest n.b. in Try Harder, a bare verdict). I calibrated to STANDARDS, not to
   the models' tone, so my notes are milder than the models. Please say which wins.
3. Footnote paragraphs: the Lens model gives each footnote a \cpara; the brief does not say.
   The audit counts them as paragraphs. I gave each a one-line \cpara.
4. Revision history. The texts in data/originals are LessWrong's 2019 revisions. For "What's
   a Bias?" the 2006 post is substantially different (different opening, more hedges, no
   "In cognitive science"). The LessWrong GraphQL `revisions` query returns the first
   version. The brief should say whether agents check this, and whether differences belong
   in the notes. Availability and Burdensome Details changed only slightly.
5. Numbers that are somewhat off: STANDARDS 3.3 says recompute every number, 2.4(2) says cut
   nitpicks with no consequence. I kept "twice" vs 1.3 (Availability) and dropped "a factor
   of four, at least" vs 3.4 (Burdensome). A rule of thumb for when a numerical discrepancy
   earns a note would help.
6. Tools: the preamble has no amsmath, so \text fails in math (use \mbox). raz_check raises
   BrokenPipeError when piped to head (cosmetic). Its pronoun flag fires on historical figures
   and on "his" for real people like Bill Gates. The skeleton for burdensome-details drops the
   post's footnote marker 4 (after "two red faces."); the verbatim check still passes.
7. Access: HathiTrust (Cloudflare), PubMed Central (reCAPTCHA) and one UCLA host (TLS chain)
   were unreachable from here; the LessWrong GraphQL API works well for posts outside the
   book. I saved such posts to my scratchpad only, since the brief forbids editing other
   files and data/originals is shared.
