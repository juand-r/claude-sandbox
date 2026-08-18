# Plan

Agreed scope (2026-08-18): full Cook-style construction, Lisp front end,
Python, Neary-Woods polynomial route at the machine->cyclic-tag step.
Honesty clause: if full Lisp eval at glider level exceeds available compute,
the deliverable is the complete verified pipeline + real glider-level runs
of cyclic tag programs + measured blowup factors per layer.

## Layer 0 - Rule 110 engine
- [x] Vectorized simulator (numpy), cyclic boundary
- [x] Differential test vs naive pure-Python reference
- [x] Ether background: verify spatial period 14 / temporal period 7 empirically
- [x] Spacetime rendering (text + PNG) for debugging
- [ ] Commit

## Layer 1 - Cyclic tag -> gliders (Cook encoding)
- [x] Block catalog: Cook 2009 bit-blocks A-L extracted from arXiv EPS figures
      (A, B, C2, E-bar, ...) as ether-phase-aware patterns
- [x] Tape builder: seam-matching canvas gluing, unique placements
- [x] Encode: central region + ossifier side + appendant side -> initial row
- [ ] Decode: read emitted glider stream back to tag output
- [ ] Validate: run a real cyclic tag program on the CA, compare vs Layer 2 reference
- [ ] Commit

## Layer 2 - Cyclic tag system layer
- [x] Direct cyclic tag interpreter (reference semantics)
- [x] TS -> CTS compiler (Cook unary encoding); TM -> TS (Cocke-Minsky); Neary-Woods polynomial route still open
- [x] Differential tests: Chapman 3x+1 TS vs CTS; TM visits vs TS firings; TM -> TS -> CTS composed
- [ ] Commit

## Layer 3 - Lisp
- [ ] Mini-Lisp spec (atoms, cons/car/cdr, cond, lambda, define, recursion)
- [ ] Reference interpreter in Python
- [ ] Lisp -> machine model compilation/interpretation
- [ ] Differential tests
- [ ] Commit

## End to end
- [ ] Smallest Lisp computation pushed as deep as compute allows
- [ ] Measure blowup factors at each layer
- [ ] REPORT.md
