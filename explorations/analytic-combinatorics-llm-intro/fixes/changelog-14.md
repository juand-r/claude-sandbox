# Chapter 14 Changelog

## What I changed

- Rebuilt the chapter around one precise sample-space convention, aligned with Chapter 10: `\EOS` is outside `\Sigma`, complete outputs live in `\Sigma^*`, and `\mu(w)` means “emit exactly the content string `w` and then stop.”
- Removed the unstable parts of the old chapter and focused the whole discussion on the exact comparison between global Gibbs reweighting of complete strings and local tokenwise temperature scaling.
- Replaced the old local/global proposition with the sharper prefix-product criterion, so equality is no longer misstated in terms of per-step partition factors being individually prefix-independent.
- Replaced the underdefined toy example with a fully specified finite model whose local/global temperature mismatch can actually be computed cleanly.
- Removed the broken ARM–EBM theorem formulas instead of trying to patch a sign-inconsistent statement.
- Removed the overstrong Lin–Tegmark–Rolnick / bounded-context heuristics and the mathematically wrong generating-function display in the creative/greedy section.
- Corrected the top-`k` / nucleus discussion so the chapter now says these heuristics preserve autoregressive prefix conditioning but lose any clean global Gibbs interpretation.
- Clarified the low-temperature limit distinction: global Gibbs concentrates on global modes, while local temperature `T \to 0` gives greedy local decoding, and those need not coincide.

## Note items addressed

- Addressed the highest-priority issues in the note: sample-space ambiguity, the too-weak local/global equality criterion, the bad worked example, the false “breaks Markov structure” claim, and the wrong formula in the creative/greedy section.
- Addressed the broader structural issue by making this chapter itself say clearly that global Gibbs temperature and local decoding temperature are different objects.
- Reduced local pressure on the book-wide temperature storyline by removing theorem-sounding or formula-level claims that the chapter could not responsibly support.

## Pushback and deferrals

- I intentionally removed the ARM–EBM and Lin–Tegmark–Rolnick sections rather than trying to repair them in place. In their old form they were creating more confusion than insight for this chapter's main job.
- I also kept the global-partition-function finiteness discussion light. The chapter now says where the issue lives without pretending to settle every convergence condition before Chapter 15.
