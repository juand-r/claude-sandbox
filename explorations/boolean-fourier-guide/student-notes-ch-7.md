# Student Notes: Chapter 7 (Application to Binary Neural Networks)

## Things I found clear
- Standard NN background is clean and appropriate for the audience.
- STE explanation is one of the clearest I've seen — the 4-step procedure with the "pretending the derivative is 1" punchline is well written.
- BitNet summary is concise. "Precision leakage" is a good term.
- The row-wise encoding (§7.2.1) is clear and concrete. The compression ratio (176 vs 1024 at k=3, n=10) makes the point.
- The two normalization principles (Parseval for parameters, CLT for activations) are clearly motivated and connected to earlier chapters.
- The chapter-by-chapter map (§7.3) is extremely useful as a reference. Every thesis section is accounted for.
- The worked example (§7.4) is good — tracing the full pipeline from weights → FWHT → truncation → sign → binary weights.
- The parity-vs-majority contrast in the worked example nicely illustrates the thesis hypothesis.
- The dependency graph is helpful for seeing the logical structure.
- The further reading section is well-curated.

## Confusions / Questions

1. **The worked example Step 1: "Apply the FWHT to w, then divide by N = 8. The result is: all zeros except f̂({1,2,3}) = 1."**
   I want to verify this, but the FWHT steps aren't shown. For a *worked* example, I'd expect to see the actual butterfly steps (like in the n=2 example in Ch5). Since this is n=3 with N=8, it would be 3 rounds of 4 butterfly operations each — 12 total. That's not too much to show. At minimum, show the intermediate state after each round.

   Let me try to verify: w = (1,-1,-1,1,-1,1,1,-1).
   Round 0 (h=1): pair (w[0],w[1])→(1+(-1), 1-(-1))=(0,2); (w[2],w[3])→(-1+1, -1-1)=(0,-2); (w[4],w[5])→(-1+1, -1-1)=(0,-2); (w[6],w[7])→(1+(-1), 1-(-1))=(0,2).
   After round 0: (0, 2, 0, -2, 0, -2, 0, 2).
   Round 1 (h=2): pair (v[0],v[2])→(0,0); (v[1],v[3])→(2+(-2), 2-(-2))=(0,4); (v[4],v[6])→(0,0); (v[5],v[7])→(-2+2, -2-2)=(0,-4).
   After round 1: (0, 0, 0, 4, 0, 0, 0, -4).
   Round 2 (h=4): pair (v[0],v[4])→(0,0); (v[1],v[5])→(0,0); (v[2],v[6])→(0,0); (v[3],v[7])→(4+(-4), 4-(-4))=(0,8).
   After round 2: (0, 0, 0, 0, 0, 0, 0, 8).

   Normalized: (0,0,0,0,0,0,0,1). So f̂({1,2,3}) = 1 (index 7 = 111 in binary → S = {1,2,3}).

   The computation checks out. But the student has to do all this themselves to verify. Showing at least the final unnormalized vector (0,0,0,0,0,0,0,8) would help.

2. **Step 2: "f^{≤1}(x) = 0" — what does sgn(0) give?**
   If f^{≤1}(x) = 0 for all x (since all degree-0 and degree-1 coefficients are zero), then sgn(f^{≤1}) is undefined (sgn(0) = ?) for ALL inputs. This is a degenerate case. The bound says Pr[sgn(f^{≤1}) ≠ f] ≤ 1, which is indeed vacuous, but the fact that sgn(0) is the problem isn't mentioned.

3. **The Transformer section (§7.1.2) — is it necessary?**
   The attention mechanism formula is given but never referenced again. The thesis applies to Transformers, yes, but the mathematical background doesn't depend on understanding multi-head attention. This section could be half its current length without losing anything. (Or add a sentence connecting attention weights to binary weights.)

4. **Thesis §2.8 (Multi-layer composition): "the composition identity follows from the spectral formula applied to composed functions."**
   This is the thinnest entry in the chapter-by-chapter map. What IS the composition identity? How does noise stability relate to multi-layer composition? If layer 1 computes f and layer 2 computes g, the composition is g ∘ f. The noise stability of g ∘ f depends on the noise stability of g and the influence structure of f. But this is never developed. At minimum, state the identity.

5. **Spectral parameterization: the error bound cites Prop 2.11, but uses different variable names.**
   The error bound says Pr[w_i(j) ≠ f(j)] ≤ Σ_{|S|>k} f̂(S)². But what is f here? It says "where f is the 'target' Boolean function." But in the spectral parameterization, the target is the TRAINED binary weight row. So f is the ideal binary function that the spectral coefficients are trying to approximate? This is circular — we're training the spectral coefficients, so there's no fixed "target" f. The bound applies to a snapshot: if the current spectral coefficients define a truncated approximation to SOME Boolean function f, then the sign-rounding error is bounded by the tail energy of f. But this is confusing because f keeps changing during training.

6. **Parseval normalization: "Projecting the spectral coefficients onto the unit sphere."**
   This is ŵ ← ŵ / ‖ŵ‖₂. But this projection only guarantees Σ_S ŵ(S)² = 1 for the TRUNCATED coefficients (|S| ≤ k). For the full function including the sgn projection, the Parseval constraint Σ_S f̂(S)² = 1 holds automatically (since f ∈ {±1}). So what does the projection actually achieve? It ensures the truncated approximation has the right energy scale BEFORE the sign is applied. But after the sign, the result is always a Boolean function with Σ f̂(S)² = 1 regardless. The normalization's purpose is to control the magnitudes going into the sign function, but this reasoning isn't explicit.

7. **"For power-of-two d, [1/√d] can even be implemented as a bit-shift."**
   1/√d for d = 2^n is 2^{-n/2}. This is a bit-shift only when n is even (so n/2 is an integer). For odd n, 2^{-n/2} is irrational. This claim is slightly misleading. (For d = 1024 = 2^10, 1/√1024 = 1/32 = 2^{-5}, which IS a bit-shift. But for d = 512 = 2^9, 1/√512 is not.)

8. **The dependency graph is missing some edges.**
   - Kronecker product → Hadamard matrices (the Hadamard definition uses ⊗)
   - Berry-Esseen / CLT → Normalization (used in §7.2.3)
   - FWHT → Spectral parameterization (the reconstruction step uses FWHT)
   These cross-chapter dependencies aren't shown. The graph only covers the theoretical chain, not the applied chain.

9. **No discussion of what happens when d is NOT a power of 2.**
   The text says "If d = 2^n (a power of 2)" and leaves it at that. But practical neural network layers often have d = 768, 1024, 2048, 4096. Of these, 768 is not a power of 2. Does the thesis pad to the next power of 2? Use a different encoding? This is a practical concern that a student reading the thesis would wonder about.

10. **The "Further Reading" section doesn't include a reading ORDER.**
    For a student, "where do I start?" is the key question. The list is organized by topic, but a student doesn't know which topics to prioritize. A suggested reading path (e.g., "Start with de Wolf for a quick overview, then O'Donnell Ch1-5 for the core theory, then Wang et al. for the BNN context") would be more helpful than a flat list.

## Overall impression
This is a good synthesis chapter. The worked example is valuable and the chapter-by-chapter map is a useful reference. The main gaps are: (a) the multi-layer composition is hand-waved, (b) the circular reasoning in the error bound needs clarification, and (c) the worked example could show more of the actual FWHT computation.

## Cross-chapter observations (now that I've read the whole guide)

1. **The guide achieves its main goal**: every mathematical concept in the thesis is covered, with explicit pointers. The expository chain is complete.

2. **Proof completeness varies significantly**: Ch2 proofs are fully worked out. Ch3 proofs are mostly complete. Ch4 has significant gaps (the level-k proof defers the key step). Ch5 and Ch6 proofs are reasonable. A student who wants to understand everything would need to consult O'Donnell for the Ch4 material.

3. **Examples are excellent where they exist**: AND, majority, parity, FWHT butterfly, spectral reconstruction pipeline. But some sections lack worked examples: the noise operator (what does T_ρ f look like for a specific f and ρ?), the Bonami Lemma (a concrete n=2 case), the RM code (a small example in both conventions).

4. **The variable naming issue (n = log₂ d vs n = d) is systemic.** Despite the remark in Ch6, it's easy to get confused because the same letter n means different things depending on whether you're in the "Fourier analysis" context or the "neural network" context. A notation table at the beginning of the guide would help.
