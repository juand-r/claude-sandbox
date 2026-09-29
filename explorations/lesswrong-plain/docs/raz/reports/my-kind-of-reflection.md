# Report: my-kind-of-reflection ("My Kind of Reflection", Yudkowsky, posted 2008-07-10; book order 271)

## 1. The argument in three sentences (written before annotating)

The post follows "Where Recursive Justification Hits Bottom" (posted two days earlier), which
concluded that it is fine to use induction and Occam's razor to assess induction and Occam's
razor, and, prompted by a comparison with Bartley's pancritical rationalism, it lists what the
author sees as the distinguishing features of this view of reflection. The features are: the
view comes from designing a self-modifying AI; it is naturalistic (the AI treats its own parts
like anything in the environment); reflective consistency is a side effect of trying to win, not
a goal; Jaynes's rule to use all information licenses using induction on induction; one inspects
foundations to improve them, not to look fair; improvements should add up to normality; "Does
induction work?" (answerable by induction) differs from "Why does it work?" (still open). Loops of
justification through the meta-level are not circular logic, though the author has not yet
formalized the difference.

## 2. Sources checked

Local copies in `data/sources/5a_my-kind-of-reflection/` (curl, 29 Sept 2026) unless noted.

1. Chris Hibbert's comment on "Where Recursive Justification Hits Bottom", LessWrong GraphQL
   (post C8nEXTcjZb9oauTCW, `wrjhb_comments.json`), posted 2008-07-08T18:31. Matched: "Hurrah!
   Eliezer says that Bayesian reasoning bottoms out in Pan-Critical Rationalism."; "I think the
   emphasis on process is more useful than your phrasing's focus on justification."
2. Bruce W. Hauptli, "A Dilemma for Bartley's Pancritical Rationalism", Philosophy of the Social
   Sciences 21(1), March 1991, 86-89 (https://faculty.fiu.edu/~hauptli/ADilemmaforBartley.pdf,
   `hauptli_bartley.txt`). Matched: "'comprehensive' rationalists attempted to justify each of
   their theories or beliefs, and the attachment to justificationalism was their undoing";
   "'Critical' rationalists ... rejected justificationalism"; pancritical rationalism demands
   "that all of their beliefs, theories and commitments (including their commitment to the
   critical methodology) be open to criticism". Also Wikipedia "Pancritical rationalism" (raw,
   `wiki_Pancritical_rationalism.txt`): "decoupling criticism and justification" (not quoted).
3. Hume, Enquiry, Hume Texts Online. Section 4 (`data/sources/4b_when-anthropomorphism-became-stupid/apriori/hume_e4.txt`):
   E 4.19 "all our experimental conclusions proceed upon the supposition, that the future will
   be conformable to the past. To endeavour, therefore, the proof of this last supposition by
   probable arguments, or arguments regarding existence, must be evidently going in a circle,
   and taking that for granted, which is the very point in question." E 4.20 "none but a fool
   or madman will ever pretend to dispute the authority of experience, or to reject that great
   guide of human life". Section 5 (https://davidhume.org/texts/e/5, `hume_e5.txt`): E 5.5
   "All inferences from experience, therefore, are effects of custom, not of reasoning".
4. SEP, "Naturalism in Epistemology" (first published 2016, rev. 2020; earlier agent's copy
   `.../apriori/sep_epistemology-naturalized.txt`). Matched Quine 1969b quotations: "Epistemology,
   or something like it, simply falls into place as a chapter of psychology and hence of natural
   science." and "such scruples against circularity have little point once we have stopped
   dreaming of deducing science from observations. (1969b: 75–76)".
5. SEP, "The Problem of Induction" (Henderson, rev. 2022; `.../apriori/sep_induction-problem.txt`,
   section 4.1). Matched: "'premise circular'", "'rule-circular'—it relies on a rule of inference
   in order to reach the conclusion that that very rule is reliable"; "although premise-circularity
   is vicious, rule-circularity is not (Cleve 1984; Papineau 1992)"; "less sane inference rules
   such as counterinduction can support themselves in a similar fashion".
6. Yudkowsky and Herreshoff, "Tiling Agents for Self-Modifying AI, and the Löbian Obstacle",
   early draft dated October 7, 2013 (https://intelligence.org/files/TilingAgentsDraft.pdf,
   `tiling.txt`). Matched: "Constructing a formalism in the most straightforward way produces a
   Gödelian difficulty, the 'Löbian obstacle.' By technical methods we demonstrate the possibility
   of avoiding this obstacle, but the underlying puzzles of rational coherence are thus only
   partially addressed."; "A consistent mathematical theory T cannot trust itself in the sense of
   verifying that a proof in T of any formula φ implies φ's truth" (paraphrased in the note).

## 3. Arithmetic

None.

## 4. Claims about other posts

- "Where Recursive Justification Hits Bottom" (`data/originals/`, posted 2008-07-08, order 270):
  "E. T. Jaynes used to say that you must always use all the information available to you";
  "The point is not to be reflectively consistent. The point is to win."; "Everything, without
  exception, needs justification."; "I do think that reflective loops have a meta-character
  which should enable one to distinguish them, by common sense, from circular logics";
  anti-Laplacian minds: "they reply, "Because it's never worked for us before!"". Posted two days
  before this post (2008-07-10), and immediately before it in book order.
- "The Simple Truth": Mark's "coherentist theory of magic buckets" (lines 123-131); its notes
  credit Russell (1907) for the objection to coherence theories. Neither The Simple Truth nor
  Twelve Virtues contains the five-maps example the post attributes to them (Twelve Virtues has
  a city map drawn "according to impulse"; The Simple Truth has buckets). I judged this a
  citation slip with no effect on the argument (STANDARDS 2.4(2)) and kept it out of the notes;
  the cpara only points to The Simple Truth.
- "Occam's Razor": Thor and Maxwell's equations (lines 17-23 of the original); our notes there
  discuss the measure and "as it turns out".
- "Living in Many Worlds": "Just remember Egan's Law: It all adds up to normality."
- "A Priori" notes already give the externalist reply (Van Cleve, via SEP) and credit Carroll.
  My rule-circularity note adds the premise/rule distinction and the counterinduction objection.

## 5. Not verified

- Jaynes's own wording of the "use all the information" principle (the post and WRJHB
  paraphrase it; no note depends on the wording).
- Whether the WRJHB annotator (order 270, being written in parallel) already makes the Quine or
  rule-circularity points in full. If so, my two clogic notes on the naturalism and last
  features should be shortened to pointers (STANDARDS 2.5). I could not read their notes; the
  files did not exist when I started.

## 6. Judgment calls

1. The Hume clogic on the AI test ("The test assumes that calling induction unjustifiable means
   advising against its use"). A defender may reply that for an AI that rewrites its code by
   reasoning, "unjustifiable" does amount to "no reason to keep it". I therefore did not say the
   test fails; I said it assumes an unstated premise and the post does not say why the Humean
   combination is unavailable. The Response and "In short" use the same wording ("assumes,
   without saying why").
2. The Bartley note: the post explicitly declines to compare ("may or may not"), so I present the
   difference on justification as information plus a scope sentence ("The post does not take up
   this difference"), not as a fault. Its source for Bartley is Hauptli's short paper, a
   secondary account; I could not reach Bartley's own texts (web.archive.org reset).
3. The Löbian obstacle note is the author's own later work, used as information about the
   post's hedged suspicion ("I strongly suspect"). The paper is about proof-based agents; the
   post's case is Occamian (probabilistic) reasoning, and the paper says the probabilistic case
   "remains open". I wrote "bears on", not "contradicts".
4. The "Does/Why" clogic says Hume's charge concerns the "does" question. This is my reading of
   E 4.19 (the supposition that the future will conform to the past). I kept it informational.
5. The cpara on the postures paragraph says "The second sentence is hard to parse". This is a
   comprehension aid, not a style charge; cut it if the editor counts it a nitpick.
6. Reserved-word flags: "wrong" is the post's own word in a paraphrase. Pronouns: he/his/him only
   for Hume and Quine (historical); Hibbert rephrased to avoid a pronoun.
7. The Response is 451 words, at the upper limit.
