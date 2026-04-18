# Student Notes on Chapter 12: "Approximating Language Models by Weighted Finite Automata"

## Overall impression

Well-structured survey of four approaches (distillation, architectural
equivalence, L*, AAK/spectral). The Hankel matrix definition and spectral
realization are clearly presented. The "one-letter is a feature" observation
is insightful.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Line 126 | "The entries of $\hat A^n$ grow as $\hat\rho^n$" — here $\hat\rho$ is the spectral radius (a growth rate), so $\hat\rho^n$ is correct. But in Ch4 and elsewhere, $\rho$ denotes the radius of convergence, and the growth is $\rho^{-n}$. This dual convention ($\rho$ = radius of convergence vs $\hat\rho$ = spectral radius = $1/R$) could confuse readers. A clarifying sentence would help. |
| 2 | LOW | Lines 42-50 | L* description is clear but could benefit from a small concrete example (e.g., a 2-state DFA being learned). |
| 3 | LOW | Line 87 | "the Hankel matrix of a real LLM is essentially full rank" — "essentially" is vague. Maybe "empirically observed to have slowly decaying singular values." |

## Summary

No mathematical errors. The four-line-of-attack structure works well. Two
exercises included. The notation for spectral radius vs radius of convergence
deserves a clarifying remark.
