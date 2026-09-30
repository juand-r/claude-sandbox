# gate: plan (round 2)

Goal: M1 = one verified data-dependent branch (zero vs nonzero changes the later
program, machine stays well-formed); M2 = a small programmable machine end to end.

Setting (round 1, verified): counter E^n (value v = n-1) moving at -4/15; rigid
G-speed (-1/3) stream: GB3 = DEC, GB4 = NOP, GB5 = INC. At zero GB3 -> E + A;
the answer A moves right (+2/3) into the stream. A vs a G-speed object has 9 classes.

Steps
- [ ] 1. Catalog scan: every G-speed object P with a clean A + P outcome
       (absorbed -> G-speed products / nothing; or A passes). (catalog data)
- [ ] 2. For those P (and their products Q): action on E^n, n = 1..5, all 3
       classes, by direct CA simulation. Want P and Q both clean instructions
       with different counter effects ("conditional substitution").
- [ ] 3. Machine model built from what exists; argue expressiveness.
- [ ] 4. M1: build one stream, simulate for v = 0 and v >= 1 in the full CA,
       with negative controls.
- [ ] 5. M2: loop / parity program end to end.
