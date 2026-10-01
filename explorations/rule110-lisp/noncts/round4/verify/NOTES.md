# verify round 4 notes (running log)

## 22:49 start: read board/README/SUMMARY/ledgers. Board only has kickoff.
- 22:51 hrun.py (HashLife wrapper) + test_hrun.py (6 scenes x 5 times, T<=2500) + test_hrun_long.py (T=30000): equal to engine cell for cell; controls (T-1, flipped cell) differ. Posted on board.
  Note: rejection sampling (try/except ValueError on vlib.build overlap) in the random-scene generator only; not a fallback for real scenes.
- 23:02 cone_brute.py: E-bg influence edge moves left at 3/5 (w=10, T<=200, e.g. zeros window): a pure cone bound cannot exclude crossings. Posted for objects.
- 23:08 clib.py (collider objects -> my vlib library, period re-found and compared) ; verify_ln1.py: theory's 4 LN examples 4/4, single class confirmed by 6 shifts each; controls differ. Ledger #1-2. Mistake on the way: control scene with a swapped cell was not on the ether lattice (snap assert) -> valid() moves it to the nearest valid x (collider build_row as oracle).
- 23:12 wall_check.py (walls at -3/5, jump (3,5) = h 31), wall_plant.py (E^45, 2/50 zero windows launch walls, both destroy). MISTAKE (round-3, mine as verify): r3 ledger #28 'only +2/5 walls' wrong about the medium; corrected on board. My 23:02 guess 'probably ether eating E-bg' was also wrong: it is an E-bg domain wall.
  Also: my typer knows E^n only to n = 15; for longer rods use rod_info() (span + (15,-4) periodicity).
