# leftstream: running log (round 3)

## 2026-10-01
- Read README, BOARD, round2 SUMMARY, gate README/NOTES, verify THEORY (part).
- Charge (slip mod 14, vlib widths): A 8, D1 3, D2 9, B 6, E 9, E^k 9+6(k-1).
  Slip conservation => a CLEAN INC of E^n by right-movers needs total slip
  6 mod 14; a clean DEC needs 8. All-A packets: k A's have slip 8k, so INC
  needs k = 6 (mod 7) A's. D1+D1 = 6, A+D1+D2 = 20 = 6.
  [arg] So round 1's negative (A, A^2..A^5, D1, D2 do not INC) was forced by
  charge: none of those has slip 6. The charge-allowed space (6-A trains,
  D1 pairs) was never searched. That is the first target.
- 05:2x SAT positive control (slip 8, delta -1, W 10): finds single A DECs.
- 05:3x SAT INC (slip 6, W 24, T2 220, ns 1..4 joint): SAT in all 3 classes.
- Mistake: first rebuild check showed junk: engine.pack pads rows to a
  multiple of 64 with zeros, so the wrap seam emits junk. Fix (lsl.run):
  crop T+20 cells at both ends after evolving (junk moves <= 1 cell/step).
- claim_inc.py [sim]: I_L + E^n -> E^(n+1), n = 1..12, displacement (7,-8)
  constant; other two classes debris (except shift 2 at n = 1).
- ops.py: A DEC class 1, disp (5,2) const for n = 2..8; A + E -> C3.
  Key changes: DEC -4, INC +4 (mod 42).
- Posted to board 05:40.
