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

## Batch 4a: Lawful Truth, Reductionism 101, Joy in the Merely Real (31 posts)

Eight agents. Edits in `docs/raz/changes/batch04a.md`. Kinds, with examples:

- Critiques a fair reading answers, cut or recast:
  - The World: An Introduction: Nagel "declined that conclusion" (the introduction never
    says Nagel drew it); "popular" versus minority polls (not a contradiction).
  - Explaining vs. Explaining Away: the reading of Keats's "unweave a rainbow" (the poem
    supports it; its second complaint, commonness, is answered in the next post).
  - Bind Yourself to Reality: "emotional energy" undefined (a metaphor offered as advice).
  - Amazing Breakthrough Day: readers will disbelieve April 1st stories (the annotator's own
    reading of how the proposal would work).
  - Universal Fire: "sole credit" to Lavoisier (the post names no one else, denies no one).
  - Perpetual Motion Beliefs: a pointer added to the author's case for simplicity priors.
- Nitpicks cut: a joke about one-eyed depth taken literally, a wording note on protein
  folding, provably equivalent statements called "distinct", the inverted-map point on
  mutual information, a reader-test note, trivia about the book's contents and the origin of
  a verse, the book's placement of a post.
- Scope kept to one sentence and out of the verdict: organized humanism (Is Humanism a
  Religion-Substitute?), multiple realizability (Reductionism).
- Points made once, with pointers: the Dumas-Mallet evidence on science news (The Beauty of
  Settled Science); the positions called anti-reductionist (Reductionism); Jaynes on
  thermodynamics (The Second Law post, from the original edition).

Checked and kept: the stopping-rule numbers in Beautiful Probability (by script); the
two-elevenths puzzle in Initiation Ceremony (by script); Haydon's two versions of the Keats
toast; Tegmark's levels in Joy in Discovery; Cialdini's own account against Scarcity's
"malfunction".

Tooling: preamble gained U+2208 (element of) and U+221E (infinity) for Qualitatively
Confused.

Layout, for the whole-book pass: the Book IV introduction adds two bare-URL overfull boxes
(42pt and 147pt) from its own footnotes. There are now thirteen such boxes, all verbatim
post text; the md2tex \url{} fix is due in the whole-book pass.

For the whole-book pass: The Second Law of Thermodynamics (original edition) is the target
of two new pointers (Jaynes's view of heat; Bennett on the cost of observing).

## Batch 4b: Physicalism 201 (15 posts)

Six agents. Edits in `docs/raz/changes/batch04b.md`. Kinds, with examples:

- Critiques a fair reading answers, cut or recast:
  - Excluding the Supernatural: "the corollary does not follow as stated" ("respectful
    tones" is defined by its link); the real weakness, a verdict on unnamed designers with
    no case, replaces it.
  - Reductive Reference: "credited only through Twin Earth" (the post cites Twin Earth and
    the debate).
  - Belief in the Implied Invisible: "central point made before" softened to "a similar
    point", on one Tegmark sentence.
  - When Anthropomorphism Became Stupid: the Aristotle corrections kept in the Response but
    out of the verdict, since the post hedges its history.
- The annotator's own unsourced arguments cut: which worlds reliability is measured over
  (Zombie Responses); a later (2018) reply the post could not answer (Excluding the
  Supernatural).
- Nitpicks cut: the gloss of neshamah, "a priori" in two consistent senses, a practical
  reason for moving on, an unused irony about Golgi.
- Points made once: Chalmers does not call his view epiphenomenalism (Zombies! Zombies?,
  with a pointer from Zombie Responses, which adds Chalmers's 2008 comment); Carrier's
  definition (Uncritical Supercriticality); Putnam and Kripke on heat (Heat vs. Motion).

Checked and kept: the Chalmers quotations throughout (against The Conscious Mind and his
papers); Chalmers's 2018 citation of Zombies! Zombies? and his concession on coincidence;
Block's lookup table (via McDermott, since Block's PDF was blocked); the ganzfeld
meta-analyses in Psychic Powers; the horizon physics in Implied Invisible; the switch
arithmetic in GAZP.

Process: one agent's retry against the Wikipedia API sent a User-Agent string containing
the user's email address; the request was refused. The address is in no file in the
repository. The brief now forbids putting personal data in request headers.

## Batch 4c: Quantum Physics and Many Worlds (14 posts)

Eight agents. Edits in `docs/raz/changes/batch04c.md`.

- The full assessment of the many-worlds case is in Many Worlds, One Best Guess: two
  premises (other worlds as a "logical consequence" of the laws, which needs the wavefunction
  to be all there is, with Bohm as the counterexample; a single world "would violate
  relativity", where nonlocality is granted and violation is disputed), the Born rule, and
  the post's closing account of dissent as sentiment, ignorance and fear. The decoherence
  posts, Privileging, Living in Many Worlds, and earlier notes (Making Beliefs Pay Rent,
  Think Like Reality, Is Reality Ugly, Joy in Discovery) point there.
- Points made once: amplitudes and QBism or Pusey--Barrett--Rudolph (Configurations and
  Amplitude; Joint and Distinct Configurations point back); "decoherence" used as a name for
  many-worlds (Decoherence is Simple); von Neumann and the founders' treatment of measurement
  (Collapse Postulates and Distinct Configurations; If Many Worlds Had Come First points
  back).
- Critiques a fair reading answers, softened or cut: Quantum Non-Realism's certainty "breaks
  its own rule" (now "sits uneasily", since the rule is the strict calculator's); a
  credentials jab in Where Philosophy Meets Science; the Lagrange-multiplier note and a line
  about the closing joke in If Many Worlds Had Come First; "leaves it standing" about the
  post's own ad hominem disclaimer in Collapse Postulates; a von Neumann line the post hedges.
- Physics checked by script: every amplitude in Configurations and Amplitude, Joint and
  Distinct Configurations; the 107 of 1,000 against 1/9 in Collapse Postulates; the Bell
  figures in Many Worlds, One Best Guess.

Tooling: preamble gained U+03A3, U+2192, U+2264, U+2009 and U+221A. md2tex now guards list
items that begin with "[" (the editor's note in Configurations and Amplitude ran off the left
margin as an \item label); check_verbatim ignores the guard. All posts pass.

Layout, for the whole-book pass: two overfull boxes (25pt, 67pt) in Joint Configurations
from long unbroken formulas in the post's own text.

## Batch 4d: Science and Rationality (rest of Book IV, 11 posts)

Five agents. Edits in `docs/raz/changes/batch04d.md`. The four posts of this sequence from
the original edition (249, 250, 253, 255) were not reannotated.

- Cut as the annotator's own reading or argument: how the joke in The Dilemma applies; in
  My Childhood Role Model, that a chimpanzee shares the brain parts the post lists (the list
  illustrates the claim; the brain-size point stays, as information), and a line on the
  unexplained ``harmed me''.
- Cut as arguing with the author's reported experience: in Einstein's Superpowers, reading
  the paraphrased ``Let's see your aura of destiny'' as a fair request for a record (note,
  Response and honest n.b.). The sourced point about the AI-Box Experiment stays.
- Cut as nitpick: ``almost no data'' in Einstein's Speed, which the post itself qualifies.
- Cut as the editors' choice: Class Project's links to posts the book leaves out.
- Points made once: Popper's improbability criterion is stated in Science Isn't Strict
  Enough; A Technical Explanation points there.
- Checked by script: the squared-error rule in A Technical Explanation that pays only on
  the outcome that happens is not proper for three outcomes (with true frequencies
  (.3, .2, .5), honest play scores 0.600 and the bets (.35, .03, .62) score 0.613). The
  afterword's ``one rule called proper that is not'' rests on this.

Tooling: preamble gained U+2211 and a private-use character (U+10FC09) found in A Technical
Explanation's text.

Whole-book pass: the original-edition notes on 249, 250, 253 and 255 (Faster than Science's
``In short'' among them) are harsher in tone than STANDARDS; already listed above.

## Batch 5a: Fake Preferences, Value Theory 270 to 273 (Book V, 12 posts)

Five agents. Edits in `docs/raz/changes/batch05a.md`.

- Critiques a fair reading answers, cut or recast:
  - Fake Selfishness: the ethical/psychological egoism split applied to a man who called
    himself selfish (psychological egoism is a thesis about everyone); "does not show the wish
    was kindness", which the post never claims.
  - Fake Utility Functions: "it means" called stronger than the post's next paragraphs (they
    explain why the argument persuades, not what the proposer values).
  - Not for the Sake of Happiness (Alone): "the arguments do not reach the evaluative
    question" became a scope sentence with a pointer to the book's later account of "should".
  - The Design Space of Minds-in-General: the post's answer is a hedged caution, not a claim
    that built AIs will be varied; the count and diagram points were answered by the post.
  - My Kind of Reflection: the induction-label test is a prescription about labels; Hume's
    position is what it rules out (information, not a missing premise).
  - No Universally Compelling Arguments: Kant's view agrees with the post's conclusion; now
    information, not a weakness.
  - Dreams of AI Design: Hanson's emulation objection was accepted by the author, so it is a
    disagreement; the AlexNet history stays in a note only.
  - Detached Lever Fallacy: the child-abuse aside is qualified by the post ("a good many of
    them break the loop") and the evidence is mixed; out of the Response.
- Prior work as credit, not fault: "names none of the earlier work" and "does not name" cut
  from Where Recursive Justification Hits Bottom, My Kind of Reflection and Created Already
  in Motion. Preface convention for Ends: An Introduction (premises reported, not charged).
- Imported dispute cut from the Response: motivational internalism in Created Already in
  Motion (the note itself says the practical point holds on either side).
- Points made once: Quine, rule-circularity and Bartley are stated in Where Recursive
  Justification Hits Bottom; My Kind of Reflection points there. The orthogonality thesis is
  stated in No Universally Compelling Arguments; Created Already in Motion points there.

Tooling: preamble gained U+22C0 (n-ary logical and, in Created Already in Motion). One agent
removed a bare "######" (a heading marker with no number) that md2tex printed literally in
Ends: An Introduction; the verbatim check passes. md2tex should drop such lines: whole-book
pass item. Agents saved "Fake Fake Utility Functions" (not in the book) to data/originals for
reference.

## Batch 5b: Value Theory 274 to 285 (Book V, 12 posts)

Six agents. Edits in `docs/raz/changes/batch05b.md`.

- Critiques a fair reading answers, cut or recast:
  - Value is Fragile: "the rule that valuable things need a valuer sits uneasily with
    evolution" (the post names evolution's case as "morally miraculous" and links The Gift We
    Give to Tomorrow).
  - Changing Your Metaethics: "explain the difference" called firmer than its sources (the
    earlier posts do explain it; they did not formalize it).
  - Sympathetic Minds: "the aliens conclusion has a gap" (the post defines how an
    unsympathetic mind sees us by the woodsaw exercise).
  - High Challenge: "a race is a game, so games are not a wasted step" (the annotator's own
    argument; the post's "wasted step" is about computer games as a substitute for work, and
    it wants "games that are fun to play").
  - Morality as Fixed Computation: "draws its contrast with Ord more sharply than it holds"
    became information (the author's comment locates the difference in how the idealization
    is specified); a patch nitpick in a post about maximizing AIs.
  - Serious Stories: "the verdict rests on guesses" (the post says "So far as I know or can
    guess"; hedges carry); a loss-aversion nitpick.
  - The True Prisoner's Dilemma: In short line now reports the author's concession that the
    complaint is about illustration.
- Not about the post: Hibbard's 2012 prize (Magical Categories), placed beside the post's
  remark on Hibbard's fitness, read as a rejoinder; cut.
- Hindsight kept out of the Response: the 2015 empathy review (Sympathetic Minds).
- Scope, reduced to pointers: 2-Place and 1-Place Words on moral language (the post does not
  apply its analysis to morality); the book's selection in Changing Your Metaethics.
- Points made once: Trivers and reciprocal altruism in The True Prisoner's Dilemma
  (Sympathetic Minds points there); simulation theory in Humans in Funny Suits; Nozick,
  Moore and Sidgwick in Not for the Sake of Happiness (Alone); Jackson's moral functionalism
  placed in both Could Anything Be Right? and Morality as Fixed Computation (whole-book pass:
  make one point to the other).

Agents fetched several posts not in the book to data/originals for reference (The Moral
Void, Is Morality Given?, The Meaning of Right, In Praise of Boredom and others).
