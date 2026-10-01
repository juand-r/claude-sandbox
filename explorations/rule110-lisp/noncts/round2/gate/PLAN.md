# gate: plan (round 2)

Goal: M1 = one verified data-dependent branch (zero vs nonzero changes the later
program, machine stays well-formed); M2 = a small programmable machine end to end.

Setting (round 1, verified): counter E^n (value v = n-1) moving at -4/15; rigid
G-speed (-1/3) stream: GB3 = DEC, GB4 = NOP, GB5 = INC. At zero GB3 -> E + A;
the answer A moves right (+2/3) into the stream. A vs a G-speed object has 9 classes.

Steps
- [x] 1. Catalog scan: G-speed objects with clean A outcomes.
- [x] 2. Their action on E^n (scan_counter.py, 565 packets, n = 1..4).
       Finding: all clean conversions conserve e mod 7 -> slip lemma.
- [x] 3. Machine model: one counter with INC, DEC-with-wrap-k (k <= 6),
       built from Z6 (wrap packet) and J (left garbage). Ceiling: ultimately
       periodic predicates (verify's theorem) -- parity, v mod k.
- [x] 4. M1: Z6 = DEC whose zero answer shatters the trailing NOP into 6 B's;
       CA-verified, composable (assembler v2, random words).
- [x] 5. M2: fixed streams (Z6 N)^10 -> (v-10) mod 7 (v = 0..14) and (J^4 L Z6^6)^8 -> v mod 2 (v = 0..8), exact CA (rafast.py, verify_ra.py). Earlier per-input versions superseded; was: mod-7 loop (CA); parity with 2 blocks (CA,
       v = 0..3); 3+ blocks: per-slot class search (DFS) running.
- [x] 6. Final writeup on the board (FINAL SUMMARY post).

Did not work / notes
- Naive builder (class rel. E(0,0) everywhere): wrong after slip-6 packets.
- Builder v1 (class only at slip-0 slots): misses Z on value 1 (verify INZZ).
- J at zero displaces E; needs per-slot classes; greedy fails at block 3.
