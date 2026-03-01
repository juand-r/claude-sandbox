# Companion Notebook Plan

## Goal
One Jupyter notebook (`companion_code.ipynb`) with runnable code for key
computations in the guide. Organized by chapter. LaTeX source gets pointers.

**Two implementations where possible**: NumPy (readable, pedagogical) and
PyTorch (GPU-ready, relevant to the thesis's ML context).

## Python Environment
- `requirements.txt` in this directory
- venv at `.venv/`
- Packages: numpy, torch, matplotlib, scipy, sympy, jupyter

## Sections

### 0. Setup & Utilities
- FWHT: numpy version and torch version
- Hypercube enumeration, subset ↔ index
- `fourier_coefficients(f)` — compute all coefficients via FWHT
- `eval_boolean_fn(f_hat)` — reconstruct from coefficients

### 1. Ch2 — Boolean Fourier Basics
- Fourier coefficients of AND, Maj_3, parity (verify book examples)
- Parseval verification
- Degree-k truncation + sign-rounding (Maj_3 example)
- Convolution theorem demo

### 2. Ch3 — Influence and Noise
- Compute influences of Maj_3, verify spectral formula
- Apply noise operator T_ρ (verify T_{1/2} Maj_3)
- Noise stability computation

### 3. Ch4 — Hypercontractivity
- Level-k inequality: numerical verification (Maj_3, AND_10)
- LMN bound: compute k* for given parameters

### 4. Ch5 — The WHT
- FWHT step-by-step trace (n=2 and n=3 examples)
- Direct H_n v vs FWHT comparison
- Timing: FWHT vs naive for increasing n

### 5. Ch6 — RM Codes and Degree-Increase
- Construct RM(1,2) codewords, show Walsh degrees
- ⊕_i b_i → full parity (degree n)
- Chow parameters of majority

### 6. Ch7 — Spectral Parameterization Pipeline
- End-to-end: binary vector → spectrum → truncate → reconstruct → sign → error
- Parameter count comparison
- CLT normalization: histogram of w^T x / √d vs N(0,1)

## LaTeX Pointers
Footnotes at relevant examples: "See companion notebook, §X."

## Status
- [x] Create venv + requirements.txt
- [x] Create notebook
- [x] Add LaTeX pointers
- [x] Compile and push
