# Chapter 06 Changelog

## What I changed

- Rewrote the chapter as an honest survey/orientation chapter rather than a fake proof chapter. The opening now says directly that major automata-theory results are being imported as black boxes and that the hierarchy only gives one-way analytic guidance, not a perfect classification.
- Added concrete beginner-facing setup in the language preliminaries: an explicit example word, a plain-English explanation of “free monoid,” and a simple generating-function example for `\Sigma^*`.
- Cleaned up the DFA/NFA material with a less abrupt extension-to-strings explanation, a subset-construction intuition sentence, and a more usable regular-language example.
- Made the Myhill-Nerode and pumping-lemma sections more honest by marking them as black boxes and by explicitly reminding the reader that pumping lemmas are necessary conditions only.
- Reworked the regular-expression section so the semantics of concatenation and star are explicit, and so the comparison with the symbolic method is now heavily qualified rather than dangerously naive for counting distinct words.
- Replaced the broken Dyck-language example with a consistent unambiguous first-return grammar and a matching algebraic generating-function equation.
- Simplified the Chomsky-hierarchy discussion so it stays at the “map of language models” level instead of trying to compress too many hard complexity-theory facts into one pass.
- Rebuilt the analytic-payoff section around implication language: regular implies rational, unambiguous CFG implies algebraic, and higher levels no longer pretend to determine one unique generating-function type. I also replaced the old vague linear-system sketch with the cleaner matrix resolvent formula for regular languages.
- Removed the impossible claim that context-sensitive languages can have word-count sequences growing faster than any geometric bound; the chapter now states the correct universal bound `|L \cap \Sigma^n| \le |\Sigma|^n`.

## Note items addressed

- Addressed the three biggest mathematical/precision problems flagged in the note: the naive regex/symbolic-method analogy, the mismatched Dyck example, and the impossible supergeometric-growth claim.
- Addressed the broader overstatement problem by replacing “faithful hierarchy-to-analytic-type correspondence” language with one-way structural implications and explicit cautions.
- Addressed several pedagogical gaps with small examples, black-box labels, clearer semantics, and more cautious closure/pumping statements.

## Pushback and deferrals

- I intentionally kept this chapter at survey depth. I did **not** try to prove Myhill-Nerode, Kleene, or CFG=PDA in full, because that would turn Chapter 6 into a second textbook on automata theory.
- I also trimmed some of the old higher-level complexity-theory detours. For this book, the useful role of the upper hierarchy levels is mainly cautionary: they tell us when the tidy regular/context-free generating-function theorems stop being reliable defaults.
