# Student Notes on Chapter 7: "Weighted Finite Automata and Rational Power Series"

## Overall impression

Strong chapter. The WFA definition, the rationality theorem F(z) = α(I-zA)^{-1}β,
and the Kleene-Schutzenberger theorem are all well-presented. The Fibonacci
WFA example is a nice callback to Ch1. The Icard hierarchy section provides
good motivation for Part III.

---

## Issues

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | HIGH | Line 4 | "Threads T4 and T5 of the research program described in the introduction" — there is no introduction that defines "Threads." This is leftover jargon from the source literature notes, not the textbook. Should be removed or rephrased. |
| 2 | HIGH | Line 129 | Same issue: "Thread T5" jargon. |
| 3 | MEDIUM | Line 39 | "Wait---$F_2 = 1$ is correct." — informal self-correction left in text. Should be cleaned up (just state the result without the "Wait"). |
| 4 | MEDIUM | Line 95 | "the all-ones vector $\mathbf{1}$ to be a right eigenvector of $A$ with eigenvalue $1$ (since $A\mathbf{1} + \beta = \mathbf{1}$...)" — this parenthetical is dense. The equation $A\mathbf{1} + \beta = \mathbf{1}$ means $A\mathbf{1} = \mathbf{1} - \beta$, so $A\mathbf{1} \le \mathbf{1}$, NOT $A\mathbf{1} = \mathbf{1}$. The text says "right eigenvector of $A$ with eigenvalue $1$" which is wrong — it should say "spectral radius $\rho(A) \le 1$." The text does correct itself ("more carefully, the substochastic matrix $A$ has spectral radius $\rho(A) \le 1$") but the initial claim about eigenvalue 1 is misleading. |
| 5 | LOW | Chapter | No exercises. |
| 6 | LOW | Line 133 | "Chapter 8 addresses the foundational question..." — correct cross-ref. |

## Summary

Two instances of "Thread" jargon from source materials need removal. The
stochastic-WFA eigenvalue discussion (line 95) has a misleading initial
claim that is corrected in the same sentence but should be stated cleanly
from the start.
