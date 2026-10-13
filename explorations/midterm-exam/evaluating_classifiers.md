# Midterm: Evaluating classifiers (20 points)

Two versions. The practice test (mine-detection rats) is slightly harder than the exam (AI-text
detection): students first turn rates into counts, and then compare two detectors and judge a
two-step plan. All numbers are made up; they are recomputed by `check_numbers.py`.

---

## Practice test: a rat that finds landmines

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

### Solutions

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

---

## Exam: detecting AI-written essays

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

### Solutions

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

---

## Notes on the two versions

- Same skeleton: confusion matrix, precision and recall, which error is worse, one conceptual
  extension.
- The practice test is harder in three ways: rates instead of counts, a second classifier, and a
  two-step plan to judge.
- They teach opposite instincts: for the rat, recall matters most; for the AI detector, precision
  matters most.
- Accuracy appears differently. For the rat it is a trap (the do-nothing rat scores higher). For
  the AI detector it is not asked, to keep the exam shorter; it is 95%, against 85% for flagging
  nothing.
