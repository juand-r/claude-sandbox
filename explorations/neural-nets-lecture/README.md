# Neural networks: lecture slides for two classes

Two interactive decks for a machine learning class, following the logistic regression deck. Class 1
(16 slides) goes from one neuron to a network: one-hot labels, softmax and cross-entropy, the loss
landscape and gradient descent, the perceptron and XOR, hidden layers and forward propagation.
Class 2 (17 slides) is about training: backpropagation, learning rates, momentum and Adam, local
minima, batch versus mini-batch versus stochastic gradient descent, early stopping, and a family tree
that leads into a later lecture on architectures. Same template and engine as `../svm-lecture/`.

## How to run

Open `neural_nets_1.html` or `neural_nets_2.html` in a browser. No server or install is needed.

- `→` / `Space`: next step; `←`: back; `↓` / `↑`: next or previous slide.
- `P`: presenter view in a second window, with speaker notes for every step.
- `F`: fullscreen; `?`: help.

Every training run in the decks was computed beforehand in Python and is replayed. The one exception
is gradient descent on the made-up two-valley surface (class 1 slide 6, class 2 slide 11), which is
cheap enough to run in the browser so the start point can be dragged.

## Files

- `neural_nets_1.html`, `neural_nets_2.html`: the decks, each one self-contained (images and data
  embedded).
- `PLAN.md`: the slide-by-slide plan agreed with the user.
- `NOTES.md`: decisions, sources and the corrections made while checking.
- `experiments.py`: computes every training run and writes `build/data.json`.
- `check_numbers.py`: recomputes, independently of `experiments.py`, every number quoted on the
  slides and in the notes, and checks the backpropagation formulas against numerical derivatives.
- `build/`: the sources of the decks. `assemble.py` combines the SVM deck's engine with
  `slides_<k>.html`, `common.js`, `code_<k>.js`, `extra.css`, `data.json` and the images in `assets/`.
  Unlike the earlier decks, the build files stay the source: edit them and re-run
  `python3 build/assemble.py 1 neural_nets_1.html` (or `2 neural_nets_2.html`).
  Formulas in `slides_<k>.html` are written in LaTeX, as `\( … \)` (inline) or `\[ … \]` (display).
  `build/tex.js` typesets them with KaTeX (version pinned in `build/package.json`) when the deck is
  assembled, and embeds KaTeX's fonts, so the deck needs no network. Run `npm install` in `build/`
  once before assembling. So far only class 1 uses this; class 2 still has plain-text formulas.
- `assets/`: the images (Pandemonium drawing, Rosenblatt, Minsky, Papert, the Perceptrons cover).
- `tests/`: Playwright scripts, run from `tests/` with `NODE_PATH=$(npm root -g) node <script>.js`:
  `steps.js <1|2> [slide-id ...]` (every step of every slide), `interact1.js` and `interact2.js`
  (dragging, replays, presenter view, dark mode, phone width), `mathwrap.js <deck.html>` (formula
  wrapping at five screen sizes).

## Reproducing the numbers

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python experiments.py      # rewrites build/data.json
.venv/bin/python check_numbers.py    # ends with "all checks passed"
```
