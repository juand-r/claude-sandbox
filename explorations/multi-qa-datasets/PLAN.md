# Plan

## MultiRC
- [x] Load via HuggingFace `super_glue` (multirc config) -- has train/validation splits
- [ ] Print a few examples
- [ ] Basic stats: num questions, num passages, answers per question distribution
- [ ] Table: fraction/count of questions with N+ total answers (N in {4,5,10,15,20,...})
- [ ] Table: fraction/count of questions with N+ incorrect answers
- [ ] Note metadata/annotations

## PlausibleQA
- [ ] Load from GitHub (DataScienceUIBK/PlausibleQA)
- [ ] Print a few examples
- [ ] Basic stats
- [ ] Same tables as above (using plausibility threshold for correct/incorrect)
- [ ] Note metadata/annotations

## Notes
- MultiRC: each row in HF is one (question, answer_option) pair with a binary label.
  Need to group by question to count answers per question.
- PlausibleQA: answers have plausibility scores 0-100. Need to define threshold for "correct" vs "incorrect".
  The dataset marks one answer as the gold correct answer.
