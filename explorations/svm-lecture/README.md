# Support vector machines: lecture slides

A 16-slide interactive lecture for a machine learning class: hyperplanes and margins, the
hard-margin support vector classifier (SVC) and its derivation, the soft-margin SVC, kernels,
and general properties of SVMs. Two classes only. It uses the same slide template and conventions
as `../roc-auc-lecture/`.

## How to run

Open `svm_lecture.html` in a browser. No server or install is needed.

- `→` / `Space`: next step; `←`: back; `↓` / `↑`: next or previous slide.
- `P`: presenter view in a second window, with speaker notes for every step.
- `F`: fullscreen; `?`: help.

## Files

- `svm_lecture.html`: the deck. CSS, JS, data and the SVM solver are all in this one file.
- `check_numbers.py`: compares the deck's solver with scikit-learn on every dataset in the
  slides and checks every number quoted on them.
- `requirements.txt`: Python packages for `check_numbers.py` (use a virtualenv).
- `NOTES.md`: plan, slide outline and design decisions.
- `tests/`: Playwright scripts (Node, uses the pre-installed Chromium), run from `tests/` with
  `NODE_PATH=$(npm root -g) node <script>.js`. Screenshots go to `tests/screenshots/`.
  - `shoot.js [light|dark]`: renders every slide at its last step, reports JS errors.
  - `interact.js`: screenshots every slide at step 0, drives the figures (drag, C slider,
    kernels, 3D rotation), opens the presenter view, checks dark mode and phone width.
  - `export.js`: runs the deck's solver on all datasets and writes `tests/solver_outputs.json`.

## Checking the numbers

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
(cd tests && NODE_PATH=$(npm root -g) node export.js)
.venv/bin/python check_numbers.py
```

## Slides

1. Title. 2. Which line? 3. A line is w·x + b = 0. 4. Distance to the hyperplane. 5. The margin.
6. The hard-margin SVC. 7. Only the support vectors matter (drag points). 8. When no line
separates (slack). 9. The role of C. 10. No line will do (lift to 3D). 11. The kernel trick.
12. General properties. 13. Exercise. 14. Takeaways. 15. Bonus: slack is hinge loss. 16. Thanks.
