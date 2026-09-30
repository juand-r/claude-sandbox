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
