# Student Review Notes for `ch02.tex`

Read from the perspective of a gifted high-school student with some probability, calculus, and linear algebra, but not much combinatorics or complex analysis.

My standard for flagging a gap here is:

- **Major gap**: a theorem-sized step is used without enough support for this audience.
- **Medium gap**: the main idea is present, but important steps are skipped or compressed.
- **Minor gap**: the passage is probably survivable, but still too fast for the stated audience.
- **Preview gap**: an advanced fact is stated before it is proved; this is fine only if clearly labeled as a preview.
- **Precision gap**: the wording is likely to mislead a beginner, even if the author knows what is meant.

## Overall assessment

This chapter is doing two different jobs at once:

1. introducing complex analysis to a beginner, and
2. giving the analytic-combinatorics storyline about singularities controlling asymptotics.

As written, it succeeds better at the second job than the first. For the target audience, the chapter currently reads more like a **guided survey** than a self-supporting lesson. The main structural problem is that several of the central theorems are either only sketched or simply announced:

- Cauchy--Hadamard,
- the equivalence of the different notions of analyticity,
- the radius = nearest singularity principle,
- Cauchy's integral formula,
- contour deformation,
- Pringsheim--Vivanti,
- and the transfer from singularity type to coefficient asymptotics.

That is a lot of heavy machinery to leave implicit in a chapter whose title promises "just enough" complex analysis. A gifted high-school student can absolutely follow the **story**, but many of the places where the story becomes mathematically true are still hidden.

## Biggest missing bridges

If I had to identify the most important unsupported moves, they would be these:

1. The proof sketch of **Cauchy--Hadamard** is far too compressed for this audience. Make it a full proof.
2. The chapter uses **holomorphic/analytic** facts that are major theorems, then moves on quickly. More intuition and explanation needed.
3. **Contour integrals** appear before they have really been introduced.
4. The statement "radius of convergence = distance to nearest singularity" is used as if established, but it is one of the core theorems of the chapter.
5. The classification of poles / square roots / logarithms is presented as if it already implies coefficient asymptotics in general, which is really the content of the later transfer theorem.
6. The sections on **square roots** and **logarithms** use complex branches without explaining what a branch is.

## Detailed gaps, section by section

### 1. Opening setup

#### 1.1 Lines 3-9: "make that move rigorous and computational"

- **Severity:** Medium gap.
- **Issue:** The introduction promises rigor, but much of the chapter relies on theorem statements, proof sketches, or intuition paragraphs instead of actual proofs.
- **Why a student may stumble:** A beginner may not know which facts are meant to be trusted as black boxes and which ones they are expected to understand or derive.
- **What would help:** Be explicit early on:
  "Several foundational theorems of complex analysis will be used without proof; our goal is intuition plus the specific consequences needed for generating functions." ACTUALLY -- even better, include the proofs! (where possible)

### 2. Complex Numbers and Convergence

#### 2.1 Lines 17-21: modulus, argument, and polar form

- **Severity:** Minor gap.
- **Issue:** The argument `\arg z` is introduced as an angle in `(-\pi,\pi]`, but the branch-choice issue is not mentioned.
- **Why a student may stumble:** A first-time reader may not realize that angles differing by `2\pi` describe the same number, and that choosing a principal argument is a convention.
- **What would help:** Add one sentence:
  "Angles are only defined modulo `2\pi`; here we choose the principal value in `(-\pi,\pi]`."

#### 2.2 Lines 22-27: Euler's formula and polar form

- **Severity:** Minor-to-medium gap.
- **Issue:** Euler's formula is used without proof or reminder.
- **Why a student may stumble:** Some readers at this level will know complex numbers but not yet have seen why `e^{i\theta} = \cos\theta + i\sin\theta`.
- **What would help:** Either briefly justify it from the power-series definitions of `e^x`, `\sin x`, `\cos x`, or say explicitly that it is a standard fact being taken for granted.

#### 2.3 Lines 28-30: multiplication in polar form

- **Severity:** Minor gap.
- **Issue:** The formula is correct, but it moves quickly from notation to law.
- **Why a student may stumble:** If the reader has not internalized `e^{i\theta_1}e^{i\theta_2}=e^{i(\theta_1+\theta_2)}`, this will feel like magic.
- **What would help:** Add a one-line reminder that exponentials add exponents.

#### 2.4 Lines 32-35: absolute convergence implies convergence

- **Severity:** Medium gap.
- **Issue:** This is stated, not shown.
- **Why a student may stumble:** A student may know the real-variable statement, but not immediately know why it remains true for complex series.
- **What would help:** Give a short proof or remark:
  if `\sum |w_k|` converges, then both `\sum \Re(w_k)` and `\sum \Im(w_k)` converge absolutely by comparison, so `\sum w_k` converges in `\mathbb C`.

#### 2.5 Lines 36-42: geometric series identity

- **Severity:** Minor gap.
- **Issue:** This is one of the cleanest parts of the chapter, but it still uses the finite-sum identity and the limit transition quickly.
- **Why a student may stumble:** The student may want reassurance that `|w|^{N+1}\to 0` is the only thing needed.
- **What would help:** This is almost fine as is; a tiny extra line connecting it to the ordinary real geometric series would help.

### 3. Power Series and Radius of Convergence

#### 3.1 Lines 48-50: "the set of `z` for which this series converges absolutely is a disk"

- **Severity:** Medium gap.
- **Issue:** The crucial boundary case is omitted here.
- **Why a student may stumble:** A beginner naturally asks: what happens when `|z| = R`?
- **Why this matters:** Boundary behavior is genuinely subtle; some series converge at some boundary points and diverge at others.
- **What would help:** Add an explicit sentence:
  "The theorem says nothing uniform about the boundary `|z|=R`; that must be analyzed separately."

#### 3.2 Lines 51-57: statement of Cauchy--Hadamard

- **Severity:** Major gap.
- **Issue:** The theorem is central, but the chapter gives only a proof sketch and never defines `\limsup`.
- **Why a student may stumble:** For a gifted high-school student, `\limsup` is not routine vocabulary.
- **What would help:** Add a short definition or intuition box:
  "`\limsup x_n` is the eventual upper envelope of the sequence; it is the largest value approached infinitely often."

#### 3.3 Lines 60-73: proof sketch of Cauchy--Hadamard

- **Severity:** Major gap.
- **Issue:** The proof sketch is much too compressed for this audience.
- **Specific missing steps:**
  - how the inequality involving `\delta` and `\epsilon` is chosen;
  - what the definition of `\limsup` is actually giving;
  - why there is an `r<1` with `|a_n z^n|\le r^n`;
  - why comparison with a geometric series proves convergence;
  - why `\limsup |a_n|^{1/n}|z| > 1` implies `|a_n z^n| > 1` infinitely often.
- **Why a student may stumble:** Every line uses nontrivial analysis vocabulary at once.
- **What would help:** Either:
  - expand the proof carefully over 1-2 pages, or
  - state clearly that this is the **root test** in disguise, and give the proof in that more familiar language.

#### 3.4 Lines 60-73: missing edge cases

- **Severity:** Medium gap.
- **Issue:** The theorem statement allows `R=0` or `R=\infty`, but the proof sketch does not discuss those cases.
- **Why a student may stumble:** The proof reads as though `1/R` is just an ordinary finite number.
- **What would help:** Add a sentence handling:
  - `R=\infty`: entire convergence;
  - `R=0`: divergence for every nonzero `z`.

#### 3.5 Lines 75-83: "combinatorial import ... immediate"

- **Severity:** Medium-to-major gap.
- **Issue:** The text jumps from the theorem to the claim that the radius of convergence captures the exponential growth rate.
- **Why a student may stumble:** This is true, but not "immediate" at beginner level.
- **Missing bridge:** One needs to explain how
  `\limsup |a_n|^{1/n} = R^{-1}`
  translates into the heuristic "roughly like `R^{-n}`."
- **What would help:** State and prove a tiny lemma:
  if `\theta(n) = a_n R^n`, then
  `\limsup |\theta(n)|^{1/n} = 1`.

#### 3.6 Lines 77-81: "for well-behaved sequences arising from combinatorics, the ordinary limit exists"

- **Severity:** Medium gap.
- **Issue:** This is plausible but unsupported.
- **Why a student may stumble:** A student may ask what "well-behaved" means and why combinatorial sequences should have actual limits instead of only limsups.
- **What would help:** Either remove this aside, or explicitly label it as a later fact arising from singularity analysis when the dominant singularity is sufficiently regular.

#### 3.7 Lines 80-81: `a_n = R^{-n}\cdot\theta(n)` with `\theta(n)` subexponential

- **Severity:** Medium gap.
- **Issue:** This is correct if one defines `\theta(n)=a_n R^n`, but the text does not say that.
- **Why a student may stumble:** It sounds like a theorem, but really it is partly a definition plus a one-line limsup calculation.
- **What would help:** Make that explicit.

#### 3.8 Lines 85-96: examples

- **Severity:** Mixed.
- **Gap A:** The first example is fine.
- **Gap B:** In the Fibonacci example, the text jumps from the pole locations to `f_n \sim C\varphi^n`.
- **Severity of Gap B:** Major preview gap.
- **Why a student may stumble:** The chapter has not yet proved that a nearest pole yields a coefficient asymptotic of that form.
- **What would help:** Label this as a preview:
  "Later transfer theorems will justify the asymptotic `f_n \sim C\varphi^n`."

#### 3.9 Lines 91-95: smallest modulus root

- **Severity:** Minor gap.
- **Issue:** The modulus comparison is not spelled out.
- **Why a student may stumble:** The roots are `(-1\pm\sqrt5)/2`, and a beginner may need a reminder that these are approximately `0.618` and `-1.618`, so the first has smaller modulus.

### 4. Analytic Functions

#### 4.1 Lines 100-102: open set and holomorphicity

- **Severity:** Minor-to-medium gap.
- **Issue:** "Open set" is used without definition.
- **Why a student may stumble:** A gifted high-school student may not have seen topological vocabulary formally.
- **What would help:** Add:
  "An open set is a region where every point is surrounded by a small disk still lying inside the region."

#### 4.2 Lines 103-110: equivalence of three definitions of analyticity

- **Severity:** Major gap.
- **Issue:** This is one of the deepest theorems in beginning complex analysis, and the text simply announces it.
- **Why a student may stumble:** This equivalence is exactly the surprising miracle of the subject. It is not a routine fact.
- **What would help:** If the proof is omitted, say explicitly that this is a major theorem and that the chapter will use it as a black box.

#### 4.3 Lines 112-127: intuition paragraph

- **Severity:** Minor gap.
- **Issue:** The intuition is good, but the paragraph leans hard on rhetoric like "rigidity" and "no real analogue" without giving a concrete example.
- **Why a student may stumble:** The student may understand the words but still not feel the mathematical force of the claim.
- **What would help:** Give one simple comparison:
  - a real differentiable function can fail to have a power series;
  - a holomorphic function automatically has one.

#### 4.4 Lines 129-132: power series are holomorphic inside their radius

- **Severity:** Major gap.
- **Issue:** The claim that power series can be differentiated term-by-term inside their disk of convergence is itself a theorem.
- **Why a student may stumble:** This is exactly the sort of thing that is true in complex analysis for good reasons, but not obvious from formal algebra alone.
- **What would help:** Either prove the term-by-term differentiation theorem, or present it as a named theorem being used without proof.

#### 4.5 Lines 133-134: holomorphic function determined by its power series at the origin

- **Severity:** Major gap.
- **Issue:** This is another big theorem, not an immediate fact.
- **Why a student may stumble:** A student may not know that a complex-differentiable function is forced to equal its Taylor series.
- **What would help:** Again, either prove it via Cauchy's integral formula later, or say clearly that it is being assumed.

#### 4.6 Lines 138-143: definition of singularity

- **Severity:** Precision gap.
- **Issue:** The definition is a little too informal for a beginner.
- **Why a student may stumble:** In standard complex analysis, one usually distinguishes:
  - points where a function is defined but not holomorphic, and
  - points outside the domain where the function fails to admit a holomorphic extension.
  The current wording blurs those together.
- **What would help:** Clarify whether "singularity" means:
  a point near which the function is holomorphic on a punctured neighborhood but cannot be extended holomorphically across that point.

#### 4.7 Line 142: "a dominant singularity is a singularity of smallest modulus"

- **Severity:** Minor precision gap.
- **Issue:** There can be more than one singularity with the same smallest modulus.
- **Why a student may stumble:** The wording sounds singular, as though there is always a unique one.
- **What would help:** Say:
  "Any singularity of minimal modulus is called dominant; there may be several."

### 5. The Geometric Series as Prototype

#### 5.1 Lines 147-152: deriving `1/(1-z)=\sum z^n`

- **Severity:** Minor gap.
- **Issue:** This is one of the best-explained derivations in the chapter.
- **Possible improvement:** A quick reminder that the equality is only valid for `|z|<1` would help keep the analytic/formal distinction sharp.

#### 5.2 Lines 153-158: holomorphicity outside `z=1` and analytic continuation

- **Severity:** Major gap.
- **Issue:** The notion of analytic continuation is introduced before the reader has really been given the tools to understand it.
- **Why a student may stumble:** The phrase
  "the unique holomorphic function that agrees with the series where the series converges"
  hides a uniqueness theorem.
- **What would help:** Either:
  - postpone analytic continuation until after uniqueness has been explained, or
  - say explicitly that uniqueness of analytic continuation is another nontrivial theorem.

#### 5.3 Lines 160-161: "simple pole" and "blows up like `(1-z)^{-1}`"

- **Severity:** Medium gap.
- **Issue:** The term "simple pole" is introduced informally, but not defined.
- **Why a student may stumble:** This is likely their first exposure to singularity classification.
- **What would help:** Add a short boxed definition:
  a simple pole at `z=\rho` means `(z-\rho)f(z)` stays finite and nonzero near `\rho`.

#### 5.4 Lines 163-168: radius of convergence = distance to nearest singularity

- **Severity:** Major gap.
- **Issue:** This is one of the central theorems of the chapter, and it is only stated informally.
- **Why a student may stumble:** The student has not yet seen why singularities in the complex plane should dictate the radius of a power series at all.
- **What would help:** Either make this a named theorem with proof later in the chapter, or label it as a forward reference to be justified after Cauchy's theorem and analytic continuation machinery.

#### 5.5 Lines 163-165: "the singularity ... is what prevents the radius from exceeding 1"

- **Severity:** Medium gap.
- **Issue:** This is the right intuition, but not yet a proof.
- **Why a student may stumble:** The sentence sounds causal, but the rigorous bridge has not been built.

### 6. Cauchy's Integral Formula for Coefficients

#### 6.1 Lines 174-180: contour integrals appear suddenly

- **Severity:** Major gap.
- **Issue:** The notation
  `\oint_{|z|=r} \cdots dz`
  appears without any introduction to contour integration.
- **Why a student may stumble:** A student with ordinary calculus is unlikely to know what a complex line integral is, how the circle is parameterized, or why orientation matters.
- **What would help:** At minimum, define the contour integral on a circle by writing
  `z = re^{it}`, `0\le t\le 2\pi`.

#### 6.2 Lines 181-189: coefficient formula via Cauchy's integral formula

- **Severity:** Major gap.
- **Issue:** This invokes another major theorem of complex analysis without proof.
- **Why a student may stumble:** Cauchy's integral formula is one of the central miracles of the subject, not a routine lemma.
- **What would help:** If a full proof is too much, say so explicitly.

#### 6.3 Lines 181-189: more accessible proof omitted

- **Severity:** Medium gap.
- **Issue:** For coefficient extraction specifically, there is a more beginner-friendly route that is not used.
- **Why this matters:** If `f(z)=\sum a_n z^n` converges on `|z|=r`, then one can parameterize the circle and use the orthogonality of `e^{int}` to extract `a_n`.
- **What would help:** Consider proving the coefficient formula directly for power series first, then mentioning that Cauchy's integral formula generalizes it.

#### 6.4 Lines 190-193: contour deformation

- **Severity:** Major gap.
- **Issue:** The ability to deform contours outward while staying in the holomorphic region is asserted, not justified.
- **Why a student may stumble:** This depends on Cauchy's theorem / homotopy invariance, which have not been introduced.
- **What would help:** State clearly that this is another standard theorem of complex analysis being used as a black box.

#### 6.5 Lines 193-199: the ML bound

- **Severity:** Medium gap.
- **Issue:** The ML bound is called "standard," but not proved.
- **Why a student may stumble:** It is actually one of the easiest parts of the section and would make a nice confidence-building proof.
- **What would help:** Parametrize the circle and derive the estimate explicitly.

#### 6.6 Line 193: existence of `M(r)=\max_{|z|=r}|f(z)|`

- **Severity:** Minor-to-medium gap.
- **Issue:** The existence of the maximum is not explained.
- **Why a student may stumble:** This uses continuity of `|f|` on a compact set (the circle).
- **What would help:** Add a short reminder that continuous functions attain maxima on compact sets.

#### 6.7 Lines 205-208: from upper bound to "dominant contribution"

- **Severity:** Major gap.
- **Issue:** The chapter moves from an upper bound
  `|a_n|\le M(r)/r^n`
  to the stronger claim that the dominant contribution comes from the nearest singularity.
- **Why a student may stumble:** An upper bound alone does not identify the true leading asymptotic behavior.
- **What would help:** Be more careful:
  the ML bound shows why farther contours give stronger exponential bounds, but actual asymptotics require additional local analysis near the singularity.

#### 6.8 Lines 205-208: singularity as "barrier"

- **Severity:** Minor precision gap.
- **Issue:** The wording "impassable barrier" is vivid, but slightly oversimplified.
- **Why a student may stumble:** In broader complex analysis, one may analytically continue around some singularities or onto other branches. The circle-centered coefficient method has a barrier, but the function-theoretic picture is subtler.

### 7. Classifying Singularities

#### 7.1 Lines 215-216: "type of a singularity determines the subexponential correction"

- **Severity:** Major preview gap.
- **Issue:** This is basically the transfer-theorem message, but it has not yet been proved.
- **Why a student may stumble:** The chapter has only analyzed a few model functions, not the general mechanism that converts local singular behavior into coefficient asymptotics.
- **What would help:** Say clearly that the section is a prototype catalogue, not yet the general theorem.

#### 7.2 Lines 217-223: Pringsheim--Vivanti theorem

- **Severity:** Major gap.
- **Issue:** This important theorem is simply cited.
- **Why a student may stumble:** It is not obvious at all that nonnegative coefficients force the positive real point `z=R` to be singular.
- **What would help:** If the proof is omitted, mark it as a major theorem from later reference material.

#### 7.3 Lines 217-223: "this case rarely arises in combinatorics"

- **Severity:** Minor gap.
- **Issue:** The remark about alternating-sign or complex coefficients is plausible but unsupported.
- **Why a student may stumble:** A beginner may not yet know which generating functions in combinatorics have cancellations.

#### 7.4 Lines 226-240: poles via repeated differentiation

- **Severity:** Medium gap.
- **Issue:** The derivation is correct but skips important details.
- **Missing pieces:**
  - why term-by-term differentiation is allowed;
  - how the index shift works after differentiation;
  - how the general binomial formula emerges after `k-1` differentiations.
- **Why a student may stumble:** The jump from `k=2` and `k=3` to the full general formula is too abrupt.
- **What would help:** Do an induction or state a general lemma.

#### 7.5 Lines 241-250: asymptotic of `\binom{n+k-1}{k-1}`

- **Severity:** Minor-to-medium gap.
- **Issue:** The idea is good, but the asymptotic symbol `\sim` is not explicitly justified.
- **Why a student may stumble:** A beginner may not know how to turn "polynomial of degree `k-1` with leading term `n^{k-1}`" into
  `\sim n^{k-1}/(k-1)!`.
- **What would help:** Divide by `n^{k-1}` and show the quotient tends to `1/(k-1)!`.

#### 7.6 Lines 252-256: rational generating functions and linear recurrences

- **Severity:** Preview gap.
- **Issue:** The statement about linear recurrences and dominant roots is true in many standard cases, but not proved here.
- **What would help:** Mark this as a preview of later chapters or of a standard linear-recurrence theorem.

#### 7.7 Lines 258-263: square-root branch points

- **Severity:** Major conceptual gap.
- **Issue:** The chapter begins discussing square-root branch points without first explaining what a branch point or branch of the square root means in the complex plane.
- **Why a student may stumble:** A beginner may not know why `\sqrt{1-z/\rho}` is not just an ordinary single-valued function everywhere away from `z=\rho`.
- **What would help:** Add a short informal explanation of branch choices and branch cuts before using the term.

#### 7.8 Lines 259-262: generalized binomial theorem reused

- **Severity:** Major inherited gap.
- **Issue:** This section depends on the generalized binomial theorem from Chapter 1, which itself was not fully proved there.
- **Why this matters:** The whole coefficient computation for the square root rests on that theorem.

#### 7.9 Lines 264-272: Stirling's approximation

- **Severity:** Medium gap.
- **Issue:** Stirling's approximation is imported without explanation.
- **Why a student may stumble:** A gifted high-school student may not have seen it before, or may not know whether to regard it as a theorem, a heuristic, or a numerical approximation.
- **What would help:** State it more carefully as an asymptotic theorem:
  `m! \sim \sqrt{2\pi m}(m/e)^m`.

#### 7.10 Lines 268-272: central binomial coefficient asymptotic

- **Severity:** Medium gap.
- **Issue:** The cancellation algebra is reasonably clear, but the use of `\approx` is informal.
- **Why a student may stumble:** This is exactly where rigorous asymptotic notation matters.
- **What would help:** Replace `\approx` by `\sim` and explain the asymptotic substitution carefully.

#### 7.11 Lines 273-276: final square-root coefficient formula

- **Severity:** Medium-to-major gap.
- **Issue:** The chapter concludes with
  `\bigl(1+O(1/n)\bigr)`
  even though only the leading asymptotic has been derived.
- **Why a student may stumble:** The explicit error term requires a more precise version of Stirling's formula than the one stated.
- **What would help:** Either:
  - drop the `O(1/n)` and keep only `\sim`, or
  - state the stronger Stirling expansion being used.

#### 7.12 Lines 278-283: "`n^{-3/2}` is the fingerprint of a square-root singularity"

- **Severity:** Major preview gap.
- **Issue:** The section has only analyzed the prototype function `\sqrt{1-z/\rho}`, not the full class of functions with square-root singular local behavior.
- **Why a student may stumble:** The word "fingerprint" sounds like a proved universal rule, but that rule belongs to the later transfer theorem.
- **What would help:** Rephrase as:
  "This prototype suggests the `n^{-3/2}` behavior that will later be proved in general."

#### 7.13 Lines 286-288: logarithmic singularities

- **Severity:** Major conceptual gap.
- **Issue:** The complex logarithm appears without any discussion of branches.
- **Why a student may stumble:** Unlike the real logarithm, the complex logarithm is multivalued, so one must specify which local branch is intended.
- **What would help:** Add a brief local definition near `z=0` or note that a principal branch is being used inside the disk `|z|<\rho`.

#### 7.14 Lines 286-288: `\log(1/(1-z/\rho)) = \sum_{n\ge1}\rho^{-n}z^n/n`

- **Severity:** Medium gap.
- **Issue:** The series is stated, not derived.
- **Why a student may stumble:** A high-school student may know the real Taylor series for `-\log(1-w)`, but not see instantly why the same holds in the complex setting.
- **What would help:** Derive it by integrating the geometric series term-by-term, at least inside `|w|<1`.

#### 7.15 Lines 292-295: `\SET` and `\CYC`

- **Severity:** Minor preview gap.
- **Issue:** These symbolic-method operators are referenced before they are defined.
- **What would help:** Add "defined in Chapter 3" or omit the notation here.

#### 7.16 Lines 297-304: essential singularities

- **Severity:** Major conceptual gap.
- **Issue:** The paragraph uses "finite Laurent expansion" without having introduced Laurent series at all.
- **Why a student may stumble:** This is brand-new vocabulary appearing with no setup.
- **What would help:** Either omit this section for now, or explicitly say:
  "We mention the term only for orientation; the precise definition uses Laurent series, which we do not develop here."

#### 7.17 Lines 298-300: "they blow up in a highly irregular ... fashion"

- **Severity:** Precision gap.
- **Issue:** This wording is potentially misleading.
- **Why a student may stumble:** Essential singularities are wilder than poles, but they do not merely "blow up"; their nearby behavior is much more erratic than that phrase suggests.
- **What would help:** Use more cautious wording:
  "their behavior near the singularity is much more irregular than pole- or branch-point behavior."

### 8. The Big Picture

#### 8.1 Lines 308-317: summary of singularity location/type

- **Severity:** Major preview gap.
- **Issue:** This summary states the transfer-theorem philosophy as if the chapter has already fully justified it.
- **Why a student may stumble:** What has actually been shown is a collection of prototype calculations plus some strong heuristic/theorem statements.
- **What would help:** Signal more clearly:
  "The general theorem making this precise appears in Chapter 4."

#### 8.2 Lines 319-323: three-step recipe

- **Severity:** Medium gap.
- **Issue:** The recipe is useful, but it hides several subtleties:
  - there may be multiple dominant singularities;
  - the local form near the singularity matters;
  - contour issues and branch cuts can matter;
  - the catalogue above is not itself a full theorem.
- **Why a student may stumble:** The procedure sounds more automatic than it really is.

#### 8.3 Lines 324-329: what is postponed

- **Severity:** Minor gap.
- **Issue:** The list of postponed machinery is accurate, but a beginner may not know which of these topics has already secretly been used in simplified form.
- **Why this matters:** Contour deformation and branch behavior are already peeking into the chapter.

### 9. Exercises

#### 9.1 Lines 331-333: radius of convergence of `\sum z^n/n^2`

- **Severity:** Medium gap.
- **Issue:** The radius `R=1` follows from Cauchy--Hadamard, but the "dominant singularity" part is subtler than the hint suggests.
- **Why a student may stumble:** The series actually converges at `z=1`, so the beginner may wonder how `z=1` can still be a singularity.
- **What would help:** Either:
  - remind the reader that convergence of the series at a boundary point does **not** imply analyticity past that point, or
  - postpone this exercise until Pringsheim's theorem and branch behavior are more established.

#### 9.2 Lines 335-337: cubic pole exercise

- **Severity:** Minor inherited gap.
- **Issue:** This exercise depends on the generalized binomial theorem from Chapter 1, which is still underexplained for the target audience.

#### 9.3 Lines 339-341: `\sum n! z^n`

- **Severity:** Medium gap.
- **Issue:** The exercise asks about the "function" the series represents and its "analytic avatar," but these are sophisticated notions.
- **Why a student may stumble:** A beginner may not know how to interpret a formal power series with radius `0` in analytic terms.
- **What would help:** Add a sentence clarifying that this is precisely an example where the formal object does not define a nontrivial analytic function near `0`.

## Highest-priority fixes

If revising this chapter for the stated audience, I would prioritize these changes first:

1. **Define `\limsup` and discuss boundary behavior** before the Cauchy--Hadamard theorem.
2. **Either prove Cauchy--Hadamard more carefully or explicitly present it as the root test in theorem form.**
3. **Introduce contour integrals before using them**, even if only for circles.
4. **Mark Cauchy's integral formula, contour deformation, and Pringsheim's theorem as major black-box theorems** if they will not be proved.
5. **Separate prototype examples from general theorems**: the pole / square-root / logarithm section should be labeled as a catalogue of model cases, not the full transfer mechanism.
6. **Explain branches** before discussing square roots and logarithms in the complex plane.
7. **Tone down the "therefore" language** in places where only an upper bound or heuristic has actually been established.

## Places that are not wrong, but still too fast

These are survivable for a strong student, but still likely to cause hesitation:

- the use of `\arg z` without discussing principal values;
- Euler's formula being dropped in without any reminder;
- the modulus comparison in the Fibonacci example;
- the polynomial asymptotic of `\binom{n+k-1}{k-1}`;
- the jump from central binomial coefficients to the final square-root asymptotic;
- the appearance of symbolic-method notation `\SET` and `\CYC` before Chapter 3.

## Bottom line

For the stated audience, `ch02.tex` is conceptually exciting but mathematically under-supported. It tells the right story:

- convergence gives a radius,
- singularities live on the boundary,
- Cauchy's formula turns coefficients into contour integrals,
- and singularity type predicts asymptotics.

But for a gifted high-school student, the chapter still needs more scaffolding at the exact places where those story beats become theorems. Right now it works best as an **orientation chapter** rather than as a fully self-contained introduction.

The fastest way to make it genuinely student-friendly would be:

- add 3-5 boxed theorem statements clearly labeled "used without proof" versus "proved here,"
- expand the Cauchy--Hadamard and coefficient-extraction discussions,
- add a short informal section on branch choices for `\sqrt{\cdot}` and `\log`,
- and more aggressively mark the transfer-theorem claims as previews rather than completed arguments.
