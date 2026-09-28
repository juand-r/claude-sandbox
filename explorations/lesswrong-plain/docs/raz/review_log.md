# Review log: Rationality: A–Z

## Pilot: Predictably Wrong (9 posts), 28 September 2026

Drafted by 3 agents (3 posts each) from `docs/raz/AGENT_BRIEF.md`. Editor's final pass:
original, then annotated notes and afterword, then honest section, then the agent's report.
Every edit is in `docs/raz/changes/pilot.md`.

### What the editor changed

| Post | Change | Rule |
|---|---|---|
| planning-fallacy | "takes the first three paragraphs out of the evidence" → "cannot show the bias on their own" (note and honest) | the post says other causes as well as the bias |
| planning-fallacy | In short: names the one source checked (the 1994 paper) | the outsider claim may come from an unread chapter |
| why-truth | honest n.b. on Xenophanes made conditional, as the note is | consistency |
| feeling-rational | cut "curiosity is not mentioned again" and "the distinction is not used again" (note, Response, honest) | fair defender: the general answer covers curiosity; nitpick |
| availability | cut "twice is loose" | "Actually" states the real ratio, which is about two |
| availability | cut the unsourced "editors cover what readers fear" alternative | speculative objection |
| what-s-a-bias | cut the notes comparing the post with its 2006 version; one neutral note explains the anachronism | ruling: annotate the current text |
| burdensome-details | cut "states the explanation more firmly than Conjunction Controversy" | the quoted "does not prove" referred to one study |
| preface | CFAR parenthesis moved to the mistake it belongs to (honest); cut "no evidence" for praise of readers | placement; any preface does that |
| biases-an-introduction | cut "no example that more data can worsen a biased prediction" | nitpick |
| scope-insensitivity | honest n.b.s: say where the quotation was checked; report both replication results | consistency with the notes |

About 12 of roughly 200 notes and 45 n.b. notes needed a change. No factual error was found
in what remained; each agent's report lists what could not be verified (mostly paywalled
primary sources).

### What the standards gained from the pilot

Added to `docs/STANDARDS.md`: fair-defender tests 7 (other posts quoted out of context) and
8 ("actually" claims); cut rule for unsourced alternatives and preface conventions; a
threshold for number notes; the current-text rule; tool warnings (WebFetch is not verbatim;
search results echo the post); a shared, uncommitted `data/sources/`; footnote paragraphs;
prefaces; honest length unified at 150 to 500 words; three pilot posts added as models.
`annotated/README.md` 5.1 and 5.3 marked superseded where they conflict. Preamble: amsmath,
and superscript digits used as footnote markers.

### Open questions for the user

None blocking. For the whole-book pass: the original 52 posts are harsher in places than
the new standard (for example "mind-reading", "only decoration" in The Lens That Sees Its
Flaws). Bringing them in line is planned for the last step.

## Batch 1: rest of Book I (25 posts), 28 September 2026

Eight agents. Every edit in `docs/raz/changes/batch01.md`. About 20 edits across the
25 posts, of the same kinds as in the pilot: claims stronger than the evidence ("reaches
none of them", "does not fit", "a different fault"), a doubt from one secondary source
repeated in three places, a naming point promoted to the verdict, one fable faulted for its
example. No factual error was found in what remained.

Corrections to earlier posts found by the batch (all checked, all logged):
- When Science Can't Help: "refused to describe it at all" (My Wild and Reckless Youth gives
  the prediction); Tegmark's 2000 calculation was disputed the same year (arXiv
  quant-ph/0005025); a "he" for the author.
- Say Not Complexity: "never defined" was wrong (the term is glossed in the sentence and
  introduced in Fake Causality).
- Making Beliefs Pay Rent: a pointer to a cut note now points to the phlogiston history in
  Fake Causality.

Tooling: md2tex link-text crash fixed (all earlier skeletons unchanged). Honest title line
broken in two (it was the old overfull box on the title page).

Known layout issue, not fixed: two bare URLs in the posts' own footnotes (Pretending to be
Wise, Truly Part of You) run about 100pt into the margin. They are verbatim post text;
a fix would be to have md2tex wrap bare URLs in \url{}, which changes skeletons and needs a
notes re-export. Left for the whole-book pass.

For the whole-book pass: Einstein's Arrogance now carries the full Peirce point, so the
Faster Than Science note can become a pointer; The Futility of Emergence and Say Not
Complexity both make the "unnamed crowds" point; the density of \cpara notes on the
dialogue lines of The Simple Truth (149) is high.

## Batch 2a: first half of Book II (33 posts)

For the whole-book pass: The Proper Use of Humility (order 52) now carries the full
dictionary point on humility; the Twelve Virtues note (order 297) should become a pointer
back, and its biographical and "AGI Ruin" material should be reviewed against STANDARDS 2.2
test 9 (motive readings).

Nine agents. Edits in `docs/raz/changes/batch02a.md`: about 25, of the usual kinds
(nitpicks cut: a missing sequence in a list, a misdated footnote, an unexplained example
ranking, "Trained by whom?"; slips moved out of verdicts: a citation, an arithmetic slip;
claims made conditional where a fair reading exists: "lie", the axioms "rule out"). One
correction of my own cut: the Persepolis point in No, Really, I've Deceived Myself is a
factual correction and was restored.

Tooling: md2tex now keeps multi-paragraph footnotes together (2+2=3, What Evidence
Filtered Evidence?); preamble gained U+2215 and U+2661. All earlier backups unchanged.

For the whole-book pass: The Fallacy of Gray's note on the lottery man can become a
pointer to But There's Still A Chance, Right? (earlier in book order, now carries the full
point); Belief as Attire's hijacker note could mention the bin Laden evidence given in Are
Your Enemies Innately Evil?; Twelve Virtues' humility note (see above). Layout: overfull
boxes of 45pt (URL in the Book II introduction's footnote) and 8pt, both post text.
