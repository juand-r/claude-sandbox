# Literature Review: Index

The full literature review is split across four documents:

1. **[Self-Modifying Computation, Reflective Towers, AIXI](papers/LITERATURE_REVIEW.md)**
   - Von Neumann, Kampis, reflective towers (Smith, Wand/Friedman, Amin/Rompf)
   - AIXI, Gödel Machines, OOPS (Hutter, Schmidhuber)
   - Kleene's recursion theorem and fixed points

2. **[Symbolic Dynamics, Tag Systems, IFS, CA](papers/LITERATURE_REVIEW_SYMBOLIC_DYNAMICS.md)**
   - Post tag systems (Post, Minsky, De Mol)
   - Symbolic dynamics (Morse/Hedlund, Lind/Marcus, Bowen)
   - Sliding block codes, Curtis-Hedlund-Lyndon
   - IFS on discrete spaces (Hutchinson, Barnsley, Martyn)
   - Substitution systems (Cobham, Allouche/Shallit)
   - CA as dynamical systems (Wolfram, Cook, Kůrka)
   - Krohn-Rhodes decomposition

3. **[LLM Self-Interaction and Formal Treatments](LIT_REVIEW.md)** (Part I, sections 1-10)
   - Self-play, debate (Irving, Arnesen)
   - Iterative refinement (Madaan, Huang, Yuan, Wu)
   - Constitutional AI (Bai)
   - Model collapse (Shumailov, Alemohammad, Dohmatob)
   - LLM fixed points and attractors (Wang, Perez, Tacheny)
   - Transformer expressivity (Chiang, Merrill, Qiu)
   - Multi-agent (Li/CAMEL, Park/Generative Agents)

4. **[Kolmogorov Complexity, Computational Mechanics, Info Theory](LIT_REVIEW.md)** (Part II, sections 11-16)
   - Algorithmic information theory (Kolmogorov, Li/Vitányi, Chaitin)
   - Brudno's theorem (orbit complexity = metric entropy)
   - Logical depth (Bennett) -- key concept for "creativity"
   - Computational mechanics (Crutchfield epsilon-machines)
   - Lempel-Ziv complexity
   - Effective complexity (Gell-Mann/Lloyd)

## Key Synthesis Points

1. **Our (f,x) -> (phi(f,x), f(x)) framework appears novel** -- no paper found formalizes
   LLM dynamics with explicit function mutation via a meta-rule phi.

2. **Creativity = logical depth** (Bennett): neither trivially simple nor random. Short
   description, long computation. In finite systems: long transients, high LZ complexity,
   high function mutation rate.

3. **Convergence to attractors is the norm** -- both theoretically (finite state spaces,
   Kleene fixed points) and empirically (LLM 2-cycles, model collapse).

4. **External input prevents degeneration** -- fresh data, constitutional principles,
   external feedback all prevent collapse to trivial attractors.

5. **Computational universality requires iteration** -- single transformer pass is TC^0,
   iterated is Turing-complete.
