# Chapter 01 Changelog

## What I changed

- Added a more explicit formal-power-series toolkit at the start of `ch01.tex`: a small operations dictionary, a proof that coefficient extraction is linear and compatible with products, a proposition characterizing when inverses exist in `\mathbb{Q}[[z]]`, a formal geometric-series lemma, and a coefficient-level verification of the formal derivative product rule.
- Reworked the recurrence-to-generating-function method so it warns about missing initial terms instead of pretending every shift is automatically `z^k A(z)`.
- Clarified the binary-string and Fibonacci examples with slower reindexing, an explicit quadratic-formula line for `\varphi` and `\hat\varphi`, a brief justification for the partial-fraction form, and a cleaner separation between what is proved now and what will later be explained by singularity analysis.
- Rebuilt the Catalan section so the convolution step is written out from the expansion of `C(z)^2`, `\sqrt{1-4z}` is introduced as a genuine formal series, the sign choice is made by constant terms rather than circular expansion, the generalized binomial theorem is labeled as a black-box theorem, and the coefficient extraction has more intermediate algebra.
- Tightened the OGF/EGF section with a concrete labeled example, a clearer explanation of binomial convolution, a ratio-test argument for why `\sum n! z^n` does not converge analytically away from `0`, and a less misleading description of the permutation example.
- Rewrote the roadmap so the chapter is honest about which asymptotic claims are previews and so it already signals that later chapters must distinguish counting generating functions from probability-weighted ones.

## Note items addressed

- Addressed the major foundational gaps around inverses, formal geometric series, Catalan convolution, formal square roots, and the generalized binomial theorem packaging.
- Addressed the main medium gaps around coefficient extraction, reindexing, initial-term corrections, the partial-fraction ansatz, labeled binomial convolution, and the EGF product rule.
- Downgraded singularity, branch-point, and `n^{-3/2}` discussion from something that sounded already established to explicit preview material.

## Pushback and deferrals

- I did **not** add a picture for the Catalan-tree decomposition. Instead I added a concrete `n=3` worked split. That seems like a reasonable compromise unless we decide later that the book should include figures systematically.
- I did **not** prove the generalized binomial theorem in full. I think the right fix here is packaging, not a full digression: it is now stated explicitly as a theorem being used as a black box, with analytic convergence deferred to Chapter 2.
