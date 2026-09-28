# Report: preface

## 1. The argument in three sentences

Looking back on two years of daily blog posts, the author lists five large mistakes: teaching
theory instead of practice, using abstract distant problems instead of everyday ones,
stressing belief over action, poor organization (the only one this book corrects), and
contempt for ideas the author thought stupid. The goal was to teach a "certain valuable way of
thinking", tied to science and to saying "Oops", that schools do not teach and that applies
to daily life as well as the laboratory. Despite the mistakes, the posts appeared to help
many people, because it is "all, in the end, one thing", so the collection is "better than
nothing".

## 2. Sources checked

- C. S. Lewis on Bulverism: Wikipedia "Bulverism" (raw wikitext fetched this session), which
  quotes Lewis's essay: "You must show that a man is wrong before you start explaining why he
  is wrong. The modern method is to assume without discussion that he is wrong and then
  distract his attention from this (the only real issue) by busily explaining how he became so
  silly." Also: "The term Bulverism was coined by C. S. Lewis"; essay of 1941 ("Notes on the
  Way", Time and Tide), expanded 1944. Secondary source, cited as such only in the report; the
  note says only that the gloss "is close to Lewis's".
- Center for Applied Rationality: Wikipedia "Center for Applied Rationality" (founded 2012 by
  Galef, Salamon, Smith, Critch). I considered a note on CFAR's ties to Yudkowsky's
  organization but the fetched text did not state them, so I made none.

## 3. Arithmetic recomputed

- None needed. Counts: "way of thinking" occurs 6 times in the original ("this valuable",
  "certain valuable", "This certain", "this certain" twice, "a certain"); "Oops" 5 times;
  "one thing" twice (both in the "Because it is all" paragraph). Only "twice" is used in a note.
- Paragraph numbering in my own reasoning: "That mistake at least is correctable" is the
  seventh paragraph (counted). No note now relies on the number.

## 4. Claims about other posts

- None in the preface notes. The biases-an-introduction notes quote this preface (see that
  report).

## 5. Not verified

- Whether the "bit" of rewriting that Bensinger did touched the first three mistakes. My notes
  say only that the preface "does not say" so. Checking would mean comparing book text with
  the original posts.
- Nothing else is asserted from outside sources.

## 6. Judgment calls for the editor

1. The main charge (cpara on the seventh paragraph, the Response and an n.b.): the book
   corrects only the fourth mistake. It rests on the preface's own words ("That mistake at
   least is correctable"; "without trying to rewrite all the actual material (though he's
   rewritten a bit of it)"). I did not write "does not correct"; I wrote that the preface does
   not say the others were addressed.
2. "No evidence" notes on the mockery view ("I thought, and still do think") and on the
   readership. A fair defender could say a preface may state its author's opinions. I kept
   them because both are claims about how people behave, and the preface itself raises the
   risk of mockery. Candidates for cutting under STANDARDS 2.4 (4).
3. The CFAR parenthesis: "this huge mistake of mine" could refer to the first or the second
   mistake (the paragraph mixes them). I wrote "this mistake about practice", which covers
   both.
4. I first misread the opening as "seeing mistakes means learning" (the converse of what the
   text says) and corrected it to "not seeing any would mean the author had learned nothing".
   Worth a second look.
5. The preface is mostly self-description. Many cparas are plain descriptions; I did not look
   for faults where the paragraph just reports the author's history.
6. No note uses a reserved word in the author's own voice; the four "wrong" flags are quotes
   or Lewis's definition.

## 7. Pilot feedback on the brief and standards (applies to all three of my posts)

1. "Substantial paragraph" is undefined. audit.py counts every line ending in `\flushnotes`
   (including citation-only footnotes and one-line questions), so its paragraph count and the
   \cpara count never match for posts with reference lists. I skipped citation footnotes. A
   rule (e.g., "footnotes that only cite a source get no \cpara unless there is a problem with
   the source") would make the audit meaningful.
2. The brief lists four model posts; STANDARDS section 1 lists five (adds
   positive-bias-look-into-the-dark). I read the four in the brief.
3. STYLE.md's final checklist says "an ironic line the author could plausibly say about
   himself", which conflicts with the pronoun rule. Harmless, but an agent copying phrasing
   from it could slip.
4. Prefaces and book introductions are not arguments, and the standard is built for
   arguments. Unclear: should unsupported self-assessments in a preface ("appeared to help",
   "my readership has been amazingly good") be flagged as unsupported, or left as "any preface
   does that" (STANDARDS 2.2 test 4)? I flagged the ones that are claims about the world and
   left the purely biographical ones. A line in STANDARDS would help.
5. The honest edition for a non-Yudkowsky author (Bensinger) worked with the same rules, first
   person as Bensinger. STYLE.md assumes Yudkowsky; worth one sentence saying so.
6. Honest-edition n.b. count: STANDARDS says "a handful". A data-heavy post (Scope
   Insensitivity) naturally produces more (7). Is that acceptable, or should n.b. notes be
   merged?
7. Tooling: md2tex leaves Unicode superscript footnote markers (¹ to ⁷); ⁴ to ⁷ break the
   LaTeX build (see biases-an-introduction report, item 6.6, for the tested preamble fix).
8. Access limits met: web.archive.org blocked; econweb.ucsd.edu fails TLS through the proxy;
   sas.upenn.edu returns 403; Google Books API quota exhausted (429); Springer paywalled. The
   brief's "If a source cannot be reached, drop the claim or say so" was easy to apply, but
   many R:A-Z posts cite the same contingent-valuation and heuristics-and-biases papers, so a
   shared folder of fetched sources would save later agents time.
9. The scratchpad directory is shared with the main session and other agents. I worked in a
   subfolder (`raz_p1/`) to avoid collisions; the brief could say to do this.
10. STANDARDS 2.5 asks that a recurring criticism be made in full once "where it matters
   most". With posts drafted in parallel, an agent cannot know where that is. I made the
   "no standard for the right response" point in full in Scope Insensitivity, where the
   evidence is; our On Caring notes make a related point.
