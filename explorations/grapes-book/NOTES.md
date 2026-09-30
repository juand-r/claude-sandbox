# Notes on the layout specimens

All specimens: LuaLaTeX, EB Garamond, TeX Live 2023 (Debian packages).
The sample passage is placeholder prose; its facts are from memory and
unchecked.

## Writing the text once

The passage is written with three semantic commands: `\note`, `\subnote`
(a note on a note), `\subsubnote`. Specimens 1 to 3 input the same file and
differ only in what these commands do. If we keep this discipline for the
book, the layout can change late without touching the prose. Specimens 4 and
5 need different markup (lemmas, hand-cut pages), so they have their own text.

## 1. Stacked footnotes (bigfoot)

- Works out of the box. `bigfoot` allows a note of one series inside a note
  of another and keeps the series in order at the foot.
- Letters and symbols restart on each page (`perpage`), so they never run
  out. This needs three LaTeX passes.
- Cost: when notes are long, a page can be mostly notes, and the main text
  shrinks to a few lines. McPhee's own notes are few; ours will not be.

## 2. Sidenotes, their notes at the foot

- Custom macro, about 20 lines. A footnote placed inside a margin note is
  lost in standard LaTeX, so inside the margin a `\subnote` prints only its
  mark and saves its text; the text is released as a footnote in the main
  text right after the anchor.
- Known flaw, visible in the PDF: on page 1 the sidenote 4 mark "d" is on
  page 1, but its footnote text was pushed to page 2 because the page was
  full. TeX does this with ordinary footnotes too, but here the mark is in the
  margin, which makes the jump harder to follow.
- Cost: long sidenotes pile up. `marginfix` keeps them from overlapping by
  pushing them down, so they drift away from their anchors.

## 3. Sidenotes, their notes in the margin

- Same macro with a switch. Notes on a sidenote are printed under it, in
  smaller type, after a short rule; letters restart for each sidenote.
- Cost: the drift problem of Specimen 2 is worse, because the margin now
  holds two levels. In the PDF, sidenote 4 belongs to the last lines of
  page 1 but is printed at the top of page 2's margin. This layout only works if sidenotes stay short.

## 4. Talmud-style page

- Built from scratch; I did not find a CTAN package for this layout and did
  not search exhaustively. Each commentary is one paragraph with a
  `\parshape`: n narrow lines beside the main text, then full width. n is
  computed from the measured height of the main text.
- Commentaries are keyed by lemma (bold opening words), not by marks, as in
  the printed Talmud. The two commentaries use two typefaces.
- Cost: one page at a time, by hand. The page does not flow. To use it for
  more than a few pages we would need a program that measures the text and
  cuts it into pages. The two columns also end at different heights; a
  real page would need the text trimmed or padded to balance them.
- A first attempt hung LuaLaTeX: I wrote `1sp` inside `\numexpr`, which is
  not a valid integer expression, and the line count came out wrong. Fixed.

## 5. Notes keyed to line numbers (reledmac)

- Lines numbered in the outer margin; three note series (gloss, words,
  aside) at the foot, each note citing line number and lemma. The text has no
  marks at all.
- Cannot be combined with `bigfoot` in the same document without care (both
  take over footnotes), so this specimen has its own preamble.
- Notes on notes are not natural here: a note cannot be keyed to a line of
  another note.

## Open questions for the author

- Which is the main reading experience: clean text with notes out of the way
  (1, 5), or notes in the eye line (2, 3, 4)?
- What does each level mean? One option: level 1 = facts and sources,
  level 2 = digressions, level 3 = asides to the reader.
  Another: levels by subject (botany, history, words).
- Trim size. Specimens use 5.5 x 8.5 in (1, 5), 7.5 x 9.5 in (2, 3),
  7 x 9 in (4). A mixed book would need one size.
