# Grapes: the book

## Writing

Read `STYLE.md` first: it holds the conventions for using these commands.

Chapters go in `chapters/`, one file each, pulled in by `\include` in
`grapes.tex`. Chapters contain text and these commands only; everything about
how notes look is in `grapes.sty`.

| Command              | What it makes | Marks |
|----------------------|---------------|-------|
| `\note[key]{...}`    | footnote at the foot of the page | 1, 2, 3; restart each chapter |
| `\subnote[key]{...}` | note on a note; only inside a `\note`; own block below the notes, under its own rule | a, b, c; restart each page |
| `\aside[key]{...}`   | margin note; may contain `\note`s, whose text goes to the foot of the page | \*, †, ‡, §, ¶, ‖, then doubled; restart each page |
| `\anchor{key}`       | a mark ❧ in the text, for a note to point back to | ❧ |
| `\xref{key}`         | the mark of the note or anchor named `key`, plus ", p. N" when it is on another page | |

`[key]` is optional. Give a key only to notes you want to point to. Keys
must be unique in the book.

Pointing works in every direction, so loops are possible: a subnote can point
to an aside, an aside's note can point back to an anchor in the text, and so
on. Example:

    \anchor{berry}A grape is a berry. ...
    ...\note{...\subnote{Which brings us back to \xref{berry}.}}

In the PDF every mark is a link: from the text to its note, and from the
note back to the text. `\xref` is a link too. Links are invisible in print.

## Turning margin notes off

In `grapes.tex`, change `\usepackage{grapes}` to
`\usepackage[nomargin]{grapes}`. Asides then go to the foot of the page, in
their own block above the notes, with the same symbols; the page narrows to
5.5 x 8.5 in. No text is lost, and every `\xref` still works. To see both
versions without editing anything: `./build.sh` and `./build.sh nomargin`.

## What stops the build

Errors, naming the line:

- `\note` inside a note (use `\subnote`);
- `\subnote` outside a `\note`, inside a `\subnote`, or directly inside an
  `\aside`;
- `\aside` inside a note or inside an `\aside`;
- an `\aside` taller than the page.

Checked on the final pass (LaTeX only warns about these; the build fails):

- a `\xref` to a key that does not exist; a key used twice;
- more than nine asides on one page;
- references that have not settled after three passes.

An `\aside` longer than a third of the page only warns: it pushes later
margin notes away from their lines.

## Build and test

    ./build.sh             # grapes.pdf, margin notes on
    ./build.sh nomargin    # grapes-nomargin.pdf
    tests/run.sh           # every rule above, in both versions, plus link checks

The tests need a Python virtualenv, once:

    python3 -m venv .venv && .venv/bin/pip install -r tests/requirements.txt

`tests/check_links.py` checks the PDF links: every link has a target, and
each mark's link sits exactly where its partner mark is. It can also be run
on the book: `.venv/bin/python tests/check_links.py grapes.pdf`.

Other requirements (TeX Live, fonts) are in `../README.md`.
