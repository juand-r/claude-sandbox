- CLOCK MISTAKE: my board post headed "06:31" was a guess; date -u then
  was about 06:05. NOTES times "06:2x/06:4x" above are also guesses. From
  now on I take every time from date -u.
- R1-face SAT alone (run_r1feas.log, stopped early): with Y free in the
  (12,-6) family the solver returns a plain B: an A-family train X (slip
  8, 21/25 cells) + E^4 -> B + E^2 in classes 0 and 2 [sat + exact CA,
  ident_sat.py]. Useless for a shuttle (B is absorbed at R2's back, one
  class, no reflection) but a candidate "R1 -= 2, R2 += 1" signal if R2
  could emit X (slip 8, like Z_L's A).
- Library shuttle scan (scan_reflect.py step 1, scan_reflect2.py step 2,
  exact; jsonl files): all 186 library gliders of velocity -1/2 vs R2 =
  E^4, every class: 74 clean reflections (one E^j + right-movers only;
  X in {A, A^2, A^3, A^2 A^2 A, A_8_A A, A^2 A^2, A^2 A, D1, F_7_F A}).
  Each X (as emitted) vs R1 = E^3..E^8 at 15 seed times: a left-mover
  return exists ONLY at R1 = E^7 (X = A^2 A^2 -> B^2 + E) and R1 = E^8
  (X = A^2 A^2 A -> B^2 + E): n-specific "reset to zero" reactions, not
  shuttle legs. No B-family library shuttle exists in this scope.
