# collider plan

Goal: machine-checked catalog of Rule 110 glider collisions (inputs -> outputs
with exact spacetime positions/phases), queryable as JSON, every entry
re-verified by simulation. Emphasis on gadget-grade reactions.

## Steps
- [ ] 1. Core library `r110lib.py`: batch (bit-sliced) evolution, ether phase
      bookkeeping, row builder from (glider, event) placements, cluster
      extraction, minimal-invariance (period vector) detection.
- [ ] 2. Glider discovery: random + exhaustive small perturbations of ether;
      collect every isolated periodic object; verify each standalone;
      canonical key per glider; name them (Cook/Martinez names where the
      period vector + width match).  -> gliders.json
- [ ] 3. Collision theory: distinct collisions of X,Y = |det|/14 classes
      (relative seed-event vector mod lattice <P_X, P_Y>). Verify count
      empirically for a few pairs.
- [ ] 4. Pairwise catalog: all ordered pairs (X left, faster than Y), every
      class; simulate to completion; outputs typed + positioned relative to X's
      seed event.  -> collisions.json
- [ ] 5. Verification script: rebuild each entry from JSON, re-simulate,
      compare outputs exactly.
- [ ] 6. Gadget queries: annihilation, conversion, reflection, fan-out, clean
      crossing, switches (outcome depends on phase).
- [ ] 7. Triples / packets (A^n, E^n, streams) for promising cases.
- [ ] 8. FINDINGS.md + board summary.
