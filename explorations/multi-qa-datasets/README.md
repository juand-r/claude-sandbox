# Multi-QA Datasets Analysis

Exploring QA datasets where questions have multiple correct and incorrect answer options.
Goal: find a dataset (or subset) of sufficient size where each question has a good number of both correct and incorrect answers.

## Datasets

- **MultiRC** (Multi-Sentence Reading Comprehension): questions with multiple answer candidates, each labeled correct/incorrect.
- **PlausibleQA**: 10K questions with 100K candidate answers scored for plausibility (0-100).

## How to run

```bash
pip install datasets pandas tabulate requests
python multirc_analysis.py
python plausibleqa_analysis.py
```

## Files

- `multirc_analysis.py` - Load, explore, and compute answer-count statistics for MultiRC
- `plausibleqa_analysis.py` - Same for PlausibleQA
- `NOTES.md` - Metadata/annotations notes for both datasets
- `PLAN.md` - Working plan
