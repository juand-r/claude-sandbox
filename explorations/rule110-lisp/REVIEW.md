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
| B1 | ~~"One CTS read per left period" is geometrically impossible.~~ My argument (reads at a fixed table rate past a fixed tape) was wrong, but so was the claim. **Partly resolved by glider-level measurement (C1):** reads are gated by ossification, not by the table. At the start of a run each A^4 converts one moving-data character into one C glider (the first ossifier makes four C gliders and the front advances from character 0 to character 4), and the first three arrivals match that accounting (9 of 9 symbols); from the fourth arrival on, 4 of 6 arrivals do not. Characters per ossifier, hence the read cadence (7.5v to 30v generations), remain open. | REPORT.md 3.2-3.3; lesson in NOTES.md | partly resolved |
| B2 | The blowup table's bottom row assumed ~30v generations per read. The measured cadence is between 7.5v and 30v (B1), so the capstone estimate is 9e19 to 3.6e20 generations. Still infeasible by 14-15 orders of magnitude. | state the range in REPORT.md | done |
| B3 | "Cyclic tag programs without empty appendants run correctly on the actual CA for hundreds of thousands of generations" is not supported. No decoded tape was ever matched against the reference beyond the first few reads; the all-Y grower produced N reads, explained by an untested "maturation aliasing" hypothesis. What is established: local exactness for 45 generations, and qualitative liveness (moving data still present). | restate as what was measured; build a decoder that reads stationary tape data (C1) and test dynamic correctness for real | done: REPORT.md 3.3 restates the claim from measurements; reading the stationary tape data directly was not achieved (C glider spacings are blurred by constant Ebar crossings), so the check reads the moving data each ossifier meets instead |
| B4 | The L-block experiment table uses "healthy/dead" = "decoder still finds moving-data patterns". The correlation with empty appendants is real observation; "localized to the acceptor-prepares-short-leader collision" rests on the flawed cadence model. | keep the observation, drop the localization claim until re-examined with C1 | done: REPORT.md 3.4 keeps the observation, withdraws the localization |

## C. Missing capability that the claims need

| id | finding | disposition | status |
|---|---|---|---|
| C1 | There is no glider-level view of the CA. Every dynamic statement above came from substring matching of moving-data block rows. | build a glider census from lattice invariance: the ether is invariant under the vectors (7,0) and (3,2) (time, space); C gliders under (7,0) only, A gliders under (3,2) only, Ebars under (30,-8) only. Classify defect cells by which shifts leave them invariant; read tape data as stationary C2 clusters | done: census.py with tests; used for REPORT.md 3.2-3.3 |

## D. Efficiency

| id | finding | disposition | status |
|---|---|---|---|
| D1 | SKI Turing machine: every S-redex copies the term to a fresh region on the right, but rescans and every counter increment/decrement walked back to `#` at the far left, across all abandoned regions. Measured: 79% of the steps of one probe read a blank cell. | Fixed: the pebble counter now lives immediately left of '$' (abandoned regions become counter space) and rescans stop at '$'. Same results on 1,497 random terms. Steps, old -> new: `(quote a)` probe 180,937 -> 44,669 (4.1x); `(quote (a b))` 13.9M -> 3.4M (4.1x); `(cdr (quote (a)))` 100.1M -> 13.7M (7.3x); `(atom? (quote a))` 2.60e9 -> 3.77e8 (6.9x). The gain grows with the number of S-reductions. | done |
| D2 | Neary-Woods rules are generated for every (letter, stage, state) combination; the unary TS->CTS encoding costs |Phi| per symbol and ~|Phi|^2 in appendant content. | Hypothesis refuted by measurement: syntactic reachability pruning removes 0 of 8,582 symbols (stage-6 rules reach every state). The inflation is upstream: binarization turns 12 symbolic clockwise states into 130 binary states, times 66 NW symbols each; the capstone run enters only 45 states and uses 2,719 symbols. Lever: a leaner binarization (extension phase). | closed, negative |
| D3 | TM interpreters are pure-Python loops (~3M steps/s). | defer to extension phase | deferred to the extension phase (DIRECTIONS.md) |

## E. Code quality (CLAUDE.md: DRY, no dead code, no junk in git)

| id | finding | disposition | status |
|---|---|---|---|
| E1 | 15 `__pycache__/*.pyc` files and 5 `*.out` files are tracked despite `.gitignore` (the earlier `git rm --cached` ran from the wrong directory). | untrack | done |
| E2 | Eleven `run_*.py` scripts each re-implement the same ~20 lines: ether-rotation lookup, right-edge trim to an ether cut, phase-matched padding, co-moving windows. | one helper module; scripts to `experiments/`; superseded diagnostics to `trash/` | done |
| E3 | Three tag-system runners (`tag.ts_run` on char strings, `tm.ts_run_list` on lists, `nw.tag_run` deque/2-deletion). | one runner in `tag.py` | done |
| E4 | `consumed.py` is unused (its method found one event and was abandoned). | trash | done |
| E5 | Dead code: unused locals in `lisp_to_ski.decode_value`, unused `PRIMS`, `Compiler.lam`; `import sys` in `ski_graph`; unused `_ETHER` in `decoder`; unused `TM` import and unused `t` parameter in `cw`; unreachable aperiodic branch in `encoder._attach`; a garbage `print` in `run_canonical.py`. | remove | done |
| E6 | Wrong or garbled docstrings: `tag.py` module doc (halting sentence), `ski.parse_spine` (claims to return a tuple), `ski.reduce_once` (stream of consciousness), `cw.binarize` (claims 3-tuple, returns 4), `engine.ETHER` comment (claims a drift test that does not exist). | fix | done |
| E7 | Magic numbers: decoder thresholds (60, 245, rows 35..65), encoder `_BASE_LO`, `_CHECK`. | name and explain | done |
| E8 | The 3-state test TM is copy-pasted into four test files. | shared test helper | done |
| E9 | `CWTM` (the clockwise machine model) lives in `nw.py` although `cw.py` produces it. | move to `cw.py` | done |

## F. Things that are good and stay as they are

- The block extraction is exact and reproducible: re-running
  `tools/extract_blocks.py` on a fresh download of arXiv:0906.3248
  regenerates `data/blocks.json` bit for bit.
- The layered design with a reference interpreter per layer and
  differential tests at every arrow is sound.
- The SKI string engine as the executable spec, with the graph engine
  fuzzed against it, is the right arrangement.
