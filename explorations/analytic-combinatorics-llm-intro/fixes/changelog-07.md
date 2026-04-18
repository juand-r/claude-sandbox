# Chapter 07 Changelog

## What I changed

- Rebuilt the chapter around a cleaner core message: WFAs are matrix models, matrix models give rational length generating functions, and those rational functions impose exact asymptotic limits.
- Sharply separated semiring-level generality from the later real/complex matrix analysis, so the chapter no longer blurs the abstract WFA definition with the specific analytic theorem.
- Slowed the WFA definition with a dimension check, a path-sum expansion for a two-letter word, and a stronger Fibonacci example that states the general matrix identity rather than only checking the first few terms.
- Fixed the biggest probabilistic issue by separating **local stochasticity** from **properness**. The chapter now includes an explicit non-halting counterexample showing why row-stochastic local transitions do not by themselves define a probability distribution on finite strings.
- Reworked the rationality proof so the collapse to `A^k` is credited correctly to distributivity, the matrix geometric series is presented both formally and analytically, and rationality is derived from the resolvent formula rather than left half-implicit.
- Replaced the overbroad eigenvalue-asymptotic statement with a safer pole-based proposition about the scalar rational function `F(z)=\alpha(I-zA)^{-1}\beta`, explicitly warning about cancellations, multiple poles on the spectral circle, and pole order versus raw eigenvalue multiplicity.
- Removed the broken balanced-parentheses / PCFG equation from the Icard discussion and replaced it with a more cautious exact-versus-algebraic contrast.
- Rewrote the language-model section so WFA approximation is framed as a research program rather than an already-justified transfer of asymptotic singular behavior.

## Note items addressed

- Addressed the highest-priority problems around stochasticity versus properness, the too-broad eigenvalue asymptotic claim, the semiring-versus-field distinction, and the overpromising approximation language.
- Addressed several medium gaps around the path-sum interpretation, the Fibonacci example, the formal/analytic meaning of the matrix geometric series, and the difference between exact impossibility and approximate finite-range modeling.
- Reduced local pressure on the manuscript-wide approximation drift by making Chapter 7 itself say that approximate WFA realizability and approximate asymptotic rationality are not automatically the same claim.

## Pushback and deferrals

- I kept the noncommutative Kleene-Schutzenberger theorem as a black box. For this chapter, I think that is the right choice: the rationality theorem for length generating functions is the real local payoff.
- I also kept the probabilistic hierarchy discussion at a high level rather than trying to reproduce Icard's examples in detail. The earlier version's concrete example was too shaky to keep, and a correct full replacement would take the chapter too far afield.
