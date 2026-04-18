# Chapter 11 Changelog

## What I changed

- Rewrote the chapter as an explicit survey-plus-modeling-stance chapter rather than a pseudo-proof chapter. The opening now states directly that recognition/simulation theorems do not automatically determine generating-function type.
- Removed the concrete parity mistakes from the old draft: the chapter no longer says parity is computed by a single threshold gate, and it no longer tries to extract a false `z=-1` generating-function moral from parity.
- Softened the single-pass-transformer story so `\mathsf{TC}^0`-style results motivate finite-state / WFA approximations without pretending to prove rational generating functions for actual output distributions.
- Reframed Hahn's theorem as an architectural warning about length-unbounded tasks rather than as a direct theorem about poles and branch points.
- Narrowed the RNN/WFA and transformer/WFA sections so they now separate exact finite-state simulation from much stronger global asymptotic conclusions.
- Removed the old chain-of-thought `\Rightarrow` algebraic `\Rightarrow n^{-3/2}` overclaim. The chapter now says only that CoT makes richer pushdown-like or beyond-finite-state behavior more plausible, not that a specific asymptotic regime automatically follows.
- Added a three-level synthesis at the end that clearly separates theorem, modeling stance, and open analytic question.

## Note items addressed

- Addressed the highest-priority correctness issues in the note: the parity errors, the too-strong `\mathsf{TC}^0`/balanced-parentheses rhetoric, the unjustified recognition-to-GF leap, the overstrong simulation-to-asymptotics claims, and the blanket CoT-to-`n^{-3/2}` story.
- Addressed the broader theorem-vs-heuristic problem by making the whole chapter explicitly about suggestive expressivity evidence rather than settled analytic consequences.
- Reduced local pressure on the manuscript-wide approximation-target issue by turning Chapter 11 into motivation for Chapter 12 rather than pretending the target is already fixed.

## Pushback and deferrals

- I kept the core expressivity theorems as black boxes and did not try to unpack all their technical hypotheses. This chapter is now intentionally a map of the literature, not a self-contained complexity-theory text.
- I also chose not to force a specific generating-function object into every paragraph. The chapter's main job is to stop overclaiming and to hand off the exact approximation question to Chapter 12.
