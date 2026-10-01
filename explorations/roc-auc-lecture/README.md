# ROC curves and AUC: lecture slides

A 12-slide interactive lecture for a machine learning class on the true positive rate,
the false positive rate, ROC curves and AUC. It is built on the uploaded slide template
(same styles, deck engine and presenter view).

## How to run

Open `roc_auc_lecture.html` in a browser. No server or install is needed.

- `→` / `Space`: next step; `←`: back; `↓` / `↑`: next or previous slide.
- `P`: presenter view in a second window, with speaker notes for every step.
- `F`: fullscreen; `?`: help.

The template does not load web fonts in the main window, so the slides use system fonts
unless Bricolage Grotesque, Source Sans 3 and JetBrains Mono are installed.

## Files

- `roc_auc_lecture.html`: the deck. Everything (CSS, JS, data) is in this one file.
- `check_numbers.py`: recomputes every number shown on the slides
  (`python3 check_numbers.py`, standard library only).
- `NOTES.md`: plan, slide outline and design decisions.
- `tests/`: Playwright scripts (Node, uses the pre-installed Chromium). Run from `tests/`
  with `NODE_PATH=$(npm root -g) node <script>.js`; screenshots go to `tests/screenshots/`.
  - `shoot.js [light|dark]`: renders every slide at its last step, reports JS errors.
  - `interact.js`: drives the figures and prints the numbers they show (pair count, AUC under
    transforms, matrix after a drag, precision), opens the presenter view, checks dark mode
    and phone width.
  - `build3.js`: checks the step-by-step build of slide 3.

## Slides

1. Title. 2. From scores to decisions. 3. A score and a threshold. 4. TPR and FPR. 5. Sweeping the threshold
traces the ROC curve. 6. What the shape tells you (two bell curves, adjustable overlap).
7. AUC as the area and as the fraction of correctly ordered (positive, negative) pairs.
8. What AUC does not see (ranking only, calibration, single threshold). 9. Rare positives
and precision. 10. Exercise with answers. 11. Takeaways. 12. Thanks.
