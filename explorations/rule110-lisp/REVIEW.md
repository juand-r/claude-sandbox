# Code review at takeover (2026-09-30)

Scope: every module, test, experiment script and document in this
directory, reviewed against the repository guidelines (CLAUDE.md) and
against the claims in REPORT.md. Findings are grouped by severity. Each
has a disposition; the "Status" column is updated as work proceeds.

## A. Correctness bugs

| id | finding | evidence | disposition | status |
|---|---|---|---|---|
| A1 | Compiled `atom?` returns `()` for nil; the reference returns `t`. The compiler tests `tag == atom`; nil has its own tag. | `(atom? (quote ()))`: ref `t`, compiled `()` | fix compiler: `atom?` = "not a cons" (McCarthy: NIL is an atom) | done |
| A2 | `eq?` on conses disagrees: the reference uses Python structural `==`, the compiler treats all conses as unequal. | `(eq? (quote (a)) (quote (a)))`: ref `t`, compiled `()` | define `eq?` as McCarthy's `eq` (meaningful on atoms; conses compare unequal); change the reference, document, test | done |
| A3 | Neither A1 nor A2 was caught because no test exercises nil in `atom?` or lists in `eq?`. | test inspection | add edge-case tests to the differential suite | done |

## B. Overclaims and model errors in REPORT.md / NOTES.md

| id | finding | disposition | status |
|---|---|---|---|
| B1 | "One CTS read per left period (~30v generations)" is geometrically impossible. Table data (Ebar speed -4/15) streams past the stationary tape data (C2, speed 0) at a fixed rate set by the right-side width, independent of the ossifiers. For De Mol that is 12 reads per ~71k generations, not 1 per ~104k. The event the decoder saw once per left period is *ossification* of in-flight moving data (each A^4 converts one Ebar and is consumed, per the paper's figSketchesEFGH caption). | remove the claim; measure the real cadences with a glider-level tool (C1) | |
| B2 | The bottom row of the blowup table (3.6e20 generations) is built on B1. Recomputed from geometry: generations = (tag steps) x (right-period width) x 15/4, about 1.3e16 for the capstone program. Still infeasible, but the stated number was ~4 orders too high. | recompute from measured widths and state it as an estimate with its formula | |
| B3 | "Cyclic tag programs without empty appendants run correctly on the actual CA for hundreds of thousands of generations" is not supported. No decoded tape was ever matched against the reference beyond the first few reads; the all-Y grower produced N reads, explained by an untested "maturation aliasing" hypothesis. What is established: local exactness for 45 generations, and qualitative liveness (moving data still present). | restate as what was measured; build a decoder that reads stationary tape data (C1) and test dynamic correctness for real | |
| B4 | The L-block experiment table uses "healthy/dead" = "decoder still finds moving-data patterns". The correlation with empty appendants is real observation; "localized to the acceptor-prepares-short-leader collision" rests on the flawed cadence model. | keep the observation, drop the localization claim until re-examined with C1 | |

## C. Missing capability that the claims need

| id | finding | disposition | status |
|---|---|---|---|
| C1 | There is no glider-level view of the CA. Every dynamic statement above came from substring matching of moving-data block rows. | build a glider census from lattice invariance: the ether is invariant under the vectors (7,0) and (3,2) (time, space); C gliders under (7,0) only, A gliders under (3,2) only, Ebars under (30,-8) only. Classify defect cells by which shifts leave them invariant; read tape data as stationary C2 clusters | |

## D. Efficiency

| id | finding | disposition | status |
|---|---|---|---|
| D1 | SKI Turing machine: every S-redex copies the term to a fresh region on the right, but rescans and every counter increment/decrement walk back to `#` at the far left, crossing all abandoned blank regions. Cost grows with the number of S-reductions so far, not with the term size. Measured: 79% of the 457,640,797 steps for the `(atom? (quote a))` tag probe read a blank cell; tape extent 37,880 for a 473-char term. | measure; keep the counter adjacent to the live term | measured |
| D2 | Neary-Woods rules are generated for every (letter, stage, state) combination whether reachable or not; the unary TS->CTS encoding then costs |Phi| per symbol and ~|Phi|^2 in appendant content. | prune to symbols reachable from the initial tape; re-measure the blowup table | |
| D3 | TM interpreters are pure-Python loops (~3M steps/s). | defer to extension phase | |

## E. Code quality (CLAUDE.md: DRY, no dead code, no junk in git)

| id | finding | disposition | status |
|---|---|---|---|
| E1 | 15 `__pycache__/*.pyc` files and 5 `*.out` files are tracked despite `.gitignore` (the earlier `git rm --cached` ran from the wrong directory). | untrack | done |
| E2 | Eleven `run_*.py` scripts each re-implement the same ~20 lines: ether-rotation lookup, right-edge trim to an ether cut, phase-matched padding, co-moving windows. | one helper module; scripts to `experiments/`; superseded diagnostics to `trash/` | |
| E3 | Three tag-system runners (`tag.ts_run` on char strings, `tm.ts_run_list` on lists, `nw.tag_run` deque/2-deletion). | one runner in `tag.py` | |
| E4 | `consumed.py` is unused (its method found one event and was abandoned). | trash | done |
| E5 | Dead code: unused locals in `lisp_to_ski.decode_value`, unused `PRIMS`, `Compiler.lam`; `import sys` in `ski_graph`; unused `_ETHER` in `decoder`; unused `TM` import and unused `t` parameter in `cw`; unreachable aperiodic branch in `encoder._attach`; a garbage `print` in `run_canonical.py`. | remove | |
| E6 | Wrong or garbled docstrings: `tag.py` module doc (halting sentence), `ski.parse_spine` (claims to return a tuple), `ski.reduce_once` (stream of consciousness), `cw.binarize` (claims 3-tuple, returns 4), `engine.ETHER` comment (claims a drift test that does not exist). | fix | |
| E7 | Magic numbers: decoder thresholds (60, 245, rows 35..65), encoder `_BASE_LO`, `_CHECK`. | name and explain | |
| E8 | The 3-state test TM is copy-pasted into four test files. | shared test helper | |
| E9 | `CWTM` (the clockwise machine model) lives in `nw.py` although `cw.py` produces it. | move to `cw.py` | |

## F. Things that are good and stay as they are

- The block extraction is exact and reproducible: re-running
  `tools/extract_blocks.py` on a fresh download of arXiv:0906.3248
  regenerates `data/blocks.json` bit for bit.
- The layered design with a reference interpreter per layer and
  differential tests at every arrow is sound.
- The SKI string engine as the executable spec, with the graph engine
  fuzzed against it, is the right arrangement.
