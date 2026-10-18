# Midterm exam: problem drafts

Drafts of midterm problems, in two versions each: a practice test (slightly harder) and the exam.
Topics and points: evaluating classifiers (20), SVMs (20), nonlinear regression (20), neural networks
(30), ensembling (10, conceptual).

- `evaluating_classifiers.md`: both versions, practice (mine-detection rats) and exam (AI-text
  detection). Each has a confusion-matrix problem and an ROC/AUC problem, with solutions.
- `check_numbers.py`: recomputes every number in the problems (`python3 check_numbers.py`, standard
  library only; ends with "all checks passed").

The scenarios' numbers are made up. Background facts behind the rat scenario, checked by web search:
APOPO trains African giant pouched rats to smell explosives; its first rats passed the International
Mine Action Standards tests in 2004. Metal detectors give roughly 100 to 1,000 false alarms per real
mine, mostly from scrap metal.

## LaTeX exams (`latex/`)

- `practice_midterm.tex`: practice test, questions 1 (TB rats), 2 (SVMs), 3 (nonlinear regression) and
  4 (neural networks: forward pass with sign units, backpropagation through sigmoid, ReLU and linear
  layers, short answers) and 5 (ensembles: multiclass SVMs, accurate and diverse base classifiers,
  bagging). The numbers for question 4 come from `nn_practice.py`. It is based on last
  year's practice problems, with new numbers; three inconsistencies in last year's backprop problem
  were fixed (sigmoid outputs outside (0, 1), a bias input of 5 instead of 1, and E = (Y' - Y)^2 with
  derivative Y' - Y; now E = 1/2 (Y' - Y)^2).
- `final_midterm.tex`: the exam, questions 1 (AI-text detection), 2 (SVMs), 3 (nonlinear
  regression) and 5 (ensembles: multiclass SVMs, base classifiers worse than random, random forests),
  slightly easier. Question 4 (neural networks) is not written yet; question 5 is numbered by hand
  until it is. The figure for 3.3 is `fig_q33.tex`, drawn from data written by
  `make_figure.py` (`.venv/bin/python make_figure.py`; packages in `requirements.txt`).
- `final_midterm2.tex`: a shorter, easier version of the exam (asked by the user, 2026-10-18), being
  edited question by question. So far: 1.4 asks for the three ROC points after (0, 0) instead of the
  whole curve; 1.5 asks what an AUC of 0.3 means and how to fix it (flip the scores: 0.7) instead of
  computing the AUC; 2.1 uses only points C, D, E; 2.2(b) asks only about xi > 1; 2.3 is
  (a)-(c) circle one of two (`\pick` in the file; the solutions circle the answer); (d) stays
  open ended, with its own answer box; 3.2 has one subpart and answer box per model (3.1's box went from
  7 lines to 3 so question 3 still fits on two pages).
  Question 4 (neural networks) is being written: 4.1 is the practice's forward pass with a ReLU
  hidden layer and linear outputs (class = larger output), new numbers; forgetting the ReLU flips the
  answer. 4.2 (14 points) is backprop on a 2-2-1 network (sigmoid hidden and output, cross-entropy,
  Y = 1): (a) update an output weight, (b) a first-layer weight, from given node values. Question 5 is
  now numbered automatically.

Each builds two PDFs, the test and its solutions; the commands are at the top of each file.
Both use `cs363m_exam.sty`, the layout of the course's practice exam: a title page with the
instructions (question count and point total filled in automatically), each question on its own page,
bold part prompts, and a lined "Answer" box after every part (`\answerbox{lines}`). In the solutions
PDFs the solution takes the box's place.
