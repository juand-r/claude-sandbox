# Style guide for Grapes

Conventions for writing the book with the commands in `README.md`. Each rule
says why, so it can be applied to cases it does not name. Add rules here as
they are decided, with the date.

## Marks

### Anchors go at the beginning of what they mark (2026-10-01)

An anchor (`\anchor{key}`, printed ❧) is a destination. The reader arrives
at it from a note and reads forward from there. So it goes at the start of
the sentence or passage it marks, never at the end.

A note mark is the opposite: it points from the text to a note, so it goes
at the end of what it comments on, after the punctuation.

    Right:  \anchor{not-berries}By this rule the tomato is a berry, ...
            ... the raspberry are not.\note{...}
    Wrong:  ... the raspberry are not.\anchor{not-berries}\note{...}

Following this rule also keeps two marks from piling up at the end of a
sentence ("not.❧¹").

## Cross-references

### Write them so they read in both versions (2026-09-30)

The book builds with margin notes (`./build.sh`) and without them
(`./build.sh nomargin`). In the second version, asides move to the foot of the
page. So never say where a note is; let `\xref` say it.

    Right:  For the town, see \xref{concord}.
    Wrong:  The town is the one in the margin, \xref{concord}.
