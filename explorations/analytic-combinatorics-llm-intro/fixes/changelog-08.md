# Chapter 08 Changelog

## What I changed

- Recentered the chapter on the right core idea: local normalization does not imply a proper global distribution on finite outputs, and `F(1)=1` is the relevant probabilistic sanity check.
- Removed the old overstatement that every generating-function manipulation in the book presupposes a proper probability distribution, and replaced it with a clearer distinction between probabilistic interpretation and analytic study.
- Simplified the PCFG section so it introduces derivation probabilities and the branching-process intuition without pretending to prove branching-process theorems from scratch.
- Rewrote the Booth-Thompson discussion to avoid the false blanket criterion `\rho(M) \le 1` as a complete theorem. The chapter now states only the safe subcritical/supercritical lessons, explicitly flags the critical case as delicate, and includes the `S \to S` counterexample.
- Clarified the meaning of `F_A(1)` and `F_S(1)`: they record total probability of finite outputs, and defectiveness is now treated as a probabilistic failure rather than an analytic impossibility.
- Reframed Chi's theorem modestly: consistency removes one foundational obstruction, not all later analytic ones.
- Rebuilt the Du-et-al. section around the stopping-hazard product formula so the divergence criterion is at least intuitive, even though the measure-theoretic theorem itself remains a black box.
- Replaced the old critical-boundary overclaim with concrete non-tight and barely-tight examples, and explicitly said that borderline models do **not** all share one universal singularity type.
- Removed the misleading Transformer proof sketch and kept only the black-box theorem statement, so the text no longer tries to prove architectural tightness from a vague “softmax is positive” argument.

## Note items addressed

- Addressed the biggest mathematical/precision issues flagged in the note: the overbroad Booth-Thompson statement, the conflation of `F(1)=1` with analytic validity, the incorrect critical-boundary singularity story, the overstrong Chi consequence, and the weak Transformer proof sketch.
- Addressed several medium gaps by adding the derivation-probability example, the explicit product formula for survival, and a more honest discussion of heavy tails and almost-sure halting.
- Reduced local pressure on the manuscript-wide probability/counting drift by making the chapter itself distinguish properness from rationality, algebraicity, and singularity type.

## Pushback and deferrals

- I still did **not** try to state the sharpest full Booth-Thompson theorem. The chapter now gives a safe summary instead, because the exact branching-process hypotheses are too technical for the current pedagogical level.
- I also kept the Du et al. and Transformer tightness results as black boxes. That is deliberate: the old proof sketch was more misleading than helpful.
