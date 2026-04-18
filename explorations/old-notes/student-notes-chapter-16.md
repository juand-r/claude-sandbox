# Student Notes on Chapter 16: "Zipf's Law and Token Distributions"

## Overall impression

Good survey of Zipf explanations (Pitman-Yor, Berman, Mikhaylovskiy,
Michaud). The critical perspective from Piantadosi is well-placed. The
bivariate GF proposal at the end connects back to the analytic toolkit.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Line 59 | Pitman-Yor exponent formula: "the rank-frequency exponent is $s = 1 + 1/a$. For $a = 0.5$, we get $s = 3$" — this is correct ($1 + 1/0.5 = 3$). But the text then says "for $a$ close to $1$, $s$ approaches $2$ from above" ($1 + 1/1 = 2$, correct) and "for $a$ close to $0$, $s$ grows without bound" ($1 + 1/\epsilon \to \infty$, correct). All fine mathematically. |
| 2 | MEDIUM | Line 162 | "This is Gap 4 in the ten open problems listed in Chapter 18." — Ch18 has Gap 4 as "Chomsky-Schutzenberger test for LLM support." The bivariate GF for Zipf/rank is NOT Gap 4. There's no explicit Gap for the bivariate rank-frequency GF in Ch18. This is a cross-ref error — or the Gap numbering needs updating. |
| 3 | LOW | Attributions | Berman (NOT Eliazar), Mikhaylovskiy (NOT Kawakami), Michaud (NOT AlphaZero) — all correct throughout. |

## Summary

Attributions verified correct. One likely cross-ref error (Gap 4 reference
doesn't match Ch18's Gap 4 definition).
