# Chapter 16 Changelog

## What I changed

- Rewrote the chapter as a careful survey chapter rather than a theorem-heavy one, with the opening now explicitly saying that the goal is to compare explanation families and identify what an eventual analytic-combinatorics treatment would actually have to model.
- Fixed the rank/tail confusion near the start by separating type-count tails from token-weighted mass.
- Removed the broken Pitman–Yor exponent display and the internally inconsistent `s = 1 + 1/a` discussion. The chapter now keeps only the safe qualitative facts it actually needs: heavy-tailed behavior and vocabulary growth of order `V(n) \asymp n^a`.
- Tightened the Berman section so it no longer treats standard Pitman–Yor vocabulary-growth facts as speculative.
- Reframed the Mikhaylovskiy section so it is explicitly about **local** decoding temperature and empirical windows, not about a settled theorem on the global partition function.
- Repaired the multinomial proposition by adding the needed strict-order assumption.
- Recast the bivariate generating-function section as a speculative research proposal rather than a fake application of standard symbolic-method marking theorems to rank.
- Removed the exercises that inherited the old Pitman–Yor/exponent instability and replaced them with simpler exercises that match the repaired chapter.

## Note items addressed

- Addressed the biggest mathematical problems flagged in the note: the rank/tail conflation, the broken Pitman–Yor formula block, the misleading Berman/PY wording, the missing distinctness assumption in the multinomial proposition, and the overclaimed BGF/singularity proposal.
- Addressed the local/global-temperature carryover issue by explicitly reminding the reader that the temperature window story is about local decoding temperature.
- Reduced local pressure on the manuscript-wide theorem/heuristic boundary by making the chapter consistently behave like a survey plus proposal chapter rather than a source of new proved analytic claims.

## Pushback and deferrals

- I deliberately did **not** reinsert a precise Pitman–Yor rank exponent formula because the old version was internally inconsistent and the chapter does not need that formula to play its intended survey role safely.
- I also kept the Berman and quantization sections high level. For this chapter, the right repair is credibility and conceptual hygiene, not maximal technical detail.
