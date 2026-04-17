# Student Notes on Chapter 13: "Boltzmann Sampling"

## Overall impression

The pivotal chapter of Part IV. The Gibbs/GF correspondence (Remark
ch13:gibbs-correspondence) is the single most important observation and is
clearly stated. The recursive construction from symbolic specs is well-explained.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Line 185 | "Wait — more directly..." — informal self-correction left in text. The uniformity check starts with a confused calculation then restarts. Should be cleaned up to give just the clean argument. |
| 2 | MEDIUM | Line 131 | "At $\beta = \beta_c$, whether the partition function converges depends on the growth rate of $a_n$. For many natural classes, $a_n \sim C \rho^{-n} n^{-\alpha}$ with $\alpha = 3/2$... in which case $Z(\beta_c) = A(\rho)$ diverges since $\sum n^{-3/2} < \infty$ but barely so." — The statement "diverges since $\sum n^{-3/2} < \infty$" is contradictory. If $\sum n^{-3/2}$ converges (which it does, since $3/2 > 1$), then $A(\rho)$ CONVERGES, not diverges. This seems to be a mathematical error. |
| 3 | LOW | Line 225 | "see the monograph of Velenik" — no citation key given, unlike all other references in the book. |

## Summary

The Gibbs correspondence is well-presented. The claim about $Z(\beta_c)$
diverging when $\sum n^{-3/2} < \infty$ (issue #2) appears to be a
mathematical error that needs checking — if $a_n \sim C\rho^{-n}n^{-3/2}$,
then $A(\rho) = \sum a_n \rho^n \sim \sum C n^{-3/2}$, which converges.
