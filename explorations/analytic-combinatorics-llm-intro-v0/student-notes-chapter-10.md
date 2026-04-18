# Student Notes on Chapter 10: "Autoregressive Language Models"

## Overall impression

Clean, well-scoped introduction to LLMs as mathematical objects. The
deliberate stripping-down ("an LLM is a probability distribution on Sigma*,
nothing more") is the right framing for this book. The tightness proof sketch
is clear.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Line 82 | "Gap 1 vs Gap 2 dichotomy [CotterellEtAl2023]" — the Gaps are numbered 1a/1b/2/.../10 in Ch18, and the dichotomy described here (probability vs length) doesn't exactly match Ch18's Gap numbering. This forward reference could confuse. |
| 2 | MEDIUM | Line 92 | "generating functions are rational by the transfer matrix theorem of Chapter 6" — Ch6 states the rationality theorem but defers the proof to Ch7. Should say "Chapter 7" or "Chapters 6-7." |
| 3 | LOW | Chapter | No exercises. |

## Summary

Solid chapter with no mathematical errors. The two-GF distinction (length PGF
vs counting GF) is correctly maintained from Ch9.
