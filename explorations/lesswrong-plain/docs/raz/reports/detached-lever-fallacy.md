# Report: detached-lever-fallacy ("Detached Lever Fallacy", Yudkowsky, posted 2008-07-31; book order 267)

## 1. The argument in three sentences (written before annotating)

A word such as "apple" works between people only because it pulls a lever on a large, shared,
invisible machinery of perception and action; writing the word into an AI's knowledge base
(a semantic network) copies the lever without the machinery, like a captain who pries the
dematerializer lever off an alien bridge. The same mistake underlies proposals to make an AI
kind by raising it with loving parents: in humans, culture and upbringing work through
evolved conditional responses, which are more complex than the responses themselves
(the fur coat grown in response to cold), so an AI without that built-in machinery will not
respond to upbringing as a child does. Structuring the right conditional response is itself
the hard problem, harder than programming unconditional niceness, and "learning" and the
"blank slate" hide this.

## 2. Sources checked

Local copies in `data/sources/5a_detached-lever-fallacy/` (scratch scripts: `insert.py`,
`notes_detached.py`, `comments.py`).

1. LessWrong comments on the post, fetched from the GraphQL API (`comments_detached.md`).
   - xSciFix, 2019-06-26: "that sounds pretty much like Star Trek TNG, Season 7 Episode 12. The
     "lever" being the phased cloaking device letting the ships pass through asteroids."
   - RobinHanson, 2008-08-02: "you unfairly slander a generation of AI researchers (which
     included me)"; quotes McDermott "Most AI workers are responsible people ...".
   - Eliezer Yudkowsky, 2008-08-02: "Of course not all past AI researchers made this mistake, but
     a very substantial fraction did so, including leaders of the field."
2. Wikipedia "The Pegasus (Star Trek: The Next Generation)" (raw,
   `wiki_The_Pegasus__Star_Trek__The_Next_Generation_.txt`): "the 12th episode of the seventh
   season"; "Pressman and Riker transport to the Pegasus and recover an experimental device";
   "a prototype for a Federation cloaking device. The device is phase-shifting and as such it
   would allow the Enterprise to travel through the solid matter of the asteroid". A web search
   found no identification of the show beyond this.
3. McDermott, "Artificial Intelligence Meets Natural Stupidity", SIGART Newsletter 57 (1976),
   `data/sources/mcdermott1976.pdf` (already in the repository), text via pdftotext
   (`mcdermott1976_raw.txt`): "3. The notion that a semantic network is semantic." (in a
   numbered list of notions to give up); "Most A! [AI, OCR] workers are responsible people who are
   aware of the pitfalls of a difficult field and produce good work in spite of them. However, to
   say anything good about anyone is beyond the scope of this paper."
4. Wikipedia "Cyc" (raw): "The project began in July 1984"; "Hoping to capture common sense
   knowledge". Wikipedia "Open Mind Common Sense" (raw, `wiki_OMCS.txt`): "ConceptNet is a
   semantic network based on the information in the OMCS database"; "The data structures that make
   up ConceptNet were significantly reorganized in 2007".
5. Harnad, "The Symbol Grounding Problem", arXiv cs/9906002 abstract (`harnad_arxiv.xml`): "How
   can the semantic interpretation of a formal symbol system be made intrinsic to the system,
   rather than just parasitic on the meanings in our heads?"
6. Turing, "Computing Machinery and Intelligence" (1950), PDF from
   https://redirect.cs.umbc.edu/courses/471/papers/turing.pdf (`turing1950.txt`, lines 728-765):
   "Instead of trying to produce a programme to simulate the adult mind, why not rather try to
   produce one which simulates the child's? If this were then subjected to an appropriate course
   of education one would obtain the adult brain. Presumably the child brain is something like a
   notebook as one buys it from the stationer's. Rather little mechanism, and lots of blank
   sheets."; "We have thus divided our problem into two parts. The child programme and the
   education process."; "We cannot expect to find a good child machine at the first attempt. One
   must experiment with teaching one such machine and see how well it learns."; "We normally
   associate punishments and rewards with the teaching process."
7. Wikipedia "Cog (project)" (raw): "It was based on the hypothesis that human-level
   intelligence requires gaining experience from interacting with humans, as human infants do.";
   "As of 2003, all development of the project had ceased."
8. DeWitt, Sih and Wilson, "Costs and limits of phenotypic plasticity", TREE 13 (1998), PubMed
   abstract (`pubmed_dewitt.txt`): "The most commonly discussed cost is that of maintaining the
   sensory and regulatory machinery needed for plasticity, which may require energy and material
   expenses."
9. Wikipedia "Vernalization" (raw): "coined the term ... to describe a chilling process he used to
   make the seeds of winter cereals behave like spring cereals". Wikipedia "Lysenkoism" (raw):
   "In 1928, rejecting natural selection and Mendelian genetics, Trofim Lysenko claimed to have
   developed agricultural techniques ... These included vernalization, species transformation ...,
   inheritance of acquired characteristics".
10. Wikipedia "Language bioprogram theory" (raw): "As articulated mostly by Derek Bickerton";
    Criticism: "Siegel 2007 disputes some of Bickerton's claims about Hawai'i Creole, claiming
    that the linguistic input of the children was not impoverished, since it came from an expanded
    pidgin, not a rudimentary one. Siegel also claims ... the substrate languages (especially
    Cantonese and Portuguese) were a significant source of grammatical features. Siegel also makes
    the point that Hawai'i Creole emerged over two generations, not one." Siegel (2007) itself was
    not read.
11. Wikipedia "Nicaraguan Sign Language" (raw): "Senghas and Coppola determined that child
    learners are creating Nicaraguan Sign Language – they "changed the language as they learned
    it"". Senghas and Coppola (2001) itself was not read.
12. Kaufman and Zigler, "Do abused children become abusive parents?", Am J Orthopsychiatry 1987,
    PubMed abstract (`pubmed_abuse.txt`): "demonstrate that its unqualified acceptance is
    unfounded."
13. Widom, Czaja and DuMont, Science 347 (2015), PubMed abstract (`pubmed_abuse.txt`) and PMC
    full text (`widom2015_pmc.txt`): "Individuals with histories of childhood abuse and neglect
    have higher rates of being reported to CPS for child maltreatment but do not self-report more
    physical and sexual abuse than matched comparisons. Offspring of parents with histories of
    childhood abuse and neglect are more likely to report sexual abuse and neglect ... but
    detection or surveillance bias may account for the greater likelihood of CPS reports."
14. Tooby and Cosmides, "The Psychological Foundations of Culture" (1992), PDF from
    https://www.cep.ucsb.edu/wp-content/uploads/2023/05/pfc92.pdf (`pfc92.txt`, `pfc92_flat.txt`;
    the post's link is dead): "The StandardSocial Science Model breaks the social sciencesinto
    schools(materialist, structural-functionalist, symbolic, Marxist, postmodernist, etc.)" (OCR
    spacing); Table 1.1: "Evoked culture ... domainspecific mechanisms are triggered by local
    circumstances".

## 3. Arithmetic

None in the post. Dates: 1976 (McDermott) to 1990 (Harnad); Cog 1990s to 2003 per Wikipedia.

## 4. Claims about other posts

- "Truly Part of You" (order 48, 2007-11-21) introduced McDermott; its notes quote the same paper.
- "Extensions and Intensions" (order 158) quotes Harnad's abstract ("Chinese/Chinese dictionary").
- "Words as Mental Paintbrush Handles" (order 180): cited by the post; my note only says the post
  cites it for the same point.
- "Artificial Addition" (order 149) names Cyc; no Turing or Cog note there, so the child-machine
  history is given here in full for the first time in book order.

## 5. Not verified

- Siegel (2007), Senghas and Coppola (2001), Bickerton (1981): only via Wikipedia, as the notes say.
- Kaufman and Zigler's rate estimate (often cited as 30 per cent): not in the abstract; not used.
- Pinker's The Blank Slate: not read; the note does not rely on it.
- "An evolutionary psychology of naughtiness based on a notion of testing constraints": I could
  not identify the work meant. Left out of the notes (no fault is claimed).
- The Soviet claims ("scowling posters", "As the Soviets found out, to some small extent"): no
  source checked; described, not assessed.

## 6. Judgment calls

1. Reserved word: "never" appears only in "the author never saw", which is the post's own
   statement ("which I never saw myself").
2. The fur-coat "truism". I considered a note that some environmental effects need no added
   machinery (for example temperature-sensitive coat colour in Siamese cats). I dropped it: the
   post's argument needs only responses that must sense a cue, and the note would be a wording
   point with no consequence (STANDARDS 2.4). The DeWitt note credits the principle instead.
3. I considered a logic note on the a fortiori step ("It's easier to program in unconditional
   niceness ...; If you don't know how to do that, you certainly don't know how ..."), using
   Turing's remark that a learning machine's teacher may be "largely ignorant of quite what is going
   on inside". I dropped it: it enters the general dispute about learned values, which the brief
   says not to import, and the post's reply (structuring the response is the hard part) is in the
   next paragraph.
4. The abuse note (cfact). The claim is an aside, and the note is information, but the post states
   "much higher probability" flatly. Widom et al. is from 2015, after the post; Kaufman and Zigler
   is from before. Both are cited as evidence on the claim, not as something the author should have
   known. The editor may think one source is enough.
5. The creole note is long (five sentences). The post takes a side ("A classic example"), so the
   dispute is not imported; I kept Nicaraguan Sign Language to show that the general point has
   good support.
6. Tooby and Cosmides: the note says the chapter's target is wider than "Marxist academics". I
   first put this in the Response as an overstatement and removed it: the post says "a good many
   Marxist academics", not "only", so it is information, not a fault.
7. Hanson's objection (last-but-one paragraph) is quoted with the author's reply, and with
   McDermott's closing joke, so that Hanson's quotation of McDermott is not read as McDermott's
   whole verdict. "slandered" in the Response and honest n.b. is Hanson's word ("slander").
8. Lysenko is offered as "a close match", not as the case the post meant.
9. Pronouns: a pronoun for Hanson was replaced by the name; the captain in the story keeps "his"
   as in the post.
