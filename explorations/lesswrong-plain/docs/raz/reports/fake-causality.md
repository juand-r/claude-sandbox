# Report: fake-causality

## 1. The argument in three sentences

Phlogiston theory explained fire, ash and extinguished flames only after the fact and could
explain anything, yet it felt like an explanation, because the mind stores such a cause in
the same format as a real one (a node and arrow in something like a Bayes net) and hindsight
makes a fitted cause feel as if it constrained its effect. Bayesian networks avoid counting
evidence twice by keeping forward messages (cause to effect) separate from backward messages
(effect to cause), as in Pearl's soldier-counting example; phlogiston theorists let the
backward inference from hot fire to phlogiston count again as a forward prediction, which is
what "hindsight bias" means in nontechnical terms. Since fake explanations are not labeled,
the only guaranteed check is to predict tomorrow's facts rather than yesterday's.

## 2. Sources checked

- Wikipedia, "Phlogiston theory" (raw wikitext, `data/sources/wp_phlogiston.txt`). Matched:
  "Soot was almost pure phlogiston"; "When the oxide was heated with a substance rich in
  phlogiston, such as charcoal, the calx again took up phlogiston and regenerated the metal"
  (a quoted source on Stahl); "Eventually, quantitative experiments revealed problems,
  including the fact that some metals gained mass after they burned, even though they were
  supposed to have lost phlogiston."
- Hasok Chang, "The Hidden History of Phlogiston", HYLE 16:2 (2010), 47-79,
  http://www.hyle.org/journal/issues/16-2/chang.pdf (`data/sources/chang2010_hyle.pdf`,
  `chang2010_raw.txt`). p. 59: "Musgrave (1976, p. 199) sets up the crucial moment of truth
  very nicely. The phlogiston program was highly progressive for a time, up to Joseph
  Priestley's prediction in 1783 that a metallic calx (or, oxide) would be reduced (turned
  back into shiny metal) through heating in inflammable air, which he considered to be
  phlogiston itself at that time. This prediction received a stunning corroboration in
  Priestley's experiment of heating minium (lead calx) in inflammable air". p. 60: "from this
  point on the phlogiston theory was forever on its back foot, adjusting itself this way and
  that way to accommodate inconvenient new findings but not managing to make any successful
  novel predictions." Also p. 50 on Kitcher and weight relations. Note: Chang himself argues
  the phlogiston theory was better than usually thought; I cite him only for Musgrave's
  account and the facts above.
- Gopnik et al., "A theory of causal learning in children: causal maps and Bayes nets",
  Psychological Review 111 (2004): 3-32. PubMed abstract (PMID 14756583,
  `data/sources/pubmed_14756583.txt`): "Children's causal learning and inference may involve
  computations similar to those for learning causal Bayes nets and for predicting with them."
- Pearl, "Reverend Bayes on Inference Engines: A Distributed Hierarchical Approach", AAAI-82
  (https://cdn.aaai.org/AAAI/1982/AAAI82-032.pdf, `data/sources/pearl1982_raw.txt`):
  "If a stronger belief in a given hypothesis means a greater expectation for the occurrence
  of a certain supporting evidence and if, in turn, a greater certainty in the occurrence of
  that evidence adds further credence to the hypothesis, how can one avoid an infinite
  updating loop when the two processors begin to communicate with one another?" and "the
  propagation of beliefs is governed by the traditional Bayes transformations on the
  relation P(D|H), which stands for the judgmental probability of data D (e.g., a combination
  of symptoms) given the hypothesis H". The paper treats trees.
- Murphy, Weiss and Jordan, "Loopy Belief Propagation for Approximate Inference: An Empirical
  Study", UAI 1999, arXiv:1301.6725 (`data/sources/murphy1999_loopy_raw.txt`). Quoting Pearl
  (1988), p. 195: "When loops are present, the network is no longer singly connected and
  local propagation schemes will invariably run into trouble ... messages may circulate
  indefinitely around the loops and the process may not converge to a stable equilibrium ...
  However, this asymptotic equilibrium is not coherent, in the sense that it does not
  represent the posterior probabilities of all nodes of the network". Also: "The algorithm is
  an exact inference algorithm for singly-connected networks".
- MacKay, *Information Theory, Inference, and Learning Algorithms* (2003), ch. 16
  (http://www.inference.org.uk/itprnn/book.pdf, `data/sources/mackay_itila.txt`, lines
  25255-25420): the soldier-counting rule set A and the remark that a group whose connections
  contain cycles cannot be split into "those in front" and "those behind". MacKay does not
  credit Pearl for the example.
- Pearl 1988 itself: the Internet Archive copy is borrow-only (401 on the text). I could not
  check the soldier metaphor in Pearl's book; the cpara says so.
- Brush, "Prediction and theory evaluation: the case of light bending", Science 246 (1989):
  1124-1129. PubMed abstract (PMID 17820957, `data/sources/pubmed_17820957.txt`): "while
  this success gained favorable publicity for the theory, most scientists did not give it any
  more weight than the deduction of the advance of Mercury's perihelion (a phenomenon known
  for several decades)."
- The two figures, downloaded and viewed (`data/sources/fakecaus_img1.png`,
  `fakecaus_img2.png`): Rain -> Sidewalk Wet -> Sidewalk Slippery; Phlogiston -> Fire Hot
  and Bright.

## 3. Arithmetic and technical checks

- Soldier counting: front soldier sends 1; the soldier behind receives 1 (one soldier ahead)
  and sends 2; so the forward message received equals the number ahead. Likewise backward.
  Total = ahead + behind + 1. Correct. (MacKay's figure 16.2: 3 + 1 + 1 = 5.)
- Screening off in the chain Rain -> Wet -> Slippery: P(Rain | Wet, Slippery) = P(Rain | Wet)
  because Slippery depends on Rain only through Wet (the Markov condition for a chain).
  Correct as stated.
- "No message bounces": Pearl's polytree algorithm is exact on singly connected networks;
  the post's example is one. The note adds the condition, with Pearl's own words.
- Bookkeeping and fitting (my derivation for the paragraph-18 note): message passing computes
  posteriors from given conditional probabilities. If P(Fire hot | Phlogiston) was set after
  seeing that fire is hot, conditioning on "fire is hot" uses the same observation twice
  (once to build the link, once as evidence), and nothing in the messages records this. So
  separating forward and backward messages does not detect it.

## 4. Claims about other posts

- "Einstein's Speed" (`data/originals/einstein-s-speed.md`, Posted 2008-05-21): "In our
  world, Einstein didn't even *use* the perihelion precession of Mercury, except for
  verification of his answer produced by other means." The note quotes this without the
  italics.
- "Guessing the Teacher's Password" says humanity "stayed stuck in holes like this for
  thousands of years"; this post is the next day's (2007-08-23 vs 2007-08-22).
- Consistency: our old note on "Making Beliefs Pay Rent" (order 13, file
  making-beliefs-pay-rent.tex) calls the phlogiston example "shaky (see notes)" but gives only
  the "alchemists" correction. The full historical criticism is made here (order 36). By
  STANDARDS 2.5 it should be at the first occurrence in book order, which is Making Beliefs
  Pay Rent ("this belief yielded no advance predictions"). The editor may want to move the
  full note there in the whole-book pass and leave a pointer here, or leave it here, where
  phlogiston is the subject. Later posts repeat the claim ("Occam's Razor", order 26: "like
  saying 'Phlogiston!'"; "Mysterious Answers", "Positive Bias"); they could point here.
- "Say Not Complexity" (order 40): our note there says the term "non-controlling causal node"
  is "never defined". This post, six days earlier, introduces "non-constraining causal node"
  and "unconstraining arrow" with the phlogiston figure. The Say Not Complexity note is true of
  that post taken alone, but the editor may want it to mention this post.

## 5. Not verified

- The soldier metaphor in Pearl (1988) (book not accessible).
- Pearl's p. 195 wording is taken from Murphy, Weiss and Jordan's quotation, and the note
  says so.
- Musgrave (1976) itself; I cite it through Chang.

## 6. Judgment calls

- The phlogiston cfact (paragraph 4) disputes the post's "You couldn't even use phlogiston
  theory to say what you ought not to see; it could explain everything." I wrote "The
  historical record is more mixed" and "overstated" (Response), not "false": the post's
  charge does fit the theory's later, ad hoc phase.
- The bookkeeping note (paragraph 18) says "Not shown" and rests on the derivation above plus
  Pearl's "judgmental probability". A defender could say "correct bookkeeping" includes
  recording which data built the network; the note says the post does not describe that.
  This is the technical claim the editor should check most carefully.
- The loops note (paragraph 14) is technically certain but may look like a limitation of scope
  rather than a fault; it matters because the post later promises that an AI would catch the
  problem by bookkeeping, and real causal networks often have loops.
- The Mercury note (paragraph 21): Brush's abstract says scientists gave light bending no
  more weight than Mercury; the note says exactly that. "Stated without exception" is fair to
  "It's the only way"; the post's "guaranteed" is a hedge of sorts, and the note does not
  call the rule wrong.
- The Response credits the technical material as "mostly accurate" (one sentence plus the
  Pearl 1982 confirmation).
- Pronouns: "he/his" for Priestley, Pearl and Einstein only.
