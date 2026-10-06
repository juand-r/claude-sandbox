# Nonlinear regression: lecture slides

A 16-slide interactive lecture for a machine learning class, built from lecture 14 (slides and
transcript): regression trees, kNN regression and support vector regression (SVR), linear and with
kernels. Same slide template, engine and conventions as `../svm-lecture/`.

## How to run

Open `nonlinear_regression_lecture.html` in a browser. No server or install is needed.

- `→` / `Space`: next step; `←`: back; `↓` / `↑`: next or previous slide.
- `P`: presenter view in a second window, with speaker notes for every step.
- `F`: fullscreen; `?`: help.

## Files

- `nonlinear_regression_lecture.html`: the deck. CSS, JS, data, the tree, kNN and SVR code are all in
  this one file. This is the file to edit.
- `check_numbers.py`: compares the deck's regression tree, kNN and SVR code with scikit-learn on every
  dataset in the slides, and checks the numbers quoted on the slides and in the notes.
- `make_data.py`: makes the datasets (`build/data.json`); describes each one.
- `build/`: the one-time scaffold that produced the deck: `assemble.py` takes the SVM deck's engine
  and adds `slides.html`, `code.js`, `extra.css` and `data.json`. Kept so the first version is
  reproducible; see the note at the top of `assemble.py`.
- `requirements.txt`: Python packages (use a virtualenv).
- `NOTES.md`: plan, slide outline, design decisions, and the places where the slides differ from the
  lecture transcript.
- `tests/`: Playwright scripts (Node, uses the pre-installed Chromium), run from `tests/` with
  `NODE_PATH=$(npm root -g) node <script>.js`. Screenshots go to `tests/screenshots/`.
  - `shoot.js [light|dark]`: renders every slide at its last step, reports JS errors.
  - `steps.js [slide-id ...]`: screenshots every step of every slide, to check the build-ups.
  - `interact.js`: drives the sliders and buttons, opens the presenter view, checks dark mode and
    phone width.
  - `export.js`: runs the deck's own code on all datasets and writes `tests/deck_outputs.json`.
  - `mathwrap.js`: checks at five screen sizes that no formula breaks across lines or sticks out.

## Checking the numbers

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
(cd tests && NODE_PATH=$(npm root -g) node export.js)
.venv/bin/python check_numbers.py
```
