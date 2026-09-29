# Report: the-generalized-anti-zombie-principle ("The Generalized Anti-Zombie Principle", Yudkowsky, posted 2008-04-05; book order 227)

## 1. The argument in three sentences

Taking as settled that consciousness is, among other things, the cause of our talk about consciousness, the post asks how far the anti-zombie argument generalizes, and answers that any change which cannot plausibly alter the causes of that talk (a switch flipped across the room, a word heard) should not be expected to switch consciousness off. It concedes that this version is about expectations, not certainty, because every physical change has some tiny effect, but holds that effects far below thermal noise cannot matter. It closes with a dialogue about replacing neurons one by one with functionally identical robots, says the principle supports the view that the result is still you, and defers the reasons to later posts.

## 2. Sources checked

Scratch folder: `data/sources/4b_zombie-responses/` (shared with my other slug).

| Claim in our text | Source | Exact words matched |
|---|---|---|
| Descartes epigraph | Project Gutenberg #13846, Discours de la méthode (`descartes_discours_fr.txt`, Part II) | "et chaque vérité que je trouvois étant une règle qui me servoit après à en trouver d'autres" |
| Earlier replacement scenarios | Chalmers, "Absent Qualia, Fading Qualia, Dancing Qualia" (1995), https://consc.net/papers/qualia.html, `chalmers_qualia.txt` | "Neural replacement scenarios along the lines discussed in this section are discussed by Pylyshyn (1980), Savitt (1980), Cuda (1985), and Searle (1992), among others." (I left out Savitt: the text says 1980, the bibliography 1982.) |
| Searle's outcome | same file, quoting Searle, The Rediscovery of the Mind, pp. 66-67 | "We imagine that your conscious experience slowly shrinks to nothing, while your externally observable behavior remains the same." and "Here, Searle embraces the possibility of Fading Qualia" |
| Switch and noticing | Chalmers, "Facing Up to the Problem of Consciousness" (JCS 2(3), 1995), https://consc.net/papers/facing.html, `chalmers_facing.txt` | "install alongside it a causally isomorphic silicon circuit, with a switch between the two"; "whenever experiences change significantly and we are paying attention, we can notice the change"; conclusion "any two functionally isomorphic systems must have the same sort of experiences" |
| Penrose | Wikipedia, "Shadows of the Mind" (raw, `wp_shadows.txt`) and "Orchestrated objective reduction" (`wp_orch_or.txt`) | "Human consciousness is non-algorithmic, and thus is not capable of being modelled by a conventional Turing machine type of digital computer."; objective reduction "related to the difference of the spacetime curvature"; Orch OR "combines ... quantum gravity" |
| Neutron size | Wikipedia "Neutron" (raw, `wp_neutron.txt`) | "The neutron has a mean-square radius of about 0.8e-15 m" |
| Z versus E pointer | see the report on zombie-responses (Chalmers comment of 8 April 2008) | |

## 3. Arithmetic

- Pull of a one-gram switch at ten metres: a = G m / r^2 = 6.674e-11 x 1e-3 / 100 = 6.67e-16 m/s^2.
  The post says "around 6 * 10-16": correct.
- Neutron diameter about 1.6 to 1.7 fm (radius about 0.8 fm). 6.67e-16 / 1.7e-15 = 0.39 diameters
  per s^2. The post says "around half": close enough; no note beyond confirming.
- Not in a note (below the threshold, the point survives): the figure is the pull of the whole
  switch, which is there whether or not the switch is flipped. Flipping changes the pull only by
  moving the switch's parts. If the whole gram moved 1 cm toward you, the change would be
  G m 2 d / r^3 = 6.674e-11 x 1e-3 x 0.02 / 1000 = 1.3e-18 m/s^2, about 500 times smaller.
  Displacement from that change: 0.5 a t^2 reaches one neutron diameter after about 50 seconds
  (1.41 diameters at t = 60 s), so "nudges them by whole neutron diameters" still holds within a
  minute. Also, a uniform pull moves the whole body together; only the tidal part changes relative
  positions, which the post mentions later. None of this changes the argument (the effect is tiny
  but not zero, and far below thermal noise), so it stays out of the notes.

## 4. Claims about other posts

- "Identity Isn't In Specific Atoms" (fetched: data/originals/identity-isn-t-in-specific-atoms.md,
  posted 2008-04-19): "**Followup to**: The Generalized Anti-Zombie Principle" and "There are many
  possible formulations of the GAZP, but one of the simpler ones says that, if alleged gigantic
  changes are occurring in your consciousness, you really ought to *notice something happening,*
  and be able to say so."
- "Timeless Identity" (fetched: data/originals/timeless-identity.md, posted 2008-06-03) refers back
  to this post ("I earlier talked about any perturbation which does not disturb your internal
  narrative ...") and applies the reasoning to vitrification: "there is nothing preserved from one
  night's sleep to the morning's waking, which cryonic suspension does not preserve also."
- Neither post is in the manifest of Rationality: A–Z (checked by slug and title).
- "Zombie Master" as a chatbot: "Zombies! Zombies?" ("feed them into a non-conscious but
  sophisticated AI ... That is just a holodeck").
- Step 4 of "Zombie Responses": "refers to that-which-is or that-which-causes or
  that-which-makes-me-say-I-have inward awareness" (consistent with "among other things" here).

## 5. Not verified

- The count behind "a considerable majority of Overcoming Bias commenters do accept this": not
  attempted (the comments are in `zombies_zombies_comments.json` if the editor wants it). The note
  only says the post gives no count.
- Penrose: checked only against Wikipedia's summaries, not the books.
- Searle's own text (pp. 66-67): read only as quoted by Chalmers.

## 6. Judgment calls for the editor

- The prior-work notes (Albert's first line; Bernice; Albert's "notice" line; Response paragraph 2)
  are framed as credit and information: the post does not claim the thought experiment is new, and
  Chalmers's argument supports Albert. The In short line mentions it as history, not as a fault.
- The logic note on "pretty much the same" (the principle does not yet cover the robot case) is my
  reading, but the post itself defers the robot case, so I described it as scope.
- "Not in this book" for the identity posts: a neutral note, per the Book III lesson on the editors'
  selection.
- Z versus E: here only a pointer to "Zombie Responses"; see that report for the placement question
  (the full point may belong at order 225).
- Honest section is 711 words, within the 900 allowed for this longer post. Summary is 188 words
  (the post has 2,871 words).
- No reserved words were flagged.
