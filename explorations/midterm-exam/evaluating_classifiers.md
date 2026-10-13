# Midterm: Evaluating classifiers (20 points)

Two versions. The practice test (mine-detection rats) is slightly harder than the exam (AI-text
detection). Each version has two problems:

1. Confusion matrix, precision and recall: parts (a) to (e).
2. ROC curves and AUC: a core of three parts, (R1) to (R3), and optional parts (R4) to (R6) to choose
   from. No tied scores; AUC is computed as the area under the staircase, as on the lecture's AUC
   slide. Points for these parts are left blank.

All numbers are made up and recomputed by `check_numbers.py`.

---

# Practice test

## Problem 1: a rat that finds landmines

A charity trains African giant pouched rats to find landmines by smell. Before a rat is allowed to
work, it is tested on a test field whose mine locations are known. The field is divided into 1,000
squares, and 40 of them contain a mine. The rat walks over every square and scratches the ground
when it smells explosive. Treat "the square contains a mine" as the positive class.

The rat scratches on 95% of the squares that contain a mine, and on 5% of the squares that do not.

**(a) (4 points)** Write down the rat's confusion matrix.

**(b) (4 points)** Compute the rat's precision and recall. For each one, say in one sentence what it
means for the people working in the field.

**(c) (3 points)** Which kind of error is worse here, a false positive or a false negative? A rat that
never scratches would have an accuracy of 96%. Compute the real rat's accuracy, and explain why
accuracy is the wrong measure for this job.

**(d) (5 points)** A metal detector is tested on the same field. It beeps on every square that
contains a mine, and also on 30% of the squares without a mine, because of scrap metal in the soil.
Write down its confusion matrix and compute its precision and recall. In two or three sentences,
compare the rat and the metal detector.

**(e) (4 points)** To save time, a team proposes this plan: the rat goes first, and deminers dig only
the squares where the rat scratched. What is the recall of this plan? On this test field, how many
mines would be left in the ground? Would you declare the field safe?

## Problem 2: the metal detector's signal strength

The metal detector from Problem 1(d) does more than beep: it reports a signal strength for every square.
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

## Solutions

### Problem 1

**(a)** 40 mine squares and 960 mine-free squares.

|                   | rat scratches | rat moves on |
|-------------------|---------------|--------------|
| **mine**          | TP = 38       | FN = 2       |
| **no mine**       | FP = 48       | TN = 912     |

TP = 0.95 × 40, FP = 0.05 × 960.

**(b)** Precision = 38 / (38 + 48) = 38/86 ≈ 0.44: of the squares the rat flags, about 44% really hold
a mine, so more than half of the digging is for nothing. Recall = 38/40 = 0.95: the rat finds 95% of
the mines, and misses 1 in 20.

**(c)** A false negative is worse: a missed mine can kill someone after the field is handed back. A
false positive only costs a slow, careful dig. The rat's accuracy is (38 + 912)/1000 = 95%, lower
than the 96% of a rat that does nothing. Accuracy is dominated by the 960 mine-free squares and says
nothing about the missed mines; the measure that matters most here is recall.

**(d)**

|                   | detector beeps | silent      |
|-------------------|----------------|-------------|
| **mine**          | TP = 40        | FN = 0      |
| **no mine**       | FP = 288       | TN = 672    |

Precision = 40/328 ≈ 0.12, recall = 40/40 = 1. The detector misses nothing, but about 88% of its
digs are wasted; the rat wastes about 56% of its digs but misses 2 of the 40 mines. The detector is
safer; the rat is much cheaper. (Accuracy 71%, if students compute it: lower than the rat's, though
the detector is the safer tool.)

**(e)** Recall of the plan = the rat's recall, 0.95: a mine the rat misses is never dug up. On this
field, 2 mines stay in the ground. The field is not safe. Grading note: full credit for seeing that
filtering by the rat can only lower recall; any sensible fix (for example, still sweeping the
squares the rat skipped) is a bonus.

### Problem 2

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

# Exam

## Problem 1: detecting AI-written essays

A course runs an AI-text detector on all 400 essays submitted for an assignment. An honor-code
review later established that 60 of the essays were written with AI. The detector flagged 50
essays, and 45 of the flagged essays were written with AI. Treat "written with AI" as the positive
class.

**(a) (5 points)** Write down the detector's confusion matrix.

**(b) (5 points)** Compute the detector's precision and recall.

**(c) (4 points)** Of the students the detector flagged, how many wrote their essay themselves? Which
kind of error is worse here, a false positive or a false negative? Which of precision or recall
should the course care about most? Explain in two or three sentences.

**(d) (3 points)** The instructor raises the detector's threshold, so that it flags fewer essays.
What happens to the recall? What usually happens to the precision?

**(e) (3 points)** Another course uses the same detector, with the same recall and the same false
positive rate, but in that course only 5% of the essays are written with AI. Will the precision be
higher or lower than in (b)? Explain without computing.

## Problem 2: the AI detector's scores

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

**(R6) Two detectors whose curves cross.** Two AI detectors are tested. Their ROC curves, drawn with
straight lines between these points, are:

- A: (0, 0), (0, 0.5), (0.2, 0.7), (0.4, 0.8), (0.6, 1), (1, 1). AUC = 0.85.
- B: (0, 0), (0.1, 0.3), (0.2, 0.6), (0.3, 1), (1, 1). AUC = 0.84.

Which detector would you use for AI essays, where false accusations must be avoided? Which would you use if
catching every AI essay mattered most?

## Solutions

### Problem 1

**(a)** 60 AI-written essays and 340 human-written essays.

|                    | flagged   | not flagged |
|--------------------|-----------|-------------|
| **written with AI**| TP = 45   | FN = 15     |
| **human-written**  | FP = 5    | TN = 335    |

**(b)** Precision = 45/50 = 0.90. Recall = 45/60 = 0.75.

**(c)** 5 of the 50 flagged students (10%) wrote the essay themselves. A false positive is worse: it
accuses an innocent student of cheating. A missed AI essay is a smaller harm. So precision matters
most: a flag should almost always be right before anyone acts on it.

**(d)** Recall cannot go up: every essay flagged at the higher threshold was also flagged before, so
the detector can only catch the same AI essays or fewer. Precision usually goes up, because the
essays that remain flagged are the ones the detector is surest about; but it is not guaranteed to.

**(e)** Lower. With fewer AI essays there are fewer true positives, while the human-written essays,
and with them the false positives, become more numerous. A larger share of the flags are false
alarms.

### Problem 2

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

## Notes on the two versions

Problem 1:

- Same skeleton: confusion matrix, precision and recall, which error is worse, one conceptual
  extension.
- The practice test is harder in three ways: rates instead of counts, a second classifier, and a
  two-step plan to judge.
- They teach opposite instincts: for the rat, recall matters most; for the AI detector, precision
  matters most.
- Accuracy appears differently. For the rat it is a trap (the do-nothing rat scores higher). For
  the AI detector it is not asked, to keep the exam shorter; it is 95%, against 85% for flagging
  nothing.

Problem 2:

- The practice version is slightly harder: 10 items instead of 8, and a threshold on a scale that is
  not 0 to 1.
- (R4) mirrors the first problem's lesson: for mines the constraint is on TPR, for essays on FPR.
- (R5)(i) in the exam has a small trap: the curve does not change, but a fixed threshold value does.
- (R6) works for either version; its two questions are the same two operating points, asked in the
  version's own setting.
