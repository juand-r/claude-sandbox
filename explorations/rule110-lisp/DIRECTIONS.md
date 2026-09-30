# Directions for v0.2: faster and more direct

Status: proposal, written at the v0.1.0 release; numbers corrected in
v0.1.1. Nothing here is implemented yet. The request was "more clever/faster/more efficient ways
of implementing this ... it should be possible to build an interpreter on
Rule 110 more directly". This document says where the cost actually is,
then ranks the ways to cut it by expected gain and risk.

## 1. Where the cost is

The capstone program (a 3-state two-way TM, 6 steps) costs about 3.6e20
generations at the bottom of the tower. The layers multiply, but one
relation dominates. Write |Phi| for the tag-system alphabet (8,586 here)
and R for the total length of all tag rules (16,554, about 2|Phi|).

- The unary TS -> CTS encoding needs 2|Phi| CTS reads per tag step.
- In Cook's construction reads are gated by ossification: each
  ossifier (four A^4) converts one moving-data character into one tape
  character, and ossifiers are about 30v generations apart. A read
  costs about 30v generations (measured, REPORT.md 3.3), with
  v ~ 80 x (total CTS appendant length) = 80 |Phi| R.
- Generations per tag step ~ 2|Phi| x 30 x 80 |Phi| R, i.e.
  ~9,600 |Phi|^3.

For the capstone: about 6e15 generations per tag step, times 61,188
tag steps = 3.7e20.

So the bottom of the tower is **cubic in the tag alphabet**. Every layer
above only matters through |Phi| and the number of tag steps.

## 2. Options, ranked

### 2.1 Demand-timed ossifiers (cubic -> quadratic)

Observation (glider census and decoder-free reads, v0.1.1): reads are
gated by ossifications. Each ossifier converts one moving-data character
into one tape character; that
character travels into the static Ebar stream until it meets the next
unread leader. Cook sizes v for the worst case (the paper: "a
conservatively large rough estimate of twice the total vertical height
of all the table data"), so every read pays for a traversal of the whole
table.

The only hard constraint on ossifier timing is that unossified moving
data must exist when an ossifier arrives (otherwise the A^4 strikes tape
data, the halting reaction). Because we build the initial condition for
a known computation, we can simulate the CTS first and give the left
side an aperiodic schedule: ossifier k placed to arrive when character k
is available. A read then costs about one appendant's traversal instead
of a whole table's.

- Expected gain: a read then costs about one appendant's traversal
  (3.75 generations per cell of table), so a tag step costs one table
  cycle, ~3,000 |Phi|^2 instead of ~9,600 |Phi|^3: a factor of about
  3.2 |Phi|. For the capstone about 27,000x (to ~1.4e16). For De Mol's
  small CTS about 17x (~104k -> ~6k generations per read).
- Measured caveat (v0.1.1): uniformly shrinking v does not work. For
  `{YYYYNN}` v = 523-528 read correctly, v <= 262 fails at read 3 or 4.
  The likely constraint (hypothesis, not yet measured): the next
  character must not arrive while the previous read's sweep is still
  running. If so, a demand schedule has a floor near one appendant
  traversal plus one sweep, and it must be non-uniform.
- Risk: moderate. Needs the alignment rules between consecutive A^4s
  (the paper's "up 5" condition) to hold for arbitrary gaps; the
  existing runs with v = 790, 1572, 3423 suggest any v works, but that
  must be checked with the glider census, not assumed. Depends on
  closing the dynamic-verification gap first (REPORT.md section 3.3).
- Cost: an encoder option for a per-gap v list, a scheduler that
  simulates the CTS, and census-based verification.

### 2.2 Shrink the tag alphabet (the cube's base)

Measured: binarization turns 12 symbolic clockwise states into 130
binary states, of which the capstone run enters 45; Neary-Woods then
multiplies each state by 66 tag symbols. Options, cheapest first:

1. Leaner binarization (fewer buffered-bit states): up to ~3x on |Phi|,
   ~27x overall under the cubic law, ~9x under the quadratic one.
   (The capstone run enters 45 of its 130 binary states.)
2. Write the SKI reducer directly as a small binary clockwise machine (a
   queue machine), skipping the two-way -> clockwise conversion and its
   binarization. The SKI reducer is naturally a pass-based string
   rewriter, which is what a clockwise machine is. This is the only
   realistic path for the Lisp machine itself: converted mechanically,
   the 256-state SKI machine becomes a 10,897-state clockwise machine
   whose binarization does not finish (v0.1.0 measurement).
3. Specialize the Neary-Woods stage alphabet to the letters a given
   machine actually uses per stage.

Risk: low for (1) and (3); moderate for (2) (new machine to verify, but
the SKI spec and differential tests exist).

### 2.3 HashLife for one-dimensional Rule 110

The automaton-level patterns are extremely regular: ether, a periodic
left side, and an Ebar stream that is static in its own frame. A 1-D
HashLife (memoized quadtree-in-time, as in Gosper's algorithm) skips
2^k generations at a time over repeated structure.

- Expected gain: unknown until measured; potentially many orders of
  magnitude on the ether and repeated table data, little on novel
  collision traffic.
- Risk: moderate; correctness is easy to check bit-for-bit against the
  packed engine on short runs.
- Combines with 2.1 and 2.2.

### 2.4 Genuinely more direct constructions (research)

- Native CTS programs: design interpreters as cyclic tag systems
  directly, avoiding the unary tag encoding altogether. Hard: a CTS has
  no finite control beyond its phase.
- New glider-level machinery: search the Rule 110 collision catalog for
  gadgets (counters, logic) and build a machine that is not a CTS at all.
  Cook's construction is the only known complete one; this is an open
  research problem, not an engineering task.

## 3. Also pending from v0.1.0

- The short-leader (L block) defect. It blocks every program with empty
  appendants, i.e. everything compiled from a tag system. Fixing it is a
  prerequisite for running compiled programs on gliders at all, and the
  glider census is the right tool to diagnose it.

## 4. Suggested order

0. Close the dynamic-verification gap: account for every character per
   ossifier (REPORT.md section 3.3), turn it into an automated check.
1. L-block defect (prerequisite for any compiled program on gliders).
2. Demand-timed ossifiers (largest expected gain, directly testable).
3. Leaner binarization / direct clockwise SKI machine.
4. HashLife, measured on the results of 1-3.
