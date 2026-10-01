# Plan (round 3, leftstream)
1. [x] Tool module (lsl.py: collider library, placement, exact run, typing, export).
2. [x] DEC from the left re-checked: A in 1 class, disp (5,2); A + E -> C3.
3. [x] INC from the left: SAT (slip 6 forced by charge) -> I_L, n = 1..23.
4. [x] Zero test keeping the counter: Z_L (E -> E + A right), n = 1..23.
       Wrap (0 -> 6) from the left: UNSAT W 24/36 (not needed per theory).
5. [x] Rigid stream by bookkeeping (lstream.py), 270/270 random runs,
       class controls fail; verified independently by verify.
6. [x] Theory's escapes, my share (all scoped negatives):
       reflection Y = Bbar at R1's front; crossing front->back (A-trains,
       conversion allowed); crossing back->front (B-, Bbar-trains);
       wall converter (SAT, free B) + library scan (partial).
7. [ ] Not done: widths > 24 for crossings; fused caps for the converter;
       G-family back crossings (coupler's library scan covered library G's).
