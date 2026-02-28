# Student Notes: Chapter 2 (Fourier Analysis on the Boolean Hypercube)

## Things I found clear
- The Boolean hypercube definition, the ±1 vs {0,1} remark, the conversion formula.
- Parity function definition and the n=3 example listing all 8 basis functions.
- Orthonormality proof — clean and the symmetric difference trick is well explained.
- The dictator, AND, majority, and parity examples are excellent. The step-by-step computation for AND is especially helpful.
- Parseval is stated cleanly and the "energy constraint" interpretation is well motivated.
- Sign-rounding error proof is clean and uses only Markov (from Ch1). The Maj_3 truncation example showing the bound is not tight is a nice touch.
- Convolution theorem proof is complete and readable.

## Confusions / Questions

1. **Why is this called "Fourier analysis"?**
   The chapter uses the word "Fourier" throughout but never really explains the analogy to classical Fourier analysis beyond one parenthetical comparison in §2.2. A student familiar with Fourier series on [0,2π) would benefit from a paragraph explaining: "Just as sin/cos form an ONB for L²([0,2π)) and we decompose periodic functions into frequencies, here the parity functions form an ONB and we decompose Boolean functions into 'frequencies' indexed by subsets S. The 'degree' |S| plays the role of frequency." This is implicit but never stated explicitly.

2. **The majority example (§2.6.3) gives the Fourier coefficients but doesn't show how they were computed.**
   The AND example shows every step of the computation. The majority example just lists the answers. I understand it would be tedious for 8 terms × 8 inputs, but at least computing one coefficient explicitly (say f̂({1})) would help me verify I understand the procedure. Or at least say "the computation is analogous to the AND case."

3. **The "sgn" function is used in the majority definition but never defined.**
   Maj₃(x) = sgn(x₁ + x₂ + x₃). What does sgn return when the argument is 0? For odd n this doesn't arise, but for general n it does. This should be addressed, especially since sgn is later used for rounding (Proposition 2.11) where sgn(0) is ambiguous.

4. **Energy decomposition (§2.7): the claim about random Boolean functions.**
   "For a random Boolean function, the expected energy at degree k is C(n,k)/2^n." This is stated without proof or even a sketch. I believe it but I'd like to see why. Is it because E[f̂(S)²] = 1/2^n for each S when f is random? Why?

5. **Plancherel proof is too terse.**
   "Expand f and g in the Fourier basis and use orthonormality." That's one sentence. A student trying to verify this would want to see:
   ⟨f,g⟩ = E[f(x)g(x)] = E[∑_S f̂(S)χ_S(x) · ∑_T ĝ(T)χ_T(x)] = ∑_S ∑_T f̂(S)ĝ(T) E[χ_S χ_T] = ∑_S f̂(S)ĝ(S).
   That's 2-3 lines and would be much more helpful than "use orthonormality."

6. **Dyadic convolution: why "dyadic"?**
   The term "dyadic" is used but not explained. I assume it refers to the group Z₂ⁿ structure but this isn't said. (Group theory comes in Ch6, so maybe just say "the name will be explained in §6.3" or something.)

7. **Dyadic convolution: where does this appear in the thesis?**
   The text says "Two additional Fourier identities that are used in the thesis" but doesn't say where the convolution theorem specifically is used. Plancherel clearly is (noise stability), but the convolution? The WHT chapter connects it to the WHT, but is the convolution itself directly used?

8. **The transition from §2.7 (energy decomposition) to §2.8 (truncation) could be smoother.**
   I understand that energy decomposition gives us a way to measure spectral concentration, and truncation exploits it. But it would help to have a sentence like: "Now that we can measure how much energy is at each degree, the natural question is: what happens if we discard the high-degree terms?"

9. **f^{>k} notation.**
   The notation f^{>k} is defined in passing as "f - f^{≤k}" but it took me a second read to see this. Might be clearer if it had its own displayed equation, since it's used in the proof immediately after.

## Minor issues
- The truth table for Maj₃ has a header with 4 columns (x₁, x₂, x₃, Maj₃) but the tabular spec says {ccccc} — five columns. This would produce an extra empty column in the PDF.
- Definition of "degree" (Def 2.5) uses "d" for the maximum degree, but d is also used later for the layer width. Potential notation collision (though different chapters, so probably fine).
