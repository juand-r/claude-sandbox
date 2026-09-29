# Report: joint-configurations

## 1. The argument in three sentences

Two photons sent at once into the two input sides of a half-silvered mirror start in one
configuration, "a photon going from B to D and a photon going from C to D", and the post's
rules (multiply by i on deflection, by 1 going straight) send amplitude along four routes,
two of which (both deflected, both straight) arrive at the same configuration "one photon to
E, one to F" with opposite amplitudes and cancel, so the detectors never fire one each. This
only works because a configuration records "a photon here, a photon there" and not which
photon is which; if configurations tracked photon identity the two amplitudes would sit in
separate configurations and one-each outcomes would occur about half the time. Since squared
moduli do not add the way probabilities do, configurations cannot be merged or split at will
as possible worlds can, so their identity is a physical fact, and physics cannot be factored
into individually identifiable particles.

## 2. Sources checked

All saved in `data/sources/4c_joint-configurations/`.

- Figure 1 of the post, fetched as a PNG rendering from Cloudinary (`joint_fig1.png`; the
  SVG is `JointConfig_1_v20wwj_huvd16.svg`). Viewed: B enters from the left, C from below;
  B's straight path continues to F (Detector 2), C's straight path to E (Detector 1). This
  matches the post's case list.
- Wikipedia, "Hong–Ou–Mandel effect" (raw, `wiki_HOM.txt`). Matched: "demonstrated in 1987 by
  Chung Ki Hong ..., Zheyu Jeff Ou ... and Leonard Mandel"; "the two photons will always be
  detected in the same output mode"; "We assume now that the two photons are identical in
  their physical properties (i.e., polarization, spatio-temporal mode structure, and
  frequency)"; "If they become more distinguishable (e.g. because they arrive at different
  times or with different wavelength), the probability of them each being detected in a
  different detector will increase"; "reflection from the bottom side of the beam splitter
  introduces a relative phase shift of π, corresponding to a factor of −1"; "the quantum
  result is independent of these phases"; and the equation
  c†²|0,0⟩ = √2|2,0⟩ (the √2 factor note).
- Wikipedia, "Indistinguishable particles" (raw, `wiki_identical.txt`). Matched: "This
  indicates that the particle labels have no physical meaning"; "symmetric states must always
  be used when describing photons or helium-4 atoms, and antisymmetric states when describing
  electrons or protons"; Pauli exclusion from antisymmetry.
- Bocquillon et al., "Coherence and Indistinguishability of Single Electrons Emitted by
  Independent Sources", arXiv:1301.7093, Science 2013 (abstract via arXiv API,
  `arxiv_bocquillon.xml`). Matched: "Both electrons, emitted in indistinguishable wavepackets
  with synchronized arrival time on the splitter, exit in different outputs".
- Aaronson, "Is Quantum Mechanics An Island In Theoryspace?", arXiv:quant-ph/0401062
  (`aaronson2004.pdf`, `.txt`). Matched: "When p = 1 and we restrict our attention to x with
  nonnegative entries, we obtain the set of stochastic matrices". The abstract adds "if we
  replace the 2-norm by some other p-norm, then there are no nontrivial norm-preserving
  linear maps".
- Stanford Encyclopedia, "Quantum-Bayesian and Pragmatist Views of Quantum Theory"
  (`sep_qbism.html`, `.txt`). Matched: "QBists also adopt a subjectivist or personalist
  interpretation of quantum states"; "Because QBists take the quantum state to have the role
  of representing an agent's epistemic state"; Equation (2) "is not just a revision of the law
  of total probability it resembles".
- Wikipedia, "Pusey–Barrett–Rudolph theorem" (raw, `wiki_PBR.txt`). Matched: "With respect to
  certain realist hidden variable theories ... the theorem rules that pure quantum states must
  be 'ontic'"; "either the quantum state |ψ⟩ is ψ-ontic, or else non-entangled quantum states
  violate the assumption of preparation independence". Basis for "under assumptions about an
  underlying physical state".

## 3. Arithmetic

Script: `data/sources/4c_joint-configurations/check_physics.py` (run with `.venv/bin/python`).

- Four flows from (−1): (−1)·i·i = 1 → EF; (−1)·i·1 = −i → EE; (−1)·1·i = −i → FF;
  (−1)·1·1 = −1 → EF. Totals: EF = 0, EE = −i, FF = −i; squared moduli 0, 1, 1. Correct.
- Labelled counterfactual: four configurations with amplitudes 1, −i, −i, −1, each 1/4;
  one-each outcomes total 1/2. Correct ("around half the time").
- Full bosonic calculation (creation operators, 50:50 splitter, 1/√2 per port): P(2 at E) =
  P(2 at F) = 0.5, P(one each) = 0. Same with the symmetric (i) convention and the asymmetric
  (+1/−1) convention.
- Unequal mirror, reflectance 1/3: post's bookkeeping (add flows into unordered
  configurations, then square) gives EE:FF:EF = RT : RT : (T−R)² = 2/9 : 2/9 : 1/9 = 2:2:1.
  Bosonic calculation gives 2RT : 2RT : (T−R)² = 4/9 : 4/9 : 1/9 = 4:4:1 (sums to 1). Hence
  the note's "2:2:1 where the correct ones are 4:4:1".
- Fermions (antisymmetric, exchange term with minus sign), same splitter: one-each amplitude
  r·r − t·t with r = i/√2, t = 1/√2 gives −1, probability 1. Two electrons always exit
  separately.
- |(2+i)+(1−i)|² = |3|² = 9; |2+i|² + |1−i|² = 5 + 2 = 7; cross term 2Re((2+i)(1+i)) =
  2Re(1+3i) = 2. Correct. For 1 and i: |1+i|² = 2 = 1 + 1 (cross term zero).
- Classical case: 4 × 1/4; two one-each cases sum to 1/2. Correct.

## 4. Claims about other posts

- "Configurations and Amplitude" (`data/originals/configurations-and-amplitude.md`, the
  previous post, same date 2008-04-11): the rule "multiply by 1 when the photon goes straight,
  and multiply by i when the photon turns at a right angle"; its editor's footnote says "a
  standard half-silvered mirror would yield a rule 'multiply by −1 when the photon turns at a
  right angle'". I did not cite the footnote, because as worded (−1 on both sides) it would not
  be unitary; my note uses Wikipedia's convention (−1 on one side, +1 on the other). The editor
  may want to check how the agent annotating "Configurations and Amplitude" treats that
  footnote.
- "Distinct Configurations" (next post): "What makes configurations distinct is particles
  occupying different positions—at least one particle in a different state." Quoted in the
  clogic note on kind and place.
- "Think Like Reality" (Posted 2007-05-02): "You have the absolutely bizarre idea that
  reality ought to consist of little billiard balls bopping around". Our note on that post
  already flags "a perfectly normal cloud of complex amplitude in configuration space" as one
  interpretation; my interpretive note here agrees with it.

## 5. Not verified

- The HOM paper itself (Phys. Rev. Lett. 59, 2044, 1987) was not opened; the date and result
  are from Wikipedia's article.
- The Bocquillon result is from the arXiv abstract only.

## 6. Judgment calls for the editor

- Reserved words: the Summary's "never" reports the post's own claim. The Response's "wrong
  ratios" rests on the derivation above (unequal mirror); the post applies its bookkeeping only
  to a 50:50 mirror, so the note and Response present this as a simplification that "does no
  harm here", not as an error in the post's result.
- The √2 note and the "kind and place" note could be seen as teaching points rather than
  faults. I kept them because the brief asks for every physical statement to be checked, and
  the post states its identity rule generally ("an electron here, an electron there"; "same
  species of particles in the same places"). The electron note is the one I think matters most:
  the rule as stated would give the wrong prediction for electrons.
- Interpretation note ("If configurations were just states of knowledge"): I describe the
  author's conclusion as going beyond what this experiment decides, and cite QBism and PBR on
  both sides. The general claim that configurations are real, not knowledge, first appears in
  "Configurations and Amplitude" (order 234, another agent). If that post's notes make the
  full point, my note could be shortened to a pointer.
- The first cpara calls "the key to understanding quantum mechanics" "the author's framing".
  It is mild; cut if the editor thinks it adds nothing.
