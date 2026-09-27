# Annotated LessWrong posts: instructions for the next annotator

This directory builds a PDF in which each LessWrong post appears verbatim in the left
column, with numbered critical commentary in the right column, followed by a Summary
and a Response. Read this whole file before touching anything. The user has corrected
earlier work several times; the corrections are folded in below, so that you do not
repeat them.

## 1. What the user wants

A careful, skeptical, unforgiving reading of each post, of the kind a very good English
teacher and a very good logician would give an anonymous student essay. Judge the text,
not the author's reputation. The user has said, in so many words:

- "Your judgment is too nice." Earlier Responses praised too readily. Do not.
- "Your comments are hyper-local." Sentence-level notes are not enough. Every
  paragraph must be read as a unit, and the essay as a whole.
- No praise notes. A "good" tag existed and was removed at the user's request. Do not
  reintroduce praise in any other tag. (It crept back once, into four notes of
  "Twelve Virtues"; they had to be removed a second time.)
- Quoting other writers is optional. Use a quotation only when it does work in your
  argument (for example Quine on testing beliefs one at a time, or the dictionary on
  "humility"). Never pad with context for its own sake.
- Do not cite Émile Torres. Cite primary sources.

## 2. Files and build

```
annotated/
  main.tex              layout, macros, title page, table of contents (committed)
  posts/<name>.tex      verbatim post text + notes (NOT committed: authors' copyright)
  afterwords/<name>.tex Summary and Response (committed: our own writing)
  build/                LaTeX output (not committed)
../data/originals/      fetched originals in Markdown (not committed)
../src/fetch.py         fetch a post:  ../.venv/bin/python ../src/fetch.py post <id>
../src/check_verbatim.py  confirm the left column matches the original
```

Build: `cd annotated && latexmk -pdf -interaction=nonstopmode -outdir=build main.tex`.
Then copy `build/main.pdf` to `../lesswrong-annotated.pdf` and send it to the user.

The repo is public. Never commit a post's text, a PDF, or anything in `data/originals`.

## 3. Layout mechanics (read before editing a post file)

- Two columns via `paracol`. Every paragraph line in a post file ends with
  `\flushnotes`, which prints that paragraph's queued notes in the right column and
  realigns the columns. Inside `quote`, `itemize` and `enumerate`, put `\flushnotes`
  only after `\end{...}`.
- Note macros: `\cpara{}` (paragraph level), `\cstyle{}`, `\clogic{}`, `\cfact{}`,
  `\ccut{}`, `\cauthor{}` (the author's own footnotes, verbatim).
- `\cpara{...}` goes at the very start of the paragraph's line, so its mark is the
  first in the paragraph and its note prints first in the margin.
- A new tag must be added in three places: a macro in `main.tex`, a line in the tag
  list on the title page, and `COMMENT_MACROS` in `src/check_verbatim.py`.
- Two adjacent marks get a comma automatically (the `\cnote` kern trick).
- Do not use Tufte sidenotes or `marginfix`. Both were tried; notes ran off the page or
  onto the next post's page. See `../docs/NOTES.md`.
- Unicode: some originals use decomposed accents (e + combining accent). Write the
  precomposed form in `.tex`. The checker normalizes to NFC.

## 4. The left column must be verbatim

Copy the text exactly, including the author's typos, italics, bold and odd spacing. The
only permitted changes: Markdown links become `\href`, escaped asterisks stay literal,
and ` -- ` is written `-{}-` so LaTeX does not turn it into a dash. After every edit
to a post file, run:

```
../.venv/bin/python ../src/check_verbatim.py posts/<name>.tex ../data/originals/<slug>.md
```

It must print `OK`. It strips notes and markup and diffs the words. It catches a
single changed word or capital letter; this was tested by mutation.

## 5. How to read: three levels, every paragraph

Read the whole post twice before writing anything. Write its argument down in three
sentences for yourself. Then comment at three levels.

### 5.1 The paragraph (`\cpara`), required for every substantial paragraph

Ask of each paragraph:

1. Job. What is this paragraph for: thesis, setup, example, evidence, objection,
   transition, conclusion? Say so.
2. Does it do the job? If it is an example, does it show what the essay says it shows?
   If it is evidence, is it evidence of the claim or of something nearby?
3. Place. Is it in the right position? Does the method come before or after the
   examples that need it? Is the thesis stated early or only implied? Is the best idea
   buried at the end, or in a footnote, or in a parenthesis?
4. Links. Does it follow from the previous paragraph and lead to the next? Does it
   quietly change the subject? Does it repeat what an earlier paragraph already said?
5. Shape. Does it make one move or several? Does its most important sentence sit where
   the reader will notice it (usually first or last)? Could it be merged with a
   neighbor or split in two?
6. Cost. What does the paragraph cost the reader (new jargon, a detour, an unexplained
   reference) and what does it give back?

Write each `\cpara` note as a judgment, not a summary. "This is the thesis" is not
enough; say whether it is stated or merely announced, and what it should have said.

### 5.2 The sentence and the phrase (`\cstyle`, `\clogic`, `\cfact`, `\ccut`)

Style, using Joseph Williams, "Style: Lessons in Clarity and Grace":
- characters as subjects, actions as verbs; flag nominalizations ("the evidential
  entanglement of the ink became fixed");
- old information before new; the important thing at the end of the sentence;
- no interruption between subject and verb, or between parts of a verb;
- hedges (count them), intensifiers, redundant pairs, metadiscourse ("this is in some
  sense a small detail");
- elegant variation (four synonyms for "strong" in four sentences);
- mixed or piled-up metaphors (map, network, barnacles, rent);
- in-group jargon and undefined terms ("the Way", "update", "epistemics", "Fully
  General Counterargument");
- fragments, chat abbreviations, slashes, scare quotes that argue by typography;
- grammar and typos in the original (point them out; never fix them in the text).

Logic (be the skeptic):
- Does the example illustrate the claim, or a different claim?
- Is a claim stated as fact without support? Is a statistic invented ("perhaps 5%")?
- Does the claim silently shift (from "not overconfident" to "less overconfident than
  average"; from "hard to beat the market" to "hard to make money")?
- Is something true by definition dressed as a finding (the PR post defines honor as
  good and PR as bad, then concludes honor is better)?
- Does the essay apply its own test to itself? ("Twelve Virtues" fails its own sixth
  virtue.)
- Do the parts contradict each other (lightness vs precision; humility vs
  perfectionism)?
- What is the unstated assumption? ("Humans are not automatically strategic" assumes
  stated goals are real goals.)
- Who does the argument flatter, and who does it make the villain? (The literature
  professor in "Making Beliefs Pay Rent"; readers who think themselves exceptional in
  "Strong Evidence is Common".)
- Is an old idea presented as new without credit (Peirce, Popper, Occam, Korzybski)?

Words: look contested words up in a dictionary and quote it. The author may be
redefining a word to suit the argument. The humility case is the model: Merriam-Webster
gives "freedom from pride or arrogance"; the essay gives "take specific actions in
anticipation of your own errors", which is prudence. I first praised that definition as
the best in the text. That was a serious error, caught by the user.

Facts: check every number and every attribution. Recompute arithmetic yourself (the
Mark Xu post needs 99:1, not 200:1). Check quotations in the original language when you
can (Saint-Exupéry's "Il semble que..." drops a hedge in translation).

### 5.3 The essay (Summary and Response, in `afterwords/`)

Summary: plain prose, about 150 words, no judgment. What it argues, how, what it
concludes.

Response: about 300 to 450 words, ending with one line beginning "In short:". Ask:
- What is the piece doing, as distinct from what it says? (Forming an identity,
  recruiting, flattering its audience, defending a community under criticism, giving
  the reader a weapon to use on others.)
- What is its structure, and is it the right one? (Verdict before definitions;
  thesis two-thirds of the way in; best idea in a footnote.)
- Where is it strongest, stated in one sentence, and where does that strength stop?
- What would a careful critic of the essay's own position say?
- Is its central claim true as written? If the author corrected it elsewhere, say so
  and say which version readers actually meet.
- What context changes how it should be read (date, what happened the day before,
  what the author went on to sell or found)? Mark inferences as inferences.

Do not grade on the author's reputation, and do not soften a verdict because some
sentences are good. One sentence of credit is enough when credit is due.

After the third round of "not critical enough", these patterns were purged. Do not
write them:
- credit phrases in notes: "does its job", "a good move", "the essay at its best",
  "lands well", "a good close", "sound advice", "the best paragraph";
- charitable repairs: supplying the argument the author did not give ("Perhaps
  because people pick moderate ratios by habit"). If the author gave no reason, say
  there is none. Do not invent one for them;
- "the point survives" when an error happens to favor the author. Say what was wrong.

And look for these, which the first passes missed:
- invented examples presented as typical (Wulky Wilkinsen does not exist; the
  comedian is someone else's "somewhat silly" hypothetical);
- whether the author applies the rule to himself (the rent test would evict his own
  many-worlds belief, argued in 2008 on simplicity, not on different predictions);
- whether a text about giving up beliefs ever gives one up;
- whether the recommended fix is itself the thing criticized ("reputation
management" is the PR industry's own name for its service).

## 6. Verification rules (non-negotiable)

- Never quote from memory. Every quotation, from the post or from anyone else, must be
  checked against a source you have actually read in this session.
- After writing a Response, check that each quoted phrase from the post occurs in the
  original. A misquote was caught this way ("glimpsed" for "glimpse the center").
- Count before you claim a count ("the Way" appears 6 times, "Art" 2 times; I first
  wrote 3 for "Art").
- If you cannot reach a primary source (web.archive.org is blocked from this
  environment), say so in `../docs/NOTES.md` and tell the user. Do not present a
  secondhand quotation as checked.
- Satire is not a source. A 2015 LessWrong post with the "only one who can make the
  effort" line is a parody; the real source is Yudkowsky's autobiography, archived at
  https://web.archive.org/web/20010205221413/http://sysopmind.com/eliezer.html#timeline_birth
  (the user checked it). Where an author has disowned early work, say so; see the humility note in
  "Twelve Virtues" for how.
- Mark every inference as an inference in the text itself.

## 7. House style for your own notes and Responses

The user's rules, which apply to everything you write here:
- plain English, short sentences, one point per sentence, no academese;
- no italics in your own text (book titles go in small caps, `\textsc{...}`);
- avoid em dashes; split the sentence instead;
- no "it's not X, it's Y" constructions; no signposting ("The key point is...");
- no intensifiers ("clearly", "notably", "importantly");
- make each point once. If a paragraph note and a local note would say the same
  thing, keep one. (After the first paragraph pass, about ten duplicates had to be removed.)
- they/them for anyone whose pronouns are not stated, including generic readers.

## 8. Checklist before sending a new PDF

1. `check_verbatim.py` prints OK for every post.
2. Every substantial paragraph has a `\cpara` note, and every note is a judgment.
3. No praise-only notes anywhere (`grep -n 'best\|good\|clear example' posts/*.tex`
   and read each hit).
4. No point is made twice across note levels, or between the notes and the Response.
5. Every quotation checked against a source read this session; every inference marked.
6. Build has no errors; overfull boxes under 1pt are acceptable.
7. Look at the rendered pages (`pdftoppm -r 70 -png`), not only the log.
8. Log what you did and any mistakes in `../docs/NOTES.md`. Commit only committable
   files; push.
