# Report: the-design-space-of-minds-in-general ("The Design Space of Minds-In-General", Yudkowsky, posted 2008-06-25; book order 269)

## 1. The argument in three sentences (written before annotating)

Asking what "AIs" will do is a trick question, because "AI" names not a natural class like
"human" (humans share one brain architecture, as a sexually reproducing species) but the
whole space of possible minds, which the post pictures as a sphere in which humans are a
tiny dot inside transhuman and posthuman regions, the whole floating in a larger space of
optimization processes that includes natural selection. Since the minds specifiable in a
trillion bits number about two to the trillionth power, any universal claim about minds has
that many chances to be false and any existential claim that many chances to be true, so
one should resist saying that all minds, or no minds, do something. The usual source of such
claims is imagining oneself in the mind's place, which gives an anthropomorphic answer; one
should instead reason about what a particular mind's makeup lawfully causes, and not define
away minds that behave differently.

## 2. Sources checked

Local copies in `data/sources/batch05a_the-design-space-of-minds-in-general/` (curl, 29 Sept
2026, User-Agent "raz-annotation-research").

1. The post's diagram, `mindspace_2.png` (536 x 536), fetched from the image URL in the post
   (http://lesswrong.com/static/imported/2008/06/24/mindspace_2.png, still served). I viewed
   it. Labels read: "Minds-in-general" (sphere), "Posthuman mindspace" (tall ellipse),
   "Transhuman mindspace" (small oval at its base), "Human minds" (dot), "Bipping AIs",
   "Freepy AIs", "Gloopy AIs". The note's description is from this image.
2. Wikipedia, "Rotating locomotion in living systems" (raw, `wp_rotating_locomotion.txt`).
   Matched: "The first, [[ATP synthase]], is a transmembrane enzyme used in the process of
   energy storage and transfer in all known organisms." Also: "There are two known examples
   of molecular-scale rotating structures used by living cells" (ATP synthase and the
   flagellar motor), and archaella driven by rotary motors "structurally and evolutionarily
   distinct from bacterial flagella". So the post's "one of three known occasions" is
   defensible (ATP synthase, bacterial flagellum, archaellum); the article also mentions the
   crystalline style of some molluscs. Not noted (nitpick).
3. Quintin Pope, "My Objections to 'We're All Gonna Die with Eliezer Yudkowsky'", LessWrong,
   2023-03-21 (post id wAczufCpMdaamF9fy, fetched via the LessWrong GraphQL API,
   `pope_objections.json` / `.txt`). Matched: "As a consequence, it's a bad idea to use "the
   size of mind space" as an intuition pump for "how similar are things from two different
   parts of mind space"?" (the note drops the final question mark and uses LaTeX single quotes
   for the inner quotes); "The manifold of possible mind designs for powerful, near-future
   intelligences is surprisingly small." Pope is answering a 2023 podcast statement of the
   same picture ("imagine like this giant sphere, and all the humans are in this like one tiny
   corner of the sphere"), not this post directly.
4. Aaron Sloman, "The structure of the space of possible minds", in S. Torrance (ed.), The Mind
   and the Machine, Ellis Horwood, 1984, pp. 35-42; HTML at
   https://www.cs.bham.ac.uk/research/projects/cogaff/sloman-space-of-minds-84.html
   (`sloman_space_of_minds.txt`). Matched: "Clearly there is not just one sort of mind."; "My
   aim for now is not to do it -- that's a long term project -- but to describe the task."
   (basis for "described the task of mapping it" in the Response); the paper also argues
   against "a single sharp division, between those with minds ... and those without".
5. Wikipedia, "AIXI" (raw, `wp_aixi.txt`). Matched: "Like [[Solomonoff induction]], AIXI is
   [[Undecidable problem|incomputable]]."; "Colloquially, this means that it doesn't consider
   itself to be contained by the environment it interacts with." The post's link
   (http://www.hutter1.net/ai/) is a frameset; I did not use it.

## 3. Arithmetic

- Bit strings of length 0 to n number 2^(n+1) - 1. For n = 10^12 that is about
  2^(10^12 + 1), twice the post's "two to the trillionth power". Not worth a note; the note
  says "about $2^{10^{12}+1}$" and calls the count right.
- Dates: "The Psychological Unity of Humankind" posted 2008-06-24, this post 2008-06-25 ("the
  day before").

## 4. Claims about other posts

- "The Psychological Unity of Humankind" (not in the book; `data/originals/the-psychological-
  unity-of-humankind.md`, line 17): "In a sexually reproducing species, *complex* adaptations
  are necessarily universal." Quoted without the italics. Not in the manifest (checked).
- "Ghosts in the Machine" (order 148, `data/originals/ghosts-in-the-machine.md`): the reaction
  "if the AI can modify its own source code, it'll just remove any constraints you try to
  place on it" and the reply that the decision must come from the source code. Matches the
  post's "the ghost in the machine will look over the corresponding source code and hand it
  back".
- "Arguing 'By Definition'" (order 174): named only as where the error is treated.

## 5. Not verified

- "ATP synthase has not changed significantly since the rise of eukaryotic life two billion
  years ago." Not checked beyond the conservation statement above (ATP synthase predates
  eukaryotes, being present in bacteria; the claim is about conservation). Not noted.
- The post's link to Hutter's page is a frameset; the AIXI description rests on Wikipedia.

## 6. Judgment calls for the editor

- The main criticism (note on "Asking what 'AIs' will do", Response paragraph 2, honest n.b.,
  In short): the post moves from the size of the space of possible minds to an answer about
  the AIs that will be built. I framed it as scope ("does not consider") with Pope as the
  source. A fair defender could say that in 2008 no one knew which designs would be built,
  so "minds-in-general" was the honest reference class. I think the note survives this,
  because the post's own reason for humans' natural class (shared architecture) applies to
  AIs made by shared methods, but the editor may prefer to soften the In short line.
- Pope's objection is from 2023 and answers a later spoken version of the same picture.
  I cite it as a source for the objection, not as a reply to this post.
- The count note (a "clarification of scope" note): the count is right; it does not threaten
  universal claims that follow from what all specifiable minds share. I kept it mild and
  pointed to the post's own "almost any". It could be judged a nitpick; I kept it because
  the count is the post's only argument for its moral.
- "I take that to be what 'can't even recognize itself in a mirror' refers to" (AIXI): marked
  as my reading.
- No reserved words are used.
