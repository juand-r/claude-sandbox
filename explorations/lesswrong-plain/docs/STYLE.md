# Rewriting style guide

Draft v0.1, to be revised after the pilot. The model is Jonathan Bennett's
earlymoderntexts.com: keep the author's argument, change only the prose.

## Faithfulness

1. Keep every claim, step of argument, and example. Do not add new claims.
2. Keep the author's voice and person. If the author says "I", the rewrite says "I".
3. Keep the author's hedges and confidence levels. Do not soften or strengthen them.
4. Cut repetition and flourish, but not content. When in doubt, keep it.
5. Anything that is mine and not the author's goes in a bracketed note:
   `[Note: ...]`. Use notes for:
   - explaining a reference the reader may not know;
   - a factual or arithmetic error in the original (show the check);
   - a place where I had to choose between two readings.

## Language

1. Plain modern English. Short sentences. One point per sentence.
2. Replace in-group jargon with ordinary words. Examples:
   - "epistemics" -> how we form beliefs / how well we reason
   - "update" -> change your mind, revise your estimate
   - "entangled with" -> correlated with, carries information about
   - "Fully General Counterargument" -> all-purpose rebuttal
   - "AFAICT" -> as far as I can tell
3. Keep a technical term when it names a real idea the post depends on
   (prior, odds ratio, Goodhart's law). Define it plainly on first use.
4. Keep the author's own coined terms when the post is about them
   ("floating beliefs", "clever arguer"). Those are the content.
5. No italics. Emphasis comes from sentence structure.
6. Keep the original title. Keep footnotes and links.

## File format

Each rewrite is Markdown with a header: original title, author, date,
source link, and a line saying it is a plain-English rewrite, not the
author's words.

# Rules for my own prose (all documents in this project)

Added September 2026 after the user objected to "the rule comes with its own exit".

Main principle: avoid strange constructions, figures of speech and Claudisms that a
reader would have to decode. Clear jokes are fine; puzzles are not. The rules below
are applications of this.

1. No invented metaphors. Never describe an argument, a rule or a text as an object
   or a place: no exits, doors, gates, ladders, bridges, seals, anchors, engines,
   machinery, scaffolding, weight-bearing. Say literally what happens.
   - Bad: "the rule comes with its own exit."
     Good: "any group can declare itself rational, so anyone can exempt themselves."
   - Bad: "the clause seals the thesis against its audience."
     Good: "a reader who disagrees only confirms the diagnosis."
2. Jokes are welcome when their literal meaning is instantly clear. "Ask you to marvel
   again, in case the first marvel did not take" is fine: it says exactly what happens.
   What is banned is a figure of speech the reader must decode to find the claim
   ("the rule comes with its own exit"). Test: can a first-time reader say what the
   sentence claims without pausing? If yes, keep the joke. Do not strip humor in the
   name of plainness (the user objected when I did).
3. No compressed allusions to what comes later ("I will need that reason in a minute").
   State the point where it applies.
4. Each sentence makes one literal claim that a first-time reader can check against
   the text. Satire comes from stating plainly what the post does, not from wordplay.
5. Before finishing, reread every sentence and ask: what does this mean, literally?
   If the answer takes more words than the sentence, rewrite the sentence.

# Checklist: run after writing each section of LessWrong, Honestly

Mandatory. Run each pass separately, in this order, before showing a section to the user.
Each pass looks for one kind of error only.

1. Decode pass. For every sentence, state its literal claim to myself. If that takes
   more words than the sentence, or needs knowledge the reader does not have, rewrite
   the sentence. Every "it", "this", "that", "they" must have exactly one possible
   referent. No invented figures of speech (see the rules above). Clear jokes stay.
2. Verbs-against-source pass. For every verb that characterizes the author (claims,
   admits, reverses, dismisses, proves, ignores, never says, repeats), open the
   original and confirm the author did exactly that. Same for numbers, counts
   ("two of my eight paragraphs"), dates and names. Apply this to my own fixes too.
   Quoted words: check verbatim against data/originals.
3. Voice pass. Every sentence is either the author speaking in the first person about
   what the post does ("I say...", "I do not mention...") or a marked quotation. An
   short plain comment is fine, as in the model sections ("That is a joke, and it is
   the whole defense"). What must never happen is that a reader cannot tell whose view
   a sentence states, or that the author seems to assert something the post denies.
4. Source pass. Claims taken from the annotated edition (notes, Responses) are leads,
   not proof. Any factual claim about the world or the post's errors must be checkable
   in the original or in a source cited in the notes; if I cannot confirm it, drop it.
5. Diff pass (for edits). Change only the phrases I can name as faulty. Diff and confirm
   nothing else moved.
6. Optional cold read. An agent reads the section without context and lists every
   sentence it had to reread. I verify each item before acting on it.

Model sections: the three samples as of commit 7753c93, especially The Lens That Sees
Its Flaws. Length: see docs/STANDARDS.md section 5 (about 150 to 500 words).

# Rules of thumb for LessWrong, Honestly (from the user's review, September 2026)

These came out of one round of review. Apply them by hand, sentence by sentence. Never apply them with a regex or a batch script.

1. **Separate the two voices.** The author's voice retells the post, including ironic lines that describe what the post does or leaves out ("I give no example", "I do not mention this"). The editor's corrections, facts from outside the post, and judgments go in `\nb{...}`, in the third person ("Yudkowsky had written", not "I had written"). If an ironic line depends on an outside fact, put that fact in an n.b. just before it. Merge neighbouring notes when that reads more clearly.
2. **No bare verdicts.** Cut sentences like "This is sensible", "Also good", "This is good advice". Keep a verdict only when the next sentence turns on it ("That is true. It also contradicts…"). Decide each case by reading the whole paragraph.
3. **Name what you refer to, and stop there.** "Two of those fields" becomes "two of those fields, social psychology and evolutionary psychology". "An earlier post" becomes the post's title. "A physicist" becomes the name. Do not add examples, dates, numbers or explanations that the sentence does not need.
4. **Quotes are the author's exact words.** A quote that stands alone as a sentence gets a short tag that states the author's move: "I say", "I admit", "I repeat", "I state without evidence", "Then I contradict myself". A harsh tag is allowed only when the surrounding text shows it is deserved. Quotes inside a sentence that already names the speaker need no tag.
5. **Paraphrase only when it helps, and keep the key terms.** Do not change words for the sake of change. If the post says "causal graphs", "nodes" and "screen off", a paraphrase keeps them.
6. **Plain language in our own voice.** Drop jargon in the editor's voice and in the retelling. The exception is the community's overused terms ("epistemics", "update your priors", "Bayesian", "rationalist", "the Way"). Keep those in the author's words, in quotation marks, where mocking them is the point.
7. **Do only what was asked.** Make the smallest edit that does the job. Show every change (before and after). Never widen an edit on your own.
8. **Opening note stays true.** If a rule changes what the document does, check that the opening note still describes it.

## Final review checklist (September 2026, after the Yoda notes)

Read each section against its original and check:

1. Voices. Every sentence outside an n.b. is something the author says, or an ironic line the author could plausibly say about the post. A sentence that reads as an outsider describing or judging the post ("X had not said...", "the post leaves out...") belongs in an n.b.
2. Placement. Each n.b. sits next to what it comments on. No n.b. / author line / n.b. sequences that depend on each other; merge them into one note.
3. Accuracy. Every paraphrase matches the original; every fact in an n.b. is checked.
4. Clarity. Each note says one clear thing a reader can follow without the original.
