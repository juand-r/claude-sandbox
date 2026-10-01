# Style guide for Grapes

Conventions for writing the book. Each rule says why, so it can be applied to
cases it does not name. Add rules here as they are decided, with the date.
Rules marked PROPOSED are my reading of the author's brief and wait for the
author's confirmation.

The narrator is described in `BIO.md`. The commands are described in
`README.md` and `LINKS.md`.

## 1. The book in one paragraph (2026-10-01)

A first-person investigation of the grape, in the manner of McPhee's
*Oranges*: the narrator goes places, reads things, counts things, and reports.
Alongside it runs a second writing, about the writing itself and the man
doing it, in the manner of the commentary in Nabokov's *Pale Fire*: the
reader assembles a story the narrator never tells outright. The notes cite
each other and invite jumps, as the chapters of Cortázar's *Rayuela* do. The
mood and the typography come from Danielewski's *House of Leaves*: something
is wrong, and the page itself starts to show it. Order at the start; chaos at
the end.

## 2. Voices

### 2.1 Who is speaking (2026-10-01; confirmed by the author)

One narrator: Hollis Vane (see `BIO.md`), an elderly Napa wine man from a
small town in Nebraska, who trained in Burgundy. He writes everything: the
investigation, the notes, the asides. The two parallel writings are two
registers of the same man: the investigator in the main text and notes, and
the private man in the asides.

Unlike *Pale Fire*, which has two people (a poet and his commentator), there
is no second voice. No editor, no translator, no found manuscript.

### 2.2 Main text: the investigation (2026-10-01)

- First person, as a researcher in the field and the library. "I drove to",
  "I counted", "I asked". He is present, as McPhee is present in *Oranges*.
- Encyclopedic tone. Definitions, taxonomies, dates, measurements, names of
  varieties and people, in complete, orderly sentences.
- Obsessive about detail, past the point of use. He measures what nobody
  needs measured, gives the third decimal, corrects himself, and counts again.
  The excess is the joke and, later, the symptom. It is never explained.
- He does not talk about himself in the main text, at first. When he starts
  to, that is part of the collapse (section 4).

Example of the register (no factual claims):

    I counted the berries on the cluster in front of me. There were 117. I
    counted them again and there were 118. One of them, I believe, had been
    hiding.

### 2.3 Notes and subnotes: digressions and crucial points (2026-10-01)

- Notes carry digressions, but also things the book cannot do without. A
  reader who skips the notes misses part of the story. So never put only
  ornament in notes, and never keep the main text self-sufficient on purpose.
- Same voice as the main text, looser: more opinion, more tangents, more
  precision about less important things.
- Subnotes go one level further out: the digression of a digression, the
  correction of a note, the source of the source.

### 2.4 Asides (margin): the second writing (2026-10-01)

- The parallel text, as in *Pale Fire*: the narrator on the process of
  researching and writing (the cards, the lamp, the hour, the typewriter,
  what he read today and why he could not finish it) and, more and more, on
  himself.
- Voice: an old man, courtly, a little formal, with French and the trade's
  vocabulary in his mouth. Under it, a Nebraska plainness that comes back
  when he is tired or angry. Sudden exactness about times and quantities.
  Self-pity he catches and dislikes. Flashes of anger.
- Asides are short at first: a line or two, mostly about method.
- The asides read as one continuous story when read alone, in order. Check
  this whenever a chapter is finished: read only the asides.

### 2.5 The mystery: show, never tell (2026-10-01)

The reader must never be told whether the death of Odile (see `BIO.md`) was
an accident. Everything reaches the reader as slips: what he avoids saying,
what he corrects, what he records and what he does not, objects that come
back. Rules:

- Never state the mystery. Never resolve it.
- Every clue must also have an innocent reading.
- Plant motifs early and quietly (the list is in `BIO.md`). Return to them.
- He is unreliable, not lying on every page. Most of what he says is true.

## 3. Facts (2026-10-01; confirmed by the author)

The world is real; the story is fiction; the two may be interleaved freely.

- Every claim about the real world (grapes, vines, wine, places, history,
  books, films) must be either verified, or attributed to a named source
  ("according to Galet, ..."). Its source is kept in the repository (format
  to be decided). The encyclopedic tone only works if the encyclopedia is
  right.
- Elements of the story are fiction: Vane, Odile, the people around them,
  the Domaine Ferrand, the town of Ardath, the pond, the cards. They may sit
  in the same sentence as real facts.
- Invented things must be invented on purpose and listed in `BIO.md`, so
  that a reader of the repository can always tell which is which.
- Real people appear only in their public, historical roles, and never in
  the fictional plot.
- Open: whether Vane may get a real fact wrong on purpose, as a character.
  If ever used, each such error must be listed, with the truth beside it.

## 4. The arc: from order to chaos (2026-10-01)

The book becomes progressively more unhinged. Three movements; the chapter
boundaries are not decided yet.

| | I. Order | II. Leakage | III. Collapse |
|---|---|---|---|
| Main text | Clean, encyclopedic, impersonal "I" | Personal remarks slip in; obsessive passages grow | Thins out; notes take over the page |
| Notes | Digressions, sources, wit | Contradict the main text; address someone ("you") | Notes on notes on notes; notes that cite notes that do not exist |
| Asides | Rare, short, about method | Longer; about him; Odile named by initial | Flood the margin; dated entries; the night itself circled |
| Cross-references | Few, helpful | Loops begin; invitations to jump ahead | Mazes; an alternative reading order, as in *Rayuela* |
| Typography | Plain | First struck-out words; a second typeface in the asides | Fonts mixed, struck passages, page layouts broken |

Escalate slowly. Each movement should feel like the previous one gone a
little further, not like a different book.

## 5. Typography as voice (2026-10-01; PLANNED, not built)

As in *House of Leaves*, the look of the page is part of the writing. Needs
layout work before it can be used:

- a separate typeface for the asides (the private voice); possibly a
  typewriter face, since he types his drafts (see `BIO.md`);
- struck-out text that stays legible (he crosses out but does not erase);
- later: marks with no note, notes with no mark, text set at angles or in
  odd shapes, an alternative reading order printed at the front.

Until built, do not fake these with ad hoc LaTeX in the chapters.

## 6. Marks

### 6.1 Anchors go at the beginning of what they mark (2026-10-01)

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

## 7. Cross-references

### 7.1 Write them so they read in both versions (2026-09-30)

The book builds with margin notes (`./build.sh`) and without them
(`./build.sh nomargin`). In the second version, asides move to the foot of the
page. So never say where a note is; let `\xref` say it.

    Right:  For the town, see \xref{concord}.
    Wrong:  The town is the one in the margin, \xref{concord}.
