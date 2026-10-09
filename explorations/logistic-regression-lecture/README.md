# Logistic regression: lecture slides

A 12-slide interactive lecture for a machine learning class, meant to follow the nonlinear regression
deck in the same class and lead into neural networks the following week. It opens with loss functions (what earlier methods minimize; why not the training error). Logistic regression is
presented as the linear SVM's score with log loss in place of hinge loss; the sigmoid turns the score
into a probability; one neuron is a logistic regression. Binary classification only. How the weights
are found (gradient descent) is left for the next lecture. Same template and engine as
`../svm-lecture/`.

## How to run

Open `logistic_regression_lecture.html` in a browser. No server or install is needed.

- `→` / `Space`: next step; `←`: back; `↓` / `↑`: next or previous slide.
- `P`: presenter view in a second window, with speaker notes for every step.
- `F`: fullscreen; `?`: help.

## Files

- `logistic_regression_lecture.html`: the deck (CSS, JS, data and the fitting code in one file). It is
  built from `build/`; edit the files there and rebuild (see below).
- `check_numbers.py`: compares the deck's logistic regression (Newton's method) and SVM fits with
  scikit-learn, and checks the numbers on the slides and in the notes.
- `build/`: the sources of the deck (`assemble.py` + `slides.html`, `code.js`, `extra.css`). Rebuild
  with `python3 build/assemble.py logistic_regression_lecture.html`. Formulas in `slides.html` are
  LaTeX, `\( … \)` inline or `\[ … \]` display; `build/tex.js` typesets them with KaTeX (version
  pinned in `build/package.json`) and embeds its fonts, so the deck needs no network. Run
  `npm install` in `build/` once first. Figure labels use the same fonts (`mtxt()` in `code.js`).
- `requirements.txt`: Python packages (use a virtualenv).
- `notes/`: student notes that go through the lecture step by step, with the 0–1 loss in detail
  (`logistic_regression_notes.tex`, compiled to `.pdf` with `latexmk -pdf`). `notes/check_notes.py`
  computes every number the notes quote.
- `NOTES.md`: plan, slide outline and decisions.
- `tests/`: Playwright scripts, run from `tests/` with `NODE_PATH=$(npm root -g) node <script>.js`:
  `shoot.js [light|dark]` (every slide at its last step), `steps.js [slide-id ...]` (every step),
  `interact.js` (slider, presenter view, dark mode, phone width), `export.js` (writes
  `tests/deck_outputs.json` for the check), `mathwrap.js` (formula wrapping at five screen sizes).

## Checking the numbers

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
(cd tests && NODE_PATH=$(npm root -g) node export.js)
.venv/bin/python check_numbers.py
```
