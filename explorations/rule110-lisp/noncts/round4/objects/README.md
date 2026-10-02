# round4/objects: storage objects that might escape Theorems 1-2

Agent "objects" (round 4), avenues (b) right-to-left crossings and (d) other
counter objects. Running log: NOTES.md. Plan: PLAN.md.

## Tools (all exact Rule 110; every SAT witness re-simulated)
| file | what |
|---|---|
| cone.py | exact influence cone of a periodic background (SAT): leftmost/rightmost cell at time T that changes on the other half-line can reach; block argument gives speed bounds |
| look.py, wall_id.py | view a cone witness; identify the domains on each side of a wall |
| wallsat.py | SAT for periodic walls between two phases of a background (g=0: gliders in it) |
| plant.py | plant a wall from wallsat into an E^N rod and type the outcome |
| objlib.py | scene builder (collider conventions), E^n for any n by splicing, typer (round3 verify v3, read-only) + long-rod recognition |
| scan_back.py | every library left-mover vs the back of a long rod: does anything reach the front? |
| launch2.py | SAT: can a free train launch a phase domain deep into the rod from the back? |
| backgrounds.py | enumerate spatially periodic Rule 110 backgrounds |
| s1_pass.py | theory's S1: a head that passes a stationary cell and re-emerges identical |

## Reproduce
    python3 cone.py 11111000100110 14,28,56      # ether control
    python3 cone.py 1101011100 15,30,60,90       # E-bg cone
    python3 wallsat.py 1101011100 30 40 walls_ebg.jsonl
    python3 plant.py 45 100 1000 -0.6
    python3 scan_back.py 24 1200 back_N24.jsonl all

## Object survey (working table; scopes in NOTES.md and on the board)

Columns: interior background; ops from each face; crossings; how influence
moves inside. [sim] exact CA, [sat] SAT with re-simulation, [r1-3] earlier
rounds, [thm] proved.

| object | v | interior | from the left | from the right | crossing L->R | crossing R->L | inside |
|---|---|---|---|---|---|---|---|
| E^n rod (dense E train) | -4/15 | E-bg 1101011100, lattice (5,2),(0,10); phases Z/50, h=2t-5s [thm] | I_L +1, Z_L, A -1 (1 of 3 classes) [r3]; walls launched by I_L/Z_L | B +1, Bbar +2, GB3 -1, GB5 +1 [r1-3] | none: A trains w<=30 (shuttle), SAT w<=24 (synth) | none: 2,523 library left-movers x all phases vs E^24, T=1200 (99,170 scenes) [sim]; SAT B-lattice trains w<=40 launch no phase domain (n=36, T2=400) [sat] | medium two-way: exact cone [-0.644 at T=90, +0.411] [sat]; walls -3/5 (15 kinds), +2/5 phonons (18, even h), co-moving cuts [sat, P<=30, W<=40]; every -3/5 wall destroys the rod at the front [sim]; glider-launched: front->back only |
| C-stack S9 (tight C1 stack, tile 100000110 etc.) | 0 | 000000111 (p9, period 7) | A, A^2, A^4: one tile off (+F / Ebar / E back left); D1, D2: two tiles off [sim, every phase] | B, B^2, B^3: whole stack destroyed (cascade) [sim] | not searched | not searched | walls: stationary only (P<=28, W<=30) [sat]; cone [-0.98, +0.34] [sat] |
| C-stack S11 (tile 11100011000 etc.) | 0 | 00000010011 (p11) | A: absorbed, stack shifted 2 (face change); A^2: -1 + F; A^3, A^4: -1 + Ebar; D1, D2: -1 [sim] | B, B^2, B^3, Bbar: destroyed [sim] | | | walls stationary only (P<=28, W<=30); cone [-0.77, +0.36] |
| single C cell | 0 | - | A: C3->C2->C1->F, one class [r1] | B: C1->C2->D1 out [r1] | 8-A packet crosses, eats 7 A's [r1 synth] | Ebar crosses C1 (2/4 classes), C2 (1/4); F crosses C1, C2 [catalog] | - |
| F lane (F pairs) | -1/9 | ether | C1/C2 cross (F drifts over them), displace F [r1 architect] | Ebar, B cross; Ebar pairs lock-and-key [r2 address] | yes | yes | ether, two-way |
| A^n, B^n (tight A/B trains) | 2/3, -1/2 | ether (pure phase walls) | | | | | |
| dense B / D / A trains as rods | -1/2, 1/2, 2/3 | p8 00010011; p11 00001011111; p4 0111, p6 000111, ... [sat rods_scan] | not measured | | | | |
| other E-speed backgrounds | -4/15 | p12 000001110011 (fronts, no back), p20 (backs, no front) | no rod exists in W<=24 [sat] | | | | cones two-way |
| gap (ether) | - | ether | | | | | cone [-0.571 at T=56 (B -1/2 inside), +0.679 (A 2/3)] [sat] |
