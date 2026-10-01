# Which links are possible

There are four kinds of place a reader can be: the main text, a note, a
subnote, an aside. Links between them come in two kinds.

## 1. Mark links: made by nesting, always two-way

Writing one command inside another makes a mark. In the PDF the mark links to
the note, and the note's own mark links back. These are the only nestings
allowed:

| Written in   | `\note` | `\subnote` | `\aside` |
|--------------|:-------:|:----------:|:--------:|
| main text    | yes     | no         | yes      |
| note         | no      | yes        | no       |
| subnote      | no      | no         | no       |
| aside        | yes     | no         | no       |

As a picture (each arrow also links back):

    main text ──► note ──► subnote
        │          ▲
        └─► aside ─┘

So the longest chain is main text → aside → note → subnote.

Why the "no"s:

- main text → subnote: a subnote is a note on a note; it needs a note to
  hang from.
- note → note, subnote → note: that would be a third level of footnotes.
  Use `\subnote`, or `\xref` to another note.
- subnote → subnote: same; only two levels are set up.
- aside → subnote directly: put a `\note` in the aside, and the `\subnote` in
  that note.
- note or subnote → aside: LaTeX cannot place a margin note from inside a
  footnote. Point to an aside with `\xref` instead.
- aside → aside: a margin note cannot hold another margin note.

Every "no" stops the build with an error that names the line.

## 2. Cross-references: `\xref`, one-way, any to any

`\xref{key}` links from wherever it is written to whatever carries that key.
It prints the target's mark, plus ", p. N" when the target is on another
page. Every combination works:

| `\xref` written in | to a note | to a subnote | to an aside | to an anchor |
|--------------------|:---------:|:------------:|:-----------:|:------------:|
| main text          | yes       | yes          | yes         | yes          |
| note               | yes       | yes          | yes         | yes          |
| subnote            | yes       | yes          | yes         | yes          |
| aside              | yes       | yes          | yes         | yes          |

Notes, subnotes and asides become targets by taking a key:
`\note[key]{...}`. A place in the main text becomes a target with
`\anchor{key}`, at the start of the sentence (see `STYLE.md`). An anchor can
also sit inside a note, subnote or aside, to mark one sentence in a long note.

The only way back into the main text, other than a note's own back-link to
its mark, is an anchor. That is how loops are made (`sample.pdf`, the
typography sample, has one).

## How this is checked

Both tables hold in both versions of the book (with and without margin
notes). `tests/run.sh` builds a test document for each "yes" in the first
table and an error case for each "no". The case `xref-matrix` covers all 16
cells of the second table, plus anchors inside a note, a subnote and an
aside. `tests/check_links.py` checks that every link in those PDFs has a
target.
