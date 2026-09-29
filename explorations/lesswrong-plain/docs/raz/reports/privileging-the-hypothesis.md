# Report: Privileging the Hypothesis (batch 4c, order 240)

## 1. The argument in three sentences

Singling out one hypothesis from a large space, even only for consideration, needs evidence
already in hand, because locating a hypothesis among many takes most of the evidence needed
to believe it (a billion boxes: 27 bits to narrow to ten, 4 more to pick one). Raising a
hypothesis with no such evidence, as a detective who names a random citizen or a theist who
points at gaps in science, does most of the work of persuasion without evidence, and "doubt
within a normal space" is then slopped onto a privileged, abnormal target. The author applies
this to quantum mechanics: with no evidence for collapse, treating single-world theories as
still in the running is privileging a hypothesis that breaks every usual property of
physical law.

Scratch files and sources: `data/sources/4c_privileging-the-hypothesis/` (shared with the
Living in Many Worlds report; insertion script `insert_notes.py`, note lists `notes_pth.py`).

## 2. Sources checked (outside quotations and figures)

| Claim in our text | Source read | Exact words matched |
|---|---|---|
| Aaronson: interpretations "all yield the same experimental predictions, at least for any experiments that we can do currently" | MIRI transcript (volunteer transcription), linked from https://intelligence.org/2013/05/29/new-transcript-yudkowsky-and-aaronson/ ; Google Doc https://docs.google.com/document/d/1JIqzTGNvdLukR0Ce5T2eiv_vxtPO53N3KGCbxVvREtU/pub ; saved as `transcript.txt` | "Any interpretation, because they all yield the same experimental predictions, at least for any experiments that we can do currently, are not going to violate causality ..." |
| Aaronson's complexity reply; "giant pink dragons" | same transcript | Eliezer: "Why shouldn't the theory that succeeds quantum mechanics recarve the conceptual space in just such a way as to make giant pink dragons materialize in the sky ..." Scott: "All of those seem to be adding a lot more Kolmogorov complexity to your description, than just saying there's just one world." |
| Transcript published by MIRI in 2013 | MIRI page URL date 2013/05/29 | page title "New Transcript: Yudkowsky and Aaronson" |
| Conversation from 2009 | LessWrong GraphQL, post 8njamAu4vgJYxbJzN (`lw_diavlog_post.json`) | "Bloggingheads: Yudkowsky and Aaronson talk about AI and Many-worlds", postedAt 2009-08-16 |
| "I don't know. It's an open problem."; "under fifty percent"; "mangled worlds" | `data/originals/the-born-probabilities.md` (2008-05-01) | "What are the Born probabilities, probabilities *of*? ... I don't know. It's an open problem."; "I'd put it under fifty percent"; "Hence Robin's cheery phrase, "mangled worlds"." |
| Koehler 1991 quotations | PubMed abstract, PMID 1758920 (`koehler1991_abstract.txt`), Psychol Bull 110(3):499-519 | "people who explain or imagine a possibility then express greater confidence in the truth of that possibility"; "any task that requires that a hypothesis be treated as if it were true is sufficient to increase confidence in the truth of that hypothesis" |
| God of the gaps: Drummond 1893, phrase credited to Coulson 1955; critics of ID | Wikipedia "God of the gaps", `?action=raw` (`wiki_god_of_the_gaps.txt`) | "The concept, although not the exact wording, goes back to Henry Drummond ... from his 1893 Lowell Lectures"; "It is claimed that the actual phrase 'God of the gaps' was invented by Coulson" (book 1955); "Critics of intelligent design creationism, for example, have accused proponents of using this basic type of argument." |
| Argument from ignorance, Locke | Wikipedia "Argument from ignorance", raw (`wiki_argument_from_ignorance.txt`) | "The term was likely coined by philosopher John Locke in the late 17th century." |
| Bohmian mechanics quotations | SEP "Bohmian Mechanics", https://plato.stanford.edu/entries/qm-bohm/ fetched by curl this session (`sep_qm-bohm_live.html`; checked by string match) | "evolving, as usual, according to Schrödinger's equation"; "any (single-world) account of quantum phenomena must be nonlocal"; deterministic motion: "the configuration of a system of particles evolves via a deterministic motion choreographed by the wave function"; Deutsch: "pilot-wave theories are parallel-universes theories in a state of chronic denial"; "Bohmians do not agree that the branches of the wave function should be construed as representing worlds" |
| Peirce credit in Einstein's Arrogance notes | `annotated/posts/einstein-s-arrogance.tex` | cfact "The counting argument is older than the post. Charles Peirce ..." |

## 3. Arithmetic recomputed

- Billion boxes narrowed to ten: factor 10^9 / 10 = 10^8; log2(10^8) = 26.58, so 27 bits. Correct.
- Then 4 bits among ten equal candidates: prior odds of the true one 1:9; likelihood ratio 2^4 = 16; posterior odds 16:9; probability 16/25 = 0.64 > 0.5. "better than even odds" correct.
- One person in a million: log2(10^6) = 19.93, about 20 bits (my added check in the note).
- "27 of the 31 bits" (my note on "more than halfway"): 27 + 4 = 31 from the post's own figures.

## 4. Claims about other posts

- Positive Bias: Look Into the Dark (linked by the post): our notes there argue the 2-4-6 task does not show a general "human instinct" (`annotated/afterwords/positive-bias-look-into-the-dark.tex`). My note only points there.
- Einstein's Arrogance (2007-09-25): "you need at least 27 bits of evidence just to focus your attention uniquely on the correct answer" (`data/originals/einstein-s-arrogance.md`).
- The Born Probabilities (2008-05-01): quotations above.
- Collapse Postulates (2008-05-09): the property list ("The only non-linear evolution ...", "violates CPT symmetry", "violates Liouville's Theorem", "non-local ... faster than light") is its numbered list, `data/originals/collapse-postulates.md` lines 54-62. Its annotation is by another agent (not yet written when I finished), so I only point to it.
- Burdensome Details: the post's own phrase "each part of a belief be separately justified" is quoted from this post, not from Burdensome Details.
- Perpetual Motion Beliefs (2008-02-27): "turn warm water into electricity and ice cubes" (line 78). Our afterword there discusses the analogy; my note points to it.
- Making Beliefs Pay Rent and Many Worlds, One Best Guess: pointer only, for the simplicity argument (STANDARDS 2.5). The Many Worlds, One Best Guess notes are being written by another agent; my pointer assumes they will assess the simplicity case, as the batch instructions say.

## 5. Not verified

- The diavlog itself (bloggingheads.tv video 2220) was not watched. I used the MIRI volunteer transcript; its wording may differ from the audio. The post's report that Aaronson "admit[ted] that there was no concrete evidence whatsoever" is not quoted verbatim in the transcript; the nearest line is the one about identical experimental predictions. I did not call the post's report inaccurate, only noted what the transcript shows.
- Koehler 1991: abstract only.
- Wikipedia is cited as a secondary source for Drummond, Coulson and Locke.

## 6. Judgment calls for the editor

- Reserved words: none remain in notes, Response or n.b.s ("the opposite" was removed). "Overstated" is used for "single-world theories violate *all* these characteristics"; the evidence is Bohmian mechanics (SEP). A fair defender might say Bohm is "many-worlds in denial" (Deutsch); the note states that dispute and that Bohmians reject it.
- Main criticism (cpara on "This is indeed what I would call ..."): the Mortimer analogy holds only with the complexity premise. The post does state that premise ("no more complicated or unlikely", and via Occam's razor), so the note says the charge "depends on" it rather than that the post hides it. Full assessment deferred to Many Worlds, One Best Guess.
- Aaronson's complexity reply: I present it as a reason "the post does not report". The post reports Aaronson's other two points (future evidence, Born). Fair defender might say a blog post need not report every argument of a conversation; I kept it because the reply answers the post's exact charge. Editor may prefer to move it to the Response only.
- "There must be a trillion better ways" note: uses the 2008 Born post (Hanson "under fifty percent") as information, not as a contradiction. The 2008 post also says "It would be much lower if I knew of a single alternative that seemed equally... reductionist"; I did not quote this, because it concerns alternatives to Hanson, not to collapse, and would read as a gotcha.
- Credit notes (Koehler; God of the gaps; argument from ignorance; Peirce via Einstein's Arrogance) are given as information, per the batch instructions. The post asked for an existing name; I did not claim none exists. In the comments (2009-09-30, `pth_comments.json`) the author linked the fallacy to "packing and unpacking"; not used.
- Placement note (posted September 2009, placed in a 2008 sequence) is neutral, per the Book III lesson.
- Honest section is 533 words by raz_check's count, slightly above "about 500". Six n.b.s.
