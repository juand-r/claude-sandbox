# Chapter 17 Changelog

## What I changed

- Rewrote the chapter as an explicitly cautious survey of analytic information theory rather than a pseudo-self-contained theorem chapter.
- Fixed the core object-definition problem in the motif section by separating counting and weighted/probabilistic generating functions instead of mixing both in one inconsistent formula.
- Removed the dropped-in and likely untrustworthy closed form for the `"aba"` motif BGF and replaced it with a clean first-moment computation that is actually explained.
- Removed the unstable Chapter 9-style entropy/radius conflation from the trie and entropy-connection material. The trie theorem now refers directly to Shannon entropy of the source and explicitly warns against confusing that with support/path growth.
- Removed the confused Perron-Frobenius / square-root sentence instead of trying to salvage it.
- Reframed the LLM-transfer section so it now states clearly that analytic information theory is exact for exact finite-state models and only a research program for WFA surrogates of LLMs.
- Added a bit more concreteness to the motif-automaton recipe and cleaned up the trie theorem wording.

## Note items addressed

- Addressed the biggest mathematical problems flagged in the note: the inconsistent motif GF definition, the suspicious `"aba"` formula, the repeated entropy/path-growth conflation, the Perron-Frobenius singularity confusion, and the overstrong WFA-to-LLM transfer claims.
- Addressed the broader theorem-vs-heuristic issue by making the whole chapter much more explicit about black-box classical results versus conditional research-program extrapolations.
- Reduced local pressure on the manuscript-wide approximation drift by making Chapter 17 itself say that preserving the statistic of interest under WFA approximation is the hard part.

## Pushback and deferrals

- I deliberately did **not** try to teach quasi-powers, Mellin transforms, or saddle-point theory in depth here. For this chapter, the right repair is better object discipline and better boundaries on the claims.
- I also chose not to force a fully worked automaton construction for a motif, beyond the overlap-machine description. That would be a useful future enhancement, but the revised chapter is already much safer and clearer than the old one.
