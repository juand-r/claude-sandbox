# Report: Empty Labels (order 168)

Agent batch 3b. Scratch files and sources: `data/sources/b3b_disputing-definitions/`.

## 1. The argument in three sentences

In an "Aristotelian" system, where a category is defined by a list of properties, a label
like "zawa" carries no information beyond its definition, and the rules work just as well if
every label is replaced by its definition. Doing so to the Socrates syllogism, with "human"
defined as a mortal featherless biped, shows it to be an empty tautology: you cannot call
Socrates human until you have seen him die, so labels only create an "illusion of inference".
Hence the saying "you can define a word any way you like" should be replaced by "Definitions
don't need words": labels are dispensable, which is not the same as definitions having no
consequences.

## 2. Sources checked

All saved in `data/sources/b3b_disputing-definitions/`.

| Claim in our text | Source | Exact words matched |
|---|---|---|
| Mill, *A System of Logic* (1843), Book II, chapter 3, §2 | Project Gutenberg #27942 (`mill_logic.txt`, lines 6642-6652) | "It must be granted that in every syllogism, considered as an argument to prove the conclusion, there is a petitio principii. When we say, All men are mortal, Socrates is a man, therefore Socrates is mortal; it is unanswerably urged by the adversaries of the syllogistic theory, that the proposition, Socrates is mortal, is presupposed in the more general assumption, All men are mortal" (Gutenberg's layout puts the syllogism on separate lines) |
| Plato, *Cratylus*, Hermogenes (Jowett) | Project Gutenberg #1616 (`plato_cratylus.txt`, lines 2648-2655) | "any name which you give, in my opinion, is the right one, and if you change that and give another, the new name is as correct as the old" |
| Featherless biped from Plato's Academy | `data/originals/similarity-clusters.md` | "the philosophers of Plato's Academy claimed that the best definition of human was a "featherless biped"" |

Also read, not quoted: Aristotle, *On Interpretation* ch. 2 ("By a noun we mean a sound significant by convention", `aristotle_interp_clean.txt`), which supports the Cratylus point but was not needed; Diogenes Laertius VI.40 (`dl_book6.txt`), not used because Similarity Clusters already tells the story.

## 3. Arithmetic (the post's label algebra)

- zawa = [A, C, D]; yokie = [B, E]; xippo = [E, ~D].
- Object 1 is zawa, B, E, so it has A, B, C, D, E. It is yokie (B and E). It is not xippo (it has D). "Is it E?" follows from yokie alone. All as the post says.
- bolo = A, C, yokie = [A, C, [B, E]]; "bolo and A" = [A, C, [B, E]], A. Correct.
- mun = A, C, xippo = [A, C, [E, ~D]]; merlacdonian = bolo and mun = [A, C, [B, E]], [A, C, [E, ~D]]. Correct, and consistent (A, B, C, E, not D).

## 4. Claims about other posts

- The Parable of Hemlock (156) makes the syllogism point: "But then we can never know for certain that Socrates is a "human" until after Socrates has been observed to be mortal." It also treats the empirical case: "if I form the uncertain empirical generalization "Humans are vulnerable to hemlock", and the uncertain empirical guess "Socrates is human", logic can tell me that my previous guesses are predicting that Socrates will be vulnerable to hemlock."
- "which you may have noticed I hate": earlier statements in Words as Hidden Inferences ("It is a common misconception that you can define a word any way you like.") and Extensions and Intensions ("So that's another reason you can't "define a word any way you like""). So the claim that readers may have noticed is accurate; no note.
- Taboo Your Words (169) has a note on the recap of this post, calling the demonstration "rigged" because the definition contains "mortal", and crediting Mill. See judgment calls.

## 5. Not verified

Nothing in the notes depends on unverified material.

## 6. Judgment calls for the editor

- Mill (cfact) is information, not a fault; the post does not claim novelty. STANDARDS 2.5: the first occurrence in book order is The Parable of Hemlock (156), being annotated by another agent now. If that post carries the full Mill point, my note here and the Mill sentence in the Response should become a pointer ("see The Parable of Hemlock"). The Taboo Your Words note (169) then should point back too.
- Taboo Your Words' note calls this demonstration "rigged" because the definition contains "mortal" "because the author put it there". In Empty Labels the stipulation is explicit ("Let's say that "human" is to be defined as a mortal featherless biped"), and Hemlock treats the other horn. I did not repeat the "rigged" charge here, and I suggest the editor review that word in Taboo (reserved word, STANDARDS 2.3) in the whole-book pass.
- The Cratylus note (clogic) reads "This idea came from the Aristotelian notion of categories" as a historical claim. A fair defender could say "came from" means "rests on"; the note allows this in its last sentence.
- The "only" note (clogic) sets the post's last claim against its own earlier "a human convenience (or inconvenience)". The post's merlacdonian example was built to look "pointlessly confusing", so a defender could say the convenience is small; the note keeps to what the post itself conceded.
- Reserved words: "never" and "contradiction" are paraphrases of the post; "invents/invented" describe the post's coined labels.
