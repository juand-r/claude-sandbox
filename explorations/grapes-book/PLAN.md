# Plan

## Phase 1: layout (in progress)

- [x] Install LaTeX toolchain; check which note packages are available.
- [x] Specimen 1: stacked footnotes, three levels (bigfoot).
- [x] Specimen 2: sidenotes whose own notes drop to the page foot.
- [x] Specimen 3: sidenotes whose own notes stay in the margin.
- [x] Specimen 4: Talmud-style page, commentaries wrapped around main text.
- [x] Specimen 5: notes keyed to line numbers (reledmac).
- [x] Show specimens to the author. Decision (2026-09-30): stacked footnotes,
      two levels with a rule between them (specimen 1, `[ruled]`), plus
      margin notes that can be switched off in one line.
- [x] Set up `book/` with `grapes.sty` (\note, \subnote, \aside), a build
      script for both modes, and tests.
- [ ] Later, tinker: trim size, typeface, chapter opening, margin notes on
      verso pages (currently ragged-right on both sides).

## Phase 2: structure (next, with the author)

- [ ] Decide the book's chapters and their order.
- [ ] Decide what each note level is for (see NOTES.md, "Open questions").
- [ ] Decide how to keep facts verified: a source for every claim, kept where?

## Phase 3: writing

Not started.
