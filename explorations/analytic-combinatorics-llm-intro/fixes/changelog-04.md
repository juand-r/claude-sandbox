# Chapter 04 Changelog

## What I changed

- Reframed the chapter opening so the transfer-theorem slogan is now qualified by explicit analyticity hypotheses instead of sounding like singularity type can always be read off mechanically.
- Reworked the dominant-singularity section to avoid false generalities: finite radius is now assumed, multiple dominant singularities are handled through a concrete `1/(1-z^2)` example, and aperiodicity is defined rather than invoked without explanation.
- Rebuilt the rational-function section around a proved prototype formula for `(1-z/\rho)^{-m}`, so the polynomial-factor story is actually earned before being used in examples.
- Repackaged the Flajolet-Odlyzko theorem as a major black box instead of a half-proved theorem: I added a `\Delta`-domain geometry explanation, a definition of the Gamma function and the special values used later, and an unpacking paragraph explaining the branch choice, the excluded `\alpha` values, and the little-`o` hypothesis.
- Replaced the old too-fast proof sketch with an explicit proof roadmap, clearly labeled as a roadmap rather than something the reader is expected to verify line by line.
- Cleaned up the exponent catalogue, especially the square-root and logarithmic cases, so the chapter no longer talks as if the logarithm literally comes from "`\alpha \to 0`" and no longer uses the sign discussion too loosely.
- Completely repaired the Catalan example: removed the bad intermediate factor-of-2 normalization, rewrote the local expansion in the correct transfer-theorem variable, and extracted the asymptotic directly from the singular term.
- Softened the summary so it no longer says “No other computation is required,” and no longer claims that context-free / algebraic automatically means a universal `n^{-3/2}` law without hypotheses.

## Note items addressed

- Addressed the highest-priority gaps around the opening overclaim, undefined aperiodicity, the too-sweeping multiple-singularity discussion, the missing rational prototype, the theorem unpacking after the transfer statement, the overcompressed proof sketch, the incorrect Catalan normalization, and the summary overstatement.
- Addressed several precision gaps around analytic continuation language, the role of `\Delta`-domains, Gamma-function placement, the logarithmic singularity discussion, and the distinction between analytic background terms and the leading singular term.
- Reduced the local contribution to the manuscript-wide over-universalization of `n^{-3/2}` by turning the Chapter 5 preview into a qualified statement rather than a blanket theorem.

## Pushback and deferrals

- I still did **not** turn the transfer-theorem proof into a fully self-contained proof. I think the right repair here is honesty plus scaffolding: the theorem is now clearly marked as a major black box, and the proof section is framed as a roadmap only.
- I did **not** add a figure for the `\Delta`-domain or the contour picture. A diagram would still help, but the revised prose now explains the slit geometry much more directly.
