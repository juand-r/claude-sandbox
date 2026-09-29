# Report: gazp-vs-glut

## 1. The argument in three sentences

A giant lookup table (GLUT) that reproduces a human's inputs and outputs seems to be a thing that talks about consciousness without being conscious, and so a problem for the Generalized Anti-Zombie Principle of the previous post. The author answers with "Follow-The-Improbability": a table that matches a human is so improbable that something must have selected it, and tracing the selection back (to a brain specification, a designer, or the philosopher who stipulates it) always finds consciousness, so the table is a relay like a cellphone, not a zombie. Only a table drawn by genuinely pure chance would talk without a conscious source; the author grants, "IMHO", that it would not be conscious, and then applies the same reasoning to AI designs said to be moral by accident.

## 2. Sources checked

Saved texts are in `data/sources/4b_gazp-vs-glut/` (helper `insert_notes.py` and the note specs `spec_*.py` are there too; the post files were edited after insertion, so the specs are not the final wording).

- Dennett, "The Unimagined Preposterousness of Zombies", J. Consciousness Studies 2(4), 1995. NOT CHECKED. The Tufts URL redirects to the university home page (`dennett_unzombie.htm`); a LiveJournal copy labelled 1994 (`lj.txt`) is cut at 20,000 characters and does not contain the sentence; Brainchildren on archive.org is lending-only (401). The note says the quotation is unchecked.
- Block (1981), "Psychologism and Behaviorism", Phil. Review 90: 5-43. The NYU PDF returns 403 to curl and 405 to WebFetch. Quotations taken from Drew McDermott, "On the Claim that a Table-Lookup Program Could Pass the Turing Test", Minds and Machines 24 (2014), preprint https://www.cs.yale.edu/homes/dvm/papers/humongous.pdf (`mcdermott.txt`, lines 144-145): "[T]he machine has the intelligence of a toaster. All the intelligence it exhibits is that of its programmers.. . . I conclude that the capacity to emit sensible responses is not sufficient for intelligence. . . . (p. 21)"; lines 672-681, Block p. 22: "The point of the machine example may be illuminated by comparing it with a two-way radio. ... The two-way radio is like my machine in being a conduit for intelligence". Discrepancy: the SEP entry "The Turing Test" (`sep_turing.txt`, line 1004-1006) quotes Block as saying Blockhead "has all of the intelligence of a toaster". I quote McDermott's wording and cite McDermott.
- Shannon and McCarthy (1956), preface to Automata Studies: not read directly. Quoted by B. Gonçalves, "Turing's Test, a Beautiful Thought Experiment", arXiv:2401.00009v3 (`arxiv_2401.00009.txt`, lines 912-918): "it has 'the disadvantage' of being susceptible to a memorizing machine playing the imitation game by looking up 'a suitable dictionary.'" Wikipedia "Blockhead (thought experiment)" (`wp_blockhead.txt`) says the same, citing Copeland.
- Feynman quotation: matches word for word the text of "Judging Books by Their Covers" in `data/sources/feyn_b1f794.txt` and `feyn_cba79c.txt` (saved by an earlier agent), from "It was the kind of thing my father would have talked about" to "the transformation of the sun's power." The post's link (textbookleague.org) now serves a bot check (`textbookleague_103feyn.txt`).
- LessWrong rendering of "10585": GraphQL API, `lw_k6EPphHiBH4WWYFCj.json`: "7.6 * 10<sup>585</sup>".

## 3. Arithmetic

- Multiplication table: 100 x 100 = 10,000 entries. Correct.
- Conversations: 20 remarks x 10 words = 200 word slots, 850 choices each: 850^200. log10(850) = 2.929419; x 200 = 585.8838; 10^0.8838 = 7.65. So 7.6 x 10^585 (7.65 truncated). Correct.
- "too large to fit in our universe": 10^585 against roughly 10^80 atoms in the observable universe. Consistent; not noted.
- Random table: if a table is N bits and drawn uniformly, the chance of one given table is 2^-N. Used in the many-worlds note ("about 2 to the minus its length in bits").

## 4. Claims about other posts

- The Generalized Anti-Zombie Principle (`data/originals/the-generalized-anti-zombie-principle.md`), last paragraphs: "I think the Generalized Anti-Zombie Principle supports Albert's position, but the reasons shall have to wait for future posts." Used in the clogic on "a conscious algorithm". Albert's position is that a brain whose neurons are replaced by functionally identical robots is still conscious, so "left open" is the right description.
- Zombies! Zombies? (`data/originals/zombies-zombies.md`): defines the "Zombie Master" ("a god within the Zombie World who surreptitiously takes control of zombie philosophers"; the chatbot trained on "one thousand human amateurs"). Used in two cparas.
- The book's next sequence (orders 233 onward, "Quantum Physics and Many Worlds", manifest) argues for many-worlds; the many-worlds point is made in full in the note on Making Beliefs Pay Rent (afterword), so this note does not repeat the charge, it only says the argument does not need the interpretation.
- "How Much Evidence Does It Take?" and "Einstein's Arrogance" are the targets of the post's own links (how-much-eviden, einsteins-arrog).

## 5. Items not verified

- Dennett's quoted sentence (see section 2). Needed: the published JCS text or Brainchildren (1998).
- Block's paper itself (pages 21-22 via McDermott only). Needed: the Phil. Review text.
- Whether anyone before 2008 claimed a GLUT is conscious. The post hedges ("I can't recall"); the SEP entry says it is "not obvious that we should deny that Blockhead is intelligent" (intelligence, not consciousness) and McDermott (2014, after the post) argues an optimized lookup program could have the mental states of the model it came from, setting phenomenal consciousness aside. I did not use either against the post.

## 6. Judgment calls for the editor

1. The clogic "Here 'zombie' changes sense." It is the main analytic note. A fair defender could say that the GAZP sense (talk traced to its cause) was the point all along, and the post says so ("the very archetype of a Zombie Master"). The note grants that this is the sense the principle needs; its claim is only that the change from the opening definition is not marked. Cut to a cpara remark if it reads as a wording point.
2. The cpara on "Well, then it wouldn't be conscious. IMHO": "the post allows that, if such a table were drawn, something would talk as we do without being conscious ... a claim about probability". I first wrote "grants that ... is possible" and weakened it to the conditional, since the post only supposes the draw.
3. The clogic on "a conscious algorithm": the post never says the specification must be run on other hardware; "computational specification ... used that to precompute" implies it. The note says the argument survives.
4. Credit notes on Block (reductio, two-way radio). These are information, not faults; "The post credits Block only through Dennett's quotation" is a neutral statement of fact. The two-way radio quotation comes via McDermott, a secondary source.
5. The AI coda: "The people described are not named; they are reported from the author's experience." I kept it neutral and did not point to the "unnamed crowds" notes in Say Not Complexity, because this is an anecdote about the author's work and the essay-anecdote rule (2.2 test 4) may apply. Cut if it seems a nitpick.
6. Reserved words: "wrong" appears only inside the paraphrase of the post's "wrong pattern of levers". No "My reading" inferences.
7. Pronouns: Dennett and Block restructured to names.
