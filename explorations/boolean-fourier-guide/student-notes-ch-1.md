# Student Notes: Chapter 1 (Prerequisites)

## Things I found clear
- Inner product definition, Cauchy-Schwarz, ONB — standard material, well stated.
- Kronecker product definition with the explicit block matrix is helpful. The H1 ⊗ H1 example is good.
- Markov/Chebyshev proofs are clean and short.
- Berry-Esseen application to BNNs is concrete (d=1024 → error ~0.015). Good.

## Confusions / Questions

1. **Prop 1.1 (Fourier expansion) is stated only for finite-dimensional spaces.**
   That's fine for our use, but it's not labeled as finite-dimensional in the statement itself — only the label says "finite-dimensional inner product space." A student might wonder whether this generalizes (and it does, but with convergence issues). Minor, but worth a sentence.

2. **Kronecker product: property (iii) says "if A and B are orthogonal, so is A ⊗ B."**
   But orthogonal in what sense? Does it mean A^T A = I? If so, then (A ⊗ B)^T (A ⊗ B) = (A^T A) ⊗ (B^T B) = I ⊗ I = I. OK — but the Hadamard matrix H_n satisfies H_n H_n^T = N·I, not I. So H_n is *not* orthogonal in the standard sense (it's a scalar multiple of an orthogonal matrix). This might confuse a student who sees "orthogonal" and then sees H_n H_n^T = N·I later. Should clarify that H_n is "orthogonal up to scaling" or define what "orthogonal" means here precisely.

3. **L^p norm section: the inequality ‖f‖_p ≤ ‖f‖_q for p ≤ q.**
   The text says "(by Jensen's inequality; the direction may seem backwards, but recall we are on a probability space)." This is hand-wavy. A student seeing this for the first time would want at least a one-line sketch: Jensen says E[|f|^p] ≤ (E[|f|^q])^{p/q} when p ≤ q, by concavity of t^{p/q}... actually wait, Jensen for convex functions gives the other direction. The text is right that it's subtle. A 2-line proof or at least a pointer would help.

4. **L^p section uses `p` for both the exponent and the probability measure.**
   In Definition 1.9 of L^p norm, the formula uses `p(ω)` for the probability and `p` for the exponent. This is a notational collision. It would be better to use `μ(ω)` or `\Pr(ω)` for the probability, or at least acknowledge the overloading.

5. **Berry-Esseen: what is S_n?**
   The theorem uses S_n = X_1 + ... + X_n but this is never defined. The CLT statement uses the full expression X_1 + ... + X_n, but Berry-Esseen suddenly switches to S_n. Should define S_n explicitly.

6. **Berry-Esseen: what is Φ(t)?**
   Defined as "the standard normal CDF" — fine, but a student who hasn't seen it might want the formula Φ(t) = (1/√(2π)) ∫_{-∞}^t e^{-s²/2} ds. Not critical.

7. **The "Why this matters for the thesis" paragraph assumes the reader knows what BitNet's learned scaling factors are.** This is forward-referencing Ch 7. For a student reading linearly, this reference is opaque. Consider either deferring this paragraph or adding one sentence of context.

8. **No worked example for Kronecker product properties.** The mixed-product rule (i) is stated but never demonstrated. A small 2×2 example showing (A ⊗ B)(C ⊗ D) = (AC) ⊗ (BD) would build intuition, especially since this rule is described as "the algebraic engine" for Hadamard matrices.

9. **Convergence in distribution (→^d) is used without definition.** In the CLT statement. A student with only calculus/linear algebra background might not know what this means.

## Missing background (for the assumed audience)
- The guide assumes "probability, linear algebra, calculus" — but convergence in distribution is a probability concept that not all undergrads would have seen. A brief definition would help.
