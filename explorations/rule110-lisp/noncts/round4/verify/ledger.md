# Verification ledger (round 4)

Status: VERIFIED / REFUTED / CANNOT REPRODUCE / PENDING / SCOPE ACCEPTED / REVIEWED.

| # | claim | by | status | check | notes |
|---|---|---|---|---|---|
| 1 | Lemma R4-L1: A, B, D vs stationary (7,0) objects have exactly one collision class (det/14 = 1) | theory 23:05 | REVIEWED, correct | board 23:08 | also tested in practice by #2's lattice shifts |
| 2 | example LN head steps: A@(0,0)+A@(-1,24) + C1 -> C2 + B_2_B_4_B_2_B; D2_7_D2#2 + C3 -> C2 + A_0_A_7_A; C1 + v-2/4s6w29 -> C1 + B; v0/7s2w48 + v-2/4s12w33 -> C2 + D1 | theory 23:05 | VERIFIED 4/4 | verify_ln1.py | my builder (rows = collider build_row), my typer, T = 700; same products at 6 lattice shifts each; cell-swap controls differ |
| 3 | E-bg (rod interior) carries right-to-left domain walls at exactly -3/5 (lab), phase jump (3,5) | objects 23:11 | VERIFIED | wall_check.py | my stepper, -60 cells / 100 steps for t = 100..600, domain phases segmented; control one domain |
| 4 | E-bg phase group Z^2/<(5,2),(0,10)> = Z/50 via h = 2t - 5s; ether lattice -> even subgroup | objects 23:11 | REVIEWED, correct | board 23:12 | |
| 5 | all 15 -3/5 wall kinds (W <= 40) destroy E^45 at the front | objects 23:11 | PARTLY re-checked (1 kind, 2 launches, both destroy) | wall_plant.py walls | 48 of 50 zero windows launch no wall |
| 6 | walls in E-bg only at -3/5, -4/15, +2/5 (P <= 30, W <= 40, SAT) | objects 23:11 | SCOPE ACCEPTED | - | ether controls reported |
| r3#28 | correction of round-3 ledger #28 | verify (self) | CORRECTED | - | -3/5 walls exist; round-3 classifier missed them |
| 7 | Lemma R4-L4: universal single-head particle TM needs clean passes in both directions; long stretches force pass cycles | theory 23:18 | REVIEWED: part 1 correct; part 2 (pure pass cycles) NOT forced (zig-zag cycles with reflections suffice) | board 23:19 | affects S1/S2 scope |
| 8 | MERGE: E^m, D1, E^n -> E^(m+n+1) in 3 of 5 classes (R1 dumped into R2) | shuttle 23:24 | VERIFIED | verify_merge.py (log verify_merge.log) | my construction; m = 1,2,3,6, n = 3..12: 120/120 clean merges, 80/80 non-merge classes not clean; class = t0 mod 5, constant over x shifts |
| 9 | E + GB4 -> E shifted +364/15, 0, +308/15 (3 classes); E^2 + GB4 -> E^2 unmoved (all classes) | delayline 23:33 | VERIFIED | verify_window.py, pairscan.py | my builder/typer; 3 placements per class asserted equal |
| 10 | an Ebar crossing a tape C displaces it by +7 (crossed Ebars count mod 8) | queue 23:30 item 4 | VERIFIED for single C (C2: 1 class, +7; C1: 2 classes) + order-8 argument checked | verify_cross.py | their 2641 crossed pairs not re-run |
| 11 | phase is not state; forced-N reader modifier (zscreen 8/119,596); next read breaks | queue 23:30 items 1-3 | PENDING (needs their Cook-machine scenes) | - | |
| 12 | DRIFT SWITCH: R2's zero (Z_L -> A) opens window R1 (E^2 -> E); later right-stream NOPs walk it (+24.27/+20.53 alternating), so the gap's drift turns on; v2 >= 1 no walk | delayline 23:33 | VERIFIED (scene c=2, v2=0, tz=20000); 18/18 scenes of the complete ds_scenes.json at 00:08 | verify_ds.py, verify_ds2.py | rebuilt row = collider's; final cells equal their result; my K = 0..10 NOP variants: 8 walks, alternation exact; control without Z_L: no walk |
| 13 | shuttle's L-table (391 B-trains x 193 walls, bounce_table_L.jsonl): kinds, wall_out, head_out canon | shuttle 23:51 | VERIFIED on a sample (1,800 rows, 450 per kind, 0 disagreements) | spot_bounce.py, rawscene.py | different gap (40 vs 24) = single-class test; scope warning: most passes leave non-lattice heads (Ebar, F, E, Bbar, G) with 2-7 classes |
| 14 | route 20: Minsky -> two-window gap machine, exact transfers x2, x3, /2, /3 under commensurate units; 79/79 | theory 23:52-23:58 | [model] REPRODUCED; REVIEW: exactness needs windows stepping over packets in flight (u > packet spacing); without skipping all tested transfers have residue-periodic offsets; finite control (modes) unplaced | review_gap2.py | scope note, not a refutation |
| 15 | shuttle's R-table (1863 A/D heads x 193 walls) | shuttle 23:51/00:10 | VERIFIED on a sample (reflect 150/150, pass 150/150, dirty 150/150); DEFECT: absorbed rows 8/150 wall_out in a wrong time phase, dx off by 0..-5 | spot_bounce.py, spot_phase.py | snapshot copy in scratchpad (table rewritten during reads) |
