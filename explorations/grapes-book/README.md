# Grapes

A book about grapes, in the spirit of John McPhee's *Oranges* (1967), with
many footnotes and notes on footnotes. This directory holds the book and the
layout experiments that led to it.

## Current state (2026-10-01)

The layout machinery is done and tested. The book has one chapter of
placeholder prose whose facts are unchecked. Next: style and content (see
`PLAN.md`).

## Where things are documented

| File | What it says |
|------|--------------|
| `book/README.md` | How to write in the book: the five commands, turning margin notes off, what stops the build, how to build and test. Start here. |
| `book/STYLE.md`  | Writing conventions, each with its reason and date (e.g. anchors go at the start of a sentence). |
| `book/LINKS.md`  | Which links between main text, notes, subnotes and asides are possible, and which are not, and why. |
| `book/grapes.sty` | The layout itself. Its header comment summarizes the commands and rules. |
| `PLAN.md`  | What is done and what comes next. |
| `NOTES.md` | Findings and decisions, in order, including mistakes and how they were caught. |
| `specimens/` | The five layouts compared before choosing (`grapes-specimens.pdf`). |

## How to build

Needs LuaLaTeX, TeX Live with `bigfoot`, `perpage`, `marginfix`, `refcount`,
`hyperref`, `titlesec`, `reledmac` (specimens only), the EB Garamond and
Linux Libertine fonts, and poppler-utils (`pdftotext`, `pdfunite`). On
Debian/Ubuntu:

    apt-get install texlive-latex-extra texlive-fonts-extra texlive-luatex \
                    texlive-humanities poppler-utils

The book (details in `book/README.md`):

    book/build.sh              # book/grapes.pdf, with margin notes
    book/build.sh nomargin     # book/grapes-nomargin.pdf
    book/tests/run.sh          # needs book/.venv, see book/README.md

The specimens:

    specimens/build.sh         # grapes-specimens.pdf
