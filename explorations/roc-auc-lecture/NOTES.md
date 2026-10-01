# Plan and notes

## Plan
- [x] Read the slide template (styles, deck engine, `chart()` helper, presenter view).
- [x] Pick the examples and verify every number with `check_numbers.py`.
- [x] Write `roc_auc_lecture.html` from the template (12 slides).
- [x] Render every slide with Playwright, look at the screenshots, fix problems.
  First pass found: charts on the wide slides too small to read; a dot clipped on the
  exercise slide (it sat in the clipped plot layer); the "10,000" tick cut off; class labels
  colliding on the bell-curve chart. All fixed (stacked layout, `fs`/`ml` chart options,
  dot moved to the unclipped layer, "1k/10k" ticks, HTML legend).
- [x] Test interactions (pair count = 79, transforms keep AUC, drag), dark mode, phone width,
  presenter view. All numbers matched `check_numbers.py`. Found and fixed: slide 9 was wider
  than a phone screen (four tiles in a row); now two per row below 620px.
- [x] Requested change: slide 3 now builds in order. Step 0-1: the points only. Step 2: the
  threshold, shaded region and slider. Step 3: the orange mistake rings and the confusion
  matrix. The threshold cannot be dragged before it is shown.
- [x] Commit and push.

## Slide outline
1. Title: ROC curves and AUC (text only; the ROC figure was removed because students have not seen ROC curves yet).
2. Today: scores to decisions. k-NN, naive Bayes and decision trees all produce scores; so far we thresholded at 0.5.
3. A score and a threshold (running example, draggable threshold, live confusion matrix).
4. Two rates: TPR and FPR, each computed inside one true class.
5. Sweep the threshold: every threshold is one point; the points make the ROC curve.
6. What the shape tells you: binormal model with a separation slider.
7. AUC as a probability: draw (positive, negative) pairs; each pair is one cell of the ROC grid.
8. What AUC does and does not tell you.
9. Rare positives: same TPR and FPR, collapsing precision.
10. Your turn: 6-example exercise, answers revealed step by step.
11. Takeaways.
12. Thanks.

## Decisions
- Running example: 10 positives, 10 negatives, all scores distinct (no ties, so the
  ROC staircase has no diagonal pieces). AUC = 79/100 = 0.79.
- Rule: predict positive when score >= t.
- Binormal model: negatives ~ N(0,1), positives ~ N(d,1); AUC = Phi(d/sqrt 2).
- Colours from the template palette: positives teal (`--model`), negatives purple
  (`--mean`), threshold amber (`--hi`), mistakes orange (`--err`).
- Presenter name left blank, as asked. The template author's copyright credit is kept as
  a small "slide template" credit; the lecture content is new.
- Dropped the template's holding and schedule slides (no course schedule given).
- Template changes outside the slides: `chart()` gained `W`, `H`, `ml` (left margin) and
  `xfmt` options; the template's example code and its regression helpers were removed; the
  BroadcastChannel is renamed `deck-roc-auc`.
- SVG elements revealed by a step are wrapped in a `<g data-step>`. Putting `data-step` on the
  shape itself would let the draw-in animation briefly show it, because that animation writes
  an inline opacity.
