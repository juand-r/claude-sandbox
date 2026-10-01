# Grapes: the book's machinery

The book itself has not been started. It will be a new LaTeX file that loads
`grapes.sty`. What is here so far:

| File | What it is |
|------|------------|
| `grapes.sty` | The layout: notes, subnotes, asides, anchors, cross-references, PDF links. |
| `sample.tex`, `sample-text.tex` | A typography sample, NOT the book: a few pages of throwaway prose used to test `grapes.sty`. Builds `sample.pdf`. |
| `STYLE.md`, `BIO.md` | How the book will be written, and its narrator. |
| `LINKS.md` | Which links between text and notes are possible. |
| `build.sh`, `lib.sh`, `tests/` | Build and test scripts. |

## Writing

Read `STYLE.md` first: it holds the conventions for using these commands.
`LINKS.md` lists which links between text, notes, subnotes and asides are
possible.

The text uses these commands only; everything about how notes look is in
`grapes.sty`.

| Command              | What it makes | Marks |
|----------------------|---------------|-------|
| `\note[key]{...}`    | footnote at the foot of the page | 1, 2, 3; restart each chapter |
| `\subnote[key]{...}` | note on a note; only inside a `\note`; own block below the notes, under its own rule | a, b, c; restart each page |
| `\aside[key]{...}`   | margin note; may contain `\note`s, whose text goes to the foot of the page | \*, †, ‡, §, ¶, ‖, then doubled; restart each page |
| `\anchor{key}`       | a mark ❧ for a note to point back to; goes at the start of a sentence (`STYLE.md`); in the text or inside any note | ❧ |
| `\xref{key}`         | the mark of the note, subnote, aside or anchor named `key`, plus ", p. N" when it is on another page; allowed anywhere | |

`[key]` is optional. Give a key only to notes you want to point to. Keys
must be unique in the book.

Pointing works in every direction, so loops are possible: a subnote can point
to an aside, an aside's note can point back to an anchor in the text, and so
on. Example (syntax only):

    \anchor{berry}A grape is a berry. ...
    ...\note{...\subnote{Which brings us back to \xref{berry}.}}

In the PDF every mark is a link: from the text to its note, and from the
note back to the text. `\xref` is a link too. Links are invisible in print.

## Turning margin notes off

In the main `.tex` file, change `\usepackage{grapes}` to
`\usepackage[nomargin]{grapes}`. Asides then go to the foot of the page, in
their own block above the notes, with the same symbols; the page narrows to
5.5 x 8.5 in. No text is lost, and every `\xref` still works. To see both
versions without editing anything: `./build.sh MAIN` and
`./build.sh MAIN nomargin`.

## What stops the build

Errors, naming the line (the full table, with reasons, is in `LINKS.md`):

- `\note` inside a note or a subnote (use `\subnote`);
- `\subnote` outside a `\note`, inside a `\subnote`, or directly inside an
  `\aside` (put a `\note` in the aside, and the `\subnote` in that note);
- `\aside` inside a note, a subnote or an `\aside`;
- an `\aside` taller than the page.

Checked on the final pass (LaTeX only warns about these; the build fails):

- a `\xref` to a key that does not exist; a key used twice;
- more than nine asides on one page;
- references that have not settled after three passes.

An `\aside` longer than a third of the page only warns: it pushes later
margin notes away from their lines.

## Build and test

    ./build.sh sample            # sample.pdf, margin notes on
    ./build.sh sample nomargin   # sample-nomargin.pdf
    tests/run.sh                 # every rule above, in both versions, plus link checks

`build.sh` takes the name of the main `.tex` file. Today the only one is
`sample` (the typography sample). The tests use their own small documents,
not the sample.

The tests need a Python virtualenv, once:

    python3 -m venv .venv && .venv/bin/pip install -r tests/requirements.txt

`tests/check_links.py` checks the PDF links: every link has a target, and
each mark's link sits exactly where its partner mark is. It can also be run
on any build: `.venv/bin/python tests/check_links.py sample.pdf`.

Other requirements (TeX Live, fonts) are in `../README.md`.
