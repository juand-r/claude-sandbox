# Report: many-worlds-one-best-guess (batch 4c, book order 246)

Posted 2008-05-11 (from `data/originals/many-worlds-one-best-guess.md`). The last post of
"Quantum Physics and Many Worlds" in the book; the post in which the book's full assessment
of the many-worlds case is made (per the editor's instructions). Earlier notes that point
here: "Making Beliefs Pay Rent" (afterword, fourth point), "Think Like Reality",
"The World: An Introduction", "Is Reality Ugly".

## 1. The argument in three sentences (written before annotating)

1. The quantum laws that fit every microscopic experiment are, taken to hold unchanged at
   every scale, the simplest generalization of the evidence; applied to observers they put
   the observers in superposition, so many decoherent "worlds" are a consequence of the
   laws, not an extra assumption, and Occam's razor properly understood does not count
   against them.
2. The one real puzzle is the Born probabilities, which may be solved without new laws;
   a single-world theory, by contrast, needs an unmotivated new law, and by Bell's theorem
   any single-world theory must have one measurement influence another faster than light,
   violating special relativity, while non-realism only evades the question.
3. So, with explicit hedges (an unknown effect "in the 20th decimal place", a possible
   hidden assumption in the relativity argument), the author puts one world about as
   likely as spinning black holes violating conservation of angular momentum, declares
   that many-worlds "wins outright", and blames its non-acceptance on historical accident
   and physicists' poor grasp of Occam's razor.

## 2. Sources checked

All saved in `data/sources/4c_many-worlds-one-best-guess/` unless stated. SEP pages fetched
with curl on 29 Sep 2026 and converted to text (`sep_*.txt`).

| Claim / quotation in our text | Source | Exact words matched |
|---|---|---|
| Goodman's "new riddle of induction", *Fact, Fiction, and Forecast* | Wikipedia raw, `wp_New_riddle_of_induction.txt` | "The '''new riddle of induction''' was presented by [[Nelson Goodman]] in ''[[Fact, Fiction, and Forecast]]''" |
| Measurement problem as setting of the cat chain | SEP "Everettian Quantum Mechanics" (Barrett, rev. 2023), https://plato.stanford.edu/entries/qm-everett/ | section "2. The Measurement Problem" |
| Riedel comment, 50-micron cantilever; quote in post; "likely that the peculiar implications..."; "serious conceptual problems..." | LessWrong GraphQL, comments srooxhyPgcBfJpPRi (legacy 25700 = base36 "jtw", the post's link) and DesgpZf9EFe2G8tEh, both by JessRiedel, 7 May 2008; `riedel_comments.md` | "superposing a cantilever that is ~50 microns across"; "everytime new experimental "regimes" are probed (e.g. large velocities, small sizes, large mass densities, large energies), phenomena are observed which lead to new theories (special relativity, quantum mechanics, general relativity, and the standard model, respectively)" (post capitalizes the theory names); "I find it likely that the peculiar implications of uncollapsed hermitian evolution are simply the artifacts of using quantum mechanics outside its regime of applicability"; "there are serious conceptual problems with defining individual worlds, even emergently" |
| 16-microgram resonator, ~10^17 atoms, 2023 | PubMed 37079693 (Bild et al., Science 380:274, 2023), `pubmed_37079693_bild2023.txt` | "Schrödinger cat states of a 16-microgram mechanical oscillator"; "the ∼10^17 constituent atoms are in a superposition of two opposite-phase oscillations" |
| "empirically equivalent to orthodox quantum theory" | SEP "Bohmian Mechanics" (rev. 2025) | "the fact that Bohmian mechanics is empirically equivalent to orthodox quantum theory" |
| Deutsch: unoccupied branches are worlds; Bohmians disagree | SEP "Bohmian Mechanics" | "pilot-wave theories are parallel-universes theories in a state of chronic denial. (Deutsch 1996: 225)"; "Not surprisingly, Bohmians do not agree that the branches of the wave function should be construed as representing worlds." |
| "shows that any (single-world) account of quantum phenomena must be nonlocal" | SEP "Bohmian Mechanics" | "Bell's analysis indeed shows that any (single-world) account of quantum phenomena must be nonlocal, not just any hidden variables account" |
| "the MWI emerges as the most economical theory" | SEP "Many-Worlds Interpretation" (Vaidman, first publ. 2002, rev. 17 Jun 2026), 7.1 | "From this perspective, the MWI emerges as the most economical theory." |
| Hemmo and Shenker: "irrelevant, since..." | same, 7.1 | "they argue that this advantage is irrelevant, since the MWI postulates alone are not enough to explain our experience" |
| preferred basis "is no longer considered a serious objection" | same, 7.2 | "the problem of preferred basis is no longer considered a serious objection; see Wallace (2010a)" |
| "arguably the most serious difficulty" | same, 7.4 | "The issue, termed the "incoherence" probability problem by Wallace (2003), is arguably the most serious difficulty. How can probability exist if all possible outcomes occur?" |
| Deutsch–Wallace critics; "continues in a flurry of mostly critical papers" | same, 4.3 | "criticism turned to the decision-theoretic assumptions being made; see Lewis (2010), Albert (2010), Kent (2010), and Price (2010). The analysis of the Deutsch-Wallace program continues in a flurry of mostly critical papers" |
| Papineau: "is at no disadvantage either" | same, 7.4 | "even if MWI holds no advantage over other interpretations regarding the derivation of the Born rule, it is at no disadvantage either" |
| "measure of existence"; "involves adding a postulate" | same, 7.4 | "accepting the idea of probability being proportional to the measure of existence of a world resolves this problem. Although this involves adding a postulate, we do not complicate the mathematical part (i) of the theory" |
| collapse models: "minute violations of energy conservation"; "some, though not all, of these models" | same, 6 | "predict additional observable effects, such as minute violations of energy conservation"; "successfully ruling out some, though not all, of these models (see Vinante et al. (2020))" |
| "the wrong type of object" (Bell, Maudlin) | same, 7.3 | "Bell (1987, p. 201) felt that either the wave function is not everything or it is not right"; "the argument, led by Maudlin (2010), that this is the wrong type of object" |
| GRW: "is subjected, at random times, to random and spontaneous localization processes" | SEP "Collapse Theories" (rev. 2025) | "each elementary constituent of any physical system is subjected, at random times, to random and spontaneous localization processes" |
| Tumulka 2006 relativistic GRW (also for my own reading) | SEP "Collapse Theories", section 9 | "the first proposal of a relativistic dynamical reduction mechanism, which satisfies all relativistic requirements. In particular it is free from divergences and foliation independent. However, it is formulated only for systems containing a fixed number of noninteracting fermions." |
| "it is possible to formulate a fully relativistic dynamical collapse theory"; Dove (1996), Tumulka (2006) | SEP "Bell's Theorem" (rev. 2024), 8.2 | "Indeed, it is possible to formulate a fully relativistic dynamical collapse theory. A relativistic generalization of the Ghirardi-Rimini-Weber (GRW) theory was constructed by Dove (1996) and, independently, by Tumulka (2006)." |
| "must invoke a distinguished foliation" | same, 8.2 | "Theories of this sort, therefore, must invoke a distinguished foliation." |
| "is symmetric, and does not require that one of the events be in the past of the other" | same, 8.2 | "A stochastic theory, such as a dynamical collapse theory, must involve correlations between spacelike separated events. A relation like that, however, is symmetric, and does not require that one of the events be in the past of the other." |
| retrocausality: Costa de Beauregard, Price, Cramer; superdeterminism as common cause | same, 8.1, 8.1.1 | "This avenue was suggested by Costa de Beauregard (1977)"; "advocated by Price and Wharton"; "Transactional Interpretation of quantum mechanics (Cramer 1986, 1988, 2016...)"; "suppose a common cause in the past that determines both experimental settings and experimental outcomes ... superdeterminism" |
| "There is no consensus that collapse necessarily involves action at a distance" (read, not quoted in our text) | SEP "Many-Worlds", 5 | "There is no consensus that collapse necessarily involves action at a distance; see Myrvold (2016) for arguments that it does not." |
| Lab-frame bound ~2/3 × 10^7 c | Scarani, Tittel, Zbinden, Gisin, arXiv quant-ph/0007008 (Phys. Lett. A 276, 2000), `arxiv_quant-ph_0007008.pdf/.txt`, footnote 19 | "We thus obtained in the G-frame \|vQI,min (Lab)\| ≈ 2/3 10^7 c" (pdftotext prints "23 107 c"; with -bbox the "23" is a 4-pt-wide, 14-pt-tall glyph group, i.e. a stacked fraction 2/3; a search-engine summary of the paper also gives "2/3 × 10^7 c"). Abstract: "We set a lower bound for the speed of quantum information in this frame [CMB] at 1.5 x 10^4 c." |
| "did not observe any disappearance of the correlations" | PubMed 11909434 (Stefanov, Zbinden, Gisin, Suarez, PRL 88:120404, 2002), `pubmed_11909434_stefanov2002.txt` | "when both analyzers are in relative motion such that each one, in its own inertial reference frame, is first to select the output of the photons ... We did not observe any disappearance of the correlations, in agreement with quantum mechanics." |
| QBists "reject any such non-local influences" | SEP "Quantum-Bayesian and Pragmatist Views of Quantum Theory" (rev. 8 Sep 2026), 1.4 | "QBists use their view of measurement-as-experience to reject any such non-local influences." |
| Nature 2025 survey: 36% Copenhagen, 15% many worlds, >1,100 respondents; "comes from historical accident, rather than its strengths" | Nature 643, 1175 (2025), paywalled; text read in the Scientific American reprint, `sciam_survey.txt` (https://www.scientificamerican.com/article/physicists-divided-on-what-quantum-mechanics-says-about-reality/); cross-checked with thequantuminsider.com summary (`tqi_survey.txt`) | "The responses — numbering more than 1,100"; "The largest chunk of responses, 36%, favoured the Copenhagen interpretation"; "Then, in 1957, US physicist Hugh Everett came up with a wilder alternative, one that 15% of survey respondents favoured"; "But others argue that Copenhagen's emergence as the default comes from historical accident, rather than its strengths." Nature's correction of 12 Aug 2025 (`nature2025_survey_clean.txt`, from the 4a source folder) says the survey option grouped many worlds with consistent histories; hence "about 15 per cent" in our note. |
| Tegmark poll 17% (published 1998); Schlosshauer et al. 18% of 33, July 2011 | arXiv 1301.1069, `data/sources/4a_the-world-an-introduction/arxiv_1301.1069.txt` | "In Tegmark's poll [1], the Everett interpretation received 17% of the vote"; "[1] M. Tegmark, Fortschr. Phys. 46, 855 (1998)"; "d. Everett (many worlds and/or many minds): 18%"; "b. Copenhagen: 42%"; "held in July 2011" |
| DeWitt "became an ardent proponent" (1970) | SEP "Everettian Quantum Mechanics", section 7 | "DeWitt became an ardent proponent of the many-worlds interpretation"; "DeWitt (1970) emphasized..." |
| SEP many-worlds entry first published 2002 | SEP "Many-Worlds Interpretation" header | "First published Sun Mar 24, 2002" |

## 3. Arithmetic

- Bell example (post: 11.6 per cent). For photons prepared with opposite polarizations
  ("Spooky Action at a Distance", which uses the same 20° case and 11.6%), the probability
  that the two observers record the same result with bases 20° apart is
  P(A trans, B trans) + P(A abs, B abs) = ½ sin²20° + ½ sin²20° = sin²20° =
  (0.34202)² = 0.11698, i.e. 11.7 per cent. The post's 11.6 is a truncation; well under the
  one-fifth threshold, so no note beyond giving the value.
- Speed bound: 2/3 × 10^7 = 6.67 × 10^6, so "six million times as fast as light" is a
  slight understatement of a lower bound. Consistent with the post.
- "fifty years ago": Everett 1957; post 2008; 51 years. Fine.
- "Ten days earlier": "The Born Probabilities" Posted 2008-05-01; this post 2008-05-11.
- Polls: 17% (Tegmark, published 1998), 18% (2011), about 15% (2025) → "15 to 18 per
  cent ... from 1998 to 2025" in afterword and honest.

## 4. Claims about other posts

- "The Born Probabilities" (`data/originals/the-born-probabilities.md`, fetched this session,
  id 3ZKvf9u2XEWddGZmS, Posted 2008-05-01): "What's the probability that Hanson's
  suggestion is right? I'd put it under fifty percent"; "A major problem with Robin's
  theory is that it seems to predict...". Also "Hence Robin's cheery phrase, "mangled
  worlds"" (source of the term).
- "Spooky Action at a Distance: The No-Communication Theorem" (fetched, id
  DY9h6zxq6EMHrkkxE): "Suppose we've got oppositely polarized photons A and B, and you're
  about to measure B in the 20° basis"; "Now, apparently, the probability that you'll see B
  transmitted is 11.6%."
- "Decoherence is Simple" (in collection): the formal Occam argument ("Solomonoff
  induction", "Minimum Message Length"). Our notes only point to it.
- "Decoherence is Falsifiable and Testable": the comment thread where Riedel's comments are.
- "Quantum Non-Realism": pointed to for the non-realism dispute; not characterized.
- Also fetched for context: "Bell's Theorem: No EPR 'Reality'" (AnHJX42C6r6deohTG),
  "Where Physics Meets Experience" (WajiC3YWeJutyAXTn). Not cited.

## 5. Not verified

- The Nature survey article itself is paywalled; figures taken from the Scientific American
  reprint of the same article, plus a second secondary summary. The survey's methodology
  and data (said to be online) were not read.
- Dove (1996), Tumulka (2006), Myrvold (2016), Hemmo and Shenker (2022), Albert/Kent/Price
  (2010), Maudlin (2010): known only through the SEP entries that cite them.
- Whether Bouwmeester's 50-micron experiment was completed was not checked; the note only
  sources the post's hedged "Apparently" and gives a later, larger result.
- The post's claim that the Born rule is the unique rule without a split-remerge problem:
  not checked (the note says only that no derivation or source is given).
- The black-hole angular momentum point ("so far as I know" unchecked in 2008): not
  pursued; hedged, and not needed for any note.

## 6. Judgment calls for the editor

1. Scope of the assessment. As instructed, this is the full statement. The case is split
   into two premises: (a) worlds are a "logical consequence" of universal unitary laws;
   (b) any single world "would violate Special Relativity". Notes grant what the literature
   grants (MWI most economical if laws are counted; any single-world theory is nonlocal;
   Bohm-type theories need a preferred foliation) and dispute only (a) as stated (needs
   wavefunction completeness; Bohm counterexample) and (b) as stated (relativistic GRW,
   Dove 1996 / Tumulka 2006). I avoided "wrong" or "refuted" for either; the words used are
   "disputed", "overstated", "only with a further premise".
2. Balance of sources. The SEP many-worlds entry (Vaidman) argues for the view; I use it
   for the concessions against interest ("most serious difficulty", "adding a postulate")
   and for the preferred-basis claim in its favour, and say in the note that the entry
   argues for the view. The Bell and Bohm entries are neutral surveys.
3. Motive notes. Two notes object to motive attributions made by the post, not by us:
   "betrays a sentimental attachment" (L71 cpara) and "The only reason ... do not have a
   mathematical grasp" (L119 clogic). The "dare not say it"/tenure paragraph (L121) gets
   "No evidence is given". The "In short" line summarizes these as "puts the remaining
   disagreement down to the ignorance, fear and sentiment of those who disagree" — please
   check that this passes the fair-defender test; I think each word is backed by a
   passage (grasp of Occam's razor; "dare not say it"/tenure; "sentimental attachment").
4. "Overstated by the post's own account" (L95, "disproved"): the evidence is the post's
   own hedge one paragraph earlier plus the Bohm empirical-equivalence point.
5. Riedel: the post quotes Riedel only for the history-of-physics sentence; our note adds
   that Riedel used it to argue against many-worlds. I changed an earlier draft
   ("the opposite conclusion") to "used the point against the post's view".
6. Reserved-word flag: "cannot be proved wrong" (L19 cpara) paraphrases the post's own
   "we can't prove they're wrong". Kept.
7. Honest section is 930 words by raz_check's count (header included), slightly over the
   "about 900" allowance.
8. Consistency with earlier notes: the afterword of "Making Beliefs Pay Rent" says the case
   "rests on Occam's razor"; this post's case rests on Occam's razor and on the relativity
   argument. Not contradictory, but the pointers in "Making Beliefs Pay Rent", "Think Like
   Reality", "The World: An Introduction" and "Is Reality Ugly" could now point here
   ("see the notes on 'Many Worlds, One Best Guess'"). I did not edit them.
9. Overlap with neighbours (drafts seen, not edited): "Decoherence is Simple",
   "Decoherence is Falsifiable and Testable" and "Privileging the Hypothesis" already use
   Bohm, Vaidman's "adding a postulate", and Hemmo and Shenker, and point here for the full
   comparison. My notes agree with theirs on every fact I saw. Observation: the preview of
   `decoherence-is-simple` currently fails on a Unicode ≤ (another agent's file, in progress).
10. Neutral clarifications of text lost in conversion ("spin 12" = spin 1/2; "1030th" =
    10^30th) are in cpara notes, as reading aids, not criticisms.
