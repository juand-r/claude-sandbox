# Chapter 05 Changelog

## What I changed

- Rewrote the chapter opening to fix the biggest structural problem: the draft no longer says or implies that being context-free by itself forces the `n^{-3/2}` law. The chapter now opens with `a^*` as an explicit counterexample to that overstatement and narrows the law to a nonlinear generic regime.
- Rebuilt the grammar-to-equation discussion so the translation is explained symbol by symbol, including the role of terminals, nonterminals, and `\varepsilon`, instead of assuming that “each production contributes a monomial” is self-evident.
- Reframed the Chomsky-Schutzenberger and Puiseux theorems as major black boxes with clearer practical interpretations, instead of pretending the proof sketches are enough for the target reader.
- Reworked the “why square roots are generic” section into an explicitly heuristic local-balance argument, including the omitted-order discussion that justifies dropping the mixed term and avoiding the earlier unsafe square-root manipulation.
- Replaced the overly broad `n^{-3/2}` theorem with a narrower theorem about nonlinear positive algebraic systems, then added informal explanations of the key structural hypotheses and an explicit reminder that rational / linear context-free cases lie outside that regime.
- Cleaned up the transfer step so the coefficient asymptotic for `(1-z/\rho)^{1/2}` has the correct sign and the analytic-background discussion no longer leans on a hidden arithmetic mistake.
- Fixed the plane-tree worked example so the Catalan asymptotic matches the earlier chapters without the old extra factor.
- Rewrote the end of the chapter so exponent fitting is presented as heuristic evidence rather than theorem-level diagnosis, and so `\beta=0`, `\beta=-1`, and `\beta=-1/2` are attached to the correct singularity models.

## Note items addressed

- Addressed the highest-priority issue: the scope of the `n^{-3/2}` law is now explicitly narrowed, with regular / linear counterexamples treated as exclusions rather than accidental contradictions.
- Addressed several major gaps around the production-to-monomial translation, the sign mistake in the transfer step, the plane-tree arithmetic typo, the unsafe branch manipulation in the heuristic square-root derivation, and the misleading implications section.
- Reduced the manuscript-wide over-universalization of the CFG/algebraic/`n^{-3/2}` story by making this chapter itself say clearly that the law belongs to a specific nonlinear square-root regime, not to every context-free language.

## Pushback and deferrals

- I still treated Chomsky-Schutzenberger, Puiseux, and the full Drmota-Lalley-Woods-style theorem family as black boxes. For this chapter, I think the right repair is to narrow the claims and explain their role, not to fake a full proof.
- The structural hypotheses are now unpacked informally, but not with complete technical precision. If later chapters lean harder on those exact hypotheses, we may want a short glossary or a more formal dependency-graph subsection.
