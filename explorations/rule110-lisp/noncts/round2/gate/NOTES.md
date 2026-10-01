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
