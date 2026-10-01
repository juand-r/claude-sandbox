# gate: running log (round 2)

## 2026-09-30
- Read round2 README, BOARD, noncts/SUMMARY, round-1 board (GB stream, hard-gate
  searches).
- Catalog scan (collider/collisions.json), A vs G-speed objects: besides the known
  A + GB4#4 -> A and A + GB1#3 -> G, there is a family A + (G, GBk) -> GB(k+2)
  (k = 0..5, many placements/classes), A + (G, GB2) -> nothing (30 packet/class
  combos) and A + G#2 -> G + A (A crosses G). [catalog, i.e. sim by collider]
- (G,GB2)@(-16,29): E^n -> E^(n+1) class-free (n>=2), and at zero classes 0,1;
  A + it #4 -> nothing. So "DEC then this INC" = identity: the answer's -1
  cancels the INC. [sim, scan_counter.py]
- LEMMA (posted 23:4x) [arg]: slip(E^k) = 9 + 6(k-1) mod 14, total slip conserved
  => counter net change mod 7 = f(stream slip - leftover slip). Garbage-free
  programs are "linear" mod 7; every clean A-conversion has e(Y) = e(X) - 1 (mod 7).
  A real branch needs data-dependent garbage that LEAVES.
- Catalog: the only clean crossings with G-speed objects are A x G #2 and
  A x tight (G,G) pairs #2; right-escape of answers is therefore hard. Left
  escape: NOT in collider's catalog, but my scan finds it: at zero,
  E + (GB1,GB1)@(-1,36) #1 -> Bbar + E  (Bbar escapes left), while for n >= 2 the
  same packet is a class-free INC. = "INC unless zero" (J). [sim, scan]
- Monotonicity [arg]: ops of the form "v>=1: v+e, v=0: e0" with e0 <= e+1 are
  monotone; compositions of monotone maps are monotone; parity is not. So need
  a unit with U(0) > U(1): zero branch must shed >= 2 more negative charge
  (escaping A's) or the nonzero branch >= 2 more positive (left B's).
  Brute force over words in {I, S, J} (S = saturating DEC): no parity (as
  expected, all monotone).
- 00:00 FOUND (scan + glidersim, then CA): wrap packets. Z6 = GB3@(0,0)+GB4@(-25,46)
  is a class-free DEC for n = 2..9; at zero (class 0) E -> E^7. Mechanism: the
  GB3's zero answer A meets the trailing GB4 in class 3 and shatters it into
  6 B's (A + GB4 #3 -> B^2 + B_2_B_4_B_2_B, catalog), which fly to E: +6.
  B-charge jumps by 7, slip conserved: exactly what the lemma allows.
  Also W7 = GB3@(0,0)+GB5@(-14,40) (NOP, zero class 0 -> +7, class 1 -> NOP),
  X8 = GB5@(0,0)+GB4@(-4,56) (INC, zero class 2 -> +8).
- test_wrap.py 3 --ca: prefix I^v then Z^3, v = 0..6: final E^((v-3) mod 7 + 1),
  glidersim == automaton cell for cell [sim]. (log test_wrap_m3_ca.log)
- Mistake: first stream builder applied the zero class to every packet; after a
  slip-6 packet the class key is meaningless (relative vector not
  ether-compatible). Fixed: apply the designated class only where the
  predecessors' slip is 0 mod 14 (the only slots where zero is possible).
- J (INC unless zero, Bbar left) at zero moves E to a different class relative
  to the stream, so J^5 Z^6 (= "DEC, wrap to 1" semantically) fails with the
  naive builder (next J meets zero in class 2 -> debris). Need per-slot classes.
- Semantic search: words over {I,Z,W,X,J} up to length 6-9: no parity; but
  Zk := J^(6-k) Z^(7-k) is "DEC with wrap to k" (k=0: saturating DEC), so
  J^5 Z^6 = mod-2 down-counter (length 11, beyond the search).
- Mistake (01:0x): CHAIN only had E..E^9, so E^10 (auto-named v-4/15s7w33 by the
  library) counted as "debris" and the 4-block parity search failed spuriously.
  Fixed in common.py (_extend_chain via E^(n-1) + B, up to E^16; slips follow
  9+6(k-1) mod 14).
- fastca.py: exact moving-window Rule 110 (ether outside, margin checked every
  step). test_fastca.py: 5/5 random defects agree with engine.py on a big
  cyclic row; flipped-cell control differs. test_cacheck.py: window check ==
  full-row check on Z6 runs (v = 0, 2), and a wrong prediction is rejected.
- adaptive.py: two J^5 Z6^6 blocks, v = 0..3, all correct at glider level with
  classes [1,0,2,1,0,1,0,0,0,0,0, 0,2,1,0,2,0,0,0,0,0,0].
- 00:06 verify found INZZ fails with my builder: Z acting on value 1 sends its
  trailing GB4 into the zero E (GB4 at zero displaces E in 2/3 classes). My
  test I^v Z^m never exercised that path. Mistake: I tested only one program
  shape. Fix: assembler v2 (stream.build2): designate classes relative to the
  reference E^(val+1), val = 5*(slip/2) mod 7 forced by slip; Z at val 1 in
  class 2 (refclass.py). verify's 4 failing words now = model in exact CA;
  diff_test.py 1 25 6: 25/25 at glider level.
- J programs: zero-J's displace E; the remaining-stream slip changes the
  coset, so keys must be compared among histories at the same slot (not with
  a global reference). Greedy fails at block 3 (history conflict); now DFS
  with "histories at the same (slot, value) share the trajectory class",
  checked at non-J slots, with a GB4 after J^5 as a phase corrector.
- Mistake: "histories at the same slot and value share a trajectory class" is
  mis-specified across inputs: the prefix I^v changes the far-right ether by
  6v mod 14, so E's of different inputs live in different ether cosets and
  their keys are not comparable (dbg4.py: second key coordinates differ by
  1/21). Dropped the strict check; plain DFS with backtracking on outcomes.
- 00:4x PARITY (2 blocks) VERIFIED in exact CA: program (J^5 Z6^6)^2 with
  per-slot classes 1,0,2,1,0,1,0,0,0,0,0, 0,2,1,0,2,0,0,0,0,0,0 (adaptive.py
  greedy), inputs v = 0..3 -> 0,1,0,1, one E^k + only Bbars (left) as garbage;
  CA (fastca window) == glidersim cell for cell (verify_classes.py).
  Control: first J in class 0 instead of 1 -> v = 0 ends as Ebar, E^3, Ebar,
  A^2, A, A (exact CA + library census), v = 1 unaffected (J class-free there).
- stream.ca_only: exact CA + collider census for controls where glidersim
  raises ThreeBody.
- 01:0x fastsearch.py: incremental greedy (cached glidersim per input, one
  packet appended at a time); reproduces adaptive.py's 2-block classes in 36 s.
- Phase experiments (3 blocks, v = 0..4, greedy): (J^5 N Z^6)^3 works iff the
  N (GB4 meeting zero only in zero-started blocks) is in class 2 (classes 0, 1
  fail at block 2-3). J^4 X Z^6 works for X = L = GB1+GB1@(-4,34) and
  X = P = GB1+GB1@(-41,56), fails for K, M. Consistent with verify's
  hypothesis: J's zero displacement is an element of order 3; L and P carry
  the inverse displacement, a class-2 GB4 at zero supplies the missing one.
- 01:3x IMPORTANT self-correction: my prefix-based builders (stream.build,
  build2, adaptive.py, fastsearch.py) place the program AFTER the input prefix
  with per-slot rules that depend on the prefix's ether (slip). So the program
  text is not literally the same for different inputs: at slip != 0 slots the
  "class index" means different physical placements for different v. Results
  obtained that way are per-input compilations, not one fixed program. (Fine
  for verify's random-word tests, where each word is its own program; NOT fine
  for "a fixed program computes f(v)".)
  Fix: rafast.py. Program text placed once; input = E(0,0) + v GB5's
  (stream.build rule); program shifted in x only (same t = 0 text), so a
  class index is one physical placement for all inputs. With this:
  * J^4 L Z^6 blocks fail at block 3 (greedy), Z^9 fails at slot 8 on inputs
    0..9 (v = 1 vs v = 8 conflict: Z acting on value 1 displaces E; one slot
    cannot serve both a wrap (v=0) and a no-displacement value-1 case).
  * Key criterion: inputs v and v+7 share the prefix ether, so at equal values
    their E's must have equal class keys (coset_ok). With it, DFS finds
    (Z N)^10 (GB4 correctors) for inputs 0..9 in 35 nodes, glider level:
    classes 0,1,0,1,0,0,1,0,2,0,0,0,1,0,2,0,0,0,1,0. CA check running.
  Earlier "parity 2 blocks verified" (adaptive.py classes) is a per-input
  compilation in this sense; to be redone with rafast.
- 01:5x (Z N)^10 fixed program, exact CA, v = 0..9 -> (v-10) mod 7, 10/10
  (verify_ZN10.log). Control: corrector at slot 1 class 1 -> 0 breaks exactly
  v = 1 (debris), others fine (verify_ZN10_control.log).
- 02:1x Parity as ONE fixed program: (J^4 L Z6^6)^8, 88 packets, rafast DFS
  with coset criterion (1406 nodes), classes in parity_ra8.classes; exact CA,
  v = 0..8 -> 0,1,0,1,0,1,0,1,0, one E^k + only Bbars (5 per zero block),
  CA == glidersim (verify_parity8.log). L = GB1+GB1@(-4,34) is the J variant
  whose zero displacement cancels J^4's.
- verify's scope lesson: a stream is only guaranteed for inputs whose
  zero/one events were in the search set. Out-of-sample runs queued
  (v = 10..14 for (Z N)^10, 9..11 for parity: these never meet zero/one,
  so they test only the class-free part) + a parity control.
- 02:3x Out of sample: (Z N)^10 v = 10..14 OK; parity v = 9..11 OK (= v-8).
  Parity control (slot 4, the L, class 0 -> 1): v = 0 debris, v = 1 OK.
  Final summary posted. No processes left running.
Reflection: the two real mistakes today were (1) testing one program shape
only (verify's INZZ), and (2) believing a per-input compilation was a fixed
program. Both were caught by asking "what exactly is held fixed across
inputs?". Rule for next time: write down the invariance claim (what is the
same for every input) before searching, and make the builder enforce it.

## 2026-10-01 ~02:40 new task from lead: F-lane ABORT (messenger eats rest of block, gate removes it)
- Catalog: C1 is the only messenger with EAT reactions (11 combos; C2/C3 none).
  c1_algebra.py: displacement of the C1 per meal; class-neutral (in
  L = <(7,0),(30,-8)>) only for (-4,23)#3 [(3,16)] and (-22,39)#3 [(1,24)].
- abort_scene.py [sim, exact CA == glidersim]: C1 + a,b,b,a,a,b + gate
  (Ebar,E)@(-9,29)#3 -> one Ebar. Fixed placements (class 3 rel. original C1,
  spacing (0,168) in L). Controls: (0,14) shift -> debris; (1,-4) -> debris;
  no C1 -> packets untouched.
- Obstacles (catalog, exhaustive over its 115 Ebar-speed pairs): address's
  movers are never eaten; neutral eaters cannot be absorbed by F (only
  convert while crossing); no C1-gate crosses F cleanly -> no-abort branch
  needs a gate disposal (idea: [MAKE][GATE] with a guard C1 emitted by T).
- Note: Lambda/<P_Ebar> is Z + Z_2 (P_Ebar = 2*(15,-4)), so F-class and
  C1-class of a mover are not simply nested; their joint constraint must be
  computed, not assumed.
- Running scan_lane.py: C1 and F vs 203 uncatalogued Ebar-speed compounds.
