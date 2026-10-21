# Neural networks: lecture slides for two classes

Two interactive decks for a machine learning class, following the logistic regression deck. Class 1
(28 slides) starts from last lecture's losses, builds a network out of simplified neurons (hidden
layers, softmax, forward propagation, activation functions, deeper networks), shows why hidden layers are needed (XOR), and
then turns to training: cross-entropy, the loss landscape and gradient descent. Four bonus slides at the
end: the perceptron, the losses compared, softmax vs argmax, and why softmax and cross-entropy
fit together.
Class 2 (27 slides, one of them a bonus) is about training: backpropagation, worked through one example with numbers on a
2-2-1 network (regression with squared error, then the same network predicting a class with log
loss, then two outputs), learning rates,
momentum, local minima, batch versus mini-batch versus stochastic gradient descent, early stopping, and a family tree
that leads into a later lecture on architectures. Same template and engine as `../svm-lecture/`.

## How to run

Open `neural_nets_1.html` or `neural_nets_2.html` in a browser. No server or install is needed.

- `→` / `Space`: next step; `←`: back; `↓` / `↑`: next or previous slide.
- `P`: presenter view in a second window, with speaker notes for every step.
- `F`: fullscreen; `?`: help.

Every training run in the decks was computed beforehand in Python and is replayed. The one exception
is gradient descent on the made-up two-valley surface (the loss landscape slide in class 1 and the local minima slide in class 2), which is
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
  once before assembling. Labels inside the figures use the same fonts: `mtxt()` in `common.js`
  draws a label such as `x₁`, `wⱼᵢ` or `x_N` with italic variables and real subscripts.
- `assets/`: the images (Pandemonium drawing, a photo of neurons, the neuron diagram by BruceBlaus
  (CC BY 3.0), Rosenblatt, Minsky, Papert, the Perceptrons cover).
- `practice/fwdprop_practice_solution.tex` (and `.pdf`): the forward-propagation practice problem (sign
  hidden layer, softmax output, record (5, 10)) solved in the class convention, z = Wx + b with column
  vectors. Build with `pdflatex` in `practice/`.
- `practice/backprop_practice_solution.tex` (and `.pdf`): the backprop practice problem (2-3-3-1: sigmoid,
  ReLU, linear; squared error; adjust W(1)21) solved for both handout versions, which differ in the ReLU
  slope at 0. C1 = 0 makes that matter: version 1 gives 1.73, version 2 (C1's input sum taken as 0) -2.2863.
- `tests/`: Playwright scripts, run from `tests/` with `NODE_PATH=$(npm root -g) node <script>.js`:
  `steps.js <1|2> [slide-id ...]` (every step of every slide), `interact1.js` and `interact2.js`
  (dragging, replays, presenter view, dark mode, phone width), `recap2.js` (the live network on
  class 2's recap slide, in the deck and from the presenter window), `mathwrap.js <deck.html>` (formula
  wrapping at five screen sizes).

## PDF versions

`neural_nets_1.pdf` and `neural_nets_2.pdf` have one page per slide, each at its last step (light theme,
controls hidden). They are images of the slides, so the text cannot be selected. To regenerate:

```
cd tests && NODE_PATH=$(npm root -g) node pdf.js 1 && cd ..   # screenshots into pdf/slides_1/
.venv/bin/python make_pdf.py 1                                  # writes neural_nets_1.pdf
```

`neural_nets_1_steps.pdf` and `neural_nets_2_steps.pdf` have one page per step instead, so they show
the order in which things appear (animations and interactive figures are shown as they end up at each
step). Same commands with `steps` as the last argument: `node pdf.js 1 steps`, `make_pdf.py 1 steps`.

`neural_nets_2_annotate.html` and `neural_nets_2_annotate.pdf` are an annotation copy of class 2: every
slide shows one fixed step and nothing appears on a press. Which step each slide shows is in
`build/annotate_2.json` (slides not listed show their full build). To rebuild:

```
python3 build/assemble.py 2 neural_nets_2_annotate.html build/annotate_2.json
cd tests && NODE_PATH=$(npm root -g) node pdf.js 2_annotate && cd ..   # screenshots into pdf/slides_2_annotate/
.venv/bin/python make_pdf.py 2_annotate                                 # writes neural_nets_2_annotate.pdf
```

## Reproducing the numbers

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python experiments.py      # rewrites build/data.json
.venv/bin/python check_numbers.py    # ends with "all checks passed"
```
