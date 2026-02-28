# Student Notes: Chapter 3 (Influence and Noise Sensitivity)

## Things I found clear
- Influence definition is intuitive and the spectral formula proof is clean.
- The discrete derivative D_i f idea is elegant — neat that flipping x_i acts as negating χ_S iff i ∈ S.
- Total influence = expected degree under the spectral distribution. Good way to think about it.
- The worked examples (dictator, parity, Maj₃ influences) are helpful and easy to verify by hand.
- Noise operator definition is now clear with the "the expectation is over y, not x" clarification.
- The spectral characterization of T_ρ is beautiful — it's literally just multiplying each coefficient by ρ^{|S|}.
- The "low-pass filter" interpretation is exactly the right intuition.

## Confusions / Questions

1. **Influence proof step: why does Inf_i[f] = E[(D_i f)²]?**
   The proof says: "f(x) ≠ f(x^⊕i) iff |D_i f(x)| = 1 (since f takes values ±1, the difference is 0 or ±2)."
   OK so D_i f = (1/2)(f(x) - f(x^⊕i)) is either 0 or ±1. Then (D_i f)² is either 0 or 1, and it's 1 exactly when f(x) ≠ f(x^⊕i). So E[(D_i f)²] = Pr[f(x) ≠ f(x^⊕i)] = Inf_i.
   I get this now, but it took me a while. The step "the difference is 0 or ±2" is doing more work than it looks — it implicitly uses that f ∈ {±1} so f(x) - f(x^⊕i) ∈ {-2, 0, +2}. This could use one more sentence.

2. **The notation [i ∈ S] in the proof.**
   The formula χ_S(x^⊕i) = (-1)^{[i ∈ S]} χ_S(x) uses Iverson bracket notation [i ∈ S] without ever defining it. Some students won't know this convention.

3. **The KKL theorem (Kahn-Kalai-Linial) is mentioned at the end of §3.1 but never unpacked.**
   "Every Boolean function depending on all n variables has max_i Inf_i[f] ≥ Ω(log n / n)." This is stated as a fact without motivation. Why does this matter? What does it mean intuitively? (It means no Boolean function can have ALL variables have negligibly small influence — there's always at least one variable with influence at least log(n)/n.) A sentence of interpretation would help.

4. **N_ρ(x) notation in the noise operator definition.**
   The formula uses E_{y ~ N_ρ(x)}[f(y)] but N_ρ(x) is never defined as a distribution. I can infer it means "the distribution of the ρ-correlated copy of x," but this is a new notation introduced without definition. Either define it or just write E_y[f(y)] with the verbal description (which is also given).

5. **Why ρ ∈ [-1, 1] and not just [0, 1]?**
   The noise operator allows negative ρ. What does ρ < 0 mean? If ρ = -1, then y_i = -x_i always, so T_{-1} f(x) = f(-x). This is the "anti-correlation" operator. Is this used anywhere in the thesis? The text never discusses negative ρ despite allowing it in the definition.

6. **Noise stability vs noise sensitivity: the relationship formula.**
   NS_δ[f] = (1 - Stab_{1-2δ}[f]) / 2. Where does this come from? It's stated without proof. For Boolean f, Pr[f(x) ≠ f(y)] = (1 - E[f(x)f(y)])/2 since f(x)f(y) ∈ {±1}, and it equals +1 iff they agree and -1 iff they disagree. So Pr[disagree] = (1 - E[f(x)f(y)])/2. And E[f(x)f(y)] = Stab_ρ when ρ = 1 - 2δ. OK, that's clear once I work through it, but a one-line derivation would help.

7. **The derivative proof in Proposition 3.4 skips a step.**
   It says d/dδ NS_δ = d/dδ [(1/2)(1 - Σ_S (1-2δ)^{|S|} f̂(S)²)] = Σ_S |S| f̂(S)².
   The chain rule gives: (1/2) Σ_S (-1)·(-2)·|S|·(1-2δ)^{|S|-1} f̂(S)² = Σ_S |S|(1-2δ)^{|S|-1} f̂(S)².
   At δ = 0: Σ_S |S|·1^{|S|-1} f̂(S)² = Σ_S |S| f̂(S)² = I[f]. OK this checks out.
   But the published proof just jumps to the answer. Showing the chain rule step would help.

8. **The noise stability examples: Maj₃ computation.**
   Stab_ρ = 3·(1/4)ρ + (1/4)ρ³. This is because f̂(∅) = 0 (so no ρ⁰ term), three degree-1 coefficients each (1/2)² = 1/4, and one degree-3 coefficient (-1/2)² = 1/4. So:
   Stab_ρ = 0·ρ⁰ + 3·(1/4)ρ¹ + 0·ρ² + (1/4)ρ³.
   This is correct but the text omits the ρ⁰ and ρ² terms, which might confuse a reader who tries to match it to the formula Σ_S ρ^{|S|} f̂(S)².

9. **"Semigroup property" of T_ρ is never mentioned.**
   T_ρ T_σ = T_{ρσ}. This is easy to see spectrally (multiply coefficients by ρ^|S| then σ^|S| = (ρσ)^|S|) and is used implicitly in Chapter 4. Stating it here would set up Chapter 4 better.

10. **No graph or plot of noise stability.**
    A plot of Stab_ρ[f] vs ρ for the three examples (dictator: linear, parity: exponential decay, majority: cubic) would be worth a thousand words. It would visually show why parity is noise-sensitive and majority is relatively robust.

## Missing connections
- The chapter ends with the influence-noise sensitivity connection. It would help to have a summary table:
  | Function | Total influence | Noise sensitivity (small δ) | Spectral concentration |
  |----------|----------------|----------------------------|----------------------|
  | Dictator | 1 | δ | All degree 1 |
  | Parity | n | ≈nδ | All degree n |
  | Maj₃ | 3/2 | ≈(3/2)δ | 75% degree 1 |

  This would tie together influence, noise sensitivity, and spectral concentration in one view.
