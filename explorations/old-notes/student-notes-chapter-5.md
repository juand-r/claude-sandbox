# Student Notes on Chapter 5: "Algebraic Generating Functions and the n^{-3/2} Law"

## Overall impression

The chapter delivers the headline result (universal n^{-3/2} exponent for
unambiguous CFGs) clearly. The Chomsky-Schutzenberger theorem, Puiseux
expansion, and the characteristic-system argument for why square roots are
generic are all well-presented. No major mathematical errors found.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Line 13 | ~~"Part II (Chapter 6) develops the theory of context-free languages in depth" — Part II starts at Ch6 but includes Ch6-9. The parenthetical "(Chapter 6)" is misleading; Part II is four chapters, not one.~~ **FIXED: changed to "(Chapters 6--9)".** |
| 2 | MEDIUM | Line 114 | ~~"The transfer theorem identifies $(1-z/\rho)^{1/2}$ as a function of type $\alpha = 1/2$ in the sense of Chapter 4" — but in Ch4 the transfer theorem uses $(1-z/\rho)^{-\alpha}$, so $(1-z/\rho)^{1/2}$ corresponds to $\alpha = -1/2$, not $\alpha = 1/2$. The text seems to use $\alpha$ inconsistently with Ch4's convention.~~ **FIXED: reworded to state the factor corresponds to $\alpha = -1/2$ in the Ch4 convention $(1-z/\rho)^{-\alpha}$.** |
| 3 | LOW | Chapter | No exercises. |
| 4 | LOW | Line 167 | "Gap 5 of Part V" — the gaps are numbered in Ch18; forward-referencing a gap number before the reader has seen Part V is a bit disorienting. |

## Summary

Solid chapter. The characteristic-system analysis (lines 82-100) explaining
WHY square roots are generic is the highlight — it's one of the clearest
expositions of this argument I've seen. The $\alpha$ sign convention issue
(#2) should be checked against Ch4 for consistency.
