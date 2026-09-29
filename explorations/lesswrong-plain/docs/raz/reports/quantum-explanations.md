# Report: Quantum Explanations (batch 4c, order 233)

## 1. The argument in three sentences

The post announces how the quantum sequence will teach: it will speak of quantum mechanics as
normal and make fun of the human intuitions that find it strange, it will skip the historical
story of particles and waves, and it will start from the quantum level rather than from
experimental results. It rests this on the claims that confusion is a fact about models, not
about the world, and that the old confusion about quantum mechanics was "finally sorted out in
the second half of the twentieth century." It declares a strictly realist stance, in which the
equations describe the territory and the classical world exists only implicitly within the
quantum one, and warns that a sizable community of scientists disputes it.

## 2. Sources checked

All fetched texts are saved in `data/sources/4c_quantum-explanations/`.

| Claim in our text | Source | Exact words matched |
|---|---|---|
| Feynman, "nobody understands quantum mechanics" | Wikiquote, Richard Feynman (`wikiquote_feynman.txt`, `https://en.wikiquote.org/w/index.php?title=Richard_Feynman&action=raw`), under *The Character of Physical Law* (1965), ch. 6, p. 129 | "I think I can safely say that nobody understands quantum mechanics." |
| Context of the Feynman passage | Excerpt of the same lecture on a Georgetown chemistry page (`bouman_feynman.txt`, `https://bouman.chem.georgetown.edu/general/feynman.html`). Secondary copy; the page mislabels it "The Messenger Lectures, 1964, MIT" (they were at Cornell, per Wikiquote). Two sentences cross-checked against Wikiquote. | "This growing confusion was resolved in 1925 or 1926 with the advent of the correct equations for quantum mechanics."; "waves or particles, particles or waves?"; "They behave in their own inimitable way"; "I will not describe it in terms of an analogy with something familiar; I will simply describe it."; "just relax and enjoy it"; "Nobody knows how it can be like that." |
| von Neumann's line | Wikiquote, John von Neumann (`wikiquote_von_neumann.txt`) | "Young man, in mathematics you don't understand things. You just get used to them." / "Reply, according to Dr. Felix T. Smith ... to a physicist friend who had said "I'm afraid I don't understand the method of characteristics," as quoted in The Dancing Wu Li Masters ... (1979) by Gary Zukav" |
| No consensus on interpretation | SEP, "Philosophical Issues in Quantum Theory" (`sep_qt-issues.txt`, https://plato.stanford.edu/entries/qt-issues/) | "there is no consensus among physicists or philosophers of physics on the question of what, if anything, the empirical success of quantum theory is telling us about the physical world." |
| Pilot-wave and collapse are realist | same | "According to this theory, there are particles with definite trajectories, that are guided by the quantum wave function."; "The major realist approaches to the measurement problem are all, in some sense, realist about quantum states."; collapse: "finding suitable indeterministic modifications of the quantum dynamics" |
| Decoherence and the measurement problem; Zeh and Zurek | SEP, "The Role of Decoherence in Quantum Mechanics" (`sep_qm-decoherence.txt`) | "decoherence as such does not provide a solution to the measurement problem, at least not unless it is combined with an appropriate foundational approach to the theory – whether this be one that attempts to solve the measurement problem, such as Bohm, Everett or GRW; or one that attempts to dissolve it"; "The modern foundation of decoherence as a subject in its own right was laid by H.-D. Zeh in the early 1970s (Zeh 1970, 1973). Equally influential were the papers by W. Zurek from the early 1980s" |
| 2011 poll | Schlosshauer, Kofler and Zeilinger, arXiv:1301.1069 (`schlosshauer2013.txt`) | "Question 9: What interpretation of quantum states do you prefer? a. Epistemic/informational: 27% b. Ontic: 24% c. A mix of epistemic and ontic: 33% d. Purely statistical ... 3%". Sample: "33 participants of a conference on the foundations of quantum mechanics" (abstract), held "July 3–7, 2011". |
| 2025 Nature survey | Nature article itself is paywalled (`nature2025.txt`: title "Physicists disagree wildly on what quantum mechanics says about reality, Nature survey shows", dated 2025-07-30, Nature 643). Figures from The Quantum Insider, 2 Aug 2025 (`survey2025_thequantuminsider.com.txt`), cross-checked with Gizmodo (`survey2025_gizmodo.com.txt`) | "over 1,100 respondents"; "Roughly 36% said it is real, while 47% said it is not. Another 8% said it represents subjective belief." |
| Everett credit (Response) | SEP, "Everett's Relative-State Formulation" (`sep_qm-everett.txt`) | "The short version of his doctoral thesis (1957a) was accepted in March 1957" |

The Response and honest section quote "nobody understands quantum mechanics": that is Feynman's, not the post's (see above).

## 3. Arithmetic

None of our notes relies on arithmetic in this post. Dates: post 2008-04-09; "Quantum Non-Realism" 2008-05-08 and "Many Worlds, One Best Guess" 2008-05-11 ("a month later").

## 4. Claims about other posts

- "Think Like Reality" (`data/originals/think-like-reality.md`, posted 2007-05-02): "Surprise exists in the map, not in the territory." Our notes on that post (afterword) already credit Feynman's *QED* for the same advice and say the post states a contested interpretation as fact; consistent.
- "If Many Worlds Had Come First" (`if-many-worlds-had-come-first.md`, 2008-05-10): "Macroscopic decoherence, a.k.a. many-worlds, was first proposed in a 1957 paper by Hugh Everett III."
- "Quantum Non-Realism" (`quantum-non-realism.md`, 2008-05-08): the promised essay on non-realism; it says "The correct answer is not available to you as a hypothesis, because it will not be invented for another thirty years" and "the wavefunction gives us a certainty of many worlds existing," which supports reading "sorted out" as many-worlds.
- "Many Worlds, One Best Guess" (`many-worlds-one-best-guess.md`, 2008-05-11), line 39: "There is no known reason for the [Born probabilities]". Context read: the paragraph is about getting probabilities within many-worlds; the sentence is a general statement that the Born rule is unexplained. It is used only as the author's own later statement.
- "No post in the book discusses pilot-wave theory": `grep -i -E 'bohm|pilot|broglie'` over all 369 files in `data/originals/` finds nothing; "hidden variables" occurs only in "Quantum Non-Realism" (local hidden variables and Bell) and in "Bell's Theorem: No EPR 'Reality'", which is not in the book.
- Consistency with earlier notes: "The World: An Introduction" notes cite the same 2011 poll (Everett 18 per cent, Copenhagen 42 per cent); "Is Reality Ugly?" and "Making Beliefs Pay Rent" point forward to the sequence for the full many-worlds assessment. Nothing here makes that assessment; it is left to "Many Worlds, One Best Guess".

## 5. Not verified

- The Feynman Lectures on Physics (feynmanlectures.caltech.edu) are blocked by Cloudflare from this environment, and web.archive.org resets the connection. I used *The Character of Physical Law* passage instead, via a secondary copy (see above). If the editor wants a primary check, the passage is on p. 129 of the 1965 book.
- The 2025 Nature survey figures are second-hand (two news reports agree). The article is paywalled.
- The post's "I get frequent grateful emails" is self-report; not checkable.
- "Six quarks" (six flavours) is correct; ordinary matter contains only up and down quarks, not worth a note.

## 6. Judgment calls for the editor

- Reserved words: none used in notes, Response or n.b.
- "The post reports his attitude accurately" (Feynman note) is credit; I kept it because the next note disputes the post's claim that the era has passed, and a reader should not think the post misreports Feynman.
- The Feynman-credit note ("does not credit him for it") is mild; Feynman's passage is from a popular lecture, not "the standard introduction". I kept it out of the "In short" line.
- The von Neumann note: the post hedges with "is reputed". I judged the change of subject (mathematics to quantum mechanics) worth a note because the post uses the line as evidence about the "dark decades" of quantum mechanics.
- The poll note: neither poll is of "theoretical physicists", and the post says it counts polls for little. I state both limits in the note. "A mix of epistemic and ontic" (33 per cent in 2011) could be read as partly realist; I therefore wrote "a purely realist view", matching the post's "I'm a pure realist".
- Inference: "Later posts show that the author means many-worlds" rests on "Quantum Non-Realism" and "If Many Worlds Had Come First" (quoted above). Not marked "My reading" because the later posts say it.
- Honest section is 511 words, slightly over the 500 guide.
