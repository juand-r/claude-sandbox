# Student Notes on Chapter 3: "The Symbolic Method"

Reading as an undergrad math/CS student who has read Chapters 1-2.

---

## Overall impression

Well-structured chapter with clear examples. The "translation dictionary" from
combinatorial constructions to GF operations is the core payoff, and the four
worked examples demonstrate it effectively. A few cross-reference errors and
one notational inconsistency need fixing.

---

## Section-by-section notes

### Combinatorial Classes (lines 14-53)

- Line 34: "whether it converges anywhere other than $z=0$ is a separate
  analytic question taken up in Chapter~4" — Chapter 4 is Singularity
  Analysis. Convergence (Cauchy-Hadamard) was Chapter 2. **Cross-ref error.**

- Line 40: "discussed briefly in Section~3" — there is no numbered Section 3;
  all sections use `\section*`. Should say "discussed briefly below" or
  "in the subsection on labeled classes." **Broken reference.**

### Translation Dictionary (lines 55-127)

- Lines 81-119: Proof of the three translation rules. Union and product
  proofs are complete. The SEQ proof invokes $1 + A + A^2 + \cdots = 1/(1-A)$
  as the geometric series identity. This was established in Ch1 for numbers
  and in Ch2 for convergent series. For formal power series with $A(0) = 0$
  it follows from the invertibility construction of Ch1 (since $1-A(z)$ has
  constant term 1). A one-sentence connection would help.

- Line 124: "$\SEQ_{\ge k}$ has OGF $A(z)^k/(1-A(z))$" — stated without
  derivation. The derivation is one line: $\SEQ_{\ge k}(\mathcal{A}) =
  \mathcal{A}^k \times \SEQ(\mathcal{A})$, so OGF = $A^k \cdot 1/(1-A)$.
  Should be shown.

### Bivariate GFs and Pointing (lines 128-148)

- Lines 141-143: The mean formula
  $\mathbf{E}[\chi \mid |\gamma|=n] = [z^n]\partial_u C(z,u)|_{u=1} / [z^n]C(z,1)$
  is stated without derivation. **Leap.** The key step is: differentiating
  $u^{\chi(\gamma)}$ with respect to $u$ and setting $u=1$ "pulls down" the
  statistic $\chi(\gamma)$. Then $[z^n]\partial_u C|_{u=1} = \sum_{|\gamma|=n} \chi(\gamma)$
  and dividing by $c_n$ gives the mean. A two-line derivation would remove
  the mystery.

- Lines 145-148: "$C^\bullet(z) = zC'(z)$ because pointing multiplies the
  number of structures of size $n$ by $n$." This is stated correctly but the
  connection to the derivative is not derived. The derivation: the GF of
  pointed objects is $\sum n c_n z^n = z \sum n c_n z^{n-1} = z C'(z)$. One
  line would suffice.

### Labeled Classes (lines 150-164)

- SET → exp and CYC → log are stated without derivation, with an explicit
  deferral to Flajolet-Sedgewick Ch II. This is honest and acceptable for a
  "just enough" chapter, but a student wanting self-containment will be
  frustrated.

### Worked Examples (lines 166-260)

- Lines 199-204: Plane trees coefficient extraction. "$[z^n]T(z) =
  \frac{1}{n}\binom{2(n-1)}{n-1} = C_{n-1}$." This is stated from
  "Expanding the square root via the generalized binomial theorem (Chapter 1)"
  but no intermediate steps are shown. In Ch1 we derived the Catalan formula
  for $C(z) = (1-\sqrt{1-4z})/(2z)$, but here $T(z) = (1-\sqrt{1-4z})/2$
  (no division by $z$). The computation is similar but not identical —
  the student needs to redo it. **Leap.**

- Line 258: "Chapter~6 when we study parameters of parse trees arising from
  probabilistic context-free grammars" — Chapter 6 is "Formal Languages and
  the Chomsky Hierarchy." PCFGs are Chapter 8. **Cross-ref error.**

### Why the Symbolic Method Matters (lines 262-302)

- Line 275: "$\kappa \rho^{-n} n^{-3/2}$" with $\rho$ as radius of
  convergence. Correct.

- Line 289: "$n^{-3/2} \rho^n$ asymptotics" — this writes $\rho^n$, but
  line 275 writes $\rho^{-n}$. If $\rho$ is the radius of convergence
  (as in Ch4), the correct form is $\rho^{-n}$. **Inconsistency/error.**

### Exercises (lines 304-326)

- Good exercises. Exercise 3 (derangements) is challenging and uses the
  labeled-class rules stated without derivation, which is a pedagogical
  tension — the student is asked to use SET and CYC without having seen
  why they work.

---

## Missing elements

None critical. The chapter has exercises and worked examples. The SET/CYC
derivations are explicitly deferred.

---

## Ranked issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | HIGH | Line 289 | $\rho^n$ should be $\rho^{-n}$ (inconsistent with line 275) |
| 2 | HIGH | Line 34 | "Chapter~4" should be "Chapter~2" (convergence) |
| 3 | HIGH | Line 258 | "Chapter~6" should be "Chapter~8" (PCFGs) |
| 4 | MEDIUM | Line 40 | "Section~3" is a broken reference (sections are unnumbered) |
| 5 | MEDIUM | Lines 141-143 | Mean formula stated without derivation |
| 6 | MEDIUM | Lines 199-204 | Plane trees coefficient: computation not shown |
| 7 | LOW | Lines 145-148 | Pointing formula $zC'(z)$ stated but not derived |
| 8 | LOW | Line 124 | $\SEQ_{\ge k}$ OGF formula not derived |

---

## Summary

The chapter is well-organized and the worked examples are effective. Three
cross-reference errors (lines 34, 258, 289) need immediate fixing. The mean
formula for bivariate GFs and the plane-trees coefficient extraction are
presented as facts without derivation and would benefit from a few lines of
calculation.
