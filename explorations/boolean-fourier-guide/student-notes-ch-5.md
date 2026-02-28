# Student Notes: Chapter 5 (The Walsh-Hadamard Transform)

## Things I found clear
- Recursive definition of Hadamard matrices is clean. The H₂ example helps.
- H_n = H_1^{⊗n} is a good way to state it.
- All five properties proved cleanly, especially the row-parity identification (property v).
- The WHT = Fourier coefficients theorem (Thm 5.2) with its short proof is the key connection. Very clearly stated.
- Self-inverse property remark nicely connects forward/inverse transform to the thesis pipeline.
- The FWHT algorithm is clear with the pseudocode. The worked example (n=2) with step-by-step butterfly operations is excellent.
- Normalization convention note is a welcome addition.
- FFT comparison table is very helpful for a student who knows the FFT.
- The "no multiplications needed" point for integer inputs is a practical insight.

## Confusions / Questions

1. **Binary-counting order: what exactly is it?**
   The text says "binary-counting order" repeatedly but the mapping is subtle. For n=2, column index c=0 maps to x = ((-1)^0, (-1)^0) = (1,1), c=1 maps to ((-1)^1, (-1)^0) = (-1, 1), c=2 maps to ((-1)^0, (-1)^1) = (1, -1), c=3 maps to ((-1)^1, (-1)^1) = (-1, -1).

   But in the FWHT example, the input v = (1, -1, -1, 1) is said to correspond to f(x₁,x₂) = x₁x₂. Let me check: f(1,1) = 1, f(-1,1) = -1, f(1,-1) = -1, f(-1,-1) = 1. Yes, that matches v = (1,-1,-1,1).

   But WAIT — the column-to-point mapping in property (v) maps c to ((-1)^{c_0}, (-1)^{c_1},...). So c=0 → (1,1), c=1 → (-1,1), c=2 → (1,-1), c=3 → (-1,-1). This means the bit ordering is: c₀ controls x₁, c₁ controls x₂. So the LEAST significant bit of c corresponds to the FIRST coordinate x₁.

   This is potentially confusing because many people would expect c=1 (binary 01) to correspond to x₁=1, x₂=-1 (MSB-first), not x₁=-1, x₂=1 (LSB-first). The guide should make this explicit. An n=2 table mapping c ∈ {0,1,2,3} to (x₁,x₂) would eliminate confusion.

2. **Property (v) proof: the index shift from c_{i-1} to x_i is confusing.**
   The proof maps row r to subset S = {i+1 : r_i = 1}, then writes (H_n)_{r,c} = (-1)^{Σ_{i∈S} c_{i-1}}. The off-by-one between S (1-indexed) and c (0-indexed) is a source of bugs and confusion. A concrete example for n=2 tracing through the indexing would help enormously.

3. **The recursive decomposition H_n v = (H_{n-1}(v₀+v₁), H_{n-1}(v₀-v₁)) — why?**
   This is stated as a consequence of H_n = H_1 ⊗ H_{n-1}, but the derivation is skipped. Let me work it out:

   H_1 ⊗ H_{n-1} = [[H_{n-1}, H_{n-1}], [H_{n-1}, -H_{n-1}]] (block matrix).

   Then: [[H_{n-1}, H_{n-1}], [H_{n-1}, -H_{n-1}]] × [v₀; v₁] = [H_{n-1}v₀ + H_{n-1}v₁; H_{n-1}v₀ - H_{n-1}v₁] = [H_{n-1}(v₀+v₁); H_{n-1}(v₀-v₁)].

   OK that works. But a student who doesn't remember the block structure of the Kronecker product would be stuck. At least showing the block matrix form of H_1 ⊗ H_{n-1} would help.

4. **The FWHT pseudocode processes variables in order ℓ = 0, 1, ..., n-1. But the recursive formula processes x_n first (top-level split), then x_{n-1}, etc. Are these the same?**
   Yes, the in-place iterative algorithm just does the butterflies in a different order than the recursion. Both produce H_n v at the end. But this equivalence is not obvious. A sentence saying "the iterative algorithm processes the same butterflies as the recursion, just in a different (bottom-up) order" would help.

5. **The convolution proposition uses ⊕ for bitwise XOR without defining it.**
   While most CS students know XOR, this is a math guide. A brief "⊕ denotes bitwise XOR (addition mod 2 on each coordinate)" would be helpful.

6. **The convolution proposition: why is the formula H_n(v ⊛ w) = (1/N)(H_n v) ⊙ (H_n w)?**
   I'd expect pointwise multiplication in the spectral domain to correspond to convolution in the spatial domain (standard Fourier result). The 1/N factor comes from the normalization. But there's no proof — just the statement. Since the abstract convolution theorem was proved in Ch2, a pointer saying "this is just Theorem 2.9 written in matrix notation" would suffice.

7. **Hadamard layer: the claim that (1/√N) H_n preserves ℓ₂ norm.**
   The text says this follows from orthogonality. Let me verify: ‖(1/√N)H_n x‖² = (1/N) x^T H_n^T H_n x = (1/N) x^T (N·I) x = x^T x = ‖x‖². Yes. But this uses H_n^T H_n = N·I (property iii). A student would benefit from seeing this one-line calculation written out.

8. **SpectralLinear: "it stores spectral coefficients ŵ and reconstructs spatial weights via w = H_n ŵ."**
   But ŵ only has the low-degree coefficients (the truncated ones). So the reconstruction is really w = H_n ŵ_truncated, where ŵ_truncated is ŵ padded with zeros at high degrees. This subtlety (zero-padding) is important for the FWHT implementation and should be mentioned. Does the FWHT work on partial input? Or do you always need a full N-length vector?

9. **No mention of numerical stability or floating-point behavior.**
   The FWHT uses only addition and subtraction, which is great for integers. But the thesis uses continuous spectral coefficients (from gradient descent), so the reconstruction involves floating-point FWHT. Is numerical stability an issue? Probably not (add/subtract is very stable), but it's worth one sentence.

## Overall impression
This is a strong chapter. The material is concrete and computational, with good examples. The main weakness is the binary-indexing convention, which is crucial for implementation but treated somewhat casually. A student trying to implement the FWHT would need to be very careful about the bit ordering (LSB-first vs MSB-first).
