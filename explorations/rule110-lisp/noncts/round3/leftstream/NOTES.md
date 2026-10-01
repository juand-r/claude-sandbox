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
- 05:4x SAT zero test (slip 8, W 24, T2 250, mode A: n = 2,3 DEC and
  n = 1 -> E | A): SAT in all 3 classes. Mode wrap (n = 1 -> E^7): UNSAT
  W 24 T2 300 (all 3 classes). Wrap W 36 T2 320 running (python PID 4089;
  pid file written by `echo $!` vanished - recorded by hand; $! was the
  bash wrapper 4088).
- check_rec.py: Z (sat_zero #1): DEC n = 2..9, at n = 1: E + A (A right);
  displacement (9,0) in BOTH cases -> no class divergence at zero.
- lpk.py (packets I, D, Z), lstream.py (rigid stream by bookkeeping:
  packet i = reference scene translated to the virtual front, + m P_E),
  rand_test.py: 30 random programs x v = 0..8 -> 270/270 match model.
  Mistake: first run had 2 "mismatches" = E^17 beyond my CHAIN (named
  only up to E^16); extended to E^24 (E^31+ fails to settle in
  collide_pair, so the chain stops there).
  Mistake avoided: run_program's default t0 depends on v; rand_test and
  lstream main fix t0 from vmax, so the stream text is the same for all v.
- Controls (lstream.py PROG VS i:j shifts packet i by j*(1,-4)): 5/5
  perturbations give mismatches (5..9 of 9 inputs).
- 06:1x Packets vs stationary C's (single class each, A-speed vs (7,0)):
  I: C1->C2, C2->E+A, C3->E;  D: C1->F, C2->C1, C3->C2;  Z: C1->F,
  C2->C1, C3->B+Bbar+F.  So D at zero (E->C3) is undone by I (C3->E).
  lstream runs: DI, DIZ, DII, DIIZ at v = 0 all match "value floor 0";
  the rebuilt E differs from the nonzero branch by (15,38), key 0 (same
  class; vector in M). [arg] For any gap between D and I the rebuilt E is
  in the same class: shifting I_L by m P_E is equivalent (mod C3's (7,0)
  and P_A) to translating the C3+I_L scene by (21m,0); nonzero front moves
  m P_E; difference 2m P_A has key 0.
- Wrap (0 -> 6) from the left: [arg] needs +6 front units at zero; the
  only front-INC known costs a 24-cell slip-6 train each, so a wrap packet
  likely needs > 100 cells; SAT UNSAT at W 24 (3 classes) and W 36
  (classes 0,1; class 2 running). I do not expect it within SAT reach.
- Coupling idea for theory: R2's Z answer A (right-going) and R1's J
  answer Bbar (left-going) annihilate if they meet in A+Bbar class #0
  (catalog: nothing). Both counters zero -> answers cancel; one zero ->
  answer reaches the other counter. An AND-like event, to be checked.
- 05:5x launched run_zl.sh (PID 6149): SAT Z2, zero answer = exact Z_L train, W 32,40,48, T2 360 -> sat_zl.log
- 06:0x stopped run_zl.sh (6149) and child 6152 (W32 unfinished): theory says a bare A answer suffices; priority now = reflection SAT at the inner face (theory 05:49 (i)).
- 06:1x Shuttle SAT (theory 05:49 (i)), sat_shuttle.py: free left-mover Y
  and free (3,2) X, jointly Y + E^m(back) -> E^(m+k) | X and
  X + E^n(front) -> Y | E^(n-k). Controls: R1 scene finds A^4+E^7 ->
  B^2+E (catalog) at W 16; R2 scene finds Bbar + E^3 -> E^5 + A.
  MISTAKE: R2 control with ms = 3,4 jointly was UNSAT (W 24 and 32): E^m
  from en.py is built by B's, so its BACK moves with m and the Y class
  label rotates with m (verify's caveat). Single m: SAT in all 3 kY.
  Rule: joint-n constraints are only valid at the face that B-building
  leaves fixed (the front). Sweep run_shuttle.sh launched (bash PID in
  run_shuttle.pid): B-trains W 20, then Bbar-trains W 24; X W 20; k 2, 1;
  all sY; m = 3, n = 4; T2 300.
- stopped run_shuttle.sh (7962, child 7998) after sY=0 (k=2, B-trains): coupler takes the joint B-family SAT; I take R1-side Bbar reflection (X free (3,2), Y = Bbar / Bbar-family), as coupler asked.
- sat_reflect.py (R1 side only, Y fixed library left-mover). MISTAKE:
  the R1-scene split point used Y.W (40 for a Fixed item) -> controls
  UNSAT; changed to mid = undisturbed front - 8, which needs T2 large
  enough for Y to clear the front (control A^4 + E^7 -> B^2 + E: SAT at
  T2 450 in all 3 kX, UNSAT at 300). run_reflect.sh launched (Y = Bbar,
  k 2,1,3, W 24,32, ns 3,4, T2 450).
- Reflection Y = Bbar (sat_reflect): W 24, k = 2,1,3, ns 3,4, T2 450, all kX: UNSAT. Stopped W 32 (PID 9812): pointless, since Bbar at R2's back emits only A (catalog), and A is ruled out at R1 (coupler). Next: crossing E^n with A-speed trains beyond width 24 (synth row 9 scope: A <= 24) = theory's open problem 2.
- run_cross.sh launched (PID in run_cross.pid): crossing E^n (n = 2,3 jointly), conv mode (any (3,2) output train of the same slip), W 24,32,40, T2 350, all slips x 3 classes. Control: n = 1, slip 8 finds Z_L-like E | A in all classes.
- Packet spacing: 10 random programs x v = 0..5: gap 120, 90, 75 steps all match; gap 60: 36/60 mismatch; 45: packets overlap. So >= 75 steps between arrivals (scope: these programs).
- 06:3x Theory (06:14): one crossing direction is not enough; asked for
  LEFT-mover crossings from the back too. Killed run_cross.sh parent
  (W 32/40 for A-trains dropped for now); its child 10621 finishes W 24.
  run_crossL.sh (PID in run_crossL.pid) then runs sat_crossL.py:
  B-trains W 24 joint n 2,3; Bbar-trains W 24 n 3, classes 0,1,2; B W 32.
  Control status for sat_crossL: no known reaction of the exact target
  form exists (catalog has no E^n + left-mover -> left-mover + E^k);
  its exit geometry equals sat_shuttle's R1 scene (control passed) and
  its entry geometry sat_shuttle's R2 scene (control passed).
- C-ladder at zero [sim, lstream run_program, t0 800]: DDII: v=0 -> E^2 + A
  (value 1 and one A answer), v=1 -> 1 (via C3), v>=2 -> v. DDIIZ, DDIIIZZ,
  DDIII: later packets work in every branch, so the rebuilt E is in the
  same class as the nonzero bookkeeping (as for DI). The C-ladder does
  not switch the front class (mode) at zero in these cases.
