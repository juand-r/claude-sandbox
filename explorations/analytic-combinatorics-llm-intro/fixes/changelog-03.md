# Chapter 03 Changelog

## What I changed

- Reframed the opening so the symbolic method is no longer presented as automatic magic: the chapter now says explicitly that a symbolic specification must describe each object exactly once, otherwise the generating function overcounts.
- Expanded the basic class definitions so the OGF equality is explained by grouping objects by size, and the local-finiteness requirement is tied directly to finite coefficients.
- Added a bit more concrete orientation around the stock examples (`words`, `plane trees`, `permutations`) and the building blocks `\mathcal E` and `\mathcal Z`.
- Rebuilt the unlabeled translation dictionary with a slower proof, especially for `\SEQ`: disjointness by sequence length, a concrete failure mode for size-0 objects, a coefficient-level explanation of product, and an explicit appeal to Chapter 1's formal geometric-series identity.
- Clarified the probabilistic meaning of the bivariate mean formula by stating the uniform distribution on `\mathcal C_n`, and made the derivative / pointing rules more explicit.
- Slowed the labeled section substantially: fixed the OGF/EGF confusion, gave a direct coefficient calculation for labeled product, proved the `\SET` rule more transparently, added a small label-set example, and demoted `\CYC` to a recorded black-box rule instead of a too-fast pseudo-proof.
- Reworked the examples so the modeling steps are explained more clearly, the Catalan index shift is explicit, and the square-root / `n^{-3/2}` discussion is framed as preview rather than as something already proved here.
- Rewrote the closing “why it matters” section so it no longer overclaims that algebraic automatically means `n^{-3/2}`, no longer compresses the CFG story into an apparent theorem bundle, and no longer blurs counting generating functions with probabilistic partition-function objects.

## Note items addressed

- Addressed the highest-priority gaps around unique decomposition, the `\SEQ` rule, the uniform probability model behind bivariate expectations, the labeled-product explanation, and the overconfident algebraic/CFG/asymptotic ending.
- Addressed several medium gaps around tagged disjoint union, coefficient-level product meaning, the role of `\mathcal E` and `\mathcal Z`, the Catalan indexing convention, the bivariate binary-word extraction step, and the exercises.
- Reduced the local contribution to the manuscript-wide drift between counting objects and weighted/probabilistic objects by explicitly warning against silently identifying them.

## Pushback and deferrals

- I still did **not** add a plane-tree figure. I compensated with slower prose and a more explicit structural explanation, but a figure could still help if we later decide to add diagrams systematically.
- I treated the `\CYC` rule as a black-box labeled construction rather than trying to fake a fully elementary proof. That feels like the right compromise for this audience.
- I deliberately kept the final CFG / algebraic / asymptotic discussion at the level of preview and removed theorem-sounding universal claims. The real analytic consequences belong in later chapters with the proper hypotheses in place.
