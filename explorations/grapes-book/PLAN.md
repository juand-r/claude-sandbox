# Plan

## Phase 1: layout (done, except tinkering)

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
- [x] Marked asides (symbols, per page), notes inside asides, keys and
      cross-references in every direction (\anchor, \xref), PDF links
      from every mark to its note and back. Tests for all of it.
- [x] 2026-10-01: a closed reading loop in chapter 1; the author's rule that
      anchors go at the start of a sentence (book/STYLE.md); book/LINKS.md
      listing every possible link, with a test for each.
- [ ] Later, tinker: trim size, typeface, chapter opening, margin notes on
      verso pages (currently ragged-right on both sides), the look of the
      * mark and of the ❧ anchor.

## Phase 2: style and content (next, with the author)

- [ ] Talk about style: voice, tone, what goes in the text and what goes in
      notes. Record decisions in book/STYLE.md.
- [ ] Decide the book's chapters and their order.
- [ ] Decide what each note level is for (see NOTES.md, "Open questions").
- [ ] Decide how to keep facts verified: a source for every claim, kept where?

## Phase 3: writing

Not started.
