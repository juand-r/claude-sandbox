# Chapter 12 Changelog

## What I changed

- Rewrote the chapter around a single central question: what exactly is a WFA supposed to approximate? The new opening explicitly separates exact structure, finite-data fit, exact rationality of the surrogate, and asymptotic conclusions about the teacher.
- Added a dedicated approximation-target section that distinguishes string-probability fitting, conditional fitting, length-statistics fitting, support-structure fitting, and low-rank Hankel approximation.
- Cleaned up the black-box distillation section so score fitting and full probabilistic distribution fitting are no longer treated as interchangeable.
- Fixed the rational-recurrence display so it now depends on the actual input symbol.
- Simplified the spectral/Hankel section by keeping the core finite-rank theorem and the idea of spectral reconstruction while dropping the opaque pseudoinverse formulas that were doing more to intimidate than to teach.
- Repaired the one-letter section so it no longer collapses the length PGF and the Chapter 9 counting/entropy object into the same series.
- Removed the false/stretched entropy proposition at the end and replaced it with a much safer payoff section: a WFA surrogate gives an exact rational model for the surrogate itself, and any inference about the original LLM depends on the chosen target and the quality of approximation.
- Corrected the “PCFG gives ground-truth rational structure” slip by replacing it with language about known formal structure in synthetic settings.

## Note items addressed

- Addressed the highest-priority conceptual problem in the note by making the approximation target explicit rather than leaving the chapter to slide between scores, probabilities, and generating functions.
- Addressed the clearly problematic recurrence display, the one-letter/entropy conflation, the overstrong payoff proposition, and the PCFG/rational wording error.
- Reduced local pressure on the manuscript-wide approximation-program instability by making Chapter 12 itself define the relevant choices instead of pretending that “WFA-like” is already precise.

## Pushback and deferrals

- I kept the spectral/Hankel and AAK material at black-box depth. For this chapter, I think the right repair is conceptual organization, not a full graduate-level treatment of operator theory.
- I also intentionally stopped short of claiming that any successful surrogate tells us the teacher's asymptotic singularity type. That is exactly the point that should remain conditional on the approximation target and fidelity notion.
