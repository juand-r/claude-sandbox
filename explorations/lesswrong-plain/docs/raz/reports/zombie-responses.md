# Report: zombie-responses ("Zombie Responses", Yudkowsky, posted 2008-04-05; book order 226)

## 1. The argument in three sentences

Replying to Richard Chappell's comment on "Zombies! Zombies?", the post separates "apparently conceivable" from "logically possible", sets out a seven-step argument that, if (as seems empirically likely) inward awareness causes our talk of awareness, the zombie world is logically impossible, and holds that the law aligning epiphenomenal experience with physical talk is an extra improbable postulate. It answers the claim that zombie utterances are meaningless by saying that accuracy can be judged from the physical, map-making system alone. It then adds the missing premise of the previous day's AI argument (a reflective mind enforces global reliability by checking each part for local reliability) and concedes that its etymology of N'Shama was wrong.

## 2. Sources checked

Scratch folder: `data/sources/4b_zombie-responses/` (comments JSON and a readable dump
`zz_comments.md`, Chalmers papers as `.html` and `.txt`, Wiktionary raw pages, Tiling Agents PDF,
and `tools/` with the note-insertion script and the note lists used to build the post file).

Comments (LessWrong GraphQL, `comments.py`; the comments of "Zombies! Zombies?" and of this post):

| Claim in our text | Source | Exact words matched |
|---|---|---|
| All four Chappell quotations in the post | comment 5YEY3LQXGzpb8apkG (Richard4, 2008-04-04 15:37) | match, except the comment has "you view" where the post has "your view" |
| Chappell's comparison and "primitive facts" | same comment, point (2) | "it's "miraculous" in the same sense that it's "miraculous" that our universe is fit to support life"; "They are *primitive* facts, not explained by anything *else*, but that doesn't make them chancy." |
| Reason for meaninglessness | same comment, point (3) | "beliefs are partly constituted by the phenomenal properties instantiated by their neural underpinnings" |
| Point (4) | same comment | "I don't see how it counts against this view, unless you illicitly assume a causal theory of knowledge (which I obviously don't)." |
| Postscript | same comment | "Note that while I'm a fan of epiphenomenalism myself, Chalmers doesn't actually commit to the view." |
| Step 4 "question-begging" | comment CX5ovfNs5vAJazg4s (Richard4, 2008-04-05 17:46) | "You can save the logical validity of the argument by tidying up (4) ... But then it's a false premise, or at least question-begging" |
| Author's reply | comment 4rdWkDzALSaaQts56 (2008-04-05 19:19) | "I've done so, since I regard this as as a simple writing error." and "This introduces problems of reference, problems of epistemic justification" |
| "empirical question" | comment JY6Qi37y3qnPujsFJ (Richard4, 2008-04-07) | "it can't be an empirical question what's logically possible" |
| Chalmers on Z and E | comment 5qKe5gQ8HWgfRq9Dw (David_Chalmers, 2008-04-08, on "Zombies! Zombies?") | "I endorse Z, but I don't endorse E"; "the correct conclusion of zombie-style arguments is the disjunction of the type-D, type-E, and type-F views" |
| Author's reply to Chalmers | comment chZLkQ8Piu4J5ibC9 (2008-04-08) | "there is a direct, two-way logical entailment between "consciousness is epiphenomenal" and "zombies are logically possible"" |
| N'Shama commenter | comment i7ERMzyqx7zKWNHY8 (anon., 2008-04-04) | matches the post's quotation exactly |

Chalmers, "Consciousness and its Place in Nature" (https://consc.net/papers/nature.html, saved as
`chalmers_nature.txt`; published 2002 and 2003):
- type-A: "According to type-A materialism, there is no epistemic gap between physical and phenomenal truths; or at least, any apparent epistemic gap is easily closed." Eliminativism and analytic functionalism as forms of type A: "Type-A materialism sometimes takes the form of eliminativism ... It sometimes takes the form of analytic functionalism".
- type-B: "According to this view, zombies and the like are conceivable, but they are not metaphysically possible."; water/H2O model.
- conceivability: "Let us say that S is conceivable when the truth of S is not ruled out a priori." "The type-B materialist grants premise (1): to deny this would be to accept type-A materialism."
- two-dimensional argument, footnote: "This is a slightly more formal version of an argument in Chalmers 1996 (pp. 131-36)."; XYZ world: "There is no reason to doubt that the XYZ-world is metaphysically possible."; "if something feels conscious, it is conscious."
- lucky coincidence: "the relationship between consciousness and reports about consciousness seems to be something of a lucky coincidence, on the epiphenomenalist view" and "there is at least a significant burden of proof here."
- constitution: "an epiphenomenalist can deny that knowledge always requires a causal connection" and "consciousness plays a role in constituting phenomenal concepts and phenomenal beliefs."

Chalmers, "Does Conceivability Entail Possibility?" (https://consc.net/papers/conceivability.html,
`chalmers_conceivability.txt`; published 2002): "S will be prima facie conceivable for a subject
when that subject cannot (after consideration) detect any contradiction in the hypothesis expressed
by S." and "S will be ideally conceivable when ideal rational reflection detects no contradiction in
the hypothesis expressed by S".

Hebrew: Wiktionary raw pages (`wikt_neshama.txt`, `wikt_shama.txt`): נשמה root "נ־שׁ־ם", sense 1
"(biblical) breath"; שמע root "שׁ־מ־ע", "to hear". The final letter ע is ayin.

Tiling Agents (http://intelligence.org/files/TilingAgents.pdf, `tiling.pdf`/`tiling.txt`): "Yudkowsky,
Eliezer; Herreshoff, Marcello; October 7, 2013 (Early Draft)"; abstract on "tiling" agents that
approve similar successor agents.

## 3. Arithmetic

None in this post.

## 4. Claims about other posts

- "Zombies! Zombies?" (data/originals/zombies-zombies.md) uses "deranged": "this separable outer
  Chalmers is deranged" and "the most deranged idea in all of philosophy".
- Its current text still has "N'Shama—"the hearer"" (paragraph 4) and "the N'Shama, the hearer".
- "Zombies! Zombies?" reports the zombie-ist view: "The Zombie World may not be *physically*
  possible, say the zombie-ists ... but the Zombie World is *logically* possible: the bridging laws
  could have been different." (used in the note on reliability across worlds).
- The (B) block quote differs in its second paragraph from the current text of "Zombies! Zombies?",
  which reads "A good AI design should, I think, look like a reflectively coherent intelligence
  embodied in a causal system, with a *testable* theory of how that selfsame causal system produces
  ...". Same meaning; probably a later edit of either post. Not noted in the margin (nitpick).
- "The Simple Truth" is in this book (manifest order 49).

## 5. Not verified

- The Conscious Mind, pp. 131-36: cited from the footnote in Chalmers 2003, not read.
- Which part of the Tiling Agents draft the 2013 edit's "section 6" means. In the draft I found,
  section 7 is "Probability and expected utility"; I could not see a section on modular local
  reliability. The note says only that I did not check; it makes no charge.
- Whether the printed book edition of "Zombies! Zombies?" still has the N'Shama gloss (I checked
  only the LessWrong text).
- Step 4 was edited after publication: the author's comment says "think" was changed to "say" after
  Chappell's objection. Per STANDARDS 2.5 the note annotates the current text and does not use the
  revision as a criticism; Chappell's "question-begging" was said of the tidied ("say") version.

## 6. Judgment calls for the editor

- Z versus E (note at "argument for epiphenomenalism", Response "Fourth"). Chalmers's comment
  (8 April) came after this post; the fault charged to the post is only that it leaves out Chappell's
  postscript, which it had. The full point (Chalmers endorses Z but not E) probably belongs in full
  at "Zombies! Zombies?" (order 225, another agent's post) under STANDARDS 2.5; if that agent makes
  it, this note could become a pointer. I kept it here because this post quotes the comment that
  raised it.
- Type-B classification (notes at step 7 and the Twin Earth paragraph; Response "Second"). The claim
  "In Chalmers's terms this is not the type-A view" applies Chalmers's own definitions ("conceivable
  = not ruled out a priori"; "to deny this would be to accept type-A materialism"). The post uses
  "logically possible" in its own sense; the notes say "in Chalmers's terms". A defender could say
  the post denies even ideal conceivability; but step 7 rests the impossibility on an empirical
  premise, which on Chalmers's definition leaves conceivability intact.
- Texas note ("has nothing to compare the belief with"): my own logical reading of the example, not
  sourced. I think it is safe because the post itself says the epiphenomenal core is undetectable.
- Reliability-across-worlds note (part B): also my reading. It states what the premise does and
  asks why, rather than asserting an error. The editor may prefer to cut it as speculative.
- The note on type-A ("The label fits in part, which is what the post says") is a judgment on how
  far Chalmers's definition fits; it agrees with the post.
- Reserved words flagged by raz_check: "wrong" (the post's own concessions; "asked the wrong way"
  is the post's phrase), "contradiction" (Chappell's request). No reserved word is used as a charge.
- The Response covers four separate points and is near the top of the length guideline; the
  honest section is 561 words, a little above the 500 guideline for a post of this length.
