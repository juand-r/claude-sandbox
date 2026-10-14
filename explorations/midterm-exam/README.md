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

- `practice_midterm.tex`: practice test, questions 1 (TB rats), 2 (SVMs) and 3 (nonlinear regression).
- `final_midterm.tex`: the exam, questions 1 (AI-text detection), 2 (SVMs) and 3 (nonlinear
  regression), slightly easier. The figure for 3.3 is `fig_q33.tex`, drawn from data written by
  `make_figure.py` (`.venv/bin/python make_figure.py`; packages in `requirements.txt`).

Each builds two PDFs, the test and its solutions; the commands are at the top of each file.
