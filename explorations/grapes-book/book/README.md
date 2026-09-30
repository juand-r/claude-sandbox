# Grapes: the book

## Writing

Chapters go in `chapters/`, one file each, pulled in by `\include` in
`grapes.tex`. For notes, use only these three commands:

| Command        | What it makes                                        | Mark        |
|----------------|------------------------------------------------------|-------------|
| `\note{...}`    | footnote at the foot of the page                     | 1, 2, 3 (restart each chapter) |
| `\subnote{...}` | note on a note; only inside `\note`; own block, under its own rule, below the notes | a, b, c (restart each page) |
| `\aside{...}`   | margin note beside the line                          | none        |

Everything about how these look is in `grapes.sty`; the chapters contain no
layout code.

## Turning margin notes off

In `grapes.tex`, change `\usepackage{grapes}` to
`\usepackage[nomargin]{grapes}`. Every `\aside` then becomes an ordinary
numbered `\note`, and the page narrows to 5.5 x 8.5 in. No text is lost. To
see both versions without editing anything: `./build.sh` and
`./build.sh nomargin`.

## Rules the build enforces

These stop the build with an error naming the line, so nothing goes missing
quietly: a `\subnote` outside a `\note`; a `\subnote` inside a `\subnote`; a
`\note` or `\subnote` inside an `\aside`; an `\aside` inside a note; an
`\aside` taller than the page. An `\aside` longer than a third of the page
only warns, because it pushes later margin notes away from their lines.

## Build and test

    ./build.sh             # grapes.pdf, margin notes on
    ./build.sh nomargin    # grapes-nomargin.pdf
    tests/run.sh           # 14 checks: each rule above, in both modes

Requirements are in `../README.md`.
