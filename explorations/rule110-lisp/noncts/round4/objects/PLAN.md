# objects (round 4) plan: storage objects that escape Theorems 1-2

Avenues (b) right-to-left crossings and (d) other counter objects.

## Approach
1. [x] Tool: exact influence cone of a periodic background (SAT, two
   half-lines): leftmost cell at time T that can depend on arbitrary changes
   at x >= x0; rightmost for x <= x0. Positive control: ether (B at -1/2,
   A at +2/3 must be inside the cone). Block argument turns a finite-T
   computation into a rigorous speed bound.
2. [x] (done: E-bg is two-way; walls -3/5, +2/5; (L) holds only for glider events) Apply to the E^n interior (E-infinity background): is right-to-left
   influence through a long rod impossible for ANY signal (incl. fuel-paying
   crossings)? If the cone's left speed equals the rod speed, (L) of
   Theorem 2 becomes a theorem, and route (b) for E^n is closed outright.
3. [x] (rods = dense glider trains) Enumerate all spatially periodic Rule 110 backgrounds (ring cycles) up
   to some period; compute their cones and velocities; find which can form
   extendable domains (rods) inside ether, and which rods are two-way.
4. [x] (README) Survey table of storage objects: E^n, A^n, B^n, F-trains/pairs,
   C-ladders/stacks, Ebar/E trains, library extendables; INC/DEC from each
   side, crossings each way, interior influence direction.
5. [~] (S1, bouncer L partial, W4, launch2) For two-way candidates: SAT for crossings / two-sided INC-DEC.
6. [x] (B-lattice <= 40 launch UNSAT) Wider SAT crossing of E^n (only if step 2 does not close it).

## Status log
(see NOTES.md)

## Final state 01:25 UTC
See README main results and board FINAL SUMMARY. Stopped jobs are resumable (NOTES).
