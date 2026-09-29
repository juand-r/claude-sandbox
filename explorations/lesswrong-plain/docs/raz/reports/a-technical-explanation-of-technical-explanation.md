# Report: A Technical Explanation of Technical Explanation (order 261)

Batch 4d, Science and Rationality. Posted 2005-01-01 (first on yudkowsky.net); the text
annotated is the book revision now on LessWrong.

## 1. The argument in three sentences

A belief is a probability distribution over future experiences, and it should be scored by
the logarithm of the probability it gave to what happened, the one rule that rewards honest
probabilities and gives the same total however experiments are grouped; under that rule a
bold, precise hypothesis gains a large likelihood advantage when it is right, and a
hypothesis that "fits" any outcome is no better than ignorance. A "technical" explanation is
one that concentrates probability on specific outcomes in advance, while a "verbal" one runs
on after-the-fact feelings of fit; but vaguer ("semitechnical") theories such as
nineteenth-century evolution can still win, advance prediction is a social rule of science
rather than a law of probability, and critics of a confirmed theory must say exactly what it
predicts badly. The same scoring view reframes Popper's falsifiability as a quantitative
matter, requires never assigning probability 1, and implies that you cannot give a good
explanation of an event (a blue tentacle) that you do not in advance anticipate.

Files: `annotated/posts/a-technical-explanation-of-technical-explanation.tex` (165 `\cpara`,
5 `\clogic`, 2 `\cfact`; the notes were inserted by
`data/sources/4d_a-technical-explanation-of-technical-explanation/insert_notes.py`, which holds
the same text), `annotated/afterwords/...tex`, `honest/sections/...tex`. Scratch and sources:
`data/sources/4d_a-technical-explanation-of-technical-explanation/`.

Density: the checker counts 225 `\flushnotes` lines. The 60 without a `\cpara` are formula
lines of the worked examples (P(color) = ..., = $0.27 ., Score(red) = ...), one-line bridges
("The flip side:", "Why not assign a probability of 1.0?", "Spoiler space"), the three lines
of the closing verse, the Democritus and Kelvin attribution lines, the one-line "History
records who won.", and citation-only footnotes (all but footnote 3, which gets a note).

## 2. Sources checked (outside quotations and figures)

All fetched with curl (User-Agent "raz-annotation-research") and saved in the folder above.

| Claim in notes | Source (file) | Exact words matched |
|---|---|---|
| Brier's multi-category rule is proper, binary form only for binary | en.wikipedia.org "Brier score" (`wiki_Brier_score.txt`, line 31) | "the original definition by Brier is applicable to multi-category forecasts as well as it remains a proper scoring rule, while the binary form (as used in the examples above) is only proper for binary events" |
| Only log is strictly proper and local for non-binary outcomes; Murphy (1973) decomposition | Wikipedia "Scoring rule" (`../4a_the-quotation-is-not-the-referent/wiki_scoring_rule.txt`, lines 112, 116-120) | "Affine functions of the logarithmic scoring rule are the only strictly proper local scoring rules on a finite set that is not binary."; decomposition into "uncertainty, reliability, and resolution" citing Murphy, A.H., 1973 |
| Good (1952) proposed the log rule | arXiv 2104.01000 (`arxiv_2104.01000.pdf`, `b.txt` lines 36-38, 205) | "logarithmic scoring rule proposed by Good (1952)"; "Irving J Good. Rational decisions. Journal of the Royal Statistical Society, Series B, ... 14: 107–114, 1952." |
| Fischhoff et al. million-to-one, 9:1 | Yudkowsky 2008 chapter (`data/sources/CognitiveBiases.txt`, lines 559-567), quoting Slovic, Fischhoff and Lichtenstein (1982, 472) | "For answers assigned odds of 1,000,000:1 or greater, accuracy was 90%; the appropriate degree of confidence would have been odds of 9:1" |
| Classical statistics violates the likelihood principle; likelihoodism; AIC | SEP "Philosophy of Statistics" https://plato.stanford.edu/entries/statistics/ (`sep_statistics.txt`) | "two problems with the classical approach are outlined, to wit, its problematic interface with belief and the fact that it violates the so-called likelihood principle"; "likelihoodism (Hacking 1965, Edwards 1972, Royall 1997)"; "AIC[M] = - 2 log P(s | h) + 2d ... d = dim(Θ) is the number of dimensions of the parameter space" |
| Lakatos: protective belt; "look for another heavenly body" | SEP "Imre Lakatos" https://plato.stanford.edu/entries/lakatos/ (`sep_lakatos.txt`) | "It is this protective belt of auxiliary hypotheses which has to bear the brunt of tests and gets adjusted and re-adjusted, or even completely replaced, to defend the thus-hardened core. (FMSRP: 48)"; "the positive heuristic of the Newtonian programme bids us look for another heavenly body whose gravitational force might be distorting the first planet's orbit" |
| 10^14 figure traced to Penrose | arXiv astro-ph/0003192 (Skalský) (`a.txt` lines 1297-1298) | "The results of twenty-year observations of the pulsar PSR 1913+16 are consistent with the predictions of the general theory of relativity with preciseness of 10-14 (Penrose 1997)." A weak secondary source; I found no primary text. |
| Hulse-Taylor orbital decay 0.997 ± 0.002 | Wikipedia "Hulse–Taylor pulsar" (`wiki_Hulse_Taylor_pulsar.txt`, line 42) | "The ratio of observed to predicted rate of orbital decay is calculated to be 0.997 ± 0.002." (citing Weisberg, Nice and Taylor 2010) |
| Dennett's reason | Dennett, Darwin's Dangerous Idea, PDF at inf.fu-berlin.de (`dennett_dda.txt`, lines 597-601) | "If I were to give an award for the single best idea anyone has ever had, I'd give it to Darwin, ahead of Newton and Einstein and everyone else. In a single stroke, the idea of evolution by natural selection unifies the realm of life, meaning, and purpose with the realm of space and time, cause and effect, mechanism and physical law." |
| Darwin's elephants and Weald (1st edition) | Project Gutenberg #1228, the 1859 first edition (`gutenberg_1228_origin.txt`, lines 2195-2201, 8697-8699) | "at the end of the fifth century there would be alive fifteen million elephants, descended from the first pair"; "the denudation of the Weald must have required 306,662,400 years; or say three hundred million years." (Gutenberg lists #1228 as "1859, First Edition".) |
| Kelvin quotation | zapatopi.net/kelvin/quotes/ (`zapato_kelvin.txt`) | "The limitations of geological periods, imposed by physical science, cannot, of course, disprove the hypothesis of transmutation of species; but it does seem sufficient to disprove the doctrine that transmutation has taken place through 'descent with modification by natural selection.'" ["Of Geological Dynamics", 1869] |
| Huxley 1869 | Wikipedia "Age of Earth" (`wiki_Age_of_Earth.txt`, "Early calculations") | "In a lecture in 1869, Darwin's great advocate, Thomas Henry Huxley, attacked Thomson's calculations, suggesting they appeared precise in themselves but were based on faulty assumptions." (Wikipedia's words, and the note says so.) |
| Mill, Keynes, Lipton, Whewell, Maher on prediction | SEP "Prediction versus Accommodation" (`../4c_decoherence-is-falsifiable-and-testable/sep_prediction.txt`) | Keynes 1921: "The peculiar virtue of prediction or predesignation is altogether imaginary…"; "John Stuart Mill (in his debate with Whewell) categorically denied this claim"; "the 'fudging explanation' defends predictivism ... (Lipton 1990, 1991: Ch. 8)"; "Whewell maintained that predictions carry special weight"; Maher: "persuasive evidence that the predictor 'has a reliable method'" |
| Old evidence, Glymour, Mercury | SEP "Bayesian Epistemology" (`data/sources/sep_bayesian_epistemology.txt`) | "the old data about the advance of Mercury's perihelion confirmed Einstein's new theory; this is Glymour's problem of old evidence" |
| Punctuated equilibrium from Mayr | Wikipedia "Punctuated equilibrium" (`wiki_Punctuated_equilibrium.txt`, line 114) | "Punctuated equilibrium originated as a logical consequence of Ernst Mayr's concept of genetic revolutions by allopatric and especially peripatric speciation as applied to the fossil record." |
| Mercury 5557 / 5600 / 43 | Kevin Brown, mathpages "Reflections on Relativity" 6.2 https://www.mathpages.com/rr/s6-02/6-02.htm (`mathpages_6-02.txt`) | "this accounts for 5557 arc seconds per century, which is close to the observed value of 5600, but still short by 43 arc seconds per century" |
| Neptune within 1 degree | Wikipedia "Discovery of Neptune" (`wiki_Discovery_of_Neptune.txt`, line 53) | "less than 1 degree from the position Le Verrier had predicted" |
| Vulcan | pointer to the note on An Intuitive Explanation (not re-quoted) | — |
| Popper SEP quotation in the post | SEP archive win2002 https://plato.stanford.edu/archives/win2002/entries/popper/ (`sep_popper_win2002.txt`) | The post's three quoted paragraphs match word for word after removing punctuation (script in this session); the post's ". . ." cuts "The Marxist account of history too ..." and ", and one genuine counter-instance falsifies the whole theory". |
| Popper: improbable theories better; "tested and falsified, but never logically verified" | same archived entry | "the more improbable a theory is the better it is scientifically, because the probability and informative content of a theory vary inversely"; "As such it can be tested and falsified, but never logically verified." |
| Crackpot Index entry | https://math.ucr.edu/home/baez/crackpot.html (`baez_crackpot.txt`, lines 61-63) | "10 points for arguing that while a current well-established theory predicts phenomena correctly, it doesn't explain "why" they occur, or fails to provide a "mechanism"." (The note renders the inner double quotes as single quotes, since the whole is inside a quotation.) |
| Halley's comet | Wikipedia "Halley's Comet" (`wiki_Halley27s_Comet.txt`, lines 68, 70, 74) | "in his 1705 Synopsis of the Astronomy of Comets, used Newton's new laws"; "not seen until 25 December 1758"; "This effect was computed before its return (with a one-month error to 13 April) by ... Alexis Clairaut, Joseph Lalande, and Nicole-Reine Lepaute"; "It was also one of the earliest successful tests of Newtonian physics" |
| Cromwell's rule, Lindley | Wikipedia "Cromwell's rule" (`wiki_Cromwell27s_rule.txt`, line 4) | "Cromwell's rule, named by statistician Dennis Lindley" |
| Kimura 1968 neutral theory | Wikipedia "Neutral theory of molecular evolution" (`wiki_Neutral_theory_of_molecular_evolution.txt`, line 13) | "The theory was introduced by the Japanese biologist Motoo Kimura in 1968" |

The raz_check "quote not in post" flags are all either titles of sources (Brier score,
Rational Decisions, Philosophy of Statistics, Age of Earth, Discovery of Neptune, Halley's
Comet, Hulse--Taylor pulsar, Cromwell's rule, Prediction versus Accommodation, Of Geological
Dynamics), terms ("fudging explanation", "problem of old evidence"), or the quotations in the
table above. One flag is the post's own verse, "Since the beginning / Not one unusual thing /
Has ever happened," which is in the post on three lines (the slashes mark the line breaks).

## 3. Arithmetic recomputed

Script: `data/sources/4d_.../check_numbers.py` (pure Python; the venv has no numpy/scipy, so
optimization over the simplex is by grid search at step 0.001, checked against the analytic
Lagrange solution). Output saved as `check_numbers_output.txt`. Key results:

- Linear rule: 0.6·0.6 + 0.2·0.2 + 0.2·0.2 = 0.44; 0.4·0.3 + 0.5·0.2 + 0.1·0.5 = 0.27;
  optimum all on red (0.5); 0.5^5 = 0.03125. All as in the post.
- Squared error on the winning bet only, three colours, F = (0.3, 0.2, 0.5): expected payoff
  Σ F_i (1 − (1 − p_i)^2). Lagrange: 2F_i(1 − p_i) = λ, so p_i = 1 − λ/(2F_i); Σp_i = 1 gives
  λ/2 = 2/Σ(1/F_i) = 0.1935 and p = (0.3548, 0.0323, 0.6129). Grid search agrees
  (0.355, 0.032, 0.613), payoff 0.6129 against 0.6000 for honest bets. So the rule is not
  proper for three colours. Full Brier (squared error on every colour): optimum (0.3, 0.2,
  0.5), proper. Two colours (footnote 3): argmax at p = f for f = 0.3, 0.6, 0.9, and
  analytically d/dp = 2f(1 − p) − 2(1 − f)p = 2(f − p). Correct.
- Log rule: optimum (0.3, 0.2, 0.5). Invariance: f(xy) = f(x) + f(y) with f continuous on
  (0, 1] gives f = c·log (substitute g(t) = f(e^−t), Cauchy's additive equation).
  0.6 × 0.25 = 0.15. dB(0.01) = −20, dB(0.03) = −15.2; log2 0.25 = −2, log2 0.03 = −5.06.
  Expected score for (0.25, 0.5, 0.25) = −1.5 bits. 995/1000 = 99.5%.
- Ten questions: 2^−10 = 0.000977; 0.9^8·0.1^2 = 0.0043; 0.8^8·0.2^2 = 0.0067 (post: "0.006
  or 0.6%", under the threshold, mentioned in the cpara only as the post's figure);
  0.99^10 = 0.904, −0.44 dB (−0.46 using 0.90), −0.145 bits. Post: −0.45 dB, −0.15 bits.
- Coin: 2^20 = 1,048,576, −20 bits, −60.2 dB. Fixed coin: prior 0.01/1024 = 9.8e−6
  ("a thousandth of one percent"); posterior after one run exactly 0.01; after a second
  identical run odds 10.34:1. 2^30 = 1.07e9.
- Precise vs vague: 1/990 = 0.00101; LR 10; 10/11 = 0.909. Prior 1:10 → 0.9:0.9.
- Vague vs ignorance, prior 1:20: after one 51 the odds are 0.09:0.20 = 9:20 (post 10:20);
  after two, 4.05:1 = 80.2% (post 10:2 = 83%). Under the threshold; the cpara says the post
  rounds 9 up to 10.
- 1:10:200 → 0.47%, 4.74%, 94.79%; class weights 0.25/100 : 0.25/10 : 0.5 = 1:10:200.
  After 51: 0.9 : 0.9 : 2 = 9:9:20. After 51, 51: 810:81:20 = 88.9%, 8.9%, 2.2%.
- Stupid theory: P(51) = 0.1/90 = 0.00111; posterior 0.29% (0.26% with the post's 0.1%);
  post "0.2%". Under the threshold; report only.
- 52, 51, 58: precise 9e−7 (−60.5 dB), vague 7.29e−4 (−31.4), ignorant 1e−6 (−60),
  stupid 1.37e−9 (−88.6). Priors (of 221): −23.4, −13.4, −0.4, −13.4 dB. Totals −83.9,
  −44.8, −60.4, −102.1. Vague highest, as the post says (post: −43).
- 80% predictions: expected gain per question over a 50% guesser, 0.8·log2 1.6 +
  0.2·log2 0.4 = 0.278 bits.
- Sun: 0.999^365 = 0.694, −0.527 bits (post "roughly −0.52"), two years −1.05 bits > 1 bit;
  0.9999^365 = 0.9642; 70 years 0.0777 (post 7.75%); 0.99999^25550 = 0.7745; 1e−5 = −50 dB;
  1 − 0.5/3652.5 = 0.99986 (post 99.98%).
- Tentacle: 1e6·1e−3·1e−2 = 10; 1e6·1e−2·1e−1 = 1000; 1e15·1e−9 = 1e6.
- Mercury: 5600 − 5557 = 43. Codons: 4^3 = 64.

## 4. Claims about other posts

- "Qualitatively Confused" (order 199): its note already says "For more than two outcomes,
  it and its linear rescalings are the only strictly proper rules that depend only on the
  probability given to what happened; for two outcomes, as here, others such as the Brier
  score (1950) are proper too." My squared-error note points there and adds the failure of
  the post's winner-only rule, which is new.
- "An Intuitive Explanation of Bayes's Theorem" (order 183): its notes carry Popper in full
  ("no conclusive disproof of a theory can ever be produced"; "corroborated") and Vulcan
  ("Le Verrier proposed an unseen planet, Vulcan, rather than give up Newton"). Pointed to,
  not repeated. My Popper note here is framed differently: in this post the claim that
  Popper saw falsification as different in kind is accurate, so the note says so.
- "Decoherence is Falsifiable and Testable" (order 239): its note gives predictivism, Popper
  and Maher ("Barnes's Stanford Encyclopedia entry describes Patrick Maher's 'Bayesian
  analysis of its predictivist implications'"). Pointed to.
- "My Wild and Reckless Youth" (order 43): its note gives the old-evidence problem ("the
  'problem of old evidence' (Glymour, 1980)"). Pointed to.
- "Fake Causality" (order 36): phlogiston "forbade outcomes" and Priestley's 1783 prediction.
  Pointed to.
- "Absolute Authority" (order 59): the Fischhoff, Slovic and Lichtenstein figure. Pointed to;
  I re-read the figure in CognitiveBiases.txt.
- "0 And 1 Are Not Probabilities" (order 62), "The Tragedy of Group Selectionism" (138),
  "Belief in Belief" (15), "Conservation of Expected Evidence" (29): neutral pointers only.
- Dates for the revision note: Conservation of Expected Evidence 2007-08-13, Fake
  Explanations 2007-08-20, Lawful Uncertainty 2008-11-10, Joy in the Merely Real 2008-03-20
  (manifest). The post's footnotes date Zapato 2008, Imagination Engines 2011, Brown 2011.

## 5. Not verified

- The Yates et al. quotation (Heuristics and Biases chapter): not found online. Said so in
  the note.
- Spee's "The investigating committee would feel disgraced ..." sentence: not in the
  Conservation of Expected Evidence original, and I had no copy of Hellyer's translation.
  Said so in the note.
- What quantity Penrose's 10^14 measures: the only source I found is a secondary citation.
  The note says so.
- The "95% shared genetic material" figure (an estimate that counts insertions and
  deletions; single-base estimates are higher). Not checked, not noted: the post's point does
  not depend on it.
- Adams's own precision for Neptune ("within one degree" is stated for both Le Verrier and
  Adams; I checked only Le Verrier's). Not noted.
- Kelvin's "three thousand years on chemical energy" figure. Not checked; the 20 to 40
  million years for gravitational energy agrees with Wikipedia (Kelvin–Helmholtz, Age of
  Earth).
- The Democritus rendering (from a popular book), the Imagination Engines sales literature,
  the source of the closing verse. Not checked.

## 6. Judgment calls for the editor

1. Reserved words: "Not proper" (squared-error note, Response) rests on a derivation and a
   script; I am confident. "The opposite" (Popper preferring improbable theories vs the
   Bayesian preference for the higher posterior; Whewell/Maher vs Mill/Keynes) rests on the
   SEP texts. "Never" appears only in paraphrases of the post or of Popper, and "Vulcan was
   never found". "Wrong" only describes the post's own examples ("wrong twice", "wrong
   range").
2. "Overstated" for Neptune as "the first" confirmed advance prediction (Halley's comet) and
   for "without a scrap of quantitative modeling" (Darwin's Weald and elephant estimates). A
   defender could say the Weald estimate is geology, not evolutionary modeling; the note
   says only that it "bears on" the age question and that the contrast with physics stands.
3. The classical-statistics note ("loosely described"): the post's "sometimes called" is a
   hedge on the name, not on the description. I judged the description itself fair game.
4. The Lakatos note on "defending hypotheses": the post's "defend" means an effort to prevent
   disproof, and a defender could say Le Verrier was testing, not defending. The note states
   Lakatos as the rival account, in the SEP's words, and does not say the post contradicts
   itself.
5. The tentacle note ("Stated too strongly ... true only in that second sense"). The post's
   next sentence (would they "go to sleep wondering") supports the second reading; I kept
   the note because "necessarily violates" is stated without the condition.
6. The old-evidence and predictivism notes are information about rival views, as the brief
   asks; both are pointers to fuller notes elsewhere. The Response says the post takes a side
   "without saying there is a dispute"; that is a scope point.
7. Possible nitpicks the editor may cut: the Dennett paraphrase note (the post does not quote
   Dennett), the Kimura and Murphy credit sentences, the 10^14 note (a secondary source only).
8. Honest section is 1,345 words with 15 n.b. notes (the brief allows about 1,500). The
   Response is 594 words (allowed about 600).
9. Build: `annotated/preview.sh posts a-technical-explanation-of-technical-explanation`
   fails on the shared preamble: the post text contains U+2211 (∑, three times) and
   U+10FC09 (a private-use character before "∑ P × log (P )"). I did not edit the preamble
   (brief: only my files). With these two lines added to a copy of the preamble
   (`previewtest/preamble_extra.tex`) the post and afterword build, 34 pages, with four
   overfull boxes (0.1pt, 3pt, and two of 24pt in footnotes 11 and 14, which are bare URLs in
   the post's own text):
   `\DeclareUnicodeCharacter{2211}{\ensuremath{\sum}}`
   `\DeclareUnicodeCharacter{10FC09}{}`
