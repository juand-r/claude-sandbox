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

## Batch 2b: rest of Book II (33 posts)

Nine agents (Seeing with Fresh Eyes, Death Spirals, Letting Go). Edits in
`docs/raz/changes/batch02b.md`. The kinds were the usual ones, with more fair-defender
failures than in earlier batches:

- Critiques that a fair reading answers, cut or recast as scope or credit:
  - Leave a Line of Retreat: the metaethical reading of "without God, morality is impossible".
  - Hold Off: "determined only by" (a revision is a new decision).
  - On Expressing: Asch "could not show" pluralistic ignorance (the post says "possibility raised"); the Prince note (the book does advise dissembling).
  - Unbounded Scales: "completely unpredictable" (6 per cent explained in dollars).
  - When None Dare: "can only rise" (the law is conditional).
  - Resist: Bacon's conditional timetable, and a speculative argument against Armstrong's advice.
  - Crackpot Offer: the hindsight rule (the post's scope is after the mistake).
  - Halo Effect: Thorndike now credited as support, not held against the post.
  - Evaporative Cooling: the selection arithmetic is the post's idea, not a flaw.
- Source check that reversed a note: the Epley and Gilovich abstract describes "a consensus
  that none [adjustment] takes place seems to be emerging", so Priming's "most anchoring is
  contamination" matches its source.
- Guilt by association cut: Wansink's later misconduct (other work) in Priming.
- Nitpicks cut: isshokenmei gloss (Crisis of Faith), opposite temperature metaphors (Every
  Cause), ten-of-twelve quadrants (Affect Heuristic, under the number threshold), dictionary
  significance (Evaluability), the author's memory of 9/11 (When None Dare), the Finney
  revision in the Response (Genetic Fallacy).
- Point made once: the half second (We Change, with a pointer from Hold Off); the Eagly
  point (Halo Effect, with a pointer from Superhero Bias); the Aumann common prior (stated in
  Asch, applied in On Expressing); the desertion effect (Asch, pointer from On Expressing).

Considered and left: Lonely Dissent and Asch's Conformity Experiment both give Asch's
independence figures. In Asch they are context; in Lonely Dissent they answer the post's
"experiment shows", so both keep them.

Unverified, as the agents report: Maier's and Dawes's results (Hold Off), Yamagishi from
summaries only (Affect Heuristic), the Unarius date and the unnamed member of Congress (When
None Dare, Evaporative Cooling), von Sydow (No One Can Exempt You).

Tooling: do-we-believe-everything-we-re-told needed a hand fix of the skeleton. The source
text itself marks footnote 3 as `[2](#footnote2)`, so md2tex left footnote 3 as a stray
paragraph. No other original has this pattern, and the verbatim check caught it, so md2tex
is unchanged.

Layout, for the whole-book pass: new bare-URL overfull boxes, all in the posts' own
footnotes: Stranger Than History (144pt), Every Cause (119pt, 116pt), Crisis of Faith
(132pt, 41pt), Generalization from Fictional Evidence (35pt), On Expressing (24pt). Same fix
as above (md2tex wrapping URLs in \url{}).

## Batch 3a: The Simple Math of Evolution, Fragile Purposes (24 posts)

Eight agents. Edits in `docs/raz/changes/batch03a.md`. Kinds, with examples:

- Critiques a fair reading answers, cut or recast:
  - Artificial Addition: the parable's evolved arithmetic against "Until you know your idea
    will work, it won't" (the rule is for designers in a human lifetime).
  - Fake Optimization Criteria: "inclusive genetic fitness" called loose (it is gene-level,
    and transposons maximize it); "two selections at once" in Wade's beetles.
  - Tragedy of Group Selectionism: "magical thinking" against "possible but very difficult".
  - Anthropomorphic Optimism: a hedge carried into the next paragraph; AI as "subtext".
  - Adaptation-Executers: the slogan placed in a methods debate the post does not enter.
  - Wonder of Evolution: evolutionary algorithms recast as tools inside human design, not a
    counterexample; the paragraph's own "Almost certainly" governs its first sentence.
  - Humans in Funny Suits: the natural-selection example now described by what it shows.
  - Minds: An Introduction: preface convention (no charge of citing no opponents).
- Nitpicks cut: quine jargon, Vinge not named, a novel's plot, a dropped hedge between two
  posts, a correlation slip and a stipulated number removed from a verdict, a physics joke's
  threshold (kept as a margin note), a citation typo in a Response, revision trivia, and
  complaints about the book's selection or order (the editors' choice, not the author's).
- Points made once, with pointers:
  - Group selection (Wade's four traits, Wynne-Edwards's own account, cannibalism known in
    Allee's and Park's work, no biologist quoted): The Tragedy of Group Selectionism.
  - Mayr's ultimate and proximate causes: Adaptation-Executers.
  - Utilities as a sum of parts: moved from Terminal Values to Leaky Generalizations, where
    the author's stated view depends on it.
  - The retina: An Alien God.
- Two Responses are short (Adaptation-Executers 185 words, Evolutionary Psychology 203)
  because little criticism survived; that is intended.

Unverified, as the agents report: Crawford, Salter and Jang (1989) itself (Wright's summary
and a commenter only; the post's N=221 against the commenter's 436); Wade (1976) beyond the
abstract; George Williams quotations; the gnxp simulation; the Soviet shoe stories; the
Perry Metzger epigraph; Cynthia Kenyon's dinner remark; Funk's closing line (not in the
downloadable text).

Tooling:
- check_verbatim now strips list markers only in blocks that start as a list, as md2tex
  does (a hard-wrapped "- " inside a paragraph is text). All posts pass.
- md2tex drops horizontal rules inside quotes, as it already did at top level (only Ghosts
  in the Machine has them).
- Process: my mid-batch notes export caught agents' half-written files. From now on I
  export only finished slugs until the batch ends.

## Batch 3b: A Human's Guide to Words (26 posts)

Eight agents. Edits in `docs/raz/changes/batch03b.md`. Kinds, with examples:

- Critiques a fair reading answers, cut or recast:
  - Entropy and Short Codes: "probability" in two senses (the post juxtaposes MML and word
    length but does not equate them); "not quite arbitrary" (the post means length).
  - Variable Question Fallacies: Martin/Bob as mere pronoun ambiguity ("left" needs a person
    as parameter, and the pronoun leaves it open).
  - Superexponential Conceptspace: "wiggin" not needing the superexponential count.
  - Disputing Definitions: the "expert botanists" question (the post's objection is that the
    dictionary records both senses and cannot choose).
  - Replace the Symbol: the school picture (hedged illustration, not a verdict).
  - Sneaking in Connotations: the In short line had dropped the thesis's "generally".
  - Common Usage and Arguing by Definition: law as scope, stated once, out of the verdict.
- Nitpicks cut: loose wording notes, style notes (metaphors, repetition), an unexplained
  aside, "shows no example" where the next posts do, a blood-type side remark, the
  "rationalist" name of the method, a loose generalization about Greek philosophers, and
  "syllogisms are valid".
- Points made once, with pointers:
  - Mill on the syllogism: The Parable of Hemlock; Empty Labels points back.
  - Diogenes' plucked chicken: Similarity Clusters; Arguing by Definition points back.
  - Wittgenstein's family resemblance: Similarity Clusters; Cluster Structure points back.
  - Design argument without evidence about brains: Neural Categories (first in book order).
  - William James: the rule in Disguised Queries, the squirrel story in Disputing
    Definitions, cross-referenced.
  - Law and definitions: Arguing by Definition.

Checked and kept: the "nine examples" in Superexponential Conceptspace (about 15 by
simulation; the growth claim survives); the sign of a weight in Neural Categories (by
simulation; the point survives); Hopfield's convergence proof against "oscillating or
chaotic"; The Simple Truth's use of "believe" (54 times) against "without invoking";
the reworded opening quotation in Where to Draw the Boundary; 29384209 = 1667 x 17627.

For the whole-book pass (already-annotated posts from the original edition):
- Taboo Your Words: its Mill note should point to The Parable of Hemlock, and its word
  "rigged" for Empty Labels' demonstration should be reviewed (Empty Labels states its
  definition openly).
- How an Algorithm Feels From Inside: its "no evidence about brains" point and its
  "oscillating or chaotic" remark should point to Neural Categories.
- Layout: new overfull box of 39pt in Feel the Meaning (the post's own pseudo-code line).
