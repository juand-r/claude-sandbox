# Three-Pass Review Findings

## Pass 1: Self-Containedness

Can you follow along without consulting outside sources?

### Ch1 (Prerequisites)
- ~~**BUG**: Markov's inequality proof (line 149) still uses `p(omega)` but the definition was changed to `mu(omega)`. Inconsistency.~~ **FIXED.**
- Added Shevtsova (2011) citation for Berry-Esseen constant.
- Otherwise self-contained. All definitions, proofs, and results are present.

### Ch2 (Boolean Fourier Analysis)
- Fully self-contained. Full proofs for orthonormality, Fourier expansion, Parseval, Plancherel, convolution theorem. Good worked examples.

### Ch3 (Influence and Noise Sensitivity)
- Fully self-contained after the previous edits. Iverson brackets defined, proofs expanded.
- The only mild gap: the equivalence "y_i = x_i z_i where E[z_i] = rho" is stated but the reader needs to verify P[z_i = 1] = (1+rho)/2. This is immediate but could be a sentence.

### Ch4 (Hypercontractivity)
- ~~**GAP**: "Bessel's" inequality cited at line 134 ("the inequality is Bessel's") but never defined or stated anywhere in the guide.~~ **FIXED**: explained inline as "projecting onto a subspace cannot increase the L^2 norm."
- ~~**GAP**: "DNF/CNF formulas" mentioned in the LMN remark but not defined.~~ **FIXED**: added inline definition (OR of ANDs / AND of ORs).
- ~~**GAP**: Furst-Saxe-Sipser and Ajtai cited by name but not by reference.~~ **FIXED**: added \citet entries and bib records.
- Otherwise the proofs are transparent about what they prove and what they defer.

### Ch5 (Walsh-Hadamard Transform)
- Fully self-contained. All proofs present, worked examples, block matrix shown.

### Ch6 (LTFs, Codes, Groups)
- ~~"Hamming distance" used in the RM code definition without explicit definition.~~ **FIXED**: added parenthetical defining it.
- Otherwise self-contained. GF(2), linear code, unitriangular all defined.

### Ch7 (Applications)
- Self-contained relative to earlier chapters. All concepts have back-references.

## Pass 2: Worked Examples Audit

### What exists:
- Ch1: Mixed-product rule, Kronecker H1⊗H1, Berry-Esseen applied to BNN
- Ch2: Dictator, AND (2 bits), Majority (3 bits), Parity, Maj3 truncation (5 worked examples)
- Ch3: Influences of dictator/parity/Maj3, noise stability of same, summary table, **T_{1/2} Maj_3 worked example (NEW)**
- Ch4: Level-k meaning with thesis numbers, LMN k* computation, **level-k numerical example for Maj_3 and AND_10 (NEW)**
- Ch5: H2 matrix, FWHT of v=(1,-1,-1,1), binary-counting table
- Ch6: LTF examples, RM(1,2) worked example, sign projection (Maj3)
- Ch7: Full pipeline (parity n=3) with FWHT steps, majority contrast, spectral reconstruction

### Previously missing (now fixed):
1. ~~**Ch3**: No worked computation of T_rho applied to a concrete function.~~ **ADDED**: T_{1/2} Maj_3 with both spectral and probabilistic verification.
2. ~~**Ch4**: No numerical example at all.~~ **ADDED**: Level-k bound checked for Maj_3 (vacuous) and AND_10 (tight), illustrating asymptotic nature.

## Pass 3: Sources and Recommended Reading

### Missing citations (now fixed):
- ~~Furst-Saxe-Sipser (1984) and Ajtai (1983) for the parity lower bound in AC^0~~ **ADDED** to bib and cited in Ch4.
- ~~Berry-Esseen constant C < 0.4748: cite Shevtsova (2011)~~ **ADDED** to bib and cited in Ch1.

### Per-chapter recommended reading:
- ~~Currently exists only at the end of Ch7.~~ **ADDED** annotated recommended reading sections to Ch1 through Ch6. Each item includes: the reference, what it covers, assumed level, and why it is worth reading.
