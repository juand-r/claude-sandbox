# Midterm: ROC curves and AUC (a pool of parts to choose from)

Each version has a computational core, (R1) to (R3), and optional parts to pick from. No tied
scores. AUC is computed as the area under the staircase (as on the lecture's AUC slide). All numbers
are made up and recomputed by `check_numbers.py`. Points are left blank.

---

## Practice test: the metal detector's signal strength

The metal detector from part (d) does more than beep: it reports a signal strength for every square.
Here are 10 squares from the test field, 5 with a mine and 5 without.

| square         | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  |
|----------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| signal         | 9.1 | 8.3 | 7.4 | 6.0 | 5.2 | 4.8 | 3.9 | 2.5 | 2.0 | 1.1 |
| contains mine? | yes | yes | no  | yes | yes | no  | no  | yes | no  | no  |

The detector flags a square when its signal is at least a threshold t.

**(R1)** Sweep t from above 9.1 down to below 1.1. List the (FPR, TPR) point after t passes each
square.

**(R2)** Sketch the ROC curve.

**(R3)** Compute the AUC.

Optional parts:

**(R4) Choosing a threshold.** The field may only be declared safe if every mine is found. What is the
largest threshold that flags all 5 mines, and what is the FPR there? If instead no false alarm were
allowed, what would the TPR be?

**(R5) Transforming the scores.** (i) The manufacturer changes the display to show √(signal) instead of
the signal. What happens to the ROC curve and the AUC? (ii) A software bug shows −signal instead.
What is the AUC now? Is the detector now useless?

**(R6) Two detectors whose curves cross.** Two radar systems are tested. Their ROC curves, drawn with
straight lines between these points, are:

- A: (0, 0), (0, 0.5), (0.2, 0.7), (0.4, 0.8), (0.6, 1), (1, 1). AUC = 0.85.
- B: (0, 0), (0.1, 0.3), (0.2, 0.6), (0.3, 1), (1, 1). AUC = 0.84.

A has the higher AUC. Which system would you use for mine clearance, and why? Which would you use if
false alarms had to be avoided completely?

### Solutions

**(R1)** Each mine moves the point up by 1/5 = 0.2; each mine-free square moves it right by 0.2.

| t passes square | 1        | 2        | 3        | 4        | 5        | 6        | 7        | 8        | 9        | 10       |
|-----------------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|
| (FPR, TPR)      | (0, 0.2) | (0, 0.4) | (0.2, 0.4) | (0.2, 0.6) | (0.2, 0.8) | (0.4, 0.8) | (0.6, 0.8) | (0.6, 1) | (0.8, 1) | (1, 1) |

Starting point: (0, 0).

**(R2)** A staircase from (0, 0) to (1, 1) through those points: up, up, right, up, up, right, right,
up, right, right.

**(R3)** Columns of width 0.2, with heights 0.4, 0.8, 0.8, 1, 1:
AUC = 0.2 × (0.4 + 0.8 + 0.8 + 1 + 1) = 0.80.

**(R4)** t = 2.5 (the weakest mine signal). Squares at or above 2.5 include the mine-free squares 3, 6
and 7, so FPR = 3/5 = 0.6. With no false alarms allowed, t must be above 7.4: only squares 1 and 2 are
flagged, TPR = 0.4.

**(R5)** (i) √ is increasing, so the order of the squares is unchanged: same ROC curve, same AUC 0.80.
Only the threshold values change (t = 2.5 becomes about 1.58). (ii) −s reverses the order: AUC =
1 − 0.80 = 0.20. Not useless: flip the scores back (or flag squares with low displayed values) and
the AUC is 0.80 again.

**(R6)** For mines, recall must be 1: B reaches TPR = 1 at FPR = 0.3, A only at FPR = 0.6, so B
wastes half as many digs. With no false alarms allowed (FPR = 0), A has TPR 0.5 and B has TPR 0, so A
wins. AUC averages over all thresholds; what matters is the curve at the operating point you need.

---

## Exam: the AI detector's scores

The AI detector reports a score between 0 and 1 for each essay; higher means "more likely written
with AI". Here are 8 essays, 4 written with AI and 4 by students.

| essay           | 1    | 2    | 3     | 4    | 5     | 6    | 7     | 8     |
|-----------------|------|------|-------|------|-------|------|-------|-------|
| score           | 0.95 | 0.85 | 0.70  | 0.60 | 0.50  | 0.40 | 0.30  | 0.10  |
| written with AI?| yes  | yes  | no    | yes  | no    | yes  | no    | no    |

An essay is flagged when its score is at least a threshold t.

**(R1)** Sweep t from 1 down to 0. List the (FPR, TPR) point after t passes each essay.

**(R2)** Sketch the ROC curve.

**(R3)** Compute the AUC.

Optional parts:

**(R4) Choosing a threshold.** The course decides that no student may be falsely accused. Which
thresholds achieve FPR = 0? What is the largest TPR among them?

**(R5) Transforming the scores.** (i) The detector is updated to report s² instead of s. What happens
to the ROC curve and the AUC? Does the threshold t = 0.5 still flag the same essays? (ii) A different
tool reports 1 − s, a "human-written" score. What is its AUC, if we keep flagging high scores?

**(R6) Two detectors whose curves cross.** (Same curves A and B as in the practice test.) Which
detector would you use for AI essays, where false accusations must be avoided? Which would you use if
catching every AI essay mattered most?

### Solutions

**(R1)** Each AI essay moves the point up by 1/4 = 0.25; each human essay moves it right by 0.25.

| t passes essay | 1         | 2        | 3           | 4           | 5          | 6        | 7         | 8      |
|----------------|-----------|----------|-------------|-------------|------------|----------|-----------|--------|
| (FPR, TPR)     | (0, 0.25) | (0, 0.5) | (0.25, 0.5) | (0.25, 0.75)| (0.5, 0.75)| (0.5, 1) | (0.75, 1) | (1, 1) |

Starting point: (0, 0).

**(R2)** A staircase from (0, 0) to (1, 1): up, up, right, up, right, up, right, right.

**(R3)** Columns of width 0.25, with heights 0.5, 0.75, 1, 1:
AUC = 0.25 × (0.5 + 0.75 + 1 + 1) = 0.8125 ≈ 0.81.

**(R4)** Any t above 0.70 (the highest human score). The largest TPR is at t just above 0.70: essays
1 and 2 are flagged, TPR = 0.5.

**(R5)** (i) Squaring is increasing on [0, 1], so the order is unchanged: same curve, same AUC
0.8125. But t = 0.5 on the new scale corresponds to s = √0.5 ≈ 0.71 on the old one, so it flags fewer
essays (only essays 1 and 2). The same cut is now t = 0.25. (ii) 1 − s reverses the order: AUC =
1 − 0.8125 = 0.1875. Flagging low "human-written" scores instead recovers 0.8125.

**(R6)** Avoiding false accusations means FPR near 0: A has TPR 0.5 there, B has 0, so A. Catching
every AI essay means TPR = 1: B gets there at FPR 0.3, A at FPR 0.6, so B. The higher AUC (A) does
not settle it; the operating point does.

---

## Notes

- The practice version is slightly harder: 10 items instead of 8, and a threshold on a scale that is
  not 0 to 1.
- (R4) mirrors the first problem's lesson: for mines the constraint is on TPR, for essays on FPR.
- (R5)(i) in the exam has a small trap: the curve does not change, but a fixed threshold value does.
- (R6) works for either version; its two questions are the same two operating points, asked in the
  version's own setting.
