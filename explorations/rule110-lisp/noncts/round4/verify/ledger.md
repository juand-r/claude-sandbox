# Verification ledger (round 4)

Status: VERIFIED / REFUTED / CANNOT REPRODUCE / PENDING / SCOPE ACCEPTED / REVIEWED.

| # | claim | by | status | check | notes |
|---|---|---|---|---|---|
| 1 | Lemma R4-L1: A, B, D vs stationary (7,0) objects have exactly one collision class (det/14 = 1) | theory 23:05 | REVIEWED, correct | board 23:08 | also tested in practice by #2's lattice shifts |
| 2 | example LN head steps: A@(0,0)+A@(-1,24) + C1 -> C2 + B_2_B_4_B_2_B; D2_7_D2#2 + C3 -> C2 + A_0_A_7_A; C1 + v-2/4s6w29 -> C1 + B; v0/7s2w48 + v-2/4s12w33 -> C2 + D1 | theory 23:05 | VERIFIED 4/4 | verify_ln1.py | my builder (rows = collider build_row), my typer, T = 700; same products at 6 lattice shifts each; cell-swap controls differ |
