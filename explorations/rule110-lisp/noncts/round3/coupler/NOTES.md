# coupler: running log (round 3)

Task (T2): couple counter R1 (E^n at -4/15, right G-speed stream) and R2
(to its left, driven by a left stream) both ways, in the exact automaton.

## 2026-10-01
- Read round3 README/BOARD, round2 SUMMARY, gate README/NOTES, verify THEORY.
- cl.py: thin toolkit importing round-2 gate/collider read-only (bytecode
  writing disabled so nothing is written outside this directory).
- [sim] J at zero reproduced: E(0,0) + J@(-4,454) -> E(13,40) + Bbar(9,1576)
  (glidersim == exact CA product list).
- Catalog facts relevant to coupling [catalog = sim by collider]:
  * E^n + Bbar, 3 classes. n>=4: #0 -> E^(n-1) + A^2 A^2 A,
    #1 -> E^(n+2) + A, #2 -> E^(n-3) + A A A. n=1: #1 -> E^3 + A;
    n=3: #1 -> E^5 + A; n=2: every class gives garbage (C3/F/B...).
  * Every E^n + Bbar class emits right-moving A's: they travel to R1
    (nothing else lies between the counters). So an R1 -> R2 signal
    always echoes back to R1.
  * A + E^2 -> E in ALL three classes (class-free DEC from the left).
    A + E^n for other n: DEC only in one class.
