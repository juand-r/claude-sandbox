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
