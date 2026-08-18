# Plan

Agreed scope (2026-08-18): full Cook-style construction, Lisp front end,
Python, Neary-Woods polynomial route. Honesty clause: if full Lisp eval
at glider level exceeds available compute, the deliverable is the
complete verified pipeline + real glider-level runs of cyclic tag
programs + measured blowup factors per layer.

Status: tower complete and tested end-to-end (see REPORT.md).

## Layer 0 - Rule 110 engine
- [x] Vectorized simulator (numpy), cyclic boundary
- [x] Bit-packed uint64 engine, 39x faster, cross-checked
- [x] Ether background verified; spacetime rendering

## Layer 1 - CTS -> gliders (Cook 2009)
- [x] Block catalog extracted from the paper's figures
- [x] Seam-matching assembly; local exactness verified (1.15M cells)
- [x] Decoder (mature-symbol core matching, block-extent aliasing fix)
- [x] Dynamic validation on empty-appendant-free programs
- [ ] BLOCKED: short-leader (L) block self-destroys at its preparation
      collision -> all TS-compiled programs unrunnable physically.
      Localized (see NOTES.md); fix would unlock De Mol 3x+1 on gliders.

## Layer 2 - machines -> CTS
- [x] CTS reference interpreter
- [x] Tag-system layer; TS -> CTS (Chapman + De Mol 3x+1 verified)
- [x] TM -> TS (Cocke-Minsky, exponential; test path only)
- [x] Two-way TM -> clockwise TM -> binary clockwise TM
- [x] Neary-Woods 2-tag from clockwise binary TM (stage tables)
- [x] Capstone: full tower on a 3-state TM, exact at every level

## Layer 3 - Lisp
- [x] Mini-Lisp spec + reference interpreter
- [x] Lisp -> SKI compiler; SKI string engine (spec) + graph engine
- [x] SKI Turing machine (255 states): Lisp runs on a TM
      ((car (quote (a b))) -> a, 5.9e8 steps)

## Reporting
- [x] REPORT.md with measured blowup table and defect analysis
