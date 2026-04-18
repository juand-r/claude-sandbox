# Chapter 13 Changelog

## What I changed

- Rewrote the chapter so its exact core result is front and center: Boltzmann sampling is exactly a Gibbs distribution with energy equal to size, and the ordinary generating function is exactly the partition function.
- Removed the old casual complexity claims about recursive sampling and universal rejection complexity, and replaced them with a much more cautious tuning/rejection discussion.
- Added the variance identity to the main text so the monotonicity of the expected size is actually justified rather than only used heuristically.
- Cut the misleading `SET` / `CYC` one-liners instead of leaving students with a likely wrong or context-free formula for the omitted hard cases.
- Rewrote the critical-temperature discussion so it focuses on the genuinely relevant limit `x \uparrow \rho` / `\beta \downarrow \beta_c` instead of the misleading “high temperature means `x` close to 1” phrasing.
- Reframed the free-energy section in terms of combinatorial exponential growth rather than reusing the unstable entropy-rate language from Chapter 9.
- Kept the binary and Catalan examples but made them do the right pedagogical work: the Catalan example now clearly shows finite critical partition function with divergent expected size.
- Rewrote the Chapter 14 preview so local tokenwise temperature and global Gibbs reweighting are no longer called exact analogues.

## Note items addressed

- Addressed the biggest problems flagged in the note: the overbroad rejection-complexity theorem, the misleading `SET` / `CYC` formula, the entropy-rate conflation in the free-energy section, the bad “high temperature = `x` near 1” phrasing, and the exactness overclaim in the LLM temperature preview.
- Addressed several medium gaps by moving monotonicity into the main text, clarifying the tuning equation, and making the critical-tail discussion more explicit.
- Reduced local pressure on the manuscript-wide local/global-temperature mismatch by having Chapter 13 itself say that the Chapter 14 bridge is an analogy that needs careful analysis, not an identity.

## Pushback and deferrals

- I deliberately did **not** try to retain a universal rejection-complexity proposition. The safe version of that story really depends on narrower admissibility conditions than the old text stated.
- I also chose not to force a thermodynamic “entropy rate” interpretation onto the coefficient growth exponent. For this chapter, it is much cleaner to keep the thermodynamic and information-theoretic stories adjacent but distinct.
