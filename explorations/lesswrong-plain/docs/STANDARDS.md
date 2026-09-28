# Standards for Rationality: A–Z (annotated and honest editions)

Written 28 September 2026, before extending the project from 52 posts to all 338 posts of
*Rationality: A–Z*. This file is the specification. Every agent reads it in full before
writing anything, and the editor (the main session) checks every post against it.

It gathers, in one place, what the user asked for over four review rounds. Where it
conflicts with an older file, this file wins:

- `annotated/README.md` section 1 ("the harshest reading") and its calibration table are
  **superseded** by section 2 below. Some rows of that table were later judged unfair
  (for example "The essay's content ends here"). Its sections 2 to 4 (files, layout,
  verbatim rule) still apply.
- `docs/STYLE.md` still applies in full to the honest edition (its "Rules for my own
  prose", "Checklist", "Rules of thumb" and "Final review checklist").
- `docs/THIRD_PASS.md` and `docs/FOURTH_PASS.md` are summarized in section 2.3.

## 1. What each post gets

For a post with slug `<slug>` (the file name of `data/originals/<slug>.md`):

| File | Content | Committed? |
|---|---|---|
| `annotated/posts/<slug>.tex` | the post verbatim, with margin notes | no (post text); notes via `annotated/notes/<slug>.json` |
| `annotated/afterwords/<slug>.tex` | Summary and Response | yes |
| `honest/sections/<slug>.tex` | the post retold in the author's voice, with `\nb{}` notes | yes |
| `docs/raz/reports/<slug>.md` | the agent's working report (section 6) | yes |

Models to imitate (read them before writing): annotated and honest versions of
`the-lens-that-sees-its-flaws`, `use-the-try-harder-luke`, `the-bottom-line`,
`positive-bias-look-into-the-dark`, `something-to-protect`. These are the corrected
versions after four review rounds.

## 2. The critical standard

### 2.1 Stance

Critical, exact and fair. The aim is the strongest criticism that is true.

- Judge the text on the page. The author's fame, the post's status and its later
  influence earn nothing.
- Say plainly where a claim has no support, an example does not show what it is said to
  show, an old idea is presented as new, or the author breaks a rule the post sets.
- Credit is allowed where leaving it out would mislead, briefly. A post that gets
  something right should not be made to look as if it did not.
- Where a paragraph gives no ground for fair criticism, its `\cpara` note plainly
  describes what the paragraph does ("Gives the second example: ..."). Do not invent a
  fault to fill the margin.

### 2.2 The fair-defender test (every note, every Response sentence, every n.b.)

Imagine the author, or a careful friend of the author, reading the note. The note fails
if any of these replies is correct:

1. "That is not what I said." Quote the exact sentence you criticize, and check that your
   evidence contradicts that sentence, not a paraphrase of it.
2. "I said probably." **Keep every hedge** ("probably", "perhaps", "I suspect", "seems",
   "as far as I know", "I have heard of", "on average"). A hedged claim is attacked as
   hedged: "offered with 'probably' and no evidence", never as an absolute.
3. "That was a joke / a figure of speech / a hypothetical." A hypothetical ("say, Lord
   Kelvin") is not a factual claim. A flagged invention is not a deception.
4. "Any essay does that." Using an anecdote, an invented example, a short form, not
   citing a standard source for a commonplace: not faults.
5. "I answer that two paragraphs later" or "in my last paragraph." Read the whole post
   before writing "never", "does not answer", "only", "no example".
6. "You read my term against its meaning here." Read technical and coined terms in the
   sense the post uses ("novel prediction" is a term of art; "can't help" means "gives
   no verdict in time", not "gives a wrong verdict").
7. "That is your guess about my motives." No readings of motive, purpose or effect on the
   reader ("exists to flatter", "the reader is invited to feel superior", "the rule is
   for everyone else") unless the text itself supports it, and then marked "My reading:"
   or "I infer". When in doubt, cut it. Jabs at readers or the community are cut.

### 2.3 Words reserved for the strongest evidence

"False", "wrong", "refutes", "contradicts", "the opposite", "backwards", "never",
"cannot fail", "unfalsifiable", "invented", "misquotes", "rigged" may be used only when
the evidence meets that exact word. Otherwise use the accurate weaker word:
"overstated", "sits uneasily with", "unsupported", "loosely worded", "not shown",
"hedged but unsupported", "could not source".

Before writing "contradicts", check both passages again. Before writing "misquotes",
check whether the difference changes the meaning; a dropped plural is not worth a note.

### 2.4 What is always cut (THIRD_PASS rules)

A note is removed when it (1) takes a joke or figure of speech literally; (2) nitpicks
wording, names, typos or an editor's slip with no consequence for the argument; (3) reads
motives with no textual basis; (4) faults the post for what any short essay does;
(5) rests on a contrived or speculative objection; (6) repeats a point already made in
another note or in the Response.

### 2.5 Consistency

- Within a post: no two notes may contradict each other (for example "never answers the
  objection" followed by "the answer to the objection is ..."). Read all notes of a post
  in sequence at the end.
- Between the editions: the annotated notes, the Response and the honest n.b. notes must
  agree on every fact and every judgment. If one is corrected, correct the others.
- Across posts: a statement about another post ("two days later the author wrote ...")
  must match that post's original in `data/originals/`, and must agree with what our
  notes on that post say. A recurring criticism (for example, many-worlds held on
  simplicity; Popper uncredited) is made in full once, where it matters most, and
  elsewhere at most briefly with a pointer.
- Dates: use the `Posted:` line of `data/originals/<slug>.md`. Do not compute "two
  days later" from memory.

### 2.6 Pronouns

Never infer anyone's pronouns from a name. For post authors (Yudkowsky, Bensinger and
any other), write "the author", "the post", "Yudkowsky", or restructure. Characters
inside a post keep the pronouns the post uses. Historical figures with well-documented
pronouns may keep them.

## 3. Verification (non-negotiable)

1. Every quotation from the post is checked against `data/originals/<slug>.md`, word for
   word, including punctuation and hedges. Truncating a sentence at a point that changes
   its meaning is a misquotation; show omissions with `\ldots`.
2. Every quotation or figure from anything else is checked against a source you have
   read in this session (fetched page, PDF, or the original of another post). Record the
   URL and the exact matched words in your report. If you cannot reach the source,
   either drop the claim or say in the note that you could not check it. Never quote
   from memory. Secondary summaries (Wikipedia) may be cited as such.
3. Recompute every number and every piece of arithmetic in the post that a note relies
   on, and show the computation in your report.
4. Physics, mathematics and statistics: a note that says the post is technically wrong
   must be right, and must be checkable from a cited source or a shown derivation. If
   you are not sure, do not assert it. Say what is unsupported instead.
5. Counts ("three examples", "the fourth paragraph") are counted, not estimated.

## 4. The annotated edition

Mechanics: `annotated/README.md` sections 2 to 4 and 5.2 (checklists for style, logic,
words and facts). In short:

- Start from the skeleton made by `src/md2tex.py`; copy it to `annotated/posts/<slug>.tex`.
  Insert notes only. Change no character of the post text.
- `\cpara{...}` at the start of every substantial paragraph (the audit counts them).
  Sentence-level notes: `\clogic{}`, `\cfact{}`, `\cstyle{}`, `\ccut{}`, placed right
  after the words they discuss. `\cauthor{}` holds the post's own footnotes; do not
  touch it.
- Notes are short: one to four sentences. One point per note.
- After every edit: `.venv/bin/python src/check_verbatim.py annotated/posts/<slug>.tex data/originals/<slug>.md` must print OK.
- Afterword (`annotated/afterwords/<slug>.tex`), using the existing format
  (`\begin{afterword} \summaryhead ... \responsehead ... \end{afterword}`):
  - Summary: about 150 words (more for very long posts), plain, no judgment.
  - Response: about 250 to 450 words, organized by argument, ending with one line that
    begins "In short:". The "In short" line must pass the fair-defender test like any
    other sentence. It restates the Response; it adds no new charge.
  - The Response may not raise a charge that the notes do not support, and may not
    repeat a charge the notes have cut.

## 5. The honest edition

Rules: `docs/STYLE.md` (all of it). In short:

- `\honest{<Title>}{<Author>}{<Year>}` then paragraphs. The author speaks in the first
  person and retells the post from start to finish, stating plainly what each part does.
- Two voices. Outside `\nb{}`: only things the author says, or ironic lines the author
  could plausibly say about the post ("I give no example"). Inside `\nb{}`: the editor's
  corrections, outside facts and judgments, in the third person ("Yudkowsky had
  written"). A sentence that reads as an outsider judging the post goes in an n.b.
- Quotes are the author's exact words, checked. Keep the post's key terms.
- No bare verdicts ("This is sensible"). Name what you refer to (titles, names).
- Length: about 150 to 500 words; up to about 900 for very long posts.
- Every n.b. must agree with the annotated notes and Response (section 2.5), and must
  pass the fair-defender test.

## 6. The agent's report (`docs/raz/reports/<slug>.md`)

For each post, the agent writes:

1. The post's argument in three sentences (written before annotating).
2. Sources checked: for each outside quotation or figure, the URL or file and the exact
   words matched.
3. Arithmetic recomputed, with the working.
4. Claims about other posts, with the file and the matched words.
5. Items not verified, and what would be needed.
6. Judgment calls the editor should look at: any note using a word from section 2.3,
   any "My reading" inference, any place the agent was unsure.

## 7. Checks before a post is handed in

Run in this order; the post is not done until all pass.

1. `check_verbatim.py` prints OK.
2. `src/audit.py <slug>`: every substantial paragraph has a `\cpara`; Summary, Response
   and "In short:" present. Read each praise-word flag.
3. `annotated/preview.sh posts <slug>` builds without errors.
4. Quote check: every ``...'' quotation attributed to the post, in the notes, afterword
   and honest section, occurs in the original (after normalizing quotes and dashes).
5. Reread every note, the Response and every n.b. once for each rule in section 2.2,
   then once for section 2.3's words, then once for pronouns, em dashes and italics.
6. Write the report (section 6).

## 8. The editor's final pass (main session)

For every post, in book order: read the original, then the annotated notes and
afterword, then the honest section. Check the fair-defender test, the reserved words,
consistency with the other edition and with neighbouring posts, and the agent's report
(spot-check its sources). Every change is made with a logged, exact replacement
(before and after) in `docs/raz/changes/<batch>.md`. Findings that need the user's
decision go in `docs/raz/review_log.md`.
