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
