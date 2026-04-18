# Chapter 09 Changelog

## What I changed

- Rebuilt the chapter around a corrected version of the headline identity. Instead of pretending that a fixed-`ε` typical-set count already gives `h = \log_2(1/R)` exactly, the chapter now uses a shrinking window `\varepsilon_n \to 0` and proves the exponential growth rate in that form.
- Added a short proof sketch for the existence of entropy rate and for the identity with the limit of conditional entropies, rather than treating both as unexplained routine facts.
- Rewrote the finite-state discussion so it no longer confuses support/path growth with Shannon entropy rate. The chapter now explicitly separates topological/support entropy from measure-theoretic entropy and includes a biased one-state counterexample.
- Strengthened the chapter's best conceptual section --- the distinction between a counting-type typical-set GF and a length PGF --- with cleaner statements and a concrete geometric-length example.
- Reframed the literature survey so the Shannon, Kontoyiannis, Takahashi, and Scheibner discussions are clearly labeled as modern reinterpretations or empirical estimates of `h`, not as direct derivations of a canonical generating-function radius.
- Removed the old theorem-sounding “slow convergence diagnoses singularity type” section and replaced it with an explicit research hypothesis / open-program framing.
- Tightened the final summary so it now states only the corrected rigorous conclusion and the object distinction, instead of repeating unsupported claims about singularity diagnostics.

## Note items addressed

- Addressed the chapter's biggest mathematical problem: the identity `h = \log_2(1/R)` is now justified in a form that actually matches the typical-set argument.
- Addressed the genuinely wrong finite-state remark by distinguishing support-growth entropy from Shannon entropy rate.
- Addressed the biggest overreach in the last section by downgrading it from an apparent theorem to an explicit research hypothesis.
- Addressed several precision gaps around `\delta_n`, the role of `F(1)=1`, the difference between counting growth and length distribution, and the status of the entropy-estimation literature.

## Pushback and deferrals

- I still did **not** make the entropy-to-generating-function bridge fully canonical. The chapter now says this out loud: one must choose a shrinking typicality window, and different reasonable choices lead to the same exponential rate rather than one uniquely privileged generating function.
- I also chose not to force a fake theorem connecting singularity type to entropy-estimator convergence. At this point in the manuscript, that really is better treated as a research direction than as settled mathematics.
