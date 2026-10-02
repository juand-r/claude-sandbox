# queue (round 4): running log

Avenue (e): a queue machine with genuine finite control in Rule 110, not a
cyclic tag system. Builds on round2/queue (Cook's read cycle at glider
level, charge law, option (c) SAT).

## Plan (tick as done)
- [ ] P0 Read board, round2/queue, scholar THEORY, Cook machinery. 
- [ ] P1 Phase as state: does a rejected appendant of length L != 0 mod 6
      leave a DIFFERENT prepared leader (P_r, r = L mod 6)? What does P_r
      read, and what does its answer write? (round2: L=8 reads 1-5 ok,
      read 6 wrong: a Y written after the shifted read was READ AS N.)
- [ ] P2 If P_r is a clean reader with a different function or a clean
      displaced reader: build the state model and verify a state-dependent
      read (same symbol, same block, different appended data).
- [ ] P3 Otherwise: option (c) / skip-with-anti-symbol by SAT with moving
      windows and wider regions.
- [ ] P4 Small demo + non-CTS argument.

## Log

### 22:48-23:10 setup, P1 (phase) answered
- P1 [sim] t_prep2.py: the rejector-prepared leader P_1 after a rejected
  appendant N^L is IDENTICAL (cell-exact, spacetime-aligned on the table to
  its right) for L = 6, 8, 10, 12, 14. So L mod 6 does not change the
  prepared leader; Cook's x6 rule is about the table's position relative to
  tape/ossifiers (static geometry), not dynamic state. Phase route as
  "state in the leader" is closed in this form.
- Tools: q.py (imports round2 splice), lscene.py (exact local scenes cut
  from the full machine; control: 0 cell diffs vs full machine on a
  2000-cell window after 3000 steps; flipped cell -> diffs), reads.py
  (decoder-free multi-read check with mid-run SURGERY; read 0 shows '!'
  when the run starts mid-way: artifact, read 0 happened before t_in).

### 23:10-23:40 a forced-N reader modifier (Z) exists
- zscreen.py [sim]: Z = two Ebars written into the ether in front of the
  rejector-prepared reader P_1 (Ebar@K0+39, E@K0+68) at t_in = 31500.
  119,596 placements (Ebar_1 tile start in [-200, 0), Ebar_2 up to 150
  left). Classes (right part [K0+100, K0+800) at t_in+3000 equal to the
  standard Y-read / N-read window up to answer delays of 30j steps):
  60 normal (Y->Y, N->N), 8 FORCED-N (Y->N, N->N), 0 inverted, 0 forced Y.
  All 8 forced-N have Ebar_1 = (k=14, x=-4); all 60 normal have
  Ebar_1 = (7, -11); Ebar_2 is crossed by the symbol's C's.
- But the debris breaks later reads: t_forced1.py (full machine, surgery)
  NYYN: plain NYYNYNNN = ref; with Z: read 1 = N (forced, correct), read 2+
  '!'. Same for a NORMAL pair (t_normal1.py): read 1 Y ok, read 2 '!'.
- Mechanism [sim, cross2.py/crossn.py]: a C crossing an Ebar is displaced
  +7 cells (the Ebar's slip); two crossings +14 (2641/2641 crossed pairs
  uniform). With 2 extra crossed Ebars in front of P the read is garbage.
  [arg] class of C vs a static Ebar-frame object lives in
  Z^2/<(7,0),(30,-8)> (order 56); a +14 shift has order 4 there, so the
  number of crossed Ebars matters mod 8. Debris that leaves an extra
  crossed Ebar desynchronises every later read.
- Charge+crossing link [arg]: Ebar slip = 7 = its crossing shift, so any
  marker whose net effect leaves e extra crossers needs e = 0 mod 8;
  with slip(Z) = 0 the cheapest is a fully consumed Z (debris identical to
  the plain N read).

### 23:30-23:55 consumed markers; V-equivalence
- zlib.py [sim]: Z = one slip-0 library object (74 objects, 56,490
  placements in [K0-345, K0+37)): 175 normal, 28 forced-N, 0 inverted/
  forced-Y. Best forced-N: compound Ebar@(0,0)+Ebar@(-1,39) at k=19,
  x = -299/-243/-187/-131/-75 (period 56): the compound is CONSUMED, debris
  = the standard remnant Ebar but displaced (left diff 5-22 cells).
- t_forcedZ.py [sim] (full machine) with that Z at x=-243: reads 1 (forced
  N), 2, 3 correct; read 4 (first read of data appended AFTER the forced
  read) broken, both tapes. Reads of old tape symbols are fine, so the
  displaced remnant is crossed by C's; [hyp] it is hit by the ossifiers
  (A4 x Ebar has 6 classes, one invisible).
- [arg] A static debris object is harmless iff its placement is in the
  standard class both against tape C's (mod <(7,0),(30,-8)>, index 4) and
  against ossifier A4's (mod <(3,2),(30,-8)>, index 6): i.e. modulo
  V = <(12,8),(30,-8)> (index 12), which is exactly round 2's empirically
  found machine-symmetry lattice. vequiv.py tests debris V-equivalence
  (lab frame, a*(12,8)+k*(0,56)).
- zmix.py [sim] pairs of E-family objects (E^3+Ebar, E^3+E^3, E+E^5,
  E^2+E^4, ...; ~200k placements): 9 more forced-N (E^4 + E^2), none with
  V-equivalent debris. vfilter1.txt: of 45 forced-N, 0 V-equivalent; of
  235 normal, 3 V-equivalent: Ebar_8_Ebar at (k=5, x=-28) is consumed with
  EXACTLY the standard outcome (left diff 0), at x=-84, -140 V-shifted.
- MISTAKE: zscreen/zmix (non-tight) required non-overlapping 43-cell
  tiles, so Ebar pairs closer than ~43 cells were never tried by the pair
  screens. build2 (tiles overlap in ether margins; positive control: the
  library compound at x=-243 is rebuilt exactly as two tiles) fixes it;
  tight screens running (zmix_tight.jsonl).

### 00:00-00:20 MISTAKE found: baseline not checked per tape
- The PLAIN machine (program {YNNNNN}, Cook's default v) FAILS tape NNYY
  at read 3 (t_plainctl.py: NNYN!! vs reference NNYYYN), from t = 0 and
  from a mid-run start alike. REPORT s.3.5 warned: runs of rejections need
  a larger ossifier spacing. Every full-machine check whose run contains
  two consecutive rejections at default v is therefore confounded:
  t_forced1 / t_forcedZ (forced read 1 after read 0 = N), the gap
  controls on NNYY, the converter full checks. Their "debris breaks later
  reads" conclusions are WITHDRAWN pending re-runs with VMULT=2 (reads.py
  now takes env VMULT). Rule: run the plain baseline on every tape with
  the same v before reading anything into a failure.
- Answer converters (zconv.py, gap of D cells at K0+310 right of the
  reader, Ebar pairs): 12 placements turn the ACCEPTOR into the standard
  rejector (right part exact, j = 0) while the rejector deletes Z with an
  exactly standard outcome. Converted-Y debris {E1, E353} vs standard N
  {E1, E128}: the read itself is standard; only K's tail leftover differs
  (E353 - E128 = 225 ~ 4*56).
- Gap at K0+100 (between core and K tail) is NOT a symmetry (read 1 Y
  became N): K's tail takes part in the read/acceptor.
- MISTAKE (process, 00:19): `cd X && nohup ... & echo $! > create2.pid`
  wrote create2.pid into noncts/ (the caller's directory), exactly the
  pattern the kickoff warns about. Removed that stray file at once (it
  held only the PID 27041); PID now recorded in queue/create2.pid. Rule:
  always `echo $! > /abs/path/queue/x.pid`.
- 00:47 lead: three heavy processes at once (tail of zfull_batch + a new
  batch + a check). Rule from now: ONE heavy process; new jobs wait for
  the previous PID (until ! kill -0 PID) inside one script.

### 00:30-01:10 acceptor path, creation attempts, class-as-state idea
- [sim] Forced-N modifiers also exist in the ACCEPTOR path (zaccpair.py:
  Q added between the last moving-data Ebar and E0; 46 forced-N of
  ~11.7k); per-object debris classes (dclass.py) show none exact. One full
  run (YYNN, 2v) breaks at read 2 as predicted; batch stopped by PID.
- [sim] Joint creation search create2.py (X = Ebar pairs in a (0,112) gap
  before K, both answers, then the next read; 2v): ~8k X; 154 X are
  invisible (both paths exactly standard), none gives a state-dependent
  read; most X break the rejector's preparation of K.
- [sim] Answer converters need a gap right of the reader; a gap at K0+100
  breaks reading (K's tail takes part), at K0+239/310 it is a symmetry
  for NYYN (8/8) but NNYY was the bad 1v baseline -> undecided, dropped
  (converters cannot be created by the previous answer anyway: it never
  reaches K's tail).
- [arg] Class as state: in the acceptor path the next symbol crosses E0
  (+7 cells, displaced -52 = 4 x (6,-13)) on top of the moving data; the
  rejector path has no E0. Cook's reader reads both normally. A modified
  reader P* (prepared identically by both answers) that is not "bi-class"
  would read differently by state, with no marker to create. Screen:
  pstar.py (P's E replaced by same-slip objects, both paths).
- [sim] Class-as-state REFUTED (scoped): pstar.py replaced P's E by all 25
  slip-9 objects (89 placements) and the whole core [K0+22, K0+125) by
  all 74 slip-2 objects (5,252 placements); every non-garbage reader
  behaves IDENTICALLY in the rejector path and the acceptor path
  (positive control: the original core reproduces all four tapes, 0
  diffs). So the two paths deliver the next symbol equivalently; the
  state must be a marker. Side finds: exact "N->Y" readers (Y garbage),
  e.g. Ebar_10_E (k=2, x=23); E^8 at (14,57) is 11 cells from a clean
  forced-N reader in both paths.
- MISTAKE: selrep.py first run produced 0 rows silently: a NameError
  (tiles_of not imported) was swallowed by `except Exception: continue`.
  Exactly the silent-fallback pattern CLAUDE.md forbids. Fixed the import
  and narrowed the except to the tile-construction errors, now printed.

### 00:40-00:55 last searches and wrap-up
- combo.py: forced-N Z (132) + exact-normal M; only 2 persisting
  exact-normal M exist (the Ebar_8_Ebar family; the other ~1490 "exact
  normal" pairs annihilate each other before the symbol arrives =
  degenerate). No composed Z with V-standard debris.
- selrep.py (K's first Ebar = the 'selector' that the acceptor turns into
  E0 and the rejector eats, tile (18, K0-25) at t = 6000): replaced by
  every slip-7 library object at every placement in [K0-47, K0+22),
  6,068 placements, both paths: only the original placement keeps both
  paths standard (positive control). selector.py: 8 acceptor-shift-
  corrected copies of the selector before K break both paths.
- t_e24.py: tape C's never cross E^2/E^4 pairs intact (no zero-shift
  crossers available).
- t_cmp.py: the class bookkeeping across reads is NOT simply "count of
  crossed Ebars": in the acceptor path the next symbol crosses 24 moving-
  data Ebars + E0 and still reads normally; the initial-tape geometry
  differs between tapes. So the mod-8 statement is about EXTRA crossers
  added to a correctly built machine (what t_chain.py measured), not
  about total counts. Mechanism of the path symmetry: open.

## Final status (00:55)
Not reached: a machine-created state-dependent read. Reached: forced-N
modifiers (one exact on Y, full machine), debris and crossing laws,
path symmetry of readers, scoped negatives for markers and creation.
See the final board post and README.

## Continuation (lead 01:00): option (c) and G1 by SAT
- sat_k.py: two scenes (acceptor YYNN t=14250, rejector NYYN t=11130,
  both = 0 mod 30), free (30,-8) train K' in [K+FL, K+FR), Ebar-frame
  moving window [K-180, K+240) margin 0, horizons 450 / 390 (+30 for a
  static check; t_horizon.py: windows static from t_a+420 / t_r+360).
  Modes control / rejdiff / accdiff (difference allowed inside
  C = [K-120, K+120) only, there static).
- Solver: cadical153 control on [-30, 8) did not finish in 900 s;
  kissat404 (pysat) control on [-20, 8) (Wt 34): SAT in 104 s, finds K,
  full-machine re-simulation 0 / 0 cell diffs (POSITIVE CONTROL OK);
  cadical195 > 130 s on the same, stopped. Using kissat404.
- K's front at t = 6000: selector Ebar cells -9..-3, E23 (17 wide), E61,
  E129...; slice boundaries must have 14 ether cells: FL in {-30,-20,54},
  FR in {8, 40..46, ~114, ~152}.
- Queue (runq_sat.sh / sat_queue.txt, one process, timeouts).
