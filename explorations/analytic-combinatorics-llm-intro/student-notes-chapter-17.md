# Student Notes on Chapter 17: "Motif Statistics and Analytic Information Theory"

## Overall impression

The most classical chapter in Part V. The autocorrelation polynomial and
bivariate GF framework are well-explained. The trie-depth result connects
nicely to Ch9's entropy rate.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | MEDIUM | Lines 88-94 | Autocorrelation of "aba": the text says $c_1 = 1$ because suffix "a" matches prefix "a". But autocorrelation convention varies — some authors use overlap at offset $k$, others at length $k$. The definition (line 47) says "$c_k = 1$ if the suffix of $M$ of length $k$ equals the prefix of $M$ of length $k$." For $k = 1$: suffix of length 1 is "a", prefix of length 1 is "a". Match → $c_1 = 1$. For $k = 2$: suffix "ba" vs prefix "ab". No match → $c_2 = 0$. So $C(z) = 1 + z$. This is correct. |
| 2 | MEDIUM | Lines 96-100 | The bivariate GF formula $F(z,u) = C(z/2)/[C(z/2) - (u-1)z^\ell/2^\ell] \cdot 1/(1-z)$ — this is stated from the Guibas-Odlyzko-Nicodeme framework without derivation. For a student, this is a "miracle" formula. A reference to where in the cited papers it comes from would help. |
| 3 | LOW | Line 198 | "the effective entropy rate $h_A$ of the WFA" — uses $h_A$ without prior definition in this chapter. Should specify this is the entropy rate from Ch9. |

## Summary

Mathematically sound. The "aba" worked example is correctly computed. The
bivariate GF formula is stated without derivation, which is acceptable for a
survey chapter but could frustrate a student wanting to verify it.
