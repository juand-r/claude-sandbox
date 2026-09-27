# Notes

## 2026-09-27

- API: https://www.lesswrong.com/graphql, no auth needed for reads.
  Useful queries: `collection` (by _id), `GetAllReviewWinners`, `post` with `contents { html }`.
  `collection` selector does not accept `slug`; list collections to find ids.
- Collections found: highlights, bestoflesswrong, codex, hpmor, rationality.
- Review winners: `reviewRanking` 0 appears to be the top post of each year (inferred
  from the ordering; not documented).
- Some winners are near-empty on LessWrong (e.g. "Embedded Agents", 49 words: it is a
  sequence of images; "Draft report on AI timelines", 191 words: a link post). These
  need special handling or exclusion.
- Licensing: authors keep copyright (LW terms). Rewrites are derivative works, so the
  repo (public) does not get the texts until we decide otherwise.

### Pilot (5 posts)
Length of rewrite vs original (words, body only):

| post | original | rewrite | ratio |
|---|---|---|---|
| Humans are not automatically strategic | 1120 | 1155 | 103% |
| Making Beliefs Pay Rent | 1128 | 1019 | 90% |
| "PR" is corrosive | 486 | 498 | 102% |
| Strong Evidence is Common | 286 | 478 | 167% |
| The Bottom Line | 1068 | 1001 | 93% |

Plain English did not make these posts shorter. Splitting long sentences adds words,
and editorial notes add more. The short Mark Xu post grew most because of three notes
checking its arithmetic.

Errors found in originals (flagged in notes, not silently fixed):
- Strong Evidence is Common: "50% sure you're in the top 1% needs 200:1 evidence".
  Prior odds 1:99, so 99:1 suffices; 200:1 gives ~67%.
- Making Beliefs Pay Rent: phlogiston attributed to alchemists; it was 17th-18th c. chemistry.
