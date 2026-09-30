# collider plan

Goal: machine-checked catalog of Rule 110 glider collisions (inputs -> outputs
with exact spacetime positions/phases), queryable as JSON, every entry
re-verified by simulation. Emphasis on gadget-grade reactions.

## Steps
- [x] 1. Core library `r110lib.py`: batch (bit-sliced) evolution, ether phase
      bookkeeping, row builder from (glider, event) placements, cluster
      extraction, minimal-invariance (period vector) detection.
- [x] 2. Glider discovery: random + exhaustive small perturbations of ether;
      collect every isolated periodic object; verify each standalone;
      canonical key per glider; name them (Cook/Martinez names where the
      period vector + width match).  -> gliders.json
- [x] 3. Collision theory: distinct collisions of X,Y = |det|/14 classes
      (relative seed-event vector mod lattice <P_X, P_Y>). Verify count
      empirically for a few pairs.
- [x] 4. Pairwise catalog: all ordered pairs (X left, faster than Y), every
      class; simulate to completion; outputs typed + positioned relative to X's
      seed event.  -> collisions.json
- [x] 5. Verification script: rebuild each entry from JSON, re-simulate,
      compare outputs exactly.
- [x] 6. Gadget queries: annihilation, conversion, reflection, fan-out, clean
      crossing, switches (outcome depends on phase).
- [x] 7. (2-glider packets only) Triples / packets (A^n, E^n, streams) for promising cases.
- [ ] 8. FINDINGS.md + board summary.
- [x] 9. predict.py (any placement from the catalog), glidersim.py
      (event-driven glider-level simulator with 3-body guard), regions.py.
- [x] 10. E^n counter (INC B; DEC A from left or G from right; zero test).
- [ ] 8. FINDINGS.md: harness refuses report files from this subagent;
      findings go to the final report + board instead.
- [ ] Future: glider gun catalog (finite seeds), 3-glider packets, B/G
      packets vs E^n (synth has B-train crossing queued).
