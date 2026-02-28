# Student Notes: Chapter 6 (LTFs, Reed-Muller Codes, and Groups)

## Things I found clear
- LTF definition is clean. The examples (dictator, majority, weighted) are good. The note that parity is NOT an LTF is important and well-placed.
- Chow's theorem statement is clear. The interpretation ("essential information lives in degree ≤ 1") is well stated.
- The variable naming remark (Remark 6.3) is very helpful — this is exactly the kind of confusion that would trip up a reader.
- Reed-Muller code definition in GF(2) is now correct and clean.
- The ±1 perspective paragraph explaining why GF(2)-monomials ≠ Walsh monomials is important and well-written. The "unitriangular" change-of-basis argument is the right level of detail.
- The three RM properties relevant to the thesis are concrete and useful, especially (iii): "sign projection is not RM decoding."
- The group theory section is clean and concise. Characters = parity functions is a satisfying punchline.
- The comparison table (classical vs Boolean Fourier) is excellent.

## Confusions / Questions

1. **Chow's theorem proof sketch: "A geometric argument shows this forces w and v to define the same halfspace."**
   This is where the proof would be interesting, and it's exactly where the sketch stops. The "geometric argument" is the whole substance of the proof. For an expository guide, either give the argument or at least describe it: "The key insight is that the Chow parameters determine the orthogonal projection of f onto the degree-1 subspace, and for LTFs, this projection has a one-to-one relationship with the normal vector of the halfspace (up to positive scaling)."

2. **Spectral concentration of LTFs: "most of the spectral energy is within the first O(√n) degrees."**
   This is stated without proof or reference. Is this a theorem? Whose result? The text cites Harsha et al. for the total influence bound I[f] = O(√n), which implies the spectral "center of mass" is at O(√n), but that's not the same as saying most energy is at degree ≤ O(√n). The level-k inequality from Ch4 combined with I = O(√n) gives W^k ≤ (e√n/k)^k, which becomes small when k ≫ e√n. So the tail bound kicks in at degree ≈ e√n. But this isn't explicitly stated.

3. **I[f] = Θ(‖w‖₁/‖w‖₂) — what is Θ here?**
   The text says "for f = sgn(w^T x) with ‖w‖₂ = 1: I[f] = Θ(‖w‖₁/‖w‖₂)." But this is an asymptotic statement — in what parameter? In n? Also, the "by Berry-Esseen arguments" is vague. The connection between Berry-Esseen and influence is not obvious. A sentence explaining the idea (each coordinate's influence is related to how likely that coordinate is to be "pivotal," which can be estimated using the CLT applied to the sum w^T x) would help.

4. **RM(1,n) example: "functions of Walsh-Fourier degree ≤ 1."**
   The text says codewords are evaluation vectors of affine GF(2) functions. It then says these are functions of Walsh-Fourier degree ≤ 1. But what do the codewords look like concretely? For n=2, the affine functions over GF(2) are: 0, 1, b₁, 1⊕b₁, b₂, 1⊕b₂, b₁⊕b₂, 1⊕b₁⊕b₂. These give evaluation vectors (0,0,0,0), (1,1,1,1), (0,1,0,1), (1,0,1,0), (0,0,1,1), (1,1,0,0), (0,1,1,0), (1,0,0,1). Mapping to ±1: (1,1,1,1), (-1,-1,-1,-1), (1,-1,1,-1), (-1,1,-1,1), (1,1,-1,-1), (-1,-1,1,1), (1,-1,-1,1), (-1,1,1,-1). That's 8 = 2³ = 2^{n+1} codewords. OK, checks out. A small worked example like this would be very helpful.

5. **The "unitriangular" change-of-basis claim is stated without proof.**
   "The change-of-basis between the two is unitriangular." This means: expressing GF(2) monomials of degree k in terms of Walsh monomials, the matrix is lower-triangular with 1s on the diagonal (when ordered by degree). This is true because b_i = (1-x_i)/2, so a GF(2)-monomial of degree k = product of (1-x_i)/2 terms = (1/2^k) × a polynomial in χ_S monomials of degree ≤ k, with the leading term being (±1/2^k)χ_{S} at degree exactly k. But "unitriangular" is a strong word that might confuse students who don't know what it means. A one-sentence clarification would help.

6. **GF(2) is never defined beyond "GF(2) = {0,1}".**
   For a student without coding theory background: GF(2) is the field with two elements where addition is XOR and multiplication is AND. Since this is a math guide, a one-line definition with the operation tables (or at least "addition is mod 2") would be helpful.

7. **What is a "linear code"?**
   The text says "RM(r,n) is a linear code" but never defines what a linear code is. For students from the Boolean analysis side who might not know coding theory: a linear code of length N over GF(2) is a linear subspace of GF(2)^N. Its "dimension" is the dimension of this subspace. Its "minimum distance" is the minimum Hamming distance between distinct codewords.

8. **Sign projection is NOT RM decoding (point iii) — this is a crucial subtlety.**
   The text says: "The sign of a degree-k polynomial can have Fourier support up to degree n." This is correct but I'd like to see WHY. Example: the degree-1 polynomial (x₁+x₂+x₃)/2 has sign = Maj₃, which has nonzero f̂({1,2,3}) — a degree-3 coefficient. So sgn applied to a degree-1 function produces a function with degree-3 terms. The sign function "creates" high-degree structure. A one-line example like this would nail the point.

9. **Characters of Z₂ⁿ theorem: why are all characters real-valued?**
   The proof shows χ(e_i) ∈ {+1, -1}, hence χ takes values in {+1,-1}^n ⊂ ℝ. The text states this as a fact before the proof. For a student, the ordering is slightly confusing — the fact that characters are real is PROVED by the argument (χ(e_i)² = 1 ⟹ χ(e_i) ∈ {±1}), but it's stated as if it's obvious beforehand.

10. **The three topics (LTFs, RM codes, group theory) feel somewhat disconnected.**
    The chapter covers three different subjects. The LTF section connects to Ch3 (influence) and Ch4 (spectral concentration). The RM section connects to Ch2 (truncation) and Ch5 (WHT). The group theory section connects to Ch2 (Fourier basis). But the three sections don't connect to EACH OTHER within this chapter. A paragraph at the beginning or end tying them together would help: "All three perspectives — computational (LTFs), coding-theoretic (RM), and algebraic (groups) — illuminate the same central phenomenon: the Walsh-Fourier basis is the natural tool for analyzing binary-valued functions."

11. **No exercise or worked example for the RM code.**
    The n=10, k=3 example with 176 parameters is good for the thesis connection, but a small worked example (n=2, r=1) showing the actual codewords in both GF(2) and ±1 conventions would be very helpful.

## Overall impression
This chapter tries to cover a lot — three fairly different topics — and does a reasonable job. The main weakness is that the three sections feel like they were written independently. The LTF material is the most relevant to the thesis and could use slightly more development (especially the spectral concentration claim and Chow's theorem proof). The RM code section has improved significantly with the corrected ±1 perspective. The group theory section is clean but brief.
