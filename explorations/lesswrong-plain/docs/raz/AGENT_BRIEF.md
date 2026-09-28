# Brief for an annotating agent (Rationality: A–Z)

You annotate a few LessWrong posts in two editions, to the standard of the 52 posts already
done. The editor (the main session) will review every line you write, so precision matters
more than volume. Work in `/home/user/claude-sandbox/explorations/lesswrong-plain`.
Use `.venv/bin/python` for every script.

## Before you start (required reading, in this order)

1. `docs/STANDARDS.md`, all of it. It is the specification. Section 2 (fair-defender test,
   hedges, reserved words) is where earlier work failed most often.
2. `docs/STYLE.md`, all of it (the honest edition's rules and checklists).
3. `annotated/README.md` sections 2 to 5 (files, layout, verbatim rule, how to read).
   Its section 1 is superseded by STANDARDS.md.
4. The model posts, all three files each:
   `annotated/posts/<m>.tex`, `annotated/afterwords/<m>.tex`, `honest/sections/<m>.tex`
   for every model listed in STANDARDS section 1 (five from the original edition, three
   from the pilot). Where a model is harsher than STANDARDS section 2, STANDARDS wins.
   Note their density: a `\cpara` on every substantial paragraph,
   a few sentence notes, a Response of 250 to 450 words, an honest section of 150 to 500
   words with a handful of n.b. notes.
5. Your posts' originals: `data/originals/<slug>.md`. Read each post twice before writing.
   Also read `data/manifests/rationality_az.json` for each post's place in the book
   (book, sequence, neighbours): posts often refer to the previous day's post, which is
   also in `data/originals/`.

## For each slug assigned to you

1. `.venv/bin/python src/new_post.py <slug>` creates `annotated/posts/<slug>.tex` (verbatim
   skeleton). Insert notes only. Never change the post text. Plain-text footnote markers
   in the skeleton (a digit glued to a word, like `\$88.1`) are the post's own markers;
   leave them.
2. Write `docs/raz/reports/<slug>.md` section 1 (the argument in three sentences) first.
3. Annotate (STANDARDS section 4), then write `annotated/afterwords/<slug>.tex` (copy the
   format of a model afterword exactly: `\begin{afterword}`, `\summaryhead`, Summary,
   `\responsehead`, Response ending "In short: ...", `\end{afterword}`).
4. Write `honest/sections/<slug>.tex` (STANDARDS section 5; first line
   `\honest{<Title>}{<Author>}{<Year>}` with the title as in the manifest, LaTeX-escaped).
5. Verify (STANDARDS section 3). Web access works through the proxy (WebFetch, WebSearch,
   or curl). LessWrong pages: `https://www.lesswrong.com/posts/<id>/<slug>`. If a source
   cannot be reached, drop the claim or say in the note that it could not be checked.
6. Run `.venv/bin/python src/raz_check.py <slug>`. Fix every failure. Read every flag:
   - "quote not in post": either correct the quote, or it is from another source and
     your report must show where you checked it.
   - "reserved": confirm the evidence meets the word (STANDARDS 2.3), else weaken it.
   - "pronoun": a post author must not get he/his/she/her; characters keep theirs.
   - "motive?": keep only if the text supports it and it is marked as inference.
7. `annotated/preview.sh posts <slug>` must build (it prints the PDF path; errors print
   the LaTeX error).
8. Finish the report (STANDARDS section 6). Be candid about doubts; the editor would
   rather see a doubt than find an error.

## Rules that are easy to break

- Keep the author's hedges when you quote or paraphrase. "I suspect X" is not "X".
- Before "never", "does not answer", "no example": search the whole post for it.
- Claims about the author's other posts: open that post in `data/originals/` and quote it.
- No motive readings, no jabs at readers or the community.
- One point per note; do not repeat a point between notes, or between notes and Response,
  except that the Response may restate the main points in its own summary form.
- No em dashes (—, ---) and no italics in your own text; book titles in `\textsc{}`.
  Plain English, short sentences. No "notably", "importantly", "clearly".
- Pronouns: never he/his/she/her for a post's author.

## Lessons from the pilot

- Check an "actually" claim against real figures, not only against the cited study.
- An alternative explanation you cannot source is not a note.
- When you quote another post's hedge, read what the hedge was about.
- WebFetch is not verbatim; use curl for exact words. Save sources in `data/sources/`.
- Math in notes: the preamble has amsmath, but prefer `\mbox{}` to `\text{}`.
- Your scratch files go in `data/sources/` or your own temporary directory, not the
  main session's scratchpad.

## Do not

- Do not edit any file other than the ones for your assigned slugs, and your reports.
- Do not commit, push, or touch git.
- Do not edit `docs/STANDARDS.md`, the models, or other posts. If you find a problem with
  them, write it in your report.

## When done

Reply with: for each slug, the raz_check summary line (verbatim, paragraphs, notes,
summary/response words, honest words), the preview build result, and the list of
"judgment calls" from your report. Keep the reply short; the details are in the report.
