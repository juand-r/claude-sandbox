# Chapter 10 Changelog

## What I changed

- Rebuilt the chapter around one clean `EOS` convention: `\EOS` is now outside the ordinary vocabulary `\Sigma`, the model emits symbols from `\Sigma \cup \{\EOS\}`, and the actual returned outputs live in `\Sigma^*`.
- Removed the old ambiguity about what the sample space is. Histories, outputs, and termination are now spelled out explicitly, and the factorization formula applies only to content strings in `\Sigma^*`.
- Kept the chapter's best abstraction --- the LLM as the induced conditional family rather than the network weights --- while stripping out the probabilistically unstable parts of the old draft.
- Replaced the incorrect transformer-tightness proof sketch with a black-box theorem reference to Du et al., so the chapter no longer misstates the Chapter 8 criterion or pretends that positivity of softmax alone proves almost-sure halting.
- Removed the old attempt to import Chapter 9's stationary entropy-rate theory directly to terminated autoregressive models. The chapter now says explicitly that this transfer is nontrivial and should not be assumed for free.
- Clarified the two generating functions attached to an LLM: the length PGF is defined cleanly, while the counting-type typical-set GF is mentioned only at the level of distinction, not rederived in a shaky way.
- Fixed the unigram example's length PGF formula by removing the extra factor of `z`.
- Softened the final preview so later “close to rational” claims are deferred to Chapters 11 and 12 instead of being asserted here.

## Note items addressed

- Addressed the highest-priority foundational problems in the note: the `EOS` convention, the sample space, the broken tightness proof, the misuse of Chapter 9 entropy-rate machinery, and the wrong unigram PGF.
- Addressed the earlier drift between length PGFs and counting-type GFs by making the distinction explicit without pretending this chapter alone fully rebuilds the Chapter 9 bridge.
- Reduced local pressure on the manuscript-wide theorem-vs-heuristic problem by black-boxing Du et al. instead of giving a misleading pseudo-proof.

## Pushback and deferrals

- I intentionally did **not** define a stationary entropy rate for a terminated autoregressive model in this chapter. That would require additional construction, and the old version's casual import from Chapter 9 was too loose to keep.
- I also left the transformer architecture discussion extremely light. For this chapter's job, the probability object matters more than a mini tutorial on attention mechanics.
