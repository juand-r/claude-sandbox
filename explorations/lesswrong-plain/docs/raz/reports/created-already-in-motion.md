# Report: created-already-in-motion ("Created Already In Motion", Yudkowsky, posted 2008-07-01; book order 273)

## 1. The argument in three sentences (written before annotating)

In Lewis Carroll's "What the Tortoise Said to Achilles", each time Achilles writes the rule of
inference down as a further premise the Tortoise asks for yet another, and the regress never
ends; the post's lesson is that a mind needs the dynamic of actually performing modus ponens,
which no premise can supply, so a mind must be "created already in motion" and no argument can
move a rock. In the same way, a mind that believes "pulling the toddler off the tracks is
fuzzle" will not act unless it implements a dynamic that sends fuzzle plans to action, and
beliefs about such dynamics, or proofs that minds with them are more fuzzle, do not help unless
the mind already has the dynamic of adopting code believed more fuzzle. Hence you cannot argue
fuzzleness into a rock.

## 2. Sources checked

Local copies in `data/sources/5a_my-kind-of-reflection/` (curl, 29 Sept 2026).

1. Carroll, "What the Tortoise Said to Achilles", Mind 1895, Wikisource transcription of the
   scan (https://en.wikisource.org/w/index.php?title=What_the_Tortoise_Said_to_Achilles&action=render,
   `carroll_wikisource.txt`). Every quotation in the post checked:
   - (A), (B), (Z): identical.
   - Tortoise: "And if some reader had not yet accepted A and B as true, he might still accept
     the sequence as a valid one, I suppose?" identical.
   - Achilles: "No doubt such a reader might exist. He might say 'I accept as true the
     Hypothetical Proposition that, if A and B be true, Z must be true; but, I don't accept A and
     B as true.' Such a reader would do wisely in abandoning Euclid, and taking to football."
     The post adds a comma after "say". Not noted.
   - Tortoise: "And might there not also be some reader who would say 'I accept A and B as true,
     but I don't accept the Hypothetical'?" Same, comma added.
   - (C) "If A and B are true, Z must be true." identical. (D) in Carroll reads "If A and B and C
     are true, then Z must be true." The post drops "then" (Achilles's spoken version has no
     "then"). Not noted.
   - Used in notes: "Certainly there might."; "Then I must ask you to accept C."; "And why must
     I?"; "that makes a thousand and one. There are several millions more to come."
   The link in the post (ditext.com) now returns a compressed page; not used.
2. Hofstadter, Gödel, Escher, Bach (1979), preview text at dokumen.pub (`geb_dokumen.txt`),
   section "The Carroll Dialogue Again", p. 192 (chapter VII, "The Propositional Calculus", per
   the contents). Matched: "An excellent exercise for you at this point would be to go back to
   the Carroll Dialogue, and code the various stages of the debate into our notation ... (Hint:
   Whatever Achilles considers a rule of inference, the Tortoise im- mediately flattens into a
   mere string of the system. If you use only the letters A, B, and Z, you will get a recursive
   pattern of longer and longer strings.)" The formulas were lost in text extraction, so the
   post's formula rendering is unchecked. Wikipedia ("What the Tortoise Said to Achilles", raw,
   `wiki_What_the_Tortoise_Said_to_Achilles.txt`) for GEB reprinting Carroll's dialogue as
   "Two-Part Invention".
3. SEP, "Knowledge How" (first published 2021; `sep_knowledge-how.txt`, section 1.4 "Lewis
   Carroll's Regress"). Matched Ryle (1946: 7): "Knowing a rule of inference is not possessing a
   bit of extra information but being able to perform an intelligent operation. Knowing a rule is
   knowing how."
4. Hume, Treatise 2.3.3, Hume Texts Online (https://davidhume.org/texts/t/2/3/3, `hume_t233.txt`):
   "reason alone can never be a motive to any action of the will" (T 2.3.3.1).
5. Bostrom (2012), as in the NUCA report: "belief and motive are separate."
6. SEP, "Moral Motivation" (rev. 2016; `sep_moral-motivation.txt`). Matched: "there is a
   necessary connection between moral judgment and motivation ("weak internalism")"; "the person
   who appears to be making a moral judgment, while remaining unmoved, must really either lack
   competence with moral concepts or be speaking insincerely. In the latter case, she judges an
   act "right" only in an "inverted commas" sense (R. M Hare, 1963)"; "Externalists, of course,
   maintain that the amoralist is not a conceptual impossibility."
7. Blackburn, "Practical Tortoise Raising", Mind 104(416): 695-711, 1995. Bibliographic data from
   Crossref (api.crossref.org/works/10.1093/mind/104.416.695). Content NOT read: OUP, PhilPapers
   and Semantic Scholar gave no abstract. The description "retold Carroll's dialogue about
   action" rests on search-engine summaries (the dialogue form with a Humean tortoise on
   practical reasoning). The note and Response say I could read only summaries.

## 3. Arithmetic

None.

## 4. Claims about other posts

- "A Priori" (`data/originals/a-priori.md`, 2007-10-08): "If a mind doesn't implement Modus
  Ponens, it can accept "A" and "A->B" all day long without ever producing "B"." Our A Priori
  notes credit Carroll and point forward to this post; consistent.
- "No Universally Compelling Arguments" (order 272) is the previous post in the book; "Sorting
  Pebbles Into Correct Heaps" (order 274) the next (manifest). "Passing the Recursive Buck" and
  "Causality and Moral Responsibility" (presumably the target of the "The Buck Stops Immediately" link, an Overcoming Bias URL "causality-and-r";
  resolved via lesswrong.com/lw/ra/) are not in the manifest.

## 5. Not verified

- Blackburn's paper (see 2.7).
- Hofstadter's formula rendering "<{(A⋀B)⋀[(A⋀B)→Z]}→Z>" (no note depends on it).

## 6. Judgment calls

1. The internalism clogic says the fuzzle example, read with moral words, "sides with" the
   externalists. The post uses a nonsense word and is about AI design; I say the practical point
   holds on either side, so this is information about a dispute the post enters by implication,
   not a fault. The brief warns against importing disputes the post does not take a side in; my
   case that it takes one is that the post says belief without the dynamic is "futile", i.e. a
   mind can hold the belief and not act, which is the externalist picture.
2. The Hume, Ryle and Blackburn notes are credit, not faults (the post claims only the phrase
   "created already in motion" as its own).
3. Build: the post text contains U+22C0 (⋀), which annotated/preamble.tex does not declare, so
   `annotated/preview.sh posts created-already-in-motion` fails with "Unicode character ⋀ (U+22C0)
   not set up". I did not edit the preamble (not my file). With one added line,
   `\DeclareUnicodeCharacter{22C0}{\ensuremath{\wedge}}`, the post builds with no errors and no
   overfull boxes (tested with a copy of the preamble in
   `data/sources/5a_my-kind-of-reflection/testbuild/`).
4. Four short paragraphs have no cpara (the lead-ins "...unless the mind also implements:" and
   "Needless to say, having the belief...", and the Next/Previous lines).
5. Pronouns: "his notebook" for Achilles and "it" for the Tortoise follow Carroll.
