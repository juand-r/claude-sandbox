# Boolean Fourier Analysis: An Expository Guide

A self-contained exposition of the mathematical background for the thesis
"Spectral Methods for Binary Neural Networks."

## What this covers

From prerequisites (linear algebra, probability) through:
1. The Boolean hypercube and Fourier analysis on {-1,+1}^n
2. Influence, noise sensitivity, and the noise operator
3. Hypercontractivity (Bonami-Beckner) and spectral concentration (LMN theorem)
4. The Walsh-Hadamard Transform and fast algorithm (FWHT)
5. Linear threshold functions and Chow's theorem
6. Reed-Muller codes and the group-theoretic perspective
7. Application to binary neural networks

## How to compile

```
cd explorations/boolean-fourier-guide
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Output: `main.pdf` (~49 pages).
