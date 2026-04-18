# Student Notes on Chapter 14: "Gibbs Measures and Temperature Decoding"

## Overall impression

The local-vs-global temperature gap (Proposition ch14:prop-local-global) is
the key insight and is well-presented with a concrete 2-token example. The
ARM-EBM bijection section is clear. Cross-references were fixed in earlier
passes and are now correct.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Line 148 | The marginal formula for $p_\beta(a \mid w_{<t})$ has a complex expression with $\vphantom{X}$ that looks like a LaTeX artifact. The formula itself is conceptually important but may not render cleanly. |
| 2 | LOW | Line 189 | "Du et al. 2023 surveys EBMs in natural language processing" — actually Du et al. 2023 is specifically about tightness, not a general EBM survey. The description is slightly inaccurate. |
| 3 | LOW | Line 196 | "Flajolet and Sedgewick, Chapter XII" — Ch XII of FS2009 is about "Multivariate Asymptotics," not Boltzmann sampling. Boltzmann sampling is in Chapter VII (or the Duchon et al. paper). Check this reference. |

## Summary

Strong chapter. The proposition and example clearly demonstrate why local
temperature != global Gibbs. One potentially incorrect FS2009 chapter
reference to check.
