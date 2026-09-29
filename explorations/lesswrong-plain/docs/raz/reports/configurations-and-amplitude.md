# Report: Configurations and Amplitude (batch 4c, order 234)

## 1. The argument in three sentences

The post gives the sequence's basic picture: reality is a set of configurations, each holding a
complex amplitude, and amplitude flows between configurations by fixed rules (multiply by 1
going straight through a half-silvered mirror, by i when turned), while observed frequencies go
as the squared moduli. Working through three interferometer set-ups, it shows that amplitudes
arriving by two paths can cancel, which a particle that simply goes one way or the other
cannot reproduce, and argues that because probabilities are never negative or complex,
amplitudes are not degrees of belief. It concludes that configurations and amplitudes are real
because they have effects, and previews that true configurations range over all particles in
the universe and form a continuous space.

## 2. Sources checked

Fetched texts are in `data/sources/4c_quantum-explanations/` (shared folder for both of my slugs).

| Claim in our text | Source | Exact words matched |
|---|---|---|
| Symmetric beam splitter has factors 1 and i, times 1/√2; the dielectric one has a −1 | Wikipedia, "Beam splitter" (`wiki_beam_splitter.txt`, `https://en.wikipedia.org/w/index.php?title=Beam_splitter&action=raw`) | "The dielectric beam splitter above, for example, has τ = (1/√2)[[1, 1],[1, −1]] ... while the "symmetric" beam splitter of Loudon has τ = (1/√2)[[1, i],[i, 1]]" (matrices in LaTeX markup in the source) |
| −1 rule does not apply to metallic coatings | same, section "Phase shift" | "This does not apply to partial reflection by conductive (metallic) coatings, where other phase shifts occur in all paths (reflected and transmitted)." |
| Feynman's arrows | Wikiquote, Richard Feynman, *QED* (1985), p. 24 (`wikiquote_feynman.txt`) | "All we do is draw little arrows on a piece of paper — that's all!" (quoted without the dash part) |
| Pilot-wave: one slit, determined by position and wave | SEP, "Bohmian Mechanics" (`sep_qm-bohm.txt`) | "when a particle is sent into a two-slit apparatus, the slit through which it passes and its location upon arrival on the photographic plate are completely determined by its initial position and wave function"; "Bohmian mechanics is empirically equivalent to orthodox quantum theory" |
| PBR theorem | SEP, "Philosophical Issues in Quantum Theory" §5.1 (`sep_qt-issues.txt`) | "Pusey, Barrett, and Rudolph (2012) showed that, if one adopts a seemingly natural independence assumption about state preparations ... any ontological model that reproduces quantum predictions and satisfies this Preparation Independence assumption must be a ψ-ontic model."; "does not close off all options for anti-realism about quantum states" |
| QBism | SEP, "Quantum-Bayesian and Pragmatist Views of Quantum Theory" (`sep_quantum-bayesian.txt`) | "a quantum state represents the epistemic state of the one who assigns it concerning that agent's possible future experiences. It does this by specifying the agent's coherent degree of belief (credence) in each of a variety of alternative experiences" |
| Photons need field theory | SEP, "Quantum Field Theory" (`sep_quantum-field-theory.txt`) | "fields, like the electromagnetic field, which are not merely difficult but impossible to deal with in the frame of QM"; "The lack of field operators at points appears to be analogous to the lack of position operators in QFT, which troubles the particle interpretation." |
| Born rule unexplained | `data/originals/many-worlds-one-best-guess.md` line 39 | "There is no known reason for the [Born probabilities]" |

The note title quotes "Beam splitter", "Bohmian Mechanics", "Quantum-Bayesian and Pragmatist Views" are article titles.

## 3. Arithmetic

Script: `data/sources/4c_quantum-explanations/check_interferometer.py` (run with `.venv/bin/python`). Output, in short:

- Figure 1: A→1 = (−1)(i) = −i; A→2 = (−1)(1) = −1; squared moduli 1 and 1. Matches the post.
- Figure 2 (post's rule): A→B = −i, A→C = −1, B→D = i(−i) = 1, C→D = i(−1) = −i. At D: to E, i·1 + 1·(−i) = 0; to F, 1·1 + i·(−i) = 2. Squared moduli 0 and 4. Matches the post.
- Totals of squared moduli under the post's rule: 1 at the start, 2 after A, 4 after D (not conserved). With the factor 1/√2: A→B = −0.707i, A→C = −0.707, E = 0, F = 1; total 1.
- Figure 3, block B–D (post's rule): E = −i, F = 1 (matches the post). Block configuration (amplitude flowing into B→D before the block) = 1, so the post's rule gives block : E : F = 1 : 1 : 1, a third each. With 1/√2: block 0.5, E 0.25, F 0.25.
- Block C–D: E = +i, F = 1 (post: "The amplitudes are different, but the ratio of the squared moduli is still 1"; correct: E's amplitude changes sign). Unitary shares again 0.5 / 0.25 / 0.25.
- Law of total probability example: 1/2 × 1/3 = 1/6. Correct. (The source text prints the fractions as "12", "13", "16".)
- Editor's note convention (reflection −1 from the coated side, +1 from the other; full mirrors −1): depending on which side of D faces B, either |DE|² = 1, |DF|² = 0 or the reverse. One detector is dark either way, as the note on "a ratio of i to 1" says.
- Full-mirror factor: each path meets exactly one full mirror, so any full-mirror factor multiplies both arriving amplitudes and cannot change a ratio (stated in a note; follows from the calculation above).

## 4. Claims about other posts

- "Quantum Explanations" (posted 2008-04-09; this post 2008-04-11, "two days earlier"): announces "I am going to make fun of the *intuitions*", which the note on "Ha, ha!" cites.
- "Many Worlds, One Best Guess" (2008-05-11), line 39, as above. Context read: the paragraph concerns deriving probabilities in many-worlds; the sentence is a general statement.
- "Probability is in the Mind": the post links it; our note only restates the link. Our notes on that post say its argument is stated for all probabilities while all its examples are classical; nothing here conflicts.
- "The sequence does not discuss field theory": `grep -i -E 'field theory|relativistic|QFT'` over the book's quantum posts finds only a simile in "Decoherence is Falsifiable and Testable" ("predict the winner of a tennis match using quantum field theory").
- "Joint Configurations" (next post, another agent): I only say that the post promises it will treat several particles.

## 5. Not verified

- The figures are SVGs of vector paths with no text; no SVG renderer is installed (no rsvg-convert, cairosvg or inkscape), so I could not view them. The first figure note says so. Labels (E, F, Detectors 1 and 2) follow the text.
- Loudon's textbook itself was not checked; the attribution is Wikipedia's.
- Whether "early scientists" ran single-photon beam-splitter experiments and read them as the post says: not checked. The note says only that they are not named.

## 6. Judgment calls for the editor

- Reserved words: none in notes. The Summary says "Probabilities are never negative" (a mathematical fact, restating the post).
- The 1/√2 note. The post flags its rule with "Roughly speaking" and later says only ratios are measured, so a defender can say the omission is deliberate. I therefore state that every result the post reports comes out right, and put the consequence (the block's share) in the separate note on "Detector 1 goes off half the time". Both points are physics, not style; I think they help a reader who compares with a textbook, as the editor's note itself anticipates.
- "Detector 1 goes off half the time" (cfact): a defender may say "half" obviously meant of the detected photons. I worded the note as "True of the photons that reach a detector" rather than as an error.
- "a ratio of i to 1" (clogic, "Loosely worded"): I am confident that one interferometer fixes only a total phase difference, and the script shows the editor's −1 convention also gives a dark port. For a lossless symmetric splitter, unitarity forces the i; so "the experiments shown do not single out i" is the claim, not "i is wrong".
- Pilot-wave note: the SEP quotations are about particles in general (two-slit); Bohmian treatment of photons is less settled. I wrote "a particle" and did not claim a Bohmian account of photons specifically.
- QBism note: I say the "not degrees of belief" argument "does not reach" QBism. This is about scope, not an error in the post; the post's sentence is marked "Correct as stated".
- Response "In short" line: "treats the realist reading of amplitudes as something the experiments show". The post's words: "Configurations and amplitude flows are causes, and they have visible effects; they are real." I read that as inferring reality from the experiments. The fair-defender reply would be that the post argues from a general principle ("What affects the world is real"), which I acknowledge in the Response ("the post asserts it").

## 7. Problems outside my files

- `annotated/preview.sh posts configurations-and-amplitude` fails: "Unicode character √ (U+221A) not set up for use with LaTeX". The √ is in the post text ("i defined as √−1"). The preamble needs `\DeclareUnicodeCharacter{221A}{\ensuremath{\surd}}`. With that line added in a private wrapper (`data/sources/4c_quantum-explanations/build/ca_test.tex`, which inputs the real preamble, post and afterword), the post builds with no errors and no overfull boxes. Four originals contain √.
- The skeleton renders the book's editor's note as `\item [\textbf{Editor's Note:} ...]`, i.e. the whole note is the item's label. In the test PDF the label runs off the left margin ("he experiment." visible at the edge of page 8). This is in the skeleton (md2tex.py), not in my notes.
