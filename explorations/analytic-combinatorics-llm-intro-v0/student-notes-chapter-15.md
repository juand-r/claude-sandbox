# Student Notes on Chapter 15: "Phase Transitions in Language Model Output"

## Overall impression

Clear bridge between Ch4's singularity classification and statistical-physics
phase transitions. The Catalan worked example is the right choice. The
empirical literature survey is well-organized with correct attributions
(Nakaishi = GPT-2, Arnold = Pythia/Mistral/Llama).

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Lines 155-173 | The Catalan partition function worked example has some algebra that's hard to follow. The expansion "1 - 4e^{-β} ≈ ε" (line 157) skips the step that $4e^{-\beta_c} = 4 \cdot 1/4 = 1$, so $1 - 4e^{-\beta} = 1 - e^{-\epsilon}$. A student might not see why $4e^{-\beta_c - \epsilon} = e^{-\epsilon}$. |
| 2 | LOW | Line 327 | "Gap 2 among the ten open problems" — correct (fixed in earlier pass). |
| 3 | LOW | Line 392-395 | Notes section says "Chapter 17: briefly, the EBM formulation..." — this was already fixed to remove the incorrect Ch17 reference. Verify the fix is in place. |

## Summary

Correct attributions throughout. The worked Catalan example could use one
more line of algebra. Otherwise solid.
