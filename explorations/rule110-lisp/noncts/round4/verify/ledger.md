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
