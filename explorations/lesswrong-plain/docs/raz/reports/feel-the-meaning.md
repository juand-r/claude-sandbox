# Report: Feel the Meaning (order 166)

Agent batch 3b. Scratch files and sources: `data/sources/b3b_disputing-definitions/`.

## 1. The argument in three sentences

Language is a complicated, partial transfer of thoughts ("telepathy"), but the brain hides
the complexity: by design, hearing a word activates its concept with no intermediate step,
as in the post's blegg network with a direct link from the word unit to the central unit.
From the inside, word and concept therefore feel almost identical, so a word seems to have a
meaning as an intrinsic property (a case of Jaynes's Mind Projection Fallacy). That feeling
is what keeps Albert and Barry arguing about what "sound" really means, as if it were a fact,
until they try to state a testable experiment.

## 2. Sources checked

All saved in `data/sources/b3b_disputing-definitions/` unless noted.

| Claim in our text | Source | Exact words matched |
|---|---|---|
| The diagram (Network 3, speech bubble "Blegg!" linked to the central unit) | Image fetched from https://www.lesswrong.com/static/imported/2008/02/12/blegg4_4.png (`blegg4_4.png`) and viewed | Labels: "Color: +blue / -red", "Shape: +egg / -cube", "Luminance: +glow / -dark", "Texture: +furred / -smooth", "Interior: +vanadium / -palladium", "Category: +BLEGG / -RUBE", bubble "Blegg!", caption "Network 3" |
| Ogden and Richards, *The Meaning of Meaning* (1923) | Internet Archive `meaningofmeaning00ogde` (seventh edition text; `ia_meaningofmeaning00ogde.txt`, pp. 9-10) | "Words, as every one now knows, ' mean ' nothing by themselves, although the belief that they did, as we shall see in the next chapter, was once equally universal." (OCR spacing; I quote with an ellipsis for "as we shall see in the next chapter,") |
| Jaynes's definition of the Mind Projection Fallacy | `data/sources/jaynes_book_ch1-3.txt` (Probability Theory: The Logic of Science, 1995 draft, chapter 1, lines 1585-1596) | "The latter statement is ontological, asserting the physical existence of something, while the former is epistemological, expressing only the speaker's personal perception." ... "To interpret the first kind of statement in the ontological sense is to assert that one's own private thoughts and sensations are realities existing externally in Nature. We call this the "Mind Projection Fallacy,"" |
| Tip-of-the-tongue; Brown and McNeill (1966) read out definitions | Wikipedia, "Tip of the tongue" (`wiki_tot.txt`, secondary); Schwartz and Metcalfe (2011) abstract, PubMed 21264637 (`pubmed_21264637_tot.txt`) | Wikipedia: "Brown and McNeill read out definitions (and ''only'' the definitions) of rare words to the study participants, and asked them to name the object or concept being defined." Schwartz and Metcalfe: "TOTs have been studied experimentally since the seminal work of Brown and McNeill (1966)." |
| Title "“Science” as Curiosity-Stopper" | `data/originals/science-as-curiosity-stopper.md` | first line |

## 3. Arithmetic

None. Dates: How an Algorithm Feels From Inside 2008-02-11, this post 2008-02-13 ("two days before" in the Response); Mind Projection Fallacy 2008-03-11 (order 196).

## 4. Claims about other posts

- "This is the term's first appearance in the book": `grep -il "mind projection"` over `data/originals/` gives posts dated 2008-03 or later, plus A Technical Explanation (2005) and The Intuitions Behind Utilitarianism (2008-01-28). Both come later in the book (Intuitions is order 291; A Technical Explanation is order 261). So within the book, order 166 is first.
- How an Algorithm Feels From Inside: our afterword there says Network 2 is offered with engineering reasons ("fast, cheap, scalable") and no evidence about brains. The figure note here points to it rather than repeating it.
- Words as Hidden Inferences has the tiger ("Yikes! A tiger!"); Neural Categories has Network 2.

## 5. Not verified

- Brown and McNeill (1966) itself (paywalled); I rely on Wikipedia's summary and the Schwartz-Metcalfe abstract.
- Whether the 1923 first edition of Ogden and Richards has exactly the same wording as the seventh edition I read. The sentence is in chapter 1 and is likely unchanged, but I did not see the first edition.

## 6. Judgment calls for the editor

- The tip-of-the-tongue note (clogic) answers a hedged claim ("on most occasions", "perhaps"). I attack it as hedged: the note begins "Offered with 'perhaps' and no evidence" and gives a counter-case to the "only ... while learning a new language" clause. The In short line says "sits uneasily with", not "contradicts".
- The design-argument point is made in full in How an Algorithm Feels From Inside; here it is a short pointer in the figure note and one paragraph of the Response. The editor may prefer to shorten the Response paragraph further (STANDARDS 2.5).
- Ogden and Richards is credit (information), not a fault; the post credits Jaynes for the general pattern.
- I considered and dropped: Putnam's externalism ("meanings just ain't in the head") against the pseudo-code; the post describes processing, not a theory of meaning, so this would import a general dispute. Also dropped a note on the post's "telepathy" relabeling (a joke) and on language models meeting the "build a computer" test (no bearing on the argument).
- Layout: one overfull box (39pt) in the post's own pseudo-code line; post text, not ours.
