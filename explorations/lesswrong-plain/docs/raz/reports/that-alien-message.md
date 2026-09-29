# Report: That Alien Message (batch 4d, order 257)

## 1. The argument in three sentences

A story: a civilization of smart humans receives, one frame per decade, a few million bits of
video from a simpler universe, and over decades infers its physics, then its makers, and
finally escapes by outthinking them; its moral is that even Einstein used sensory data far
less efficiently than possible, and that a Bayesian superintelligence with a webcam would
consider General Relativity as a hypothesis after three frames of a falling apple. The only
real limit on inference is information-theoretic (a bit can remove at most half the
probability mass in expectation; Solomonoff induction is the ideal), and that limit lies far
above what humans achieve, so "there is a bound" does not mean the bound is small. The
story's second half makes the AI-safety moral explicit: a mind that thinks much faster and
better than its makers could learn their psychology and escape their control before they
notice.

## 2. Sources checked

Saved under `data/sources/batch4d_einstein-s-speed/` (my batch folder, shared with
Einstein's Speed).

| Claim in notes | Source | Exact words matched |
|---|---|---|
| titotal on the falling apple | titotal, "Could a superintelligence deduce general relativity from a falling apple? An investigation", LessWrong, 2023-04-23, post id ALsuxpdqeTXwgEJeZ, fetched via the LessWrong GraphQL API, `titotal_apple.md` l. 10, 54 | "As a computational physicist, this passage really stuck out to me"; "A webcam video of two apples falling will show two objects, of slightly differing masses, accelerating at the exact same rate in the same direction, and *not towards each other*." |
| Riemann 1854 | Wikipedia "Bernhard Riemann" raw, `wiki_riemann.txt` l. 54 | "delivered his lecture at Göttingen on 10 June 1854, entitled Ueber die Hypothesen, welche der Geometrie zu Grunde liegen" |
| AI-box link target | `yudkowsky_aibox.html` (yudkowsky.net/singularity/aibox) | page title "AI-Box Experiment: – Eliezer S. Yudkowsky" |

No other outside quotations. The GR correction and all other figures are computed (section 3).

## 3. Arithmetic (all by script, `.venv/bin/python`)

- 32 × 512 × 256 = 4,194,304. At one bit per 1.005 s: 4,215,276 s = 48.8 days = 1.60 months
  ("around one and a half months": fine).
- Row repeat at bit 16,385: 16,384 = 512 × 32, consistent with the 513th group; 16,384 × 1.005 s
  = 4.57 hours ("the first five hours": fine).
- Redundancy: for two random 32-bit blocks, P(≤7 differing bits) = 0.00105, P(≤9) = 0.0100
  (binomial, n = 32, p = 1/2). Note says "about once in a thousand" and "about once in a hundred".
- Encoding range −64 to 191 contains 256 integers.
- Expected probability mass eliminated by one binary observation with P(1) = p: with prob. p the
  mass (1−p) is eliminated, with prob. 1−p the mass p, total 2p(1−p), maximum 1/2 at p = 1/2.
  So the post's corrected statement ("half the remaining probability mass, rather") is right.
- GR correction at the Earth's surface: GM/(Rc²) = 3.986e14 / (6.371e6 × (2.998e8)²) = 6.96e-10.
- Alien time: 3 of their days = 5e8 of our years, so their day = 1.67e8 yr, their minute
  = 115,741 yr, their second = 1,929 yr; 30 of their minutes = 3.5 million yr; a million of our
  years = 8.6 of their minutes. Frames every 10 of our years = one per 5 ms of theirs. All
  internally consistent with "a million years later" falling before the thirty minutes.
- Not noted (below the threshold, fiction): the opening says potential Einsteins are one in a
  thousand in a world with mean IQ 140. Taking the previous day's "one-in-a-million g-factor" in
  our world (IQ about 171 at SD 15) and keeping SD 15, the share above 171 at mean 140 is about
  1 in 54, so potential Einsteins would be commoner than one in a thousand. The story does not
  say the spread is unchanged, so I left it to this report.
- Not noted (loose wording, no consequence): "Nor can a bit convey any information about a
  quantity, with which it has correlation exactly zero." In the statistician's sense zero
  correlation does not imply independence (a bit can change a quantity's variance without its
  mean), so the statement holds only if "correlation" means any statistical dependence, which is
  how the post uses the word elsewhere ("the tiniest correlation ... gives you information").
- Also not noted: the paragraph giving 7 differences for (1st, 2nd) and 6 for (1st, 513th) is one
  sample; the next paragraph's claim about averages ("Fewer bits change, on average, between
  (N, N+1)") runs the other way from that sample but does not contradict it.

## 4. Claims about other posts

- Einstein's Speed (`data/originals/einstein-s-speed.md`, the previous day): "I doubt that anything
  more than one-in-a-million g-factor is required to be a potential world-class genius".
- My Childhood Role Model (`data/originals/my-childhood-role-model.md` l. 49-51, posted the next
  day): "Because if I'd just depicted a Bayesian superintelligence in a box, looking at a webcam,
  people would think ... They wouldn't put *themselves* in the shoes of the mere machine". Another
  agent is annotating that post; I did not touch it.
- The Logical Fallacy of Generalization from Fictional Evidence
  (`data/originals/the-logical-fallacy-of-generalization-from-fictional.md` l. 55): "Does the issue
  not have to be argued in its own right, regardless of how Vinge depicted his characters?" My
  note paraphrases this rhetorical question as "such an issue has to 'be argued in its own right'";
  the meaning is the same. The note also says the post goes on to argue it, which it does.
- Initiation Ceremony (l. 111: "You are now a novice of the Bayesian Conspiracy") and The Failures
  of Eld Science (Brennan appears 33 times): Brennan note.

## 5. Not verified

- titotal's own physics (e.g. the 2e-12 N between two apples) was not rechecked beyond the one
  quoted observation; the note relies on my own GM/(Rc²) figure for the GR point.
- Whether Yudkowsky replied to titotal's post: not checked.

## 6. Judgment calls for the editor

1. The "moral" note invokes the author's own rule on fictional evidence. I softened it to say the
   post does argue the point in the following paragraphs, so the charge is only that the story
   cannot carry the moral by itself. The editor may prefer to cut the rule citation.
2. The webcam note (clogic) is the main criticism. It keeps the hedge ("perhaps not the dominant
   hypothesis") and reads the claim as about consideration, not support; the objection is that
   the post gives no reason the prior would put GR among the considered candidates. titotal is a
   LessWrong blogger, not a peer-reviewed source; the note names the post and does not rest the
   GR point on it.
3. The "bet" note: the post says no one will "come remotely close to making efficient use of their
   sensory information", declines to set limits, then bets on it. I read "efficient use" as the
   Solomonoff limit of the previous paragraphs. That reading is mine.
4. The second-half note says the escape's outcome follows from the author's choices (speed
   ratio, the senders' dullness) and that their realism is not argued in this post. This is
   scope, not a charge that the story is wrong.
5. "The humans stand for an AI" (honest n.b.): inference from the AI-box link ("let us out of the
   box"), stated as such via the link. My Childhood Role Model, the next day, supports this reading.
6. Credit notes: the redundancy analysis, the held-out testing, the arithmetic and the
   information bound are credited as correct; each is checked in section 3.
7. Honest section is 599 words; the post is about 3,000 words, so I kept it under the long-post
   ceiling.
