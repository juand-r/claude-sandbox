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

## 2026-09-27 (later): annotated edition

Change of strategy (user's request): original text verbatim in the main column,
ruthless commentary (skeptic + English teacher, Williams's "Style: Lessons in Clarity
and Grace") in a wide right margin. Same five pilot posts.

- `annotated/main.tex` + `annotated/posts/*.tex` (posts not committed). PDF copied to
  `lesswrong-annotated.pdf` (not committed).
- Note tags: style, logic, fact, cut, good, author's footnote.
- Layout history:
  1. tufte-handout sidenotes. Failed: dense notes ran off the page bottom
     (4 of 12 pages), because a Tufte sidenote cannot break across pages.
  2. + marginfix. Failed: notes from one post landed on the next post's page, even
     with \clearmargin.
  3. paracol (current). Each paragraph ends with \flushnotes, which prints its queued
     notes in the right column and realigns the columns. No overflow; cost is white
     space in the text column beside long notes.
- `src/check_verbatim.py` strips notes and markup and diffs against the original. All
  five match. Tested by mutating two words: both caught.
- One deviation: " -- " in the Salamon footnote is typeset as two hyphens (-{}-) so
  LaTeX does not turn it into an en dash.
- Facts checked for the notes: tree riddle first printed in The Chautauquan, June 1883
  (Wikipedia); West & Stanovich 1997 is the source behind "12% aren't overconfident";
  Barber, Lee, Liu, Odean: <1% of Taiwanese day traders predictably profitable;
  "What Evidence Filtered Evidence?" posted 29 Sep 2007, day after "The Bottom Line".

- Removed the "good" notes at the user's request. Two of them also held criticism
  (Bottom Line: thesis comes late; PR: structure, stray comma); those parts kept as style notes.
- Added "Twelve Virtues of Rationality" (user's request) as post 6, and a table of
  contents. Adjacent note marks now get a comma ("1,2", not "12").
- check_verbatim.py: now also handles footnote markers after closing quotes, "######"
  footnote lists, and Unicode normalization (the original spells "é" in Saint-Exupéry
  as e + combining accent). All six posts match.
- Facts checked for Twelve Virtues notes: Saint-Exupéry's French begins "Il semble
  que", in a passage on aircraft design; Musashi quotation matches Victor Harris's
  translation; counts in the notes ("the Way" 6x, "Art" 2x, "Beware lest" 3x) counted
  with grep.
- Added a Summary and a Response after each post (annotated/afterwords/, committed:
  my own writing). Response judges the post as an anonymous essay and places it in
  context. Quotes verified before use: Peirce 1878 pragmatic maxim; James 1907
  squirrel; Quine 1951 "corporate body"; Franklin's "reasonable creature"; Feynman
  1974; Bernays 1928 ch. 1 first sentence (checked in the text); Sagan/Truzzi dates;
  Turing & Good ban/deciban 1940; Nisbett & Cohen honor/homicide finding; Simon 1956
  satisficing; Stanovich & West 2000 System 1/2; CFAR 2012; Sosa 1980.
- Marked as my inference in the text: the PR post (14 Feb 2021) may respond to the
  NYT article on Slate Star Codex (13 Feb 2021).
- User: Responses too nice. Rewrote all six to judge what each piece is doing
  (rhetorical function, whom it flatters, hidden assumptions), quoting others only
  where the quote does work. Each ends with "In short: ...".
- Mistake corrected: I had praised Twelve Virtues' definition of humility as "the best
  definition in the text". Merriam-Webster: humility = "freedom from pride or
  arrogance"; humble = "not proud or haughty: not arrogant or assertive"; Latin
  humilis "low". The essay's definition is prudence, not humility. Margin note replaced.
- Also found and removed praise that had crept back into four Twelve Virtues margin
  notes after the user asked to drop "good" comments.
- Checked all quotations in the new Responses against the originals; fixed one
  misquote ("glimpsed" -> "glimpse the center"). CFAR workshop price ($3,900, 4 days)
  from rationality.org FAQ via search.
- Lesson: I was grading on the authors' reputation and on surface quality. Read for
  what the piece does to its reader, and check my own praise as hard as my criticism.
- Humility note (Twelve Virtues) extended with quotes from "AGI Ruin: A List of
  Lethalities" (2022, items 41-42), checked verbatim against the fetched post, and the
  "Against Modest Epistemology" chapter of Inadequate Equilibria (2017). The post says he
  is the only one who could write the list, not literally the only one who can save the
  world; the note quotes what it says.
- Humility note: added the "only one who can make the effort" quote from Yudkowsky's
  ~2000 autobiography. Primary (web.archive.org) unreachable from this environment;
  quoted via Torres, with the archive link, and the note says so. Added his own
  disclaimer (yudkowsky.net/singularity, verified): everything 2002 or earlier obsolete.
  The 2015 LessWrong post with the same wording is satire, not the source.
- Per user: removed the Torres citation; the note now cites the archived page directly
  (web.archive.org snapshot 2001-02-05, #timeline_birth). I still have not read that page:
  archive.org is blocked here. Wording rests on the secondary quotation until checked.
