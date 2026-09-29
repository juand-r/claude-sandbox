# Report: decoherence-is-falsifiable-and-testable

Batch 4c, Quantum Physics and Many Worlds, book order 239. Posted 2008-05-07.

## 1. The argument in three sentences

The post splits two ideas that "falsifiable" and "testable" often blur: falsifiability, a
property of one hypothesis (does it concentrate its probability so that some outcomes would
nearly refute it?), and testability, a relation between two (is there an outcome whose
probability differs under them?). Decoherent (many-worlds) quantum mechanics is falsifiable
in the first sense, and in the second sense any untestability relative to collapse is
symmetric, since Bayes's theorem does not care which theory came first; useless
complications should be rejected for being useless, not for being new, and by that rule the
collapse postulate, not the many worlds, is the extra part. The many worlds are not an added
claim but a deductive consequence of the tested wave equation applied universally, so they
cost no extra probability, and the arguments that exclude decoherence as extra entities,
untestable or lacking new predictions are errors of probability theory.

## 2. Sources checked

All fetched with curl (generic User-Agent), HTML stripped to text; files in
`data/sources/4c_decoherence-is-falsifiable-and-testable/` unless noted.

- Popper, "Science: Conjectures and Refutations" (lecture 1957, in Conjectures and
  Refutations, 1962/63), https://bertie.ccsu.edu/naturesci/PhilSci/PopperArticle.html, reused
  from `data/sources/b2b_death_spirals/popper_ccsu.txt`. Matched: "Testability is
  falsifiability; but there are degrees of testability"; "the criterion of the scientific
  status of a theory is its falsifiability, or refutability, or testability"; "The more a theory
  forbids, the better it is."; "The two psycho-analytic theories were in a different class. They
  were simply non-testable, irrefutable. There was no conceivable human behaviour which could
  contradict them."; "(2) Confirmations should count only if they are the result of risky
  predictions; that is to say, if, unenlightened by the theory in question, we should have
  expected an event which was incompatible with the theory". The post's Popper claim (Freud
  "equally good at coming up with an explanation for every possible thing") matches in
  substance; Popper's word is "irrefutable"/"non-testable", not "unfalsifiable", and his
  example is two men and a drowning child, not a patient. Neither difference changes the
  meaning, so no critical note.
- Barnes, SEP "Prediction versus Accommodation" (rev. 23 Sep 2022),
  https://plato.stanford.edu/entries/prediction-accommodation/ (`sep_prediction.txt`).
  Matched: "Popper held that it was impossible to show that a theory was even probable based on
  the evidence, for he embraced Hume's critique of inductive logic"; "Karl Popper is probably the
  most famous proponent of prediction in the history of philosophy"; "Patrick Maher (1988, 1990,
  1993) presented a seminal thought experiment and a Bayesian analysis of its predictivist
  implications"; "Maher argues that the successful prediction of the initial 99 flips constitutes
  persuasive evidence that the predictor 'has a reliable method'". Also "7. Anti-Predictivism"
  (Keynes), not used.
- Vaidman, SEP "Many-Worlds Interpretation of Quantum Mechanics" (rev. 17 Jun 2026),
  https://plato.stanford.edu/entries/qm-manyworlds/ (`sep_mwi.txt`). Section 6: "It is
  frequently claimed (e.g., by DeWitt (1970)) that the MWI is, in principle, indistinguishable
  from an ideal collapse theory. This is not the case."; "These proposals remain strictly gedanken
  experiments, far beyond the reach of current or foreseeable technology"; "To date, such effects
  have not been observed, successfully ruling out some, though not all, of these models".
  Section 7.1: "the MWI emerges as the most economical theory"; "Hemmo and Shenker (2022) agree
  that the postulates of the MWI are economical ... but they argue that this advantage is
  irrelevant, since the MWI postulates alone are not enough to explain our experience."
  Section 7.4: "Although this involves adding a postulate, we do not complicate the mathematical
  part (i) of the theory"; Papineau: MWI "at no disadvantage" on the Born rule (not quoted in a note).
- Goldstein, SEP "Bohmian Mechanics" (rev. 20 Sep 2025), https://plato.stanford.edu/entries/qm-bohm/
  (`sep_bohm.txt`). Matched: "the wave function provides only a partial description of the
  system. This description is completed by the specification of the actual positions of the
  particles"; "since Bohmian mechanics involves no wave-function collapse (for the wave function
  of the universe), all of the branches of the wave function ... persist"; "As David Deutsch ...
  the 'unoccupied grooves' must be physically real"; "for anyone who, like Wallace, accepts ... the
  claim should be compelling. On the other hand, for those who reject the functional analysis ...
  the claim should seem, not merely wrong, but silly."
- Bacciagaluppi, SEP "The Role of Decoherence in Quantum Mechanics" (rev. 23 Jan 2025),
  https://plato.stanford.edu/entries/qm-decoherence/ (`sep_decoherence.txt`). Matched:
  "interactions between a system and its environment that lead to suppression of interference
  effects"; "It is thus important to consider not decoherence by itself, but the interplay between
  decoherence and the various approaches to the foundations of quantum mechanics".
- Schlosshauer, "Quantum Decoherence", Phys. Rep. 831, 1-57 (2019), arXiv 1911.06282 abstract
  (`arxiv_1911.06282.xml`): "an overview of the theory and experimental observation of the
  decoherence mechanism". Also Schlosshauer 2004 (Rev. Mod. Phys. 76, arXiv quant-ph/0312059),
  abstract only, not quoted.
- Einstein 1905, "On the Electrodynamics of Moving Bodies", English translation at
  https://www.fourmilab.ch/etexts/einstein/specrel/www/ (`einstein1905.txt`): "The introduction
  of a “luminiferous ether” will prove to be superfluous inasmuch as ...". The note quotes up to
  "superfluous" and marks that the sentence continues.
- Wikipedia, "Lorentz ether theory" (raw, `wiki_lorentz_ether.txt`), cited as Wikipedia's
  summary: "it became both empirically and deductively equivalent to special relativity"; "SR is
  widely preferred over LET, due to the superfluous assumption of an undetectable aether in LET".
- SEP "Collapse Theories" (Ghirardi and Bassi, `sep_collapse.txt`) read for background; not quoted.

## 3. Arithmetic and mathematics

- Bayes's theorem as printed (flattened): P(Ai|B) = P(B|Ai)P(Ai) / Σj P(B|Aj)P(Aj). Correct.
- "if P(B|Ai) is tiny ... likewise the posterior": holds only if Σj P(B|Aj)P(Aj) is not also tiny,
  i.e. some rival gives B a much higher probability. The post grants this ("the sum in the
  denominator has got to contain some other hypothesis"). Note 7 says so.
- Odds form: P(Ad|B)/P(Ac|B) = [P(B|Ad)/P(B|Ac)] × [P(Ad)/P(Ac)]; if the likelihood ratio ≠ 1
  and prior odds are finite and nonzero, posterior odds ≠ prior odds. Correct. The last line
  in the online text reads "≠/fracP(Ad)P(Ac)", a markup slip.
- Order independence: P(H|X,Y) computed by updating on X then Y equals Y then X (both equal
  P(X,Y|H)P(H)/P(X,Y)). Correct.
- P(Y) ≥ P(X and (X→Y)): X ∧ (X→Y) entails Y. Correct. If P(Y|X) ≈ 1 then
  P(X,Y) = P(X)P(Y|X) ≈ P(X). Correct.

## 4. Claims about other posts

- "Decoherence is Simple" (`data/originals/decoherence-is-simple.md`, 2008-05-06, order 238):
  "The decoherence (a.k.a. many-worlds) version of quantum mechanics". Used for the
  terminology note.
- "Collapse Postulates" (`data/originals/collapse-postulates.md`, 2008-05-09, order 237):
  "But experiments are steadily ruling out the possibility of “collapse” in increasingly large
  entangled systems." Written two days after this post, placed two posts before it in the book.
  Oddity for the editor: its "underway" link points to this post's own URL; the current text of
  this post says nothing about a 50-micrometer experiment.
- "The Born Probabilities" (`data/originals/the-born-probabilities.md`, 2008-05-01, not in the
  book): "One serious mystery of decoherence is where the Born probabilities come from"
  (link text "serious mystery of decoherence"). 2008-05-07 minus 2008-05-01 = six days.
- "Many Worlds, One Best Guess" (order 246): "There is no known reason for the Born
  probabilities"; discusses Hanson, Wallace and Deutsch. Only pointed to.
- "Scientific Evidence, Legal Evidence, Rational Evidence" (2007-08-19): "I am wearing white
  socks"; "Science is made up of *generalizations* which apply to many particular instances".
- "Belief in the Implied Invisible": our afterword there says "a sound argument, with correct
  physics". The spaceship reference is consistent with it.
- "An Intuitive Explanation of Bayes's Theorem" (order 183): its notes discuss the Bayesian
  reading of Popper; pointed to, not repeated.
- "Your Strength as a Rationalist": the "Popper uncredited" point does not apply here, since
  this post names Popper.

## 5. Not verified

- Maher's papers themselves (only Barnes's SEP summary). Hemmo and Shenker (only Vaidman's
  report of them, and the note says so).
- The primary experiments behind "ruling out some, though not all" collapse models (Vinante et al.
  2020 etc.); cited through Vaidman's SEP entry.
- Whether the online text's "/frac" and the missing spaces ("*strictly*simpler",
  "*single*hypothesis", "*useless*complications") are in the current LessWrong page or come from
  our conversion. raz_check flags "strictly simpler" as not in the post for this reason; the
  words are the post's.

## 6. Judgment calls

- Reserved words: "refute" appears only in describing the post's own concept of falsifiability;
  "invented" only for the order in which theories were invented. "wrong" appears only inside a
  Goldstein quotation. No reserved word is used as a charge.
- Title point (note 57, cfact 58, Response para 2, honest last n.b.): I say "testable", in the
  post's own two-hypothesis sense, is argued by symmetry, not shown, and that the missing tests
  exist and support the title. The fair defender may say the conclusion only rejects
  "untestable" as a reason for exclusion. I kept the point because the sentence asserts "nor is
  it untestable" and the post defines testability as the existence of such a B.
- "Necessarily" (Bohm note): the post says denying worlds is "necessarily" to deny universal
  quantum laws. Bohmian mechanics is my counterexample, with the dispute over its empty branches
  stated both ways. Worded as "claims more than the logic gives", not "wrong".
- "Strictly simpler" and the Born rule: this overlaps with what the agents on "Decoherence is
  Simple" (238) and "Many Worlds, One Best Guess" (246) may write. I kept it short, tied to this
  post's own words ("plus the Born probability rule"; "a collapse postulate that obeys the Born
  probabilities"), and pointed to 246. The editor may want to move the full point to one place.
- Terminology note (note 10): neutral; may duplicate a note on an earlier QM post.
- Predictivism (clogic 29, Response para 4): I state the rival view through Popper and Barnes's
  report of Maher. The claim that the post "answers it as order-dependence" rests on the post's
  own framing ("If we reject what you call 'hysteresis'").
- Ether precedent (note 55): the post's claim is hedged ("may be unique"); I give the ether as a
  close precedent and say it supports the post's rule. Lorentz's theory being empirically
  equivalent to special relativity is cited as Wikipedia's summary.
- Preview build: `annotated/preview.sh posts decoherence-is-falsifiable-and-testable` FAILS
  because the post text contains Σ (U+03A3) and → (U+2192), which `annotated/preamble.tex` does
  not declare. I did not edit the shared preamble. With these two lines added it builds (tested
  in `data/sources/4c_decoherence-is-falsifiable-and-testable/previewtest/`, 8 pages, no
  errors):
  `\DeclareUnicodeCharacter{03A3}{\ensuremath{\Sigma}}` and
  `\DeclareUnicodeCharacter{2192}{\ensuremath{\rightarrow}}`.
- Honest section is 899 words, at the upper limit given for this post.
- Helper script: `data/sources/4c_decoherence-is-falsifiable-and-testable/insert_notes.py`
  (inserts the notes into the skeleton; kept in sync with later edits).
