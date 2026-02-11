# Research: Pi Algorithms & Physical Limits of Computation

## Part 1: Pi Computation Algorithms

### 1.1 Spigot Algorithms (Compute nth digit without all previous digits)

#### BBP Formula (Hexadecimal Only)

The Bailey-Borwein-Plouffe formula (1995) computes the nth **hexadecimal** digit of pi without computing all preceding digits. It uses only standard-precision arithmetic.

- **Complexity**: O(n log n) per digit
- **Memory**: O(log n)
- **Limitation**: Only works in base 16 (hexadecimal). Cannot directly produce decimal digits.

#### Decimal Digit Extraction: Bellard/Gourdon

Fabrice Bellard (1997) found an algorithm to compute the nth **decimal** digit of pi:

- **Complexity**: O(n^2) per digit (Bellard), improved to O(n^2 log log n / log^2 n) by Gourdon (2003)
- **Memory**: O(log n) for Bellard, O(log^2 n) for Gourdon
- **Practical reach**: Can compute digits at position ~4,000,000 in hours
- **Key advantage**: Uses only small integer arithmetic (64-bit integers suffice for reachable n)
- **Key limitation**: Still O(n^2) per digit -- much slower than computing all digits sequentially with Chudnovsky

#### Plouffe's 2022 Decimal Formula

Simon Plouffe published a new formula in January 2022 (arXiv:2201.12601) that directly extracts the nth decimal digit of pi using Bernoulli/Euler numbers.

- **Convergence**: Polynomial (not geometric), but high degree
- **Practical reach**: A few million digits with modern hardware
- **Limitation**: Requires precomputing large Bernoulli numbers. Not practical for very large n.

#### Rabinowitz-Wagon Spigot Algorithm (Sequential Decimal)

This produces decimal digits sequentially (not random access), one at a time.

- **Complexity**: O(n^2) for n digits total (O(n) work per digit, n digits)
- **Memory**: O(n) -- array of ~10n/3 small integers
- **Advantage**: Only integer arithmetic. Simple to implement.
- **Disadvantage**: Must commit to number of digits in advance. Bounded algorithm.
- **Improvement**: Gibbons (2004) made an unbounded version that generates digits indefinitely given enough memory.

**Assessment for robustness**: Spigot algorithms are excellent for fault tolerance. If the machine loses state, it can restart from a known digit position. The BBP formula (hex) lets you verify any previously computed digit. The Bellard/Gourdon algorithm (decimal) lets you spot-check decimal digits at specific positions, but at O(n^2) cost per check. For a robust system, a hybrid approach -- sequential computation plus periodic checkpointing via digit extraction -- is attractive.

---

### 1.2 Simple Iterative Algorithms

#### Leibniz Series: pi/4 = 1 - 1/3 + 1/5 - 1/7 + ...

- **Convergence**: Extremely slow. ~500,000 terms for 5 correct decimal digits.
- **Operations per digit**: Roughly 10^n operations per nth correct digit (each digit requires ~10x more terms)
- **Advantage**: Trivially simple. Could be implemented mechanically.
- **Verdict**: Impractical for any serious digit count. Good for teaching, terrible for computation.

#### Nilakantha Series: pi = 3 + 4/(2*3*4) - 4/(4*5*6) + 4/(6*7*8) - ...

- **Convergence**: Much faster than Leibniz. ~28 iterations for 3 correct digits (vs 999 for Leibniz).
- **Roughly 35x fewer iterations** than Leibniz for comparable accuracy.
- **Still linearly convergent** -- each term adds a fixed (small) amount of accuracy.
- **Advantage**: Simple arithmetic. Easy to implement.
- **Verdict**: Better than Leibniz but still very slow for serious computation.

#### Machin-Like Formulas: pi/4 = 4*arctan(1/5) - arctan(1/239)

- **Convergence**: ~6 terms for 10 correct digits (vs 5 billion for raw arctan(1))
- **Complexity**: O(n^2) for n digits. Each of ~O(n) terms requires O(n) work (short division).
- **Operations per digit**: O(n) operations per additional digit
- **Practical speed**: 1,000,000 digits in ~40 minutes (historical benchmark)
- **Advantage**: Uses only integer arithmetic (short division). Historically used for records up to 1.24 trillion digits.
- **Verdict**: Good balance of simplicity and speed. The most robust "classical" algorithm. Used for pi records before Chudnovsky took over.

**Assessment for robustness**: Machin-like formulas are excellent for mechanical/simple computation. They require only short division (dividing a long number by a small number), which is mechanically simple. The O(n^2) scaling means they become impractical for very large n, but for a machine optimizing robustness over speed, this is acceptable.

---

### 1.3 Chudnovsky Algorithm

- **Convergence**: ~14.18 decimal digits per term (by far the fastest known series)
- **Overall complexity**: O(n (log n)^3) using binary splitting
- **Practical performance**: ~1 trillion digits in ~32 hours on a modern PC
- **Current record**: 314 trillion digits (December 2025, using y-cruncher on a Dell PowerEdge server, took ~4.5 months)
- **Memory**: Significant. 100 trillion digits requires ~470 TiB of swap space.
- **Requires**: High-precision arithmetic (arbitrary-precision integers/floats), FFT-based multiplication

**Assessment for robustness**: The Chudnovsky algorithm is the fastest by far, but it requires:
1. Arbitrary-precision arithmetic libraries
2. FFT-based multiplication (complex)
3. Enormous memory for large computations
4. Sophisticated binary splitting implementation

This makes it fragile. A bit flip in a high-precision multiplication could corrupt everything. It is the opposite of robust. For a perpetual computer, this is a poor choice unless you have excellent error correction.

---

### 1.4 Iterative (AGM-type) Algorithms

#### Brent-Salamin (Arithmetic-Geometric Mean)

- **Convergence**: Quadratic -- doubles correct digits each iteration. ~25 iterations for 10 million digits.
- **Complexity**: O(n (log n)^2) -- theoretically faster than Chudnovsky
- **In practice**: Slower than Chudnovsky due to requiring full-precision square roots and divisions at each step
- **Advantage**: Very few iterations needed

#### Borwein Quartic Algorithm
- **Convergence**: Quartic -- quadruples digits each iteration. 20 iterations for over a trillion digits.
- **Same practical issues as Brent-Salamin**: requires full-precision arithmetic

**Assessment**: These are theoretically elegant but practically worse than Chudnovsky. Same fragility issues.

---

### 1.5 Key Question: Best Algorithm for Robustness

**Recommendation: Hybrid approach with Machin-like formula as primary**

For a system optimizing robustness over speed:

1. **Primary computation**: Machin-like formula (or equivalent arctan-based series)
   - Simple integer arithmetic only
   - Can be implemented mechanically or with very simple electronics
   - O(n^2) scaling is acceptable when you have billions of years
   - Checkpointable: save the running partial sums periodically

2. **Verification/recovery**: BBP formula (hexadecimal)
   - Can verify any computed digit independently
   - If state is lost, you can determine exactly where you were by checking digit values
   - Even though it produces hex digits, you can use it to verify decimal digits by converting

3. **Alternative primary**: Gibbons' unbounded spigot algorithm
   - Produces decimal digits one at a time, indefinitely
   - Only integer arithmetic
   - Memory grows as O(n) with digits computed
   - Checkpointable: the array state IS the checkpoint

**The critical insight about state loss**: If memory corrupts, a spigot algorithm's internal state is ruined and you must restart from scratch (or the last checkpoint). But with the BBP formula, you can always verify any hex digit at position n in O(n log n) time without needing any prior state. This lets you determine which digits are valid after a corruption event.

**For a system meant to run for 5 billion years**, the dominant concern is not speed but recoverability. Computing 10^20 digits slowly but reliably is better than computing 10^30 digits and losing them all to a single corruption event.

---

## Part 2: Fundamental Physical Limits on Computation

### 2.1 Landauer's Principle

**Statement**: Any irreversible bit operation (erasure) dissipates at minimum kT ln 2 of energy as heat.

**Values**:
- k = 1.380649 x 10^-23 J/K (Boltzmann constant)
- At T = 300K (room temperature): **kT ln 2 = 2.87 x 10^-21 J per bit erasure**
- At T = 3K (cosmic microwave background): **kT ln 2 = 2.87 x 10^-23 J per bit erasure**

**Experimental verification**: In 2016, researchers measured bit erasure on nanomagnetic bits at 300K and found dissipation of ~4.2 x 10^-21 J -- only 44% above the Landauer minimum. The principle is real and experimentally confirmed.

**Current computers vs the limit**: Modern computers use about **1 billion times** more energy per operation than the Landauer limit. There is enormous room for improvement.

#### Computation budget at 1 watt for 5 billion years:

- Duration: 5 x 10^9 years = 1.577 x 10^17 seconds
- Total energy at 1W: **1.577 x 10^17 J**
- At 300K Landauer limit: 1.577 x 10^17 / 2.87 x 10^-21 = **5.5 x 10^37 irreversible bit operations**
- At 3K (CMB temperature): 1.577 x 10^17 / 2.87 x 10^-23 = **5.5 x 10^39 irreversible bit operations**

#### Computation budget at 1 milliwatt for 5 billion years:

- Total energy at 1mW: 1.577 x 10^14 J
- At 300K: **5.5 x 10^34 bit operations**
- At 3K: **5.5 x 10^36 bit operations**

### 2.2 Bremermann's Limit

**Statement**: Maximum computational speed of a self-contained system = c^2/h per unit mass.

**Value**: **~1.36 x 10^50 bits per second per kilogram**

Derived from mass-energy equivalence (E = mc^2) combined with the Heisenberg uncertainty principle (minimum energy to distinguish states = h/t).

**Correction for general relativity**: If the computer is too massive and compact, it collapses into a black hole. Accounting for this gives an absolute maximum bitrate independent of mass: **(c^5 / Gh)^1/2 ~ 10^43 bits per second** (related to the Planck time ~10^-43 s).

**Practical context**: The world's fastest supercomputer (El Capitan, Nov 2025) achieves ~2 x 10^18 FLOPS, which is ~10^32 times below the Bremermann limit for its mass.

**Earth-mass computer at Bremermann's limit**: ~10^75 operations per second.

### 2.3 Margolus-Levitin Theorem

**Statement**: Maximum computation rate = **6 x 10^33 operations per second per joule** of energy.

This is a quantum speed limit. It says a quantum system with energy E needs at least h/(4E) time to transition between orthogonal states.

**At 1 watt**: Maximum 6 x 10^33 ops/sec. Over 5 billion years: 6 x 10^33 x 1.577 x 10^17 = **~10^51 total operations**.

This is a much more generous bound than Landauer (which constrains only irreversible operations). The Margolus-Levitin theorem constrains ALL operations, but gives a higher rate because it bounds speed (not energy dissipation).

### 2.4 Reversible Computing

**Concept**: Landauer's principle only applies to **irreversible** operations. If every computation step is logically reversible (bijective mapping of states), no information is erased and no minimum energy is dissipated.

**In principle**: A reversible computer could compute indefinitely with zero energy dissipation beyond what's needed to maintain the physical system.

**Engineering challenges (as of 2025)**:
1. **Traditional logic gates are irreversible**: AND, OR gates destroy information. Must use Toffoli, Fredkin, or similar reversible gates.
2. **Garbage data**: Reversible computation generates "history" data that must be managed.
3. **CMOS implementation**: Adiabatic operation requires slow voltage ramps, trading speed for energy. LC resonators needed, but CMOS LC resonators have low quality factors.
4. **Error correction**: Traditional error correction erases data, violating reversibility. Need novel approaches.
5. **Overhead**: The extra circuitry and control needed may consume more energy than is saved.

**Commercial status**: Vaire Computing (startup, 2024) is building reversible CMOS chips. First chip (reversible adder) was sent for fabrication in early 2025. AI inference chip planned for 2027. Full 4000x energy improvement is "10-15 years out."

**For our purposes**: Reversible computing is theoretically possible but not practically relevant for a robust long-duration system. The engineering complexity is the opposite of what we want. However, the *principle* matters: it tells us that the Landauer limit is not a hard wall -- it applies only to irreversible operations.

### 2.5 Maximum Digits of Pi: Energy-Limited Estimate

The key question: given a power budget and the Landauer limit, how many digits of pi can be computed in 5 billion years?

#### Framework

1. **Power budget**: P watts for t = 1.577 x 10^17 seconds
2. **Total energy**: E = P * t joules
3. **Bit operations available** (Landauer, 300K): N_ops = E / (kT ln 2) = E / (2.87 x 10^-21)
4. **Algorithm**: determines how many bit operations per digit of pi

#### Algorithm Cost Per Digit

For n total digits computed:

| Algorithm | Total bit ops for n digits | Bit ops per additional digit (marginal) |
|---|---|---|
| Leibniz series | ~10^n (exponential -- impractical) | Exponential |
| Machin-like | O(n^2) * O(log n) bits per operation = O(n^2 log n) | O(n log n) |
| Chudnovsky + binary splitting | O(n (log n)^3 * M(n)) where M(n) is multiplication cost | Much lower than Machin |
| Spigot (Rabinowitz-Wagon) | O(n^2) elementary ops on small integers | O(n) |
| BBP (hex digits) | O(n log n) per digit | O(n log n) per isolated digit |

#### Concrete Estimates

**Scenario A: 1 watt, 300K, 5 billion years, Machin-like formula**

- Available bit ops: ~5.5 x 10^37
- Machin-like needs ~O(n^2) multi-precision operations for n digits. Each multi-precision operation on an n-digit number requires O(n) bit operations (for short division). Total: O(n^3) bit operations for n digits.
- Solving n^3 = 5.5 x 10^37 gives **n ~ 3.8 x 10^12** (~3.8 trillion digits)

**Scenario B: 1 watt, 300K, 5 billion years, Chudnovsky algorithm**

- Available bit ops: ~5.5 x 10^37
- Chudnovsky with binary splitting and FFT multiplication: O(n (log n)^3) multi-precision operations, each involving O(n log n) bit operations (FFT multiply). Total: ~O(n^2 (log n)^4) bit operations.
- Solving n^2 (log n)^4 ~ 5.5 x 10^37: For n ~ 10^18, n^2 ~ 10^36, (log n)^4 ~ (41)^4 ~ 2.8 x 10^6. Product ~ 2.8 x 10^42. Too high.
- For n ~ 10^16: n^2 ~ 10^32, (log n)^4 ~ (37)^4 ~ 1.9 x 10^6. Product ~ 1.9 x 10^38. Close.
- **n ~ 5 x 10^15** (roughly 5 quadrillion digits, or 5000 trillion)

**Scenario C: 1 milliwatt, 300K, 5 billion years, Machin-like formula**

- Available bit ops: ~5.5 x 10^34
- n^3 = 5.5 x 10^34 gives **n ~ 3.8 x 10^11** (~380 billion digits)

**Scenario D: 1 milliwatt, 300K, 5 billion years, Chudnovsky**

- Available bit ops: ~5.5 x 10^34
- n ~ 10^15: n^2 ~ 10^30, (log n)^4 ~ (34.5)^4 ~ 1.4 x 10^6. Product ~ 1.4 x 10^36. Still a bit high.
- **n ~ 10^14 to 10^15** (100 trillion to 1 quadrillion digits)

**Scenario E: What about the Margolus-Levitin bound instead?**

If we could use reversible computing and are limited by speed rather than energy dissipation:
- 1 watt gives 6 x 10^33 ops/sec max (Margolus-Levitin)
- Over 5 billion years: ~10^51 total operations
- With Chudnovsky: n^2 (log n)^4 ~ 10^51 gives **n ~ 10^24** (a septillion digits)
- This is an absolute upper bound for 1 watt of sustained power, regardless of technology.

#### Summary Table

| Scenario | Power | Algorithm | Max Digits |
|---|---|---|---|
| Conservative | 1 mW | Machin-like | ~4 x 10^11 (400 billion) |
| Conservative | 1 mW | Chudnovsky | ~10^14 (100 trillion) |
| Moderate | 1 W | Machin-like | ~4 x 10^12 (4 trillion) |
| Moderate | 1 W | Chudnovsky | ~5 x 10^15 (5 quadrillion) |
| Aggressive (reversible) | 1 W | Chudnovsky | ~10^24 (theoretical max) |

Note: These estimates assume operating at the Landauer limit -- about 10^9 times more efficient than current computers. They are theoretical maximums, not engineering targets. Real machines would be many orders of magnitude less efficient, but we have 5 billion years of engineering progress to close the gap.

**For context**: The current world record is 314 trillion digits (3.14 x 10^14). Our "moderate / Chudnovsky" estimate of ~5 x 10^15 digits is only about 16x the current record -- achievable with 1 watt at the Landauer limit over 5 billion years. This suggests that the Landauer limit is not the binding constraint. The real constraints are engineering: building a machine that lasts 5 billion years and operates anywhere near the theoretical efficiency.

---

## Key Takeaways

1. **For robustness, use Machin-like formulas or spigot algorithms.** They use simple integer arithmetic, are checkpointable, and can be verified with BBP. Chudnovsky is faster but fragile.

2. **The Landauer limit allows 10^34 to 10^39 bit operations** with milliwatt-to-watt power over 5 billion years at room temperature. This translates to 10^11 to 10^15 digits of pi with classical algorithms.

3. **Reversible computing could push this to ~10^24 digits** (Margolus-Levitin bound), but practical reversible computers are decades away from being useful and add enormous complexity.

4. **The real bottleneck is not physics but engineering**: making a machine that survives 5 billion years. The Landauer limit is generous enough that even a very inefficient machine (10^6x above the limit) running on 1 watt could still compute trillions of digits.

5. **Spigot algorithms have a unique advantage for recovery**: if the machine crashes and loses all state, the BBP formula can verify any previously stored hex digit in O(n log n) time. This enables a "checkpoint and verify" architecture that no other approach offers.

---

## Sources

- [Bailey-Borwein-Plouffe formula (Wikipedia)](https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula)
- [BBP Algorithm for Pi - David H. Bailey](https://www.davidhbailey.com/dhbpapers/bbp-alg.pdf)
- [Bellard's nth decimal digit of pi in O(n^2)](https://bellard.org/pi/pi_n2/pi_n2.html)
- [Gourdon: Computation of the n-th decimal digit of pi with low memory](http://numbers.computation.free.fr/Constants/Algorithms/nthdecimaldigit.pdf)
- [Plouffe 2022: Formula for nth digit of pi (arXiv:2201.12601)](https://arxiv.org/abs/2201.12601)
- [Rabinowitz & Wagon: A Spigot Algorithm for the Digits of Pi](https://www.cs.williams.edu/~heeringa/classes/cs135/s15/readings/spigot.pdf)
- [Gibbons: Unbounded Spigot Algorithms for the Digits of Pi](https://www.cs.ox.ac.uk/people/jeremy.gibbons/publications/spigot.pdf)
- [Chudnovsky algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Chudnovsky_algorithm)
- [Leibniz formula for pi (Wikipedia)](https://en.wikipedia.org/wiki/Leibniz_formula_for_%CF%80)
- [Machin-like formula (Wikipedia)](https://en.wikipedia.org/wiki/Machin-like_formula)
- [Pi computation with Machin formulas - Craig Wood](https://www.craig-wood.com/nick/articles/pi-machin/)
- [Computing the Digits of Pi - Carl Offner (UMass)](https://www.cs.umb.edu/~offner/files/pi.pdf)
- [Landauer's principle (Wikipedia)](https://en.wikipedia.org/wiki/Landauer%27s_principle)
- [Experimental test of Landauer's principle - Science Advances](https://www.science.org/doi/10.1126/sciadv.1501492)
- [Bremermann's limit (Wikipedia)](https://en.wikipedia.org/wiki/Bremermann%27s_limit)
- [Bremermann's Limit and cGh-physics (arXiv)](https://arxiv.org/pdf/0910.3424)
- [Margolus-Levitin theorem (Wikipedia)](https://en.wikipedia.org/wiki/Quantum_speed_limit)
- [Margolus & Levitin: The maximum speed of dynamical evolution](https://arxiv.org/abs/quant-ph/9710043)
- [Reversible Computing Escapes the Lab in 2025 - IEEE Spectrum](https://spectrum.ieee.org/reversible-computing)
- [StorageReview: 314 Trillion Digits of Pi](https://www.storagereview.com/review/storagereview-sets-new-pi-record-314-trillion-digits-on-a-dell-poweredge-r7725)
- [Fundamental energy cost of finite-time parallelizable computing (Nature Communications)](https://www.nature.com/articles/s41467-023-36020-2)
- [Limits of computation (Wikipedia)](https://en.wikipedia.org/wiki/Limits_of_computation)
