# verify round 4 notes (running log)

## 22:49 start: read board/README/SUMMARY/ledgers. Board only has kickoff.
- 22:51 hrun.py (HashLife wrapper) + test_hrun.py (6 scenes x 5 times, T<=2500) + test_hrun_long.py (T=30000): equal to engine cell for cell; controls (T-1, flipped cell) differ. Posted on board.
  Note: rejection sampling (try/except ValueError on vlib.build overlap) in the random-scene generator only; not a fallback for real scenes.
- 23:02 cone_brute.py: E-bg influence edge moves left at 3/5 (w=10, T<=200, e.g. zeros window): a pure cone bound cannot exclude crossings. Posted for objects.
- 23:08 clib.py (collider objects -> my vlib library, period re-found and compared) ; verify_ln1.py: theory's 4 LN examples 4/4, single class confirmed by 6 shifts each; controls differ. Ledger #1-2. Mistake on the way: control scene with a swapped cell was not on the ether lattice (snap assert) -> valid() moves it to the nearest valid x (collider build_row as oracle).
- 23:12 wall_check.py (walls at -3/5, jump (3,5) = h 31), wall_plant.py (E^45, 2/50 zero windows launch walls, both destroy). MISTAKE (round-3, mine as verify): r3 ledger #28 'only +2/5 walls' wrong about the medium; corrected on board. My 23:02 guess 'probably ether eating E-bg' was also wrong: it is an E-bg domain wall.
  Also: my typer knows E^n only to n = 15; for longer rods use rod_info() (span + (15,-4) periodicity).
- 23:19 reviewed theory R4-L4 (pass cycles not forced; zig-zag counterexample).
- 23:33 rodval.py (value of any-length rod) + verify_merge.py: MERGE verified 120/120. MISTAKE on the way: first rodval window did not cover the light cone to the right, so escaping A's were missed and a few non-merge classes looked like clean 'rod m' outcomes; widened to the full cone, now 80/80 non-merge classes are debris, matching shuttle's dump2 output.
- 23:41 pairscan.py (class-resolved pair scans, asserted per class), verify_window.py (delayline E/E^2 + GB4 exact), verify_cross.py (C x Ebar). ds_scenes.json truncated; wait.
- 23:46 verified delayline drift switch (verify_ds*.py); clib.register_auto for collider auto-names of IL/ZL.
- 23:59 rawscene.py (raw bits scenes) + spot_bounce.py: L-table sample 1,800/1,800 after fixing three of MY classification errors: (1) object span must be first-diff-from-left-ether .. last-diff-from-right-ether (not vlib defect bounds); (2) compound stationary walls (C1+C2 6 cells apart) appear as two defects; merge stationary defects < 20 apart; (3) B and Bbar have the same speed but different periods: compare speeds as fractions. Also velocity test by family periods (fixed 420-step shift fails for F (36), G (42)).
- 00:02 reviewed route 20 (review_gap2.py): skipping + finite control.
- 00:07 verify_ds.py on all 18 scenes: equal. Mistake: seeds are in program order, not left-to-right -> sort by start column. Also: a spot_bounce R-side 'mismatch' hunt was confused by shuttle's table being rewritten during my reads (different line contents for the same (head_i, wall_j)); hashlife was suspected and cleared (engine vs hrun equal, pad 400 vs 2080).
- 00:17 R-table checks; bouncer_direct.py started (PID 24285), chunk 40000; controls ok.
- 00:18 verify_lstop.py: delayline reverse switch verified. Mistake: first intercept formula had the sign of 4tE/15 wrong (shift looked class-dependent within a class); fixed.
- 00:22 verify_fullstop.py 41/41.
- 00:23 verify_cstack.py (objects C-stacks).
- 00:24 quality watch post: queue 3, shuttle 2 heavy processes.
- 00:34 reproduced bouncer.py; posted direct-bouncer half result.
- 00:35 reviewed route 22 (charge conservation kills U2 as stated).
- 00:39 verify_xconv.py (objects bubble wall).
- 00:39 reviewed route 23 (Bbar emits A's into the right stream).
- 00:51 W4 work (w4_scan/w4_repeat/w4_cands); bouncer_direct done 0/84700 alive. MISTAKE: first w4_repeat used T = 2D (B blocks close on the rod at 7/30, need 30D/7): all multi-block runs read 'None'; fixed.
- 00:53 W4 analysis posted (probe, charge mod 7, target).
- 00:53 W4 composition argument posted.
