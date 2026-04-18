# Chapter 02 Changelog

## What I changed

- Reframed the chapter so it is honest about scope: some results are now proved in full, while deeper complex-analysis facts are explicitly labeled as black boxes instead of being smuggled in as if routine.
- Added more beginner-facing setup in the opening complex-number section: principal argument, a reminder about Euler's formula, a proof that absolute convergence implies convergence in `\mathbb{C}`, and a slightly slower geometric-series discussion.
- Rebuilt the radius-of-convergence section around a proved root test and a clean derivation of Cauchy--Hadamard, including boundary caution, the `R=0` / `R=\infty` edge cases, a definition of `\limsup`, and a precise subexponential-factor calculation.
- Reworked the analytic-functions section so open sets, holomorphicity, singularities, and dominant singularities are introduced more carefully, and the big equivalence / power-series-calculus facts are clearly labeled as black-box theorems.
- Replaced the abrupt contour-integral section with a more accessible coefficient-extraction formula proved directly on circles by parameterization and Fourier orthogonality, then derived the circle bound from it.
- Softened the singularity-asymptotics storyline: the nearest-singularity principle, contour deformation, Pringsheim, and the transfer theorem are now named as major results; the pole / square-root / logarithm material is presented as a prototype catalogue rather than a completed general theorem.
- Added a short branch-warning paragraph before square roots and logarithms, removed the overstrong `O(1/n)` closure in the square-root asymptotic, and clarified the exercises so they no longer ask for more than the chapter has actually established.

## Note items addressed

- Addressed the biggest structural gaps around `\limsup`, Cauchy--Hadamard, boundary behavior, contour-integral notation, coefficient extraction, ML-style bounds, and the difference between prototype examples and theorem-level transfer machinery.
- Addressed the precision gaps around open sets, singularities, multiple dominant singularities, simple poles, and symbolic-method notation appearing before Chapter 3.
- Downgraded several previously overconfident claims to preview or black-box status, especially around radius = nearest singularity, contour deformation, Pringsheim, and singularity type controlling asymptotics.

## Pushback and deferrals

- I did **not** prove the heavy complex-analysis theorems in full: analyticity equivalences, nearest-singularity principle, contour deformation, Pringsheim, and Stirling are still used as black boxes. I think that is the right editorial choice for the stated audience as long as the text is explicit about it.
- I kept a brief branch explanation instead of adding a full standalone section on branch cuts. That seems sufficient for this chapter's prototype role, but if later chapters lean harder on complex branches, we may want to expand this further.
