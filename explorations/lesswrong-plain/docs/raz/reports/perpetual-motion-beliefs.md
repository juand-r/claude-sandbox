# Report: Perpetual Motion Beliefs (order 191)

Agent: batch 4a. Slug: `perpetual-motion-beliefs`. Posted 2008-02-27.

## 1. The argument in three sentences

The previous post's conclusion, that accurate belief requires observation, implies that the laws
of probability are as binding as the laws of thermodynamics: a low probability is not a mere
suggestion one may ignore, any more than one may expect a smashed egg to reassemble or boiling
water to cool one's hand. People who believe without evidence build elaborate arguments, like the
man whose spreadsheet showed reactionless thrust, and somewhere in them a tiny probability is
turned into a large one. Adding more steps to such an argument only lowers its joint probability,
as adding gears only makes a machine less efficient.

## 2. Sources checked

- The quoted conclusion: `data/originals/the-second-law-of-thermodynamics-and-engines-of-cognition.md`,
  lines 130 and 149. Matched: "To form accurate beliefs about something, you really do have to
  observe it. It's a very physical, very real process: any rational mind does "work" in the
  thermodynamic sense, not just the sense of mental effort." and "So unless you can tell me which
  specific step in your argument violates the laws of physics by giving you true knowledge of the
  unseen, don't expect me to believe that a big, elaborate clever argument can do it either." The
  ellipsis skips the paragraphs between them. raz_check flags "true knowledge of the unseen" in the
  honest section as not in the post: it is in the post's quotation block, hard-wrapped across two
  lines in the original ("of the\nunseen"), which defeats the checker.
- Our notes on that post (order 190): Bennett (1982) on measurement vs. erasure; Jaynes's view of
  entropy "contested" (SEP). My two pointer notes rely on those notes and add nothing new.
- SEP, "Bayesian Epistemology" (`data/sources/sep_epistemology_bayesian.txt`, earlier agent):
  "there is the party of subjective Bayesians, who hold that every prior is permitted unless it
  fails to be coherent." Also "some coherent priors lead to Ockham's razor and some don't".
- "Burdensome Details" (linked by the post): conjunction rule; our notes there accept it.

## 3. Arithmetic recomputed

- "Your chance of guessing correctly by luck, is even less than the chance of the boiling water
  cooling your hand by luck": with N equally likely microstates and a set C of states that would
  cool the hand, P(guess the exact state) = 1/N <= |C|/N whenever C is non-empty. Correct (the
  post's "even less" is at most "no more than").
- Final comparison: {guessed state and not burned} is a subset of {not burned}, so its probability
  is at most P(not burned). Correct.
- "a few decillion": 10^33 each (short scale). No claim is made about the actual probability of
  reassembly, so I did not attempt one.
- Dates: 190 posted 2008-02-27T00:48Z, this post 2008-02-27T20:22Z; "Yesterday" fits the US date of
  the earlier post (26 February). No note.

## 4. Claims about other posts

- 190: quoted above; the note says its last paragraph and the bold sentence are quoted, which
  matches.
- The egg note says 190 called the second law probabilistic: 190 line "The Second Law of
  Thermodynamics is actually probabilistic in nature".
- The reactionless-drive note says 190 made the same argument: 190 paragraph beginning "A similar
  argument applies to a "reactionless drive"".
- "Beautiful Probability" is linked from "the laws of probability are theorems"; consistent with my
  notes there.

## 5. Not verified

- The anecdote about the man with the spreadsheet (unverifiable, and not faulted).

## 6. Judgment calls for the editor

- The main critical note (on "far more thin air than ground") says the tiny starting probability
  is a claim about priors, not one of the laws of probability. A defender could reply that the
  author holds an Occam or complexity prior and that the sentence states it. The note does not
  deny that; it says the post presents a claim about priors beside laws it calls "harder than
  steel" without marking the difference. I think this is the fairest form of the point.
- "No argument of this kind is analysed": checked the whole post. The lottery line and the
  boiling-water dialogue are the nearest; neither is an "edifice of justification". The spreadsheet
  is explicitly an analogy ("One must learn to see this as analogous"); the note now says so.
- "never shown" in the Response changed to "not shown" (reserved word).
- The school-regimen note says the explanation is "stated as fact, with no evidence". Mild; a
  defender could call it any essay's generalization. Kept because the post's diagnosis of why
  people discount probabilities is a factual claim about learning.
- Pronoun flag "his" in the Summary refers to the post's character ("his system of wheels and
  gears"), whom the post calls "he".
