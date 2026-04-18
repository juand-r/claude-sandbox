# Student Notes on Chapter 6: "Formal Languages and the Chomsky Hierarchy"

## Overall impression

A well-organized survey chapter covering DFA/NFA, Myhill-Nerode, regular
expressions, CFGs, pushdown automata, pumping lemmas, and the four-level
hierarchy. The "analytic-combinatorial payoff" section at the end ties
everything back to GFs effectively.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Line 51 | "the close parallel between regular expressions and the symbolic method will be made precise in Chapter 7" — Ch7 is about WFAs, not about the regular-expression/symbolic-method parallel per se. The connection is implicit in Ch7's transfer-matrix approach but not "made precise" in the way the reader might expect. |
| 2 | MEDIUM | Line 121-126 | "levels 2 and 3 of the hierarchy" — the Chomsky hierarchy numbers Type 3 = regular, Type 2 = CF, Type 1 = CS, Type 0 = RE. So "levels 2 and 3" means CF and regular. But the text says "we work almost exclusively within levels 2 and 3" — shouldn't this say "Types 2 and 3" or "the regular and context-free levels"? The word "levels" vs "types" could confuse since higher type number = lower expressive power. |
| 3 | LOW | Chapter | No exercises. A DFA-to-GF exercise would reinforce the rational-GF connection. |

## Summary

Clean chapter with no mathematical errors. The hierarchy is correctly stated
and the separation examples are standard. The main pedagogical gap is the
absence of exercises.
