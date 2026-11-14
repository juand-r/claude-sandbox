# Plan: 2D Writing v2

## Where v1 (`../2d-writing`) ended

Summary taken from v1's `NOTES.md`, `PLAN.md` and source headers. I have not
re-run the v1 code in this session.

- `grid2d.py`: beam search with summed row + column n-gram scores, and a
  variant with a fixed word category per column. Rows were sentences; columns
  were only word lists ("i we they you").
- `grid2d_v2.py`: beam search in diagonal order. An interior cell accepts only
  words in the intersection of the top-k continuations of its row and of its
  column. Trigram model on the Brown corpus. Best 4x4:

  ```
  but it is not
  it was the only
  is the way to
  not only to the
  ```

  The grid is symmetric (row i equals column i), and it is built from function
  words. 5x5 degenerates in the fifth row and column.
- GPT-2 as the scorer did worse than the n-gram model: poor sentence starters
  and locally plausible but ungrammatical phrases ("had be a good").
- `grid2d_v3.py`: GPT-2 with top-p sampling; rows wrap into one continuous
  passage, each column is an independent sentence. Its results are not
  recorded in v1's notes.

## Open questions for v2 (to be decided with the user)

- [ ] What is the goal of v2? (larger grids, non-symmetric grids, content
      words, a different reading scheme, a different model, ...)
- [ ] How do we measure success?

## Tasks

- [x] Create project directory, README, PLAN
- [ ] Decide goals
