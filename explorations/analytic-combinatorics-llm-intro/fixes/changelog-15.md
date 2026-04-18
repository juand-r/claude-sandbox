# Chapter 15 Changelog

## What I changed

- Rewrote the chapter so it no longer treats `Z(\beta)=\sum_w \mu(w)^\beta` as if it were automatically an ordinary generating function after the substitution `z=e^{-\beta}`.
- Removed the unstable free-energy derivative classification and the false pole/square-root `\Rightarrow` first/second-order theorem story. The chapter now speaks more cautiously about nonanalyticity and empirical crossover signatures.
- Replaced the flawed Catalan derivative example with a clean algebraic-critical-tail prototype: `\beta_c=\log 4` and critical weights of order `n^{-3/2}`.
- Explicitly separated the mathematically defined **global** Gibbs partition function from the **local** temperature-decoding procedures used in the empirical LLM papers, instead of treating them as if they were measuring the same object.
- Rewrote the empirical section so it is clearly about suggestive local-temperature evidence, not a proof that the global partition function has a specific singularity or universality class.
- Replaced the old PCFG bridging paragraph with a much safer conjectural proposal that does **not** apply Chomsky-Schützenberger directly to `\sum_w \mu(w)^\beta`.
- Replaced the exercises that depended on the broken derivative classification with simpler exercises that actually fit the repaired chapter.

## Note items addressed

- Addressed the biggest mathematical errors flagged in the note: the misuse of Chapter 4 OGF language for `Z(\beta)`, the broken free-energy derivative classification, the bad Catalan/proposition/exercise chain, the false finite-model analyticity claim, and the direct misuse of the PCFG counting theorem on the partition sum.
- Addressed the major conceptual mismatch between global Gibbs temperature and empirical local decoding temperature by making that distinction explicit in the empirical section itself.
- Reduced local pressure on the manuscript-wide temperature storyline by turning the analytic-combinatorics explanation into an explicit conjectural bridge rather than a theorem-sounding conclusion.

## Pushback and deferrals

- I intentionally did **not** rebuild a full statistical-mechanics free-energy formalism here. The old attempt was too brittle, and for this audience the safer chapter is the one that states the right object and the right limitations.
- I also left the empirical finite-size-scaling language somewhat high level. A full pedagogical treatment of susceptibility, order parameters, and thermodynamic limits would take the chapter too far off its main bridge-building job.
