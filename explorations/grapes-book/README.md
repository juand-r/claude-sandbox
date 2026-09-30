# Grapes

A book about grapes, in the spirit of John McPhee's *Oranges* (1967), with
many footnotes and notes on footnotes. This directory holds the book's
layout experiments and, later, the book itself.

## Current state

- `book/`: the book's working setup. Two levels of footnotes stacked at the
  foot, plus optional margin notes. See `book/README.md` for how to write in
  it. Chapter 1 holds placeholder prose with unchecked facts.
- `specimens/` and `grapes-specimens.pdf`: the five layouts we compared
  before choosing (see `NOTES.md`).

## How to build

Needs LuaLaTeX, TeX Live with `bigfoot`, `perpage`, `marginfix`, `reledmac`,
the EB Garamond and Linux Libertine fonts, and `pdfunite` (poppler-utils).
On Debian/Ubuntu:

    apt-get install texlive-latex-extra texlive-fonts-extra texlive-luatex \
                    texlive-humanities poppler-utils

Then:

    cd specimens && ./build.sh      # writes ../grapes-specimens.pdf

## Files

- `specimens/common.tex`: shared preamble (fonts, three note levels).
- `specimens/passage.tex`: the sample text, written once with semantic note
  commands (`\note`, `\subnote`, `\subsubnote`) that each layout maps to its
  own mechanism.
- `specimens/0N-*.tex`: one file per specimen.
- `PLAN.md`: what we are doing and in what order.
- `NOTES.md`: findings about each layout.
